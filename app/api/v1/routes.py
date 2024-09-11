# app/api/v1/routes.py
from fastapi import APIRouter
from app.api.v1.endpoints.users import router as user_router
from app.api.v1.endpoints.signup import router as signup_router
from app.api.v1.endpoints.login import router as login_router
from app.api.v1.endpoints.support_cases import router as support_cases_router

router = APIRouter()
router.include_router(user_router, prefix="/users")
router.include_router(signup_router, prefix="/signup")
router.include_router(login_router, prefix="/login")
router.include_router(support_cases_router, prefix="/support-cases")