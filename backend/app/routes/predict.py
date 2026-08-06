from typing import Optional
from fastapi import APIRouter, Depends
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

# Handler logic reusable across /api/predict and /api/loan routes
async def _handle_predict(payload: LoanPredictionInputSchema, token: str = Depends(oauth2_scheme)):
    user_id = None
    if token:
        try:
            user = await get_current_user(token)
            user_id = str(user["_id"])
        except Exception:
            user_id = None
    return await create_prediction(payload.model_dump(by_alias=True), user_id)

async def _handle_history(current_user: dict = Depends(get_current_user)):
    user_id = str(current_user["_id"])
    return await get_user_predictions(user_id)

async def _handle_get_by_id(id: str):
    return await get_prediction_by_id(id)

async def _handle_delete(id: str, current_user: dict = Depends(get_current_user)):
    user_id = str(current_user["_id"])
    return await delete_prediction_by_id(id, user_id)

# Standard Prompt Endpoints (/api/predict)
@router.post("/predict")
async def predict_loan(payload: LoanPredictionInputSchema, token: str = Depends(oauth2_scheme)):
    return await _handle_predict(payload, token)

@router.get("/predict/history")
async def predict_history(current_user: dict = Depends(get_current_user)):
    return await _handle_history(current_user)

@router.get("/predict/{id}")
async def get_predict_by_id(id: str):
    return await _handle_get_by_id(id)

@router.delete("/predict/{id}")
async def delete_predict_by_id(id: str, current_user: dict = Depends(get_current_user)):
    return await _handle_delete(id, current_user)

# React Frontend Alias Routes (/api/loan/*)
@router.post("/loan/predict")
async def loan_predict_alias(payload: LoanPredictionInputSchema, token: str = Depends(oauth2_scheme)):
    return await _handle_predict(payload, token)

@router.get("/loan/history")
async def loan_history_alias(current_user: dict = Depends(get_current_user)):
    return await _handle_history(current_user)

@router.get("/loan/{id}")
async def get_loan_by_id_alias(id: str):
    return await _handle_get_by_id(id)

@router.delete("/loan/{id}")
async def delete_loan_by_id_alias(id: str, current_user: dict = Depends(get_current_user)):
    return await _handle_delete(id, current_user)

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
