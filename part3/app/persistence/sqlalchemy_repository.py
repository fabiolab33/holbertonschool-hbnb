from app import db
from datetime import datetime

class SQLAlchemyRepository:
    """Base repository for SQLAlchemy models"""

    def __init__(self, model):
        """
        Initialize repository with a SQLAlchemy model.
        
        Args:
            model: SQLAlchemy model class
        """
        self.model = model

    def add(self, obj):
        """
        Add a new object to the database.
        
        Args:
            obj: SQLAlchemy model instance
            
        Returns:
            Created object
        """
        db.session.add(obj)
        db.session.commit()
        db.session.refresh(obj)
        return obj
    
    # Alias for compatibility
    create = add

    def get(self, obj_id):
        """
        Retrieve an object by ID.
        
        Args:
            obj_id: Object ID
            
        Returns:
            Object or None if not found
        """
        return db.session.get(self.model, obj_id)
    
    def get_all(self):
        """
        Get all objects.
        
        Returns:
            List of all objects
        """
        return db.session.query(self.model).all()
    
    # Alias for compatibility
    list = get_all

    def get_by_attribute(self, attr_name, attr_value):
        """
        Get object by any attribute.
        
        Args:
            attr_name: Attribute name (e.g., 'email')
            attr_value: Attribute value
            
        Returns:
            Object or None if not found
        """
        return db.session.query(self.model).filter(
            getattr(self.model, attr_name) == attr_value
        ).first()
    
    def get_by_email(self, email):
        """
        Get user by email (for User model).
        
        Args:
            email: Email address
            
        Returns:
            User object or None
        """
        return self.get_by_attribute('email', email)

    def update(self, obj_id, data):
        """
        Update an object's attributes.
        
        Args:
            obj_id: Object ID
            data: Dictionary of attributes to update
            
        Returns:
            Updated object or None if not found
        """
        obj = self.get(obj_id)
        if not obj:
            return None
        
        # Handle password separately if it's a User model
        if 'password' in data and hasattr(obj, 'set_password'):
            obj.set_password(data.pop('password'))
        
        # Update other attributes
        for key, value in data.items():
            if hasattr(obj, key) and key not in ['id', 'created_at']:
                setattr(obj, key, value)
        
        # Update timestamp if exists
        if hasattr(obj, 'updated_at'):
            obj.updated_at = datetime.utcnow()
        
        db.session.commit()
        db.session.refresh(obj)
        return obj
    
    def delete(self, obj_id):
        """
        Delete an object by ID.
        
        Args:
            obj_id: Object ID
            
        Returns:
            True if deleted, False if not found
        """
        obj = self.get(obj_id)
        if not obj:
            return False
        
        db.session.delete(obj)
        db.session.commit()
        return True
