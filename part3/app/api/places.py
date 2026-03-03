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
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(required=True, description='Place description'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(description='Latitude coordinate'),
    'longitude': fields.Float(description='Longitude coordinate'),
    'amenities': fields.List(fields.String, description='List of amenity IDs')
})

place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude coordinate'),
    'longitude': fields.Float(description='Longitude coordinate')
})


@api.route('/')
class PlaceList(Resource):
    @api.doc('list_places')
    @api.marshal_list_with(place_model)
    def get(self):
        """
        List all places (Public endpoint - no authentication required).
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
        Only authenticated users can create places.
        The authenticated user becomes the owner.
        """
        from app import facade
        
        try:
            # Get current user from JWT
            current_user_id = get_jwt_identity()
            
            data = request.get_json()
            
            # Create place with current user as owner
            place = facade.create_place(
                title=data['title'],
                description=data['description'],
                price=data['price'],
                latitude=data.get('latitude'),
                longitude=data.get('longitude'),
                owner_id=current_user_id  # Authenticated user is the owner
            )
            
            # Add amenities if provided
            if 'amenities' in data:
                for amenity_id in data['amenities']:
                    amenity = facade.get_amenity(amenity_id)
                    if amenity:
                        place.add_amenity(amenity)
            
            return place.to_dict(), 201
            
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': f'Error creating place: {str(e)}'}, 500


@api.route('/<string:place_id>')
@api.param('place_id', 'The place identifier')
class PlaceResource(Resource):
    @api.doc('get_place')
    @api.marshal_with(place_model)
    def get(self, place_id):
        """
        Get a place by ID (Public endpoint - no authentication required).
        Returns place with extended attributes (owner, amenities, reviews).
        """
        from app import facade
        
        place = facade.get_place(place_id)
        if not place:
            return {'message': 'Place not found'}, 404
        
        # Return extended place information
        owner = facade.get_user(place.owner_id)
        
        place_data = place.to_dict()
        place_data['owner'] = owner.to_dict() if owner else None
        place_data['amenities'] = [a.to_dict() for a in place.amenities]
        place_data['reviews'] = [r.to_dict() for r in place.reviews]
        
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
            
            # Update place
            updated_place = facade.update_place(place_id, **data)
            return updated_place.to_dict(), 200
            
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': f'Error updating place: {str(e)}'}, 500

    @api.doc('delete_place', security='Bearer Auth')
    @jwt_required()
    def delete(self, place_id):
        """
        Delete a place (Protected endpoint).
        Only the owner or admin can delete a place.
        """
        from app import facade
        
        try:
            # Get current user from JWT
            current_user_id = get_jwt_identity()
            claims = get_jwt()
            is_admin = claims.get('is_admin', False)
            
            place = facade.get_place(place_id)
            if not place:
                return {'message': 'Place not found'}, 404
            
            # Check ownership or admin status
            if place.owner_id != current_user_id and not is_admin:
                return {'message': 'You can only delete your own places'}, 403
            
            # Delete place (implement in facade)
            # Note: This will be implemented when we add delete_place to facade
            return {'message': 'Place deletion not yet implemented'}, 501
            
        except Exception as e:
            return {'message': f'Error deleting place: {str(e)}'}, 500
