import streamlit as st
try:
    from frontend.services.api import make_api_request
except ModuleNotFoundError:
    from services.api import make_api_request


def login(email: str, password: str) -> tuple[bool, dict, str]:
    """
    Authenticates user via POST /api/auth/login.
    On success, stores access_token, user, and role in st.session_state.
    """
    payload = {"email": email, "password": password}
    success, res, err = make_api_request("/auth/login", method="POST", payload=payload, use_token=False)

    if success:
        user_obj = res.get("user") or res.get("data", {}).get("user", {})
        token = res.get("access_token") or res.get("token") or res.get("data", {}).get("token")
        user_role = (user_obj.get("role") or "user").lower()

        st.session_state["token"] = token
        st.session_state["user"] = user_obj
        st.session_state["role"] = user_role

        return True, res, ""
    return False, {}, err


def register(name: str, email: str, password: str, role: str = "user", phone: str = "", occupation: str = "") -> tuple[bool, dict, str]:
    """
    Registers new user via POST /api/auth/register.
    """
    payload = {
        "name": name,
        "email": email,
        "password": password,
        "role": role,
        "phone": phone,
        "occupation": occupation
    }
    return make_api_request("/auth/register", method="POST", payload=payload, use_token=False)


def logout() -> bool:
    """
    Calls POST /api/auth/logout and clears user session state.
    """
    make_api_request("/auth/logout", method="POST", use_token=True)
    st.session_state["token"] = None
    st.session_state["user"] = None
    st.session_state["role"] = None
    return True


def refresh_token() -> tuple[bool, dict, str]:
    """
    Refreshes access token via POST /api/auth/refresh.
    """
    return make_api_request("/auth/refresh", method="POST", use_token=True)
