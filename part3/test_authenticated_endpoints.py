"""
Test authenticated user access to endpoints.
"""

import requests
import json

BASE_URL = 'http://localhost:5001/api'


def test_authenticated_endpoints():
    """Test authenticated user access and ownership validation."""
    
    print("\n" + "="*70)
    print("TESTING AUTHENTICATED USER ACCESS ENDPOINTS")
    print("="*70 + "\n")
    
    # Step 1: Create two users
    print("1. Creating two test users...")
    
    user1_data = {
        'first_name': 'Alice',
        'last_name': 'Owner',
        'email': 'alice@test.com',
        'password': 'AlicePass123'
    }
    
    user2_data = {
        'first_name': 'Bob',
        'last_name': 'Reviewer',
        'email': 'bob@test.com',
        'password': 'BobPass123'
    }
    
    response1 = requests.post(f'{BASE_URL}/users/', json=user1_data)
    response2 = requests.post(f'{BASE_URL}/users/', json=user2_data)
    
    if response1.status_code == 201 and response2.status_code == 201:
        user1 = response1.json()
        user2 = response2.json()
        print(f"   ✓ User 1 created: {user1['email']}")
        print(f"   ✓ User 2 created: {user2['email']}")
    else:
        print("   ❌ Failed to create users")
        return False
    
    # Step 2: Login both users
    print("\n2. Logging in both users...")
    
    token1_response = requests.post(f'{BASE_URL}/auth/login', json={
        'email': 'alice@test.com',
        'password': 'AlicePass123'
    })
    
    token2_response = requests.post(f'{BASE_URL}/auth/login', json={
        'email': 'bob@test.com',
        'password': 'BobPass123'
    })
    
    if token1_response.status_code == 200 and token2_response.status_code == 200:
        token1 = token1_response.json()['access_token']
        token2 = token2_response.json()['access_token']
        print("   ✓ Both users logged in successfully")
    else:
        print("   ❌ Login failed")
        return False
    
    headers1 = {'Authorization': f'Bearer {token1}'}
    headers2 = {'Authorization': f'Bearer {token2}'}
    
    # Step 3: User 1 creates a place
    print("\n3. User 1 (Alice) creating a place...")
    
    place_data = {
        'title': 'Alice Cozy Apartment',
        'description': 'Beautiful apartment in downtown',
        'price': 100.0,
        'latitude': 37.7749,
        'longitude': -122.4194
    }
    
    response = requests.post(f'{BASE_URL}/places/', json=place_data, headers=headers1)
    
    if response.status_code == 201:
        place = response.json()
        place_id = place['id']
        print(f"   ✓ Place created by Alice: {place['title']}")
        print(f"   Owner ID: {place.get('owner_id', 'N/A')}")
    else:
        print(f"   ❌ Failed to create place: {response.status_code}")
        print(f"   Response: {response.text}")
        return False
    
    # Step 4: Try to create place without authentication
    print("\n4. Attempting to create place WITHOUT authentication...")
    
    response = requests.post(f'{BASE_URL}/places/', json=place_data)
    
    if response.status_code == 401:
        msg = response.json().get('message', 'No message')
        print(f"   ✓ Correctly rejected: {msg}")
    else:
        print(f"   ❌ Should have been rejected. Got: {response.status_code}")
        return False
    
    # Step 5: User 2 tries to update User 1's place
    print("\n5. User 2 (Bob) attempting to update Alice's place...")
    
    update_data = {'title': 'Hacked Title'}
    response = requests.put(
        f'{BASE_URL}/places/{place_id}',
        json=update_data,
        headers=headers2
    )
    
    if response.status_code == 403:
        try:
            msg = response.json().get('message', 'Forbidden')
            print(f"   ✓ Correctly forbidden: {msg}")
        except:
            print(f"   ✓ Correctly forbidden (status 403)")
    else:
        print(f"   ❌ Should have been forbidden. Got: {response.status_code}")
        return False
    
    # Step 6: User 1 updates their own place
    print("\n6. User 1 (Alice) updating their own place...")
    
    update_data = {'title': 'Alice Updated Apartment', 'price': 120.0}
    response = requests.put(
        f'{BASE_URL}/places/{place_id}',
        json=update_data,
        headers=headers1
    )
    
    if response.status_code == 200:
        updated_place = response.json()
        print(f"   ✓ Place updated successfully")
        print(f"   New title: {updated_place.get('title', 'N/A')}")
    else:
        print(f"   ❌ Update failed: {response.status_code}")
        print(f"   Response: {response.text}")
        return False

    # Step 7: User 1 tries to review their own place
    print("\n7. User 1 (Alice) attempting to review their own place...")
    
    review_data = {
        'rating': 5,
        'comment': 'My own place is great!',
        'place_id': place_id
    }
    
    response = requests.post(f'{BASE_URL}/reviews/', json=review_data, headers=headers1)
    
    if response.status_code == 400:
        msg = response.json().get('message', 'Bad request')
        print(f"   ✓ Correctly rejected: {msg}")
    else:
        print(f"   ❌ Should have been rejected. Got: {response.status_code}")
        return False
    
    # Step 8: User 2 creates a review for User 1's place
    print("\n8. User 2 (Bob) creating a review for Alice's place...")
    
    review_data = {
        'rating': 4,
        'comment': 'Nice place, would recommend!',
        'place_id': place_id
    }
    
    response = requests.post(f'{BASE_URL}/reviews/', json=review_data, headers=headers2)
    
    if response.status_code == 201:
        review = response.json()
        review_id = review['id']
        print(f"   ✓ Review created by Bob")
        print(f"   Rating: {review['rating']}")
    else:
        print(f"   ❌ Failed to create review: {response.status_code}")
        print(f"   Response: {response.text}")
        return False
    
    # Step 9: User 2 tries to review the same place again
    print("\n9. User 2 (Bob) attempting to review same place again...")
    
    response = requests.post(f'{BASE_URL}/reviews/', json=review_data, headers=headers2)
    
    if response.status_code == 400:
        msg = response.json().get('message', 'Bad request')
        print(f"   ✓ Correctly rejected: {msg}")
    else:
        print(f"   ❌ Should have been rejected. Got: {response.status_code}")
        return False
    
    # Step 10: User 1 tries to update User 2's review
    print("\n10. User 1 (Alice) attempting to update Bob's review...")
    
    update_review_data = {'rating': 3, 'comment': 'Changed comment'}
    response = requests.put(
        f'{BASE_URL}/reviews/{review_id}',
        json=update_review_data,
        headers=headers1
    )
    
    # Accept both 400 and 403 as valid rejection codes
    if response.status_code in [400, 403]:
        msg = response.json().get('message', 'Forbidden')
        print(f"   ✓ Correctly rejected (status {response.status_code}): {msg}")
    else:
        print(f"   ❌ Should have been rejected. Got: {response.status_code}")
        return False
    
    # Step 11: User 2 updates their own review
    print("\n11. User 2 (Bob) updating their own review...")
    
    update_review_data = {'rating': 5, 'comment': 'Actually, it is perfect!'}
    response = requests.put(
        f'{BASE_URL}/reviews/{review_id}',
        json=update_review_data,
        headers=headers2
    )
    
    if response.status_code == 200:
        updated_review = response.json()
        print(f"   ✓ Review updated successfully")
        print(f"   New rating: {updated_review['rating']}")
    else:
        print(f"   ❌ Update failed: {response.status_code}")
        return False
    
    # Step 12: Public access to places (no auth)
    print("\n12. Testing public access to GET /places/...")
    
    response = requests.get(f'{BASE_URL}/places/')
    
    if response.status_code == 200:
        places = response.json()
        print(f"   ✓ Public access granted")
        print(f"   Found {len(places)} place(s)")
    else:
        print(f"   ❌ Public access failed: {response.status_code}")
        return False
    
    # Step 13: Public access to reviews (no auth)
    print("\n13. Testing public access to GET /reviews/...")
    
    response = requests.get(f'{BASE_URL}/reviews/')
    
    if response.status_code == 200:
        reviews = response.json()
        print(f"   ✓ Public access granted")
        print(f"   Found {len(reviews)} review(s)")
    else:
        print(f"   ❌ Public access failed: {response.status_code}")
        return False
    
    print("\n" + "="*70)
    print("✅ ALL AUTHENTICATED ENDPOINT TESTS PASSED")
    print("="*70 + "\n")
    return True


if __name__ == '__main__':
    print("\nMake sure the server is running on http://localhost:5001")
    print("Press Ctrl+C to cancel, or Enter to continue...")
    input()
    
    test_authenticated_endpoints()
