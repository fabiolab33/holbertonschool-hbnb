# app/business/place.py
from app.business.base_model import BaseModel

class Place(BaseModel):
    """Place entity representing a property listing"""

    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        self.title = title
        self.description = description
        self.price = self._validate_price(price)
        self.latitude = self._validate_latitude(latitude) if latitude is not None else None
        self.longitude = self._validate_longitude(longitude) if longitude is not None else None
        self.owner_id = owner_id
        self.reviews = []
        self.amenities = []

    def _validate_price(self, price):
        """Validate that price is positive"""
        if price < 0:
            raise ValueError("Price must be a positive number")
        return price

    def _validate_latitude(self, latitude):
        """Validate latitude is within valid range"""
        if not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        return latitude

    def _validate_longitude(self, longitude):
        """Validate longitude is within valid range"""
        if not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        return longitude

    def add_review(self, review):
        """Add a review to the place"""
        self.reviews.append(review)
        self.save()

    def add_amenity(self, amenity):
        """Add an amenity to the place"""
        if amenity not in self.amenities:
            self.amenities.append(amenity)
            self.save()

    def to_dict(self):
        """Return dictionary representation"""
        data = super().to_dict()
        data.update({
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id
        })
        return data