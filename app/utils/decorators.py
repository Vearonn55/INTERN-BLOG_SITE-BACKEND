# app/utils/decorators.py
from functools import wraps
from flask import g, abort
from flask_jwt_extended import get_jwt_identity
from app.engine import get_session
from app.crud.user import get_user_by_id

def with_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with next(get_session()) as session:
            g.session = session
            return func(*args, **kwargs)
    return wrapper

def admin_required(func):
    @wraps(func)
    @with_session
    def wrapper(*args, **kwargs):
        user_id = int(get_jwt_identity())
        user = get_user_by_id(g.session, user_id)
        if not user or user.role != "admin":
            abort(403, description="Admin privileges required")
        return func(*args, **kwargs)
    return wrapper
