from fastapi.testclient import TestClient
import sys
sys.path.append("..")
from main import app
from dbhelper import runSQL

client = TestClient(app)


response = client.post("/login", data={"username": "user", "password" : "user"})
user_header = {}
user_header["Authorization"] =  "Bearer " + response.json()["access_token"]

def test_create_task():
    response = client.get("/posts", headers = user_header)

    assert response.status_code == 200

