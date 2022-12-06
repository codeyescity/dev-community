from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel

from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded


def verify_access_token(token: str):
    try: #this code can error out
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:  
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=f"Could not validate credentials", 
                                headers={"WWW-Authenticate": "Bearer"})
    except JWTError:    
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Could not validate credentials", 
                            headers={"WWW-Authenticate": "Bearer"})
    return id



def get_current_user(token: str = Depends(oauth2_scheme)):
    
    return verify_access_token(token)