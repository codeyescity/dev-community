from fastapi import FastAPI,status, HTTPException, Depends, APIRouter, Response
from fastapi import UploadFile, File
from dbhelper import runSQL, Database
from oauth2 import get_current_user

#from routes import login
#to generate random file name
import uuid

import uvicorn

#image hosting
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#app.include_router(login.app)

SERVER_PORT = 4000
#SERVER_DOMAIN_NAME = "m.devcommunity.tech"
SERVER_DOMAIN_NAME = "127.0.0.1"

server_ip = SERVER_DOMAIN_NAME + ":" + str(SERVER_PORT)

@app.post("/user_profile_img/", status_code = status.HTTP_200_OK)
#def change_user_profile_img(image: UploadFile):
def change_user_profile_img(image: UploadFile, user_id : int = Depends(get_current_user)):
    #image.content_type image/png image/jpeg
    if(image.content_type not in ["image/png", "image/jpeg"]):
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="file format unsupported")

    #generate random file name
    filename = str(uuid.uuid4())
    try:
        # read the file
        file_content = image.file.read()
        # file size limit 10 mb
        SIZE_LIMIT = 1024 * 1024 * 10
        if(len(file_content) > SIZE_LIMIT):
            raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail=f"the file is  larger then 5 Mb")

        with open("./static/img/" + filename, 'wb') as f:
            f.write(file_content)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        image.file.close()


    path = "http://" + server_ip + "/static/img/" + filename
    res = runSQL("""UPDATE users SET img_url = %s WHERE user_id = %s """,(path, user_id))

    return {"path": path }



if __name__ == "__main__":
    #uvicorn.run("main:app", host = "0.0.0.0", port = server_port, reload=True)
    uvicorn.run("fileserver:app", host = "127.0.0.1", port = SERVER_PORT, reload=True)
