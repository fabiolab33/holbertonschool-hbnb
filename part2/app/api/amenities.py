# app/api/amenities.py
from flask_restx import Namespace, Resource, fields

api = Namespace("Amenities", description="Amenity operations")

amenity_model = api.model('Amenity', {
    'id': fields.String(readonly=True),
    'name': fields.String(required=True),
    'description': fields.String(required=True),
})

@api.route("/")
class AmenityList(Resource):
    def get(self):
        return []

    def post(self):
        return {"message": "Amenity creation endpoint"}, 201
