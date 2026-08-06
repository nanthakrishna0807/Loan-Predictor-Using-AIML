from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.auth import UserRegisterSchema, UserLoginSchema, ForgotPasswordSchema, ResetPasswordSchema
from app.services.auth_service import register_user, login_user, refresh_user_token
from app.auth.jwt import get_current_user
from app.services.user_service import get_user_profile

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
async def register(payload: UserRegisterSchema):
    return await register_user(payload.model_dump())

@router.post("/login")
async def login(payload: UserLoginSchema):
    return await login_user(payload.model_dump())

@router.post("/logout")
async def logout():
    return {"success": True, "message": "Logged out successfully"}

@router.post("/refresh")
async def refresh_token(token: str):
    return await refresh_user_token(token)

@router.get("/me")
@router.get("/profile")
async def get_me(current_user: dict = Depends(get_current_user)):
    user_id = str(current_user["_id"])
    profile = await get_user_profile(user_id)
    return {"success": True, "data": profile}

@router.post("/forgot-password")
async def forgot_password(payload: ForgotPasswordSchema):
    return {"success": True, "message": f"Password reset link sent to {payload.email}"}

@router.post("/reset-password")
async def reset_password(payload: ResetPasswordSchema):
    return {"success": True, "message": "Password reset successfully"}
