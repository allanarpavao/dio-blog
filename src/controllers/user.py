from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models import User, db
from http import HTTPStatus
from sqlalchemy import inspect
from src.utils import requires_role
from src.app import bcrypt

# __name__ nome do módulo "user.py"
# padrao restful: nomes no plural
app = Blueprint("user", __name__, url_prefix="/users")


def _create_user():
    data = request.json
    user = User(
        username=data["username"],
        password=bcrypt.generate_password_hash(data["password"]),
        role_id=data["role_id"],
        )

    db.session.add(user)
    db.session.commit()


def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()

    return [
        {
            "id": user.id,
            "username": user.username,
            "role": {
                "id": user.role.id,
                "name": user.role.name
                }
        }
        for user in users
    ]


#  http://127.0.0.1:5000/users/
@app.route("/", methods=["GET", "POST"])
@jwt_required()
@requires_role("admin")
def list_or_create_user():
    if request.method == "POST":
        _create_user()
        return {"message": "User created!"}, HTTPStatus.CREATED
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
