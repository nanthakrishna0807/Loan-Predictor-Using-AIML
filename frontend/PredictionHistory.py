import streamlit as st
import pandas as pd
import requests
import asyncio
import json
from backend.config import settings
from backend.services.prediction_service import get_user_predictions, delete_prediction_by_id
from frontend.components.cards import render_banner, render_status_badge

def render():
    user = st.session_state.get("user")
    if not user:
        st.warning("Please log in to access your prediction history.")
        return

    render_banner(
        title="Prediction History & Audit Logs",
        subtitle="Search, filter, and export credit risk evaluation reports stored in MongoDB Atlas.",
        icon="📜"
    )

    token = st.session_state.get("token")
    user_id = str(user.get("_id") or user.get("id"))

    # Fetch User History
    predictions = []
    try:
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        res = requests.get(f"http://127.0.0.1:{settings.PORT}/api/predict/history", headers=headers, timeout=4)
        if res.status_code == 200:
            predictions = res.json().get("data", [])
        else:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            res_data = loop.run_until_complete(get_user_predictions(user_id))
            predictions = res_data.get("data", [])
    except Exception:
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            res_data = loop.run_until_complete(get_user_predictions(user_id))
            predictions = res_data.get("data", [])
        except Exception:
            predictions = []

    if not predictions:
        st.info("No prediction history recorded yet. Run a new prediction to populate your history!")
        return

    # Filters Row
    col1, col2 = st.columns([1, 2])
    with col1:
        status_filter = st.selectbox("Filter Status", ["All Statuses", "Approved", "Rejected"])
    with col2:
        search_query = st.text_input("Search Applicant Name or Amount", "")

    filtered = predictions
    if status_filter == "Approved":
        filtered = [p for p in filtered if p.get("result", {}).get("approved") or p.get("result", {}).get("loan_status") == "Approved"]
    elif status_filter == "Rejected":
        filtered = [p for p in filtered if not (p.get("result", {}).get("approved") or p.get("result", {}).get("loan_status") == "Approved")]

    if search_query:
        q = search_query.lower()
        filtered = [
            p for p in filtered if
            q in str(p.get("inputData", {}).get("fullName", "")).lower() or
            q in str(p.get("inputData", {}).get("LoanAmount", "")).lower()
        ]

    st.markdown(f"<p style='color: #4B5563; font-weight: 600;'>Displaying <b>{len(filtered)}</b> of <b>{len(predictions)}</b> records.</p>", unsafe_allow_html=True)

    # Data Table View
    table_rows = []
    for p in filtered:
        inp = p.get("inputData", {})
        res = p.get("result", {})
        approved = res.get("approved") or res.get("loan_status") == "Approved"
        table_rows.append({
            "Record ID": str(p.get("id") or p.get("_id")),
            "Applicant": inp.get("fullName", "N/A"),
            "Loan Amount": f"₹{float(inp.get('LoanAmount') or inp.get('loanAmount') or 0):,.0f}",
            "CIBIL": res.get("cibil_score", inp.get("CIBILScore", 0)),
            "Status": "Approved ✅" if approved else "Rejected ❌",
            "Probability": f"{res.get('approval_probability', 0)}%",
            "Risk Level": res.get("credit_risk_level", "N/A"),
            "Created Date": str(p.get("createdAt"))[:19]
        })

    if table_rows:
        df = pd.DataFrame(table_rows)
        st.dataframe(df, use_container_width=True)

        # Download Export Buttons
        col_exp1, col_exp2 = st.columns(2)
        with col_exp1:
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export Table to CSV",
                data=csv_data,
                file_name="loan_predictions_history.csv",
                mime="text/csv",
                use_container_width=True
            )
        with col_exp2:
            json_data = json.dumps(predictions, indent=2).encode('utf-8')
            st.download_button(
                label="📥 Export Full Records JSON",
                data=json_data,
                file_name="loan_predictions_raw.json",
                mime="application/json",
                use_container_width=True
            )

    st.markdown("---")
    st.markdown("### 🔍 Detailed Record Inspector")

    for p in filtered:
        p_id = str(p.get("id") or p.get("_id"))
        inp = p.get("inputData", {})
        res = p.get("result", {})
        approved = res.get("approved") or res.get("loan_status") == "Approved"

        with st.expander(f"{'✅' if approved else '❌'} ID: {p_id} | {inp.get('fullName', 'Applicant')} | Loan: ₹{float(inp.get('LoanAmount', 0)):,.0f}"):
            d1, d2 = st.columns(2)
            with d1:
                st.markdown("<h5 style='color: #111827;'>Input Parameters</h5>", unsafe_allow_html=True)
                st.json(inp)
            with d2:
                st.markdown("<h5 style='color: #111827;'>AI Output Results</h5>", unsafe_allow_html=True)
                st.json(res)

            if st.button(f"🗑️ Delete Record {p_id}", key=f"del_{p_id}"):
                try:
                    headers = {"Authorization": f"Bearer {token}"} if token else {}
                    res_del = requests.delete(f"http://127.0.0.1:{settings.PORT}/api/predict/{p_id}", headers=headers, timeout=3)
                    if res_del.status_code == 200:
                        st.success("Record deleted.")
                        st.rerun()
                    else:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        loop.run_until_complete(delete_prediction_by_id(p_id, user_id))
                        st.success("Record deleted.")
                        st.rerun()
                except Exception:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(delete_prediction_by_id(p_id, user_id))
                    st.success("Record deleted.")
                    st.rerun()
