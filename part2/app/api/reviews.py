# app/api/reviews.py
from flask_restx import Namespace, Resource, fields

api = Namespace("Reviews", description="Review operations")

review_model = api.model('Review', {
    'id': fields.String(readonly=True),
    'rating': fields.Integer(required=True),
    'comment': fields.String(required=True),
})

@api.route("/")
class ReviewList(Resource):
    def get(self):
        return []

    def post(self):
        return {"message": "Review creation endpoint"}, 201
