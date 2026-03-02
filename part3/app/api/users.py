# app/api/users.py
from flask_restx import Namespace, Resource, fields
from flask import request

api = Namespace("users", description="User operations")

# User model for API documentation
user_model = api.model('User', {
    'id': fields.String(readonly=True, description='User unique identifier'),
    'first_name': fields.String(required=True, description='User first name'),
    'last_name': fields.String(required=True, description='User last name'),
    'email': fields.String(required=True, description='User email address'),
    'is_admin': fields.Boolean(description='Admin status', default=False)
})

# User input model (includes password for creation)
user_input_model = api.model('UserInput', {
    'first_name': fields.String(required=True, description='User first name'),
    'last_name': fields.String(required=True, description='User last name'),
    'email': fields.String(required=True, description='User email address'),
    'password': fields.String(required=True, description='User password (will be hashed)')
})

user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='User first name'),
    'last_name': fields.String(description='User last name'),
    'email': fields.String(description='User email address'),
    'password': fields.String(description='New password (will be hashed)')
})

@api.route("/")
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_model)
    def get(self):
        """List all users"""
        from app import facade
        users = facade.list_users()
        return [user.to_dict() for user in users], 200

    @api.doc('create_user')
    @api.expect(user_input_model, validate=True)
    @api.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user"""
        from app import facade

        try:
            data = request.get_json()
              # Validate required fields
            if not data.get('password'):
                return {'message': 'Password is required'}, 400
            
            # Check email uniqueness
            existing_user = facade.get_user_by_email(data['email'])
            if existing_user:
                return {'message': 'Email already registered'}, 400
            
            # Create user (password will be hashed in User.__init__)
            user = facade.create_user(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                password=data['password']  # This will be hashed
            )
            
            # Return user data WITHOUT password
            return user.to_dict(), 201
            
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': f'Error creating user: {str(e)}'}, 500
        
@api.route("/<string:user_id>")
@api.param('user_id', 'The user unique identifier')
class UserResource(Resource):
    @api.doc('get_user')
    @api.marshal_with(user_model)
    def get(self, user_id):
        """Get a user by ID"""
        from app import facade

        user = facade.get_user(user_id)
        if not user:
            return {'message': 'User not found'}, 404

# Password automatically excluded by to_dict()
        return user.to_dict(), 200
    
    @api.doc('update_user')
    @api.expect(user_model, validate=True)
    @api.marshal_with(user_model)
    def put(self, user_id):
        """Update a user"""
        from app import facade

        try:
            user = facade.get_user(user_id)
            if not user:
                return {'message': 'User not found'}, 404
            
            data = request.get_json()

# Check email uniqueness if email is being updated
            if 'email' in data and data['email'] != user.email:
                existing_user = facade.get_user_by_email(data['email'])
                if existing_user:
                    return {'message': 'Email already registered'}, 400
            
            # Update user (password will be hashed if provided)
            updated_user = facade.update_user(user_id, **data)
            
            # Return user data WITHOUT password
            return updated_user.to_dict(), 200
            
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': f'Error updating user: {str(e)}'}, 500

