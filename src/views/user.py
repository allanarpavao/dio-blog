from src.app import ma
from src.views.role import RoleSchema
from marshmallow import fields


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "role")
        ordered = True
        include_fk = True
        load_instance = True
        include_relationships = True
    
    role = ma.Nested(RoleSchema)

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