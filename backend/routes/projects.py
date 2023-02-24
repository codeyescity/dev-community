from fastapi import status, HTTPException, Depends, APIRouter, Response
from dbhelper import runSQL, runSQL_return_id
from pydantic import BaseModel
from oauth2 import get_current_user


from helper import project_exist, user_member_project, user_admin_project

# tags are just for the ui
app = APIRouter(tags=['projects'])

class Project(BaseModel):
    project_name: str
    project_description: str


@app.get("/projects/{project_id}", status_code = status.HTTP_200_OK)
def get_project(project_id: int, user_id : int = Depends(get_current_user)):
 
    project_exist(project_id)
    user_member_project(user_id, project_id)

    #################### need change(more info for main page maybe use joins ?)
    res = runSQL("""SELECT  
                    p.project_id,
                    p.project_owner_id,
                    p.project_name,
                    p.project_description,
                    m.member_id,
                    m.member_role,
                    u.username,
                    u.img_url
                    FROM projects p
                    LEFT JOIN members m ON p.project_id = m.project_id
                    LEFT JOIN users u ON u.user_id = p.project_owner_id
                    WHERE p.project_id = %s AND m.user_id = %s""", (project_id, user_id))
    return res


@app.post("/projects", status_code = status.HTTP_201_CREATED)
def create_project(project : Project, user_id : int = Depends(get_current_user)):

    # create project with the as the current user as the admin of the project
    project_id = runSQL_return_id("""INSERT INTO projects (project_owner_id, project_name, project_description, project_creation_date) VALUES (%s,%s,%s,NOW());""" ,(user_id, project.project_name, project.project_description));
    res = runSQL("""INSERT INTO members (member_role, user_id, project_id,member_join_date) VALUES (%s,%s,%s,NOW());""", ("admin", user_id, project_id));

    return project_id


@app.put("/projects/{project_id}", status_code = status.HTTP_200_OK)
def edit_project(project_id: int, project: Project, user_id : int = Depends(get_current_user)):

    project_exist(project_id)
    user_admin_project(user_id, project_id)

    # update project info and return the new info
    res = runSQL("""UPDATE projects SET project_name = %s, project_description = %s WHERE project_id = %s""",(project.project_name, project.project_description, project_id))

    return res



@app.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def edit_project(project_id: int, user_id : int = Depends(get_current_user)):

    project_exist(project_id)
    user_admin_project(user_id, project_id)
    # delete project
    runSQL("""DELETE FROM projects WHERE project_id = %s""",(project_id,))

    return Response(status_code=status.HTTP_204_NO_CONTENT)