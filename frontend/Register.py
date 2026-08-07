import streamlit as st

try:
    from frontend.services.auth_service import register
except ModuleNotFoundError:
    from services.auth_service import register

def render():
    is_dark = st.session_state.get("theme", "light") == "dark"
    text_color = "#FFFFFF" if is_dark else "#0F172A"
    sub_color = "#94A3B8" if is_dark else "#475569"

    st.markdown(f"<h2 style='color: {text_color} !important;'>📝 Create New Account</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: {sub_color} !important; font-size: 0.95rem;'>Register to store prediction reports and manage your credit score profile.</p>", unsafe_allow_html=True)

    with st.form("register_enterprise_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name *", placeholder="John Doe")
            email = st.text_input("Email Address *", placeholder="john@example.com")
            password = st.text_input("Password *", type="password", placeholder="••••••••")
            confirm_password = st.text_input("Confirm Password *", type="password", placeholder="••••••••")

        with col2:
            phone = st.text_input("Phone Number", placeholder="+91 9876543210")
            occupation = st.selectbox("Occupation Category", ["Salaried", "Self-Employed", "Business Owner", "Student", "Other"])
            role = st.selectbox("Account Role", ["user", "admin"], index=0)

        st.markdown("<br>", unsafe_allow_html=True)
        btn_c1, btn_c2 = st.columns(2)
        with btn_c1:
            submit = st.form_submit_button("Register Account", use_container_width=True)
        with btn_c2:
            back_btn = st.form_submit_button("Back to Login", use_container_width=True)

        if back_btn:
            st.session_state["current_page"] = "Login"
            st.rerun()

        if submit:
            if not name or not email or not password or not confirm_password:
                st.toast("⚠️ Please fill in all required fields marked with *.", icon="⚠️")
                st.error("Please fill in all required fields marked with *.")
            elif password != confirm_password:
                st.toast("⚠️ Passwords do not match.", icon="⚠️")
                st.error("Passwords do not match. Please ensure both password fields are identical.")
            else:
                success, res, err = register(name, email, password, role, phone, occupation)
                if success:
                    st.toast("🎉 Account created successfully! Please sign in.", icon="🎉")
                    st.success("🎉 Account created successfully! Redirecting to login...")
                    st.session_state["current_page"] = "Login"
                    st.rerun()
                else:
                    st.toast(f"❌ Registration failed: {err}", icon="🚨")
                    st.error(f"❌ Registration failed: {err}")
