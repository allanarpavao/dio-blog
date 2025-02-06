import os
from flask import Flask, request
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from src.models import db
from flask import json
from werkzeug.exceptions import HTTPException
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask_swagger_ui import get_swaggerui_blueprint


migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()
ma = Marshmallow()

spec = APISpec(
    title="DIO Bank",
    version="1.0.0",
    openapi_version="3.0.3",
    info=dict(description="DIO Bank API"),
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

def create_app(environment=os.environ['ENVIRONMENT']):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(f"src.config.{environment.title()}Config")

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    ma.init_app(app)

    # register blueprints
    from src.controllers import user, post, auth, role
    app.register_blueprint(user.app)
    app.register_blueprint(post.app)
    app.register_blueprint(auth.app)
    app.register_blueprint(role.app)

    # Adiciona as rotas ao APISpec
    with app.test_request_context():
        spec.path(view=user.get_user)
        spec.path(view=user.update_user)
        spec.path(view=user.delete_user)

    # Rota para retornar JSON da especificação OpenAPI
    @app.route("/swagger.json")
    def swagger_spec():
        return spec.to_dict()

    # Configuração do Swagger UI
    SWAGGER_URL = '/docs'  # Rota para acessar o Swagger UI
    API_URL = '/swagger.json'  # Rota que retorna a especificação OpenAPI em JSON

    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "DIO Bank API"}
    )
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """Return JSON instead of HTML for HTTP errors."""
        # start with the correct headers and status code from the error
        response = e.get_response()
        # replace the body with JSON
        response.data = json.dumps({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        })
        response.content_type = "application/json"
        return response

    return app
