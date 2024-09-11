import pytest
from fastapi.testclient import TestClient

from app.use_cases.auth import decode_jwt, generate_jwt
from app.main import app

from app.schemas.user import UserInDB
from app.api.v1.endpoints.login import LoginRequest
import os

from app.utils.security import encrypt_password

os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"

client = TestClient(app)

@pytest.fixture
def expected_password():
  return "password123"

@pytest.fixture
def expected_hashed_password(expected_password):
  return encrypt_password(expected_password)

@pytest.fixture
def expected_jwt():
  return generate_jwt({"username": "testuser",
    "email": "test@email.com",
    "role_id": 1,})

@pytest.fixture
def mocked_user(mocker, expected_password, expected_hashed_password):
  expected_hashed_password = encrypt_password(expected_password)
  return mocker.AsyncMock(return_value=UserInDB(**{
    "id": 1,
    "username": "testuser",
    "email": "test@email.com",
    "role_id": 1,
    "hashed_password": expected_hashed_password
  }))

def test_login_success(mocker, mocked_user, expected_password, monkeypatch): 
  monkeypatch.setenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
  monkeypatch.setenv("SECRET_KEY", "testSecret")

  mocker.patch('app.models.user.UserModel.get_by_username', mocked_user)
  
  response = client.post(
    "/api/v1/login", 
    data={"username": "testuser", "password": expected_password},
    headers={"Content-Type": "application/x-www-form-urlencoded"}
  )

  assert response.status_code == 200
  assert "access_token" in response.json()  
  assert response.json()["token_type"] == "bearer"


def test_login_invalid_credentials(mocker, mocked_user):
  mocker.patch('app.models.user.UserModel.exists', mocked_user)

  response = client.post(
    "/api/v1/login",
    data={"username": "wronguser", "password": "wrongpassword"},
    headers={"Content-Type": "application/x-www-form-urlencoded"}
  )
  
  assert response.status_code == 401
  assert response.json() == {"detail": "Invalid username or password"}


def test_login_missing_username():
  response = client.post("/api/v1/login", json={"password": "testpassword"})
  assert response.status_code == 422


def test_login_missing_password():
  response = client.post("/api/v1/login", json={"username": "testuser"})
  assert response.status_code == 422