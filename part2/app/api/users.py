# app/api/users.py
from flask_restx import Namespace, Resource, fields
from flask import request

api = Namespace("users", description="User operations")

# User model for API documentation
user_model = api.model('User', {
    'id': fields.String(readonly=True, description='User unique identifier'),
    'first_name': fields.String(required=True, description='User first name'),
    'last_name': fields.String(required=True, description='User last name'),
    'email': fields.String(required=True, description='User email address')
})

# User input model (includes password for creation)
user_input_model = api.model('UserInput', {
    'first_name': fields.String(required=True, description='User first name'),
    'last_name': fields.String(required=True, description='User last name'),
    'email': fields.String(required=True, description='User email address'),
    'password': fields.String(required=True, description='User password')
})

@api.route("/")
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_model)
    def get(self):
        """List all users"""
        from app import facade
        users = facade.list_users()
        return users

    @api.doc('create_user')
    @api.expect(user_input_model, validate=True)
    @api.marshal_with(user_model, code=201)
    @api.response(201, 'User created successfully')
    @api.response(400, 'Invalid input or email already exists')
    def post(self):
        """Create a new user"""
        from app import facade
        data = request.get_json()

        try:
            user = facade.create_user(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                password=data['password']
            )
            return user, 201

        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f"An error occurred: {str(e)}")

@api.route("/<string:user_id>")
@api.param('user_id', 'The user unique identifier')
class UserResource(Resource):
    @api.doc('get_user')
    @api.marshal_with(user_model)
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get a user by ID"""
        from app import facade
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")
        return user

    @api.doc('update_user')
    @api.expect(user_model, validate=True)
    @api.marshal_with(user_model)
    @api.response(200, 'User updated successfully')
    @api.response(400, 'Invalid input')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update a user"""
        from app import facade
        data = request.get_json()

        try:
            updated_user = facade.update_user(
                user_id,
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                email=data.get('email')
            )
            return updated_user

        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f"An error occurred: {str(e)}")