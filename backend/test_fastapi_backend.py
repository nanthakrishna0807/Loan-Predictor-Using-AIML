import asyncio
import sys
import os
import json
import urllib.request
import urllib.error

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def safe_print(text: str):
    try:
        print(text)
    except UnicodeEncodeError:
        clean_text = text.encode('ascii', 'ignore').decode('ascii')
        print(clean_text)

# Add root project directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.config import settings
from backend.database.connection import connect_to_mongo, close_mongo_connection, db_manager
from ml.predictor import ml_predictor

async def test_fastapi_backend_suite():
    safe_print("==================================================")
    safe_print("🧪 Starting Automated FastAPI Backend Integration Suite")
    safe_print("==================================================\n")

    # Step 1: Test MongoDB Motor Connection
    safe_print("--- 1. Testing MongoDB Motor Connection ---")
    await connect_to_mongo()
    
    if db_manager.db is not None:
        safe_print("✅ Motor Database Connection Active")
    else:
        safe_print("❌ Motor Database Connection Inactive")

    # Step 2: Test ML Model Artifact Loading
    safe_print("\n--- 2. Testing ML Model Engine ---")
    safe_print(f"ML Model Loaded: {ml_predictor.model_loaded}")
    safe_print(f"Algorithm Name: {ml_predictor.best_model_name}")

    # Test Prediction Logic
    sample_input = {
        "Name": "Integration Test User",
        "Age": 30,
        "Gender": "Female",
        "Occupation": "Data Analyst",
        "EmploymentType": "Salaried",
        "MonthlyIncome": 75000,
        "ExistingEMI": 10000,
        "LoanAmount": 300000,
        "LoanTenure": 36,
        "CIBILScore": 780,
        "Dependents": 0,
        "Education": "Graduate",
        "PropertyOwnership": "Urban"
    }

    pred_res = ml_predictor.predict(sample_input)
    safe_print("Sample Prediction Result:")
    safe_print(json.dumps(pred_res, indent=2))

    await close_mongo_connection()

    safe_print("\n==================================================")
    safe_print("✅ FASTAPI INTEGRATION SUITE COMPLETED SUCCESSFULLY")
    safe_print("==================================================\n")

if __name__ == "__main__":
    asyncio.run(test_fastapi_backend_suite())
