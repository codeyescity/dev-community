from fastapi import status, HTTPException, Depends, APIRouter, Response
from dbhelper import runSQL, runSQL_return_id
from pydantic import BaseModel
from oauth2 import get_current_user

from project_helper import project_exist, user_admin_project, user_member_project, team_exits

# tags are just for the ui
app = APIRouter(tags=['teams'])

class Team(BaseModel):
    team_name: str

@app.get("/projects/{project_id}/teams", status_code = status.HTTP_200_OK)
def get_all_teams(project_id: int, user_id : int = Depends(get_current_user)):
    project_exist(project_id)
    user_member_project(user_id, project_id)

    # get all teams of the project
    res = runSQL("""SELECT * FROM teams WHERE project_id = %s""", (project_id,))
    return res

@app.get("/projects/{project_id}/teams/{team_id}", status_code = status.HTTP_200_OK)
def get_team(project_id: int, team_id: int, user_id : int = Depends(get_current_user)):
    project_exist(project_id)
    user_member_project(user_id, project_id)

    # get all teams of the project
    res = runSQL("""SELECT * FROM teams WHERE project_id = %s""", (project_id,))
    return res

@app.post("/projects/{project_id}/teams", status_code = status.HTTP_201_CREATED)
def create_team(project_id: int, team: Team, user_id : int = Depends(get_current_user)):
    project_exist(project_id)
    user_admin_project(user_id, project_id)

    # create team
    res = runSQL("""INSERT INTO teams (team_name, project_id) VALUES (%s,%s);""",(team.team_name, project_id))
    return res

@app.delete("/projects/{project_id}/teams/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_team(project_id: int, team_id: int, user_id : int = Depends(get_current_user)):
    project_exist(project_id)
    user_admin_project(user_id, project_id)
    team_exits(team_id)

    # remove team
    runSQL("""DELETE FROM teams WHERE project_id = %s AND team_id = %s""", (project_id,team_id))
    return Response(status_code=status.HTTP_204_NO_CONTENT)


    

