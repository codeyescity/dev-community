from fastapi import status, HTTPException, Depends, APIRouter, Response
from dbhelper import runSQL, Database
from pydantic import BaseModel
#to generate random file name
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
    password : str | None = None
    new_password : str | None = None

    

@app.get("/userprofile", status_code = status.HTTP_200_OK)
def get_user_info(user_id: int = Depends(get_current_user)):

    res = runSQL("""SELECT user_id,username,img_url,first_name,last_name,email,phone_number,about FROM users WHERE user_id = %s""",(user_id,))

    if not res:
        raise HTTPException(status_code = 404, detail=f"User with id: {user_id} does not exist")
    
    return res

@app.put("/userprofile", status_code = status.HTTP_200_OK)
def edit_user_info(user: User, user_id : int = Depends(get_current_user)):
    res = runSQL("""SELECT * FROM users WHERE user_id = %s""",(user_id,))
    if not res :
        raise HTTPException(status_code = 404, detail=f"User can't be found")
 
    if(user.password):
        if(user.new_password):
            password = user.password
            hashed_password = res[0]["password"]

            if(verify(password,hashed_password)):
                new_hashed_password = hash(user.new_password)
                res = runSQL(""" UPDATE users SET password = %s WHERE user_id = %s""",(new_hashed_password, user_id))
                
            else:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid password")
    res = runSQL(""" UPDATE users SET username = %s, first_name = %s, last_name = %s , email = %s, about = %s WHERE user_id = %s""",(user.username, user.first_name, user.last_name, user.email, user.about, user_id))

    return res


@app.get("/user/{id}", status_code = status.HTTP_200_OK)
def get_user(id: int, user_id: int = Depends(get_current_user)):

    res = runSQL("""SELECT user_id,username,img_url,first_name,last_name,email,phone_number,about FROM users WHERE user_id = %s""",(id,))

    if not res:
        raise HTTPException(status_code = 404, detail=f"User with id: {id} does not exist")


    res[0]["user_skills"] = runSQL("""SELECT technologies.technology_id, technology_experience, technology_name
                                        FROM users_technologies 
                                        LEFT JOIN technologies ON users_technologies.technology_id = technologies.technology_id
                                        WHERE user_id = %s AND technology_experience > %s""",(id,0))

    return res

@app.get("/user/{id}/posts", status_code = status.HTTP_200_OK)
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
        LIMIT %s, %s;
        """
    data = (user_id, id, type,start, limit)

    res = runSQL(sql, data)
    return res





@app.get("/user/{id}/projects", status_code = status.HTTP_200_OK)
def get_user_projects(id: int, user_id : int = Depends(get_current_user)):
    # get the projects that the user is part of
    res = runSQL("""
                    SELECT 
                        p.project_id, 
                        p.project_name,
                        u.img_url
                    FROM projects p
                    LEFT JOIN members m ON p.project_id = m.project_id  
                    LEFT JOIN users u ON u.user_id = p.project_owner_id
                    WHERE m.user_id = %s
                """,(id,))

    return res

#SELECT username FROM users WHERE user_id = (SELECT user_id FROM members WHERE project_id = ( SELECT project_id FROM projects WHERE  ))  

@app.post("/user_profile_img/", status_code = status.HTTP_200_OK)
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
