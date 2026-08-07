from datetime import datetime
from fastapi import HTTPException, status
from bson import ObjectId
from app.database.connection import get_database
from app.auth.security import hash_password, verify_password
from app.auth.jwt import create_access_token, create_refresh_token, decode_token
from app.utils.logger import logger

async def register_user(user_data: dict) -> dict:
    db = get_database()
    if db is None:
        raise HTTPException(status_code=503, detail="Database connection unavailable")

    existing_user = await db.users.find_one({"email": user_data["email"].lower()})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    user_doc = {
        "name": user_data["name"],
        "email": user_data["email"].lower(),
        "password": hash_password(user_data["password"]),
        "role": user_data.get("role", "user"),
        "phone": user_data.get("phone", ""),
        "occupation": user_data.get("occupation", ""),
        "isActive": True,
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    }

    result = await db.users.insert_one(user_doc)
    user_id = str(result.inserted_id)
    user_doc["_id"] = user_id

    token = create_access_token({"id": user_id, "email": user_doc["email"], "role": user_doc["role"]})
    refresh_token = create_refresh_token({"id": user_id, "email": user_doc["email"]})

    logger.info(f"User registered successfully: {user_doc['email']}")

    user_obj = {
        "id": user_id,
        "_id": user_id,
        "name": user_doc["name"],
        "email": user_doc["email"],
        "role": user_doc["role"],
        "createdAt": user_doc["createdAt"].isoformat()
    }

    return {
        "success": True,
        "message": "Registration successful",
        "access_token": token,
        "token_type": "bearer",
        "token": token,
        "user": user_obj,
        "data": {
            "token": token,
            "access_token": token,
            "token_type": "bearer",
            "refreshToken": refresh_token,
            "user": user_obj
        }
    }

async def login_user(login_data: dict) -> dict:
    db = get_database()
    if db is None:
        raise HTTPException(status_code=503, detail="Database connection unavailable")

    user = await db.users.find_one({"email": login_data["email"].lower()})
    if not user or not verify_password(login_data["password"], user.get("password", "")):
        logger.warning(f"Failed login attempt for email: {login_data['email']}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    user_id = str(user["_id"])
    token = create_access_token({"id": user_id, "email": user["email"], "role": user.get("role", "user")})
    refresh_token = create_refresh_token({"id": user_id, "email": user["email"]})

    # Log login activity
    try:
        from app.services.activity_log_service import log_activity
        await log_activity(
            action="User Login",
            actor_id=user_id,
            actor_name=user.get("name", "User"),
            metadata={"email": user["email"], "role": user.get("role", "user")}
        )
    except Exception:
        pass

    logger.info(f"User logged in successfully: {user['email']}")

    user_obj = {
        "id": user_id,
        "_id": user_id,
        "name": user.get("name"),
        "email": user.get("email"),
        "role": user.get("role", "user")
    }

    return {
        "success": True,
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer",
        "token": token,
        "user": user_obj,
        "data": {
            "token": token,
            "access_token": token,
            "token_type": "bearer",
            "refreshToken": refresh_token,
            "user": user_obj
        }
    }

async def refresh_user_token(refresh_token_str: str) -> dict:
    payload = decode_token(refresh_token_str)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=400, detail="Invalid token type")

    user_id = payload.get("id")
    db = get_database()
    try:
        user = await db.users.find_one({"_id": ObjectId(user_id)})
    except Exception:
        user = await db.users.find_one({"_id": user_id})

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_token = create_access_token({"id": str(user["_id"]), "email": user["email"], "role": user.get("role", "user")})
    user_obj = {
        "id": str(user["_id"]),
        "_id": str(user["_id"]),
        "name": user.get("name"),
        "email": user.get("email"),
        "role": user.get("role", "user")
    }
    return {
        "success": True,
        "access_token": new_token,
        "token_type": "bearer",
        "token": new_token,
        "user": user_obj,
        "data": {
            "token": new_token,
            "access_token": new_token,
            "token_type": "bearer",
            "user": user_obj
        }
    }
