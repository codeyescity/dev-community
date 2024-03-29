from fastapi import status, HTTPException, Depends, APIRouter, Response
from dbhelper import runSQL, Database, runSQL_return_id
from pydantic import BaseModel, Field
from oauth2 import get_current_user

from helper import post_exist, user_post_owner
# tags are just for the ui
app = APIRouter(tags=['Posts'])

class Post(BaseModel):
    post_type: str
    post_title: str | None = None
    post_body: str = Field(..., min_length=1)
    post_code: str | None = None
    post_skills : list[int] | None = None

@app.get("/posts", status_code=200)
def get_posts(user_id : int = Depends(get_current_user), start: int = 0, limit: int = 20, type: str = "all"):

    res = None
    if type not in ["post","question","job_offer","all"]:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"the post with the type {type} can t be found")
    # get all posts posts, questions , job offers
    if type == "all":
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
                LIMIT %s, %s;"""
        res = runSQL(sql, (user_id,start, limit))
    else:
        sql ="""
            SELECT 
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
            WHERE p.post_type = %s
            LIMIT %s, %s;"""
        res = runSQL(sql, (user_id, type, start, limit))
    
    for post in res:
        post["post_skills"] = runSQL("""SELECT posts_technologies.technology_id, technology_name
                                        FROM posts_technologies 
                                        LEFT JOIN technologies ON posts_technologies.technology_id = technologies.technology_id
                                        WHERE post_id = %s""",(post["post_id"],))

    return res

@app.get("/posts/{post_id}", status_code = status.HTTP_200_OK)
def get_post(post_id : int, user_id : int = Depends(get_current_user)):
    sql ="""
        SELECT 
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
        WHERE p.post_id = %s;"""

    res = runSQL(sql,(user_id,post_id))    
    # check if post exists and returns
    if not res:
        raise HTTPException(status_code=404, detail=f"the post with id {post_id} can t be found")

    res[0]["post_skills"] = runSQL("""SELECT posts_technologies.technology_id, technology_name
                                        FROM posts_technologies 
                                        LEFT JOIN technologies ON posts_technologies.technology_id = technologies.technology_id
                                        WHERE post_id = %s""",(post_id,))
    return res

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_post(post : Post, user_id : int = Depends(get_current_user)):
    if post.post_type not in ["post","question","job_offer"]:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"the post with type {post.post_type} can t be created")

    # add the post to the db 
    post_id = runSQL_return_id("""INSERT INTO posts (post_owner_id , post_type, post_title, post_body, post_code, post_creation_date) VALUES 
            (%s,%s,%s,%s,%s,NOW());""" ,(user_id, post.post_type, post.post_title, post.post_body, post.post_code))

    if(post.post_skills):
        for element in post.post_skills:
            runSQL("INSERT INTO posts_technologies (post_id, technology_id) VALUES (%s,%s)",(post_id, element))

    return post_id

@app.put("/posts/{post_id}", status_code = status.HTTP_200_OK)
def edit_post(post_id : int, post : Post, user_id : int = Depends(get_current_user)):
    user_post_owner(user_id, post_id)
    
    res = runSQL("""UPDATE posts SET post_title = %s, post_body = %s, post_code = %s WHERE post_id = %s""",(post.post_title,post.post_body,post.post_code,post_id))
    # return the edited post
    res = runSQL("""SELECT * FROM posts WHERE post_id = %s""",(post_id,))
    return res

@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id : int, user_id : int = Depends(get_current_user)):
    user_post_owner(user_id, post_id)
    
    res = runSQL("""DELETE FROM posts WHERE post_id = %s""",(post_id,))
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.post("/postlike/{post_id}")
async def like_post(post_id: int, user_id : int = Depends(get_current_user)):

    post_exist(post_id)
    # check if user has liked the post
    res = runSQL("""SELECT * FROM users_likes_posts WHERE post_id = %s AND post_liker_id = %s""",(post_id, user_id))
    if(res):
        # remove like 
        runSQL("""DELETE FROM users_likes_posts WHERE post_id = %s AND post_liker_id = %s""",(post_id,user_id) )
        runSQL("""UPDATE posts SET post_number_likes = post_number_likes - 1 WHERE post_id = %s """,(post_id,))
        return Response(status_code = status.HTTP_204_NO_CONTENT)
    else:
        # add like
        runSQL("""INSERT INTO  users_likes_posts (post_id,post_liker_id) VALUES (%s,%s)""",(post_id,user_id) )
        runSQL("""UPDATE posts SET post_number_likes = post_number_likes + 1 WHERE post_id = %s """,(post_id,))
        return Response(status_code = status.HTTP_201_CREATED)

    

