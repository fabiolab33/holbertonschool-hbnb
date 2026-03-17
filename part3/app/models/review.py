"""
Review model with SQLAlchemy mapping.
"""
from app import db
from app.models.base import BaseModel


class Review(BaseModel):
    """Review model for database storage."""
    
    __tablename__ = 'reviews'
    
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    
    def __init__(self, rating, comment, user_id, place_id):
        """Initialize review with validation."""
        super().__init__()
        
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        
        if not comment:
            raise ValueError("Comment is required")
        
        self.rating = rating
        self.comment = comment
        self.user_id = user_id
        self.place_id = place_id
