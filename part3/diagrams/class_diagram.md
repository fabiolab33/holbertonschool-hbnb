# HBnB Class Diagram - SQLAlchemy Models

## Class Structure
```mermaid
classDiagram
    class BaseModel {
        +String id
        +DateTime created_at
        +DateTime updated_at
        +to_dict()
    }
    
    class User {
        +String first_name
        +String last_name
        +String email
        +String _password_hash
        +Boolean is_admin
        +List~Place~ places
        +List~Review~ reviews
        +set_password(password)
        +verify_password(password)
        +_validate_email(email)
    }
    
    class Place {
        +String title
        +String description
        +Float price
        +Float latitude
        +Float longitude
        +String owner_id
        +User owner
        +List~Review~ reviews
        +List~Amenity~ amenities
        +add_amenity(amenity)
        +remove_amenity(amenity)
    }
    
    class Review {
        +Integer rating
        +String comment
        +String user_id
        +String place_id
        +User user
        +Place place
    }
    
    class Amenity {
        +String name
        +String description
        +List~Place~ places
    }
    
    BaseModel <|-- User
    BaseModel <|-- Place
    BaseModel <|-- Review
    BaseModel <|-- Amenity
    
    User "1" --> "0..*" Place : owns
    User "1" --> "0..*" Review : writes
    Place "1" --> "0..*" Review : has
    Place "0..*" --> "0..*" Amenity : includes
```

## Inheritance

All models inherit from `BaseModel` which provides:
- Unique ID generation (UUID)
- Automatic timestamps (created_at, updated_at)
- Common serialization method (to_dict)

## Relationships in SQLAlchemy

### One-to-Many (with backref)
```python
# User → Places
places = db.relationship('Place', backref='owner', cascade='all, delete-orphan')

# User → Reviews
reviews = db.relationship('Review', backref='user', cascade='all, delete-orphan')

# Place → Reviews
reviews = db.relationship('Review', backref='place', cascade='all, delete-orphan')
```

### Many-to-Many (with association table)
```python
# Place ↔ Amenities
amenities = db.relationship('Amenity', secondary='place_amenity', 
                           back_populates='places')
places = db.relationship('Place', secondary='place_amenity', 
                        back_populates='amenities')
```