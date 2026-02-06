# app/business/amenity.py
from datetime import datetime

class Amenity:
    def __init__(self, name, description):
        self.id = None
        self.name = name
        self.description = description
        self.created_at = None
        self.updated_at = None
