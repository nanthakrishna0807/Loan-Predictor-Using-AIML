from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class UserModel(BaseModel):
    id: Optional[str] = None
    name: str
    email: EmailStr
    password_hash: str
    role: str = "user"
    phone: Optional[str] = None
    occupation: Optional[str] = None
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
