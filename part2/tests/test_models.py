"""
Unit Tests for HBnB Business Logic Layer
Tests all entity models and their validation rules
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.business.user import User
from app.business.place import Place
from app.business.review import Review
from app.business.amenity import Amenity


class TestUserModel:
    """Test User entity validation"""
    
    def test_user_creation_valid(self):
        """Test creating a user with valid data"""
        user = User("John", "Doe", "john.doe@example.com", "password123")
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.email == "john.doe@example.com"
        assert user.password == "password123"
        assert user.id is not None
        assert user.created_at is not None
        assert user.is_admin == False
        
    def test_user_invalid_email_no_at(self):
        """Test that email without @ raises ValueError"""
        with pytest.raises(ValueError, match="Invalid email format"):
            User("John", "Doe", "invalid-email", "password123")
    
    def test_user_invalid_email_no_domain(self):
        """Test email without domain raises error"""
        with pytest.raises(ValueError, match="Invalid email format"):
            User("John", "Doe", "john@", "password123")
    
    def test_user_invalid_email_no_local(self):
        """Test email without local part raises error"""
        with pytest.raises(ValueError, match="Invalid email format"):
            User("John", "Doe", "@example.com", "password123")
    
    def test_user_invalid_email_no_tld(self):
        """Test email without TLD raises error"""
        with pytest.raises(ValueError, match="Invalid email format"):
            User("John", "Doe", "john@example", "password123")
    
    def test_user_valid_email_formats(self):
        """Test various valid email formats"""
        valid_emails = [
            "simple@example.com",
            "name.surname@example.com",
            "name+tag@example.co.uk",
            "name_123@example.org"
        ]
        for email in valid_emails:
            user = User("Test", "User", email, "pass")
            assert user.email == email
    
    def test_user_update_profile(self):
        """Test updating user profile"""
        user = User("John", "Doe", "john@example.com", "pass")
        user.update_profile(first_name="Jane", email="jane@example.com")
        assert user.first_name == "Jane"
        assert user.email == "jane@example.com"
    
    def test_user_update_profile_invalid_email(self):
        """Test updating with invalid email raises error"""
        user = User("John", "Doe", "john@example.com", "pass")
        with pytest.raises(ValueError, match="Invalid email format"):
            user.update_profile(email="invalid-email")


class TestPlaceModel:
    """Test Place entity validation"""
    
    def test_place_creation_valid(self):
        """Test creating a place with valid data"""
        place = Place("Cozy Apartment", "Nice place", 100.0, 37.7749, -122.4194, "owner-id")
        assert place.title == "Cozy Apartment"
        assert place.description == "Nice place"
        assert place.price == 100.0
        assert place.latitude == 37.7749
        assert place.longitude == -122.4194
        assert place.owner_id == "owner-id"
        assert place.reviews == []
        assert place.amenities == []
    
    def test_place_negative_price(self):
        """Test that negative price raises ValueError"""
        with pytest.raises(ValueError, match="Price must be a positive number"):
            Place("Invalid", "Bad price", -50.0, 37.7749, -122.4194, "owner-id")
    
    def test_place_zero_price(self):
        """Test that zero price is allowed"""
        place = Place("Free", "Free place", 0.0, 37.7749, -122.4194, "owner-id")
        assert place.price == 0.0
    
    def test_place_invalid_latitude_high(self):
        """Test latitude > 90 raises error"""
        with pytest.raises(ValueError, match="Latitude must be between -90 and 90"):
            Place("Invalid", "Bad latitude", 100.0, 95.0, -122.4194, "owner-id")
    
    def test_place_invalid_latitude_low(self):
        """Test latitude < -90 raises error"""
        with pytest.raises(ValueError, match="Latitude must be between -90 and 90"):
            Place("Invalid", "Bad latitude", 100.0, -95.0, -122.4194, "owner-id")
    
    def test_place_boundary_latitude_90(self):
        """Test latitude exactly 90 is valid"""
        place = Place("North Pole", "Description", 100.0, 90.0, 0.0, "owner-id")
        assert place.latitude == 90.0
    
    def test_place_boundary_latitude_minus_90(self):
        """Test latitude exactly -90 is valid"""
        place = Place("South Pole", "Description", 100.0, -90.0, 0.0, "owner-id")
        assert place.latitude == -90.0
    
    def test_place_invalid_longitude_high(self):
        """Test longitude > 180 raises error"""
        with pytest.raises(ValueError, match="Longitude must be between -180 and 180"):
            Place("Invalid", "Bad longitude", 100.0, 37.7749, 200.0, "owner-id")
    
    def test_place_invalid_longitude_low(self):
        """Test longitude < -180 raises error"""
        with pytest.raises(ValueError, match="Longitude must be between -180 and 180"):
            Place("Invalid", "Bad longitude", 100.0, 37.7749, -200.0, "owner-id")
    
    def test_place_boundary_longitude_180(self):
        """Test longitude exactly 180 is valid"""
        place = Place("Date Line", "Description", 100.0, 0.0, 180.0, "owner-id")
        assert place.longitude == 180.0
    
    def test_place_boundary_longitude_minus_180(self):
        """Test longitude exactly -180 is valid"""
        place = Place("Date Line", "Description", 100.0, 0.0, -180.0, "owner-id")
        assert place.longitude == -180.0
    
    def test_place_none_coordinates(self):
        """Test that None coordinates are allowed"""
        place = Place("Apartment", "Description", 100.0, None, None, "owner-id")
        assert place.latitude is None
        assert place.longitude is None
    
    def test_place_add_review(self):
        """Test adding a review to a place"""
        place = Place("Apartment", "Description", 100.0, None, None, "owner-id")
        review = Review(5, "Great!", "user-id", place.id)
        place.add_review(review)
        assert len(place.reviews) == 1
        assert place.reviews[0] == review
    
    def test_place_add_amenity(self):
        """Test adding an amenity to a place"""
        place = Place("Apartment", "Description", 100.0, None, None, "owner-id")
        amenity = Amenity("WiFi", "High-speed internet")
        place.add_amenity(amenity)
        assert len(place.amenities) == 1
        assert place.amenities[0] == amenity
    
    def test_place_add_duplicate_amenity(self):
        """Test that duplicate amenities are not added"""
        place = Place("Apartment", "Description", 100.0, None, None, "owner-id")
        amenity = Amenity("WiFi", "High-speed internet")
        place.add_amenity(amenity)
        place.add_amenity(amenity)  # Try to add again
        assert len(place.amenities) == 1


class TestReviewModel:
    """Test Review entity validation"""
    
    def test_review_creation_valid(self):
        """Test creating a review with valid data"""
        review = Review(5, "Great place!", "user-id", "place-id")
        assert review.rating == 5
        assert review.comment == "Great place!"
        assert review.user_id == "user-id"
        assert review.place_id == "place-id"
        assert review.id is not None
    
    def test_review_rating_boundary_1(self):
        """Test rating of 1 is valid (lower boundary)"""
        review = Review(1, "Poor", "user-id", "place-id")
        assert review.rating == 1
    
    def test_review_rating_boundary_5(self):
        """Test rating of 5 is valid (upper boundary)"""
        review = Review(5, "Excellent", "user-id", "place-id")
        assert review.rating == 5
    
    def test_review_invalid_rating_high(self):
        """Test rating > 5 raises error"""
        with pytest.raises(ValueError, match="Rating must be an integer between 1 and 5"):
            Review(6, "Comment", "user-id", "place-id")
    
    def test_review_invalid_rating_low(self):
        """Test rating < 1 raises error"""
        with pytest.raises(ValueError, match="Rating must be an integer between 1 and 5"):
            Review(0, "Comment", "user-id", "place-id")
    
    def test_review_invalid_rating_negative(self):
        """Test negative rating raises error"""
        with pytest.raises(ValueError, match="Rating must be an integer between 1 and 5"):
            Review(-1, "Comment", "user-id", "place-id")
    
    def test_review_invalid_rating_float(self):
        """Test non-integer rating raises error"""
        with pytest.raises(ValueError, match="Rating must be an integer between 1 and 5"):
            Review(3.5, "Comment", "user-id", "place-id")
    
    def test_review_invalid_rating_string(self):
        """Test string rating raises error"""
        with pytest.raises(ValueError, match="Rating must be an integer between 1 and 5"):
            Review("3", "Comment", "user-id", "place-id")
    
    def test_review_empty_comment(self):
        """Test empty comment raises error"""
        with pytest.raises(ValueError, match="Comment cannot be empty"):
            Review(4, "", "user-id", "place-id")
    
    def test_review_whitespace_only_comment(self):
        """Test whitespace-only comment raises error"""
        with pytest.raises(ValueError, match="Comment cannot be empty"):
            Review(4, "   ", "user-id", "place-id")
    
    def test_review_whitespace_tabs_comment(self):
        """Test tabs-only comment raises error"""
        with pytest.raises(ValueError, match="Comment cannot be empty"):
            Review(4, "\t\t", "user-id", "place-id")
    
    def test_review_comment_trimmed(self):
        """Test that comment whitespace is trimmed"""
        review = Review(4, "  Great!  ", "user-id", "place-id")
        assert review.comment == "Great!"
    
    def test_review_comment_with_newlines_trimmed(self):
        """Test comment with newlines is trimmed"""
        review = Review(4, "\n  Great!  \n", "user-id", "place-id")
        assert review.comment == "Great!"
    
    def test_review_all_ratings_valid(self):
        """Test all valid ratings (1-5)"""
        for rating in range(1, 6):
            review = Review(rating, "Comment", "user-id", "place-id")
            assert review.rating == rating


class TestAmenityModel:
    """Test Amenity entity validation"""
    
    def test_amenity_creation_valid(self):
        """Test creating amenity with valid data"""
        amenity = Amenity("WiFi", "High-speed internet")
        assert amenity.name == "WiFi"
        assert amenity.description == "High-speed internet"
        assert amenity.id is not None
    
    def test_amenity_empty_name(self):
        """Test empty name raises error"""
        with pytest.raises(ValueError, match="Amenity name cannot be empty"):
            Amenity("", "Description")
    
    def test_amenity_whitespace_name(self):
        """Test whitespace-only name raises error"""
        with pytest.raises(ValueError, match="Amenity name cannot be empty"):
            Amenity("   ", "Description")
    
    def test_amenity_tabs_name(self):
        """Test tabs-only name raises error"""
        with pytest.raises(ValueError, match="Amenity name cannot be empty"):
            Amenity("\t\t", "Description")
    
    def test_amenity_name_trimmed(self):
        """Test that name is trimmed"""
        amenity = Amenity("  WiFi  ", "Description")
        assert amenity.name == "WiFi"
    
    def test_amenity_name_with_newlines_trimmed(self):
        """Test name with newlines is trimmed"""
        amenity = Amenity("\n  Pool  \n", "Description")
        assert amenity.name == "Pool"
    
    def test_amenity_empty_description_allowed(self):
        """Test that empty description is allowed"""
        amenity = Amenity("WiFi", "")
        assert amenity.description == ""
    
    def test_amenity_various_names(self):
        """Test various valid amenity names"""
        names = ["WiFi", "Air Conditioning", "Pool", "Gym", "Parking", "Kitchen"]
        for name in names:
            amenity = Amenity(name, "Description")
            assert amenity.name == name


class TestBaseModel:
    """Test BaseModel functionality"""
    
    def test_id_generation(self):
        """Test that ID is automatically generated"""
        user1 = User("John", "Doe", "john@example.com", "pass")
        user2 = User("Jane", "Doe", "jane@example.com", "pass")
        assert user1.id is not None
        assert user2.id is not None
        assert user1.id != user2.id
    
    def test_created_at_set(self):
        """Test that created_at is set on creation"""
        user = User("John", "Doe", "john@example.com", "pass")
        assert user.created_at is not None
    
    def test_updated_at_set(self):
        """Test that updated_at is set on creation"""
        user = User("John", "Doe", "john@example.com", "pass")
        assert user.updated_at is not None
    
    def test_save_updates_timestamp(self):
        """Test that save() updates the updated_at timestamp"""
        import time
        user = User("John", "Doe", "john@example.com", "pass")
        original_updated_at = user.updated_at
        time.sleep(0.01)  # Small delay
        user.save()
        assert user.updated_at > original_updated_at


if __name__ == "__main__":
    pytest.main([__file__, "-v"])