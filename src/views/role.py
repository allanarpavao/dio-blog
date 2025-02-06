from src.app import ma
from src.models.role import Role

class RoleSchema(ma.Schema):
    class Meta:
        fields = ("id", "name")
        ordered = True
        include_fk = True
        load_instance = True
        include_relationships = True