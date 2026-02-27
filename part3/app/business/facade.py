# app/business/facade.py
from app.persistence.memory_repository import InMemoryRepository
from app.business.user import User
from app.business.place import Place
from app.business.review import Review
from app.business.amenity import Amenity

class HBnBFacade:
    """Facade pattern to simplify interactions between layers"""

    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ----- USER OPERATIONS -----
    def create_user(self, first_name, last_name, email, password):
        """Create a new user"""
        # Check if email already exists
        existing_users = self.user_repo.list()
        for user in existing_users:
            if user.email == email:
                raise ValueError("Email already registered")
        
        user = User(first_name, last_name, email, password)
        return self.user_repo.create(user)

    def get_user(self, user_id):
        """Get a user by ID"""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Get a user by email"""
        users = self.user_repo.list()
        for user in users:
            if user.email == email:
                return user
        return None

    def list_users(self):
        """List all users"""
        return self.user_repo.list()

    def update_user(self, user_id, **kwargs):
        """Update a user"""
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("User not found")
        
        # Check if email is being updated and if it's already in use
        if 'email' in kwargs and kwargs['email'] != user.email:
            existing_user = self.get_user_by_email(kwargs['email'])
            if existing_user:
                raise ValueError("Email already registered")
        
        user.update_profile(**kwargs)
        return user

    # ----- PLACE OPERATIONS -----
    def create_place(self, title, description, price, latitude, longitude, owner_id):
        """Create a new place"""
        # Validate that owner exists
        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError("Owner not found")
        
        place = Place(title, description, price, latitude, longitude, owner_id)
        created_place = self.place_repo.create(place)
        
        # Add place to owner's places list
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
            raise ValueError("Place not found")
        
        # Validate owner if being updated
        if 'owner_id' in kwargs:
            owner = self.user_repo.get(kwargs['owner_id'])
            if not owner:
                raise ValueError("Owner not found")
        
        return self.place_repo.update(place_id, **kwargs)

    # ----- REVIEW OPERATIONS -----
    def create_review(self, rating, comment, user_id, place_id):
        """Create a new review"""
        # Validate that user exists
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("User not found")
        
        # Validate that place exists
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")
        
        # Check if user is not reviewing their own place
        if place.owner_id == user_id:
            raise ValueError("You cannot review your own place")
        
        review = Review(rating, comment, user_id, place_id)
        created_review = self.review_repo.create(review)
        
        # Add review to user's and place's review lists
        user.reviews.append(created_review)
        place.add_review(created_review)
        
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
            raise ValueError("Place not found")
        return place.reviews

    def update_review(self, review_id, **kwargs):
        """Update a review"""
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")
        
        # Validate rating if being updated
        if 'rating' in kwargs:
            if not isinstance(kwargs['rating'], int) or not (1 <= kwargs['rating'] <= 5):
                raise ValueError("Rating must be an integer between 1 and 5")
        
        # Validate comment if being updated
        if 'comment' in kwargs:
            if not kwargs['comment'] or not kwargs['comment'].strip():
                raise ValueError("Comment cannot be empty")
            kwargs['comment'] = kwargs['comment'].strip()
        
        return self.review_repo.update(review_id, **kwargs)

    def delete_review(self, review_id):
        """Delete a review"""
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")
        
        # Remove review from user's reviews list
        user = self.user_repo.get(review.user_id)
        if user and review in user.reviews:
            user.reviews.remove(review)
        
        # Remove review from place's reviews list
        place = self.place_repo.get(review.place_id)
        if place and review in place.reviews:
            place.reviews.remove(review)
        
        return self.review_repo.delete(review_id)

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
            raise ValueError("Amenity not found")
        return self.amenity_repo.update(amenity_id, **kwargs)