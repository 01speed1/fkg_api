from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.use_cases.users import login_user, InvalidCredentialsException
from app.use_cases.auth import generate_jwt

router = APIRouter()

class LoginRequest(BaseModel):
  username: str
  password: str
  
class TokenResponse(BaseModel):
  access_token: str
  token_type: str

@router.post("/", response_model=TokenResponse)
async def login(request: LoginRequest):
    
  try:
    user = await login_user(
      username=request.username, password=request.password
    )
    if not user:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Incorrect email or password",
      )
    
    access_token = generate_jwt({
      "email": user.email,
      "username": user.username ,
      "role_id": user.role_id
    })
    
    return {
      "access_token": access_token,
      "token_type": "bearer",
    }

  except InvalidCredentialsException as e:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail=str(e),
    )