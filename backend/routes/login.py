from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from dbhelper import runSQL, runSQL_return_id
from pydantic import BaseModel, Field

# weird hack to import 
import sys
sys.path.append("..")
from utiles import hash,verify
from oauth2 import create_access_token
from helper import technologies

app = APIRouter(tags=['login'])

class User(BaseModel):
    username : str = Field(..., min_length=1)
    password : str = Field(..., min_length=1)
    first_name: str
    last_name: str
    email: str
    phone_number: int


@app.post("/register", status_code = status.HTTP_201_CREATED)
def register_user(user: User):

    # check lenght of thr username and password
    if len(str(user.username)) > 20 or len(str(user.password)) > 20:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # check if name is taken
    res = runSQL("""SELECT * FROM users WHERE username = %s""", (user.username,))
    if res:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail=f"the username {user.username} is already taken.")
    
    # hash the password and ass password to the db
    user.password = hash(user.password)
    user_id = runSQL_return_id("""INSERT INTO users (username, password, first_name, last_name, email, phone_number) VALUES (%s,%s,%s,%s,%s,%s)""",(user.username, user.password,user.first_name, user.last_name, user.email, user.phone_number))

    list_technologies = list(technologies.keys())

    for tech in list_technologies:
        runSQL("INSERT INTO users_technologies (user_id, technology_id) VALUES (%s,%s)", tuple([(user_id)] + [tech]))

    return user_id


@app.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    #OAuth2PasswordRequestForm dict
    #{"username": "example", "password" : "examplepassword"}

    user = runSQL("""SELECT * FROM users WHERE username = %s""",(user_credentials.username,))
    # check if user name is in db
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    # check if password is the same as the hashed password in db
    if not verify(user_credentials.password, user[0]['password']):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # create a token
    access_token = create_access_token(data={"user_id": user[0]["user_id"]})

    return {"access_token": access_token, "token_type": "bearer"}