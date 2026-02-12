from flask_restx import Namespace, Resource, fields
from flask import request
from flask import current_app

api = Namespace("Amenities", description="Amenity operations")

amenity_model = api.model('Amenity', {
    'id': fields.String(readonly=True),
    'name': fields.String(required=True),
    'description': fields.String(required=True),
})

@api.route("/")
class AmenityList(Resource):
    @api.marshal_list_with(amenity_model)
    def get(self):
        amenities = facade.list_amenities()
        result = []
        for a in amenities:
            result.append({
                'id': a.id,
                'name': a.name,
                'description': a.description
            })
        return result

    @api.expect(amenity_model, validate=True)
    @api.marshal_with(amenity_model, code=201)
    def post(self):
        data = request.get_json()
        amenity = facade.create_amenity(
            name=data.get('name'),
            description=data.get('description')
        )
        return {
            'id': amenity.id,
            'name': amenity.name,
            'description': amenity.description
        }, 201

@api.route("/<string:amenity_id>")
class AmenityResource(Resource):
    @api.marshal_with(amenity_model)
    def get(self, amenity_id):
        amenity = facade.amenity_repo.get(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        return {
            'id': amenity.id,
            'name': amenity.name,
            'description': amenity.description
        }

    @api.expect(amenity_model, validate=True)
    @api.marshal_with(amenity_model)
    def put(self, amenity_id):
        amenity = facade.amenity_repo.get(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        data = request.get_json()
        facade.amenity_repo.update(
            amenity_id,
            name=data.get('name', amenity.name),
            description=data.get('description', amenity.description)
        )
        updated = facade.amenity_repo.get(amenity_id)
        return {
            'id': updated.id,
            'name': updated.name,
            'description': updated.description
        }
