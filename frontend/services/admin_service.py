try:
    from frontend.services.api import make_api_request
except ModuleNotFoundError:
    from services.api import make_api_request


def get_admin_dashboard_stats() -> tuple[bool, dict, str]:
    """
    Fetches real-time admin KPIs and charts via GET /api/admin/dashboard.
    """
    success, res, err = make_api_request("/admin/dashboard", method="GET", use_token=True)
    if success:
        return True, res.get("data", res), ""
    return False, {}, err


def get_all_users() -> tuple[bool, list, str]:
    """
    Fetches all registered users via GET /api/admin/users.
    """
    success, res, err = make_api_request("/admin/users", method="GET", use_token=True)
    if success:
        return True, res.get("data", []), ""
    return False, [], err


def update_user_by_admin(user_id: str, payload: dict) -> tuple[bool, dict, str]:
    """
    Updates user details, role, status, or password via PUT /api/admin/users/{user_id}.
    """
    return make_api_request(f"/admin/users/{user_id}", method="PUT", payload=payload, use_token=True)


def delete_user_by_admin(user_id: str) -> tuple[bool, dict, str]:
    """
    Deletes user account via DELETE /api/admin/users/{user_id}.
    """
    return make_api_request(f"/admin/users/{user_id}", method="DELETE", use_token=True)


def get_admin_activity_logs() -> tuple[bool, list, str]:
    """
    Fetches activity logs via GET /api/admin/activity.
    """
    success, res, err = make_api_request("/admin/activity", method="GET", use_token=True)
    if success:
        return True, res.get("data", []), ""
    return False, [], err


def get_pending_loan_requests() -> tuple[bool, list, str]:
    """
    Fetches pending loans via GET /api/admin/loan-requests.
    """
    success, res, err = make_api_request("/admin/loan-requests", method="GET", use_token=True)
    if success:
        return True, res.get("data", []), ""
    return False, [], err


def approve_loan_request(loan_id: str) -> tuple[bool, dict, str]:
    """
    Approves loan application via PUT /api/admin/loan/{loan_id}/approve.
    """
    return make_api_request(f"/admin/loan/{loan_id}/approve", method="PUT", use_token=True)


def reject_loan_request(loan_id: str) -> tuple[bool, dict, str]:
    """
    Rejects loan application via PUT /api/admin/loan/{loan_id}/reject.
    """
    return make_api_request(f"/admin/loan/{loan_id}/reject", method="PUT", use_token=True)
