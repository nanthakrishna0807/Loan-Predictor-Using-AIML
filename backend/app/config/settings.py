import os
from dotenv import load_dotenv

load_dotenv()

try:
    from pydantic_settings import BaseSettings
    class Settings(BaseSettings):
        PROJECT_NAME: str = "AI Loan Predictor API"
        VERSION: str = "2.0.0"
        API_V1_STR: str = "/api"
        
        PORT: int = int(os.getenv("PORT", 5000))
        HOST: str = os.getenv("HOST", "0.0.0.0")
        ENVIRONMENT: str = os.getenv("ENVIRONMENT", os.getenv("NODE_ENV", "development"))
        
        MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017/loanpredictor")
        DB_NAME: str = os.getenv("DB_NAME", "loanpredictor")
        
        JWT_SECRET: str = os.getenv("JWT_SECRET", "super_secret_jwt_key_loan_predictor_2026_ai")
        JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
        ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 43200))
        
        ALLOWED_ORIGINS: str = os.getenv(
            "ALLOWED_ORIGINS",
            "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173,http://127.0.0.1:3000"
        )

        @property
        def origins_list(self) -> list[str]:
            return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]

except ImportError:
    from pydantic import BaseModel
    class Settings(BaseModel):
        PROJECT_NAME: str = "AI Loan Predictor API"
        VERSION: str = "2.0.0"
        API_V1_STR: str = "/api"
        
        PORT: int = int(os.getenv("PORT", 5000))
        HOST: str = os.getenv("HOST", "0.0.0.0")
        ENVIRONMENT: str = os.getenv("ENVIRONMENT", os.getenv("NODE_ENV", "development"))
        
        MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017/loanpredictor")
        DB_NAME: str = os.getenv("DB_NAME", "loanpredictor")
        
        JWT_SECRET: str = os.getenv("JWT_SECRET", "super_secret_jwt_key_loan_predictor_2026_ai")
        JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
        ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 43200))
        
        ALLOWED_ORIGINS: str = os.getenv(
            "ALLOWED_ORIGINS",
            "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173,http://127.0.0.1:3000"
        )

        @property
        def origins_list(self) -> list[str]:
            return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]

settings = Settings()
