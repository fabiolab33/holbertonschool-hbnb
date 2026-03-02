"""
Authentication endpoints for JWT-based login.
"""
from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

api = Namespace('auth', description='Authentication operations')

# API Models
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email address'),
    'password': fields.String(required=True, description='User password')
})

token_response_model = api.model('TokenResponse', {
    'access_token': fields.String(description='JWT access token'),
    'user': fields.Nested(api.model('UserInfo', {
        'id': fields.String(description='User ID'),
        'email': fields.String(description='User email'),
        'first_name': fields.String(description='User first name'),
        'last_name': fields.String(description='User last name'),
        'is_admin': fields.Boolean(description='Admin status')
    }))
})


@api.route('/login')
class Login(Resource):
    @api.doc('user_login')
    @api.expect(login_model, validate=True)
    @api.response(200, 'Login successful', token_response_model)
    @api.response(400, 'Invalid credentials')
    @api.response(401, 'Unauthorized')
    def post(self):
        """
        Authenticate user and return JWT token.
        
        Returns JWT access token if credentials are valid.
        Token includes user identity and is_admin claim.
        """
        from app import facade
        
        try:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
            
            # Validate input
            if not email or not password:
                return {'message': 'Email and password are required'}, 400
            
            # Get user by email
            user = facade.get_user_by_email(email)
            if not user:
                return {'message': 'Invalid credentials'}, 401
            
            # Verify password
            if not user.verify_password(password):
                return {'message': 'Invalid credentials'}, 401
            
            # Create JWT token with additional claims
            additional_claims = {
                'is_admin': user.is_admin
            }
            access_token = create_access_token(
                identity=user.id,
                additional_claims=additional_claims
            )
            
            # Return token and user info (without password)
            return {
                'access_token': access_token,
                'user': user.to_dict()
            }, 200
            
        except Exception as e:
            return {'message': f'Login error: {str(e)}'}, 500


@api.route('/protected')
class ProtectedResource(Resource):
    @api.doc('protected_endpoint', security='Bearer Auth')
    @jwt_required()
    def get(self):
        """
        Example protected endpoint.
        Requires valid JWT token in Authorization header.
        
        Headers:
            Authorization: Bearer <access_token>
        """
        current_user_id = get_jwt_identity()
        return {
            'message': 'This is a protected endpoint',
            'user_id': current_user_id
        }, 200