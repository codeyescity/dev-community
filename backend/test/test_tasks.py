from fastapi.testclient import TestClient
import sys
sys.path.append("..")
from main import app
from dbhelper import runSQL

client = TestClient(app)


response = client.post("/login", data={"username": "user", "password" : "user"})
user_header = {}
user_header["Authorization"] =  "Bearer " + response.json()["access_token"]

def test_get_tasks():
    response = client.post("/projects", headers = user_header, 
                            json={"project_name": "user_project" , "project_description": "str"})

    assert response.status_code == 201

    global project_id
    project_id = response.json()[0]["project_id"]

    response = client.get(f"/projects/{project_id}/task", headers = user_header)

    assert response.status_code == 200

    response = client.get(f"/projects/{project_id}/alltasks", headers = user_header)

    assert response.status_code == 200





def test_create_tasks():

    response = client.post(f"/projects/{project_id}/task", headers = user_header, json={"task_title": "title","task_description": "str","task_type": "bug fix","member_id" : "3"})
    assert response.status_code == 201
