import streamlit as st
import requests
import asyncio
from backend.config import settings
from backend.services.auth_service import register_user

def render():
    st.markdown("<h2 style='color: #111827;'>📝 Create New Account</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #4B5563; font-size: 0.95rem;'>Register to store prediction reports and manage your credit score profile.</p>", unsafe_allow_html=True)

    with st.form("register_enterprise_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name *", placeholder="John Doe")
            email = st.text_input("Email Address *", placeholder="john@example.com")
            password = st.text_input("Password *", type="password", placeholder="••••••••")
            role = st.selectbox("Account Role", ["user", "admin"])

        with col2:
            phone = st.text_input("Phone Number", placeholder="+91 9876543210")
            occupation = st.selectbox("Occupation Category", ["Salaried", "Self-Employed", "Business Owner", "Student", "Other"])
            income = st.number_input("Monthly Income (₹)", min_value=0.0, value=50000.0, step=5000.0)

        submit = st.form_submit_button("Create Account & Access Portal", use_container_width=True)

        if submit:
            if not name or not email or not password:
                st.error("Please fill in all required fields marked with *.")
                return

            payload = {
                "name": name,
                "email": email,
                "password": password,
                "role": role,
                "phone": phone,
                "occupation": occupation,
                "monthly_income": income
            }

            try:
                try:
                    from frontend.config import API_URL
                except ModuleNotFoundError:
                    from config import API_URL
                backend_url = f"{API_URL}/api/auth/register"
                res = requests.post(backend_url, json=payload, timeout=5)
                
                if res.status_code == 200:
                    data = res.json()
                    st.session_state["token"] = data.get("access_token") or data.get("token")
                    st.session_state["user"] = data.get("user")
                    st.success("🎉 Account created successfully!")
                    st.rerun()
                else:
                    err_msg = res.json().get("detail", "Registration failed.")
                    st.error(f"❌ {err_msg}")
            except Exception:
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    data = loop.run_until_complete(register_user(payload))
                    st.session_state["token"] = data.get("access_token") or data.get("token")
                    st.session_state["user"] = data.get("user")
                    st.success("🎉 Account created successfully!")
                    st.rerun()
                except Exception as ex:
                    st.error(f"❌ Registration error: {ex}")
