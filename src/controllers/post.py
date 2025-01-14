from flask import Blueprint, request
from src.app import Post, db
from http import HTTPStatus
from sqlalchemy import inspect


# __name__ nome do módulo "user.py"
# padrao restful: nomes no plural
app = Blueprint("post", __name__, url_prefix="/posts")


def _create_blog_post():
    data = request.json
    blog = Post(title=data["title"], body=data["body"], author_id=data["author_id"])
    db.session.add(blog)
    db.session.commit()


#  http://127.0.0.1:5000/posts/
@app.route("/", methods=["GET", "POST"])
def create_or_list_blog_post():
    if request.method == "POST":
        _create_blog_post()
        return {"message": "Post created!"}, HTTPStatus.CREATED
    else:
        return "vazio"
