from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from run import connect
# tags are just for the ui
app = APIRouter(tags=['Posts'])





@app.get("/posts")
def get_user():
    con = connect()
    cur = con.cursor(dictionary=True)
    cur.execute("""SELECT * FROM posts""")
    res = cur.fetchall()

    return {"posts": res}

@app.get("/posts/{id}")
def get_user(id : int):
    return {"id": id}