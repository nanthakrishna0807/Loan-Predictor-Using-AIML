import streamlit as st
import os
import sys

# Ensure root directory and frontend directory are in python path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

# Session State Initialization
st.session_state.setdefault("current_page", "Home")
st.session_state.setdefault("theme", "light")
st.session_state.setdefault("startup_done", False)
st.session_state["_header_bar_rendered"] = False

try:
    from frontend.components.theme import apply_banking_theme, render_top_header_bar
    from frontend.components.sidebar import render_sidebar
    from frontend.components.loading import render_loading_screen
    from frontend.components.cards import render_banner, render_metric_card
    from frontend.LoanPrediction import render as render_loan_pred
    from frontend.CibilCalculatorPage import render as render_cibil_calc
    from frontend.About import render as render_about
    from frontend.Contact import render as render_developer
    from frontend.AdminDashboard import render as render_admin
    from frontend.Login import render as render_login
    from frontend.Register import render as render_register
    from frontend.Dashboard import render as render_user_dashboard
    from frontend.PredictionHistory import render as render_history
    from frontend.Profile import render as render_profile
except ModuleNotFoundError:
    from components.theme import apply_banking_theme, render_top_header_bar
    from components.sidebar import render_sidebar
    from components.loading import render_loading_screen
    from components.cards import render_banner, render_metric_card
    from LoanPrediction import render as render_loan_pred
    from CibilCalculatorPage import render as render_cibil_calc
    from About import render as render_about
    from Contact import render as render_developer
    from AdminDashboard import render as render_admin
    from Login import render as render_login
    from Register import render as render_register
    from Dashboard import render as render_user_dashboard
    from PredictionHistory import render as render_history
    from Profile import render as render_profile

st.set_page_config(
    page_title="AI Loan Predictor | Enterprise Banking Platform",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Active Light/Dark Theme CSS
apply_banking_theme()

# Page Name Constants
PAGE_HOME        = "Home"
PAGE_LOAN_PRED   = "LoanPrediction"
PAGE_CIBIL       = "CibilCalculator"
PAGE_ABOUT       = "About"
PAGE_DEVELOPER   = "Developer"
PAGE_ADMIN       = "AdminDashboard"
PAGE_LOGIN       = "Login"
PAGE_REGISTER    = "Register"
PAGE_DASHBOARD   = "Dashboard"
PAGE_HISTORY     = "PredictionHistory"
PAGE_PROFILE     = "Profile"

# Top Header Bar & Sidebar Navigation
render_top_header_bar()
render_sidebar()

# Main Home View
def render_home_page():
    render_banner(
        title="Royal Banking AI Credit Assessment Platform",
        subtitle="Automated loan prediction, risk evaluation, and CIBIL score calculation using Scikit-learn Gradient Boosting machine learning engine.",
        icon="🏦"
    )

    is_dark = st.session_state.get("theme", "light") == "dark"
    card_bg = "#1E293B" if is_dark else "#FFFFFF"
    border_color = "#475569" if is_dark else "#CBD5E1"
    text_primary = "#FFFFFF" if is_dark else "#0F172A"
    text_secondary = "#E2E8F0" if is_dark else "#0F172A"
    title_color = "#60A5FA" if is_dark else "#1E3A8A"

    # KPI Metric Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_metric_card("Model Accuracy", "95.0%", "Gradient Boosting Engine", "#16A34A", "🎯")
    with col2:
        render_metric_card("CIBIL Benchmark", "750+", "Prime Credit Rating Tier", "#1E3A8A", "📈")
    with col3:
        render_metric_card("Inference Latency", "< 25 ms", "Real-Time AI Predictions", "#2563EB", "⚡")
    with col4:
        render_metric_card("Database Cluster", "MongoDB Atlas", "Motor Async Driver Active", "#0EA5E9", "🗄️")

    st.markdown("<br>", unsafe_allow_html=True)

    # Modern Banking Visual Banner
    st.markdown(
        f"""
        <div style="background-color: {card_bg}; border: 2px solid {border_color}; border-radius: 18px; padding: 28px 32px; margin-bottom: 24px; box-shadow: 0 10px 25px rgba(0,0,0,0.06); display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 20px;">
            <div style="flex: 1; min-width: 280px;">
                <div style="font-size: 0.95rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; color: {title_color} !important; margin-bottom: 6px;">AUTOMATED CREDIT INTELLIGENCE</div>
                <h2 style="margin: 0; font-size: 1.85rem; font-weight: 800; color: {text_primary} !important;">Welcome to AI Loan Assessment</h2>
                <p style="font-size: 1.1rem; margin-top: 10px; line-height: 1.6; color: {text_secondary} !important; font-weight: 600;">
                    Evaluate applicant financial indicators instantly. Calculate loan approval probability %, debt-to-income (DTI) caps, credit risk levels, and CIBIL score ratings with AI precision.
                </p>
            </div>
            <div style="background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%); color: #FFFFFF; width: 100px; height: 100px; border-radius: 20px; display: flex; align-items: center; justify-content: center; font-size: 3.5rem; box-shadow: 0 10px 24px rgba(37, 99, 235, 0.35);">
                💳
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(f"<h3 style='color: {text_primary} !important;'>🌟 Key Feature Set</h3>", unsafe_allow_html=True)
    
    st.markdown(
        f"""
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 18px; margin-top: 14px; margin-bottom: 28px;">
            <div class="enterprise-card">
                <div class="card-title-text">🤖 Gradient Boosting Model</div>
                <div class="card-body-text">Predicts loan approval probability based on monthly income, existing EMIs, DTI ratio, and credit history variables.</div>
            </div>
            <div class="enterprise-card">
                <div class="card-title-text">📈 CIBIL Score Estimator</div>
                <div class="card-body-text">Simulates credit score ratings (300 to 900) based on payment history, utilization ratio, credit age, and hard inquiries.</div>
            </div>
            <div class="enterprise-card">
                <div class="card-title-text">📊 Risk & Cashflow Diagnostics</div>
                <div class="card-body-text">Computes Debt-to-Income (DTI) ratio, recommends allowable loan ceilings, estimates monthly EMIs, and provides risk tips.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.markdown(f"<h3 style='text-align: center; margin-bottom: 20px; color: {text_primary} !important;'>🚀 Get Started Now</h3>", unsafe_allow_html=True)

    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("📝 Run New Loan Prediction Assessment", key="home_nav_pred_btn", use_container_width=True):
            st.session_state["current_page"] = PAGE_LOAN_PRED
            st.rerun()
    with btn_col2:
        if st.button("📈 Calculate CIBIL Score", key="home_nav_cibil_btn", use_container_width=True):
            st.session_state["current_page"] = PAGE_CIBIL
            st.rerun()

# Router Execution
selected_page = st.session_state.get("current_page", PAGE_HOME)

if not st.session_state.get("startup_done", False):
    render_loading_screen()
    st.rerun()

ROUTES = {
    PAGE_HOME:      render_home_page,
    PAGE_LOAN_PRED: render_loan_pred,
    PAGE_CIBIL:     render_cibil_calc,
    PAGE_ABOUT:     render_about,
    PAGE_DEVELOPER: render_developer,
    PAGE_ADMIN:     render_admin,
    PAGE_LOGIN:     render_login,
    PAGE_REGISTER:  render_register,
    PAGE_DASHBOARD: render_user_dashboard,
    PAGE_HISTORY:   render_history,
    PAGE_PROFILE:   render_profile,
}

render_view = ROUTES.get(selected_page, render_home_page)
render_view()
