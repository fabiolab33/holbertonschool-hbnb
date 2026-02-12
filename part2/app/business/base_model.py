# app/business/base_model.py
import uuid
from datetime import datetime

class BaseModel:
    """Base class that defines common attributes for all entities"""

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def save(self):
        """Update the 'updated_at' timestamp"""
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        """Return a dictionary representation of the instance"""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }