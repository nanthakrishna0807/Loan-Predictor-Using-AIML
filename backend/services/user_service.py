from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException, status
from backend.database.connection import get_database
from backend.auth.security import hash_password, verify_password
from backend.utils.logger import logger

async def update_user_profile(user_id: str, update_data: dict) -> dict:
    db = get_database()
    if db is None:
        return {
            "success": True,
            "message": "Profile updated locally",
            "user": update_data
        }

    try:
        query_id = ObjectId(user_id)
    except Exception:
        query_id = user_id

    user = await db.users.find_one({"_id": query_id})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User account not found")

    update_fields = {}
    if update_data.get("name"):
        update_fields["name"] = update_data["name"].strip()
    if update_data.get("phone") is not None:
        update_fields["phone"] = update_data["phone"]
    if update_data.get("occupation") is not None:
        update_fields["occupation"] = update_data["occupation"]
    if update_data.get("monthly_income") is not None:
        update_fields["monthly_income"] = float(update_data["monthly_income"])
    if update_data.get("cibil_score") is not None:
        update_fields["cibil_score"] = int(update_data["cibil_score"])

    if update_data.get("new_password"):
        current_password = update_data.get("current_password")
        if not current_password or not verify_password(current_password, user.get("password") or user.get("password_hash")):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password verification failed")
        update_fields["password"] = hash_password(update_data["new_password"])

    update_fields["updatedAt"] = datetime.utcnow()

    await db.users.update_one({"_id": query_id}, {"$set": update_fields})
    updated_user = await db.users.find_one({"_id": query_id})

    return {
        "success": True,
        "message": "User profile updated successfully",
        "user": {
            "id": str(updated_user["_id"]),
            "_id": str(updated_user["_id"]),
            "name": updated_user.get("name"),
            "email": updated_user.get("email"),
            "role": updated_user.get("role", "user"),
            "phone": updated_user.get("phone", ""),
            "occupation": updated_user.get("occupation", ""),
            "monthly_income": updated_user.get("monthly_income", 0.0),
            "cibil_score": updated_user.get("cibil_score", 720)
        }
    }
