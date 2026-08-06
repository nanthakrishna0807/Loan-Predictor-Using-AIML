from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException, status
from app.database.connection import get_database
from app.auth.security import hash_password, verify_password
from app.auth.jwt import create_access_token
from app.utils.logger import logger

# Fallback in-memory store if DB unavailable
MEMORY_USERS = {}

async def register_user(user_data: dict) -> dict:
    db = get_database()
    email = user_data["email"].lower().strip()
    
    if db is not None:
        existing = await db.users.find_one({"email": email})
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Account with this email address already exists"
            )

        hashed_pw = hash_password(user_data["password"])
        new_user = {
            "name": user_data["name"].strip(),
            "email": email,
            "password": hashed_pw,
            "role": user_data.get("role", "user"),
            "phone": user_data.get("phone", ""),
            "occupation": user_data.get("occupation", ""),
            "monthly_income": user_data.get("monthly_income", 0.0),
            "cibil_score": 720,
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        }
        res = await db.users.insert_one(new_user)
        user_id = str(res.inserted_id)
        user_obj = {
            "id": user_id,
            "_id": user_id,
            "name": new_user["name"],
            "email": new_user["email"],
            "role": new_user["role"],
            "phone": new_user["phone"],
            "occupation": new_user["occupation"],
            "monthly_income": new_user["monthly_income"],
            "cibil_score": new_user["cibil_score"]
        }
    else:
        if email in MEMORY_USERS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Account with this email address already exists"
            )
        hashed_pw = hash_password(user_data["password"])
        user_id = f"mem_{len(MEMORY_USERS) + 1}"
        user_obj = {
            "id": user_id,
            "_id": user_id,
            "name": user_data["name"].strip(),
            "email": email,
            "password": hashed_pw,
            "role": user_data.get("role", "user"),
            "phone": user_data.get("phone", ""),
            "occupation": user_data.get("occupation", ""),
            "monthly_income": user_data.get("monthly_income", 0.0),
            "cibil_score": 720
        }
        MEMORY_USERS[email] = user_obj

    token = create_access_token({"sub": user_id, "email": email, "role": user_obj["role"]})
    logger.info(f"User registered successfully: {email}")

    return {
        "success": True,
        "message": "User account created successfully",
        "token": token,
        "access_token": token,
        "token_type": "bearer",
        "user": user_obj
    }

async def login_user(login_data: dict) -> dict:
    db = get_database()
    email = login_data["email"].lower().strip()
    password = login_data["password"]

    user = None
    if db is not None:
        user = await db.users.find_one({"email": email})
    else:
        user = MEMORY_USERS.get(email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    hashed_pw = user.get("password") or user.get("password_hash")
    if not hashed_pw or not verify_password(password, hashed_pw):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    user_id = str(user.get("_id") or user.get("id"))
    token = create_access_token({"sub": user_id, "email": email, "role": user.get("role", "user")})

    user_response = {
        "id": user_id,
        "_id": user_id,
        "name": user.get("name"),
        "email": user.get("email"),
        "role": user.get("role", "user"),
        "phone": user.get("phone", ""),
        "occupation": user.get("occupation", ""),
        "monthly_income": user.get("monthly_income", 0.0),
        "cibil_score": user.get("cibil_score", 720)
    }

    logger.info(f"User logged in successfully: {email}")

    return {
        "success": True,
        "message": "Login successful",
        "token": token,
        "access_token": token,
        "token_type": "bearer",
        "user": user_response
    }
