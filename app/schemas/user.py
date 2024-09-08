from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
  username: str
  email: EmailStr

class UserCreate(UserBase):
  hashed_password: str
  role_id: int

class UserUpdate(UserBase):
  hashed_password: str
  role_id: int

class UserInDB(UserBase):
  id: int
  hashed_password: str
  role_id: int