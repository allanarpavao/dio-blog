from src.app import ma
from marshmallow import fields
from src.models.user import User

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True

class UserIdParameter(ma.Schema):
    user_id = fields.Integer(required=True, strict=True)

    class Meta:
        fields = ("user_id",)
        ordered = True
        load_instance = True
        include_fk = True

class CreateUserSchema(ma.Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    role_id = fields.Integer(required=True, strict=True)

    class Meta:
        fields = ("username", "password", "role_id")
        ordered = True
        load_instance = True
        include_fk = True
        include_relationships = True


class CreateUserSchemaForm(ma.Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)

    class Meta:
        fields = ("username", "password", "role_id")
        ordered = True
        load_instance = True
        include_fk = True
        include_relationships = True
