from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from flask import Blueprint, flash, get_flashed_messages, redirect, render_template, request, session, url_for
from http import HTTPStatus
from flask_jwt_extended import create_access_token
from src.app import bcrypt
from flask import g

from src.models import User, db
from src.views.user import CreateUserSchemaForm


app = Blueprint("auth", __name__, url_prefix="/auth")

def _valid_password(password_hash, password_raw):
    """
    Check if the provided raw password matches the hashed password.

    Args:
        password_hash (str): The hashed password stored in the database.
        password_raw (str): The raw password input by the user.

    Returns:
        bool: True if the raw password matches the hashed password, False otherwise.
    """
    return bcrypt.check_password_hash(password_hash, password_raw)


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        user_schema = CreateUserSchemaForm()
        error = None

        # check if request is form 
        try:
            data = user_schema.load(request.form, many=False)
        except ValidationError as exc:
            error = exc.messages
            flash(error)
        else:
            username = data["username"]
            password = data["password"]
            user = User(
                username=username,
                password=bcrypt.generate_password_hash(password),
                role_id=2,
            )

            # check if username already exists
            try:
                db.session.add(user)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                error = f"User {username} is already registered."
                flash(error)
            else:
                return redirect(url_for("auth.login"))
    return render_template('auth/register.html')


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        # JSON data
        if request.is_json:
            username = request.json.get("username", None)
            password = request.json.get("password", None)
            
            query = db.select(User).where(User.username == username)
            user = db.session.execute(query).scalar_one_or_none()

            if not user or not _valid_password(user.password, password):
                return {"message": "Bad username or password"}, HTTPStatus.UNAUTHORIZED
            
            access_token = create_access_token(identity=str(user.id))
            return {'access_token': access_token}
        
        # Form data
        else:
            username = request.form.get("username", None)
            password = request.form.get("password", None)

        query = db.select(User).where(User.username == username)
        user = db.session.execute(query).scalar_one_or_none()

        if not user or not _valid_password(user.password, password):
            return {"message": "Bad username or password"}, HTTPStatus.UNAUTHORIZED

        session.clear()
        session["user_id"] = user.id
        return redirect(url_for('index'))
    
    return render_template('auth/login.html')

@app.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        query = db.select(User).where(User.id == user_id)
        g.user = db.session.execute(query).scalar_one_or_none()

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
