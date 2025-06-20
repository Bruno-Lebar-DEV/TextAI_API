import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_user():
    # Garante que o usuário existe para o teste de login
    client.post("/users/register", json={"username": "testlogin", "password": "testpass123"})

def test_login_success(setup_user):
    response = client.post("/users/login", json={"username": "testlogin", "password": "testpass123"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(setup_user):
    response = client.post("/users/login", json={"username": "testlogin", "password": "wrongpass"})
    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]

def test_login_user_not_found():
    response = client.post("/users/login", json={"username": "usernotfound", "password": "any"})
    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]
