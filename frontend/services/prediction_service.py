try:
    from frontend.services.api import make_api_request
except ModuleNotFoundError:
    from services.api import make_api_request


def predict_loan(payload: dict) -> tuple[bool, dict, str]:
    """
    Submits loan application parameters to POST /api/predict.
    Returns ML predictions, approval probability, EMI breakdown, and risk metrics.
    """
    success, res, err = make_api_request("/predict", method="POST", payload=payload, use_token=True)
    if success:
        result = res.get("result") or res.get("data", {}).get("result") or res
        return True, result, ""
    return False, {}, err


def get_loan_types() -> tuple[bool, dict, str]:
    """
    Fetches loan type rules and limits via GET /api/loans/types.
    """
    success, res, err = make_api_request("/loans/types", method="GET", use_token=False)
    if success:
        return True, res.get("data", {}), ""
    return False, {}, err
