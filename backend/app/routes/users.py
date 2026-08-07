from fastapi import APIRouter, Depends
from app.schemas.user import UserProfileUpdateSchema
from app.auth.jwt import get_current_user
from app.services.user_service import get_user_profile, update_user_profile
from app.services.prediction_service import get_user_predictions

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/profile")
async def get_profile(current_user: dict = Depends(get_current_user)):
    user_id = str(current_user["_id"])
    profile = await get_user_profile(user_id)
    return {"success": True, "data": profile, **profile}

@router.put("/profile")
async def update_profile(
    payload: UserProfileUpdateSchema,
    current_user: dict = Depends(get_current_user)
):
    user_id = str(current_user["_id"])
    updated_profile = await update_user_profile(user_id, payload.model_dump())
    return {"success": True, "message": "Profile updated successfully", "data": updated_profile}

@router.get("/history")
async def get_history(current_user: dict = Depends(get_current_user)):
    user_id = str(current_user["_id"])
    return await get_user_predictions(user_id)
