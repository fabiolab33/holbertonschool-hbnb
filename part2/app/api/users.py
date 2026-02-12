from flask_restx import Namespace, Resource, fields
from flask import request
from flask import current_app

api = Namespace("Users", description="User operations")

user_model = api.model('User', {
    'id': fields.String(readonly=True),
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
})

@api.route("/")
class UserList(Resource):
    @api.marshal_list_with(user_model)
    def get(self):
        """Retrieve all users (password omitted)"""
        users = facade.list_users()
        result = []
        for u in users:
            result.append({
                'id': u.id,
                'first_name': u.first_name,
                'last_name': u.last_name,
                'email': u.email
            })
        return result, 200

    @api.expect(user_model, validate=True)
    @api.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user"""
        data = request.get_json()
        user = facade.create_user(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            password=data.get('password', 'default123')  # placeholder password
        )
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 201

@api.route("/<string:user_id>")
class UserResource(Resource):
    @api.marshal_with(user_model)
    def get(self, user_id):
        """Get a user by ID"""
        user = facade.user_repo.get(user_id)
        if not user:
            api.abort(404, "User not found")
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }

    @api.expect(user_model, validate=True)
    @api.marshal_with(user_model)
    def put(self, user_id):
        """Update a user's information"""
        user = facade.user_repo.get(user_id)
        if not user:
            api.abort(404, "User not found")
        data = request.get_json()
        # Update user using business logic
        user.update_profile(
            first_name=data.get('first_name', user.first_name),
            last_name=data.get('last_name', user.last_name),
            email=data.get('email', user.email)
        )
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }
