"""
Places API endpoints with JWT authentication and ownership validation.
"""
from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('places', description='Place operations')

# API Models
place_model = api.model('Place', {
    'id': fields.String(readonly=True, description='Place unique identifier'),
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(description='Latitude coordinate'),
    'longitude': fields.Float(description='Longitude coordinate'),
    'owner_id': fields.String(description='Owner user ID'),
    'created_at': fields.String(description='Creation date'),
    'updated_at': fields.String(description='Last update date')
})

place_input_model = api.model('PlaceInput', {
    'title': fields.String(required=True, description='Place title (max 100 chars)'),
    'description': fields.String(required=True, description='Place description'),
    'price': fields.Float(required=True, description='Price per night (must be positive)'),
    'latitude': fields.Float(description='Latitude (-90 to 90)'),
    'longitude': fields.Float(description='Longitude (-180 to 180)'),
    'amenities': fields.List(fields.String, description='List of amenity IDs')
})

place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(description='Place title (max 100 chars)'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(description='Price per night (must be positive)'),
    'latitude': fields.Float(description='Latitude (-90 to 90)'),
    'longitude': fields.Float(description='Longitude (-180 to 180)')
})


@api.route('/')
class PlaceList(Resource):
    @api.doc('list_places')
    @api.marshal_list_with(place_model)
    def get(self):
        """
        List all places (Public endpoint - no authentication required).

        Returns basic place information without related data.
        Use GET /places/{id} to get full details including owner and amenities.
        """
        from app import facade
        places = facade.list_places()
        return [place.to_dict() for place in places], 200

    @api.doc('create_place', security='Bearer Auth')
    @jwt_required()
    @api.expect(place_input_model, validate=True)
    @api.marshal_with(place_model, code=201)
    def post(self):
        """
        Create a new place (Protected endpoint).

        Requirements:
        - User must be authenticated
        - Title is required (max 100 characters)
        - Price must be positive
        - Latitude must be between -90 and 90
        - Longitude must be between -180 and 180
        
        The authenticated user automatically becomes the owner.
        """
        from app import facade
        
        try:
            # Get current user from JWT
            current_user_id = get_jwt_identity()
            data = request.get_json()
            
            # Validate required fields
            if not data.get('title'):
                return {'message': 'Title is required'}, 400
            
            if not data.get('price'):
                return {'message': 'Price is required'}, 400
            
            # Create place with current user as owner
            place = facade.create_place(
                title=data['title'],
                description=data.get('description', ''),
                price=data['price'],
                latitude=data.get('latitude'),
                longitude=data.get('longitude'),
                owner_id=current_user_id  # Authenticated user is the owner
            )
            
            # Add amenities if provided
            if 'amenities' in data and data['amenities']:
                for amenity_id in data['amenities']:
                    amenity = facade.get_amenity(amenity_id)
                    if amenity:
                        place.add_amenity(amenity)
                    else:
                        return {'message': f'Amenity {amenity_id} not found'}, 404
            
            return place.to_dict(), 201
            
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': f'Error creating place: {str(e)}'}, 500


@api.route('/<string:place_id>')
@api.param('place_id', 'The place identifier')
class PlaceResource(Resource):
    @api.doc('get_place')
    def get(self, place_id):
        """
        Get a place information (Public endpoint).
        
        Returns complete place data including:
        - Basic place information
        - Owner details (without password)
        - List of amenities
        - List of reviews
        """
        from app import facade
        
        place = facade.get_place(place_id)
        if not place:
            return {'message': 'Place not found'}, 404
        
        # Return extended place information
        owner = facade.get_user(place.owner_id)
        
        # BUILD RESPONSE WITH RELATED DATA
        place_data = place.to_dict()
        place_data['owner'] = owner.to_dict() if owner else None
        place_data['amenities'] = [amenity.to_dict() for amenity in place.amenities]
        place_data['reviews'] = [review.to_dict() for review in place.reviews]
        
        return place_data, 200

    @api.doc('update_place', security='Bearer Auth')
    @jwt_required()
    @api.expect(place_update_model, validate=True)
    @api.marshal_with(place_model)
    def put(self, place_id):
        """
        Update a place (Protected endpoint).
        Only the owner can update their place.
        """
        from app import facade
        
        try:
            # Get current user from JWT
            current_user_id = get_jwt_identity()
            
            place = facade.get_place(place_id)
            if not place:
                return {'message': 'Place not found'}, 404
            
            # Check ownership
            if place.owner_id != current_user_id:
                return {'message': 'You can only update your own places'}, 403
            
            data = request.get_json()
            
            # Prevent owner_id change
            if 'owner_id' in data:
                return {'message': 'Cannot change place owner'}, 400
            
            # Update place
            updated_place = facade.update_place(place_id, **data)
            return updated_place.to_dict(), 200
            
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': f'Error updating place: {str(e)}'}, 500
