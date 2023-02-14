from fastapi import status, HTTPException, Depends, APIRouter, Response
from dbhelper import runSQL, Database
from pydantic import BaseModel
from oauth2 import get_current_user

# tags are just for the ui
app = APIRouter(tags=['project invites'])

class Invite(BaseModel):
    username : str

@app.get("/projects/{project_id}/invites", status_code = status.HTTP_200_OK)
def get_all_invites_project(project_id: int, user_id : int = Depends(get_current_user)):
    # check if project exits
    res = runSQL("""SELECT * FROM projects WHERE project_id = %s""",(project_id,))
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the project with id {project_id} can t be found")
    # check if user is admin 
    res = runSQL("""SELECT * FROM members WHERE project_id = %s AND user_id = %s""", (project_id, user_id))
    if res[0]["member_role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not Not authorized in this project with id {project_id}")

    res = runSQL("""SELECT 
                    i.invite_id,
                    i.user_id,
                    i.project_id,
                    i.invite_date,
                    u.username,
                    u.img_url 
                    FROM invites i
                    LEFT JOIN  users u ON u.user_id = i.user_id
                    WHERE project_id = %s""", (project_id,))

    return res

@app.get("/projects/{project_id}/allusertobeinvited", status_code = 200)
def get_all_users_can_be_invited(project_id: int, user_id: int = Depends(get_current_user)):
    # get all user not member in project and user don t have invite to this project
    res = runSQL("""SELECT user_id,username,img_url,first_name,last_name,email,phone_number FROM users 
                    WHERE user_id NOT IN 
                    ( 
                        SELECT user_id FROM members WHERE project_id = %s 
                    ) AND user_id NOT IN 
                    (
                        SELECT user_id FROM invites WHERE project_id = %s
                    )
                    """,(project_id,project_id))
    return res

@app.post("/projects/{project_id}/invites", status_code = status.HTTP_201_CREATED)
def create_invite_for_user(project_id: int, invite : Invite, user_id : int = Depends(get_current_user)):
    # check if project exits
    res = runSQL("""SELECT * FROM projects WHERE project_id = %s""",(project_id,))
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the project with id {project_id} can t be found")
    # check if user is admin 
    res = runSQL("""SELECT * FROM members WHERE project_id = %s AND user_id = %s""", (project_id, user_id))
    if res[0]["member_role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not Not authorized in this project with id {project_id}")
    # check if the username exists
    res = runSQL("""SELECT * FROM users WHERE username = %s""", (invite.username,))
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with name: '{invite.username}' does not exist")
    # check if the user was already invited to the project
    invited_user_id = res[0]["user_id"]
    res = runSQL("""SELECT * FROM invites WHERE project_id = %s AND user_id = %s;""",(project_id, invited_user_id))
    if res:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User with name: '{invite.username}' is already invited")
    # add invite
    res = runSQL("""INSERT INTO invites (user_id, project_id, invite_date) VALUES (%s,%s,NOW());""",(invited_user_id, project_id))
    return res

@app.delete("/projects/{project_id}/invites/{invite_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_invite(project_id: int, invite_id: int, user_id : int = Depends(get_current_user)):
    # check if project exits
    res = runSQL("""SELECT * FROM projects WHERE project_id = %s""",(project_id,))
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the project with id {project_id} can t be found")
    # check if user is admin 
    res = runSQL("""SELECT * FROM members WHERE project_id = %s AND user_id = %s""", (project_id, user_id))
    if res[0]["member_role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not Not authorized")
    # search for the invite in the invites table
    res  = runSQL("""SELECT * FROM invites WHERE invite_id = %s """, (invite_id,))
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the project with id {project_id} can t be found")

    runSQL("""DELETE FROM invites WHERE invite_id = %s """, (invite_id,))

    return Response(status_code=status.HTTP_204_NO_CONTENT)




