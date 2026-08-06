from datetime import datetime
from fastapi import APIRouter
from app.config import settings
from app.database.connection import db_manager
from app.ml.predictor import ml_predictor

router = APIRouter(tags=["Health"])

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "database_connected": db_manager.db is not None,
        "ml_model_loaded": ml_predictor.model_loaded,
        "ml_model_name": ml_predictor.best_model_name,
        "timestamp": datetime.utcnow().isoformat()
    }
