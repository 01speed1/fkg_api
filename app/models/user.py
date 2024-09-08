from app.db.connections.postgres import init_connection, execute, fetch, close_connection
from app.schemas.user import UserCreate, UserUpdate, UserInDB

class UserModel:
  def __init__(self):
    self.conn = None
      
  async def connect(self):
    self.conn = await init_connection()
  
  async def disconnect(self):
    await close_connection(self.conn)

  async def create_user(self, user: UserCreate) -> UserInDB:
    await self.connect()
    
    query = """
    INSERT INTO users (username, email, hashed_password, role_id)
    VALUES ($1, $2, $3, $4)
    RETURNING id, username, email, hashed_password, role_id
    """
    values = (user.username, user.email, user.hashed_password)
    
    creted_user = await execute(self.conn, query, values)
    
    await self.disconnect()
    
    return UserInDB(**creted_user)

  async def get_user_by_id(self, user_id: int) -> UserInDB:
    query = "SELECT id, username, email, hashed_password FROM users WHERE id = $1"
    row = await fetch(self.conn, query, (user_id))
    if row:
      return UserInDB(**row)
    return None
  
  async def user_exists(self, username: str, email: str) -> bool:
    await self.connect()
    
    query = "SELECT 1 FROM users WHERE username = $1 OR email = $2"
    found_user = await fetch(self.conn, query, (username, email))
    
    await self.disconnect()
    
    return found_user is not None

  async def update_user(self, user_id: int, user: UserUpdate) -> UserInDB:
    query = """
    UPDATE users
    SET username = $1, email = $2, hashed_password = $3
    WHERE id = $4
    RETURNING id, username, email, hashed_password
    """
    row = await self.conn.fetchrow(query, user.username, user.email, user.hashed_password, user_id)
    if row:
      return UserInDB(**row)
    return None

  async def delete_user(self, user_id: int) -> bool:
    query = "DELETE FROM users WHERE id = $1"
    result = await self.conn.execute(query, user_id)
    return result == "DELETE 1"