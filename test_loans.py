#!/usr/bin/env python
# Test loan API endpoints

import requests
import json

BASE_URL = "http://localhost:8000/api"

def login_and_get_token():
    """Login and get access token"""
    data = {
        "username": "testuser2",
        "password": "testpass123"
    }

    response = requests.post(f"{BASE_URL}/auth/login/", json=data)
    if response.status_code == 200:
        result = response.json()
        return result.get('access'), result.get('user')
    else:
        print(f"Login failed: {response.text}")
        return None, None

def test_borrow_book(access_token, user):
    """Test borrowing a book"""
    print("\nTesting book borrowing...")

    # Get first available book
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/books/", headers=headers)

    if response.status_code != 200:
        print(f"Failed to get books: {response.text}")
        return

    books = response.json()
    available_book = None
    for book in books:
        if book['available_quantity'] > 0:
            available_book = book
            break

    if not available_book:
        print("No available books found")
        return

    print(f"Borrowing book: {available_book['title']}")

    # Borrow the book
    data = {"book_id": available_book['id']}
    response = requests.post(f"{BASE_URL}/loans/borrow/", json=data, headers=headers)

    print(f"Borrow status: {response.status_code}")
    if response.status_code == 201:
        loan = response.json()
        print("Book borrowed successfully!")
        print(json.dumps(loan, indent=2, default=str))
        return loan['id']
    else:
        print(f"Borrow failed: {response.text}")
        return None

def test_get_my_loans(access_token):
    """Test getting user's loans"""
    print("\nTesting get my loans...")

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/loans/my_loans/", headers=headers)

    print(f"My loans status: {response.status_code}")
    if response.status_code == 200:
        loans = response.json()
        print(f"Found {len(loans)} loans")
        for loan in loans:
            print(f"- {loan['book']['title']} ({loan['status']})")
    else:
        print(f"Get loans failed: {response.text}")

def test_return_book(access_token, loan_id):
    """Test returning a book"""
    print(f"\nTesting return book (loan ID: {loan_id})...")

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.post(f"{BASE_URL}/loans/{loan_id}/return_book/", headers=headers)

    print(f"Return status: {response.status_code}")
    if response.status_code == 200:
        loan = response.json()
        print("Book returned successfully!")
        print(json.dumps(loan, indent=2, default=str))
    else:
        print(f"Return failed: {response.text}")

def test_get_all_loans(access_token, user):
    """Test getting all loans (librarian only)"""
    print("\nTesting get all loans...")

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/loans/", headers=headers)

    print(f"All loans status: {response.status_code}")
    if response.status_code == 200:
        loans = response.json()
        print(f"Found {len(loans)} total loans")
    else:
        print(f"Get all loans failed: {response.text}")

if __name__ == "__main__":
    print("Testing Loan API")
    print("=" * 40)

    # Login first
    access_token, user = login_and_get_token()

    if access_token:
        # Test borrowing
        loan_id = test_borrow_book(access_token, user)

        # Test getting my loans
        test_get_my_loans(access_token)

        # Test getting all loans
        test_get_all_loans(access_token, user)

        # Test returning if we borrowed a book
        if loan_id:
            test_return_book(access_token, loan_id)

            # Check loans again after return
            test_get_my_loans(access_token)
    else:
        print("Authentication failed, cannot test loan functionality")