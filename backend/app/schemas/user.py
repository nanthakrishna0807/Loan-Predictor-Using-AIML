from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserProfileUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=2)
    phone: Optional[str] = None
    occupation: Optional[str] = None

class UserResponseSchema(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str
    phone: Optional[str] = None
    occupation: Optional[str] = None
    createdAt: Optional[str] = None
