import pytest

from unittest.mock import AsyncMock

from app.models.user import UserModel
from app.schemas.user import UserCreate, UserInDB

@pytest.mark.asyncio
async def test_create_user(mocker): 
    mock_insert = AsyncMock(return_value={
        "id": 1,
        "username": "testuser",
        "email": "test@email.com",
        "hashed_password": "hashedpassword",
        "role_id": 1
    })
    mocker.patch('app.db.connections.postgres.insert', mock_insert)
      
    expected_user = UserInDB(
        id=1,
        username="testuser",
        email="test@email.com",
        hashed_password="hashedpassword",
        role_id=1
    )

    user_in = UserCreate(
        username=expected_user.username,
        email=expected_user.email,
        hashed_password=expected_user.hashed_password,
        role_id=expected_user.role_id
    )

    user_model = UserModel()

    created_user = await user_model.create(user_in)
    
    mock_insert.assert_called_once_with('users', {
      'username': expected_user.username,
      'email': expected_user.email,
      'hashed_password': expected_user.hashed_password,
      'role_id': expected_user.role_id
      })

    assert created_user.id == expected_user.id
    assert created_user.username == expected_user.username
    assert created_user.email == expected_user.email
    assert created_user.hashed_password == expected_user.hashed_password
    assert created_user.role_id == expected_user.role_id

@pytest.mark.asyncio
async def test_create_user_already_exists(mocker):
  mock_insert = AsyncMock(side_effect=Exception("User already exists"))
  mocker.patch('app.db.connections.postgres.insert', mock_insert)

  user_model = UserModel()

  user_in = UserCreate(
    username="existinguser",
    email="existinguser@example.com",
    hashed_password="hashedpassword",
    role_id=1
  )

  with pytest.raises(Exception) as excinfo:
    await user_model.create(user_in)

  mock_insert.assert_called_once_with('users', {
    'username': user_in.username,
    'email': user_in.email,
    'hashed_password': user_in.hashed_password,
    'role_id': user_in.role_id
  })

  assert str(excinfo.value) == "User already exists"
  
@pytest.mark.asyncio
async def test_user_exists_true(mocker):
  mock_fetch_one = AsyncMock(return_value={"id": 1})
  mocker.patch('app.db.connections.postgres.fetch_one', mock_fetch_one)

  user_model = UserModel()

  user_in = UserCreate(
    username="existinguser",
    email="existinguser@example.com",
    hashed_password="hashedpassword",
    role_id=1
  )

  exists = await user_model.exists(user_in.username)

  mock_fetch_one.assert_called_once_with('SELECT 1 FROM users WHERE username = %s OR email = %s', ( user_in.username, ""))

  assert exists is True

@pytest.mark.asyncio
async def test_user_exists_false(mocker):
  mock_fetch_one = AsyncMock(return_value=None)
  mocker.patch('app.db.connections.postgres.fetch_one', mock_fetch_one)

  user_model = UserModel()

  user_in = UserCreate(
    username="nonexistentuser",
    email="nonexistentuser@example.com",
    hashed_password="hashedpassword",
    role_id=1
  )

  exists = await user_model.exists(user_in.username)

  mock_fetch_one.assert_called_once_with('SELECT 1 FROM users WHERE username = %s OR email = %s', ( user_in.username, ""))

  assert exists is False
