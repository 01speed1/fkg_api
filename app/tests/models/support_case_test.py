import pytest
from unittest.mock import AsyncMock
from app.models.support_case import SupportCaseModel
from app.schemas.support_case import SupportCase, SupportCaseInDB, SupportCaseType


@pytest.fixture
def support_case_data():
	return SupportCase(
		title="Test Support Case",
		details="Details of the support case",
		user_reporter_id=1,
    type=SupportCaseType.SUPPORT
	)

@pytest.fixture
def created_support_case():
	return SupportCaseInDB(
		id=1,
		title="Test Support Case",
		details="Details of the support case",
		user_reporter_id=1,
    type=SupportCaseType.SUPPORT
	)

@pytest.mark.asyncio
async def test_create_support_case(mocker, support_case_data, created_support_case):
	mocker.patch("app.db.connections.postgres.insert", AsyncMock(return_value={"id": 1, **support_case_data.model_dump()}))

	model = SupportCaseModel()
	result = await model.create(support_case_data)

	assert result == created_support_case

@pytest.mark.asyncio
async def test_get_all_support_cases(mocker, created_support_case):
	mocker.patch("app.db.connections.postgres.fetch", AsyncMock(return_value=[created_support_case.model_dump()]))

	model = SupportCaseModel()
	result = await model.get_all()

	assert result == [created_support_case]