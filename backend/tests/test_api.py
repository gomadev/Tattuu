"""Testes básicos da API."""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, SessionLocal, engine

Base.metadata.create_all(bind=engine)
client = TestClient(app)

# Dados reutilizáveis para testes
usuario_teste = {
    "email": "test@example.com",
    "username": "testuser",
    "full_name": "Test User",
    "password": "password123"
}

artista_teste = {
    "user_id": 1,
    "bio": "Tatuador profissional com experiência",
    "location": "São Paulo",
    "years_experience": 5,
    "style_ids": []
}

portfolio_teste = {
    "artist_id": 1,
    "title": "Tatuagem Dragão",
    "description": "Dragão em estilo oriental",
    "image_url": "https://example.com/dragon.jpg"
}

avaliacao_teste = {
    "user_id": 1,
    "artist_id": 1,
    "score": 5.0,
    "comment": "Excelente trabalho!"
}


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Tattuu API"


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_register_user():
    response = client.post("/api/v1/users/register", json=usuario_teste)
    assert response.status_code == 201
    assert response.json()["email"] == usuario_teste["email"]


def test_login_user():
    client.post("/api/v1/users/register", json=usuario_teste)
    
    login_data = {
        "username": usuario_teste["username"],
        "password": usuario_teste["password"]
    }
    response = client.post("/api/v1/users/login", json=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_list_artists():
    response = client.get("/api/v1/artists/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_artist():
    client.post("/api/v1/users/register", json=usuario_teste)
    
    response = client.post("/api/v1/artists/", json=artista_teste)
    assert response.status_code == 201
    assert response.json()["location"] == artista_teste["location"]


def test_create_portfolio():
    client.post("/api/v1/users/register", json=usuario_teste)
    client.post("/api/v1/artists/", json=artista_teste)
    
    response = client.post("/api/v1/portfolios/", json=portfolio_teste)
    assert response.status_code == 201
    assert response.json()["title"] == portfolio_teste["title"]


def test_create_rating():
    client.post("/api/v1/users/register", json=usuario_teste)
    client.post("/api/v1/artists/", json=artista_teste)
    
    response = client.post("/api/v1/ratings/", json=avaliacao_teste)
    assert response.status_code == 201
    assert response.json()["score"] == avaliacao_teste["score"]


def test_search_artistas():
    response = client.get("/api/v1/search/artistas")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_listar_estilos():
    response = client.get("/api/v1/search/estilos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
