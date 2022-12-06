from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from dbhelper import runSQL
from pydantic import BaseModel

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# weird hack to import 
import sys
sys.path.append("..")
from utiles import hash,verify
from oauth2 import create_access_token

app = APIRouter(tags=['Authentication'])

@app.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    #OAuth2PasswordRequestForm dict
    #{"username": "example", "password" : "examplepassword"}

    user = runSQL("""SELECT * FROM users WHERE user_name = %s""",(user_credentials.username,))
    # check if user name is in db
    print(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    # check if 
    if not verify(user_credentials.password, user[0]['user_password']):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # create a token

    access_token = create_access_token(data={"user_id": user[0]["user_id"]})

    return {"access_token": access_token, "token_type": "bearer"}
