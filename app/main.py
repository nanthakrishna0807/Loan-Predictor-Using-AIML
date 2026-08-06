import sys
import os
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# Add project root directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import settings
from app.database.connection import connect_to_mongo, close_mongo_connection
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.predict import router as predict_router
from app.api.admin import router as admin_router
from app.api.health import router as health_router
from app.utils.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager: handles startup and shutdown tasks.
    """
    logger.info("Initializing FastAPI Backend startup sequence...")
    await connect_to_mongo()
    yield
    logger.info("Shutting down FastAPI Backend...")
    await close_mongo_connection()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Production-ready FastAPI Backend for AI Loan Predictor using Machine Learning & MongoDB Atlas",
    lifespan=lifespan
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers under /api
app.include_router(health_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(predict_router, prefix="/api")
app.include_router(admin_router, prefix="/api")

# Custom Request Validation Exception Handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        loc = " -> ".join([str(x) for x in err.get("loc", [])])
        msg = err.get("msg")
        errors.append(f"{loc}: {msg}")
    
    logger.warning(f"Validation failure on {request.url.path}: {errors}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "message": "Input validation error",
            "errors": errors,
            "detail": exc.errors()
        }
    )

# Root endpoint
@app.get("/")
async def root():
    return {
        "success": True,
        "message": "AI Loan Predictor Python FastAPI Backend is Live",
        "docs": "/docs",
        "health": "/api/health"
    }

if __name__ == "__main__":
    print(f"🚀 Launching FastAPI Server on {settings.HOST}:{settings.PORT}")
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
