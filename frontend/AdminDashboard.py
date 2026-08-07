import streamlit as st
import pandas as pd
import requests
from frontend.components.cards import render_banner, render_metric_card
from frontend.components.charts import create_risk_distribution_pie

def render():
    user = st.session_state.get("user")
    if not user or user.get("role") != "admin":
        st.error("🛡️ Access Denied: Administrator privileges required to view this page.")
        if not user:
            if st.button("🔑 Account Login", use_container_width=True):
                st.session_state["current_page"] = "Login"
                st.rerun()
        return

    render_banner(
        title="Admin Control Operations & Diagnostics",
        subtitle="Monitor system health, ML model diagnostics, registered users, and system prediction activity.",
        icon="🛡️"
    )

    token = st.session_state.get("token")
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    # Fetch Admin Dashboard Stats via REST API
    stats = {}
    users_list = []
    predictions_list = []

    try:
        try:
            from frontend.config import API_URL
        except ModuleNotFoundError:
            from config import API_URL
        res_stats = requests.get(f"{API_URL}/api/admin/dashboard-stats", headers=headers, timeout=10)
        if res_stats.status_code == 200:
            stats = res_stats.json().get("data", {})
        
        res_users = requests.get(f"{API_URL}/api/admin/users", headers=headers, timeout=10)
        if res_users.status_code == 200:
            users_list = res_users.json().get("data", [])

        res_preds = requests.get(f"{API_URL}/api/admin/predictions", headers=headers, timeout=10)
        if res_preds.status_code == 200:
            predictions_list = res_preds.json().get("data", [])
    except Exception:
        stats = {}

    tot_users = stats.get("totalUsers", len(users_list))
    tot_preds = stats.get("totalPredictions", len(predictions_list))
    approved_cnt = stats.get("approvedCount", 0)
    rejected_cnt = tot_preds - approved_cnt
    approval_rate = stats.get("approvalRate", 0.0)
    ml_status = stats.get("mlModelStatus", {})
    ml_algo = ml_status.get("algorithm", "Gradient Boosting Model")
    ml_acc = ml_status.get("accuracy", 95.0)

    # Top KPI Metrics Row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_card("Registered Users", str(tot_users), "Database Total", "#1E3A8A", "👥")
    with c2:
        render_metric_card("Total Predictions", str(tot_preds), "System Inferences", "#2563EB", "📋")
    with c3:
        render_metric_card("Approval Rate", f"{approval_rate}%", f"{approved_cnt} Approved / {max(0, rejected_cnt)} Rejected", "#16A34A", "📈")
    with c4:
        render_metric_card("ML Model Engine", str(ml_algo), f"Accuracy: {ml_acc}%", "#F59E0B", "🎯")

    st.markdown("---")

    chart_col, info_col = st.columns([1.2, 1])
    with chart_col:
        st.plotly_chart(create_risk_distribution_pie(approved_cnt, max(0, rejected_cnt)), use_container_width=True)

    with info_col:
        st.markdown("### 🤖 ML Model Engine Status")
        st.write(f"**Loaded Status:** `{'✅ Active Model' if ml_status.get('loaded', True) else '⚠️ Fallback Mode'}`")
        st.write(f"**Algorithm Name:** `{ml_algo}`")
        st.write(f"**Test Accuracy:** `{ml_acc}%`")
        st.write(f"**Model Artifact File:** `ml/model.pkl` & `ml/scaler.pkl`")

    st.markdown("---")
    st.markdown("### 👥 Registered Users Registry")
    if users_list:
        users_df = pd.DataFrame(users_list)
        st.dataframe(users_df, use_container_width=True)
    else:
        st.info("No registered user accounts found.")

    st.markdown("---")
    st.markdown("### 📜 System Prediction Audit Log")
    if predictions_list:
        preds_df = pd.DataFrame([
            {
                "Prediction ID": str(p.get("id") or p.get("_id")),
                "User ID": p.get("userId", "Anonymous"),
                "Applicant": p.get("inputData", {}).get("fullName", "N/A"),
                "Loan Amount": f"₹{float(p.get('inputData', {}).get('LoanAmount', 0)):,.0f}",
                "Status": "Approved ✅" if p.get("result", {}).get("approved") else "Rejected ❌",
                "Probability": f"{p.get('result', {}).get('approval_probability', 0)}%",
                "Created Date": str(p.get("createdAt"))[:19]
            }
            for p in predictions_list
        ])
        st.dataframe(preds_df, use_container_width=True)
    else:
        st.info("No prediction logs recorded yet.")

