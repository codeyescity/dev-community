from fastapi import status, HTTPException, Depends, APIRouter, Response
from dbhelper import runSQL, runSQL_return_id
from pydantic import BaseModel
from oauth2 import get_current_user


# tags are just for the ui
app = APIRouter(tags=['teams'])

class Team(BaseModel):
    team_name: str

@app.get("/projects/{project_id}/teams", status_code = status.HTTP_200_OK)
def get_all_teams(project_id: int, user_id : int = Depends(get_current_user)):
    # check if project exits
    res = runSQL("""SELECT * FROM projects WHERE project_id = %s""",(project_id,))
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the project with id {project_id} can t be found")
    # check if user is member for project
    res = runSQL("""SELECT * FROM members WHERE project_id = %s AND user_id = %s""", (project_id, user_id))
    if not res:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not member of this project")
    # get all teams of the project
    res = runSQL("""SELECT * FROM teams WHERE project_id = %s""", (project_id,))
    return res

@app.get("/projects/{project_id}/teams/{team_id}", status_code = status.HTTP_200_OK)
def get_team(project_id: int, team_id: int, user_id : int = Depends(get_current_user)):
    # check if project exits
    res = runSQL("""SELECT * FROM projects WHERE project_id = %s""",(project_id,))
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the project with id {project_id} can t be found")
    # check if user is member for project
    res = runSQL("""SELECT * FROM members WHERE project_id = %s AND user_id = %s""", (project_id, user_id))
    if not res:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not member of this project")
    # get all teams of the project
    res = runSQL("""SELECT * FROM teams WHERE project_id = %s""", (project_id,))
    return res

@app.post("/projects/{project_id}/teams", status_code = status.HTTP_201_CREATED)
def create_team(project_id: int, team: Team, user_id : int = Depends(get_current_user)):
    # check if project exits
    res = runSQL("""SELECT * FROM projects WHERE project_id = %s""",(project_id,))
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the project with id {project_id} can t be found")
    # check if user is member for project
    res = runSQL("""SELECT * FROM members WHERE project_id = %s AND user_id = %s""", (project_id, user_id))
    if not res:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not member of this project")
    # check if the member is admin
    if res[0]["member_role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not admin of this project")

    # create team
    res = runSQL("""INSERT INTO teams (team_name, project_id) VALUES (%s,%s);""",(team.team_name, project_id))
    return res

@app.delete("/projects/{project_id}/teams/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_team(project_id: int, team_id: int, user_id : int = Depends(get_current_user)):
    # check if project exits
    res = runSQL("""SELECT * FROM projects WHERE project_id = %s""",(project_id,))
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the project with id {project_id} can t be found")
    # check if user is member for project
    res = runSQL("""SELECT * FROM members WHERE project_id = %s AND user_id = %s""", (project_id, user_id))
    if not res:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not member of this project")
    # check if the member is admin
    if res[0]["member_role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not admin of this project")

    # check if the team exist
    res = runSQL("""SELECT * FROM teams WHERE team_id = %s""", (team_id,))
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the team with id {team_id} can t be found")

    # remove team
    runSQL("""DELETE FROM teams WHERE project_id = %s AND team_id = %s""", (project_id,team_id))
    return Response(status_code=status.HTTP_204_NO_CONTENT)


    

