import os
from dotenv import load_dotenv

load_dotenv()

try:
    from pydantic_settings import BaseSettings
    class Settings(BaseSettings):
        APP_NAME: str = os.getenv("APP_NAME", "AI Loan Predictor")
        APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
        API_PREFIX: str = os.getenv("API_PREFIX", "/api")
        
        PORT: int = int(os.getenv("PORT", 8000))
        HOST: str = os.getenv("HOST", "0.0.0.0")
        ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
        
        MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017/loanpredictor")
        DATABASE_NAME: str = os.getenv("DATABASE_NAME", os.getenv("DB_NAME", "loanpredictor"))
        
        JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", os.getenv("JWT_SECRET", "super_secret_jwt_key_loan_predictor_2026_ai"))
        JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
        ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
        
        ALLOWED_ORIGINS: str = os.getenv(
            "ALLOWED_ORIGINS",
            "http://localhost:8501,http://127.0.0.1:8501,http://localhost:8000,http://127.0.0.1:8000"
        )

        @property
        def origins_list(self) -> list[str]:
            return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]

except ImportError:
    from pydantic import BaseModel
    class Settings(BaseModel):
        APP_NAME: str = os.getenv("APP_NAME", "AI Loan Predictor")
        APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
        API_PREFIX: str = os.getenv("API_PREFIX", "/api")
        
        PORT: int = int(os.getenv("PORT", 8000))
        HOST: str = os.getenv("HOST", "0.0.0.0")
        ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
        
        MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017/loanpredictor")
        DATABASE_NAME: str = os.getenv("DATABASE_NAME", os.getenv("DB_NAME", "loanpredictor"))
        
        JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", os.getenv("JWT_SECRET", "super_secret_jwt_key_loan_predictor_2026_ai"))
        JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
        ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
        
        ALLOWED_ORIGINS: str = os.getenv(
            "ALLOWED_ORIGINS",
            "http://localhost:8501,http://127.0.0.1:8501,http://localhost:8000,http://127.0.0.1:8000"
        )

        @property
        def origins_list(self) -> list[str]:
            return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]

settings = Settings()
