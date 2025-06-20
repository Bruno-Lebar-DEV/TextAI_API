import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_and_login():
    # Garante que o usuário existe
    client.post("/users/register", json={"username": "testlist", "password": "testpass123"})
    # Faz login e retorna o token
    response = client.post("/users/login", json={"username": "testlist", "password": "testpass123"})
    token = response.json()["access_token"]
    return token

def test_list_users_authorized(setup_and_login):
    token = setup_and_login
    response = client.get("/users/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(u["username"] == "testlist" for u in response.json())

def test_list_users_unauthorized():
    response = client.get("/users/")
    assert response.status_code == 401
