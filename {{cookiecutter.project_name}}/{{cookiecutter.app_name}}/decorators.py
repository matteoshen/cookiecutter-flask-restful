from functools import wraps
from flask_jwt_extended import get_jwt_identity, jwt_required
from werkzeug.exceptions import HTTPException

from {{cookiecutter.app_name}}.models import User
from {{cookiecutter.app_name}}.config import DEBUG
from {{cookiecutter.app_name}}.extensions import db


def role_required(access_role):
    """Allow roles in access_role to access end point
    """

    def _role_required(f):
        @wraps(f)
        @jwt_required
        def decorated(*args, **kwargs):
            current_user_id = get_jwt_identity()
            current_user = db.session.query(User).filter_by(id=current_user_id).first()
            if isinstance(access_role, int):
                if current_user.role_id == access_role:
                    return f(*args, **kwargs)
            elif isinstance(access_role, list):
                if current_user.role_id in access_role:
                    return f(*args, **kwargs)
            else:
                raise ValueError("accees role should be int or list")
            return {"msg": "access denied by role"}, 401

        return decorated

    return _role_required


def error_handler(f):
    """Handle errors
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            if DEBUG:
                raise e
            elif type(e).__bases__[0] == HTTPException:
                return f(*args, **kwargs)
            else:
                return {"msg": type(e).__name__}, 500

    return decorated
