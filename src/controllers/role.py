from flask import Blueprint, request
from src.models import db, Role
from http import HTTPStatus

# __name__ nome do módulo "user.py"
# padrao restful: nomes no plural
app = Blueprint("role", __name__, url_prefix="/roles")


@app.route("/", methods=["POST"])
def create_role():
    data = request.json

    role = Role(
        name=data["name"],
        )
    

    db.session.add(role)
    db.session.commit()
    return {"message": "Role created!"}, HTTPStatus.CREATED