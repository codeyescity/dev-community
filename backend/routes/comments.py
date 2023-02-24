from fastapi import status, HTTPException, Depends, APIRouter, Response
from dbhelper import runSQL, Database, runSQL_return_id
from pydantic import BaseModel
from oauth2 import get_current_user

from helper import user_comment_owner, comment_exist

class Comment(BaseModel):
    comment_body: str
    comment_code: str | None = None


# tags are just for the ui
app = APIRouter(tags=['comments'])


@app.get("/posts/{post_id}/comments")
def get_post_comments(post_id: int, user_id: int = Depends(get_current_user), start: int = 0, limit: int = 5):
    # return the comment for the post and if the post was liked by the user
    sql ="""SELECT 
                c.comment_id,
                c.post_id,
                c.comment_owner_id,
                u.username,
                u.img_url,
                c.comment_date,
                c.comment_body,
                c.comment_code,
                c.comment_number_likes, 
                IF((SELECT comment_liker_id FROM users_likes_comments cl WHERE cl.comment_liker_id = %s AND cl.comment_id = c.comment_id), "true", "false") AS 'liked'
            FROM users_comments_posts c
            LEFT JOIN users u ON c.comment_owner_id = u.user_id
            WHERE post_id = %s LIMIT %s, %s;
        """

    data = (user_id, post_id, start, limit)
    res = runSQL(sql,data)

    return res

@app.post("/posts/{post_id}/comments")
def add_post_comment(post_id: int, comment: Comment, user_id : int = Depends(get_current_user)):
    # add comment to the db then update the number of comments for the post
    res = runSQL_return_id("""INSERT INTO users_comments_posts (comment_owner_id, post_id, comment_body, comment_code, comment_date) VALUES (%s,%s,%s,%s,NOW());""" ,(user_id, post_id, comment.comment_body, comment.comment_code))
    # change the number of comment for the post
    runSQL("""UPDATE posts SET post_number_comments = post_number_comments + 1 WHERE post_id = %s """,(post_id,))
    return res

@app.put("/posts/{post_id}/comments/{comment_id}")
def edit_post_comment(comment_id: int, comment: Comment, user_id : int = Depends(get_current_user)):

    user_comment_owner(user_id, comment_id)
    
    res = runSQL_return_id("""UPDATE users_comments_posts SET comment_body = %s, comment_code = %s WHERE comment_id = %s """,(comment.comment_body, comment.comment_code, comment_id))
    return res

@app.delete("/posts/{post_id}/likecomment/{comment_id}")
def delete_post_comment(post_id: int, comment_id: int, user_id : int = Depends(get_current_user)):
    
    user_comment_owner(user_id, comment_id)
    # remove the comment from the db and change the number of comment the post
    runSQL("""DELETE FROM users_comments_posts WHERE post_id = %s AND comment_id = %s""",(post_id, comment_id))
    runSQL("""UPDATE posts SET post_number_comments = post_number_comments - 1 WHERE post_id = %s """,(post_id,))
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.post("/posts/{post_id}/likecomment/{comment_id}")
def like_comment(post_id: int , comment_id: int, user_id : int = Depends(get_current_user)):

    comment_exist(comment_id)
    # check if user has liked the comment
    res = runSQL("""SELECT * FROM users_likes_comments WHERE comment_id = %s AND comment_liker_id = %s""",(comment_id, user_id))
    if(res):
        # remove like
        runSQL("""DELETE FROM users_likes_comments WHERE comment_id = %s AND comment_liker_id = %s""",(comment_id, user_id))
        runSQL("""UPDATE users_comments_posts SET comment_number_likes = comment_number_likes - 1 WHERE comment_id = %s""",(comment_id,))
        return Response(status_code = status.HTTP_204_NO_CONTENT)
    else:
        # add like
        runSQL("""INSERT INTO  users_likes_comments (comment_id,comment_liker_id) VALUES (%s,%s)""",(comment_id, user_id))
        runSQL("""UPDATE users_comments_posts SET comment_number_likes = comment_number_likes + 1 WHERE comment_id = %s""",(comment_id,))
        return Response(status_code = status.HTTP_201_CREATED)