"""
POST /admin/login -- matches exactly what the frontend's adminLogin() in
lib/api.js already calls:

    POST /admin/login  { username, password }  ->  { token: "..." }

Mount this router in your main FastAPI app, e.g.:

    from app.routers.admin_auth import router as admin_auth_router
    app.include_router(admin_auth_router)
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from auth.security import create_admin_token, verify_admin_credentials

router = APIRouter()


class AdminLoginRequest(BaseModel):
    username: str
    password: str


class AdminLoginResponse(BaseModel):
    token: str


@router.post("/admin/login", response_model=AdminLoginResponse)
def admin_login(payload: AdminLoginRequest) -> AdminLoginResponse:
    if not verify_admin_credentials(payload.username, payload.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    return AdminLoginResponse(token=create_admin_token())
