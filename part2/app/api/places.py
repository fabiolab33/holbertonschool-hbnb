# app/api/places.py
from flask_restx import Namespace, Resource, fields

api = Namespace("Places", description="Place operations")

place_model = api.model('Place', {
    'id': fields.String(readonly=True),
    'title': fields.String(required=True),
    'description': fields.String(required=True),
    'price': fields.Float(required=True),
})

@api.route("/")
class PlaceList(Resource):
    def get(self):
        return []

    def post(self):
        return {"message": "Place creation endpoint"}, 201
