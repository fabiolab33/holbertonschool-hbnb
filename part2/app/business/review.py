# app/business/review.py
from app.business.base_model import BaseModel

class Review(BaseModel):
    """Review entity representing a user review for a place"""

    def __init__(self, rating, comment, user_id, place_id):
        super().__init__()
        self.rating = rating
        self.comment = comment
        self.user_id = user_id    # Task 1 reference to User.id
        self.place_id = place_id  # Task 1 reference to Place.id
