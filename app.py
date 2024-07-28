from fastapi import FastAPI
from parul import Parul
import uvicorn
app = FastAPI()

@app.get("/")
def read_root():
    return "API is working"

@app.post("/")
def login(credentials: dict):
    parul = Parul()
    admin = credentials['admin']
    password = credentials['password']
    parul.login(admin,password)
    return parul.get_attendance()

if __name__ == "__main__":
    uvicorn.run(app)