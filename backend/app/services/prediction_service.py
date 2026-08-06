from datetime import datetime
from fastapi import HTTPException
from bson import ObjectId
from app.database.connection import get_database
from app.ml.predictor import ml_predictor
from app.utils.logger import logger

async def create_prediction(input_data: dict, user_id: str = None) -> dict:
    """
    Executes prediction engine and persists request/result in predictions collection.
    """
    prediction_result = ml_predictor.predict(input_data)

    db = get_database()
    doc = {
        "userId": user_id,
        "inputData": input_data,
        "result": prediction_result,
        "createdAt": datetime.utcnow()
    }

    if db is not None:
        try:
            res = await db.predictions.insert_one(doc)
            doc["_id"] = str(res.inserted_id)
            doc["id"] = str(res.inserted_id)
            logger.info(f"Saved prediction record {res.inserted_id} for user {user_id}")
        except Exception as e:
            logger.error(f"Error persisting prediction to MongoDB: {e}")
            doc["_id"] = "temp_id"
            doc["id"] = "temp_id"
    else:
        doc["_id"] = "temp_id"
        doc["id"] = "temp_id"

    # Formatting payload to match React frontend PredictionResult.jsx expectation
    return {
        "success": True,
        "message": "Loan prediction generated successfully",
        "data": {
            "id": doc["id"],
            "_id": doc["_id"],
            "prediction": prediction_result,
            "result": prediction_result,
            "inputData": input_data,
            "createdAt": doc["createdAt"].isoformat() if isinstance(doc["createdAt"], datetime) else str(doc["createdAt"])
        }
    }

async def get_user_predictions(user_id: str) -> dict:
    db = get_database()
    if db is None:
        return {"success": True, "count": 0, "data": []}

    cursor = db.predictions.find({"userId": user_id}).sort("createdAt", -1).limit(50)
    records = []
    async for doc in cursor:
        doc_id = str(doc["_id"])
        records.append({
            "id": doc_id,
            "_id": doc_id,
            "userId": doc.get("userId"),
            "inputData": doc.get("inputData", {}),
            "prediction": doc.get("result", {}),
            "result": doc.get("result", {}),
            "createdAt": doc.get("createdAt").isoformat() if isinstance(doc.get("createdAt"), datetime) else str(doc.get("createdAt", ""))
        })

    return {
        "success": True,
        "count": len(records),
        "data": records
    }

async def get_prediction_by_id(prediction_id: str) -> dict:
    db = get_database()
    if db is None:
        raise HTTPException(status_code=503, detail="Database connection unavailable")

    try:
        query_id = ObjectId(prediction_id)
    except Exception:
        query_id = prediction_id

    doc = await db.predictions.find_one({"_id": query_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Prediction record not found")

    doc_id = str(doc["_id"])
    return {
        "success": True,
        "data": {
            "id": doc_id,
            "_id": doc_id,
            "userId": doc.get("userId"),
            "inputData": doc.get("inputData", {}),
            "prediction": doc.get("result", {}),
            "result": doc.get("result", {}),
            "createdAt": doc.get("createdAt").isoformat() if isinstance(doc.get("createdAt"), datetime) else str(doc.get("createdAt", ""))
        }
    }

async def delete_prediction_by_id(prediction_id: str, user_id: str = None) -> dict:
    db = get_database()
    if db is None:
        raise HTTPException(status_code=503, detail="Database connection unavailable")

    try:
        query_id = ObjectId(prediction_id)
    except Exception:
        query_id = prediction_id

    filter_q = {"_id": query_id}
    if user_id:
        filter_q["userId"] = user_id

    result = await db.predictions.delete_one(filter_q)
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Prediction record not found or unauthorized")

    return {
        "success": True,
        "message": "Prediction record deleted successfully"
    }
