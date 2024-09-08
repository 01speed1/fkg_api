from typing import Union
from fastapi import FastAPI
import psycopg

app = FastAPI()

DATABASE_URL = "postgresql://postgres:password@postgres_db:5432/postgres"

@app.on_event("startup")
async def startup():
    global conn
    conn = await psycopg.AsyncConnection.connect(DATABASE_URL)

@app.on_event("shutdown")
async def shutdown():
    await conn.close()

@app.get("/")
async def root():
    try:
        async with conn.cursor() as cur:
            await cur.execute("SELECT 1")
            result = await cur.fetchone()
        return {"status": "Connection successful", "result": result}
    except Exception as e:
        return {"status": "Connection failed", "error": str(e)}