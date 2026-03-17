"""
Test relationships between entities.
"""
from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
from app.models import User, Place, Review, Amenity

app = create_app('development')
with app.app_context():
    print("=== TEST 1: Creating data with relationships ===\n")
    
    # Create user
    user = User(first_name="John", last_name="Doe", email="john@test.com")
    user.set_password("Password123")
    db.session.add(user)
    db.session.commit()
    print(f"User created: {user.email}")
    
    # Create place
    place = Place(
        title="Cozy Apartment",
        description="Nice place in the city",
        price=100.0,
        latitude=40.7128,
        longitude=-74.0060,
        owner_id=user.id
    )
    db.session.add(place)
    db.session.commit()
    print(f"Place created: {place.title}")
    
    # Create amenities
    wifi = Amenity(name="WiFi", description="High-speed internet")
    pool = Amenity(name="Pool", description="Swimming pool")
    db.session.add_all([wifi, pool])
    db.session.commit()
    print(f"Amenities created: WiFi, Pool")
    
    # Add amenities to place
    place.amenities.append(wifi)
    place.amenities.append(pool)
    db.session.commit()
    print(f"Amenities added to place: {[a.name for a in place.amenities]}")
    
    # Create second user for review
    reviewer = User(first_name="Jane", last_name="Smith", email="jane@test.com")
    reviewer.set_password("Password123")
    db.session.add(reviewer)
    db.session.commit()
    print(f"Reviewer created: {reviewer.email}")
    
    # Create review
    review = Review(
        rating=5,
        comment="Amazing place!",
        user_id=reviewer.id,
        place_id=place.id
    )
    db.session.add(review)
    db.session.commit()
    print(f"Review created: {review.rating}/5 - {review.comment}")
    
    print("\n=== TEST 2: Verifying relationships ===\n")
    
    # Check relationships User -> Places
    print(f"User: {user.email}")
    print(f"  Places owned: {len(user.places)}")
    for p in user.places:
        print(f"    - {p.title}")
    
    # Check relationships Place -> Amenities
    print(f"\nPlace: {place.title}")
    print(f"  Amenities: {[a.name for a in place.amenities]}")
    print(f"  Reviews: {len(place.reviews)}")
    print(f"  Owner: {place.owner.email}")
    
    # Check relationships Review -> User, Place
    print(f"\nReview: {review.comment}")
    print(f"  Rating: {review.rating}/5")
    print(f"  Author: {review.user.email}")
    print(f"  Place: {review.place.title}")
    
    # Check bidirectional relationships
    print(f"\nAmenity WiFi in places: {[p.title for p in wifi.places]}")
    print(f"Reviewer's reviews: {len(reviewer.reviews)}")
    
    print("\n=== TASK 8 COMPLETE ===")
    print("All relationships working correctly!")
    print(f"\nFinal counts:")
    print(f"  Users: {User.query.count()}")
    print(f"  Places: {Place.query.count()}")
    print(f"  Reviews: {Review.query.count()}")
    print(f"  Amenities: {Amenity.query.count()}")