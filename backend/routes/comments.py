from fastapi import status, HTTPException, Depends, APIRouter, Response
from dbhelper import runSQL
from pydantic import BaseModel
from oauth2 import get_current_user


class Comment(BaseModel):
    comment_text : str



# tags are just for the ui
app = APIRouter(tags=['comments'])


@app.get("/posts/{post_id}/comments")
def get_post_comments(post_id: int,user_id: int = Depends(get_current_user), start: int = 0, limit: int = 5):
    res = runSQL("""SELECT * FROM postscomments WHERE post_id = %s LIMIT %s, %s;""",(post_id,start,limit))
    return res

@app.post("/posts/{post_id}/comments")
def add_post_comment(post_id: int, comment: Comment,user_id : int = Depends(get_current_user)):
    runSQL("""INSERT INTO postscomments (user_id, post_id, comment_text,comment_creation_date) VALUES (%s,%s,%s,NOW());""" ,(user_id, post_id, comment.comment_text))
    return comment

@app.put("/posts/{post_id}/comments/{comment_id}")
def edit_post_comment(comment_id: int, comment: Comment, user_id : int = Depends(get_current_user)):

    res = runSQL("""SELECT * FROM postscomments WHERE comment_id = %s""",(comment_id,))
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the comment with id {comment_id} can t be found")
    if res[0]["user_id"] != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    res = runSQL("""UPDATE postscomments SET comment_text = %s WHERE comment_id = %s """,(comment.comment_text, comment_id))
    # return the edited post
    res = runSQL("""SELECT * FROM postscomments WHERE comment_id = %s""",(comment_id,))
    return res

@app.delete("/posts/{post_id}/likecomment/{comment_id}")
def delete_post_comment(post_id: int, comment_id: int, user_id : int = Depends(get_current_user)):
    res = runSQL("""SELECT * FROM postscomments WHERE post_id = %s AND comment_id = %s""",(post_id, comment_id))
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the comment with id {comment_id} can t be found")
    if res[0]["user_id"] != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    res = runSQL("""DELETE FROM postscomments WHERE post_id = %s AND comment_id = %s""",(post_id, comment_id))
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.post("/posts/{post_id}/likecomment/{comment_id}")
def like_comment(post_id: int , comment_id: int, user_id : int = Depends(get_current_user)):
    # check if comment exists
    res = runSQL("""SELECT * FROM postscomments WHERE comment_id = %s""",(comment_id,))
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the comment with id {comment_id} can t be found")
    # check if user has liked the comment
    res = runSQL("""SELECT user_id FROM commentlikes WHERE comment_id = %s AND user_id = %s""",(comment_id, user_id))
    if(res):
        # remove like
        runSQL("""DELETE FROM commentlikes WHERE comment_id = %s AND user_id = %s""",(comment_id, user_id))
        runSQL("""UPDATE postscomments SET comment_likes = comment_likes - 1 WHERE comment_id = %s""",(comment_id,))
        return Response(status_code = status.HTTP_204_NO_CONTENT)
    else:
        # add like
        runSQL("""INSERT INTO  commentlikes (comment_id,user_id) VALUES (%s,%s)""",(comment_id, user_id))
        runSQL("""UPDATE postscomments SET comment_likes = comment_likes + 1 WHERE comment_id = %s""",(comment_id,))
        return Response(status_code = status.HTTP_201_CREATED)