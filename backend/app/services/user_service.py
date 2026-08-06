from datetime import datetime
from fastapi import HTTPException
from bson import ObjectId
from app.database.connection import get_database

async def get_user_profile(user_id: str) -> dict:
    db = get_database()
    try:
        user = await db.users.find_one({"_id": ObjectId(user_id)})
    except Exception:
        user = await db.users.find_one({"_id": user_id})

    if not user:
        raise HTTPException(status_code=404, detail="User profile not found")

    user_id_str = str(user["_id"])
    return {
        "id": user_id_str,
        "_id": user_id_str,
        "name": user.get("name"),
        "email": user.get("email"),
        "role": user.get("role", "user"),
        "phone": user.get("phone", ""),
        "occupation": user.get("occupation", ""),
        "createdAt": user.get("createdAt").isoformat() if isinstance(user.get("createdAt"), datetime) else str(user.get("createdAt", ""))
    }

async def update_user_profile(user_id: str, update_data: dict) -> dict:
    db = get_database()
    update_fields = {k: v for k, v in update_data.items() if v is not None}
    update_fields["updatedAt"] = datetime.utcnow()

    try:
        query_id = ObjectId(user_id)
    except Exception:
        query_id = user_id

    result = await db.users.update_one({"_id": query_id}, {"$set": update_fields})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return await get_user_profile(user_id)
