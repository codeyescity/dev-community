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
app = APIRouter(tags=['chat'])

"""
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
            runSQL("INSERT INTO chatlogs (user_id, project_id, message, message_date) VALUES (%s,%s,%s,NOW())",(data['senderId'], project_id, data['message']))
            
            
            await manager.broadcast_project(json.dumps(payload), project_id)
            
    # This code will be executed when a connection closed
    except WebSocketDisconnect:
        manager.disconnect(websocket, project_id)
        #message = { 'project_id': project_id, "body": "Offline" }
        #await manager.broadcast_project(json.dumps(message), project_id)


"""


@app.get("/projects/{project_id}/chat", status_code = status.HTTP_200_OK)
def get_chat_log(project_id: int, start: int = 0, limit: int = 20, user_id : int = Depends(get_current_user)):
    # add checks later

    data = (project_id,)
    sql ="SELECT c.user_id, c.message, u.username, u.img_url, message_date FROM chatlogs c LEFT JOIN users u ON c.user_id = u.user_id WHERE c.project_id = %s"
    res = runSQL(sql,data)

    return res



    




