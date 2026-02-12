# app/api/places.py
from flask_restx import Namespace, Resource, fields
from flask import request

api = Namespace("places", description="Place operations")

# Amenity model (simplified for nested display)
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Amenity name')
})

# Review model (simplified for nested display)
review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'rating': fields.Integer(description='Rating'),
    'comment': fields.String(description='Comment'),
    'user_id': fields.String(description='User ID')
})

# Owner model (for nested display)
owner_model = api.model('PlaceOwner', {
    'id': fields.String(description='Owner ID'),
    'first_name': fields.String(description='Owner first name'),
    'last_name': fields.String(description='Owner last name'),
    'email': fields.String(description='Owner email')
})

# Place model for input
place_input_model = api.model('PlaceInput', {
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(required=True, description='Place description'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(description='Latitude coordinate'),
    'longitude': fields.Float(description='Longitude coordinate'),
    'owner_id': fields.String(required=True, description='Owner user ID'),
    'amenities': fields.List(fields.String, description='List of amenity IDs')
})

# Place model for output (with extended attributes)
place_output_model = api.model('PlaceOutput', {
    'id': fields.String(readonly=True, description='Place unique identifier'),
    'title': fields.String(description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude coordinate'),
    'longitude': fields.Float(description='Longitude coordinate'),
    'owner_id': fields.String(description='Owner user ID'),
    'owner': fields.Nested(owner_model, description='Owner details'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})

def serialize_place(place, facade):
    """Serialize a place with extended attributes"""
    # Get owner details
    owner = facade.get_user(place.owner_id)
    owner_data = {
        'id': owner.id,
        'first_name': owner.first_name,
        'last_name': owner.last_name,
        'email': owner.email
    } if owner else None

    # Get amenities details
    amenities_data = []
    for amenity in place.amenities:
        amenities_data.append({
            'id': amenity.id,
            'name': amenity.name
        })

    # Get reviews details
    reviews_data = []
    for review in place.reviews:
        reviews_data.append({
            'id': review.id,
            'rating': review.rating,
            'comment': review.comment,
            'user_id': review.user_id
        })

    return {
        'id': place.id,
        'title': place.title,
        'description': place.description,
        'price': place.price,
        'latitude': place.latitude,
        'longitude': place.longitude,
        'owner_id': place.owner_id,
        'owner': owner_data,
        'amenities': amenities_data,
        'reviews': reviews_data
    }

@api.route("/")
class PlaceList(Resource):
    @api.doc('list_places')
    @api.marshal_list_with(place_output_model)
    def get(self):
        """List all places with extended attributes"""
        from app import facade
        places = facade.list_places()
        return [serialize_place(place, facade) for place in places]

    @api.doc('create_place')
    @api.expect(place_input_model, validate=True)
    @api.marshal_with(place_output_model, code=201)
    @api.response(201, 'Place created successfully')
    @api.response(400, 'Invalid input')
    @api.response(404, 'Owner not found')
    def post(self):
        """Create a new place"""
        from app import facade
        data = request.get_json()

        try:
            # Create place through facade
            place = facade.create_place(
                title=data['title'],
                description=data['description'],
                price=data['price'],
                latitude=data.get('latitude'),
                longitude=data.get('longitude'),
                owner_id=data['owner_id']
            )

            # Add amenities if provided
            if 'amenities' in data and data['amenities']:
                for amenity_id in data['amenities']:
                    amenity = facade.get_amenity(amenity_id)
                    if amenity:
                        place.add_amenity(amenity)

            return serialize_place(place, facade), 201

        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f"An error occurred: {str(e)}")

@api.route("/<string:place_id>")
@api.param('place_id', 'The place unique identifier')
class PlaceResource(Resource):
    @api.doc('get_place')
    @api.marshal_with(place_output_model)
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get a place by ID with extended attributes"""
        from app import facade
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")
        return serialize_place(place, facade)

    @api.doc('update_place')
    @api.expect(place_input_model, validate=True)
    @api.marshal_with(place_output_model)
    @api.response(200, 'Place updated successfully')
    @api.response(400, 'Invalid input')
    @api.response(404, 'Place not found')
    def put(self, place_id):
        """Update a place"""
        from app import facade
        data = request.get_json()

        try:
            # Check if place exists
            place = facade.get_place(place_id)
            if not place:
                api.abort(404, "Place not found")

            # Update basic attributes
            update_data = {}
            if 'title' in data:
                update_data['title'] = data['title']
            if 'description' in data:
                update_data['description'] = data['description']
            if 'price' in data:
                update_data['price'] = data['price']
            if 'latitude' in data:
                update_data['latitude'] = data['latitude']
            if 'longitude' in data:
                update_data['longitude'] = data['longitude']

            if update_data:
                place = facade.update_place(place_id, **update_data)

            # Update amenities if provided
            if 'amenities' in data:
                place.amenities = []
                for amenity_id in data['amenities']:
                    amenity = facade.get_amenity(amenity_id)
                    if amenity:
                        place.add_amenity(amenity)

            return serialize_place(place, facade)

        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f"An error occurred: {str(e)}")