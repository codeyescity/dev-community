from fastapi import status, HTTPException, Depends, APIRouter, Response
from dbhelper import runSQL, runSQL_return_id
from pydantic import BaseModel
from oauth2 import get_current_user

from project_helper import user_member_project, project_exist, user_admin_project

# tags are just for the ui
app = APIRouter(tags=['project_members'])


@app.get("/projects/{project_id}/members", status_code = status.HTTP_200_OK)
def get_project_members(project_id: int, user_id : int = Depends(get_current_user)):

    user_member_project(user_id, project_id)
    sql ="""SELECT 
            u.user_id,
            m.member_id,
            m.member_role,
            u.username,
            u.img_url
            FROM members m
            LEFT JOIN users u ON m.user_id = u.user_id
            WHERE project_id = %s 
        """
    data = (project_id,)

    # get the list of the member of the project
    res = runSQL(sql,data)
    return res


@app.delete("/projects/{project_id}/members/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_member_from_project(project_id: int, member_id: int, user_id : int = Depends(get_current_user)):
    
    project_exist(project_id)
    user_admin_project(user_id, project_id)
    user_member_project(member_id, project_id)

    # remove member from the project
    runSQL("""DELETE FROM members WHERE member_id = %s""", (member_id,))

    return Response(status_code=status.HTTP_204_NO_CONTENT)

