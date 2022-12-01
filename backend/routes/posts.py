from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from run import connect
from pydantic import BaseModel
# tags are just for the ui
app = APIRouter(tags=['Posts'])

class Post(BaseModel):
    user_id: int
    post_type: str
    title: str
    description: str
    code: str

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

    return {"posts": res}

@app.post("/posts")
def get_user(post : Post):
    con = connect()
    cur = con.cursor(dictionary=True)
    print(post.description)
    cur.execute("""INSERT INTO posts (user_id,type,description,post_creation_date) VALUES (1,"post",%s,NOW());""" ,(post.description,))
    con.commit()
    return {"post description": post.description}

@app.put("/posts/{id}")
def get_user(id : int):
    return {"id": id}

@app.delete("/posts/{id}")
def get_user(id : int):
    return {"id": id}