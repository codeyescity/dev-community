from fastapi import HTTPException, status
from dbhelper import runSQL, Database


technologies = {1 : "html", 2 : "css" , 3 : "javascript", 4 : "c++", 5 :"java", 6 :"sql", 7: "php", 8: "python", 9 : "c", 10 : "c#", 11 : "go" }

def project_exist(project_id : int):
    # check if project exits
    res = runSQL("""SELECT * FROM projects WHERE project_id = %s""",(project_id,))
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the project with id {project_id} can t be found")


def user_member_project(user_id: int, project_id: int):
    # check if user is member for project
    res = runSQL("""SELECT * FROM members WHERE project_id = %s AND user_id = %s""", (project_id, user_id))
    if not res:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not member of this project")


def user_admin_project(user_id: int, project_id: int):
    # check if user is member for project
    res = runSQL("""SELECT * FROM members WHERE project_id = %s AND user_id = %s""", (project_id, user_id))
    if not res:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not member of this project")
    # check if the member is admin
    if res[0]["member_role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not admin of this project")
    
def comment_exist(comment_id: int):
    res = runSQL("""SELECT * FROM users_comments_posts WHERE comment_id = %s""",(comment_id,))
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the comment with id {comment_id} can t be found")

def user_comment_owner(user_id : int , comment_id : int):
    #check if the user is owner of this comment
    res = runSQL("""SELECT * FROM users_comments_posts WHERE comment_id = %s""",(comment_id,))
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the comment with id {comment_id} can t be found")
    if res[0]["comment_owner_id"] != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")



def post_exist(post_id : int):
    res = runSQL("""SELECT * FROM posts WHERE post_id = %s""",(post_id,))
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the post with id {post_id} can t be found")    

def user_post_owner(user_id: int, post_id: int):
    res = runSQL("""SELECT post_owner_id FROM posts WHERE post_id = %s""",(post_id,))
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the post with id {post_id} can t be found")
    if res[0]["post_owner_id"] != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")