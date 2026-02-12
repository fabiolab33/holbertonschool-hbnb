# app/business/review.py
from app.business.base_model import BaseModel

class Review(BaseModel):
    """Review entity representing a user review for a place"""

    def __init__(self, rating, comment, user_id, place_id):
        super().__init__()
        self.rating = self._validate_rating(rating)
        self.comment = self._validate_comment(comment)
        self.user_id = user_id
        self.place_id = place_id

    def _validate_rating(self, rating):
        """Validate that rating is between 1 and 5"""
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")
        return rating

    def _validate_comment(self, comment):
        """Validate that comment is not empty"""
        if not comment or not comment.strip():
            raise ValueError("Comment cannot be empty")
        return comment.strip()

    def to_dict(self):
        """Return dictionary representation"""
        data = super().to_dict()
        data.update({
            'rating': self.rating,
            'comment': self.comment,
            'user_id': self.user_id,
            'place_id': self.place_id
        })
        return data