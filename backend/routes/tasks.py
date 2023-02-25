from fastapi import status, HTTPException, Depends, APIRouter, Response
from dbhelper import runSQL, runSQL_return_id
from pydantic import BaseModel
from oauth2 import get_current_user

from project_helper import project_exist

# tags are just for the ui
app = APIRouter(tags=['tasks'])

class Task(BaseModel):
    task_title: str
    task_description: str
    task_type: str
    member_id : int


def validate_task_state(task_state: str):
    if(task_state in ["todo", "inprogress", "invalidation", "completed"]):
        return True
    else:
        return False

def validate_task_type(task_type: str):
    if(task_type in ["task", "bug_fix", "feature", "issue"]):
        return True
    else:
        return False

# tasks can be "todo" "inprogress" "invalidation" "completed"
# tasks need state manegment


@app.get("/projects/{project_id}/task", status_code = status.HTTP_200_OK)
def get_user_tasks(project_id: int, user_id : int = Depends(get_current_user)):
    # this route is for the user part
    project_exist(project_id)

    res = runSQL("""SELECT * FROM tasks WHERE member_id IN (SELECT member_id FROM members WHERE user_id  = %s) AND project_id = %s""", (user_id,project_id))

    return res


@app.get("/projects/{project_id}/alltasks", status_code = status.HTTP_200_OK)
def get_all_project_tasks(project_id: int, user_id : int = Depends(get_current_user)):
    # this route is for the admins only
    project_exist(project_id)
    sql ="""SELECT 
                t.task_id,
                t.member_id,
                t.task_title,
                t.task_description,
                t.task_type,
                t.task_state,
                t.task_progress,
                m.member_role,
                u.user_id,
                u.username,
                u.img_url
            FROM tasks t
            LEFT JOIN members m ON t.member_id = m.member_id
            LEFT JOIN users u ON m.user_id = u.user_id
            WHERE t.project_id = %s
        """

    data = ((project_id,))
    res = runSQL(sql,data)

    return res

@app.post("/projects/{project_id}/task", status_code = status.HTTP_201_CREATED)
def create_task(project_id: int, task: Task, user_id : int = Depends(get_current_user)):
    # for admins only
    project_exist(project_id)
    #validate task type
    data = (project_id, task.task_title, task.task_description, task.task_type, "todo", task.member_id)
    res = runSQL_return_id("""INSERT INTO tasks (project_id, task_title, task_description ,task_type, task_state, member_id) VALUES (%s,%s,%s,%s,%s,%s)""",data)

    return res
    



@app.put("/projects/{project_id}/task/{task_id}", status_code = status.HTTP_200_OK)
def edit_task(project_id: int, task_id: int, task: Task, user_id : int = Depends(get_current_user)):
    project_exist(project_id)

    data = (task.task_title, task.task_description, task.task_type, task.member_id, task_id)
    res = runSQL_return_id("""UPDATE tasks SET task_title = %s, task_description = %s, task_type = %s , member_id = %s WHERE task_id = %s""",data)

    return res

@app.delete("/projects/{project_id}/task/{task_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_task(project_id: int, task_id: int, user_id : int = Depends(get_current_user)):
    project_exist(project_id)

    res = runSQL_return_id("""DELETE FROM tasks WHERE task_id = %s""", (task_id,))

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/projects/{project_id}/task/{task_id}/state", status_code = status.HTTP_200_OK)
def change_task_state(project_id: int, task_id: int, task_state : str, user_id : int = Depends(get_current_user)):
    project_exist(project_id)

    res = runSQL("""UPDATE tasks SET task_state = %s WHERE task_id = %s""",(task_state,task_id))

    return res 

@app.put("/projects/{project_id}/task/{task_id}/progress", status_code = status.HTTP_200_OK)
def change_task_state(project_id: int, task_id: int, task_progress : int, user_id : int = Depends(get_current_user)):
    project_exist(project_id)

    res = runSQL("""UPDATE tasks SET task_progress = %s WHERE task_id = %s""",(task_progress,task_id))

    return res 

