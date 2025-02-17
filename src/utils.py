from http import HTTPStatus
from flask import g, redirect, url_for, request
from flask_jwt_extended import get_jwt_identity
from functools import wraps

from src.models import User, db


def requires_role(role_name):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user_id = get_jwt_identity()
            user = db.get_or_404(User, user_id)
            if user.role.name != role_name:
                return {"message": "User without access"}, HTTPStatus.FORBIDDEN
            return f(*args, **kwargs)
        return wrapped
    return decorator

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

def authorization_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        user_id = get_jwt_identity()
        if not user_id:
            return {"message": "User without access"}, HTTPStatus.FORBIDDEN
        return view(**kwargs)
    return wrapped_view
