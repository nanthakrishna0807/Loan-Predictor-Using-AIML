from typing import Optional
from fastapi import APIRouter, Depends, Request
from app.schemas.prediction import EmiCalculationInputSchema
from app.services.prediction_service import (
    create_prediction,
    get_user_predictions,
    get_prediction_by_id,
    delete_prediction_by_id
)
from app.auth.jwt import get_current_user, oauth2_scheme
from app.ml.predictor import ml_predictor
from app.utils.logger import logger
from app.utils.loan_type_rules import LOAN_CONFIG, LOAN_TYPES

router = APIRouter(tags=["Loan Predictions"])

# ── Loan types config endpoint (public) ─────────────────────────────────────
@router.get("/loans/types")
async def get_loan_types():
    """Returns all loan type configurations for the frontend."""
    types_data = {}
    for lt, cfg in LOAN_CONFIG.items():
        types_data[lt] = {
            "icon":              cfg["icon"],
            "rate":              cfg["rate"],
            "min_tenure_years":  cfg["min_tenure_years"],
            "max_tenure_years":  cfg["max_tenure_years"],
            "default_tenure_years": cfg["default_tenure_years"],
            "max_amount":        cfg["max_amount"],
            "min_amount":        cfg["min_amount"],
            "min_cibil":         cfg["min_cibil"],
            "required_documents": cfg["required_documents"],
        }
    return {"success": True, "data": types_data, "loan_types": LOAN_TYPES}

# -----------------------------------------------------------------------
# POST /api/predict & /api/predict/public
# Accepts JSON with loan fields (loan_type, loan_amount, tenure, etc.)
# -----------------------------------------------------------------------
@router.post("/predict")
@router.post("/predict/public")
async def predict_loan(request: Request, token: Optional[str] = Depends(oauth2_scheme)):
    """
    Main prediction endpoint. Accepts any loan prediction payload.
    Identifies user if Bearer token is provided.
    """
    user_id = None
    if token:
        try:
            user = await get_current_user(token)
            user_id = str(user["_id"])
        except Exception:
            user_id = None

    try:
        raw_payload = await request.json()
    except Exception:
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": "Invalid JSON payload"}
        )

    res_doc = await create_prediction(raw_payload, user_id)
    pred_res = res_doc.get("data", {}).get("result", {})

    # Log activity
    try:
        from app.services.activity_log_service import log_activity
        await log_activity(
            action="Loan Application Submitted",
            actor_id=user_id or "anonymous",
            actor_name=raw_payload.get("fullName", "Applicant"),
            loan_type=pred_res.get("loan_type", "Personal Loan"),
            metadata={"loanAmount": pred_res.get("loan_amount"), "approved": pred_res.get("approved")}
        )
    except Exception:
        pass

    # Ensure response contains all standardized fields matching requirements
    approval_prob = pred_res.get("approval_probability", 50.0)
    loan_status = pred_res.get("loan_status", "Approved" if pred_res.get("approved") else "Rejected")
    risk_str = pred_res.get("credit_risk_level", "Low")
    interest_rate = pred_res.get("interest_rate_estimate", 8.5)
    monthly_emi = pred_res.get("emi_estimate", 0.0)
    recommended_amount = pred_res.get("suggested_max_loan", pred_res.get("loan_amount", 0))
    dti_ratio = int(pred_res.get("debt_to_income_ratio", 0.3) * 100)

    return {
        "success": True,
        "approval_probability": approval_prob,
        "loan_status": loan_status,
        "risk": risk_str,
        "interest_rate": interest_rate,
        "monthly_emi": monthly_emi,
        "recommended_amount": recommended_amount,
        "dti_ratio": dti_ratio,
        "approved": pred_res.get("approved", False),
        "data": res_doc.get("data", {}),
        "result": pred_res
    }

@router.get("/predict/history")
async def predict_history(current_user: dict = Depends(get_current_user)):
    user_id = str(current_user["_id"])
    return await get_user_predictions(user_id)

@router.get("/predict/{id}")
async def get_predict_by_id(id: str):
    return await get_prediction_by_id(id)

@router.delete("/predict/{id}")
async def delete_predict_by_id(id: str, current_user: dict = Depends(get_current_user)):
    user_id = str(current_user["_id"])
    return await delete_prediction_by_id(id, user_id)

# Alias routes
@router.post("/loan/predict")
async def loan_predict_alias(request: Request, token: Optional[str] = Depends(oauth2_scheme)):
    return await predict_loan(request, token)

@router.get("/loan/history")
async def loan_history_alias(current_user: dict = Depends(get_current_user)):
    user_id = str(current_user["_id"])
    return await get_user_predictions(user_id)

@router.post("/loan/calculate-emi")
async def calculate_emi_endpoint(payload: EmiCalculationInputSchema):
    emi = ml_predictor.calculate_emi(payload.loanAmount, payload.interestRate, payload.tenureMonths)
    return {
        "success": True,
        "data": {
            "emi": emi,
            "loanAmount": payload.loanAmount,
            "interestRate": payload.interestRate,
            "tenureMonths": payload.tenureMonths
        }
    }
