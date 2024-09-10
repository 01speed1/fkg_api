import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import AsyncMock
from app.schemas.user import UserInDB


client = TestClient(app)

@pytest.fixture
def user_data():
  return {
    "username": "testuser2",
    "password": "testpassword",
    "email": "testuser@example2.com",
    "role_id": 1
  }

def test_sign_up_success(mocker, user_data):
  mocker.patch("app.db.connections.postgres.fetch_one", AsyncMock(return_value=None))
  
  def reuse_entry_parameters(*args, **kwargs):
    return {
      **args[1],
      "id": 1,
    }
  
  expected_insert_async_mock = AsyncMock(side_effect=reuse_entry_parameters)
  
  mocker.patch("app.db.connections.postgres.insert",expected_insert_async_mock)
    
  response = client.post("/api/v1/signup", json=user_data)
      
  assert response.status_code == 201
  assert response.json() == {'status': 'success', 'message': 'User created successfully'}

def test_sign_up_existing_user(mocker, user_data):
  mocker.patch("app.db.connections.postgres.fetch_one", return_value=True)

  response = client.post("/api/v1/signup", json=user_data)
  assert response.status_code == 409
  assert response.json() == {"detail": "User already exists"}

@pytest.fixture
def invalid_user_data():
  return {
    "username": "testuser",
    "password": "short",
    "email": "invalidemail"
  }

def test_sign_up_invalid_data(invalid_user_data):
  response = client.post("/api/v1/signup", json=invalid_user_data)
  assert response.status_code == 422