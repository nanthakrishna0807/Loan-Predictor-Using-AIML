from fastapi import APIRouter, Depends, Header
from typing import Optional
from app.schemas.prediction import LoanPredictionInputSchema, EmiCalculationInputSchema
from app.services.prediction_service import (
    create_prediction,
    get_user_predictions,
    get_prediction_by_id,
    delete_prediction_by_id
)
from app.auth.jwt import get_current_user, oauth2_scheme
from app.ml.predictor import ml_predictor

router = APIRouter(tags=["Loan Predictions"])

async def get_user_from_auth_header(token: Optional[str] = Depends(oauth2_scheme)) -> Optional[dict]:
    if not token:
        return None
    try:
        return await get_current_user(token)
    except Exception:
        return None

@router.post("/predict")
@router.post("/predict/loan")
@router.post("/loan/predict")
async def predict_loan(payload: LoanPredictionInputSchema, current_user: Optional[dict] = Depends(get_user_from_auth_header)):
    user_id = str(current_user["_id"]) if current_user else None
    return await create_prediction(payload.model_dump(by_alias=True), user_id)

@router.get("/predict/history")
@router.get("/loan/history")
async def get_history(current_user: dict = Depends(get_current_user)):
    user_id = str(current_user["_id"])
    return await get_user_predictions(user_id)

@router.get("/predict/{id}")
@router.get("/loan/{id}")
async def get_by_id(id: str):
    return await get_prediction_by_id(id)

@router.delete("/predict/{id}")
@router.delete("/loan/{id}")
async def delete_by_id(id: str, current_user: dict = Depends(get_current_user)):
    user_id = str(current_user["_id"])
    return await delete_prediction_by_id(id, user_id)

@router.post("/calculate-emi")
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
