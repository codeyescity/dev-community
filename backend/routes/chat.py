from fastapi import status, HTTPException, Depends, APIRouter, Response
from dbhelper import runSQL, Database, runSQL_return_id
from pydantic import BaseModel
from oauth2 import get_current_user

# tags are just for the ui
app = APIRouter(tags=['chat'])


@app.get("/projects/{project_id}/chat", status_code = status.HTTP_200_OK)
def get_chat_log(project_id: int, start: int = 0, limit: int = 20, user_id : int = Depends(get_current_user)):
    # add checks later

    data = (project_id,)
    sql ="""SELECT 
                c.user_id,
                c.message,
                u.username,
                u.img_url,
                message_date
            FROM chatlogs c
            LEFT JOIN users u ON c.user_id = u.user_id
            WHERE c.project_id = %s
        """
    res = runSQL(sql,data)

    return res



    




