import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def clear_users():
    # Opcional: Limpar tabela de usuários antes do teste (requer permissão)
    pass

def test_register_user_success():
    response = client.post("/users/register", json={"username": "testuser1", "password": "testpass123"})
    if response.status_code == 200:
        assert response.status_code == 200
    else:
        # Aceita 409 se a mensagem indicar usuário já existente (PT ou EN)
        assert response.status_code == 409
        detail = response.json().get("detail", "").lower()
        assert ("existe" in detail) or ("exists" in detail)

def test_register_user_duplicate():
    # Tenta registrar o mesmo usuário novamente
    response = client.post("/users/register", json={"username": "testuser1", "password": "testpass123"})
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]

def test_register_user_missing_fields():
    response = client.post("/users/register", json={"username": ""})
    assert response.status_code == 422 or response.status_code == 400
