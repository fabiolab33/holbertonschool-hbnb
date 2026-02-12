# app/business/user.py
from app.business.base_model import BaseModel
import re

class User(BaseModel):
    """User entity representing a system user"""

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = self._validate_email(email)
        self.password = password
        self.is_admin = is_admin
        self.places = []
        self.reviews = []

    def _validate_email(self, email):
        """Validate email format"""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            raise ValueError("Invalid email format")
        return email

    def update_profile(self, **kwargs):
        """Update user attributes"""
        if 'email' in kwargs:
            kwargs['email'] = self._validate_email(kwargs['email'])
        
        for key, value in kwargs.items():
            if hasattr(self, key) and key not in ['id', 'created_at', 'is_admin']:
                setattr(self, key, value)
        self.save()

    def to_dict(self):
        """Return dictionary representation without password"""
        data = super().to_dict()
        data.update({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
        })
        return data