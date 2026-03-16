# app/api/amenities.py
from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt

api = Namespace("amenities", description="Amenity operations")

# Amenity model for API documentation
amenity_model = api.model('Amenity', {
    'id': fields.String(readonly=True, description='Amenity unique identifier'),
    'name': fields.String(required=True, description='Amenity name'),
    'description': fields.String(required=True, description='Amenity description')
})

@api.route("/")
class AmenityList(Resource):
    @api.doc('list_amenities')
    @api.marshal_list_with(amenity_model)
    def get(self):
        """List all amenities"""
        from app import facade
        amenities = facade.list_amenities()
        return amenities, 200

    @api.doc('create_amenity', security='Bearer Auth')
    @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.marshal_with(amenity_model, code=201)
    @api.response(201, 'Amenity created successfully')
    @api.response(400, 'Invalid input')
    @api.response(403, 'Admin access required')
    def post(self):
        """Create a new amenity"""
        from app import facade

        # Check if user is admin
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        if not is_admin:
            return {'message': 'Admin privileges required'}, 403
        
        data = request.get_json()

        try:
            amenity = facade.create_amenity(
                name=data['name'],
                description=data['description']
            )
            return amenity, 201

        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f"An error occurred: {str(e)}")

@api.route("/<string:amenity_id>")
@api.param('amenity_id', 'The amenity unique identifier')
class AmenityResource(Resource):
    @api.doc('get_amenity')
    @api.marshal_with(amenity_model)
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get an amenity by ID"""
        from app import facade
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        return amenity

    @api.doc('update_amenity', security='Bearer Auth')
    @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.marshal_with(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(400, 'Invalid input')
    @api.response(403, 'Admin access required')
    @api.response(404, 'Amenity not found')
    def put(self, amenity_id):
        """Update an amenity"""
        from app import facade

        # Check if user is admin
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        if not is_admin:
            return {'message': 'Admin privileges required'}, 403
        
        data = request.get_json()

        try:
            updated_amenity = facade.update_amenity(
                amenity_id,
                name=data.get('name'),
                description=data.get('description')
            )
            return updated_amenity

        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f"An error occurred: {str(e)}")