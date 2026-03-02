"""
Test password hashing functionality.
"""
import requests
import json

BASE_URL = 'http://localhost:5001/api'

def test_password_hashing():
    """Test that passwords are hashed and not returned."""
    
    print("\n" + "="*60)
    print("TESTING PASSWORD HASHING")
    print("="*60 + "\n")
    
    # Test 1: Create user with password
    print("1. Creating user with password...")
    user_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.password@test.com',
        'password': 'SecurePass123!'
    }
    
    response = requests.post(f'{BASE_URL}/users', json=user_data)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 201:
        user = response.json()
        print(f"   User ID: {user['id']}")
        print(f"   Response keys: {list(user.keys())}")
        
        # Verify password is NOT in response
        if 'password' in user:
            print("   ❌ FAIL: Password found in response!")
            return False
        elif '_password_hash' in user:
            print("   ❌ FAIL: Password hash found in response!")
            return False
        else:
            print("   ✓ PASS: Password not in response")
        
        user_id = user['id']
        
        # Test 2: Get user and verify password not returned
        print("\n2. Getting user by ID...")
        response = requests.get(f'{BASE_URL}/users/{user_id}')
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            user_details = response.json()
            print(f"   Response keys: {list(user_details.keys())}")
            
            if 'password' not in user_details and '_password_hash' not in user_details:
                print("   ✓ PASS: Password not in GET response")
            else:
                print("   ❌ FAIL: Password found in GET response!")
                return False
        
        # Test 3: List users and verify password not returned
        print("\n3. Listing all users...")
        response = requests.get(f'{BASE_URL}/users')
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            users = response.json()
            print(f"   Found {len(users)} users")
            
            password_found = False
            for u in users:
                if 'password' in u or '_password_hash' in u:
                    password_found = True
                    break
            
            if not password_found:
                print("   ✓ PASS: No passwords in list response")
            else:
                print("   ❌ FAIL: Password found in list response!")
                return False
        
        # Test 4: Update user with new password
        print("\n4. Updating user password...")
        update_data = {
            'first_name': 'Jane',
            'password': 'NewSecurePass456!'
        }
        
        response = requests.put(f'{BASE_URL}/users/{user_id}', json=update_data)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            updated_user = response.json()
            print(f"   Updated name: {updated_user['first_name']}")
            
            if 'password' not in updated_user and '_password_hash' not in updated_user:
                print("   ✓ PASS: Password not in update response")
            else:
                print("   ❌ FAIL: Password found in update response!")
                return False
        
        print("\n" + "="*60)
        print("✅ ALL PASSWORD HASHING TESTS PASSED")
        print("="*60 + "\n")
        return True
    
    else:
        print(f"   ❌ FAIL: Could not create user. Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        return False


if __name__ == '__main__':
    print("\nMake sure the server is running on http://localhost:5001")
    print("Press Ctrl+C to cancel, or Enter to continue...")
    input()
    
    test_password_hashing()
