from datetime import datetime
from fastapi import HTTPException
from bson import ObjectId
from app.database.connection import get_database
from app.auth.security import hash_password

async def get_user_profile(user_id: str) -> dict:
    db = get_database()
    if db is None:
        raise HTTPException(status_code=503, detail="Database connection unavailable")

    try:
        user = await db.users.find_one({"_id": ObjectId(user_id)})
    except Exception:
        user = await db.users.find_one({"_id": user_id})

    if not user:
        raise HTTPException(status_code=404, detail="User profile not found")

    user_id_str = str(user["_id"])

    # Count predictions for this user from predictions collection
    prediction_count = 0
    try:
        prediction_count = await db.predictions.count_documents({"userId": user_id_str})
    except Exception:
        pass

    created_at = user.get("createdAt")
    joined_date = created_at.strftime("%Y-%m-%d") if isinstance(created_at, datetime) else str(created_at or "")[:10]

    return {
        "id": user_id_str,
        "_id": user_id_str,
        "name": user.get("name"),
        "email": user.get("email"),
        "role": user.get("role", "user"),
        "phone": user.get("phone", ""),
        "occupation": user.get("occupation", ""),
        "joined_date": joined_date,
        "createdAt": created_at.isoformat() if isinstance(created_at, datetime) else str(created_at or ""),
        "prediction_count": prediction_count
    }

async def update_user_profile(user_id: str, update_data: dict) -> dict:
    db = get_database()
    if db is None:
        raise HTTPException(status_code=503, detail="Database connection unavailable")

    update_fields = {k: v for k, v in update_data.items() if v is not None}
    if "password" in update_fields and update_fields["password"]:
        update_fields["password"] = hash_password(update_fields["password"])

    update_fields["updatedAt"] = datetime.utcnow()

    try:
        query_id = ObjectId(user_id)
    except Exception:
        query_id = user_id

    result = await db.users.update_one({"_id": query_id}, {"$set": update_fields})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return await get_user_profile(user_id)
