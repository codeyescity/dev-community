
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
from routes import posts, comments, users, login, projects, invites, user_invites, members, teams, team_members, chat, tasks

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
app.include_router(chat.app)
app.include_router(tasks.app)

@app.get("/")
def read_root():
    return {"data":"data"}



class ConnectionManager:

    def __init__(self) -> None:
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, project_id: int):
        await websocket.accept()

        try:
            self.active_connections[project_id].append(websocket)
        except :
            self.active_connections[project_id] = []
            self.active_connections[project_id].append(websocket)

        #self.active_connections.append({ 'project_id': project_id, 'websocket': websocket})

    def disconnect(self, websocket: WebSocket, project_id: int):

        try:
            self.active_connections[project_id].remove(websocket)
        except :
            print("disconnect error fix later ")
        finally:
            try:
                if(len(self.active_connections[project_id]) == 0):
                    del self.active_connections[project_id]
            except:
                print("error removing empty websocket list fix later ")

        #self.active_connections.remove({ 'project_id': project_id, 'websocket': websocket })

    async def broadcast_project(self, message: str, project_id: int):
        print(self.active_connections)
        for connection in self.active_connections[project_id]:
            await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws/{project_id}")
async def websocket_endpoint(websocket: WebSocket, project_id: int):
    await manager.connect(websocket, project_id)
    try:
        while True:
            data = json.loads(await websocket.receive_text())
            message_time = datetime.now().strftime("%H:%M")
            print(data)
            payload = { "user_id" : data['senderId'], 'message': data['message'],'sender_username': data['senderUsername'], 'sender_profile_img': data['senderProfileImg'], 'message_time': message_time }
            runSQL("""INSERT INTO chatlogs (user_id, project_id, message, message_date) VALUES (%s,%s,%s,NOW())""",(data['senderId'], project_id, data['message']))
            
            
            await manager.broadcast_project(json.dumps(payload), project_id)
            
    # This code will be executed when a connection closed
    except WebSocketDisconnect:
        manager.disconnect(websocket, project_id)
        #message = { 'project_id': project_id, "body": "Offline" }
        #await manager.broadcast_project(json.dumps(message), project_id)

if __name__ == "__main__":
    uvicorn.run("main:app", host = "127.0.0.1", port = 3000, reload=True)
