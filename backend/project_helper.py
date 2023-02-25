from fastapi import HTTPException, status
from dbhelper import runSQL, Database


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

def team_exits(team_id: int):
    res = runSQL("""SELECT * FROM teams WHERE team_id = %s""", (team_id,))
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the team with id {team_id} can t be found")

def member_part_team(member_id : int, team_id: int):
    # check if member is part of the team
    res = runSQL("""SELECT * FROM team_members WHERE member_id = %s AND team_id  = %s""", (member_id, team_id))
    if not res:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="member is not part of a team")

def member_id_part_project(member_id: int , project_id : int):
    #check if user to be added to the team is member
    res = runSQL("""SELECT * FROM members WHERE project_id = %s AND member_id = %s""", (project_id, member_id))
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the member with id {member_id} is not part of the project")

def member_not_part_team_in_project(member_id: int, project_id: int):
    # check if member is not is already part of a team in the project
    res = runSQL("""SELECT * FROM team_members WHERE member_id = %s AND team_id IN (SELECT team_id FROM teams WHERE project_id = %s)""", (member_id, project_id))
    if res:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="member already part of a team")