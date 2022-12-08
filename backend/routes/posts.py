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
def get_posts(user_id : int = Depends(get_current_user), start: int = 0, limit: int = 20, type: str = "all"):

    if type not in ["post","question","job_offer","all"]:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"the post type  {type} can t be found")

    if type == "all":
        sql ="""SELECT posts.post_id, posts.post_creation_date, users.user_id, users.user_name, posts.description, posts.number_likes
            FROM posts 
            INNER JOIN users ON users.user_id = posts.user_id 
            LIMIT %s, %s;"""
        res = runSQL(sql, (start, limit))
    else:
        sql ="""SELECT posts.post_id, posts.post_creation_date, users.user_id, users.user_name, posts.description, posts.number_likes
            FROM posts 
            INNER JOIN users ON users.user_id = posts.user_id 
            WHERE type = %s LIMIT %s, %s;"""
        res = runSQL(sql, (type, start, limit))

    return res

@app.get("/posts/{post_id}", status_code = status.HTTP_200_OK)
def get_post(post_id : int, user_id : int = Depends(get_current_user)):
    res = runSQL("""SELECT * FROM posts WHERE post_id = %s""",(post_id,))    
    if not res:
        raise HTTPException(status_code=404, detail=f"the post with id {post_id} can t be found")
    return res

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_post(post : Post, user_id : int = Depends(get_current_user)):
    runSQL("""INSERT INTO posts (user_id,type,description,post_creation_date) VALUES (%s,"post",%s,NOW());""" ,(user_id,post.description))
    return post

@app.put("/posts/{post_id}", status_code = status.HTTP_200_OK)
def edit_post(post_id : int, post : Post, user_id : int = Depends(get_current_user)):
    res = runSQL("""SELECT * FROM posts WHERE post_id = %s""",(post_id,))
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the post with id {post_id} can t be found")
    if res[0]["user_id"] != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    res = runSQL("""UPDATE posts SET description = %s WHERE post_id = %s """,(post.description,post_id))
    # return the edited post
    res = runSQL("""SELECT * FROM posts WHERE post_id = %s""",(post_id,))
    return res

@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id : int, user_id : int = Depends(get_current_user)):
    res = runSQL("""SELECT * FROM posts WHERE post_id = %s""",(post_id,))
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the post with id {post_id} can t be found")
    if res[0]["user_id"] != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    res = runSQL("""DELETE FROM posts WHERE post_id = %s""",(post_id,))
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.post("/postlike/{post_id}")
def like_post(post_id: int, user_id : int = Depends(get_current_user)):
    # check if the post exists
    res = runSQL("""SELECT * FROM posts WHERE post_id = %s""",(post_id,))
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the post with id {post_id} can t be found")    
    # check if user has liked the post
    res = runSQL("""SELECT user_id FROM postlikes WHERE post_id = %s AND user_id = %s""",(post_id,user_id))
    if(res):
        # remove like 
        runSQL("""DELETE FROM postlikes WHERE post_id = %s AND user_id = %s""",(post_id,user_id) )
        runSQL("""UPDATE posts SET number_likes = number_likes - 1 WHERE post_id = %s """,(post_id,))
        return Response(status_code = status.HTTP_204_NO_CONTENT)
    else:
        # add like
        runSQL("""INSERT INTO  postlikes (post_id,user_id) VALUES (%s,%s)""",(post_id,user_id) )
        runSQL("""UPDATE posts SET number_likes = number_likes + 1 WHERE post_id = %s """,(post_id,))
        return Response(status_code = status.HTTP_201_CREATED)

    

