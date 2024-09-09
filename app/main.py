import os
from fastapi import FastAPI

from dotenv import load_dotenv

from app.api.v1.endpoints.users import router as user_router
from app.api.v1.endpoints.signup import router as signup_router

env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

app = FastAPI()

app.include_router(user_router)
app.include_router(signup_router)

@app.get("/hello")
def read_hello() -> dict:
  return {"message": "Hello, world!"}