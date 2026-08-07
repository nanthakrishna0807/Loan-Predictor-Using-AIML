import streamlit as st
import requests

def render():
    st.markdown("<h2 style='color: #111827;'>🔑 Enterprise User Authentication</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #4B5563; font-size: 0.95rem;'>Sign in to access your loan predictions, credit history, and analytics dashboard.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns([1.1, 1])

    with col1:
        with st.form("login_enterprise_form"):
            st.markdown("<h4 style='color: #111827;'>Sign In to Your Account</h4>", unsafe_allow_html=True)
            email = st.text_input("Email Address *", placeholder="user@example.com")
            password = st.text_input("Password *", type="password", placeholder="••••••••")
            submit = st.form_submit_button("Sign In to Portal", use_container_width=True)

            if submit:
                if not email or not password:
                    st.error("Please enter both email address and password.")
                else:
                    try:
                        try:
                            from frontend.config import API_URL
                        except ModuleNotFoundError:
                            from config import API_URL
                        backend_url = f"{API_URL}/api/auth/login"
                        res = requests.post(backend_url, json={"email": email, "password": password}, timeout=10)
                        
                        if res.status_code == 200:
                            data = res.json()
                            st.session_state["token"] = data.get("access_token") or data.get("token")
                            st.session_state["user"] = data.get("user")
                            st.session_state["current_page"] = "Dashboard"
                            st.success("✅ Login successful! Redirecting to Executive Dashboard...")
                            st.rerun()
                        else:
                            try:
                                err_msg = res.json().get("detail", "Invalid login credentials.")
                            except Exception:
                                err_msg = "Invalid login credentials."
                            st.error(f"❌ {err_msg}")
                    except Exception as ex:
                        st.error(f"❌ Unable to connect to authentication server at {API_URL}. Details: {ex}")

    with col2:
        st.markdown(
            """
            <div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 14px; padding: 22px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
                <div style="font-size: 1.1rem; font-weight: 700; color: #111827; margin-bottom: 8px;">💡 Demo User Credentials</div>
                <div style="font-size: 0.9rem; color: #111827; margin-bottom: 6px;"><b>Admin Account:</b> <code>admin@loanpredictor.com</code> / <code>admin123</code></div>
                <div style="font-size: 0.9rem; color: #111827; margin-bottom: 14px;"><b>Regular Account:</b> <code>user@example.com</code> / <code>user123</code></div>
                <div style="font-size: 0.85rem; color: #4B5563; margin-bottom: 12px;">Don't have an account? Click below to register a new account!</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📝 Create a New Account", use_container_width=True):
            st.session_state["current_page"] = "Register"
            st.rerun()

