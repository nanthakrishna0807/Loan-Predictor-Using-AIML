from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.database.connection import db_manager
from app.utils.logger import logger

class DBMonitorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        is_connected = db_manager.db is not None
        request.state.db_connected = is_connected

        if not is_connected and not request.url.path.startswith("/api/health"):
            logger.warning(f"Request to {request.url.path} while database is disconnected")

        response = await call_next(request)
        return response
