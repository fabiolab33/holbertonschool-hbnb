# app/api/reviews.py
from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import get_jwt, jwt_required, get_jwt_identity

api = Namespace("reviews", description="Review operations")

# Review model for API documentation
review_model = api.model('Review', {
    'id': fields.String(readonly=True, description='Review unique identifier'),
    'rating': fields.Integer(required=True, description='Rating from (1-5)'),
    'comment': fields.String(required=True, description='Review comment'),
    'user_id': fields.String(description='User ID of'),
    'place_id': fields.String(description='Place ID'),
    'created_at': fields.String(description='Creation date'),
    'updated_at': fields.String(description='Last update date')
})

review_input_model = api.model('ReviewInput', {
    'rating': fields.Integer(required=True, description='Rating (1-5)', min=1, max=5),
    'comment': fields.String(required=True, description='Review comment'),
    'place_id': fields.String(required=True, description='Place ID')
})

review_update_model = api.model('ReviewUpdate', {
    'rating': fields.Integer(description='Rating (1-5)', min=1, max=5),
    'comment': fields.String(description='Review comment')
})


@api.route("/")
class ReviewList(Resource):
    @api.doc('list_reviews')
    @api.marshal_list_with(review_model)
    def get(self):
        """List all reviews"""
        from app import facade
        reviews = facade.list_reviews()
        return [review.to_dict() for review in reviews], 200

    @api.doc('create_review', security='Bearer Auth')
    @jwt_required()
    @api.expect(review_input_model, validate=True)
    @api.marshal_with(review_model, code=201)
    def post(self):
        """Create a new review"""
        from app import facade

        try:
            # Get current user from JWT
            current_user_id = get_jwt_identity()
            
            data = request.get_json()
            place_id = data['place_id']
            
            # Check if place exists
            place = facade.get_place(place_id)
            if not place:
                return {'message': 'Place not found'}, 404
            
            # Check if user is trying to review their own place
            if place.owner_id == current_user_id:
                return {'message': 'You cannot review your own place'}, 400
            
            # Check if user has already reviewed this place
            existing_reviews = facade.get_reviews_by_place(place_id)
            for review in existing_reviews:
                if review.user_id == current_user_id:
                    return {'message': 'You have already reviewed this place'}, 400
            
            # Create review
            review = facade.create_review(
                rating=data['rating'],
                comment=data['comment'],
                user_id=current_user_id,
                place_id=place_id
            )
            
            return review.to_dict(), 201

        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': f'Error creating review: {str(e)}'}, 500

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
            return {'message': 'Review not found'}, 404
        
        return review.to_dict(), 200

    @api.doc('update_review', security='Bearer Auth')
    @jwt_required()
    @api.expect(review_model, validate=True)
    @api.marshal_with(review_model)
    def put(self, review_id):
        """Update a review"""
        from app import facade
        data = request.get_json()

        try:
            # Get current user from JWT
            current_user_id = get_jwt_identity()
            claims = get_jwt()
            is_admin = claims.get('is_admin', False)

            # Check if review exists
            review = facade.get_review(review_id)
            if not review:
                return {'message': 'Review not found'}, 404

            # Check ownership
            if review.user_id != current_user_id and not is_admin:
                return {'message': 'You can only update your own reviews'}, 403
            
            data = request.get_json()
            
            # Update review
            updated_review = facade.update_review(review_id, **data)
            return updated_review.to_dict(), 200

        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': f'Error updating review: {str(e)}'}, 500

    @api.doc('delete_review', security='Bearer Auth')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        from app import facade
        
        try:
             # Get current user from JWT
            current_user_id = get_jwt_identity()
            claims = get_jwt()
            is_admin = claims.get('is_admin', False)

            # Check if review exists
            review = facade.get_review(review_id)
            if not review:
                return {'message': 'Review not found'}, 404

            # Check ownership
            if review.user_id != current_user_id and not is_admin:
                return {'message': 'You can only delete your own reviews'}, 403

            # Delete review through facade
            facade.delete_review(review_id)
            return '', 204

        except ValueError as e:
            return {'message': f'Error deleting review: {str(e)}'}, 500

@api.route("/places/<string:place_id>/reviews")
@api.param('place_id', 'The place unique identifier')
class PlaceReviewList(Resource):
    @api.doc('get_place_reviews')
    @api.marshal_list_with(review_model)
    def get(self, place_id):
        """Get all reviews for a specific place"""
        from app import facade
        
        place = facade.get_place(place_id)
        if not place:
            return {'message': 'Place not found'}, 404

        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:
            return [], 200
        
        return [review.to_dict() for review in reviews], 200