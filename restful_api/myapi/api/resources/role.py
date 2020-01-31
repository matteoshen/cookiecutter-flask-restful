from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from myapi.models import Role
from myapi.extensions import ma, db
from myapi.commons.pagination import paginate


class RoleSchema(ma.ModelSchema):

    id = ma.Int(dump_only=True)

    class Meta:
        model = Role
        sqla_session = db.session


class RoleResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - api
      parameters:
        - in: path
          name: role_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  role: RoleSchema
        404:
          description: role does not exists
    put:
      tags:
        - api
      parameters:
        - in: path
          name: role_id
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema:
              RoleSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: role updated
                  role: RoleSchema
        404:
          description: role does not exists
    delete:
      tags:
        - api
      parameters:
        - in: path
          name: role_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: role deleted
        404:
          description: role does not exists
    """

    method_decorators = [jwt_required]

    def get(self, role_id):
        schema = RoleSchema()
        role = Role.query.get_or_404(role_id)
        return {"role": schema.dump(role)}

    def put(self, role_id):
        schema = RoleSchema(partial=True)
        role = Role.query.get_or_404(role_id)
        role = schema.load(request.json, instance=role)

        db.session.commit()

        return {"msg": "role updated", "role": schema.dump(role)}

    def delete(self, role_id):
        role = Role.query.get_or_404(role_id)
        db.session.delete(role)
        db.session.commit()

        return {"msg": "role deleted"}


class RoleList(Resource):
    """Creation and get_all

    ---
    get:
      tags:
        - api
      responses:
        200:
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/PaginatedResult'
                  - type: object
                    properties:
                      results:
                        type: array
                        items:
                          $ref: '#/components/schemas/RoleSchema'
    post:
      tags:
        - api
      requestBody:
        content:
          application/json:
            schema:
              RoleSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: role created
                  role: RoleSchema
    """

    method_decorators = [jwt_required]

    def get(self):
        schema = RoleSchema(many=True)
        query = Role.query
        return paginate(query, schema)

    def post(self):
        schema = RoleSchema()
        role = schema.load(request.json)

        db.session.add(role)
        db.session.commit()

        return {"msg": "role created", "role": schema.dump(role)}, 201
