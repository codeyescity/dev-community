from fastapi import status, HTTPException, Depends, APIRouter, Response
from dbhelper import runSQL, runSQL_return_id
from pydantic import BaseModel
from oauth2 import get_current_user

from project_helper import user_member_project, project_exist, user_admin_project, team_exits, member_not_part_team_in_project, member_id_part_project

# tags are just for the ui
app = APIRouter(tags=['team_members'])





@app.get("/projects/{project_id}/teams/{team_id}/members", status_code = status.HTTP_201_CREATED)
def get_team_members(project_id: int, team_id: int, user_id : int = Depends(get_current_user)):

    project_exist(project_id)
    user_member_project(user_id, project_id)
    team_exits(team_id)
    res = runSQL("""SELECT * FROM team_members tm
                LEFT JOIN members m ON m.member_id = tm.member_id
                LEFT JOIN users u ON m.user_id = u.user_id
                WHERE tm.team_id = %s""", (team_id,))
    return res




@app.post("/projects/{project_id}/teams/{team_id}/members/{member_id}", status_code = status.HTTP_201_CREATED)
def add_team_member(project_id: int, team_id: int, member_id: int, user_id : int = Depends(get_current_user)):
    
    project_exist(project_id)
    user_admin_project(user_id, project_id)
    team_exits(team_id)
    member_id_part_project(member_id, project_id)
    member_not_part_team_in_project(member_id, project_id)
    # add member to the team
    res = runSQL("""INSERT INTO team_members (team_id, member_id) VALUES (%s,%s)""",(team_id, member_id) )
    return res


    
@app.delete("/projects/{project_id}/teams/{team_id}/members/{member_id}", status_code = status.HTTP_204_NO_CONTENT)
def remove_member_from_team(project_id: int, team_id: int, member_id: int, user_id : int = Depends(get_current_user)):

    project_exist(project_id)
    user_admin_project(user_id, project_id)  
    team_exits(team_id)
    member_part_team(member_id, team_id)
    # add member to the team
    runSQL("""DELETE FROM team_members WHERE member_id = %s AND team_id = %s""",(member_id, team_id))

    return Response(status_code=status.HTTP_204_NO_CONTENT)

