import pytest
from app.use_cases.users import signup_user, UserAlreadyExistsException, login_user, InvalidCredentialsException
from app.schemas.user import UserSignup, UserInDB
from app.schemas.user import UserInDB
from app.utils.security import encrypt_password

@pytest.fixture
def hashed_password():
    return encrypt_password("plainpassword")

@pytest.mark.asyncio
async def test_signup_user_success(mocker, hashed_password):
  
  expected_user = UserInDB(
    id=1,
    email="test@email.com",
    hashed_password=hashed_password,
    role_id=1,
    username="testuser"
  )
  mocker.patch('app.models.user.UserModel.exists', return_value=False)
  mocker.patch('app.models.user.UserModel.create', return_value=expected_user)
  
  user_data = UserSignup(
    email=expected_user.email,
    password="plainpassword",
    role_id=expected_user.role_id,
    username=expected_user.username
  )
    
  user_signedup = await signup_user(user_data)

  assert user_signedup.id == expected_user.id
  assert user_signedup.email == expected_user.email
  assert user_signedup.username == expected_user.username
  assert user_signedup.hashed_password != user_data.password
  assert user_signedup.role_id == expected_user.role_id

@pytest.mark.asyncio
async def test_signup_user_email_taken(mocker):
  mocker.patch('app.models.user.UserModel.exists', return_value=True)
  
  user_data = UserSignup(
    email='test@email.com',
    password='password123',
    role_id=1,
    username='testuser'
  )

  with pytest.raises(UserAlreadyExistsException, match='User already exists'):
    await signup_user(user_data)

@pytest.mark.asyncio
async def test_signup_user_username_taken(mocker): 
  mocker.patch('app.models.user.UserModel.exists', return_value=True)
  
  user_data = UserSignup(
    email='newemail@example.com',
    password='password123',
    role_id=1,
    username='testuser'
  )

  with pytest.raises(UserAlreadyExistsException, match='User already exists'):
    await signup_user(user_data)

@pytest.mark.asyncio
async def test_login_user_success(mocker, hashed_password):
  expected_user = UserInDB(
    id=1,
    email="test@email.com",
    hashed_password=hashed_password,
    role_id=1,
    username="testuser"
  )
  mocker.patch('app.models.user.UserModel.get_by_username', return_value=expected_user)
  mocker.patch('app.utils.security.verify_password', return_value=True)
  
  user_logged_in = await login_user("testuser", "plainpassword")
  
  assert user_logged_in.id == expected_user.id
  assert user_logged_in.email == expected_user.email
  assert user_logged_in.username == expected_user.username
  assert user_logged_in.hashed_password == expected_user.hashed_password
  assert user_logged_in.role_id == expected_user.role_id

@pytest.mark.asyncio
async def test_login_user_invalid_username(mocker):
  mocker.patch('app.models.user.UserModel.exists', return_value=None)

  with pytest.raises(InvalidCredentialsException, match='Invalid username or password'):
    await login_user("invaliduser", "password123")

@pytest.mark.asyncio
async def test_login_user_invalid_password(mocker, hashed_password):
  expected_user = UserInDB(
    id=1,
    email="test@email.com",
    hashed_password=hashed_password,
    role_id=1,
    username="testuser"
  )
  mocker.patch('app.models.user.UserModel.get_by_username',  mocker.AsyncMock(return_value=expected_user))
  mocker.patch('app.utils.security.verify_password', return_value=False)

  with pytest.raises(InvalidCredentialsException, match='Invalid username or password'):
    await login_user("testuser", "wrongpassword")