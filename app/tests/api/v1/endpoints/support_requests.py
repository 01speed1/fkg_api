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
def support_report_data():
	return {
		"title": "Test Support Case",
		"details": "Details of the support case"
	}

def test_create_support_report_success(mocker, valid_token, support_report_data):
	mocker.patch("app.models.support_report.SupportReportModel.create", AsyncMock(return_value={"id": 1}))

	response = client.post(
		"/api/v1/support_reports",
		json=support_report_data,
		headers={"Authorization": f"Bearer {valid_token}"}
	)

	assert response.status_code == 201
	assert response.json() == {"message": "Case created"}

def test_create_support_report_missing_token(support_report_data):
	response = client.post("/api/v1/support_reports", json=support_report_data)
	assert response.status_code == 401
	assert response.json() == {"detail": "Not authenticated"}

def test_create_support_report_missing_title(valid_token):
	response = client.post(
		"/api/v1/support_reports",
		json={"details": "Details of the support case"},
		headers={"Authorization": f"Bearer {valid_token}"}
	)
	assert response.status_code == 422

def test_create_support_report_missing_details(valid_token):
	response = client.post(
		"/api/v1/support_reports",
		json={"title": "Test Support Case"},
		headers={"Authorization": f"Bearer {valid_token}"}
	)
	assert response.status_code == 422