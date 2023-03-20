from fastapi import status, HTTPException, Depends, APIRouter, Response
from dbhelper import runSQL, runSQL_return_id
from pydantic import BaseModel
from oauth2 import get_current_user

from project_helper import project_exist

# tags are just for the ui
app = APIRouter(tags=['technologies'])


@app.get("/technologies", status_code = status.HTTP_200_OK)
def get_all_technologies(user_id : int = Depends(get_current_user)):


    # get all technologies
    res = runSQL("SELECT * FROM technologies")

    return res

    