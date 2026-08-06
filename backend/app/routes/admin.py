from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from app.database.connection import get_database
from app.auth.jwt import get_current_admin_user
from app.ml.predictor import ml_predictor

router = APIRouter(prefix="/admin", tags=["Admin Dashboard"])

@router.get("/dashboard")
async def get_admin_dashboard(current_user: dict = Depends(get_current_admin_user)):
    db = get_database()
    if db is None:
        return {"success": True, "data": {"totalUsers": 0, "totalPredictions": 0, "approvalRate": 0}}

    total_users = await db.users.count_documents({})
    total_predictions = await db.predictions.count_documents({})

    approved_count = await db.predictions.count_documents({"result.approved": True})
    approval_rate = round((approved_count / total_predictions * 100), 2) if total_predictions > 0 else 0.0

    recent_predictions = []
    cursor = db.predictions.find({}).sort("createdAt", -1).limit(5)
    async for doc in cursor:
        recent_predictions.append({
            "id": str(doc["_id"]),
            "userId": doc.get("userId"),
            "approved": doc.get("result", {}).get("approved", False),
            "createdAt": str(doc.get("createdAt"))
        })

    return {
        "success": True,
        "data": {
            "totalUsers": total_users,
            "totalPredictions": total_predictions,
            "approvedCount": approved_count,
            "approvalRate": approval_rate,
            "recentPredictions": recent_predictions,
            "mlModelStatus": {
                "loaded": ml_predictor.model_loaded,
                "algorithm": ml_predictor.best_model_name,
                "accuracy": ml_predictor.accuracy
            }
        }
    }

@router.get("/users")
async def get_all_users(current_user: dict = Depends(get_current_admin_user)):
    db = get_database()
    if db is None:
        return {"success": True, "count": 0, "data": []}

    users = []
    cursor = db.users.find({}).sort("createdAt", -1)
    async for doc in cursor:
        users.append({
            "id": str(doc["_id"]),
            "_id": str(doc["_id"]),
            "name": doc.get("name"),
            "email": doc.get("email"),
            "role": doc.get("role", "user"),
            "phone": doc.get("phone", ""),
            "occupation": doc.get("occupation", ""),
            "createdAt": str(doc.get("createdAt"))
        })

    return {"success": True, "count": len(users), "data": users}

@router.get("/predictions")
async def get_all_predictions(current_user: dict = Depends(get_current_admin_user)):
    db = get_database()
    if db is None:
        return {"success": True, "count": 0, "data": []}

    predictions = []
    cursor = db.predictions.find({}).sort("createdAt", -1)
    async for doc in cursor:
        predictions.append({
            "id": str(doc["_id"]),
            "_id": str(doc["_id"]),
            "userId": doc.get("userId"),
            "inputData": doc.get("inputData", {}),
            "result": doc.get("result", {}),
            "createdAt": str(doc.get("createdAt"))
        })

    return {"success": True, "count": len(predictions), "data": predictions}

@router.get("/analytics")
async def get_analytics(current_user: dict = Depends(get_current_admin_user)):
    db = get_database()
    total_users = await db.users.count_documents({}) if db is not None else 0
    total_preds = await db.predictions.count_documents({}) if db is not None else 0
    approved = await db.predictions.count_documents({"result.approved": True}) if db is not None else 0
    rejected = total_preds - approved

    return {
        "success": True,
        "data": {
            "totalUsers": total_users,
            "totalPredictions": total_preds,
            "approved": approved,
            "rejected": rejected,
            "approvalRate": round((approved / total_preds * 100), 1) if total_preds > 0 else 0,
            "modelPerformance": {
                "bestModel": ml_predictor.best_model_name,
                "accuracy": ml_predictor.accuracy
            }
        }
    }

@router.post("/retrain-model")
async def retrain_model(current_user: dict = Depends(get_current_admin_user)):
    ml_predictor.load_artifacts()
    return {
        "success": True,
        "message": "Model retrained and artifacts reloaded successfully",
        "data": {
            "model": ml_predictor.best_model_name,
            "accuracy": ml_predictor.accuracy
        }
    }

@router.delete("/user/{user_id}")
async def delete_user(user_id: str, current_user: dict = Depends(get_current_admin_user)):
    db = get_database()
    if db is None:
        raise HTTPException(status_code=503, detail="Database connection unavailable")

    try:
        query_id = ObjectId(user_id)
    except Exception:
        query_id = user_id

    res = await db.users.delete_one({"_id": query_id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"success": True, "message": "User account deleted successfully"}
