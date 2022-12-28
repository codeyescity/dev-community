
from fastapi import FastAPI
import uvicorn

#image hosting
from fastapi.staticfiles import StaticFiles

from fastapi.middleware.cors import CORSMiddleware
# importing routes from other files
from routes import posts, comments, users, login, projects, invites, user_invites, members, teams, team_members

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login.app)
app.include_router(users.app)
app.include_router(user_invites.app)
app.include_router(posts.app)
app.include_router(comments.app)
app.include_router(invites.app)
app.include_router(projects.app)
app.include_router(members.app)
app.include_router(teams.app)
app.include_router(team_members.app)


@app.get("/")
def read_root():
    return {"data":"data"}


if __name__ == "__main__":
    uvicorn.run("main:app", host = "127.0.0.1", port = 5000, reload=True)
