import streamlit as st
import requests
import pandas as pd
from frontend.components.cards import render_banner, render_metric_card
from frontend.components.charts import create_cibil_distribution_bar, create_risk_distribution_pie

def render():
    user = st.session_state.get("user")
    if not user:
        st.warning("Please log in to access your enterprise dashboard.")
        if st.button("🔑 Account Login", use_container_width=True):
            st.session_state["current_page"] = "Login"
            st.rerun()
        return

    render_banner(
        title=f"Executive Dashboard — Welcome, {user.get('name')}!",
        subtitle="Real-time monitoring of loan predictions, credit scoring analytics, and portfolio performance.",
        icon="📊"
    )

    token = st.session_state.get("token")

    # Fetch User Prediction History via REST API
    predictions = []
    try:
        try:
            from frontend.config import API_URL
        except ModuleNotFoundError:
            from config import API_URL
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        res = requests.get(f"{API_URL}/api/predict/history", headers=headers, timeout=10)
        if res.status_code == 200:
            predictions = res.json().get("data", [])
        else:
            predictions = []
    except Exception:
        predictions = []

    total_preds = len(predictions)
    approved_preds = [p for p in predictions if p.get("result", {}).get("approved") or p.get("result", {}).get("loan_status") == "Approved"]
    approved_count = len(approved_preds)
    rejected_count = total_preds - approved_count
    cibil_scores = [int(p.get("result", {}).get("cibil_score") or p.get("inputData", {}).get("CIBILScore", 720)) for p in predictions]
    avg_cibil = int(sum(cibil_scores) / max(1, len(cibil_scores))) if cibil_scores else int(user.get("cibil_score", 720))

    # Top 5 KPI Metric Cards
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        render_metric_card("Total Predictions", str(total_preds), "Portfolio Inferences", "#1E3A8A", "📋")
    with col2:
        render_metric_card("Approved Loans", str(approved_count), f"{round(approved_count/max(1,total_preds)*100)}% Approval Rate", "#16A34A", "✅")
    with col3:
        render_metric_card("Rejected Loans", str(rejected_count), f"{round(rejected_count/max(1,total_preds)*100)}% Risk Flagged", "#DC2626", "❌")
    with col4:
        render_metric_card("Avg CIBIL Score", str(avg_cibil), "Portfolio Credit Rating", "#0EA5E9", "📈")
    with col5:
        render_metric_card("Model Accuracy", "95.0%", "Gradient Boosting Trained", "#F59E0B", "🎯")

    st.markdown("---")

    # Charts Row
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.plotly_chart(create_risk_distribution_pie(approved_count, rejected_count), use_container_width=True)
    with chart_col2:
        st.plotly_chart(create_cibil_distribution_bar(predictions), use_container_width=True)

    st.markdown("---")
    st.markdown("### 📜 Recent Predictions Audit Table")

    if not predictions:
        st.info("No prediction history recorded yet. Click below to run your first loan application assessment.")
        if st.button("🚀 Run New Loan Prediction Assessment", use_container_width=True):
            st.session_state["current_page"] = "LoanPrediction"
            st.rerun()
    else:
        recent_rows = []
        for p in predictions[:8]:
            inp = p.get("inputData", {})
            res = p.get("result", {})
            approved = res.get("approved") or res.get("loan_status") == "Approved"
            recent_rows.append({
                "Prediction ID": str(p.get("id") or p.get("_id")),
                "Applicant": inp.get("fullName", "N/A"),
                "Loan Amount": f"₹{float(inp.get('LoanAmount') or inp.get('loanAmount') or 0):,.0f}",
                "CIBIL Score": res.get("cibil_score", inp.get("CIBILScore", 0)),
                "Status": "Approved ✅" if approved else "Rejected ❌",
                "Probability": f"{res.get('approval_probability', 0)}%",
                "Risk Level": res.get("credit_risk_level", "N/A"),
                "Created Date": str(p.get("createdAt"))[:19]
            })

        df_recent = pd.DataFrame(recent_rows)
        st.dataframe(df_recent, use_container_width=True)

