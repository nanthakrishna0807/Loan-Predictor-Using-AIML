from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class PredictionModel(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    user_id: Optional[str] = None
    input_data: Dict[str, Any]
    result: Dict[str, Any]
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
