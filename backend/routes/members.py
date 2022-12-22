from fastapi import status, HTTPException, Depends, APIRouter, Response
from dbhelper import runSQL, runSQL_return_id
from pydantic import BaseModel
from oauth2 import get_current_user


# tags are just for the ui
app = APIRouter(tags=['project_members'])

# ----------------------> edit member / admin

@app.get("/projects/{project_id}/members", status_code = status.HTTP_200_OK)
def get_project_members(project_id: int, user_id : int = Depends(get_current_user)):
    # check if project exits
    res = runSQL("""SELECT * FROM projects WHERE project_id = %s""",(project_id,))
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the project with id {project_id} can t be found")
    # check if user is member for project
    res = runSQL("""SELECT * FROM members WHERE project_id = %s AND user_id = %s""", (project_id, user_id))
    if not res:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not member of this project")
    # get the list of the member of the project
    res = runSQL("""SELECT * FROM members m
                LEFT JOIN users u ON m.user_id = u.user_id
                WHERE project_id = %s """, (project_id,))
    return res


@app.delete("/projects/{project_id}/members/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_member_from_project(project_id: int, member_id: int, user_id : int = Depends(get_current_user)):
    # check if project exits
    res = runSQL("""SELECT * FROM projects WHERE project_id = %s""",(project_id,))
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the project with id {project_id} can t be found")
    # check if current user is member for project
    res = runSQL("""SELECT * FROM members WHERE project_id = %s AND user_id = %s""", (project_id, user_id))
    if not res:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not member of this project")
    # check if the member is admin
    if res[0]["member_role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not admin of this project")
    # check if the member is in the project
    res = runSQL("""SELECT * FROM members WHERE member_id = %s""", (member_id,))
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the member with id {member_id} can t be found")
    # remove member from the project
    runSQL("""DELETE FROM members WHERE member_id = %s""", (member_id,))


    return Response(status_code=status.HTTP_204_NO_CONTENT)

