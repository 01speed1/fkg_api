from pydantic import BaseModel, EmailStr, ConfigDict

class UserBase(BaseModel):
  username: str
  email: EmailStr

class UserSignup(UserBase):
  password: str
  role_id: int
  
class UserLogin(UserBase):
  password: str

class UserCreate(UserBase):
  hashed_password: str
  role_id: int

  model_config = ConfigDict(from_attributes=True)

class UserUpdate(UserBase):
  hashed_password: str
  role_id: int

class UserInDB(UserBase):
  id: int
  hashed_password: str
  role_id: int