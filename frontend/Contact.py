import streamlit as st

try:
    from frontend.components.cards import render_banner
except ModuleNotFoundError:
    from components.cards import render_banner

def render():
    render_banner(
        title="Developer Profile",
        subtitle="Meet the developer behind AI Loan Predictor. Learn more about the technology stack, project architecture, and repository links.",
        icon="👨‍💻"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    is_dark = st.session_state.get("theme", "light") == "dark"
    card_bg = "#1E293B" if is_dark else "#FFFFFF"
    border_color = "#475569" if is_dark else "#CBD5E1"
    primary_title = "#60A5FA" if is_dark else "#1E3A8A"
    text_primary = "#FFFFFF" if is_dark else "#0F172A"
    text_secondary = "#E2E8F0" if is_dark else "#0F172A"

    col1, col2 = st.columns([1.2, 1], gap="large")

    with col1:
        st.markdown(
            f"""
            <div style="background-color: {card_bg}; border: 2px solid {border_color}; border-radius: 18px; padding: 30px; box-shadow: 0 10px 25px rgba(0,0,0,0.08);">
                <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 22px;">
                    <div style="background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%); color: #FFFFFF; font-size: 2.5rem; width: 76px; height: 76px; border-radius: 18px; display: flex; align-items: center; justify-content: center; font-weight: 800; box-shadow: 0 8px 20px rgba(37, 99, 235, 0.35);">
                        👨‍💻
                    </div>
                    <div>
                        <div style="font-size: 1.85rem; font-weight: 800; line-height: 1.2; color: {text_primary} !important;">Nantha Krishna V</div>
                        <div style="font-size: 1.15rem; font-weight: 800; color: {primary_title} !important; margin-top: 4px;">B.Tech Information Technology</div>
                        <div style="font-size: 1rem; font-weight: 700; color: {text_secondary} !important;">Jeppiaar Institute of Technology</div>
                    </div>
                </div>
                <hr style="border: 0; border-top: 2px solid {border_color}; margin: 22px 0;">
                <div style="font-size: 1.05rem; line-height: 1.65; color: {text_secondary} !important; font-weight: 600;">
                    Full-Stack Software Engineer & Machine Learning Practitioner specializing in Python microservices, FastAPI REST APIs, Scikit-learn Machine Learning pipelines, and interactive Streamlit web architectures. Designed and built this enterprise AI Loan Assessment platform.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div style="display: flex; flex-direction: column; gap: 16px;">
                <a href="https://github.com/nanthakrishna0807" target="_blank" style="text-decoration: none;">
                    <div style="background-color: {card_bg}; border: 2px solid {border_color}; border-radius: 16px; padding: 22px; display: flex; align-items: center; gap: 18px; box-shadow: 0 6px 16px rgba(0,0,0,0.04); transition: transform 0.25s ease;">
                        <div style="font-size: 2.2rem;">🐙</div>
                        <div>
                            <div style="font-weight: 800; font-size: 1.2rem; color: {primary_title} !important;">GitHub Profile</div>
                            <div style="font-size: 0.95rem; color: {text_secondary} !important; font-weight: 700;">github.com/nanthakrishna0807</div>
                        </div>
                    </div>
                </a>

                <a href="https://linkedin.com" target="_blank" style="text-decoration: none;">
                    <div style="background-color: {card_bg}; border: 2px solid {border_color}; border-radius: 16px; padding: 22px; display: flex; align-items: center; gap: 18px; box-shadow: 0 6px 16px rgba(0,0,0,0.04); transition: transform 0.25s ease;">
                        <div style="font-size: 2.2rem;">💼</div>
                        <div>
                            <div style="font-weight: 800; font-size: 1.2rem; color: {primary_title} !important;">LinkedIn Profile</div>
                            <div style="font-size: 0.95rem; color: {text_secondary} !important; font-weight: 700;">Connect on LinkedIn</div>
                        </div>
                    </div>
                </a>

                <a href="mailto:nanthakrishna0807@example.com" style="text-decoration: none;">
                    <div style="background-color: {card_bg}; border: 2px solid {border_color}; border-radius: 16px; padding: 22px; display: flex; align-items: center; gap: 18px; box-shadow: 0 6px 16px rgba(0,0,0,0.04); transition: transform 0.25s ease;">
                        <div style="font-size: 2.2rem;">✉️</div>
                        <div>
                            <div style="font-weight: 800; font-size: 1.2rem; color: {primary_title} !important;">Email Contact</div>
                            <div style="font-size: 0.95rem; color: {text_secondary} !important; font-weight: 700;">Send an inquiry email</div>
                        </div>
                    </div>
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # Explicit Back to Home button on page
    if st.button("🏠 Back to Home", key="dev_back_home", use_container_width=True):
        st.session_state["current_page"] = "Home"
        st.rerun()
