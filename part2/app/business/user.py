# app/business/user.py
from app.business.base_model import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.places = []   # Task 1 list of Place
        self.reviews = []  # Task 1 list of Review

    def update_profile(self, **kwargs):
        """Update user attributes"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def delete(self):
        """Delete the user (implementation depends on repository)"""
        pass # Task 1 delete logic to be implemented in repository layer
