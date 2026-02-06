# app/api/users.py
from flask_restx import Namespace, Resource, fields

api = Namespace("Users", description="User operations")

user_model = api.model('User', {
    'id': fields.String(readonly=True),
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
})

@api.route("/")
class UserList(Resource):
    def get(self):
        # Placeholder: devuelve lista vacía por ahora
        return []

    def post(self):
        # Placeholder para crear usuario
        return {"message": "User creation endpoint"}, 201
