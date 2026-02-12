from flask_restx import Namespace, Resource, fields
from flask import request
from flask import current_app

api = Namespace("Reviews", description="Review operations")

review_model = api.model('Review', {
    'id': fields.String(readonly=True),
    'rating': fields.Integer(required=True),
    'comment': fields.String(required=True),
    'user_id': fields.String,
    'place_id': fields.String
})

@api.route("/")
class ReviewList(Resource):
    @api.marshal_list_with(review_model)
    def get(self):
        reviews = facade.list_reviews()
        result = []
        for r in reviews:
            result.append({
                'id': r.id,
                'rating': r.rating,
                'comment': r.comment,
                'user_id': r.user_id,
                'place_id': r.place_id
            })
        return result

    @api.expect(review_model, validate=True)
    @api.marshal_with(review_model, code=201)
    def post(self):
        data = request.get_json()
        review = facade.create_review(
            rating=data.get('rating'),
            comment=data.get('comment'),
            user_id=data.get('user_id'),
            place_id=data.get('place_id')
        )
        return {
            'id': review.id,
            'rating': review.rating,
            'comment': review.comment,
            'user_id': review.user_id,
            'place_id': review.place_id
        }, 201

@api.route("/<string:review_id>")
class ReviewResource(Resource):
    @api.marshal_with(review_model)
    def get(self, review_id):
        review = facade.review_repo.get(review_id)
        if not review:
            api.abort(404, "Review not found")
        return {
            'id': review.id,
            'rating': review.rating,
            'comment': review.comment,
            'user_id': review.user_id,
            'place_id': review.place_id
        }

    @api.expect(review_model, validate=True)
    @api.marshal_with(review_model)
    def put(self, review_id):
        review = facade.review_repo.get(review_id)
        if not review:
            api.abort(404, "Review not found")
        data = request.get_json()
        facade.review_repo.update(
            review_id,
            rating=data.get('rating', review.rating),
            comment=data.get('comment', review.comment),
            user_id=data.get('user_id', review.user_id),
            place_id=data.get('place_id', review.place_id)
        )
        updated = facade.review_repo.get(review_id)
        return {
            'id': updated.id,
            'rating': updated.rating,
            'comment': updated.comment,
            'user_id': updated.user_id,
            'place_id': updated.place_id
        }
