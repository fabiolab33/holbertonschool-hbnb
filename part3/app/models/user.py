"""
User model with SQLAlchemy mapping.
"""
from app import db, bcrypt
from app.models.base import BaseModel
import re


class User(BaseModel):
    """User model for database storage."""
    
    __tablename__ = 'users'
    
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)
    _password_hash = db.Column('password', db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

     # Relationships
    places = db.relationship('Place', backref='owner', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user', lazy=True, cascade='all, delete-orphan')
        
    def __init__(self, first_name, last_name, email, is_admin=False):
        """Initialize user with validation."""
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = self._validate_email(email)
        self.is_admin = is_admin
        self._password_hash = None
    
    def _validate_email(self, email):
        """Validate email format using regex."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            raise ValueError("Invalid email format")
        return email
    
    def set_password(self, password):
        """Hash and set the password."""
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def verify_password(self, password):
        """Verify the password against the hash."""
        return bcrypt.check_password_hash(self._password_hash, password)
    
    @property
    def password(self):
        """Prevent password from being accessed."""
        raise AttributeError('password is not a readable attribute')
    
    def to_dict(self):
        """Convert to dictionary without password."""
        data = super().to_dict()
        # Remove password hash from output
        data.pop('password', None)
        data.pop('_password_hash', None)
        return data
