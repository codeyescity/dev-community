from fastapi import status, HTTPException, Depends, APIRouter, Response
from dbhelper import runSQL, runSQL_return_id
from pydantic import BaseModel
from oauth2 import get_current_user

from project_helper import project_exist

# tags are just for the ui
app = APIRouter(tags=['technologies'])

class UserSkill(BaseModel):
    user_skills : dict[int,int]



@app.get("/technologies", status_code = status.HTTP_200_OK)
def get_all_technologies(user_id : int = Depends(get_current_user)):


    # get all technologies
    res = runSQL("SELECT * FROM technologies")

    return res


@app.put("/user_technologies", status_code = status.HTTP_200_OK)
def get_all_technologies(skills : UserSkill, user_id : int = Depends(get_current_user)):


    for tech_id in skills.user_skills:
        print(tech_id , skills.user_skills[tech_id])
        res = runSQL("UPDATE users_technologies SET technology_experience = %s WHERE technology_id = %s AND user_id = %s", (skills.user_skills[tech_id], tech_id, user_id))
        #print(res)

    # get all technologies

    return res
   