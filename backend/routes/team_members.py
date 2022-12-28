from fastapi import status, HTTPException, Depends, APIRouter, Response
from dbhelper import runSQL, runSQL_return_id
from pydantic import BaseModel
from oauth2 import get_current_user


# tags are just for the ui
app = APIRouter(tags=['team_members'])





@app.get("/projects/{project_id}/teams/{team_id}/members", status_code = status.HTTP_201_CREATED)
def get_team_members(project_id: int, team_id: int, user_id : int = Depends(get_current_user)):
    # check if project exits
    res = runSQL("""SELECT * FROM projects WHERE project_id = %s""",(project_id,))
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the project with id {project_id} can t be found")
    # check if user is member for project
    res = runSQL("""SELECT * FROM members WHERE project_id = %s AND user_id = %s""", (project_id, user_id))
    if not res:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not member of this project")

    
    # check if the team exist
    res = runSQL("""SELECT * FROM teams WHERE team_id = %s""", (team_id,))
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the team with id {team_id} can t be found")
    res = runSQL("""SELECT * FROM team_members tm
                LEFT JOIN members m ON m.member_id = tm.member_id
                LEFT JOIN users u ON m.user_id = u.user_id
                WHERE tm.team_id = %s""", (team_id,))
    return res




@app.post("/projects/{project_id}/teams/{team_id}/members/{member_id}", status_code = status.HTTP_201_CREATED)
def add_team_member(project_id: int, team_id: int, member_id: int, user_id : int = Depends(get_current_user)):
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
    # check if user to be added to the team is member
    res = runSQL("""SELECT * FROM members WHERE project_id = %s AND member_id = %s""", (project_id, member_id))
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the member with id {member_id} is not part of the project")
    # check if member is not is already part of a team in the project
    res = runSQL("""SELECT * FROM team_members WHERE member_id = %s AND team_id IN (SELECT * FROM teams WHERE project_id = %s)""", (member_id, project_id))
    if res:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="member already part of a team")
    # add member to the team
    res = runSQL("""INSERT INTO team_members (team_id, member_id) VALUES (%s,%s)""",(team_id, member_id) )
    return res


    
@app.delete("/projects/{project_id}/teams/{team_id}/members/{member_id}", status_code = status.HTTP_204_NO_CONTENT)
def remove_member_from_team(project_id: int, team_id: int, member_id: int, user_id : int = Depends(get_current_user)):
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

    # check if member is part of the team
    res = runSQL("""SELECT * FROM team_members WHERE member_id = %s AND team_id  = %s""", (member_id, team_id))
    if not res:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="member is not part of a team")
    # add member to the team
    runSQL("""DELETE FROM team_members WHERE member_id = %s AND team_id = %s""",(member_id, team_id))

    return Response(status_code=status.HTTP_204_NO_CONTENT)

