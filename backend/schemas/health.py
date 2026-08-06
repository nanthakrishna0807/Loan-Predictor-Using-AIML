from pydantic import BaseModel

class HealthResponseSchema(BaseModel):
    status: str
    version: str
    environment: str
    database_connected: bool
    ml_model_loaded: bool
    timestamp: str
