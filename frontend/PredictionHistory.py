import streamlit as st
import pandas as pd
import requests
import json

try:
    from frontend.components.cards import render_banner
    from frontend.config import get_api_url
except ModuleNotFoundError:
    from components.cards import render_banner
    from config import get_api_url

def render():
    user = st.session_state.get("user")
    token = st.session_state.get("token")

    if not user:
        st.info("🔐 Please log in to access your prediction history.")
        if st.button("🔑 Account Login", key="history_login_btn", use_container_width=True):
            st.session_state["current_page"] = "Login"
            st.rerun()
        return

    is_dark = st.session_state.get("theme", "light") == "dark"
    card_bg = "#1E293B" if is_dark else "#FFFFFF"
    border_c = "#334155" if is_dark else "#CBD5E1"
    text_color = "#FFFFFF" if is_dark else "#0F172A"
    sub_color = "#94A3B8" if is_dark else "#475569"

    render_banner(
        title="Prediction History & Audit Logs",
        subtitle="Search, filter, and export credit risk evaluation reports stored in MongoDB Atlas.",
        icon="📜"
    )

    # Fetch User History via FastAPI
    predictions = []
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    history_url = get_api_url("/users/history")

    try:
        res = requests.get(history_url, headers=headers, timeout=10)
        if res.status_code == 200:
            predictions = res.json().get("data", [])
        elif res.status_code == 401:
            st.toast("⚠️ Session expired. Please sign in again.", icon="🚨")
            st.error("❌ 401 Unauthorized: Session expired. Please sign in again.")
            return
        elif res.status_code == 500:
            st.toast("❌ Server Error fetching history.", icon="💥")
            st.error("❌ 500 Internal Server Error: Unable to fetch prediction history.")
            return
        else:
            st.toast(f"❌ Error {res.status_code}", icon="⚠️")
    except Exception as ex:
        st.error(f"❌ Connection Error: Unable to reach backend server at {history_url}. ({ex})")
        return

    if not predictions:
        st.info("ℹ️ No prediction history recorded yet. Run a new prediction to populate your history!")
        if st.button("🚀 Run New Loan Prediction Assessment", key="pred_hist_new_btn", use_container_width=True):
            st.session_state["current_page"] = "LoanPrediction"
            st.rerun()
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
            q in str(p.get("inputData", {}).get("LoanAmount", "")).lower() or
            q in str(p.get("result", {}).get("loan_type", "")).lower()
        ]

    st.markdown(f"<p style='color: {sub_color} !important; font-weight: 600;'>Displaying <b>{len(filtered)}</b> of <b>{len(predictions)}</b> records.</p>", unsafe_allow_html=True)

    # Data Table View
    table_rows = []
    for p in filtered:
        inp = p.get("inputData", {})
        res = p.get("result", {})
        approved = res.get("approved") or res.get("loan_status") == "Approved"
        table_rows.append({
            "Loan Type": res.get("loan_type", inp.get("LoanType", "Loan")),
            "Amount": f"₹{float(res.get('loan_amount', inp.get('LoanAmount', 0))):,.0f}",
            "Date": str(p.get("createdAt", ""))[:19],
            "Status": "Approved ✅" if approved else "Rejected ❌",
            "Credit Score": res.get("cibil_score", inp.get("CIBILScore", "N/A")),
            "EMI": f"₹{res.get('emi_estimate', 0):,.2f}",
            "Probability": f"{res.get('approval_probability', 0):.1f}%",
            "Record ID": str(p.get("id") or p.get("_id"))
        })

    if table_rows:
        df = pd.DataFrame(table_rows)
        st.dataframe(df, use_container_width=True)

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
    st.markdown(f"<h3 style='color: {text_color} !important;'>🔍 Detailed Record Inspector</h3>", unsafe_allow_html=True)

    for p in filtered:
        p_id = str(p.get("id") or p.get("_id"))
        inp = p.get("inputData", {})
        res = p.get("result", {})
        approved = res.get("approved") or res.get("loan_status") == "Approved"

        with st.expander(f"{'✅' if approved else '❌'} ID: {p_id} | {inp.get('fullName', 'Applicant')} | Loan: ₹{float(res.get('loan_amount', inp.get('LoanAmount', 0))):,.0f}"):
            d1, d2 = st.columns(2)
            with d1:
                st.markdown(f"<h5 style='color: {text_color} !important;'>Input Parameters</h5>", unsafe_allow_html=True)
                st.json(inp)
            with d2:
                st.markdown(f"<h5 style='color: {text_color} !important;'>AI Output Results</h5>", unsafe_allow_html=True)
                st.json(res)

            if st.button(f"🗑️ Delete Record {p_id}", key=f"del_{p_id}"):
                del_url = get_api_url(f"/predict/{p_id}")
                try:
                    res_del = requests.delete(del_url, headers=headers, timeout=10)
                    if res_del.status_code == 200:
                        st.toast("✅ Record deleted.", icon="🗑️")
                        st.success("Record deleted successfully.")
                        st.rerun()
                    else:
                        st.toast("❌ Delete failed.", icon="🚨")
                        st.error("Failed to delete record from database.")
                except Exception as ex:
                    st.error(f"Error deleting record: {ex}")
