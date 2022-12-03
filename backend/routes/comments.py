from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
# tags are just for the ui
app = APIRouter(tags=['comments'])


@app.get("/posts/{id}/coments")
def get_post_comments():
    return {"data":"data"}

@app.post("/posts/{id}/coments")
def add_post_comment():
    return {"data":"data"}

@app.put("/posts/{id}/comments/{Cid}")
def edit_post_comment():
    return {"data":"data"}

@app.delete("/posts/{id}/comments/{Cid}")
def delete_post_comment():
    return {"data":"data"}
