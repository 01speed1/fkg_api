from app.db.connections import postgres as db
from app.schemas.user import UserCreate, UserInDB

USERS_TABLE = "users"

class UserModel:
  async def create(self, user: UserCreate) -> UserInDB:
    created_user = await db.insert(USERS_TABLE, user.model_dump())

    return UserInDB(**created_user)

  async def exists(self, username: str = "", email: str = "") -> bool:
    query = "SELECT 1 FROM users WHERE username = %s OR email = %s"
    found_user = await db.fetch_one(query, (username, email,))
    
    return found_user is not None
