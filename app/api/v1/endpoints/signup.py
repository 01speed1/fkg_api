from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.schemas.user import UserSignup
from app.use_cases.users import signup_user, UserAlreadyExistsException

router = APIRouter()
  
class SigUpResponse(BaseModel):
  status: str
  message: str

@router.post("/sign_up", response_model=SigUpResponse, status_code=status.HTTP_201_CREATED)
async def sign_up(user_data: UserSignup):
  try:
    await signup_user(user_data)
    
    return SigUpResponse(
      status="success",
      message="User created successfully"
    )
    
  except UserAlreadyExistsException as e:
    raise HTTPException(status_code=409, detail=str(e))