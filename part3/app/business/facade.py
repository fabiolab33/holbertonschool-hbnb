import os

class HBnBFacade:
    """Facade for managing business logic operations using SQLAlchemy repository."""

    def __init__(self):
        """Initialize facade with appropriate repository."""
        # Read environment variable
        use_db = os.getenv('USE_DATABASE', 'false').lower() == 'true'
        
        if use_db:
            # SQLAlchemy repositories (requires models to be mapped)
            # This will be activated in Task 6 after model mapping
            print("✅ Using SQLAlchemy repository")
            from app.persistence.sqlalchemy_repository import SQLAlchemyRepository
            from app.models.user import User as UserModel
            from app.models.place import Place as PlaceModel
            from app.models.review import Review as ReviewModel
            from app.models.amenity import Amenity as AmenityModel

            self.user_repo = SQLAlchemyRepository(UserModel)
            self.place_repo = SQLAlchemyRepository(PlaceModel)
            self.review_repo = SQLAlchemyRepository(ReviewModel)
            self.amenity_repo = SQLAlchemyRepository(AmenityModel)
        else:
            # In-memory repositories (current implementation)
            print("✅ Using InMemory repository")
            from app.persistence.memory_repository import InMemoryRepository
            self.user_repo = InMemoryRepository()
            self.place_repo = InMemoryRepository()
            self.review_repo = InMemoryRepository()
            self.amenity_repo = InMemoryRepository()

    # ----- USER OPERATIONS -----
    def create_user(self, user_data):
        """Create a new user with hashed password."""
        from app.models.user import User
        user = User(**user_data)
        return  self.user_repo.add(user)
    
    def get_user(self, user_id):
        """Get a user by ID"""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Get a user by email"""
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """Get all users."""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update a user information (handle password hashing inside repo)"""
        return self.user_repo.update(user_id, user_data)

    def delete_user(self, user_id):
        """Delete user."""
        self.user_repo.delete(user_id)

    # ----- PLACE OPERATIONS -----
    def create_place(self, place_data):
        """Create a new place."""
        from app.models.place import Place
        place = Place(**place_data)
        return self.place_repo.add(place)

    def get_place(self, place_id):
        """Get a place by ID"""
        return self.place_repo.get(place_id)
    
    def get_all_places(self):
        """Get all places."""
        return self.place_repo.get_all()
    
    def update_place(self, place_id, place_data):
        """Update a place"""
        return self.place_repo.update(place_id, place_data)
    
    def delete_place(self, place_id):
        """Delete a place and all its associated reviews."""
        self.place_repo.delete(place_id)

    # ----- REVIEW OPERATIONS -----
    def create_review(self, review_data):
        """Create a new review."""
        from app.models.review import Review
        review = Review(**review_data)
        return self.review_repo.add(review)
    
    def get_review(self, review_id):
        """Get a review by ID"""
        return self.review_repo.get(review_id)
    
    def get_all_reviews(self):
        """Get all reviews."""
        return self.review_repo.get_all()
    
    def get_reviews_by_place(self, place_id):
        """Get all reviews for a specific place"""
        all_reviews = self.review_repo.get_all()
        return [r for r in all_reviews if r.place_id == place_id]

    def update_review(self, review_id, review_data):
        """Update a review"""
        return self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        """Delete a review"""
        self.review_repo.delete(review_id)

    # ----- AMENITY OPERATIONS -----
    def create_amenity(self, amenity_data):
        """Create a new amenity"""
        from app.models.amenity import Amenity
        amenity = Amenity(**amenity_data)
        return self.amenity_repo.add(amenity)

    def get_amenity(self, amenity_id):
        """Get an amenity by ID"""
        return self.amenity_repo.get(amenity_id)
    
    def get_all_amenities(self):
        """Get all amenities."""
        return self.amenity_repo.get_all()
    
    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity"""
        return self.amenity_repo.update(amenity_id, amenity_data)
    
    def delete_amenity(self, amenity_id):
        """Delete amenity."""
        self.amenity_repo.delete(amenity_id)

# Global facade instance
facade = HBnBFacade()