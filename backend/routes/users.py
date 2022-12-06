from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from dbhelper import runSQL
from pydantic import BaseModel
# weird hack to import 
import sys
sys.path.append("..")
from utiles import hash
from oauth2 import get_current_user
app = APIRouter(tags=['users'])

class User(BaseModel):
    name : str
    password : str


@app.get('/users/{id}')
def get_user(id: int, user_id: int = Depends(get_current_user)):
    res = runSQL(""" SELECT * FROM users WHERE user_id = %s""",(id,))
    print(user_id)
    if not res:
        raise HTTPException(status_code = 404, detail=f"User with id: {id} does not exist")
    return res

@app.post("/users/", status_code=201)
def create_user(user: User):

    user.password = utiles.hash(user.password)
    res = runSQL(""" INSERT INTO users (user_name, user_password) VALUES (%s,%s)""",(user.name,user.password))
    # hash the password - user.password

    return res


