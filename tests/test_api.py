import pytest
from rest_framework import status
from library.models import User, Book, Loan
from django.utils import timezone
from datetime import timedelta


@pytest.mark.django_db
class TestUserAPI:
    def test_user_list_requires_auth(self, api_client):
        """Test that user list requires authentication"""
        response = api_client.get('/api/users/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_list_authenticated(self, authenticated_client):
        """Test user list with authenticated user"""
        client, user = authenticated_client
        response = client.get('/api/users/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1  # At least the authenticated user

    def test_user_creation(self, api_client):
        """Test user creation via API"""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass123',
            'password_confirm': 'newpass123',
            'first_name': 'New',
            'last_name': 'User',
            'role': 'student'
        }
        response = api_client.post('/api/auth/register/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert 'access' in response.data
        assert 'user' in response.data

    def test_user_login(self, api_client, user_factory):
        """Test user login"""
        user = user_factory.create(username='loginuser', password='loginpass123')
        data = {
            'username': 'loginuser',
            'password': 'loginpass123'
        }
        response = api_client.post('/api/auth/login/', data)
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'user' in response.data


@pytest.mark.django_db
class TestBookAPI:
    def test_book_list_requires_auth(self, api_client):
        """Test that book list requires authentication"""
        response = api_client.get('/api/books/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_book_list_authenticated(self, authenticated_client, book_factory):
        """Test book list with authenticated user"""
        client, user = authenticated_client
        book = book_factory.create()
        response = client.get('/api/books/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_book_creation(self, authenticated_client):
        """Test book creation"""
        client, user = authenticated_client
        data = {
            'title': 'New Book',
            'author': 'New Author',
            'isbn': '9876543210987',
            'category': 'Science',
            'total_quantity': 3
        }
        response = client.post('/api/books/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'New Book'
        assert response.data['available_quantity'] == 3

    def test_book_update(self, authenticated_client, book_factory):
        """Test book update"""
        client, user = authenticated_client
        book = book_factory.create()
        data = {'title': 'Updated Title'}
        response = client.patch(f'/api/books/{book.id}/', data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Title'

    def test_book_deletion(self, authenticated_client, book_factory):
        """Test book deletion"""
        client, user = authenticated_client
        book = book_factory.create()
        response = client.delete(f'/api/books/{book.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_book_filtering(self, authenticated_client, book_factory):
        """Test book filtering"""
        client, user = authenticated_client
        book1 = book_factory.create(category='Fiction')
        book2 = book_factory.create(category='Science')

        response = client.get('/api/books/?category=Fiction')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['category'] == 'Fiction'

    def test_book_search(self, authenticated_client, book_factory):
        """Test book search"""
        client, user = authenticated_client
        book = book_factory.create(title='Python Programming')

        response = client.get('/api/books/?search=Python')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1
        assert 'Python' in response.data[0]['title']


@pytest.mark.django_db
class TestLoanAPI:
    def test_loan_list_requires_auth(self, api_client):
        """Test that loan list requires authentication"""
        response = api_client.get('/api/loans/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_loan_creation(self, authenticated_client, book_factory):
        """Test loan creation (borrow book)"""
        client, user = authenticated_client
        book = book_factory.create(available_quantity=2)

        data = {'book_id': book.id}
        response = client.post('/api/loans/borrow/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert 'id' in response.data

    def test_loan_creation_unavailable_book(self, authenticated_client, book_factory):
        """Test borrowing unavailable book"""
        client, user = authenticated_client
        book = book_factory.create(available_quantity=0)

        data = {'book_id': book.id}
        response = client.post('/api/loans/borrow/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_loan_return(self, authenticated_client):
        """Test loan return"""
        client, user = authenticated_client
        # Get user's first loan
        response = client.get('/api/loans/my_loans/')
        assert response.status_code == status.HTTP_200_OK

    def test_my_loans(self, authenticated_client, book_factory):
        """Test getting user's own loans"""
        client, user = authenticated_client
        book = book_factory.create()

        # Create a loan for the user
        loan = Loan.objects.create(
            user=user,
            book=book,
            due_date=timezone.now() + timedelta(days=14)
        )

        response = client.get('/api/loans/my_loans/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['id'] == loan.id

    def test_overdue_loans_librarian_only(self, authenticated_client):
        """Test that overdue loans endpoint requires librarian role"""
        client, user = authenticated_client
        # User is student by default
        response = client.get('/api/loans/overdue/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_overdue_loans_librarian(self, authenticated_client, user_factory, book_factory):
        """Test overdue loans for librarian"""
        # Create librarian user
        librarian = user_factory.create(role='librarian', username='librarian')
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(librarian)
        client = authenticated_client[0]  # Get the client
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        # Create an overdue loan
        student = user_factory.create(username='student')
        book = book_factory.create()
        past_date = timezone.now() - timedelta(days=1)
        Loan.objects.create(
            user=student,
            book=book,
            due_date=past_date
        )

        response = client.get('/api/loans/overdue/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1


@pytest.mark.django_db
class TestChatAPI:
    def test_chat_recommend_requires_auth(self, api_client):
        """Test that chat endpoint requires authentication"""
        data = {'query': 'science books'}
        response = api_client.post('/api/chat/recommend/', data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_chat_recommend_empty_query(self, authenticated_client):
        """Test chat with empty query"""
        client, user = authenticated_client
        data = {'query': ''}
        response = client.post('/api/chat/recommend/', data)
        assert response.status_code == status.HTTP_200_OK
        assert 'message' in response.data
        assert response.data['suggestions'] == []

    def test_chat_recommend_with_results(self, authenticated_client, book_factory):
        """Test chat recommendation with results"""
        client, user = authenticated_client
        # Create test books
        book = book_factory.create(
            title='Python Programming',
            category='Technology',
            available_quantity=2
        )

        data = {'query': 'python programming'}
        response = client.post('/api/chat/recommend/', data)
        assert response.status_code == status.HTTP_200_OK
        assert 'message' in response.data
        assert 'suggestions' in response.data
        assert len(response.data['suggestions']) >= 1
        assert response.data['suggestions'][0]['title'] == 'Python Programming'

    def test_chat_recommend_by_category(self, authenticated_client, book_factory):
        """Test chat recommendation by category"""
        client, user = authenticated_client
        # Create test books with different categories
        book_fiction = book_factory.create(category='Fiction', available_quantity=1)
        book_science = book_factory.create(category='Science', available_quantity=1)

        data = {'query': 'fiction'}
        response = client.post('/api/chat/recommend/', data)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['suggestions']) >= 1
        assert response.data['suggestions'][0]['category'] == 'Fiction'

    def test_chat_recommend_no_results(self, authenticated_client):
        """Test chat recommendation with no results"""
        client, user = authenticated_client
        data = {'query': 'nonexistentbookquery123'}
        response = client.post('/api/chat/recommend/', data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['suggestions'] == []
        assert 'couldn\'t find' in response.data['message'].lower()