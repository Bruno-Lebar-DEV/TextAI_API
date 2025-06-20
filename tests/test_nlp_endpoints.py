import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_and_login():
    client.post("/users/register", json={"username": "testnlp", "password": "testpass123"})
    response = client.post("/users/login", json={"username": "testnlp", "password": "testpass123"})
    token = response.json()["access_token"]
    return token

def test_sentiment_analysis(setup_and_login):
    token = setup_and_login
    data = {"text": "I love this API!"}
    response = client.post("/sentiment/", json=data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    result = response.json()
    assert "sentiment" in result
    assert "confidence" in result
    assert result["text"] == data["text"]

def test_summary_analysis(setup_and_login):
    token = setup_and_login
    data = {"text": "FastAPI is a modern, fast web framework for building APIs with Python. It is easy to use and very powerful."}
    response = client.post("/summary/", json=data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    result = response.json()
    assert "summary" in result
    assert result["text"] == data["text"]

def test_classify_analysis(setup_and_login):
    token = setup_and_login
    data = {"text": "The new iPhone was released today.", "labels": ["technology", "sports", "politics"]}
    response = client.post("/classify/", json=data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    result = response.json()
    assert "category" in result
    assert "confidence" in result
    assert "all_categories" in result
    assert "all_confidences" in result
    assert result["text"] == data["text"]

def test_history_endpoint(setup_and_login):
    token = setup_and_login
    response = client.get("/history/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
