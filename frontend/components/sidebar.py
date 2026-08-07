import streamlit as st
try:
    from frontend.services.auth_service import logout
except ModuleNotFoundError:
    from services.auth_service import logout


def render_sidebar():
    """
    Renders sidebar navigation, user session info, theme control radio, and logout button.
    Enforces role-based navigation item visibility.
    """
    current_page = st.session_state.get("current_page", "Home")
    current_theme = st.session_state.get("theme", "light")
    user_session = st.session_state.get("user")
    role_session = (st.session_state.get("role") or (user_session.get("role") if user_session else "") or "").lower()

    with st.sidebar:
        st.markdown(
            """
            <div style="display: flex; align-items: center; gap: 14px; margin-bottom: 16px; padding: 4px;">
                <div style="background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%); color: #FFFFFF; font-size: 1.8rem; width: 52px; height: 52px; border-radius: 14px; display: flex; align-items: center; justify-content: center; font-weight: 800; box-shadow: 0 6px 16px rgba(59, 130, 246, 0.35);">
                    🏦
                </div>
                <div>
                    <div style="font-size: 1.3rem; font-weight: 800; line-height: 1.1; letter-spacing: -0.02em;">AI Loan Predictor</div>
                    <div style="font-size: 0.8rem; font-weight: 700; color: #1E3A8A;">Enterprise Credit Portal</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("---")

        # User Profile / Auth Status in Sidebar
        if user_session:
            role_disp = role_session.upper()
            st.markdown(
                f"""
                <div style="background: rgba(30, 58, 138, 0.1); border-radius: 12px; padding: 12px 14px; margin-bottom: 14px; border: 1px solid rgba(59, 130, 246, 0.3);">
                    <div style="font-size: 0.85rem; font-weight: 700; color: #3B82F6;">👤 LOGGED IN AS</div>
                    <div style="font-size: 1rem; font-weight: 800; margin-top: 2px;">{user_session.get('name', 'User')}</div>
                    <div style="font-size: 0.75rem; color: #64748B;">{user_session.get('email', '')} | <b>{role_disp}</b></div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div style="background: rgba(100, 116, 139, 0.1); border-radius: 12px; padding: 10px 14px; margin-bottom: 14px; border: 1px solid rgba(100, 116, 139, 0.2);">
                    <div style="font-size: 0.8rem; font-weight: 700; color: #64748B;">🔓 GUEST SESSION</div>
                    <div style="font-size: 0.85rem; margin-top: 2px;">Sign in to access your portal</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Sidebar Theme Switcher Radio
        st.markdown("<b style='font-size: 1rem;'>🎨 Theme Control</b>", unsafe_allow_html=True)
        theme_option = st.radio(
            "Theme Control Radio",
            ["☀️ Light Mode", "🌙 Dark Mode"],
            index=0 if current_theme == "light" else 1,
            key="sidebar_theme_radio",
            label_visibility="collapsed",
            horizontal=True
        )

        new_theme = "dark" if "Dark" in theme_option else "light"
        if current_theme != new_theme:
            st.session_state["theme"] = new_theme
            st.rerun()

        st.markdown("---")
        st.markdown("<b style='font-size: 1rem;'>🧭 Navigation Menu</b>", unsafe_allow_html=True)

        # Dynamic Navigation List based on session state & role
        nav_items = [("🏠 Home", "Home")]

        if user_session:
            if role_session == "admin":
                nav_items.append(("🛡️ Admin Dashboard", "AdminDashboard"))
            else:
                nav_items.append(("👤 User Dashboard", "Dashboard"))
                nav_items.append(("📝 Loan Prediction", "LoanPrediction"))
                nav_items.append(("📈 CIBIL Calculator", "CibilCalculator"))
                nav_items.append(("📜 Prediction History", "PredictionHistory"))
                nav_items.append(("⚙️ Profile Settings", "Profile"))
        else:
            nav_items.append(("📝 Loan Prediction", "LoanPrediction"))
            nav_items.append(("📈 CIBIL Calculator", "CibilCalculator"))
            nav_items.append(("🔑 Account Login", "Login"))
            nav_items.append(("📝 Register Account", "Register"))
            nav_items.append(("🛡️ Admin Control", "AdminDashboard"))

        nav_items.append(("ℹ️ About Project", "About"))
        nav_items.append(("👨‍💻 Developer", "Developer"))

        for label, page_key in nav_items:
            is_active = (current_page == page_key)
            display_label = f"👉 {label}" if is_active else label
            
            if st.button(display_label, key=f"sidebar_nav_{page_key}", use_container_width=True):
                if current_page != page_key:
                    st.session_state["current_page"] = page_key
                    st.rerun()

        # Logout Button if user is logged in
        if user_session:
            st.markdown("---")
            if st.button("🚪 Sign Out", key="sidebar_logout_btn", use_container_width=True):
                logout()
                st.toast("👋 Logged out successfully.", icon="🚪")
                st.session_state["current_page"] = "Home"
                st.rerun()
