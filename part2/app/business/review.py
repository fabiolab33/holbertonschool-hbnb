# app/business/review.py
from datetime import datetime

class Review:
    def __init__(self, rating, comment, user_id=None, place_id=None):
        self.id = None
        self.rating = rating
        self.comment = comment
        self.user_id = user_id
        self.place_id = place_id
        self.created_at = None
        self.updated_at = None
