from marshmallow import fields
from src.models.post import Post
from src.app import ma

class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        include_fk = True

class CreatePostSchema(ma.Schema):
    title = fields.String(required=True)
    body = fields.String(required=True)
    author_id = fields.Integer(required=True, strict=True)

    class Meta:
        fields = ("title", "body", "author_id")
        ordered = True
        load_instance = True
        include_fk = True
        include_relationships = True