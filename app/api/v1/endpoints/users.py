from fastapi import APIRouter, HTTPException

from pydantic import BaseModel

from app.schemas.user import UserCreate
from app.models.user import UserModel
from fastapi import status

router = APIRouter()

class UsersEndpointResponse(BaseModel):
  status: str
  message: str
  data: dict = None

@router.post("/", response_model=UsersEndpointResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate):
  user_model = UserModel()

  user_exists = await user_model.exists(user_in.username, user_in.email)
  
  if user_exists:
    raise HTTPException(
      status_code=status.HTTP_409_CONFLICT,
      detail="User already exists"
    )

  created_user = await user_model.create(user_in)

  return UsersEndpointResponse(
    status="success",
    message="User created successfully",
    data={"id": created_user.id, "username": created_user.username, "email": created_user.email}
  )

