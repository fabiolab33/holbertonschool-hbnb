from flask_restx import Namespace, Resource, fields
from flask import request
from app import facade

api = Namespace("Places", description="Place operations")

place_model = api.model('Place', {
    'id': fields.String(readonly=True),
    'title': fields.String(required=True),
    'description': fields.String(required=True),
    'price': fields.Float(required=True),
    'latitude': fields.Float,
    'longitude': fields.Float,
    'owner_id': fields.String
})

@api.route("/")
class PlaceList(Resource):
    @api.marshal_list_with(place_model)
    def get(self):
        places = facade.list_places()
        result = []
        for p in places:
            result.append({
                'id': p.id,
                'title': p.title,
                'description': p.description,
                'price': p.price,
                'latitude': p.latitude,
                'longitude': p.longitude,
                'owner_id': p.owner_id
            })
        return result

    @api.expect(place_model, validate=True)
    @api.marshal_with(place_model, code=201)
    def post(self):
        data = request.get_json()
        place = facade.create_place(
            title=data.get('title'),
            description=data.get('description'),
            price=data.get('price'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            owner_id=data.get('owner_id')
        )
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner_id': place.owner_id
        }, 201

@api.route("/<string:place_id>")
class PlaceResource(Resource):
    @api.marshal_with(place_model)
    def get(self, place_id):
        place = facade.place_repo.get(place_id)
        if not place:
            api.abort(404, "Place not found")
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner_id': place.owner_id
        }

    @api.expect(place_model, validate=True)
    @api.marshal_with(place_model)
    def put(self, place_id):
        place = facade.place_repo.get(place_id)
        if not place:
            api.abort(404, "Place not found")
        data = request.get_json()
        facade.place_repo.update(
            place_id,
            title=data.get('title', place.title),
            description=data.get('description', place.description),
            price=data.get('price', place.price),
            latitude=data.get('latitude', place.latitude),
            longitude=data.get('longitude', place.longitude),
            owner_id=data.get('owner_id', place.owner_id)
        )
        updated = facade.place_repo.get(place_id)
        return {
            'id': updated.id,
            'title': updated.title,
            'description': updated.description,
            'price': updated.price,
            'latitude': updated.latitude,
            'longitude': updated.longitude,
            'owner_id': updated.owner_id
        }
