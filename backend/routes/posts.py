from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from dbhelper import runSQL
from pydantic import BaseModel

# tags are just for the ui
app = APIRouter(tags=['Posts'])

class Post(BaseModel):
    user_id: int
    post_type: str
    title: str | None = None
    description: str
    code: str | None = None

@app.get("/posts", status_code=200)
def get_posts():
    res = runSQL("""SELECT * FROM posts""")
    return res

@app.get("/posts/{id}", status_code=200)
def get_post(id : int):
    res = runSQL("""SELECT * FROM posts WHERE post_id = %s""",(id,))
    return res

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_post(post : Post):
    runSQL("""INSERT INTO posts (user_id,type,description,post_creation_date) VALUES (1,"post",%s,NOW());""" ,(post.description,))
    return {"added" : "post"}

@app.put("/posts/{id}")
def edit_post(id : int,post : Post):
    res = runSQL("""UPDATE posts SET description = %s WHERE post_id = %s """,(post.description,id))
    return {"edited": id}

@app.delete("/posts/{id}")
def delete_post(id : int):
    res = runSQL("""DELETE FROM posts WHERE post_id = %s""",(id,))
    return {"deleted": id}



@app.post("/postlike/{id}")
def like_post(id:int):
    userid = 2
    res = runSQL("""SELECT user_id FROM postlikes WHERE post_id = %s AND user_id = %s""",(id,userid))

    if(res):
        runSQL("""DELETE FROM postlikes WHERE post_id = %s AND user_id = %s""",(id,userid) )
        return "deleted"
    else:
        runSQL("""INSERT INTO  postlikes (post_id,user_id) VALUES (%s,%s)""",(id,userid) )
        return "added"

    