import streamlit as st

try:
    from frontend.services.auth_service import login
except ModuleNotFoundError:
    from services.auth_service import login

def render():
    is_dark = st.session_state.get("theme", "light") == "dark"
    card_bg = "#1E293B" if is_dark else "#FFFFFF"
    border_c = "#334155" if is_dark else "#CBD5E1"
    text_color = "#FFFFFF" if is_dark else "#0F172A"
    sub_color = "#94A3B8" if is_dark else "#475569"

    st.markdown(f"<h2 style='color: {text_color} !important;'>🔑 Enterprise User Authentication</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: {sub_color} !important; font-size: 0.95rem;'>Sign in to access your loan predictions, credit history, and analytics dashboard.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1], gap="medium")

    with col1:
        with st.form("login_enterprise_form"):
            st.markdown(f"<h4 style='color: {text_color} !important;'>Sign In to Your Account</h4>", unsafe_allow_html=True)
            email = st.text_input("Email Address *", placeholder="user@example.com")
            password = st.text_input("Password *", type="password", placeholder="••••••••")
            
            b_col1, b_col2 = st.columns(2)
            with b_col1:
                submit = st.form_submit_button("Sign In to Portal", use_container_width=True)
            with b_col2:
                reg_nav_btn = st.form_submit_button("Register New Account", use_container_width=True)

            if reg_nav_btn:
                st.session_state["current_page"] = "Register"
                st.rerun()

            if submit:
                if not email or not password:
                    st.toast("⚠️ Please enter both email address and password.", icon="⚠️")
                    st.error("Please enter both email address and password.")
                else:
                    success, res, err = login(email, password)
                    if success:
                        st.toast("✅ Login successful!", icon="🎉")
                        user_role = st.session_state.get("role", "user")
                        if user_role == "admin":
                            st.session_state["current_page"] = "AdminDashboard"
                        else:
                            st.session_state["current_page"] = "Dashboard"
                        st.rerun()
                    else:
                        st.toast(f"❌ Login failed: {err}", icon="🚨")
                        st.error(f"❌ Login failed: {err}")

    with col2:
        st.markdown(
            f"""
            <div style="background: {card_bg}; border: 2px solid {border_c}; border-radius: 16px; padding: 24px; box-shadow: 0 4px 12px rgba(0,0,0,0.06);">
                <div style="font-size: 1.1rem; font-weight: 800; color: {text_color} !important; margin-bottom: 12px;">🛡️ Secure Portal Access</div>
                <p style="font-size: 0.95rem; color: {sub_color} !important; margin-bottom: 16px; line-height: 1.6;">
                    Log in with your registered user credentials or admin account to view live credit reports, real-time MongoDB analytics, and past loan applications.
                </p>
                <div style="font-size: 0.85rem; color: {sub_color} !important; margin-bottom: 14px;">Don't have an account yet? Click Register above!</div>
            </div>
            """,
            unsafe_allow_html=True
        )
