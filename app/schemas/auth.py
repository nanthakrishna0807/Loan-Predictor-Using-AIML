from typing import Optional
from pydantic import BaseModel, EmailStr

class RegisterSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Optional[str] = "user"
    phone: Optional[str] = ""
    occupation: Optional[str] = ""
    monthly_income: Optional[float] = 0.0

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict
