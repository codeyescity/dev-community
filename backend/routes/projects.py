from fastapi import status, HTTPException, Depends, APIRouter, Response
from dbhelper import runSQL, runSQL_return_id
from pydantic import BaseModel
from oauth2 import get_current_user

# tags are just for the ui
app = APIRouter(tags=['projects'])

class Project(BaseModel):
    project_name: str
    project_description: str


@app.get("/projects/{project_id}", status_code = status.HTTP_200_OK)
def get_project(project_id: int, user_id : int = Depends(get_current_user)):
    # check if project exits
    res = runSQL("""SELECT * FROM projects WHERE project_id = %s""",(project_id,))
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the project with id {project_id} can t be found")
    # check if user is member for project
    res = runSQL("""SELECT * FROM members WHERE project_id = %s AND user_id = %s""", (project_id, user_id))
    if not res:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not member of this project")
    #################### need change(more info for main page maybe use joins ?)
    res = runSQL("""SELECT * FROM projects WHERE project_id = %s""", (project_id,))
    return res


@app.post("/projects", status_code = status.HTTP_201_CREATED)
def create_project(project : Project, user_id : int = Depends(get_current_user)):
    # create project with the as the current user as the admin of the project
    project_id = runSQL_return_id("""INSERT INTO projects (project_owner_id, project_name, project_description, project_creation_date) VALUES (%s,%s,%s,NOW());""" ,(user_id, project.project_name, project.project_description));
    res = runSQL("""INSERT INTO members (member_role, user_id, project_id,member_join_date) VALUES (%s,%s,%s,NOW());""", ("admin", user_id, project_id));

    res = runSQL("""SELECT * FROM projects WHERE project_id = %s""", (project_id,))
    return res


@app.put("/projects/{project_id}", status_code = status.HTTP_200_OK)
def edit_project(project_id: int, project: Project, user_id : int = Depends(get_current_user)):
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
    # update project info and return the new info
    res = runSQL("""UPDATE projects SET project_name = %s, project_description = %s WHERE project_id = %s""",(project.project_name, project.project_description, project_id))
    res = runSQL("""SELECT * FROM projects WHERE project_id = %s""",(project_id,))

    return res



@app.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def edit_project(project_id: int, user_id : int = Depends(get_current_user)):
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
    # delete project
    runSQL("""DELETE FROM projects WHERE project_id = %s""",(project_id,))

    return Response(status_code=status.HTTP_204_NO_CONTENT)