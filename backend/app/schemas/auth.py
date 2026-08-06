from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserRegisterSchema(BaseModel):
    name: str = Field(..., min_length=2, description="Full Name")
    email: EmailStr = Field(..., description="Valid Email Address")
    password: str = Field(..., min_length=6, description="Password min 6 characters")
    role: Optional[str] = Field("user", description="User role (user or admin)")

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class TokenResponseSchema(BaseModel):
    token: str
    refreshToken: Optional[str] = None
    user: dict

class ForgotPasswordSchema(BaseModel):
    email: EmailStr

class ResetPasswordSchema(BaseModel):
    password: str = Field(..., min_length=6)
