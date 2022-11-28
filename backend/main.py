from fastapi import FastAPI
import uvicorn


app = FastAPI()

@app.get("/")
def read_root():
    return {"data":"hello"}



if __name__ == "__main__":
    uvicorn.run("main:app", host = "127.0.0.1", port = 3000, reload=True)