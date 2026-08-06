import streamlit as st
import requests
import asyncio
from backend.config import settings
from backend.services.user_service import update_user_profile
from frontend.components.cards import render_banner, render_metric_card

def render():
    user = st.session_state.get("user")
    if not user:
        st.warning("Please log in to manage your profile.")
        return

    render_banner(
        title="User Profile & Security Management",
        subtitle="Manage your personal identity, financial parameters, and account credentials.",
        icon="👤"
    )

    token = st.session_state.get("token")
    user_id = str(user.get("_id") or user.get("id"))

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 🪪 Account Identity Card")
        render_metric_card("Full Name", user.get("name", "User"), "Verified Account Holder", "#1E3A8A", "👤")
        st.markdown("<br>", unsafe_allow_html=True)
        render_metric_card("Email Address", user.get("email", "user@example.com"), f"Role: {user.get('role', 'user').upper()}", "#16A34A", "📧")
        st.markdown("<br>", unsafe_allow_html=True)
        render_metric_card("Monthly Income", f"₹{float(user.get('monthly_income', 50000)):,.0f}", f"Occupation: {user.get('occupation', 'Salaried')}", "#F59E0B", "💳")

    with col2:
        st.markdown("### ✏️ Edit Profile Settings")
        with st.form("edit_profile_form"):
            new_name = st.text_input("Full Name", value=user.get("name", ""))
            new_phone = st.text_input("Phone Number", value=user.get("phone", ""))
            new_occ = st.selectbox("Occupation Category", ["Salaried", "Self-Employed", "Business", "Student", "Other"], index=0)
            new_inc = st.number_input("Monthly Income (₹)", value=float(user.get("monthly_income", 50000.0)))
            new_cibil = st.number_input("Target CIBIL Score", min_value=300, max_value=900, value=int(user.get("cibil_score", 720)))

            st.markdown("---")
            st.markdown("<h5 style='color: #111827;'>🔒 Security Settings (Optional)</h5>", unsafe_allow_html=True)
            curr_pass = st.text_input("Current Password", type="password", placeholder="Leave blank if unchanged")
            new_pass = st.text_input("New Password", type="password", placeholder="Leave blank if unchanged")

            submit = st.form_submit_button("💾 Save Profile Changes", use_container_width=True)

            if submit:
                payload = {
                    "name": new_name,
                    "phone": new_phone,
                    "occupation": new_occ,
                    "monthly_income": new_inc,
                    "cibil_score": new_cibil
                }
                if new_pass:
                    payload["current_password"] = curr_pass
                    payload["new_password"] = new_pass

                try:
                    try:
                        from frontend.config import API_URL
                    except ModuleNotFoundError:
                        from config import API_URL
                    headers = {"Authorization": f"Bearer {token}"} if token else {}
                    res = requests.put(f"{API_URL}/api/users/profile", json=payload, headers=headers, timeout=5)
                    if res.status_code == 200:
                        updated_user = res.json().get("user")
                        st.session_state["user"] = updated_user
                        st.success("✅ Profile updated successfully!")
                        st.rerun()
                    else:
                        err_msg = res.json().get("detail", "Update failed.")
                        st.error(f"❌ {err_msg}")
                except Exception:
                    try:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        res_obj = loop.run_until_complete(update_user_profile(user_id, payload))
                        st.session_state["user"] = res_obj.get("user")
                        st.success("✅ Profile updated successfully!")
                        st.rerun()
                    except Exception as ex:
                        st.error(f"❌ Profile update error: {ex}")
