from fastapi import status, HTTPException, Depends, APIRouter, Response
from dbhelper import runSQL, Database
from pydantic import BaseModel
#temp
import uuid
# temp 
from fastapi import UploadFile, File

# weird hack to import 
import sys
sys.path.append("..")
from oauth2 import  get_current_user
from utiles import hash,verify

app = APIRouter(tags=['users'])

class User(BaseModel):
    first_name: str
    last_name: str
    username : str
    email: str
    about : str
    password : str
    new_password : str

    

@app.get("/userprofile", status_code = 200)
def get_user_info(user_id: int = Depends(get_current_user)):

    res = runSQL("""SELECT user_id,username,img_url,first_name,last_name,email,phone_number,about FROM users WHERE user_id = %s""",(user_id,))

    if not res:
        raise HTTPException(status_code = 404, detail=f"User with id: {user_id} does not exist")
    
    return res

@app.get("/user/{id}", status_code = 200)
def get_user(id: int, user_id: int = Depends(get_current_user)):
    #res = runSQL("""SELECT user_id,username,img_url,first_name,last_name,email,phone_number FROM users WHERE user_id = %s""",(id,))
    res = runSQL("""SELECT user_id,username,img_url,first_name,last_name,email,phone_number,about FROM users WHERE user_id = %s""",(id,))

    if not res:
        raise HTTPException(status_code = 404, detail=f"User with id: {id} does not exist")
    return res

@app.get("/user/{id}/posts", status_code = 200)
def get_user_posts(id: int, type: str, start: int = 0, limit: int = 20, user_id: int = Depends(get_current_user)):
    sql ="""SELECT 
            p.post_id, 
            p.post_creation_date, 
            p.post_owner_id, 
            u.username, 
            u.img_url,
            p.post_type,
            p.post_title,
            p.post_body, 
            p.post_code,
            p.post_number_likes, 
            p.post_number_comments,
            IF((SELECT post_liker_id FROM users_likes_posts pl WHERE pl.post_liker_id = %s AND pl.post_id = p.post_id), "true", "false") AS 'liked'
        FROM posts p
        LEFT JOIN users u ON p.post_owner_id  = u.user_id
        WHERE u.user_id = %s AND p.post_type = %s
        LIMIT %s, %s;"""

    res = runSQL(sql, (user_id, id, type,start, limit))

    # check later
    #if not res:
    #    raise HTTPException(status_code = 404, detail=f"User posts can't be found")
    return res


#@app.get("/user/{id}/questions", status_code = 200)
#def get_user_posts(user_id: int = Depends(get_current_user), id: int, start: int = 0, limit: int = 20):
#    sql ="""SELECT 
"""            p.post_id, 
            p.post_creation_date, 
            p.post_owner_id, 
            u.username, 
            u.img_url,
            p.post_type,
            p.post_title,
            p.post_body, 
            p.post_code,
            p.post_number_likes, 
            p.post_number_comments,
            IF((SELECT post_liker_id FROM users_likes_posts pl WHERE pl.post_liker_id = %s AND pl.post_id = p.post_id), "true", "false") AS 'liked'
        FROM posts p
        LEFT JOIN users u ON p.post_owner_id  = u.user_id
        WHERE u.user_id = %s AND p.post_type  = "question"
        LIMIT %s, %s;"""

#    res = runSQL(sql, (user_id, id, start, limit))

    #if not res:
    #    raise HTTPException(status_code = 404, detail=f"User posts can't be found")
#    return res



@app.get("/user/{id}/projects", status_code = status.HTTP_200_OK)
def get_user_projects(user_id : int = Depends(get_current_user)):
    res = runSQL(""" SELECT p.project_id, p.project_name FROM members m
                LEFT JOIN projects p ON m.project_id = p.project_id  
                WHERE user_id = %s""", (user_id,))

    return res


# note: changing password don t work
@app.put("/userprofile", status_code = 200)
def edit_user_info(user: User, user_id : int = Depends(get_current_user)):
    res = runSQL("""SELECT * FROM users WHERE user_id = %s""")
    if not res :
        raise HTTPException(status_code = 404, detail=f"User can't be found")

    password = user.password
    hashed_password = res["password"]

    if(verify(password,hashed_password)):
        print("he")


    
    res = runSQL(""" UPDATE users SET username = %s, first_name = %s, last_name = %s , email = %s, about = %s WHERE user_id = %s""",(user.username, user.first_name, user.last_name, user.email, user.about))



    res = runSQL("""SELECT user_id,username,img_url,first_name,last_name,email,phone_number,about FROM users WHERE user_id = %s""",(user_id,))
    return res






@app.post("/user_profile_img/")
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

    path = "http://127.0.0.1:3000/static/img/" + filename
    runSQL("""UPDATE users SET img_url = %s WHERE user_id = %s """,(path, user_id))

    return {"path": path }
