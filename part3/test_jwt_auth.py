"""
Test JWT authentication functionality.
"""
import requests
import json

BASE_URL = 'http://localhost:5001/api'


def test_jwt_authentication():
    """Test JWT login and protected endpoints."""
    
    print("\n" + "="*60)
    print("TESTING JWT AUTHENTICATION")
    print("="*60 + "\n")
    
    # Step 1: Register a new user
    print("1. Registering new user...")
    user_data = {
        'first_name': 'Jane',
        'last_name': 'Smith',
        'email': 'jane.jwt@test.com',
        'password': 'SecurePass123!'
    }
    
    response = requests.post(f'{BASE_URL}/users', json=user_data)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 201:
        user = response.json()
        user_id = user['id']
        print(f"   ✓ User created: {user['email']}")
    else:
        print(f"   ❌ Failed to create user: {response.json()}")
        return False
    
    # Step 2: Login and get JWT token
    print("\n2. Logging in...")
    login_data = {
        'email': 'jane.jwt@test.com',
        'password': 'SecurePass123!'
    }
    
    response = requests.post(f'{BASE_URL}/auth/login', json=login_data)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        login_response = response.json()
        token = login_response['access_token']
        print(f"   ✓ Login successful")
        print(f"   Token (first 50 chars): {token[:50]}...")
        print(f"   User: {login_response['user']['email']}")
    else:
        print(f"   ❌ Login failed: {response.json()}")
        return False
    
    # Step 3: Access protected endpoint WITHOUT token
    print("\n3. Accessing protected endpoint WITHOUT token...")
    response = requests.get(f'{BASE_URL}/users')
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 401:
        print(f"   ✓ Correctly rejected: {response.json()['message']}")
    else:
        print(f"   ❌ Should have been rejected")
        return False
    
    # Step 4: Access protected endpoint WITH valid token
    print("\n4. Accessing protected endpoint WITH valid token...")
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(f'{BASE_URL}/users', headers=headers)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        users = response.json()
        print(f"   ✓ Access granted")
        print(f"   Found {len(users)} user(s)")
    else:
        print(f"   ❌ Access denied: {response.json()}")
        return False
    
    # Step 5: Test protected example endpoint
    print("\n5. Testing /auth/protected endpoint...")
    response = requests.get(f'{BASE_URL}/auth/protected', headers=headers)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Protected endpoint accessible")
        print(f"   Message: {data['message']}")
        print(f"   User ID from token: {data['user_id']}")
    else:
        print(f"   ❌ Failed: {response.json()}")
        return False
    
    # Step 6: Test invalid credentials
    print("\n6. Testing login with invalid password...")
    bad_login = {
        'email': 'jane.jwt@test.com',
        'password': 'WrongPassword'
    }
    response = requests.post(f'{BASE_URL}/auth/login', json=bad_login)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 401:
        print(f"   ✓ Correctly rejected: {response.json()['message']}")
    else:
        print(f"   ❌ Should have rejected invalid credentials")
        return False
    
    # Step 7: Test user update with JWT
    print("\n7. Updating user profile with JWT...")
    update_data = {
        'first_name': 'Janet'
    }
    response = requests.put(
        f'{BASE_URL}/users/{user_id}',
        headers=headers,
        json=update_data
    )
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        updated = response.json()
        print(f"   ✓ Profile updated")
        print(f"   New name: {updated['first_name']} {updated['last_name']}")
    else:
        print(f"   ❌ Update failed: {response.json()}")
        return False
    
    # Step 8: Test updating another user's profile (should fail)
    print("\n8. Attempting to update another user's profile...")
    # First create another user
    other_user_data = {
        'first_name': 'Bob',
        'last_name': 'Jones',
        'email': 'bob@test.com',
        'password': 'BobPass123'
    }
    response = requests.post(f'{BASE_URL}/users', json=other_user_data)
    other_user_id = response.json()['id']
    
    # Try to update Bob's profile with Jane's token
    response = requests.put(
        f'{BASE_URL}/users/{other_user_id}',
        headers=headers,
        json={'first_name': 'Hacked'}
    )
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 403:
        print(f"   ✓ Correctly forbidden: {response.json()['message']}")
    else:
        print(f"   ❌ Should have been forbidden")
        return False
    
    print("\n" + "="*60)
    print("✅ ALL JWT AUTHENTICATION TESTS PASSED")
    print("="*60 + "\n")
    return True


if __name__ == '__main__':
    print("\nMake sure the server is running on http://localhost:5001")
    print("Press Ctrl+C to cancel, or Enter to continue...")
    input()
    
    test_jwt_authentication()
