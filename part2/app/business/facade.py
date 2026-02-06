# app/business/facade.py
from app.persistence.memory_repository import InMemoryRepository
from app.business.user import User
from app.business.place import Place
from app.business.review import Review
from app.business.amenity import Amenity

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ----- USERS -----
    def create_user(self, first_name, last_name, email, password):
        user = User(first_name, last_name, email, password)
        return self.user_repo.create(user)

    def list_users(self):
        return self.user_repo.list()

    # ----- PLACES -----
    def create_place(self, title, description, price, latitude=None, longitude=None):
        place = Place(title, description, price, latitude, longitude)
        return self.place_repo.create(place)

    def list_places(self):
        return self.place_repo.list()

    # ----- REVIEWS -----
    def create_review(self, rating, comment, user_id=None, place_id=None):
        review = Review(rating, comment, user_id, place_id)
        return self.review_repo.create(review)

    def list_reviews(self):
        return self.review_repo.list()

    # ----- AMENITIES -----
    def create_amenity(self, name, description):
        amenity = Amenity(name, description)
        return self.amenity_repo.create(amenity)

    def list_amenities(self):
        return self.amenity_repo.list()
