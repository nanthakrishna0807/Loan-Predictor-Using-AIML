from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr

class UserModel(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    email: EmailStr
    password_hash: str
    role: str = "user"  # "user" or "admin"
    phone: Optional[str] = ""
    occupation: Optional[str] = ""
    monthly_income: Optional[float] = 0.0
    cibil_score: Optional[int] = 700
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
