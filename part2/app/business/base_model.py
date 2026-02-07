# app/business/base_model.py
# Task 1
import uuid
from datetime import datetime

class BaseModel:
    """Base class that defines common attributes for all entities"""

    def __init__(self):
        self.id = str(uuid.uuid4())        # unique identifier
        self.created_at = datetime.utcnow() # timestamp of creation
        self.updated_at = datetime.utcnow() # timestamp of last update

    def save(self):
        """Update the 'updated_at' timestamp"""
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        """Return a dictionary representation of the instance"""
        return self.__dict__
