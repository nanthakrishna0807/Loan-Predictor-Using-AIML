from typing import Optional
from pydantic import BaseModel, EmailStr

class UserProfileUpdateSchema(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    occupation: Optional[str] = None
    monthly_income: Optional[float] = None
    cibil_score: Optional[int] = None
    current_password: Optional[str] = None
    new_password: Optional[str] = None

class UserResponseSchema(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str
    phone: Optional[str] = ""
    occupation: Optional[str] = ""
    monthly_income: Optional[float] = 0.0
    cibil_score: Optional[int] = 700
