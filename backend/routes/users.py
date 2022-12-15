from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from dbhelper import runSQL, Database
from pydantic import BaseModel
#temp
import uuid
# temp 
from fastapi import UploadFile

# weird hack to import 
import sys
sys.path.append("..")
from utiles import hash,verify
from oauth2 import create_access_token, get_current_user
app = APIRouter(tags=['users'])

class User(BaseModel):
    username : str
    password : str
    first_name: str
    last_name: str
    email: str
    phone_number: int
    
db = Database()

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
    res = runSQL("""INSERT INTO users (username, password, first_name, last_name, email, phone_number) VALUES (%s,%s,%s,%s,%s,%s)""",(user.username, user.password,user.first_name, user.last_name, user.email, user.phone_number))

    return res

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


@app.get("/userprofile", status_code = 200)
def get_user(user_id: int = Depends(get_current_user)):
    res = runSQL("""SELECT * FROM users WHERE user_id = %s""",(user_id,))

    if not res:
        raise HTTPException(status_code = 404, detail=f"User with id: {user_id} does not exist")
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

@app.post("/user_profile_img/")
async def change_user_profile_img(image: UploadFile, user_id : int = Depends(get_current_user)):
    #image.content_type image/png image/jpeg
    if(image.content_type not in ["image/png", "image/jpeg"]):
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="file format unsupported")

    # file size limit 5 mb
    SIZE_LIMIT = 1024 * 1024 * 5
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