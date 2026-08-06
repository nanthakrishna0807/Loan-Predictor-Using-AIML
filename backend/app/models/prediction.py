from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel

class PredictionModel(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    input_data: dict[str, Any]
    result: dict[str, Any]
    created_at: datetime = datetime.utcnow()
