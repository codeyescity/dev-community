from fastapi import status, HTTPException, Depends, APIRouter, Response
from dbhelper import runSQL
from pydantic import BaseModel
from oauth2 import get_current_user

# tags are just for the ui
app = APIRouter(tags=['Posts'])

class Post(BaseModel):
    user_id: int
    post_type: str
    title: str | None = None
    description: str
    code: str | None = None

@app.get("/posts", status_code=200)
def get_posts(user_id : int = Depends(get_current_user)):

    sql ="""SELECT posts.post_id, posts.post_creation_date, users.user_id, users.user_name, posts.description, posts.number_likes
            FROM posts 
            INNER JOIN users ON users.user_id = posts.user_id; """

    res = runSQL(sql)

    return res

@app.get("/posts/{id}", status_code = status.HTTP_200_OK)
def get_post(id : int, user_id : int = Depends(get_current_user)):
    res = runSQL("""SELECT * FROM posts WHERE post_id = %s""",(id,))    
    if not res:
        raise HTTPException(status_code=404, detail=f"the post with id {id} can t be found")
    return res

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_post(post : Post, user_id : int = Depends(get_current_user)):
    runSQL("""INSERT INTO posts (user_id,type,description,post_creation_date) VALUES (%s,"post",%s,NOW());""" ,(user_id,post.description))
    return post

@app.put("/posts/{id}", status_code = status.HTTP_200_OK)
def edit_post(id : int, post : Post, user_id : int = Depends(get_current_user)):
    res = runSQL("""SELECT * FROM posts WHERE post_id = %s""",(id,))
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the post with id {id} can t be found")
    if res[0]["user_id"] != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    res = runSQL("""UPDATE posts SET description = %s WHERE post_id = %s """,(post.description,id))
    res = runSQL("""SELECT * FROM posts WHERE post_id = %s""",(id,))
    return res

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, user_id : int = Depends(get_current_user)):
    res = runSQL("""SELECT * FROM posts WHERE post_id = %s""",(id,))
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the post with id {id} can t be found")
    if res[0]["user_id"] != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    res = runSQL("""DELETE FROM posts WHERE post_id = %s""",(id,))
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.post("/postlike/{id}")
def like_post(id:int, user_id : int = Depends(get_current_user)):
    res = runSQL("""SELECT user_id FROM postlikes WHERE post_id = %s AND user_id = %s""",(id,user_id))

    if(res):
        runSQL("""DELETE FROM postlikes WHERE post_id = %s AND user_id = %s""",(id,user_id) )
        runSQL("""UPDATE posts SET number_likes = number_likes - 1 WHERE post_id = %s """,(id,))
        return Response(status_code = status.HTTP_204_NO_CONTENT)
    else:
        runSQL("""INSERT INTO  postlikes (post_id,user_id) VALUES (%s,%s)""",(id,user_id) )
        runSQL("""UPDATE posts SET number_likes = number_likes + 1 WHERE post_id = %s """,(id,))
        return Response(status_code = status.HTTP_201_CREATED)

    