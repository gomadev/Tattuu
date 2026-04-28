"""Testes básicos da API."""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, SessionLocal, engine

Base.metadata.create_all(bind=engine)
client = TestClient(app)


def test_root_endpoint():
    """Testa endpoint raiz."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Tattuu API"


def test_health_check():
    """Testa health check."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_register_user():
    """Testa registro de novo usuário."""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "password": "password123"
    }
    response = client.post("/api/v1/users/register", json=user_data)
    assert response.status_code == 201
    assert response.json()["email"] == user_data["email"]
    assert response.json()["username"] == user_data["username"]


def test_list_artists():
    """Testa listagem de tatuadores."""
    response = client.get("/api/v1/artists/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
