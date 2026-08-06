from fastapi import APIRouter, Depends
from app.schemas.user import UserProfileUpdateSchema
from app.services.user_service import update_user_profile
from app.auth.jwt import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/profile")
async def get_profile(current_user: dict = Depends(get_current_user)):
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

@router.put("/profile")
async def update_profile(payload: UserProfileUpdateSchema, current_user: dict = Depends(get_current_user)):
    user_id = str(current_user["_id"])
    return await update_user_profile(user_id, payload.model_dump(exclude_unset=True))
