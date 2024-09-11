from app.models.user import UserModel
from app.schemas.user import UserSignup, UserInDB, UserCreate
from app.utils.security import encrypt_password, verify_password

async def signup_user(user_data: UserSignup) -> UserInDB:
    user_model = UserModel()
    
    user_exists = await user_model.exists(user_data.username, user_data.email)
    
    if user_exists:
        raise UserAlreadyExistsException("User already exists")
    
    hashed_password = encrypt_password(user_data.password)
    
    new_user = UserCreate(
        email=user_data.email,
        hashed_password=hashed_password,
        role_id=user_data.role_id,
        username=user_data.username
    )
    
    created_user = await user_model.create(new_user)
    return created_user
  
async def login_user(username: str, password: str) -> UserInDB:
  user_model = UserModel()
  
  found_user = await user_model.get_by_username(username)
  
  if not found_user or not verify_password(password, found_user.hashed_password):
    raise InvalidCredentialsException("Invalid username or password")
  
  return found_user

class InvalidCredentialsException(Exception):
  def __init__(self, message="Invalid username or password"):
    self.message = message
    super().__init__(self.message)

class UserAlreadyExistsException(Exception):
    def __init__(self, message="User already exists"):
        self.message = message
        super().__init__(self.message)