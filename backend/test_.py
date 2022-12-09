from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200


def test_posts():
    response = client.get("/posts", headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo2LCJleHAiOjE2NzExOTc2ODl9.LJnDLiTayR24thzvSCVY52POZecZ7nEgfLrKBscf5yk"})
    assert response.status_code == 200

def test_read_main():
    response = client.post("/")
    assert response.status_code == 200