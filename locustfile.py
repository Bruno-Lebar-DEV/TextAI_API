from locust import HttpUser, task, between
import random

class TextAIUser(HttpUser):
    wait_time = between(1, 3)
    token = None

    def on_start(self):
        # Registra e faz login para obter o token
        username = f"locustuser{random.randint(1, 100000)}"
        password = "testpass123"
        self.client.post("/users/register", json={"username": username, "password": password})
        resp = self.client.post("/users/login", json={"username": username, "password": password})
        if resp.status_code == 200:
            self.token = resp.json()["access_token"]
        else:
            self.token = None

    @task(2)
    def sentiment(self):
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            data = {"text": "I love this API!"}
            self.client.post("/sentiment/", json=data, headers=headers)

    @task(2)
    def summary(self):
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            data = {"text": "FastAPI is a modern, fast web framework for building APIs with Python. It is easy to use and very powerful."}
            self.client.post("/summary/", json=data, headers=headers)

    @task(2)
    def classify(self):
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            data = {"text": "The new iPhone was released today.", "labels": ["technology", "sports", "politics"]}
            self.client.post("/classify/", json=data, headers=headers)
