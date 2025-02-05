from flask import Blueprint, request
from http import HTTPStatus
from flask_jwt_extended import create_access_token
from src.app import bcrypt

from src.models import User, db


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

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    
    query = db.select(User).where(User.username == username)
    user = db.session.execute(query).scalar_one_or_none()
    
    if not user or not _valid_password(user.password, password):
        return {"message": "Bad username or password"}, HTTPStatus.UNAUTHORIZED

    access_token = create_access_token(identity=str(user.id))
    return {'access_token': access_token}
