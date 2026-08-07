import streamlit as st

def render_top_navbar():
    """
    Renders top header navbar with app brand logo and theme toggle.
    Guards against duplicate rendering per Streamlit run loop.
    """
    if st.session_state.get("_header_bar_rendered", False):
        return

    is_dark = st.session_state.get("theme", "light") == "dark"
    current_page = st.session_state.get("current_page", "Home")
    toggle_label = "☀️ Switch to Light Mode" if is_dark else "🌙 Switch to Dark Mode"

    col_brand, col_toggle = st.columns([3, 1])

    with col_brand:
        st.markdown(
            """
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                <div style="font-size: 2.2rem;">🏦</div>
                <div>
                    <div style="font-size: 1.35rem; font-weight: 800; line-height: 1.1; letter-spacing: -0.02em;">AI Loan Predictor</div>
                    <div style="font-size: 0.8rem; font-weight: 700; color: #1E3A8A;">Enterprise Banking Intelligence</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_toggle:
        if st.button(toggle_label, key=f"top_navbar_toggle_{current_page}", use_container_width=True):
            st.session_state["theme"] = "light" if is_dark else "dark"
            st.session_state["_header_bar_rendered"] = True
            st.rerun()

    st.markdown("<hr style='margin: 8px 0 20px 0; border: none; border-top: 1px solid rgba(148, 163, 184, 0.25);'>", unsafe_allow_html=True)
    st.session_state["_header_bar_rendered"] = True
