import pytest
from unittest import mock
from app.use_cases.users import signup_user, UserAlreadyExistsException
from app.schemas.user import UserSignup, UserInDB


@pytest.mark.asyncio
async def test_signup_user_success(mocker):
  
  expected_user = UserInDB(
    id=1,
    email="test@email.com",
    hashed_password="hashedpassword",
    role_id=1,
    username="testuser"
  )
  mocker.patch('app.models.user.UserModel.exists', return_value=False)
  mocker.patch('app.models.user.UserModel.create', return_value=expected_user)
  
  user_data = UserSignup(
    email=expected_user.email,
    password="password123",
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