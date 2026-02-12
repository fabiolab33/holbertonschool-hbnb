# app/api/places.py
from flask_restx import Namespace, Resource, fields
from flask import request
from flask import current_app

api = Namespace("Places", description="Place operations")

place_model = api.model('Place', {
    'id': fields.String(readonly=True),
    'title': fields.String(required=True),
    'description': fields.String(required=True),
    'price': fields.Float(required=True),
    'latitude': fields.Float(),
    'longitude': fields.Float(),
    'owner_id': fields.String(required=True),
    'amenities': fields.List(fields.String),  # lista de IDs de amenities
})

@api.route("/")
class PlaceList(Resource):
    @api.marshal_list_with(place_model)
    def get(self):
        """List all places"""
        return facade.list_places()

    @api.expect(place_model)
    @api.marshal_with(place_model, code=201)
    def post(self):
        """Create a new place"""
        data = request.json

        # Basic validations
        if data['price'] < 0:
            api.abort(400, "Price must be a positive number")
        if data.get('latitude') is not None and not (-90 <= data['latitude'] <= 90):
            api.abort(400, "Latitude must be between -90 and 90")
        if data.get('longitude') is not None and not (-180 <= data['longitude'] <= 180):
            api.abort(400, "Longitude must be between -180 and 180")

        # Validate that owner exists
        owner = facade.user_repo.get(data['owner_id'])
        if owner is None:
            api.abort(400, "Owner user not found")

        place = facade.create_place(
            title=data['title'],
            description=data['description'],
            price=data['price'],
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            owner_id=data['owner_id']
        )

        # Associate amenities if provided
        amenity_ids = data.get('amenities', [])
        for amenity_id in amenity_ids:
            amenity = facade.amenity_repo.get(amenity_id)
            if amenity:
                place.amenities.append(amenity)

        return place, 201

@api.route("/<string:place_id>")
class PlaceDetail(Resource):
    @api.marshal_with(place_model)
    def get(self, place_id):
        """Retrieve a single place by ID"""
        place = facade.place_repo.get(place_id)
        if place is None:
            api.abort(404, "Place not found")
        return place

    @api.expect(place_model)
    @api.marshal_with(place_model)
    def put(self, place_id):
        """Update an existing place"""
        place = facade.place_repo.get(place_id)
        if place is None:
            api.abort(404, "Place not found")
        data = request.json

        # Basic validations
        if 'price' in data and data['price'] < 0:
            api.abort(400, "Price must be a positive number")
        if 'latitude' in data and not (-90 <= data['latitude'] <= 90):
            api.abort(400, "Latitude must be between -90 and 90")
        if 'longitude' in data and not (-180 <= data['longitude'] <= 180):
            api.abort(400, "Longitude must be between -180 and 180")

        # Update basic attributes
        updated_place = facade.place_repo.update(place_id, **data)

        # Update amenities if provided
        if 'amenities' in data:
            updated_place.amenities = []
            for amenity_id in data['amenities']:
                amenity = facade.amenity_repo.get(amenity_id)
                if amenity:
                    updated_place.amenities.append(amenity)

        return updated_place
