import os
from fastapi import FastAPI

from dotenv import load_dotenv

from app.api.v1.routes import router as api_v1_router
from fastapi import Response

env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

app = FastAPI()

app.include_router(api_v1_router, prefix="/api/v1")

@app.get("/")
def home_page(response: Response) -> dict:
  response.status_code = 200
  return {"status": "ok"}