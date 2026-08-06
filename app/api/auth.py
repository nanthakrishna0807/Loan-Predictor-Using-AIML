from fastapi import APIRouter, Depends
from app.schemas.auth import RegisterSchema, LoginSchema
from app.services.auth_service import register_user, login_user
from app.auth.jwt import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
async def register(payload: RegisterSchema):
    return await register_user(payload.model_dump())

@router.post("/login")
async def login(payload: LoginSchema):
    return await login_user(payload.model_dump())

@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    return {
        "success": True,
        "user": {
            "id": current_user.get("_id"),
            "_id": current_user.get("_id"),
            "name": current_user.get("name"),
            "email": current_user.get("email"),
            "role": current_user.get("role", "user"),
            "phone": current_user.get("phone", ""),
            "occupation": current_user.get("occupation", ""),
            "monthly_income": current_user.get("monthly_income", 0.0),
            "cibil_score": current_user.get("cibil_score", 720)
        }
    }
