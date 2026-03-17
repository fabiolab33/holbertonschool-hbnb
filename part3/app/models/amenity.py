"""
Amenity model with SQLAlchemy mapping.
"""
from app import db
from app.models.base import BaseModel


class Amenity(BaseModel):
    """Amenity model for database storage."""
    
    __tablename__ = 'amenities'
    
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(200), nullable=True)
        
    def __init__(self, name, description=None):
        """Initialize amenity."""
        super().__init__()
        self.name = name
        self.description = description
