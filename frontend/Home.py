import streamlit as st
import os
import sys

# Ensure backend app & frontend modules are in python path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from frontend.components.theme import apply_banking_theme
from frontend.components.cards import render_banner, render_metric_card

st.set_page_config(
    page_title="AI Loan Predictor | Enterprise Credit Assessment Portal",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_banking_theme()

# Initialize session state
if "token" not in st.session_state:
    st.session_state["token"] = None
if "user" not in st.session_state:
    st.session_state["user"] = None
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Home"

# Sidebar Navigation (Crisp White Background, Dark #111827 Typography)
with st.sidebar:
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
            <div style="background-color: #1E3A8A; color: #FFFFFF; font-size: 1.5rem; width: 44px; height: 44px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-weight: 800;">
                🏦
            </div>
            <div>
                <div style="font-size: 1.1rem; font-weight: 800; color: #111827; line-height: 1.2;">AI Loan Predictor</div>
                <div style="font-size: 0.75rem; color: #4B5563; font-weight: 600;">Enterprise Fintech Portal</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")

    user = st.session_state.get("user")
    is_logged_in = user is not None
    is_admin = is_logged_in and user.get("role") == "admin"

    # User Profile Card in Sidebar
    if is_logged_in:
        st.markdown(
            f"""
            <div style="background-color: #F8FAFC; border: 1px solid #E5E7EB; border-radius: 12px; padding: 14px; margin-bottom: 16px;">
                <div style="font-size: 0.8rem; color: #4B5563; font-weight: 700; text-transform: uppercase;">CURRENT USER</div>
                <div style="font-size: 1rem; font-weight: 700; color: #111827; margin-top: 2px;">{user.get('name')}</div>
                <div style="font-size: 0.825rem; color: #4B5563; word-break: break-all;">{user.get('email')}</div>
                <div style="display: inline-block; background-color: #EEF4FF; color: #1E3A8A; font-weight: 700; font-size: 0.75rem; padding: 2px 8px; border-radius: 6px; margin-top: 6px;">
                    ROLE: {user.get('role', 'user').upper()}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    nav_options = ["🏠 Home"]
    if is_logged_in:
        nav_options.extend(["📊 Dashboard", "📝 New Loan Prediction", "📜 Prediction History", "👤 My Profile"])
        if is_admin:
            nav_options.append("🛡️ Admin Dashboard")
        nav_options.append("🚪 Logout")
    else:
        nav_options.extend(["🔑 Login", "📝 Register", "📝 Quick Prediction Form"])

    choice = st.radio("Enterprise Navigation", nav_options, index=0)

    if choice == "🚪 Logout":
        st.session_state["token"] = None
        st.session_state["user"] = None
        st.session_state["current_page"] = "Home"
        st.rerun()

    page_map = {
        "🏠 Home": "Home",
        "🔑 Login": "Login",
        "📝 Register": "Register",
        "📊 Dashboard": "Dashboard",
        "📝 New Loan Prediction": "LoanPrediction",
        "📝 Quick Prediction Form": "LoanPrediction",
        "📜 Prediction History": "PredictionHistory",
        "👤 My Profile": "Profile",
        "🛡️ Admin Dashboard": "AdminDashboard"
    }

    selected_page = page_map.get(choice, "Home")

# Main Page Content Routing
if selected_page == "Login":
    import frontend.Login as LoginModule
    LoginModule.render()
elif selected_page == "Register":
    import frontend.Register as RegisterModule
    RegisterModule.render()
elif selected_page == "Dashboard":
    import frontend.Dashboard as DashboardModule
    DashboardModule.render()
elif selected_page == "LoanPrediction":
    import frontend.LoanPrediction as LoanPredModule
    LoanPredModule.render()
elif selected_page == "PredictionHistory":
    import frontend.PredictionHistory as HistoryModule
    HistoryModule.render()
elif selected_page == "Profile":
    import frontend.Profile as ProfileModule
    ProfileModule.render()
elif selected_page == "AdminDashboard":
    import frontend.AdminDashboard as AdminModule
    AdminModule.render()
else:
    # Home Landing Page
    render_banner(
        title="Enterprise AI Loan Approval & Credit Scoring Platform",
        subtitle="Automated credit risk assessment, CIBIL score calculation, and loan probability forecasting powered by Scikit-learn Gradient Boosting models.",
        icon="🏦"
    )

    # Top KPI Metrics Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_metric_card("Model Accuracy", "95.0%", "Gradient Boosting Trained", "#16A34A", "🎯")
    with col2:
        render_metric_card("CIBIL Benchmark", "750+", "Excellent Credit Rating", "#1E3A8A", "📈")
    with col3:
        render_metric_card("Inference Latency", "< 25ms", "Real-time AI Scoring", "#2563EB", "⚡")
    with col4:
        render_metric_card("Database Cluster", "MongoDB Atlas", "Motor Async Driver Active", "#0EA5E9", "🗄️")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🌟 Platform Core Capabilities")
    
    st.markdown(
        """
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 16px; margin-top: 12px;">
            <div class="enterprise-card">
                <div style="font-size: 1.2rem; font-weight: 700; color: #111827; margin-bottom: 6px;">🤖 Gradient Boosting AI Engine</div>
                <div style="font-size: 0.95rem; color: #4B5563;">Predicts loan approval probability with 95.0% validated accuracy based on 22 financial parameters.</div>
            </div>
            <div class="enterprise-card">
                <div style="font-size: 1.2rem; font-weight: 700; color: #111827; margin-bottom: 6px;">🧮 Interactive CIBIL Estimator</div>
                <div style="font-size: 0.95rem; color: #4B5563;">Calculates credit score breakdown from payment history, credit card utilization, and hard inquiries.</div>
            </div>
            <div class="enterprise-card">
                <div style="font-size: 1.2rem; font-weight: 700; color: #111827; margin-bottom: 6px;">📊 Cashflow & Risk Diagnostics</div>
                <div style="font-size: 0.95rem; color: #4B5563;">Computes DTI ratio, interest rate estimates, allowable loan limits, and personalized financial tips.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.markdown("### 🚀 Get Started Now")

    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("📝 Run New Loan Prediction Assessment", use_container_width=True):
            st.session_state["current_page"] = "LoanPrediction"
            st.rerun()
    with btn_col2:
        if not is_logged_in:
            if st.button("🔑 Account Login / Sign Up", use_container_width=True):
                st.session_state["current_page"] = "Login"
                st.rerun()
        else:
            if st.button("📊 Access Personal Executive Dashboard", use_container_width=True):
                st.session_state["current_page"] = "Dashboard"
                st.rerun()
