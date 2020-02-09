from flask_restful import Resource as _Resource
from flask_jwt_extended import jwt_required
from myapi.decorators import error_handler, role_required
from myapi.config import ADMIN_ROLE_ID


class Resource(_Resource):
    """Resource with error handler, to use as base resource
    """

    method_decorators = [error_handler]


class JWTResource(Resource):
    """Resource require jwt validation, based on ErrorResource
    """

    def __init__(self, **kwargs):
        super(JWTResource, self).__init__(**kwargs)
        self.method_decorators.append(jwt_required)


class AdminResource(Resource):
    """Resource require jwt validation, based on ErrorResource
    """

    def __init__(self, **kwargs):
        super(AdminResource, self).__init__(**kwargs)
        self.method_decorators.append(role_required(ADMIN_ROLE_ID))
