from datetime import datetime
from fastapi import APIRouter
from backend.config import settings
from backend.database.connection import db_manager
from ml.predictor import ml_predictor

router = APIRouter(tags=["Health Check"])

@router.get("/health")
async def health_check():
    """Overall system health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "database_connected": db_manager.db is not None,
        "ml_model_loaded": ml_predictor.model_loaded,
        "ml_model_name": ml_predictor.best_model_name,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/health/database")
async def database_health():
    """MongoDB Atlas database connection health check."""
    if db_manager.db is not None:
        try:
            collections = await db_manager.db.list_collection_names()
            return {
                "status": "connected",
                "database_name": settings.DATABASE_NAME,
                "collections_count": len(collections),
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Database query failed: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
    return {
        "status": "disconnected",
        "message": "Database not connected or in fallback mode",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/health/ml")
async def ml_health():
    """Machine Learning model engine health check."""
    return {
        "status": "loaded" if ml_predictor.model_loaded else "fallback_mode",
        "algorithm": ml_predictor.best_model_name,
        "accuracy": f"{ml_predictor.accuracy}%",
        "model_file": "ml/model.pkl",
        "scaler_file": "ml/scaler.pkl",
        "timestamp": datetime.utcnow().isoformat()
    }
