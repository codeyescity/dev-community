from fastapi.testclient import TestClient
import sys
sys.path.append("..")
from main import app
from dbhelper import runSQL

client = TestClient(app)

print("hello")
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200


def test_posts():
    response = client.get("/posts", 
                    headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo2LCJleHAiOjE2NzExOTc2ODl9.LJnDLiTayR24thzvSCVY52POZecZ7nEgfLrKBscf5yk"})
    assert response.status_code == 200

def test_register():
    runSQL("""DELETE FROM users WHERE username = 'test' """)
    response = client.post("/register",
                    json = {"username" : "test", "password" : "test", "first_name": "bob", "last_name": "bob", "email": "bob@gmail.com", "phone_number": 1234567890})
    assert response.status_code == 201
    # duplicate username
    response = client.post("/register",
                    json = {"username" : "test", "password" : "test", "first_name": "bob", "last_name": "bob", "email": "bob@gmail.com", "phone_number": 1234567890})
    assert response.status_code == 403
    # long username
    response = client.post("/register",
                    json = {"username" : "loooooooooooooooooooong", "password" : "test", "first_name": "bob", "last_name": "bob", "email": "bob@gmail.com", "phone_number": 1234567890})
    assert response.status_code == 403

def test_login():
    # right username and password
    response = client.post("/login",
                    headers = {"Content-Type": "application/x-www-form-urlencoded"},
                    data = {"username" : "test", "password" : "test"}
                    )
    assert response.status_code == 200

def test_login_wrong_password():
    # wrong password
    response = client.post("/login",
                    headers = {"Content-Type": "application/x-www-form-urlencoded"},
                    data = {"username" : "test", "password" : "bad"}
                    )
    assert response.status_code == 403
    
def test_login_wrong_username():
    response = client.post("/login",
                    headers = {"Content-Type": "application/x-www-form-urlencoded"},
                    data = {"username" : "bad", "password" : "bad"}
                    )
    assert response.status_code == 403