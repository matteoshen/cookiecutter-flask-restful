from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError

from {{cookiecutter.app_name}}.config import VERSION
from {{cookiecutter.app_name}}.extensions import apispec
from {{cookiecutter.app_name}}.api.resources import UserResource, UserList, RoleResource, RoleList
from {{cookiecutter.app_name}}.api.resources.user import UserSchema
from {{cookiecutter.app_name}}.api.resources.role import RoleSchema


blueprint = Blueprint("api", __name__, url_prefix=f"/api/v{VERSION[0]}")
api = Api(blueprint)


api.add_resource(UserResource, "/users/<int:user_id>")
api.add_resource(UserList, "/users")
api.add_resource(RoleResource, "/roles/<int:role_id>")
api.add_resource(RoleList, "/roles")


@blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("UserSchema", schema=UserSchema)
    apispec.spec.path(view=UserResource, app=current_app)
    apispec.spec.path(view=UserList, app=current_app)
    apispec.spec.components.schema("RoleSchema", schema=RoleSchema)
    apispec.spec.path(view=RoleResource, app=current_app)
    apispec.spec.path(view=RoleList, app=current_app)


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marhsmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), 400
