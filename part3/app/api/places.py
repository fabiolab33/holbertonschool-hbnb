"""
Places API endpoints with JWT authentication and ownership validation.
"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.business.facade import facade

api = Namespace('places', description='Place operations')

# API Models
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(description='Latitude coordinate'),
    'longitude': fields.Float(description='Longitude coordinate'),
    'owner_id': fields.String(description='Owner user ID'),
})


@api.route('/')
class PlaceList(Resource):
    @api.doc('list_places')
    @jwt_required()
    def get(self):
        """List all places"""
        try:
            places = facade.get_all_places()
            return [place.to_dict() for place in places], 200
        except Exception as e:
            return {'message': f'Error fetching places: {str(e)}'}, 500

    @api.doc('create_place')
    @api.expect(place_model, validate=True)
    @jwt_required()
    def post(self):
        """Create a new place"""
        try:
            current_user_id = get_jwt_identity()
            place_data = api.payload
            place_data['owner_id'] = current_user_id
            
            place = facade.create_place(place_data)
            return place.to_dict(), 201
        except Exception as e:
            return {'message': f'Error creating place: {str(e)}'}, 400

@api.route('/<string:place_id>')
class Place(Resource):
    @api.doc('get_place')
    @jwt_required()
    def get(self, place_id):
        """Get a place by ID"""
        try:
            place = facade.get_place(place_id)
            if not place:
                return {'message': 'Place not found'}, 404
            return place.to_dict(), 200
        except Exception as e:
            return {'message': f'Error: {str(e)}'}, 500
        
    @api.doc('update_place')
    @api.expect(place_model)
    @jwt_required()
    def put(self, place_id):
        """Update a place"""
        try:
            # Get current user from JWT
            current_user_id = get_jwt_identity()
            claims = get_jwt()
            is_admin = claims.get('is_admin', False)

            place = facade.get_place(place_id)
            if not place:
                return {'message': 'Place not found'}, 404
            
            # Check ownership
            if place.owner_id != current_user_id and not is_admin:
                return {'message': 'Unauthorized'}, 403
                                    
            # Update place
            updated_place = facade.update_place(place_id, api.payload)
            return updated_place.to_dict(), 200   
        except Exception as e:
            return {'message': f'Error: {str(e)}'}, 400
        
    @api.doc('delete_place')
    @jwt_required()
    def delete(self, place_id):
        """Delete a place"""
        try:
            # Get current user from JWT
            current_user_id = get_jwt_identity()
            claims = get_jwt()
            is_admin = claims.get('is_admin', False)
            
            place = facade.get_place(place_id)
            if not place:
                return {'message': 'Place not found'}, 404
            
            # Check ownership (or admin)
            if place.owner_id != current_user_id and not is_admin:
                return {'message': 'Unauthorized'}, 403

            facade.delete_place(place_id)           
            return {'message': 'Place deleted successfully'}, 200            
        except Exception as e:
            return {'message': f'Error: {str(e)}'}, 400
