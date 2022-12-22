from fastapi import status, HTTPException, Depends, APIRouter, Response
from dbhelper import runSQL, Database
from pydantic import BaseModel
from oauth2 import get_current_user

# tags are just for the ui
app = APIRouter(tags=['invites'])



@app.get("/projects/{project_id}/invites", status_code = status.HTTP_200_OK)
def main(project_id: int, user_id : int = Depends(get_current_user)):
    # check if project exits
    res = runSQL("""SELECT * FROM projects WHERE project_id = %s""",(project_id,))
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the project with id {project_id} can t be found")
    # check if user is admin 
    res = runSQL("""SELECT * FROM members WHERE project_id = %s AND user_id = %s""", (project_id, user_id))
    if res["member_role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not Not authorized")

    res = runSQL("""SELECT * FROM invites WHERE project_id = %s""", (project_id,))

    return res



@app.post("/projects/{project_id}/invites", status_code = status.HTTP_201_CREATED)
def main(project_id: int, user_id : int = Depends(get_current_user)):
    ...

@app.delete("/projects/{project_id}/invites/{invite_id}", status_code=status.HTTP_204_NO_CONTENT)
def main(project_id: int, invite_id: int, user_id : int = Depends(get_current_user)):
    ...





