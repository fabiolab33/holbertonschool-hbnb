# app/business/user.py
from datetime import datetime

class User:
    def __init__(self, first_name, last_name, email, password):
        self.id = None
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = False
        self.created_at = None
        self.updated_at = None
