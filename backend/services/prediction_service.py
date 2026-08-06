from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException, status
from backend.database.connection import get_database
from ml.predictor import ml_predictor
from backend.utils.logger import logger

MEMORY_PREDICTIONS = []

async def create_prediction(input_data: dict, user_id: str = None) -> dict:
    result = ml_predictor.predict(input_data)
    
    db = get_database()
    prediction_doc = {
        "userId": user_id,
        "inputData": input_data,
        "result": result,
        "createdAt": datetime.utcnow()
    }

    if db is not None:
        try:
            res = await db.predictions.insert_one(prediction_doc)
            pred_id = str(res.inserted_id)
        except Exception as e:
            logger.error(f"Error inserting prediction to DB: {e}")
            pred_id = f"mem_{len(MEMORY_PREDICTIONS) + 1}"
            prediction_doc["_id"] = pred_id
            MEMORY_PREDICTIONS.append(prediction_doc)
    else:
        pred_id = f"mem_{len(MEMORY_PREDICTIONS) + 1}"
        prediction_doc["_id"] = pred_id
        MEMORY_PREDICTIONS.append(prediction_doc)

    logger.info(f"Loan prediction generated successfully [ID: {pred_id}, Approved: {result['approved']}]")

    return {
        "success": True,
        "message": "Loan prediction calculated successfully",
        "prediction_id": pred_id,
        "id": pred_id,
        "data": result,
        "result": result,
        "inputData": input_data,
        "createdAt": datetime.utcnow().isoformat()
    }

async def get_user_predictions(user_id: str) -> dict:
    db = get_database()
    history = []

    if db is not None:
        try:
            query = {"userId": user_id} if user_id else {}
            cursor = db.predictions.find(query).sort("createdAt", -1)
            async for doc in cursor:
                history.append({
                    "id": str(doc["_id"]),
                    "_id": str(doc["_id"]),
                    "userId": doc.get("userId"),
                    "inputData": doc.get("inputData", {}),
                    "result": doc.get("result", {}),
                    "createdAt": doc.get("createdAt").isoformat() if isinstance(doc.get("createdAt"), datetime) else str(doc.get("createdAt"))
                })
        except Exception as e:
            logger.error(f"Error reading prediction history from DB: {e}")
    else:
        for doc in MEMORY_PREDICTIONS:
            if not user_id or doc.get("userId") == user_id:
                history.append({
                    "id": str(doc.get("_id")),
                    "_id": str(doc.get("_id")),
                    "userId": doc.get("userId"),
                    "inputData": doc.get("inputData", {}),
                    "result": doc.get("result", {}),
                    "createdAt": str(doc.get("createdAt"))
                })

    return {
        "success": True,
        "count": len(history),
        "data": history
    }

async def get_prediction_by_id(prediction_id: str) -> dict:
    db = get_database()
    if db is not None:
        try:
            try:
                query_id = ObjectId(prediction_id)
            except Exception:
                query_id = prediction_id
            
            doc = await db.predictions.find_one({"_id": query_id})
            if doc:
                return {
                    "success": True,
                    "data": {
                        "id": str(doc["_id"]),
                        "_id": str(doc["_id"]),
                        "userId": doc.get("userId"),
                        "inputData": doc.get("inputData", {}),
                        "result": doc.get("result", {}),
                        "createdAt": str(doc.get("createdAt"))
                    }
                }
        except Exception as e:
            logger.error(f"Error fetching prediction by ID: {e}")

    for doc in MEMORY_PREDICTIONS:
        if str(doc.get("_id")) == str(prediction_id):
            return {
                "success": True,
                "data": {
                    "id": str(doc.get("_id")),
                    "_id": str(doc.get("_id")),
                    "userId": doc.get("userId"),
                    "inputData": doc.get("inputData", {}),
                    "result": doc.get("result", {}),
                    "createdAt": str(doc.get("createdAt"))
                }
            }

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prediction record not found")

async def delete_prediction_by_id(prediction_id: str, user_id: str) -> dict:
    db = get_database()
    if db is not None:
        try:
            try:
                query_id = ObjectId(prediction_id)
            except Exception:
                query_id = prediction_id
            
            res = await db.predictions.delete_one({"_id": query_id, "userId": user_id})
            if res.deleted_count > 0:
                return {"success": True, "message": "Prediction record deleted"}
        except Exception as e:
            logger.error(f"Error deleting prediction record: {e}")

    global MEMORY_PREDICTIONS
    MEMORY_PREDICTIONS = [p for p in MEMORY_PREDICTIONS if not (str(p.get("_id")) == str(prediction_id) and p.get("userId") == user_id)]
    return {"success": True, "message": "Prediction record deleted"}
