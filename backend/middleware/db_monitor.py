import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from backend.utils.logger import logger

class DBMonitorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        
        # Add server processing timing header
        response.headers["X-Process-Time-MS"] = f"{process_time:.2f}"
        return response
