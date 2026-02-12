# app/business/amenity.py
from app.business.base_model import BaseModel

class Amenity(BaseModel):
    """Amenity entity representing a feature of a place"""

    def __init__(self, name, description):
        super().__init__()
        self.name = self._validate_name(name)
        self.description = description

    def _validate_name(self, name):
        """Validate that name is not empty"""
        if not name or not name.strip():
            raise ValueError("Amenity name cannot be empty")
        return name.strip()

    def to_dict(self):
        """Return dictionary representation"""
        data = super().to_dict()
        data.update({
            'name': self.name,
            'description': self.description
        })
        return data