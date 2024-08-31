from fastapi import FastAPI
from parul import Parul
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
