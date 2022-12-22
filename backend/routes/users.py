from fastapi import status, HTTPException, Depends, APIRouter, Response
from dbhelper import runSQL, Database
from pydantic import BaseModel
#temp
import uuid
# temp 
from fastapi import UploadFile

# weird hack to import 
import sys
sys.path.append("..")
from oauth2 import  get_current_user

app = APIRouter(tags=['users'])

class User(BaseModel):
    username : str
    password : str
    first_name: str
    last_name: str
    email: str
    phone_number: int
    

@app.get("/userprofile", status_code = 200)
def get_user(user_id: int = Depends(get_current_user)):
    res = runSQL("""SELECT user_id,username,img_url,first_name,last_name,email,phone_number FROM users WHERE user_id = %s""",(user_id,))

    if not res:
        raise HTTPException(status_code = 404, detail=f"User with id: {user_id} does not exist")
    return res

@app.get("/user/{id}", status_code = 200)
def get_user(id: int, user_id: int = Depends(get_current_user)):
    res = runSQL("""SELECT user_id,username,img_url,first_name,last_name,email,phone_number FROM users WHERE user_id = %s""",(id,))

    if not res:
        raise HTTPException(status_code = 404, detail=f"User with id: {id} does not exist")
    return res

@app.get("/userprofile/posts", status_code=200)
def get_posts(user_id : int = Depends(get_current_user), start: int = 0, limit: int = 20, type: str = "all"):

    if type not in ["post","question","job_offer","all"]:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"the post type  {type} can t be found")

    if type == "all":
        sql ="""SELECT posts.post_id, posts.post_creation_date, users.user_id, users.username, posts.description, posts.number_likes
            FROM posts 
            INNER JOIN users ON users.post_owner_id = posts.user_id 
            WHERE user_id = %s
            LIMIT %s, %s;"""
        res = runSQL(sql, (user_id, start, limit))
    else:
        sql ="""SELECT posts.post_id, posts.post_creation_date, users.user_id, users.username, posts.description, posts.number_likes
            FROM posts 
            INNER JOIN users ON users.user_id = posts.user_id 
            WHERE user_id = %s
            WHERE type = %s LIMIT %s, %s;"""
        res = runSQL(sql, (user_id, type, start, limit))

    return res
#maybe more info
@app.get("/user/projects/", status_code = status.HTTP_200_OK)
def get_user_projects(user_id : int = Depends(get_current_user)):
    res = runSQL(""" SELECT p.project_id, p.project_name FROM members m
                LEFT JOIN projects p ON m.project_id = p.project_id  
                WHERE user_id = %s""", (user_id,))

    return res

@app.post("/user_profile_img/")
async def change_user_profile_img(image: UploadFile, user_id : int = Depends(get_current_user)):
    #image.content_type image/png image/jpeg
    if(image.content_type not in ["image/png", "image/jpeg"]):
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="file format unsupported")

    # file size limit 10 mb
    SIZE_LIMIT = 1024 * 1024 * 10
    if(len(image.file.read()) > SIZE_LIMIT):
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail=f"the file is  larger then 5 Mb")
    
    #generate random file name
    filename = str(uuid.uuid4())
    try:
        file_content = await image.read()
        with open("./static/img/" + filename, 'wb') as f:
            f.write(file_content)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        image.file.close()

    path = "http://127.0.0.1:3000/static/img/" + filename
    runSQL("""UPDATE users SET img_url = %s WHERE user_id = %s """,(path, user_id))

    return {"filename": image.filename}


