from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel

class ConnectionTestModel(BaseModel):
    id: Optional[str] = None
    test_message: str = "MongoDB Atlas Verification"
    status: str = "SUCCESS"
    environment: str = "development"
    verified_at: datetime = datetime.utcnow()
    metadata: dict[str, Any] = {}
