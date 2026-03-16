# app/business/facade.py
from app.persistence.memory_repository import InMemoryRepository
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository
from app.business.user import User
from app.business.place import Place
from app.business.review import Review
from app.business.amenity import Amenity
import os

class HBnBFacade:
    """Facade for managing business logic operations using SQLAlchemy repository."""

    def __init__(self, use_database=False):
        """
        Initialize the facade with either in-memory or database repositories.
        
        Args:
            use_database: If True, use SQLAlchemy repositories. 
                         If False, use in-memory repositories.
        """
        self.use_database = use_database
        
        if use_database:
            # SQLAlchemy repositories (requires models to be mapped)
            # This will be activated in Task 6 after model mapping
            from app.models import User as UserModel
            from app.models import Place as PlaceModel
            from app.models import Review as ReviewModel
            from app.models import Amenity as AmenityModel

            self.user_repo = SQLAlchemyRepository(UserModel)
            self.place_repo = SQLAlchemyRepository(PlaceModel)
            self.review_repo = SQLAlchemyRepository(ReviewModel)
            self.amenity_repo = SQLAlchemyRepository(AmenityModel)

            print("✅ Using SQLAlchemy repository")
        else:
            # In-memory repositories (current implementation)
            self.user_repo = InMemoryRepository()
            self.place_repo = InMemoryRepository()
            self.review_repo = InMemoryRepository()
            self.amenity_repo = InMemoryRepository()

            print("✅ Using InMemory repository")

    # ----- USER OPERATIONS -----
    def create_user(self, first_name, last_name, email, password):
        """Create a new user with hashed password."""
        if self.use_database:
            from app.models import User as UserModel
            user = UserModel(
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            user.set_password(password)
        else:
            user = User(first_name, last_name, email, password)
        return self.user_repo.create(user)
    
    def get_user(self, user_id):
        """Get a user by ID"""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Get a user by email"""
        return self.user_repo.get_by_email(email)

    def list_users(self):
        """List all users"""
        return self.user_repo.list()

    def update_user(self, user_id, **kwargs):
        """Update a user information (handle password hashing inside repo)"""
        return self.user_repo.update(user_id, **kwargs)

    # ----- PLACE OPERATIONS -----
    def create_place(self, title, description, price, latitude, longitude, owner_id):
        """Create a new place."""
        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError("Owner not found")
        
        if self.use_database:
            from app.models import Place as PlaceModel
            place = PlaceModel(
                title=title,
                description=description,
                price=price,
                latitude=latitude,
                longitude=longitude,
                owner_id=owner_id
            )
        else:
            place = Place(title, description, price, latitude, longitude, owner_id)
        
        created_place = self.place_repo.create(place)
        
        # Add to owner's places if using in-memory
        if not self.use_database and hasattr(owner, 'places'):
            owner.places.append(created_place)
        return created_place

    def get_place(self, place_id):
        """Get a place by ID"""
        return self.place_repo.get(place_id)
    
    def list_places(self):
        """List all places"""
        return self.place_repo.list()
    
    def update_place(self, place_id, **kwargs):
        """Update a place"""
        return self.place_repo.update(place_id, **kwargs)
    
    def delete_place(self, place_id):
        """Delete a place and all its associated reviews."""
        place = self.place_repo.get(place_id)
        if not place:
            return False
        
        # Delete all reviews for this place
        if self.use_database:
            # With database, cascade delete should handle this
            pass
        else:
            reviews_to_delete = place.reviews[:]
            for review in reviews_to_delete:
                self.delete_review(review.id)
        
        # Remove from owner's places list
        if not self.use_database:
            owner = self.user_repo.get(place.owner_id)
            if owner and hasattr(owner, 'places') and place in owner.places:
                owner.places.remove(place)
        
        # Delete the place
        return self.place_repo.delete(place_id)

    # ----- REVIEW OPERATIONS -----
    def create_review(self, rating, comment, user_id, place_id):
        """Create a new review."""
        user = self.user_repo.get(user_id)
        place = self.place_repo.get(place_id)
        
        if not user or not place:
            raise ValueError("User or Place not found")
        
        if place.owner_id == user_id:
            raise ValueError("You cannot review your own place")
        
        if self.use_database:
            from app.models import Review as ReviewModel
            review = ReviewModel(
                rating=rating,
                comment=comment,
                user_id=user_id,
                place_id=place_id
            )
        else:
            review = Review(rating, comment, user_id, place_id)
        
        created_review = self.review_repo.create(review)
        
        # Add to lists if using in-memory
        if not self.use_database:
            if hasattr(user, 'reviews'):
                user.reviews.append(created_review)
            if hasattr(place, 'reviews'):
                place.reviews.append(created_review)
        
        return created_review
    
    def get_review(self, review_id):
        """Get a review by ID"""
        return self.review_repo.get(review_id)

    def list_reviews(self):
        """List all reviews"""
        return self.review_repo.list()
    
    def get_reviews_by_place(self, place_id):
        """Get all reviews for a specific place"""
        place = self.place_repo.get(place_id)
        if not place:
            return None
        
        if self.use_database:
            # Query reviews by place_id
            from app.models import Review as ReviewModel
            from app import db
            return db.session.query(ReviewModel).filter_by(place_id=place_id).all()
        else:
            return place.reviews

    def update_review(self, review_id, **kwargs):
        """Update a review"""
        return self.review_repo.update(review_id, **kwargs)

    def delete_review(self, review_id):
        """Delete a review"""
        review = self.review_repo.get(review_id)
        if not review:
            return False
        
        if not self.use_database:
            # In-memory: Remove from user and place lists
            user = self.user_repo.get(review.user_id)
            place = self.place_repo.get(review.place_id)
        
            if user and hasattr(user, 'reviews') and review in user.reviews:
                user.reviews.remove(review)
        
            if place and hasattr(place, 'reviews') and review in place.reviews:
                place.reviews.remove(review)
        
        return self.review_repo.delete(review_id)

    # ----- AMENITY OPERATIONS -----
    def create_amenity(self, name, description):
        """Create a new amenity"""
        if self.use_database:
            from app.models import Amenity as AmenityModel
            amenity = AmenityModel(name=name, description=description)
        else:
            amenity = Amenity(name, description)

        return self.amenity_repo.create(amenity)

    def get_amenity(self, amenity_id):
        """Get an amenity by ID"""
        return self.amenity_repo.get(amenity_id)
    
    def list_amenities(self):
        """List all amenities"""
        return self.amenity_repo.list()
    
    def update_amenity(self, amenity_id, **kwargs):
        """Update an amenity"""
        return self.amenity_repo.update(amenity_id, **kwargs)

# Global facade instance
USE_DATABASE = os.environ.get('USE_DATABASE', 'false').lower() == 'true'
facade = HBnBFacade(use_database=USE_DATABASE)
