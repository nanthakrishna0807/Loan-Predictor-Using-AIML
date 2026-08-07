import streamlit as st

try:
    from frontend.components.cards import render_banner
except ModuleNotFoundError:
    from components.cards import render_banner

def render():
    render_banner(
        title="About AI Loan Predictor Platform",
        subtitle="An intelligent machine learning platform designed to streamline automated credit approval, risk assessment, and financial scoring for modern fintech applications.",
        icon="ℹ️"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    is_dark = st.session_state.get("theme", "light") == "dark"
    card_bg = "#1E293B" if is_dark else "#FFFFFF"
    border_color = "#475569" if is_dark else "#CBD5E1"
    primary_title = "#60A5FA" if is_dark else "#1E3A8A"
    tech_bg = "#1E293B" if is_dark else "#F1F5F9"
    text_primary = "#FFFFFF" if is_dark else "#0F172A"
    text_secondary = "#E2E8F0" if is_dark else "#0F172A"

    # Project Overview & Architectural Pillars
    st.markdown(f"<h3 style='color: {text_primary} !important;'>🌟 Architectural Overview & Core Capabilities</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(
            f"""
            <div style="background-color: {card_bg}; border: 2px solid {border_color}; border-radius: 16px; padding: 24px; margin-bottom: 18px; box-shadow: 0 8px 20px rgba(0,0,0,0.06);">
                <div style="font-size: 1.25rem; font-weight: 800; color: {primary_title} !important; margin-bottom: 8px;">🤖 Gradient Boosting Machine Learning Engine</div>
                <div style="font-size: 1rem; line-height: 1.6; color: {text_secondary} !important; font-weight: 600;">
                    Utilizes a Scikit-learn Gradient Boosting Classifier trained on financial indicators. Delivers 95.0% validated accuracy in forecasting loan approval probability and classifying risk tiers under 25ms latency.
                </div>
            </div>
            <div style="background-color: {card_bg}; border: 2px solid {border_color}; border-radius: 16px; padding: 24px; box-shadow: 0 8px 20px rgba(0,0,0,0.06);">
                <div style="font-size: 1.25rem; font-weight: 800; color: {primary_title} !important; margin-bottom: 8px;">📈 Interactive CIBIL Estimator</div>
                <div style="font-size: 1rem; line-height: 1.6; color: {text_secondary} !important; font-weight: 600;">
                    Simulates credit score ratings (300 to 900) by weighting on-time payment history (35%), credit utilization (30%), history age (15%), credit mix (10%), and hard inquiry penalties (10%).
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div style="background-color: {card_bg}; border: 2px solid {border_color}; border-radius: 16px; padding: 24px; margin-bottom: 18px; box-shadow: 0 8px 20px rgba(0,0,0,0.06);">
                <div style="font-size: 1.25rem; font-weight: 800; color: {primary_title} !important; margin-bottom: 8px;">📊 DTI Ratio & Cashflow Diagnostics</div>
                <div style="font-size: 1rem; line-height: 1.6; color: {text_secondary} !important; font-weight: 600;">
                    Computes Debt-to-Income (DTI) ratios from existing liabilities and proposed EMIs. Prevents over-leveraging by establishing allowable credit limits and personalized financial tips.
                </div>
            </div>
            <div style="background-color: {card_bg}; border: 2px solid {border_color}; border-radius: 16px; padding: 24px; box-shadow: 0 8px 20px rgba(0,0,0,0.06);">
                <div style="font-size: 1.25rem; font-weight: 800; color: {primary_title} !important; margin-bottom: 8px;">⚡ Async Microservices Architecture</div>
                <div style="font-size: 1rem; line-height: 1.6; color: {text_secondary} !important; font-weight: 600;">
                    Powered by FastAPI async REST endpoints, Motor MongoDB Atlas cloud driver, Pydantic v2 validation, and responsive Glassmorphism Streamlit UI components.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # Technologies Used
    st.markdown(f"<h3 style='color: {text_primary} !important;'>🛠️ Technologies Used</h3>", unsafe_allow_html=True)

    t1, t2, t3, t4, t5 = st.columns(5)
    with t1:
        st.markdown(
            f"""
            <div style="background-color: {tech_bg}; border: 2px solid {border_color}; border-radius: 14px; padding: 20px 14px; text-align: center;">
                <div style="font-size: 2.3rem;">🐍</div>
                <div style="font-weight: 800; color: {primary_title} !important; margin-top: 6px;">Python</div>
                <div style="font-size: 0.85rem; color: {text_secondary} !important; font-weight: 700;">Core Language</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with t2:
        st.markdown(
            f"""
            <div style="background-color: {tech_bg}; border: 2px solid {border_color}; border-radius: 14px; padding: 20px 14px; text-align: center;">
                <div style="font-size: 2.3rem;">👑</div>
                <div style="font-weight: 800; color: {primary_title} !important; margin-top: 6px;">Streamlit</div>
                <div style="font-size: 0.85rem; color: {text_secondary} !important; font-weight: 700;">Interactive UI</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with t3:
        st.markdown(
            f"""
            <div style="background-color: {tech_bg}; border: 2px solid {border_color}; border-radius: 14px; padding: 20px 14px; text-align: center;">
                <div style="font-size: 2.3rem;">⚡</div>
                <div style="font-weight: 800; color: {primary_title} !important; margin-top: 6px;">FastAPI</div>
                <div style="font-size: 0.85rem; color: {text_secondary} !important; font-weight: 700;">Async REST API</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with t4:
        st.markdown(
            f"""
            <div style="background-color: {tech_bg}; border: 2px solid {border_color}; border-radius: 14px; padding: 20px 14px; text-align: center;">
                <div style="font-size: 2.3rem;">🤖</div>
                <div style="font-weight: 800; color: {primary_title} !important; margin-top: 6px;">Scikit-learn</div>
                <div style="font-size: 0.85rem; color: {text_secondary} !important; font-weight: 700;">Machine Learning</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with t5:
        st.markdown(
            f"""
            <div style="background-color: {tech_bg}; border: 2px solid {border_color}; border-radius: 14px; padding: 20px 14px; text-align: center;">
                <div style="font-size: 2.3rem;">🗄️</div>
                <div style="font-weight: 800; color: {primary_title} !important; margin-top: 6px;">MongoDB</div>
                <div style="font-size: 0.85rem; color: {text_secondary} !important; font-weight: 700;">Atlas Database</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # Machine Learning Workflow
    st.markdown(f"<h3 style='color: {text_primary} !important;'>🔄 Machine Learning Workflow</h3>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="background-color: {card_bg}; border: 2px solid {border_color}; border-radius: 16px; padding: 28px;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px; text-align: center;">
                <div style="flex: 1; min-width: 140px;">
                    <div style="font-size: 2.2rem;">👤</div>
                    <div style="font-weight: 800; color: {text_primary} !important; margin-top: 6px;">1. Applicant Data</div>
                    <div style="font-size: 0.88rem; color: {text_secondary} !important; font-weight: 600;">Income, Liabilities & CIBIL</div>
                </div>
                <div style="font-size: 1.6rem; font-weight: 800; color: {primary_title} !important;">➡️</div>
                <div style="flex: 1; min-width: 140px;">
                    <div style="font-size: 2.2rem;">⚙️</div>
                    <div style="font-weight: 800; color: {text_primary} !important; margin-top: 6px;">2. Preprocessing</div>
                    <div style="font-size: 0.88rem; color: {text_secondary} !important; font-weight: 600;">Standard Scaling & DTI</div>
                </div>
                <div style="font-size: 1.6rem; font-weight: 800; color: {primary_title} !important;">➡️</div>
                <div style="flex: 1; min-width: 140px;">
                    <div style="font-size: 2.2rem;">🤖</div>
                    <div style="font-weight: 800; color: {text_primary} !important; margin-top: 6px;">3. Model Inference</div>
                    <div style="font-size: 0.88rem; color: {text_secondary} !important; font-weight: 600;">Gradient Boosting</div>
                </div>
                <div style="font-size: 1.6rem; font-weight: 800; color: {primary_title} !important;">➡️</div>
                <div style="flex: 1; min-width: 140px;">
                    <div style="font-size: 2.2rem;">📊</div>
                    <div style="font-weight: 800; color: {text_primary} !important; margin-top: 6px;">4. Decision & Tips</div>
                    <div style="font-size: 0.88rem; color: {text_secondary} !important; font-weight: 600;">Approval, EMI & Advisory</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # Explicit Back to Home button on page
    if st.button("🏠 Back to Home", key="about_back_home", use_container_width=True):
        st.session_state["current_page"] = "Home"
        st.rerun()
