from pydantic import BaseModel
from typing import Optional
from enum import Enum

class SupportCaseType(str, Enum):
  SUPPORT = "Support"
  BUSINESS = "Business Requirement"

class SupportCaseStatus(str, Enum):
  OPEN = "Open"
  CLOSED = "Closed"
  IN_PROGRESS = "In Progress"

class SupportCase(BaseModel):
  title: str
  details: str
  user_reporter_id: int
  type: str
  status: SupportCaseStatus = SupportCaseStatus.OPEN

class SupportCaseInDB(SupportCase):
  id: int
  user_support_id: Optional[int] = None
  