import streamlit as st
import pandas as pd

try:
    from frontend.components.cards import render_banner, render_metric_card
    from frontend.components.charts import create_cibil_distribution_bar
    from frontend.services.user_service import get_user_prediction_history
except ModuleNotFoundError:
    from components.cards import render_banner, render_metric_card
    from components.charts import create_cibil_distribution_bar
    from services.user_service import get_user_prediction_history

def render():
    user = st.session_state.get("user")
    if not user:
        st.info("🔐 Please log in to access your user dashboard.")
        if st.button("🔑 Account Login", key="dash_login_btn", use_container_width=True):
            st.session_state["current_page"] = "Login"
            st.rerun()
        return

    is_dark = st.session_state.get("theme", "light") == "dark"
    text_color = "#FFFFFF" if is_dark else "#0F172A"

    render_banner(
        title=f"User Dashboard — Welcome, {user.get('name', 'Applicant')}!",
        subtitle="View your loan application status, credit score analytics, EMI details, and prediction history.",
        icon="👤"
    )

    # Fetch User Prediction History via FastAPI user service
    success, predictions, err = get_user_prediction_history()
    if not success and err:
        st.error(f"❌ Error fetching history: {err}")

    # Metrics computation from real database records
    total_preds = len(predictions)
    recent_pred = predictions[0] if predictions else None

    if recent_pred:
        res_obj = recent_pred.get("result", {})
        inp_obj = recent_pred.get("inputData", {})
        
        recent_loan_type = res_obj.get("loan_type", inp_obj.get("LoanType", "Personal Loan"))
        recent_status = res_obj.get("loan_status", "Approved" if res_obj.get("approved") else "Rejected")
        recent_cibil = res_obj.get("cibil_score", inp_obj.get("CIBILScore", "N/A"))
        recent_emi = f"₹{res_obj.get('emi_estimate', 0):,.2f}" if res_obj.get("emi_estimate") else "N/A"
        recent_prob = f"{res_obj.get('approval_probability', 0):.1f}%"
        recent_amount = f"₹{float(res_obj.get('loan_amount', inp_obj.get('LoanAmount', 0))):,.0f}"
    else:
        recent_loan_type = "No Applications"
        recent_status = "No Records"
        recent_cibil = "N/A"
        recent_emi = "N/A"
        recent_prob = "N/A"
        recent_amount = "N/A"

    # Display Top Overview Cards
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        render_metric_card("Recent Loan", recent_loan_type, f"Amount: {recent_amount}", "#1E3A8A", "🏠")
    with c2:
        render_metric_card("Credit Score", str(recent_cibil), "Latest Bureau Score", "#0EA5E9", "📈")
    with c3:
        render_metric_card("Monthly EMI", recent_emi, "Estimated Obligation", "#2563EB", "💳")
    with c4:
        render_metric_card("Approval Prob.", recent_prob, "AI Probability Score", "#16A34A", "🎯")
    with c5:
        render_metric_card("Loan Status", recent_status, f"Total Applications: {total_preds}", "#F59E0B", "📜")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")

    # Prediction History Section
    st.markdown(f"<h3 style='color: {text_color} !important;'>📜 Prediction History</h3>", unsafe_allow_html=True)

    if not predictions:
        st.info("ℹ️ No prediction history available. Apply for a loan to view your credit risk analysis here.")
        if st.button("🚀 Apply for a New Loan", key="dash_apply_btn", use_container_width=True):
            st.session_state["current_page"] = "LoanPrediction"
            st.rerun()
    else:
        history_rows = []
        for p in predictions:
            inp = p.get("inputData", {})
            res = p.get("result", {})
            approved = res.get("approved") or res.get("loan_status") == "Approved"
            
            history_rows.append({
                "Prediction ID": str(p.get("id") or p.get("_id")),
                "Loan Type": res.get("loan_type", inp.get("LoanType", "Loan")),
                "Amount": f"₹{float(res.get('loan_amount', inp.get('LoanAmount', 0))):,.0f}",
                "Status": "Approved ✅" if approved else "Rejected ❌",
                "Credit Score": res.get("cibil_score", inp.get("CIBILScore", "N/A")),
                "Monthly EMI": f"₹{res.get('emi_estimate', 0):,.2f}",
                "Probability": f"{res.get('approval_probability', 0):.1f}%",
                "Date": str(p.get("createdAt", ""))[:19]
            })

        df_history = pd.DataFrame(history_rows)
        st.dataframe(df_history, use_container_width=True)

    st.markdown("---")
    b1, b2 = st.columns(2)
    with b1:
        if st.button("📝 Apply for Another Loan", key="user_dash_new_pred", use_container_width=True):
            st.session_state["current_page"] = "LoanPrediction"
            st.rerun()
    with b2:
        if st.button("👤 View / Edit Profile", key="user_dash_profile", use_container_width=True):
            st.session_state["current_page"] = "Profile"
            st.rerun()
