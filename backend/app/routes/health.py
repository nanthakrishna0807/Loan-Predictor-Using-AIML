import sys
import time
from datetime import datetime
from fastapi import APIRouter
from app.config.settings import settings
from app.database.connection import db_manager
from app.ml.predictor import ml_predictor

router = APIRouter(prefix="/health", tags=["Health Checks"])
start_time = time.time()

@router.get("")
@router.get("/")
async def get_server_health():
    uptime_sec = round(time.time() - start_time, 2)
    return {
        "success": True,
        "server_status": "Online",
        "python_version": sys.version.split()[0],
        "environment": settings.ENVIRONMENT,
        "current_time": datetime.utcnow().isoformat() + "Z",
        "uptime": f"{int(uptime_sec)}s",
        "uptime_seconds": uptime_sec,
        "database_connected": db_manager.db is not None,
        "ml_model_loaded": ml_predictor.model_loaded
    }

@router.get("/database")
async def get_database_health():
    is_connected = db_manager.db is not None
    db_name = settings.DB_NAME if is_connected else "N/A"
    host = "Atlas Cluster"
    collection_count = 0

    if is_connected:
        try:
            collections = await db_manager.db.list_collection_names()
            collection_count = len(collections)
        except Exception:
            pass

    return {
        "success": is_connected,
        "mongodb_status": "Connected" if is_connected else "Disconnected",
        "database_name": db_name,
        "database": db_name,
        "status": "Connected" if is_connected else "Disconnected",
        "host": host,
        "collection_count": collection_count,
        "collections": collection_count,
        "connection_time": db_manager.connected_since.isoformat() + "Z" if db_manager.connected_since else None,
        "ready_state": 1 if is_connected else 0,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@router.get("/ml")
async def get_ml_health():
    return {
        "success": True,
        "model_loaded": ml_predictor.model_loaded,
        "algorithm_name": ml_predictor.best_model_name,
        "accuracy": ml_predictor.accuracy,
        "features_count": ml_predictor.feature_count,
        "model_version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
