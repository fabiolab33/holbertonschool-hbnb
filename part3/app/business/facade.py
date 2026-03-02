# app/business/facade.py
from app.persistence.memory_repository import InMemoryRepository
from app.business.user import User
from app.business.place import Place
from app.business.review import Review
from app.business.amenity import Amenity

class HBnBFacade:
    """Facade for managing business logic operations using SQLAlchemy repository."""

    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ----- USER OPERATIONS -----
    def create_user(self, first_name, last_name, email, password):
        """Create a new user with hashed password."""
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
        
        place = Place(title, description, price, latitude, longitude, owner_id)
        created_place = self.place_repo.create(place)
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
        place = self.place_repo.get(place_id)
        if not place:
            return None
        
        for key, value in kwargs.items():
            if hasattr(place, key) and key not in ['id', 'created_at', 'owner_id']:
                setattr(place, key, value)
        
        place.save()
        return self.place_repo.update(place_id, place)
    
    # ----- REVIEW OPERATIONS -----
    def create_review(self, rating, comment, user_id, place_id):
        """Create a new review."""
        user = self.user_repo.get(user_id)
        place = self.place_repo.get(place_id)
        
        if not user or not place:
            raise ValueError("User or Place not found")
        
        if place.owner_id == user_id:
            raise ValueError("You cannot review your own place")
        
        review = Review(rating, comment, user_id, place_id)
        created_review = self.review_repo.create(review)
        
        user.reviews.append(created_review)
        place.reviews.append(created_review)
        
        return created_review
    
    def get_review(self, review_id):
        """Get a review by ID"""
        return self.repo.get_review(review_id)

    def list_reviews(self):
        """List all reviews"""
        return self.repo.list_reviews()
    
    def get_reviews_by_place(self, place_id):
        """Get all reviews for a specific place"""
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return place.reviews

    def update_review(self, review_id, **kwargs):
        """Update a review"""
        review = self.review_repo.get(review_id)
        if not review:
            return None
        
        for key, value in kwargs.items():
            if hasattr(review, key) and key not in ['id', 'created_at', 'user_id', 'place_id']:
                setattr(review, key, value)
        
        review.save()
        return self.review_repo.update(review_id, review)

    def delete_review(self, review_id):
        """Delete a review"""
        review = self.review_repo.get(review_id)
        if not review:
            return False
        
        user = self.user_repo.get(review.user_id)
        place = self.place_repo.get(review.place_id)
        
        if user and review in user.reviews:
            user.reviews.remove(review)
        
        if place and review in place.reviews:
            place.reviews.remove(review)
        
        self.review_repo.delete(review_id)
        return True

    # ----- AMENITY OPERATIONS -----
    def create_amenity(self, name, description):
        """Create a new amenity"""
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
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        
        for key, value in kwargs.items():
            if hasattr(amenity, key) and key not in ['id', 'created_at']:
                setattr(amenity, key, value)
        
        amenity.save()
        return self.amenity_repo.update(amenity_id, amenity)


# Global facade instance
facade = HBnBFacade()