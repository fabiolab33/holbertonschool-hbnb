# app/business/place.py
from datetime import datetime

class Place:
    def __init__(self, title, description, price, latitude=None, longitude=None):
        self.id = None
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.created_at = None
        self.updated_at = None
