import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database.database import engine
from sqlmodel import SQLModel, Session
from src.models.user import User
from unittest.mock import patch

client = TestClient(app)

def test_register_user():
    """Test user registration"""
    # Use a unique email for this test
    response = client.post(
        "/auth/register",
        json={
            "email": "test_unique@example.com",
            "password": "testpassword123",
            "password_confirm": "testpassword123",
            "first_name": "Test",
            "last_name": "User"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test_unique@example.com"
    assert data["first_name"] == "Test"
    assert "id" in data

def test_register_duplicate_email():
    """Test registration with duplicate email"""
    # First registration should succeed
    client.post(
        "/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "testpassword123",
            "password_confirm": "testpassword123",
            "first_name": "Test",
            "last_name": "User"
        }
    )

    # Second registration with same email should fail
    response = client.post(
        "/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "anotherpassword123",
            "password_confirm": "anotherpassword123",
            "first_name": "Another",
            "last_name": "User"
        }
    )
    assert response.status_code == 409

def test_login_valid_credentials():
    """Test login with valid credentials"""
    # First register a user
    client.post(
        "/auth/register",
        json={
            "email": "login_test@example.com",
            "password": "testpassword123",
            "password_confirm": "testpassword123",
            "first_name": "Login",
            "last_name": "Test"
        }
    )

    # Then try to login - use params for query parameters
    response = client.post(
        "/auth/login",
        params={
            "email": "login_test@example.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "user" in data

def test_login_invalid_credentials():
    """Test login with invalid credentials"""
    response = client.post(
        "/auth/login",
        params={
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 400

def test_logout():
    """Test logout endpoint"""
    response = client.post("/auth/logout")
    assert response.status_code == 200
    assert response.json()["message"] == "Logged out successfully"

def test_register_long_password():
    """Test registration with a password longer than 72 bytes"""
    # Create a password longer than 72 bytes (using ASCII characters)
    long_password = "a" * 73  # 73 bytes, exceeding the limit
    
    response = client.post(
        "/auth/register",
        json={
            "email": "longpass@example.com",
            "password": long_password,
            "password_confirm": long_password,
            "first_name": "Long",
            "last_name": "Password"
        }
    )
    assert response.status_code == 400
    assert "72 bytes" in response.json()["detail"]

def test_register_long_password_with_unicode():
    """Test registration with a password that's short in characters but long in bytes due to unicode"""
    # A password with 25 characters but >72 bytes due to multi-byte unicode characters
    unicode_password = "🔑🔒🔐" * 10  # Each emoji is typically 4 bytes in UTF-8, so ~120 bytes total
    
    response = client.post(
        "/auth/register",
        json={
            "email": "unicodepass@example.com",
            "password": unicode_password,
            "password_confirm": unicode_password,
            "first_name": "Unicode",
            "last_name": "Password"
        }
    )
    assert response.status_code == 400
    assert "72 bytes" in response.json()["detail"]