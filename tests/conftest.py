import pytest
import django
from django.conf import settings

# Configure Django settings
if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY='test-secret-key',
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'rest_framework',
            'rest_framework_simplejwt',
            'rest_framework_simplejwt.token_blacklist',
            'corsheaders',
            'django_filters',
            'library',
        ],
        ROOT_URLCONF='thuvienso_backend.urls',
        USE_TZ=True,
        AUTH_USER_MODEL='library.User',
        REST_FRAMEWORK={
            'DEFAULT_AUTHENTICATION_CLASSES': [
                'rest_framework_simplejwt.authentication.JWTAuthentication',
            ],
            'DEFAULT_PERMISSION_CLASSES': [
                'rest_framework.permissions.IsAuthenticated',
            ]
        }
    )
    django.setup()

@pytest.fixture
def api_client():
    """API client fixture for testing"""
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def user_factory():
    """Factory for creating test users"""
    from library.models import User

    class UserFactory:
        def create(self, **kwargs):
            defaults = {
                'username': 'testuser',
                'email': 'test@example.com',
                'role': 'student'
            }
            defaults.update(kwargs)
            if 'password' not in defaults:
                defaults['password'] = 'testpass123'
            return User.objects.create_user(**defaults)

    return UserFactory()

@pytest.fixture
def book_factory():
    """Factory for creating test books"""
    from library.models import Book
    import random

    class BookFactory:
        def __init__(self):
            self.isbn_counter = 1000000000000  # Start from 13-digit number

        def create(self, **kwargs):
            self.isbn_counter += 1
            defaults = {
                'title': 'Test Book',
                'author': 'Test Author',
                'isbn': str(self.isbn_counter),
                'category': 'Fiction',
                'total_quantity': 5,
                'available_quantity': 5
            }
            defaults.update(kwargs)
            return Book.objects.create(**defaults)

    return BookFactory()

@pytest.fixture
def authenticated_client(api_client, user_factory, transactional_db):
    """API client with authenticated user"""
    user = user_factory.create()
    from rest_framework_simplejwt.tokens import RefreshToken
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client, user