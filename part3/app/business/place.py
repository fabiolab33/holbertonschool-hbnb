# app/business/place.py
from app.business.base_model import BaseModel

class Place(BaseModel):
    """Place entity representing a property listing"""

    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        self.title = self._validate_title(title)
        self.description = description
        self.price = self._validate_price(price)
        self.latitude = self._validate_latitude(latitude)
        self.longitude = self._validate_longitude(longitude)
        self.owner_id = owner_id
        self.reviews = []
        self.amenities = []
    
    def _validate_title(self, title):
        """Validate place title."""
        if not title or len(title.strip()) == 0:
            raise ValueError("Title cannot be empty")
        if len(title) > 100:
            raise ValueError("Title cannot exceed 100 characters")
        return title.strip()

    def _validate_price(self, price):
        """Validate that price is positive"""
        try:
            price = float(price)
            if price <= 0:
                raise ValueError("Price must be a positive value")
            return price
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid price: {price}")

    def _validate_latitude(self, latitude):
        """Validate latitude is between -90 and 90."""
        if latitude is None:
            return None
        
        try:
            latitude = float(latitude)
            if latitude < -90 or latitude > 90:
                raise ValueError("Latitude must be between -90 and 90")
            return latitude
        except (TypeError, ValueError):
            raise ValueError(f"Invalid latitude: {latitude}")

    def _validate_longitude(self, longitude):
        """Validate longitude is between -180 and 180"""
        if longitude is None:
            return None
        
        try:
            longitude = float(longitude)
            if longitude < -180 or longitude > 180:
                raise ValueError("Longitude must be between -180 and 180")
            return longitude
        except (TypeError, ValueError):
            raise ValueError(f"Invalid longitude: {longitude}")

    def add_amenity(self, amenity):
        """Add an amenity to the place"""
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def remove_amenity(self, amenity):
        """Remove an amenity from the place."""
        if amenity in self.amenities:
            self.amenities.remove(amenity)

    def add_review(self, review):
        """Add a review to the place"""
        self.reviews.append(review)
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