"""
Test Place CRUD endpoints.
"""
import requests

BASE_URL = 'http://localhost:5001/api'


def test_place_endpoints():
    """Test all place CRUD operations."""
    
    print("\n" + "="*70)
    print("TESTING PLACE CRUD ENDPOINTS")
    print("="*70 + "\n")
    
    # Step 1: Create a user and login
    print("1. Creating user and logging in...")
    
    user_data = {
        'first_name': 'John',
        'last_name': 'Host',
        'email': 'john.host@test.com',
        'password': 'JohnPass123'
    }
    
    response = requests.post(f'{BASE_URL}/users/', json=user_data)
    if response.status_code != 201:
        print(f"   ❌ Failed to create user: {response.json()}")
        return False
    
    user = response.json()
    print(f"   ✓ User created: {user['email']}")
    
    # Login
    login_response = requests.post(f'{BASE_URL}/auth/login', json={
        'email': 'john.host@test.com',
        'password': 'JohnPass123'
    })
    
    if login_response.status_code != 200:
        print(f"   ❌ Login failed")
        return False
    
    token = login_response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    print(f"   ✓ User logged in")
    
    # Step 2: Create a place with valid data
    print("\n2. Creating place with valid data...")
    
    place_data = {
        'title': 'Cozy Beach House',
        'description': 'Beautiful beachfront property with amazing sunset views',
        'price': 150.00,
        'latitude': 34.0522,
        'longitude': -118.2437
    }
    
    response = requests.post(f'{BASE_URL}/places/', json=place_data, headers=headers)
    
    if response.status_code == 201:
        place = response.json()
        place_id = place['id']
        print(f"   ✓ Place created: {place['title']}")
        print(f"   ID: {place_id}")
        print(f"   Price: ${place['price']}")
        print(f"   Location: ({place.get('latitude')}, {place.get('longitude')})")
    else:
        print(f"   ❌ Failed: {response.status_code} - {response.text}")
        return False
    
    # Step 3: Try to create place with invalid price
    print("\n3. Testing validation: negative price...")
    
    invalid_price_data = {
        'title': 'Invalid Price Place',
        'description': 'This should fail',
        'price': -50.00,
        'latitude': 40.7128,
        'longitude': -74.0060
    }
    
    response = requests.post(f'{BASE_URL}/places/', json=invalid_price_data, headers=headers)
    
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.text}")

    if response.status_code == 400:
        try:
            msg = response.json().get('message', 'Bad request')
            print(f"   ✓ Correctly rejected: {msg}")
        except:
            print(f"   ✓ Correctly rejected (status 400)")
    else:
        print(f"   ❌ Should have been rejected. Got: {response.status_code}")
        return False
    
    # Step 4: Try to create place with invalid latitude
    print("\n4. Testing validation: invalid latitude...")
    
    invalid_lat_data = {
        'title': 'Invalid Latitude Place',
        'description': 'This should fail',
        'price': 100.00,
        'latitude': 95.0,  # > 90
        'longitude': -74.0060
    }
    
    response = requests.post(f'{BASE_URL}/places/', json=invalid_lat_data, headers=headers)
    
    print(f"   Status: {response.status_code}")

    if response.status_code == 400:
        try:
            msg = response.json().get('message', 'Bad request')
            print(f"   ✓ Correctly rejected: {msg}")
        except:
            print(f"   ✓ Correctly rejected (status 400)")
    else:
        print(f"   ❌ Should have been rejected")
        return False
    
    # Step 5: Try to create place with invalid longitude
    print("\n5. Testing validation: invalid longitude...")
    
    invalid_lon_data = {
        'title': 'Invalid Longitude Place',
        'description': 'This should fail',
        'price': 100.00,
        'latitude': 40.7128,
        'longitude': -200.0  # < -180
    }
    
    response = requests.post(f'{BASE_URL}/places/', json=invalid_lon_data, headers=headers)
    
    print(f"   Status: {response.status_code}")

    if response.status_code == 400:
        try:
            msg = response.json().get('message', 'Bad request')
            print(f"   ✓ Correctly rejected: {msg}")
        except:
            print(f"   ✓ Correctly rejected (status 400)")
    else:
        print(f"   ❌ Should have been rejected")
        return False
    
    # Step 6: Get place details
    print("\n6. Getting place details...")
    
    response = requests.get(f'{BASE_URL}/places/{place_id}')
    
    if response.status_code == 200:
        place_details = response.json()
        print(f"   ✓ Place retrieved successfully")
        print(f"   Title: {place_details['title']}")
        
        owner = place_details.get('owner')
        if owner:
            print(f"   Owner: {owner.get('first_name')} {owner.get('last_name')}")
        
        print(f"   Amenities: {len(place_details.get('amenities', []))}")
        print(f"   Reviews: {len(place_details.get('reviews', []))}")
    else:
        print(f"   ❌ Failed: {response.status_code}")
        return False
    
    # Step 7: Update place
    print("\n7. Updating place...")
    
    update_data = {
        'title': 'Luxury Beach House',
        'price': 200.00
    }
    
    response = requests.put(f'{BASE_URL}/places/{place_id}', json=update_data, headers=headers)
    
    if response.status_code == 200:
        updated_place = response.json()
        print(f"   ✓ Place updated successfully")
        print(f"   New title: {updated_place['title']}")
        print(f"   New price: ${updated_place['price']}")
    else:
        print(f"   ❌ Failed: {response.json()}")
        return False
    
    # Step 8: List all places
    print("\n8. Listing all places...")
    
    response = requests.get(f'{BASE_URL}/places/')
    
    if response.status_code == 200:
        places = response.json()
        print(f"   ✓ Retrieved {len(places)} place(s)")
        for p in places:
            print(f"      - {p['title']}: ${p['price']}")
    else:
        print(f"   ❌ Failed: {response.json()}")
        return False
    
    # Step 9: Try to create place without authentication
    print("\n9. Testing authentication requirement...")
    
    response = requests.post(f'{BASE_URL}/places/', json=place_data)
    
    if response.status_code == 401:
        try:
            msg = response.json().get('message', 'Unauthorized')
            print(f"   ✓ Correctly rejected: {msg}")
        except:
            print(f"   ✓ Correctly rejected (status 401)")
    else:
        print(f"   ❌ Should have required authentication")
        return False
    
    # Step 10: Create another user and try to update first user's place
    print("\n10. Testing ownership validation...")
    
    user2_data = {
        'first_name': 'Jane',
        'last_name': 'User',
        'email': 'jane@test.com',
        'password': 'JanePass123'
    }
    
    requests.post(f'{BASE_URL}/users/', json=user2_data)
    
    login2 = requests.post(f'{BASE_URL}/auth/login', json={
        'email': 'jane@test.com',
        'password': 'JanePass123'
    })
    
    token2 = login2.json()['access_token']
    headers2 = {'Authorization': f'Bearer {token2}'}
    
    response = requests.put(
        f'{BASE_URL}/places/{place_id}',
        json={'title': 'Hacked'},
        headers=headers2
    )
    
    if response.status_code == 403:
        try:
            msg = response.json().get('message', 'Forbidden')
            print(f"   ✓ Correctly forbidden: {msg}")
        except:
            print(f"   ✓ Correctly forbidden (status 403)")
    else:
        print(f"   ❌ Should have been forbidden")
        return False
    
    print("\n" + "="*70)
    print("✅ ALL PLACE ENDPOINT TESTS PASSED")
    print("="*70 + "\n")
    return True


if __name__ == '__main__':
    print("\nMake sure the server is running on http://localhost:5001")
    print("Press Ctrl+C to cancel, or Enter to continue...")
    input()
    
    test_place_endpoints()
