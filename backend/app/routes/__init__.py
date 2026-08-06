from .auth import router as auth_router
from .users import router as users_router
from .predict import router as predict_router
from .health import router as health_router
from .admin import router as admin_router

__all__ = ["auth_router", "users_router", "predict_router", "health_router", "admin_router"]
