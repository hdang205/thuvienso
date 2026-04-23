import os
import pytest
from rest_framework import status


@pytest.mark.django_db
class TestEmailLogin:
    def test_login_with_email(self, api_client, user_factory):
        """User can log in using email address"""
        user = user_factory.create(
            username="emailuser",
            email="emailuser@example.com",
            password="testpass123",
        )
        data = {"email": "emailuser@example.com", "password": "testpass123"}
        response = api_client.post("/api/auth/login/", data)
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "user" in response.data

    def test_login_with_username_still_works(self, api_client, user_factory):
        """Username-based login is still supported for backward compatibility"""
        user = user_factory.create(
            username="backcompat",
            email="backcompat@example.com",
            password="testpass123",
        )
        data = {"username": "backcompat", "password": "testpass123"}
        response = api_client.post("/api/auth/login/", data)
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data

    def test_login_wrong_password(self, api_client, user_factory):
        """Login with correct email but wrong password returns 400"""
        user = user_factory.create(
            username="wrongpass",
            email="wrongpass@example.com",
            password="correctpass",
        )
        data = {"email": "wrongpass@example.com", "password": "wrongpass"}
        response = api_client.post("/api/auth/login/", data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_nonexistent_email(self, api_client):
        """Login with email that does not exist returns 400"""
        data = {"email": "nobody@example.com", "password": "somepass"}
        response = api_client.post("/api/auth/login/", data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_missing_credentials(self, api_client):
        """Login without email or username returns 400"""
        data = {"password": "somepass"}
        response = api_client.post("/api/auth/login/", data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_missing_password(self, api_client):
        """Login without password returns 400"""
        data = {"email": "test@example.com"}
        response = api_client.post("/api/auth/login/", data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestEnsureAdminUserCommand:
    def test_creates_admin_from_env(self, monkeypatch):
        """Command creates a new admin when env vars are set"""
        from django.core.management import call_command
        from library.models import User

        monkeypatch.setenv("ADMIN_EMAIL", "admin@library.edu")
        monkeypatch.setenv("ADMIN_PASSWORD", "StrongAdminPass#1")
        monkeypatch.setenv("ADMIN_USERNAME", "admin_lib")
        monkeypatch.setenv("ADMIN_FIRST_NAME", "Admin")
        monkeypatch.setenv("ADMIN_LAST_NAME", "Library")

        call_command("ensure_admin_user")

        user = User.objects.get(email="admin@library.edu")
        assert user.username == "admin_lib"
        assert user.first_name == "Admin"
        assert user.last_name == "Library"
        assert user.is_staff is True
        assert user.is_superuser is True
        assert user.check_password("StrongAdminPass#1")

    def test_updates_existing_admin(self, monkeypatch, user_factory):
        """Command updates an existing admin's password when user already exists"""
        from django.core.management import call_command
        from library.models import User

        user_factory.create(
            username="admin_lib",
            email="admin@library.edu",
            password="OldPass#99",
        )

        monkeypatch.setenv("ADMIN_EMAIL", "admin@library.edu")
        monkeypatch.setenv("ADMIN_PASSWORD", "NewStrongPass#2")

        call_command("ensure_admin_user")

        user = User.objects.get(email="admin@library.edu")
        assert user.is_staff is True
        assert user.is_superuser is True
        assert user.check_password("NewStrongPass#2")

    def test_missing_env_vars_does_nothing(self, monkeypatch):
        """Command exits gracefully when required env vars are missing"""
        from django.core.management import call_command
        from library.models import User

        monkeypatch.delenv("ADMIN_EMAIL", raising=False)
        monkeypatch.delenv("ADMIN_PASSWORD", raising=False)

        call_command("ensure_admin_user")

        assert not User.objects.filter(is_superuser=True).exists()

    def test_default_username_is_email(self, monkeypatch):
        """ADMIN_USERNAME defaults to ADMIN_EMAIL when not set"""
        from django.core.management import call_command
        from library.models import User

        monkeypatch.setenv("ADMIN_EMAIL", "defaultuser@library.edu")
        monkeypatch.setenv("ADMIN_PASSWORD", "StrongPass#3")
        monkeypatch.delenv("ADMIN_USERNAME", raising=False)

        call_command("ensure_admin_user")

        user = User.objects.get(email="defaultuser@library.edu")
        assert user.username == "defaultuser@library.edu"
