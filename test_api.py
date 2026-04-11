import requests

BASE_URL = 'http://127.0.0.1:8000/api'

def test_api():
    print("Testing API endpoints...")

    # Test books endpoint
    try:
        response = requests.get(f'{BASE_URL}/books/')
        if response.status_code == 200:
            books = response.json()
            print(f"✓ Books endpoint: {len(books)} books found")
        else:
            print(f"✗ Books endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Books endpoint error: {e}")

    # Test users endpoint
    try:
        response = requests.get(f'{BASE_URL}/users/')
        if response.status_code == 200:
            users = response.json()
            print(f"✓ Users endpoint: {len(users)} users found")
        else:
            print(f"✗ Users endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Users endpoint error: {e}")

    # Test loans endpoint
    try:
        response = requests.get(f'{BASE_URL}/loans/')
        if response.status_code == 200:
            loans = response.json()
            print(f"✓ Loans endpoint: {len(loans)} loans found")
        else:
            print(f"✗ Loans endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Loans endpoint error: {e}")

    print("API testing completed!")

if __name__ == '__main__':
    test_api()