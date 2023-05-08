from fastapi import status, HTTPException, Depends, APIRouter, Response
from dbhelper import runSQL, Database, runSQL_return_id
from pydantic import BaseModel
from oauth2 import get_current_user


from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from dbhelper import runSQL

import uvicorn
from datetime import datetime
import json
#image hosting
from fastapi.staticfiles import StaticFiles


from fastapi.middleware.cors import CORSMiddleware


# tags are just for the ui
#app = APIRouter(tags=['chat'])

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
            message_time = str(datetime.now())
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
    uvicorn.run("chat:app", host = "127.0.0.1", port = 5000, reload=True)



