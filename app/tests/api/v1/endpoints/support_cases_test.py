import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.use_cases.auth import generate_jwt
from unittest.mock import AsyncMock

client = TestClient(app)

@pytest.fixture
def valid_token():
  return generate_jwt({"username": "testuser", "email": "testuser@example.com", "role_id": 1, "id": 1})

@pytest.fixture
def support_case_data():
  return {
    "title": "Test Support Case",
    "details": "Details of the support case",
    "type": "Support"
  }

def test_create_support_case_success(mocker, valid_token, support_case_data):
  mocker.patch("app.models.support_case.SupportCaseModel.create", AsyncMock(return_value={"id": 1}))

  response = client.post(
    f"/api/v1/support-cases?token={valid_token}",
    json=support_case_data
  )

  assert response.status_code == 201
  assert response.json() == {"message": "Case created"}


def test_create_support_case_missing_token(support_case_data):
  response = client.post(f"/api/v1/support-cases?token=", json=support_case_data)
  assert response.status_code == 401
  assert response.json() == {"detail": "Invalid authentication credentials"}


def test_create_support_case_missing_title(valid_token):
  response = client.post(
    f"/api/v1/support-cases?token={valid_token}",
    json={"details": "Details of the support case"}
  )
  assert response.status_code == 422


def test_create_support_case_missing_details(valid_token):
  response = client.post(
    f"/api/v1/support-cases?token={valid_token}",
    json={"title": "Test Support Case"}
  )
  assert response.status_code == 422