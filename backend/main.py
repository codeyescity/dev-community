from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from passlib.context import CryptContext
from pydantic import BaseModel
import uvicorn

# importing routes from other files
from routes import posts, comments, users

app = FastAPI()

app.include_router(posts.app)
app.include_router(comments.app)
app.include_router(users.app)


@app.get("/")
def read_root():
    return {"data":"data"}



if __name__ == "__main__":
    uvicorn.run("main:app", host = "127.0.0.1", port = 3000, reload=True)
