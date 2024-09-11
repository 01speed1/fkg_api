from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.schemas.support_case import SupportCase, SupportCaseInDB, SupportCaseStatus
from app.models.support_case import SupportCaseModel
from app.api.v1.endpoints.login import get_current_user

router = APIRouter()


class SupportReportCreate(BaseModel):
  title: str
  details: str
  type: str


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_support_case(
    report: SupportReportCreate,
    current_user: dict = Depends(get_current_user)
):
  
    user_reporter_id = current_user.get("id")

    support_case_model = SupportCaseModel()

    await support_case_model.create(SupportCase(
      details=report.details,
      title=report.title,
      type=report.type,
      user_reporter_id=user_reporter_id,  
      status=SupportCaseStatus.OPEN 
    ))

    return {"message": "Case created"}


@router.get("/", response_model=list[SupportCaseInDB])
async def get_support_cases(
  limit: int = 10,
  offset: int = 0,
  current_user: dict = Depends(get_current_user)
):
  user_reporter_id = current_user.get("id")

  support_case_model = SupportCaseModel()
  cases = await support_case_model.get_all(limit, offset)
  return cases


@router.get("/{case_id}", response_model=SupportCaseInDB)
async def get_support_case_by_id(
    case_id: int,
    current_user: dict = Depends(get_current_user)
):
    user_reporter_id = current_user.get("id")

    support_case_model = SupportCaseModel()
    support_case = await support_case_model.get_by_id(case_id)
    if not support_case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Support case not found",
        )
    return support_case
  
  
class UpdateStatusRequest(BaseModel):
    status: str

@router.put("/{id}/status", response_model=SupportCaseInDB)
async def update_support_case_status(
    id: int,
    request: UpdateStatusRequest,
    current_user: dict = Depends(get_current_user)
):
    if request.status not in list(SupportCaseStatus):
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid status value",
      )

    support_case_model = SupportCaseModel()
    support_case = await support_case_model.get_by_id(id)
    
    if not support_case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Support case not found",
        )

    ajam = await support_case_model.update_one(support_case.id, request.status)
  
    return ajam