import os

# Backend API URL configuration for Render production and local development
API_URL = os.getenv(
    "API_URL",
    os.getenv("BACKEND_API_URL", "https://loan-predictor-ml-model.onrender.com")
).rstrip('/')
