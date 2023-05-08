from fastapi import status, HTTPException, Depends, APIRouter, Response
from dbhelper import runSQL, Database
from pydantic import BaseModel


# weird hack to import 
import sys
sys.path.append("..")
from oauth2 import  get_current_user

app = APIRouter(tags=['users_invites'])



@app.get("/user/invites/", status_code = status.HTTP_200_OK)
def get_user_invites(user_id : int = Depends(get_current_user)):
    # get all the invites of the current user
    res = runSQL(""" SELECT * FROM invites 
                     LEFT JOIN projects ON invites.project_id = projects.project_id
                     WHERE user_id = %s""", (user_id,))
    return res

@app.post("/user/invites/{invite_id}", status_code = status.HTTP_201_CREATED)
def accept_invite(invite_id: int, user_id : int = Depends(get_current_user)):
    # check if there is invite 
    res = runSQL(""" SELECT * FROM invites WHERE invite_id = %s""", (invite_id,))
    if not res:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"the invite with the id {invite_id} can t be found")
    # check if the invite is for the current user 
    if res[0]["user_id"] != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    # add the member to the member of the project and remove the invite
    invited_user_id = res[0]["user_id"]
    project_id = res[0]["project_id"]
    member_role = res[0]["invite_role"]
    res = runSQL("""INSERT INTO members (user_id, project_id, member_role, member_join_date) VALUES (%s,%s,%s,NOW());""", (invited_user_id, project_id, member_role))
    runSQL(""" DELETE FROM invites WHERE invite_id = %s""", (invite_id,))

    return res

@app.delete("/user/invites/{invite_id}", status_code=status.HTTP_204_NO_CONTENT)
def decline_invite(invite_id: int, user_id : int = Depends(get_current_user)):
    # check if there is invite 
    res = runSQL(""" SELECT * FROM invites WHERE invite_id = %s""", (invite_id,))
    if not res:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"the invite with the id {invite_id} can t be found")
    # check if the invite is for the current user 
    if res[0]["user_id"] != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    runSQL(""" DELETE FROM invites WHERE invite_id = %s""", (invite_id,))

    return Response(status_code=status.HTTP_204_NO_CONTENT)