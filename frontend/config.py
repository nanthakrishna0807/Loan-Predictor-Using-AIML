import os

BASE_URL = os.getenv("API_URL") or os.getenv("BACKEND_API_URL") or "http://127.0.0.1:8000/api"

def get_api_url(path: str = "") -> str:
    """
    Returns full API URL for a given endpoint path.
    Example: get_api_url("/health") -> "http://127.0.0.1:8000/api/health"
    """
    base = BASE_URL.rstrip('/')
    if not path:
        return base
    return f"{base}/{path.lstrip('/')}"

API_URL = BASE_URL
