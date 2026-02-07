# app/business/amenity.py
# Task 1
from app.business.base_model import BaseModel

class Amenity(BaseModel):
    """Amenity entity representing a feature of a place"""

    def __init__(self, name, description):
        super().__init__()
        self.name = name
        self.description = description
