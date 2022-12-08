from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from dbhelper import runSQL
from pydantic import BaseModel

# weird hack to import 
import sys
sys.path.append("..")
from utiles import hash,verify
from oauth2 import create_access_token, get_current_user

app = APIRouter(tags=['users'])

class User(BaseModel):
    username : str
    password : str


@app.post("/register/", status_code = status.HTTP_201_CREATED)
def register_user(user: User):

    res = runSQL("""SELECT * FROM users WHERE user_name = %s""", (user.username,))
    # check if name is taken
    if res:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail=f"the username {user.username} is already taken.")
    
    # hash the password
    user.password = hash(user.password)
    res = runSQL(""" INSERT INTO users (user_name, user_password) VALUES (%s,%s)""",(user.username,user.password))

    return res

@app.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    #OAuth2PasswordRequestForm dict
    #{"username": "example", "password" : "examplepassword"}

    user = runSQL("""SELECT * FROM users WHERE user_name = %s""",(user_credentials.username,))
    # check if user name is in db
    print(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    # check if password is the same as the hashed password in db
    if not verify(user_credentials.password, user[0]['user_password']):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # create a token
    access_token = create_access_token(data={"user_id": user[0]["user_id"]})

    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/userprofile", status_code = 200)
def get_user(user_id: int = Depends(get_current_user)):
    res = runSQL(""" SELECT * FROM users WHERE user_id = %s""",(user_id,))

    if not res:
        raise HTTPException(status_code = 404, detail=f"User with id: {user_id} does not exist")
    return res