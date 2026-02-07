# app/business/place.py
from app.business.base_model import BaseModel

class Place(BaseModel):
        """Place entity representing a property listing"""
        
        def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id  # Task 1 reference to User.id
        self.reviews = []         # Task 1 list of Review
        self.amenities = []       # Task 1 list of Amenity
