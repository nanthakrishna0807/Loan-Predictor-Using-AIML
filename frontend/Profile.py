import streamlit as st

try:
    from frontend.components.cards import render_banner, render_metric_card
    from frontend.services.user_service import get_user_profile, update_user_profile
except ModuleNotFoundError:
    from components.cards import render_banner, render_metric_card
    from services.user_service import get_user_profile, update_user_profile

def render():
    user = st.session_state.get("user")
    if not user:
        st.info("🔐 Please log in to manage your user profile.")
        if st.button("🔑 Account Login", key="profile_login_btn", use_container_width=True):
            st.session_state["current_page"] = "Login"
            st.rerun()
        return

    is_dark = st.session_state.get("theme", "light") == "dark"
    text_color = "#FFFFFF" if is_dark else "#0F172A"

    render_banner(
        title="User Profile & Account Management",
        subtitle="Manage your personal identity, account security credentials, and view membership stats.",
        icon="👤"
    )

    # Fetch fresh profile from user service
    success, prof_data, err = get_user_profile()
    if not success:
        prof_data = user
    else:
        st.session_state["user"] = prof_data

    name = prof_data.get("name", "User")
    email = prof_data.get("email", "user@example.com")
    role = prof_data.get("role", "user").upper()
    joined_date = prof_data.get("joined_date", prof_data.get("createdAt", "N/A")[:10])
    pred_count = prof_data.get("prediction_count", 0)

    col1, col2 = st.columns([1, 1], gap="medium")

    with col1:
        st.markdown(f"<h3 style='color: {text_color} !important;'>🪪 Account Identity</h3>", unsafe_allow_html=True)
        render_metric_card("Full Name", name, "Verified Profile", "#1E3A8A", "👤")
        st.markdown("<br>", unsafe_allow_html=True)
        render_metric_card("Email Address", email, f"Role: {role}", "#16A34A", "📧")
        st.markdown("<br>", unsafe_allow_html=True)
        render_metric_card("Total Predictions", str(pred_count), f"Joined: {joined_date}", "#0EA5E9", "📊")

    with col2:
        st.markdown(f"<h3 style='color: {text_color} !important;'>✏️ Update Profile</h3>", unsafe_allow_html=True)
        with st.form("edit_profile_form"):
            new_name = st.text_input("Full Name", value=name)
            st.text_input("Email Address (Read-Only)", value=email, disabled=True)

            st.markdown("---")
            st.markdown(f"<h5 style='color: {text_color} !important;'>🔒 Update Password (Optional)</h5>", unsafe_allow_html=True)
            new_pass = st.text_input("New Password", type="password", placeholder="Leave blank to keep current password")
            confirm_pass = st.text_input("Confirm New Password", type="password", placeholder="Re-enter new password")

            submit = st.form_submit_button("💾 Save Profile Changes", use_container_width=True)

            if submit:
                if new_pass and new_pass != confirm_pass:
                    st.toast("⚠️ New passwords do not match.", icon="⚠️")
                    st.error("New passwords do not match.")
                else:
                    success_upd, updated_obj, err_upd = update_user_profile(name=new_name, password=new_pass if new_pass else None)
                    if success_upd:
                        st.session_state["user"] = updated_obj
                        st.toast("✅ Profile updated successfully!", icon="🎉")
                        st.success("✅ Profile updated successfully!")
                        st.rerun()
                    else:
                        st.toast(f"❌ Error updating profile: {err_upd}", icon="🚨")
                        st.error(f"❌ Error updating profile: {err_upd}")
