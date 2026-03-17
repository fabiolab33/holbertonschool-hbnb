"""
Place model with SQLAlchemy mapping.
"""
from app import db
from app.models.base import BaseModel


class Place(BaseModel):
    """Place model for database storage."""
    
    __tablename__ = 'places'
    
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    owner_id = db.Column(db.String(36), nullable=False)
        
    def __init__(self, title, description, price, latitude, longitude, owner_id):
        """Initialize place with validation."""
        super().__init__()
        
        if not title or len(title) > 100:
            raise ValueError("Title must be between 1 and 100 characters")
        
        if price <= 0:
            raise ValueError("Price must be positive")
        
        if latitude is not None and not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        
        if longitude is not None and not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
