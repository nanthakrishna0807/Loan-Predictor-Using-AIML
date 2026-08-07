try:
    from frontend.services.api import make_api_request
except ModuleNotFoundError:
    from services.api import make_api_request


def get_user_profile() -> tuple[bool, dict, str]:
    """
    Fetches user profile via GET /api/users/profile.
    """
    success, res, err = make_api_request("/users/profile", method="GET", use_token=True)
    if success:
        return True, res.get("data", res), ""
    return False, {}, err


def update_user_profile(name: str = None, password: str = None) -> tuple[bool, dict, str]:
    """
    Updates user profile via PUT /api/users/profile.
    """
    payload = {}
    if name:
        payload["name"] = name
    if password:
        payload["password"] = password
    return make_api_request("/users/profile", method="PUT", payload=payload, use_token=True)


def get_user_prediction_history() -> tuple[bool, list, str]:
    """
    Fetches prediction history via GET /api/users/history.
    """
    success, res, err = make_api_request("/users/history", method="GET", use_token=True)
    if success:
        return True, res.get("data", []), ""
    return False, [], err
