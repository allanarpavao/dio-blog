from flask import Blueprint, abort, flash, g, redirect, render_template, request, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError
from src.models import Post, db
from http import HTTPStatus
from sqlalchemy import inspect

from src.utils import authorization_required, login_required
from src.views.post import CreatePostSchema


app = Blueprint("blog", __name__)

def _get_post_web(id):
    post = db.session.query(Post).get(id)
    if post is None:
        abort(404, f"Post id {id} doesn't exist.")
    if post.author_id != g.user.id:
        abort(403)
    return post

# routes
@app.route("/", methods=["GET"])
def index():
    posts = db.session.query(Post).all()
    return render_template('blog/index.html', posts=posts)

# create a new post
@jwt_required()
@authorization_required
def _create_blog_post_api():
    input_data = request.json  # Retrieve data internally
    post_schema = CreatePostSchema()
    try:
        data = post_schema.load(input_data, many=False)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY
    
    post = Post(
        title=data["title"],
        body=data["body"],
        author_id=data["author_id"],
        )
    db.session.add(post)
    db.session.commit()
    return {"message": "Post created!"}, HTTPStatus.CREATED

@login_required
def _create_blog_post_web():
    input_data = request.form  # Retrieve data internally
    title = input_data.get("title")
    body = input_data.get("body")
    error = None

    if not title or not body:
        error = "Title and body are required."
    if error is not None:
        flash(error)
    else:
        post = Post(
            title=title,
            body=body,
            author_id=g.user.id,
            )

        db.session.add(post)
        db.session.commit()

@app.route("/create", methods=["POST", "GET"])
def create():
    if request.method == "POST":
        if request.is_json:
            return _create_blog_post_api()
        else:
            _create_blog_post_web()
            return redirect(url_for('blog.index'))
    else:
        return render_template('blog/create.html')
    
# update post
@jwt_required()
@authorization_required
def _update_post_api():
    input_data = request.json
    id = input_data.get('id')
    # user_id = get_jwt_identity()
    post = db.session.query(Post).get(id)
    if post is None:
        return {"message": "Post not found"}, HTTPStatus.NOT_FOUND
    # if post.author_id != user_id:
    #     return {"message": "You are not authorized to edit this post"}, HTTPStatus.FORBIDDEN
    post.title = input_data.get("title")
    post.body = input_data.get("body")
    db.session.commit()
    return {"message": "Post updated!"}, HTTPStatus.OK

@login_required
def _update_post_web():
    input_data = request.form
    id = request.view_args.get('id')
    title = input_data.get("title")
    body = input_data.get("body")
    error = None

    if not title or not body:
        error = "Title and body are required."
    if error is not None:
        flash(error)
    else:
        post = _get_post_web(id)
        post.title = title
        post.body = body
        db.session.commit()

@app.route("/update/<int:id>", methods=["POST", "GET", "PATCH"])
def update(id):
    if request.method == "PATCH":
        return _update_post_api()
    if request.method == "POST":
        post = _get_post_web(id)
        _update_post_web()
        return redirect(url_for('blog.index'))
    post = db.session.query(Post).get(id)
    return render_template('blog/update.html', post=post)


# delete post
@login_required
def _delete_post_web():
    id = request.view_args.get('id')
    post = _get_post_web(id)
    db.session.delete(post)
    db.session.commit()

@jwt_required()
@authorization_required
def _delete_post_api():
    input_data = request.json
    id = input_data.get('id')
    post = db.session.query(Post).get(id)
    if post is None:
        return {"message": "Post not found"}, HTTPStatus.NOT_FOUND

    db.session.delete(post)
    db.session.commit()
    return {"message": "Post deleted!"}, HTTPStatus.OK

@app.route("/delete/<int:id>", methods=["POST", "DELETE"])
def delete(id):
    if request.method == "DELETE":
        return _delete_post_api()
    if request.method == "POST":
        _delete_post_web()
        return redirect(url_for('blog.index'))
