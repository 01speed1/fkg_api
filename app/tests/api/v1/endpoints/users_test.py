import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_success(mocker):
  mocker.patch('app.models.user.UserModel.exists', return_value=False)
  mock_user = mocker.AsyncMock()
  mock_user.id = 1
  mock_user.username = "newuser"
  mock_user.email = "newuser@example.com"
  mock_user.hashed_password = "securepassword"
  mock_user.role_id = 1

  mocker.patch('app.models.user.UserModel.create', return_value=mock_user)
  
  response = client.post("/api/v1/users", json={
    "username": "newuser",
    "email": "newuser@example.com",
    "hashed_password": "securepassword",
    "role_id": 1
  })
  
  print(response.json())
  
  assert response.status_code == 201
  assert response.json() == {'status': 'success', 'message': 'User created successfully', 'data': {'id': 1, 'username': 'newuser', 'email': 'newuser@example.com'}}


def test_register_existing_user(mocker):
  mocker.patch('app.models.user.UserModel.exists', return_value=True)
  
  response = client.post("/api/v1/users", json={
    "username": "existinguser",
    "email": "existinguser@example.com",
    "hashed_password": "securepassword",
    "role_id": 1
  })
  assert response.status_code == 409
  assert response.json() == {"detail": "User already exists"}

def test_register_invalid_data():
  response = client.post("/api/v1/users", json={
    "username": "",
    "email": "invalidemail",
    "password": "short"
  })
  assert response.status_code == 422
  assert "detail" in response.json()