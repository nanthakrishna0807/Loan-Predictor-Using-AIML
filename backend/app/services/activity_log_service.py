"""
Activity Log Service — writes audit trail entries to MongoDB activity_logs collection.
"""
from datetime import datetime
from app.database.connection import get_database
from app.utils.logger import logger


async def log_activity(
    action: str,
    actor_id: str = "anonymous",
    actor_name: str = "System",
    metadata: dict = None,
    loan_type: str = None,
) -> None:
    """
    Inserts one activity log record into the activity_logs collection.
    Fails silently so it never breaks the calling endpoint.
    """
    doc = {
        "action": action,
        "actorId": actor_id,
        "actorName": actor_name,
        "loanType": loan_type,
        "metadata": metadata or {},
        "timestamp": datetime.utcnow(),
    }
    try:
        db = get_database()
        if db is not None:
            await db.activity_logs.insert_one(doc)
    except Exception as ex:
        logger.warning(f"Activity log write failed: {ex}")


async def get_recent_activity(limit: int = 50) -> list:
    """Return the most recent activity log entries."""
    db = get_database()
    if db is None:
        return []
    try:
        cursor = db.activity_logs.find().sort("timestamp", -1).limit(limit)
        results = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            doc["timestamp"] = doc["timestamp"].isoformat() if isinstance(doc.get("timestamp"), datetime) else str(doc.get("timestamp", ""))
            results.append(doc)
        return results
    except Exception as ex:
        logger.warning(f"Activity log read failed: {ex}")
        return []
