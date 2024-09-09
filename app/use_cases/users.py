from app.models.user import UserModel
from app.schemas.user import UserSignup, UserInDB, UserCreate
from app.utils.security import encrypt_password

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
  
class UserAlreadyExistsException(Exception):
    """Exception raised when a user already exists."""
    def __init__(self, message="User already exists"):
        self.message = message
        super().__init__(self.message)