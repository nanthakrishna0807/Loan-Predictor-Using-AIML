from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException, status
from backend.database.connection import get_database
from backend.auth.security import hash_password, verify_password
from backend.auth.jwt import create_access_token
from backend.utils.logger import logger

MEMORY_USERS = {}

async def ensure_seed_users():
    """Seeds default demo admin and user accounts into MongoDB Atlas or memory if not already present."""
    db = get_database()
    demo_accounts = [
        {
            "name": "System Administrator",
            "email": "admin@loanpredictor.com",
            "password": hash_password("admin123"),
            "role": "admin",
            "phone": "+91 9999999999",
            "occupation": "Administrator",
            "monthly_income": 150000.0,
            "cibil_score": 850
        },
        {
            "name": "John Demo User",
            "email": "user@example.com",
            "password": hash_password("user123"),
            "role": "user",
            "phone": "+91 9876543210",
            "occupation": "Salaried",
            "monthly_income": 75000.0,
            "cibil_score": 750
        }
    ]

    for acc in demo_accounts:
        email = acc["email"]
        if db is not None:
            try:
                existing = await db.users.find_one({"email": email})
                if not existing:
                    acc_copy = dict(acc)
                    acc_copy["createdAt"] = datetime.utcnow()
                    acc_copy["updatedAt"] = datetime.utcnow()
                    await db.users.insert_one(acc_copy)
                    logger.info(f"Seeded demo account to MongoDB: {email}")
            except Exception as ex:
                logger.warning(f"Error seeding {email} to MongoDB: {ex}")
        else:
            if email not in MEMORY_USERS:
                acc_copy = dict(acc)
                acc_copy["id"] = f"seed_{email}"
                acc_copy["_id"] = f"seed_{email}"
                MEMORY_USERS[email] = acc_copy
                logger.info(f"Seeded demo account to Memory: {email}")

async def register_user(user_data: dict) -> dict:
    await ensure_seed_users()
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
    await ensure_seed_users()
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

async def refresh_user_token(token: str) -> dict:
    from jose import JWTError, jwt
    from backend.config import settings

    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get("sub") or payload.get("id")
        email = payload.get("email")
        role = payload.get("role", "user")
        if not user_id or not email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

        new_token = create_access_token({"sub": user_id, "email": email, "role": role})
        return {
            "success": True,
            "message": "Token refreshed successfully",
            "access_token": new_token,
            "token": new_token,
            "token_type": "bearer"
        }
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")


