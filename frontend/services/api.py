import requests
import streamlit as st
try:
    from frontend.config import get_api_url
except ModuleNotFoundError:
    from config import get_api_url


def make_api_request(
    endpoint: str,
    method: str = "GET",
    payload: dict = None,
    use_token: bool = True,
    timeout: int = 10
) -> tuple[bool, dict, str]:
    """
    Central HTTP client helper for Streamlit frontend.
    Handles Bearer auth token, status code validation (200, 400, 401, 403, 404, 422, 500),
    and error formatting.
    """
    url = get_api_url(endpoint)
    headers = {"Content-Type": "application/json"}

    if use_token:
        token = st.session_state.get("token")
        if token:
            headers["Authorization"] = f"Bearer {token}"

    m = method.upper()
    try:
        if m == "POST":
            response = requests.post(url, json=payload or {}, headers=headers, timeout=timeout)
        elif m == "PUT":
            response = requests.put(url, json=payload or {}, headers=headers, timeout=timeout)
        elif m == "DELETE":
            response = requests.delete(url, headers=headers, timeout=timeout)
        else:
            response = requests.get(url, headers=headers, timeout=timeout)

        status_code = response.status_code

        if status_code in (200, 201):
            try:
                res_data = response.json()
                return True, res_data, ""
            except Exception:
                return True, {}, ""

        # Error status code handling
        try:
            res_json = response.json()
            err_msg = res_json.get("detail") or res_json.get("message") or f"HTTP Error {status_code}"
        except Exception:
            err_msg = f"HTTP Error {status_code}"

        if status_code == 401:
            st.toast("⚠️ Session expired or invalid credentials.", icon="🚨")
        elif status_code == 403:
            st.toast("🛡️ Access forbidden.", icon="🚫")
        elif status_code == 422:
            st.toast("⚠️ Validation error in request.", icon="⚠️")
        elif status_code == 500:
            st.toast("💥 Internal server error.", icon="💥")

        return False, {}, err_msg

    except requests.exceptions.Timeout:
        err_msg = f"Request to {endpoint} timed out after {timeout} seconds."
        st.toast("⏱️ Request Timeout", icon="⏳")
        return False, {}, err_msg
    except Exception as ex:
        err_msg = f"Unable to reach server at {url}: {ex}"
        return False, {}, err_msg
