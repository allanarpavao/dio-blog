from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models import User, db
from http import HTTPStatus
from sqlalchemy import inspect
from src.utils import requires_role
from src.app import bcrypt
from src.views.user import UserSchema, CreateUserSchema
from marshmallow import ValidationError

# __name__ nome do módulo "user.py"
# padrao restful: nomes no plural
app = Blueprint("user", __name__, url_prefix="/users")


def _create_user():
    user_schema = CreateUserSchema()
    try:
        data = user_schema.load(request.json, many=False)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY

    user = User(
        username=data["username"],
        password=bcrypt.generate_password_hash(data["password"]),
        role_id=data["role_id"],
        )
    db.session.add(user)
    db.session.commit()
    
    return {"message": "User created!"}, HTTPStatus.CREATED

   

@jwt_required()
@requires_role("admin")
def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()

    users_schema = UserSchema(many=True)
    return users_schema.dump(users)
 

@app.route("/", methods=["GET", "POST"])
def list_or_create_user():
    if request.method == "POST":
        return _create_user()
    else:
        return {"users": _list_users()}


@app.route("/<int:user_id>")
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    return {
        "id": user.id,
        "username": user.username,
    }


@app.route("/<int:user_id>", methods=["PATCH", "PUT"])
def update_user(user_id):
    user = db.get_or_404(User, user_id)

    # input por request
    data = request.json

    mapper = inspect(User)  # pega todos os atributos do modelo
    for column in mapper.attrs:
        if column.key in data:
            setattr(user, column.key, data[column.key])

    db.session.commit()

    return {
        "id": user.id,
        "username": user.username,
    }


@app.route("/<int:user_id>", methods=["DELETE"])
def remove_user(user_id):
    user = db.get_or_404(User, user_id)

    db.session.delete(user)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT
