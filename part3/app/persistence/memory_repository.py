# app/persistence/memory_repository.py
import uuid
from datetime import datetime

class InMemoryRepository:
    """In-memory repository for storing entities"""

    def __init__(self):
        self.storage = {}

    def create(self, obj):
        """Add a new object to the repository"""
        if not hasattr(obj, 'id'):
            obj.id = str(uuid.uuid4())
        if not hasattr(obj, 'created_at'):
            obj.created_at = datetime.utcnow()
        if not hasattr(obj, 'updated_at'):
            obj.updated_at = datetime.utcnow()
        
        self.storage[obj.id] = obj
        return obj

    def get(self, obj_id):
        """Retrieve an object by ID"""
        return self.storage.get(obj_id)
    
    def get_by_email(self, email):
        """Get user by email (for User entities)"""
        for obj in self.storage.values():
            if hasattr(obj, 'email') and obj.email == email:
                return obj
        return None

    def list(self):
        """List all objects"""
        return list(self.storage.values())

    def update(self, obj_id, **kwargs):
        """Update an object's attributes"""
        obj = self.storage.get(obj_id)
        if not obj:
            return None
 # Handle password separately if it's a User
        if 'password' in kwargs and hasattr(obj, 'hash_password'):
            obj.hash_password(kwargs.pop('password')) 

# Update other attributes        
        for key, value in kwargs.items():
            if hasattr(obj, key) and key not in ['id', 'created_at', '_password_hash']:
                setattr(obj, key, value)
        
        obj.updated_at = datetime.utcnow()
        return obj

    def delete(self, obj_id):
        """Delete an object by ID"""
        return self.storage.pop(obj_id, None)