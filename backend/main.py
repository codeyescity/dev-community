from fastapi import FastAPI
import sqlite3
import uvicorn
# importing routes from other files
from routes import posts,comments

app = FastAPI()
app.include_router(posts.app)
app.include_router(comments.app)

@app.get("/")
def read_root():
    return {"data":"data"}



if __name__ == "__main__":
    uvicorn.run("main:app", host = "127.0.0.1", port = 3000, reload=True)
