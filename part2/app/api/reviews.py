# app/api/reviews.py
from flask_restx import Namespace, Resource, fields
from flask import request

api = Namespace("reviews", description="Review operations")

# Review model for API documentation
review_model = api.model('Review', {
    'id': fields.String(readonly=True, description='Review unique identifier'),
    'rating': fields.Integer(required=True, description='Rating from 1 to 5', min=1, max=5),
    'comment': fields.String(required=True, description='Review comment text'),
    'user_id': fields.String(required=True, description='ID of the user who wrote the review'),
    'place_id': fields.String(required=True, description='ID of the place being reviewed')
})

@api.route("/")
class ReviewList(Resource):
    @api.doc('list_reviews')
    @api.marshal_list_with(review_model)
    def get(self):
        """List all reviews"""
        from app import facade
        reviews = facade.list_reviews()
        return reviews

    @api.doc('create_review')
    @api.expect(review_model, validate=True)
    @api.marshal_with(review_model, code=201)
    @api.response(201, 'Review created successfully')
    @api.response(400, 'Invalid input')
    @api.response(404, 'User or Place not found')
    def post(self):
        """Create a new review"""
        from app import facade
        data = request.get_json()

        try:
            # Validate required fields
            if 'rating' not in data or 'comment' not in data or 'user_id' not in data or 'place_id' not in data:
                api.abort(400, "Missing required fields: rating, comment, user_id, place_id")

            # Create review through facade
            review = facade.create_review(
                rating=data['rating'],
                comment=data['comment'],
                user_id=data['user_id'],
                place_id=data['place_id']
            )
            return review, 201

        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f"An error occurred: {str(e)}")

@api.route("/<string:review_id>")
@api.param('review_id', 'The review unique identifier')
class ReviewResource(Resource):
    @api.doc('get_review')
    @api.marshal_with(review_model)
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get a review by ID"""
        from app import facade
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")
        return review

    @api.doc('update_review')
    @api.expect(review_model, validate=True)
    @api.marshal_with(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(400, 'Invalid input')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        """Update a review"""
        from app import facade
        data = request.get_json()

        try:
            # Check if review exists
            review = facade.get_review(review_id)
            if not review:
                api.abort(404, "Review not found")

            # Update review through facade
            updated_review = facade.update_review(
                review_id,
                rating=data.get('rating', review.rating),
                comment=data.get('comment', review.comment)
            )
            return updated_review

        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f"An error occurred: {str(e)}")

    @api.doc('delete_review')
    @api.response(204, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        from app import facade
        
        try:
            # Check if review exists
            review = facade.get_review(review_id)
            if not review:
                api.abort(404, "Review not found")

            # Delete review through facade
            facade.delete_review(review_id)
            return '', 204

        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f"An error occurred: {str(e)}")

@api.route("/places/<string:place_id>/reviews")
@api.param('place_id', 'The place unique identifier')
class PlaceReviewList(Resource):
    @api.doc('get_place_reviews')
    @api.marshal_list_with(review_model)
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        from app import facade
        
        try:
            reviews = facade.get_reviews_by_place(place_id)
            return reviews
        except ValueError as e:
            api.abort(404, str(e))
        except Exception as e:
            api.abort(500, f"An error occurred: {str(e)}")