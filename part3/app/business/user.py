# app/business/user.py
import re
from app.business.base_model import BaseModel
from app import bcrypt

class User(BaseModel):
    """User entity representing a system user"""

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = self._validate_email(email)
        self.is_admin = is_admin
        self.places = []
        self.reviews = []

 # Hash password on creation
        if password:
            self.hash_password(password)
        else:
            self._password_hash = None

    def _validate_email(self, email):
        """Validate email format using regex"""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            raise ValueError("Invalid email format")
        return email
    
    def hash_password(self, password):
        """Hash the password using bcrypt."""
        if not password:
            raise ValueError("Password cannot be empty")
        
         # Generate password hash
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
         """Verify a password against the stored hash."""
         if not self._password_hash:
            return False
    
         return bcrypt.check_password_hash(self._password_hash, password)

    def update_profile(self, **kwargs):
        """Update user attributes safely."""
        # Handle password update separately to ensure hashing
        if 'password' in kwargs:
            self.hash_password(kwargs.pop('password'))
        
        # Validate email if it's being updated
        if 'email' in kwargs:
            kwargs['email'] = self._validate_email(kwargs['email'])
       
        # Update other attributes
        for key, value in kwargs.items():
            if hasattr(self, key) and key not in ['id', 'created_at', 'is_admin', '_password_hash']:
                setattr(self, key, value)
        
        self.save()
    
    def to_dict(self):
        """Return dictionary representation WITHOUT password."""
        data = super().to_dict()
        data.update({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
        })
        # Explicitly exclude password from dictionary representation
        return data