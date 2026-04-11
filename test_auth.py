#!/usr/bin/env python
# Test authentication API endpoints

import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_register():
    """Test user registration"""
    print("Testing user registration...")
    data = {
        "username": "testuser2",
        "email": "test2@example.com",
        "password": "testpass123",
        "password_confirm": "testpass123",
        "first_name": "Test",
        "last_name": "User",
        "role": "student"
    }

    response = requests.post(f"{BASE_URL}/auth/register/", json=data)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        result = response.json()
        print("Registration successful!")
        return result.get('access'), result.get('refresh')
    else:
        print(f"Error: {response.text}")
        return None, None

def test_login():
    """Test user login"""
    print("\nTesting user login...")
    data = {
        "username": "testuser2",
        "password": "testpass123"
    }

    response = requests.post(f"{BASE_URL}/auth/login/", json=data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print("Login successful!")
        return result.get('access'), result.get('refresh')
    else:
        print(f"Error: {response.text}")
        return None, None

def test_me(access_token):
    """Test get current user info"""
    print("\nTesting get current user...")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/auth/me/", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("User info retrieved successfully!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.text}")

def test_logout(refresh_token):
    """Test user logout"""
    print("\nTesting user logout...")
    data = {"refresh": refresh_token}
    response = requests.post(f"{BASE_URL}/auth/logout/", json=data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("Logout successful!")
    else:
        print(f"Error: {response.text}")

def test_protected_endpoint(access_token):
    """Test accessing protected endpoint"""
    print("\nTesting protected endpoint (books)...")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/books/", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        books = response.json()
        print(f"Retrieved {len(books)} books successfully!")
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    print("Testing Authentication API")
    print("=" * 40)

    # Test registration
    access_token, refresh_token = test_register()

    if access_token:
        # Test login
        access_token, refresh_token = test_login()

        if access_token:
            # Test protected endpoints
            test_me(access_token)
            test_protected_endpoint(access_token)

            # Test logout
            test_logout(refresh_token)

            # Test accessing protected endpoint after logout
            print("\nTesting protected endpoint after logout...")
            test_protected_endpoint(access_token)
        else:
            print("Login failed, skipping further tests")
    else:
        print("Registration failed, trying login with existing user...")
        access_token, refresh_token = test_login()
        if access_token:
            test_me(access_token)
            test_protected_endpoint(access_token)