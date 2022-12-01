from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from run import connect
from pydantic import BaseModel
# tags are just for the ui
app = APIRouter(tags=['Posts'])

class Post(BaseModel):
    user_id: int
    post_type: str
    title: str | None = None
    description: str
    code: str | None = None

@app.get("/posts")
def get_user():
    con = connect()
    cur = con.cursor(dictionary=True)
    cur.execute("""SELECT * FROM posts""")
    res = cur.fetchall()

    return res

@app.get("/posts/{id}")
def get_user(id : int):
    con = connect()
    cur = con.cursor(dictionary=True)
    cur.execute("""SELECT * FROM posts WHERE post_id = %s""",(id,) )
    res = cur.fetchall()

    return res

@app.post("/posts")
def get_user(post : Post):
    con = connect()
    cur = con.cursor(dictionary=True)
    cur.execute("""INSERT INTO posts (user_id,type,description,post_creation_date) VALUES (1,"post",%s,NOW());""" ,(post.description,))
    con.commit()
    return post

@app.put("/posts/{id}")
def get_user(id : int,post : Post):
    con = connect()
    cur = con.cursor(dictionary=True)
    cur.execute("""UPDATE posts SET description = %s WHERE post_id = %s """,(post.description,id))
    con.commit()
    return post

@app.delete("/posts/{id}")
def get_user(id : int):
    con = connect()
    cur = con.cursor(dictionary=True)

    cur.execute("""DELETE FROM posts WHERE post_id = %s""",(id,))
    con.commit()

    return {"deleted": id}



@app.post("/postlike/{id}")
def like_post(id:int):
    userid = 1
    con = connect()
    cur = con.cursor(dictionary=True)
    try:
        cur.execute("""SELECT user_id FROM postlikes WHERE post_id = %s AND user_id = %s""",(id,userid) )
        res = cur.fetchone()
    except :
        pass

    if(res):
        cur.execute("""DELETE FROM postlikes WHERE post_id = %s AND user_id = %s""",(id,userid) )
        con.commit()
        return "deleted"
    else:
        pass
        cur.execute("""INSERT INTO  postlikes (post_id,user_id) VALUES (%s,%s)""",(id,userid) )
        con.commit()
        return "added"

    