from fastapi import APIRouter, Depends, HTTPException, Body
from bson import ObjectId
from datetime import datetime, timedelta
from collections import defaultdict
from app.database.connection import get_database
from app.auth.jwt import get_current_admin_user
from app.ml.predictor import ml_predictor
from app.utils.logger import logger

router = APIRouter(prefix="/admin", tags=["Admin Dashboard"])

async def _count(db, collection: str, query: dict = {}) -> int:
    try:
        return await db[collection].count_documents(query)
    except Exception:
        return 0

# ─────────────────────────────────────────────────────────────────────────────
# GET /api/admin/dashboard
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/dashboard")
@router.get("/dashboard-stats")
async def get_admin_dashboard(current_user: dict = Depends(get_current_admin_user)):
    db = get_database()
    if db is None:
        return {
            "success": True,
            "total_users": 0, "active_users": 0, "total_predictions": 0,
            "approved_loans": 0, "pending_loans": 0, "rejected_loans": 0,
            "today_logins": 0,
            "data": {
                "totalUsers": 0, "activeUsers": 0, "totalPredictions": 0,
                "approvedCount": 0, "rejectedCount": 0, "pendingCount": 0,
                "todayApplications": 0, "todayLogins": 0, "approvalRate": 0.0,
                "averageCibilScore": 0.0, "loanTypeDistribution": {},
                "userStatusBreakdown": {"Active": 0, "Pending": 0, "Inactive": 0, "Locked": 0},
                "dailyTrends": []
            }
        }

    total_users = await _count(db, "users")
    active_users = await _count(db, "users", {"isActive": True})
    inactive_users = await _count(db, "users", {"isActive": False})
    total_predictions = await _count(db, "predictions")
    approved_loans = await _count(db, "predictions", {"result.approved": True})
    rejected_loans = total_predictions - approved_loans
    pending_loans = await _count(db, "predictions", {"status": "Pending"})

    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_applications = await _count(db, "predictions", {"createdAt": {"$gte": today_start}})
    today_logins = await _count(db, "activity_logs", {"action": "User Login", "timestamp": {"$gte": today_start}})

    # Calculate average CIBIL
    avg_cibil = 0.0
    try:
        pipeline = [{"$group": {"_id": None, "avg": {"$avg": "$result.cibil_score"}}}]
        async for doc in db.predictions.aggregate(pipeline):
            avg_cibil = round(doc.get("avg", 0) or 0, 1)
    except Exception:
        pass

    # Loan type distribution
    loan_type_dist = defaultdict(int)
    try:
        async for doc in db.predictions.find({}, {"result.loan_type": 1}):
            lt = (doc.get("result") or {}).get("loan_type", "Personal Loan")
            loan_type_dist[lt] += 1
    except Exception:
        pass

    # Daily trends for last 30 days
    since = datetime.utcnow() - timedelta(days=30)
    daily_trends = []
    try:
        logins_by_day = defaultdict(int)
        async for doc in db.activity_logs.find({"action": "User Login", "timestamp": {"$gte": since}}):
            dt = doc.get("timestamp")
            day_str = dt.strftime("%m/%d") if isinstance(dt, datetime) else str(dt)[:10]
            logins_by_day[day_str] += 1

        apps_by_day = defaultdict(int)
        async for doc in db.predictions.find({"createdAt": {"$gte": since}}):
            dt = doc.get("createdAt")
            day_str = dt.strftime("%m/%d") if isinstance(dt, datetime) else str(dt)[:10]
            apps_by_day[day_str] += 1

        for i in range(30):
            day_dt = since + timedelta(days=i)
            day_str = day_dt.strftime("%m/%d")
            daily_trends.append({
                "date": day_str,
                "logins": logins_by_day.get(day_str, 0),
                "applications": apps_by_day.get(day_str, 0),
                "logs": logins_by_day.get(day_str, 0) + apps_by_day.get(day_str, 0)
            })
    except Exception as ex:
        logger.warning(f"Trend error: {ex}")

    approval_rate = round((approved_loans / total_predictions * 100), 2) if total_predictions > 0 else 0.0

    return {
        "success": True,
        "total_users": total_users,
        "active_users": active_users,
        "total_predictions": total_predictions,
        "approved_loans": approved_loans,
        "pending_loans": pending_loans,
        "rejected_loans": rejected_loans,
        "today_logins": today_logins,
        "data": {
            "totalUsers": total_users,
            "activeUsers": active_users,
            "inactiveUsers": inactive_users,
            "totalPredictions": total_predictions,
            "approvedCount": approved_loans,
            "rejectedCount": rejected_loans,
            "pendingCount": pending_loans,
            "todayApplications": today_applications,
            "todayLogins": today_logins,
            "approvalRate": approval_rate,
            "averageCibilScore": avg_cibil,
            "loanTypeDistribution": dict(loan_type_dist),
            "userStatusBreakdown": {
                "Active": active_users,
                "Pending Request": pending_loans,
                "Inactive": inactive_users,
                "Locked": 0
            },
            "dailyTrends": daily_trends,
            "mlModelStatus": {
                "loaded": ml_predictor.model_loaded,
                "algorithm": ml_predictor.best_model_name,
                "accuracy": ml_predictor.accuracy
            }
        }
    }

# ─────────────────────────────────────────────────────────────────────────────
# GET /api/admin/users
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/users")
async def get_all_users(current_user: dict = Depends(get_current_admin_user)):
    db = get_database()
    if db is None:
        return {"success": True, "count": 0, "data": []}

    users = []
    async for doc in db.users.find({}).sort("createdAt", -1):
        users.append({
            "id": str(doc["_id"]),
            "_id": str(doc["_id"]),
            "name": doc.get("name"),
            "email": doc.get("email"),
            "role": doc.get("role", "user"),
            "phone": doc.get("phone", ""),
            "occupation": doc.get("occupation", ""),
            "isActive": doc.get("isActive", True),
            "createdAt": str(doc.get("createdAt", ""))[:19]
        })

    return {"success": True, "count": len(users), "data": users}

# ─────────────────────────────────────────────────────────────────────────────
# PUT /api/admin/users/{user_id}
# ─────────────────────────────────────────────────────────────────────────────
@router.put("/users/{user_id}")
async def update_user_by_admin(
    user_id: str,
    payload: dict = Body(...),
    current_user: dict = Depends(get_current_admin_user)
):
    db = get_database()
    if db is None:
        raise HTTPException(status_code=503, detail="Database connection unavailable")

    try:
        query_id = ObjectId(user_id)
    except Exception:
        query_id = user_id

    update_fields = {k: v for k, v in payload.items() if v is not None}
    update_fields["updatedAt"] = datetime.utcnow()

    res = await db.users.update_one({"_id": query_id}, {"$set": update_fields})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"success": True, "message": "User updated successfully"}

# ─────────────────────────────────────────────────────────────────────────────
# DELETE /api/admin/users/{user_id}
# ─────────────────────────────────────────────────────────────────────────────
@router.delete("/users/{user_id}")
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

# ─────────────────────────────────────────────────────────────────────────────
# GET /api/admin/activity  (All activity: login history, requests, predictions)
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/activity")
@router.get("/activity-logs")
async def get_activity_logs(current_user: dict = Depends(get_current_admin_user)):
    db = get_database()
    if db is None:
        return {"success": True, "count": 0, "data": []}

    logs = []
    try:
        cursor = db.activity_logs.find({}).sort("timestamp", -1).limit(100)
        async for doc in cursor:
            dt = doc.get("timestamp")
            logs.append({
                "id": str(doc["_id"]),
                "_id": str(doc["_id"]),
                "user": doc.get("actorName", doc.get("actorId", "System")),
                "activityType": doc.get("action", "General Activity"),
                "timestamp": dt.isoformat() if isinstance(dt, datetime) else str(dt)[:19],
                "details": str(doc.get("metadata", {})),
                "loanType": doc.get("loanType", "N/A")
            })
    except Exception as ex:
        logger.warning(f"Error reading activity logs: {ex}")

    return {"success": True, "count": len(logs), "data": logs}

# ─────────────────────────────────────────────────────────────────────────────
# GET /api/admin/loan-requests
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/loan-requests")
async def get_pending_loan_requests(current_user: dict = Depends(get_current_admin_user)):
    db = get_database()
    if db is None:
        return {"success": True, "count": 0, "data": []}

    requests_list = []
    cursor = db.predictions.find({"status": "Pending"}).sort("createdAt", -1)
    async for doc in cursor:
        res = doc.get("result", {})
        inp = doc.get("inputData", {})
        dt = doc.get("createdAt")
        requests_list.append({
            "id": str(doc["_id"]),
            "_id": str(doc["_id"]),
            "requestId": f"Request #{str(doc['_id'])[-4:]}",
            "user": inp.get("fullName", doc.get("userId", "Applicant")),
            "loanType": res.get("loan_type", "Personal Loan"),
            "amount": res.get("loan_amount", inp.get("LoanAmount", 0)),
            "status": doc.get("status", "Pending"),
            "details": f"Loan Amount: ₹{float(res.get('loan_amount', 0)):,.0f}",
            "date": dt.isoformat() if isinstance(dt, datetime) else str(dt)[:19]
        })

    return {"success": True, "count": len(requests_list), "data": requests_list}

# ─────────────────────────────────────────────────────────────────────────────
# PUT /api/admin/loan/{id}/approve
# ─────────────────────────────────────────────────────────────────────────────
@router.put("/loan/{id}/approve")
async def approve_loan_request(id: str, current_user: dict = Depends(get_current_admin_user)):
    db = get_database()
    if db is None:
        raise HTTPException(status_code=503, detail="Database connection unavailable")

    try:
        query_id = ObjectId(id)
    except Exception:
        query_id = id

    res = await db.predictions.update_one(
        {"_id": query_id},
        {"$set": {"status": "Approved", "result.approved": True, "result.loan_status": "Approved", "updatedAt": datetime.utcnow()}}
    )
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Loan request record not found")

    return {"success": True, "message": "Loan application approved successfully"}

# ─────────────────────────────────────────────────────────────────────────────
# PUT /api/admin/loan/{id}/reject
# ─────────────────────────────────────────────────────────────────────────────
@router.put("/loan/{id}/reject")
async def reject_loan_request(id: str, current_user: dict = Depends(get_current_admin_user)):
    db = get_database()
    if db is None:
        raise HTTPException(status_code=503, detail="Database connection unavailable")

    try:
        query_id = ObjectId(id)
    except Exception:
        query_id = id

    res = await db.predictions.update_one(
        {"_id": query_id},
        {"$set": {"status": "Rejected", "result.approved": False, "result.loan_status": "Rejected", "updatedAt": datetime.utcnow()}}
    )
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Loan request record not found")

    return {"success": True, "message": "Loan application rejected successfully"}

# ─────────────────────────────────────────────────────────────────────────────
# GET /api/admin/predictions
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/predictions")
async def get_all_predictions(current_user: dict = Depends(get_current_admin_user)):
    db = get_database()
    if db is None:
        return {"success": True, "count": 0, "data": []}

    predictions = []
    async for doc in db.predictions.find({}).sort("createdAt", -1).limit(200):
        result = doc.get("result", {})
        dt = doc.get("createdAt")
        predictions.append({
            "id": str(doc["_id"]),
            "_id": str(doc["_id"]),
            "userId": doc.get("userId", "anonymous"),
            "loanType": result.get("loan_type", "Unknown"),
            "loanAmount": result.get("loan_amount", 0),
            "approved": result.get("approved", False),
            "probability": result.get("approval_probability", 0),
            "riskLevel": result.get("credit_risk_level", "N/A"),
            "cibilScore": result.get("cibil_score", 0),
            "inputData": doc.get("inputData", {}),
            "result": result,
            "createdAt": dt.isoformat() if isinstance(dt, datetime) else str(dt)[:19]
        })

    return {"success": True, "count": len(predictions), "data": predictions}
