import streamlit as st
import pandas as pd
import requests
import asyncio
from backend.config import settings
from backend.database.connection import get_database
from ml.predictor import ml_predictor
from frontend.components.cards import render_banner, render_metric_card
from frontend.components.charts import create_risk_distribution_pie

def render():
    user = st.session_state.get("user")
    if not user or user.get("role") != "admin":
        st.error("🛡️ Access Denied: Administrator privileges required to view this page.")
        return

    render_banner(
        title="Admin Control Operations & Diagnostics",
        subtitle="Monitor system health, ML model diagnostics, registered users, and system prediction activity.",
        icon="🛡️"
    )

    token = st.session_state.get("token")
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    # Fetch Admin Dashboard Stats
    stats = {}
    users_list = []
    predictions_list = []

    try:
        res_stats = requests.get(f"http://127.0.0.1:{settings.PORT}/api/admin/dashboard-stats", headers=headers, timeout=4)
        if res_stats.status_code == 200:
            stats = res_stats.json().get("data", {})
        
        res_users = requests.get(f"http://127.0.0.1:{settings.PORT}/api/admin/users", headers=headers, timeout=4)
        if res_users.status_code == 200:
            users_list = res_users.json().get("data", [])

        res_preds = requests.get(f"http://127.0.0.1:{settings.PORT}/api/admin/predictions", headers=headers, timeout=4)
        if res_preds.status_code == 200:
            predictions_list = res_preds.json().get("data", [])
    except Exception:
        db = get_database()
        if db is not None:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            async def _fetch():
                tot_u = await db.users.count_documents({})
                tot_p = await db.predictions.count_documents({})
                app_p = await db.predictions.count_documents({"result.approved": True})
                rate = round((app_p / tot_p * 100), 2) if tot_p > 0 else 0.0
                return {"totalUsers": tot_u, "totalPredictions": tot_p, "approvedCount": app_p, "approvalRate": rate}
            stats = loop.run_until_complete(_fetch())

    tot_users = stats.get("totalUsers", len(users_list))
    tot_preds = stats.get("totalPredictions", len(predictions_list))
    approved_cnt = stats.get("approvedCount", 0)
    rejected_cnt = tot_preds - approved_cnt
    approval_rate = stats.get("approvalRate", 0.0)

    # Top KPI Metrics Row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_card("Registered Users", str(tot_users), "Database Total", "#1E3A8A", "👥")
    with c2:
        render_metric_card("Total Predictions", str(tot_preds), "System Inferences", "#2563EB", "📋")
    with c3:
        render_metric_card("Approval Rate", f"{approval_rate}%", f"{approved_cnt} Approved / {rejected_cnt} Rejected", "#16A34A", "📈")
    with c4:
        render_metric_card("ML Model Engine", ml_predictor.best_model_name, f"Accuracy: {ml_predictor.accuracy}%", "#F59E0B", "🎯")

    st.markdown("---")

    chart_col, info_col = st.columns([1.2, 1])
    with chart_col:
        st.plotly_chart(create_risk_distribution_pie(approved_cnt, max(0, rejected_cnt)), use_container_width=True)

    with info_col:
        st.markdown("### 🤖 ML Model Engine Status")
        st.write(f"**Loaded Status:** `{'✅ Active Model' if ml_predictor.model_loaded else '⚠️ Fallback Mode'}`")
        st.write(f"**Algorithm Name:** `{ml_predictor.best_model_name}`")
        st.write(f"**Test Accuracy:** `{ml_predictor.accuracy}%`")
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
