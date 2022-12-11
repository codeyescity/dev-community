from datetime import datetime, timedelta

# temp 
from fastapi import File, UploadFile
#temp
from fastapi.staticfiles import StaticFiles
#temp 
import uuid

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from passlib.context import CryptContext
from pydantic import BaseModel
import uvicorn

from fastapi.middleware.cors import CORSMiddleware
# importing routes from other files
from routes import posts, comments, users

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.app)
app.include_router(comments.app)
app.include_router(users.app)


@app.get("/")
def read_root():
    return {"data":"data"}


@app.post("/uploadfile/")
async def create_upload_file(image: UploadFile):
    #print(file.content_type == "image/png")
    #print(len(image.file.read()))
    #generate random file name
    filename = "./static/img/" + str(uuid.uuid4())
    try:
        file_content = await image.read()
        with open(filename, 'wb') as f:
            f.write(file_content)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        image.file.close()

    return {"filename": image.filename}

if __name__ == "__main__":
    uvicorn.run("main:app", host = "127.0.0.1", port = 3000, reload=True)
