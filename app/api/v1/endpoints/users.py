from fastapi import APIRouter, HTTPException
from typing import List

from pydantic import BaseModel

from app.schemas.user import UserCreate
from app.models.user import UserModel

router = APIRouter()

class UsersEndpointResponse(BaseModel):
  status: str
  message: str
  data: dict = None

@router.post("/", response_model=UsersEndpointResponse)
async def create_user(user_in: UserCreate):
    user_model = UserModel()
    #try:        
    user_exists = await user_model.user_exists(user_in.username, user_in.email)
      
    if user_exists:
      return UsersEndpointResponse(
        status="error",
        message="User already exists",
        data=None
      )
    
    created_user = await user_model.create_user(user_in)

    #finally:
      #await user_model.disconnect()

""" @router.get("/", response_model=List[schemas.User])
async def read_users(skip: int = 0, limit: int = 10):
    conn = await connect_to_db()
    try:
        query = "SELECT * FROM users LIMIT $1 OFFSET $2"
        users = await conn.fetch(query, limit, skip)
        return [{"id": row["id"], "name": row["name"], "email": row["email"]} for row in users]
    finally:
        await disconnect_from_db(conn)

@router.get("/{user_id}", response_model=schemas.User)
async def read_user(user_id: int):
    conn = await connect_to_db()
    try:
        query = "SELECT * FROM users WHERE id = $1"
        user = await conn.fetchrow(query, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return {"id": user["id"], "name": user["name"], "email": user["email"]}
    finally:
        await disconnect_from_db(conn)

@router.put("/{user_id}", response_model=schemas.User)
async def update_user(user_id: int, user_in: schemas.UserUpdate):
    conn = await connect_to_db()
    try:
        query = "SELECT * FROM users WHERE id = $1"
        user = await conn.fetchrow(query, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        query = "UPDATE users SET name = $1, email = $2, hashed_password = $3 WHERE id = $4"
        await conn.execute(query, user_in.name, user_in.email, user_in.hashed_password, user_id)
        return {**user_in.dict(), "id": user_id}
    finally:
        await disconnect_from_db(conn)

@router.delete("/{user_id}", response_model=schemas.User)
async def delete_user(user_id: int):
    conn = await connect_to_db()
    try:
        query = "SELECT * FROM users WHERE id = $1"
        user = await conn.fetchrow(query, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        query = "DELETE FROM users WHERE id = $1"
        await conn.execute(query, user_id)
        return {"id": user["id"], "name": user["name"], "email": user["email"]}
    finally:
        await disconnect_from_db(conn) """
