from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from app.use_cases.users import login_user, InvalidCredentialsException
from app.use_cases.auth import generate_jwt, decode_jwt
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")

class LoginRequest(BaseModel):
  username: str
  password: str
  
class TokenResponse(BaseModel):
  access_token: str
  token_type: str
  
async def get_current_user(token: str =  Annotated[str, Depends(oauth2_scheme)]):
  try:
    payload = decode_jwt(token)
    return payload["data"]
  except Exception:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid authentication credentials",
    )

@router.post("/", response_model=TokenResponse)
async def login(request:  Annotated[OAuth2PasswordRequestForm, Depends()]):
      
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
      "role_id": user.role_id,
      "id": user.id,
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