from pydantic import BaseModel
from typing import Optional

class ServerHealthSchema(BaseModel):
    success: bool = True
    server_status: str = "Online"
    python_version: str
    environment: str
    current_time: str
    uptime: str
    uptime_seconds: float

class DatabaseHealthSchema(BaseModel):
    success: bool = True
    mongodb_status: str
    database_name: str
    host: str
    collection_count: int
    connection_time: Optional[str] = None
    ready_state: int = 1

class MLHealthSchema(BaseModel):
    success: bool = True
    model_loaded: bool
    algorithm_name: str
    accuracy: float
    features_count: int
    model_version: str = "1.0.0"
