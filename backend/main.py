
from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from dbhelper import runSQL

import uvicorn
from datetime import datetime
import json
#image hosting
from fastapi.staticfiles import StaticFiles

from fastapi.middleware.cors import CORSMiddleware
# importing routes from other files
from routes import posts, comments, users, login, projects, invites, user_invites, members, teams, team_members, chat, tasks, autotasks, technologies

app = FastAPI()
#
#app.mount("/static", StaticFiles(directory="static"), name="static")

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
app.include_router(chat.app)
app.include_router(tasks.app)
app.include_router(autotasks.app)
app.include_router(technologies.app)
app.include_router(chat.app)

if __name__ == "__main__":
    uvicorn.run("main:app", host = "127.0.0.1", port = 3000, reload=True)
