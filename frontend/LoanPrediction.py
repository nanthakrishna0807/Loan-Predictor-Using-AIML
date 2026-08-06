import streamlit as st
import requests
import asyncio
from backend.config import settings
from backend.services.prediction_service import create_prediction
from frontend.components.cards import render_banner, render_status_badge, render_metric_card, render_tip_box
from frontend.components.charts import create_approval_meter, create_cibil_gauge, create_income_vs_emi_chart
from frontend.components.cibil_widget import render_cibil_calculator_widget

def render():
    render_banner(
        title="AI Credit Risk & Loan Approval Assessment Form",
        subtitle="Complete the grouped 5-section evaluation form below to execute instant ML prediction and financial diagnostics.",
        icon="📝"
    )

    tab_form, tab_cibil = st.tabs(["📋 Loan Application Form", "🧮 Integrated CIBIL Estimator"])

    with tab_cibil:
        calculated_cibil = render_cibil_calculator_widget()

    with tab_form:
        st.markdown("<p style='color: #4B5563; font-size: 0.95rem; font-weight: 500;'>Please fill in all applicant financial parameters accurately.</p>", unsafe_allow_html=True)

        with st.form("loan_prediction_enterprise_form"):
            # Section 1: Personal Information
            st.markdown(
                """
                <div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 12px; padding: 18px 22px; margin-bottom: 16px; border-left: 5px solid #1E3A8A;">
                    <div style="font-size: 1.05rem; font-weight: 700; color: #111827;">1. Personal Information</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            col1, col2, col3 = st.columns(3)
            user = st.session_state.get("user") or {}
            with col1:
                full_name = st.text_input("Full Name *", value=user.get("name", "John Doe"))
                age = st.number_input("Age (Years) *", min_value=18, max_value=100, value=32, help="Must be at least 18 years old")
            with col2:
                gender = st.selectbox("Gender *", ["Male", "Female", "Other"])
                marital_status = st.selectbox("Marital Status *", ["Single", "Married", "Divorced", "Widowed"])
            with col3:
                education = st.selectbox("Education Level *", ["Graduate", "Post-Graduate", "Doctorate", "Undergraduate", "High School"])
                dependents = st.number_input("Dependents Count", min_value=0, max_value=10, value=1)

            # Section 2: Employment Details
            st.markdown(
                """
                <div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 12px; padding: 18px 22px; margin-bottom: 16px; border-left: 5px solid #2563EB;">
                    <div style="font-size: 1.05rem; font-weight: 700; color: #111827;">2. Employment Details</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            emp_col1, emp_col2 = st.columns(2)
            with emp_col1:
                occupation = st.selectbox("Occupation Category *", ["Salaried", "Self-Employed", "Business Owner", "Freelancer", "Professional"])
            with emp_col2:
                employment_type = st.selectbox("Employment Sector *", ["Salaried", "Self-Employed", "Government", "Private Sector", "Unemployed"])

            # Section 3: Financial Information
            st.markdown(
                """
                <div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 12px; padding: 18px 22px; margin-bottom: 16px; border-left: 5px solid #0EA5E9;">
                    <div style="font-size: 1.05rem; font-weight: 700; color: #111827;">3. Financial & Liquidity Details</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            fin_col1, fin_col2, fin_col3 = st.columns(3)
            with fin_col1:
                monthly_income = st.number_input("Monthly Net Income (₹) *", min_value=1000.0, value=65000.0, step=5000.0, help="Must be greater than 0")
            with fin_col2:
                annual_income = st.number_input("Annual Gross Income (₹)", min_value=12000.0, value=monthly_income * 12, step=50000.0)
            with fin_col3:
                bank_balance = st.number_input("Liquid Bank Balance (₹)", min_value=0.0, value=120000.0, step=10000.0)

            # Section 4: Loan Request Information
            st.markdown(
                """
                <div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 12px; padding: 18px 22px; margin-bottom: 16px; border-left: 5px solid #F59E0B;">
                    <div style="font-size: 1.05rem; font-weight: 700; color: #111827;">4. Loan Request Information</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            loan_col1, loan_col2, loan_col3, loan_col4 = st.columns(4)
            with loan_col1:
                loan_amount = st.number_input("Desired Loan Amount (₹) *", min_value=5000.0, value=350000.0, step=25000.0, help="Must be greater than 0")
            with loan_col2:
                loan_tenure = st.number_input("Loan Tenure (Months) *", min_value=6, max_value=360, value=36, step=6)
            with loan_col3:
                existing_loans = st.number_input("Active Loans Count", min_value=0, max_value=10, value=0)
            with loan_col4:
                existing_emi = st.number_input("Existing Monthly EMI (₹)", min_value=0.0, value=5000.0, step=1000.0)

            # Section 5: Credit & Bureau Details
            st.markdown(
                """
                <div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 12px; padding: 18px 22px; margin-bottom: 16px; border-left: 5px solid #16A34A;">
                    <div style="font-size: 1.05rem; font-weight: 700; color: #111827;">5. Credit Bureau & Asset Details</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            cred_col1, cred_col2, cred_col3, cred_col4 = st.columns(4)
            with cred_col1:
                cibil_score = st.slider("CIBIL Score *", min_value=300, max_value=900, value=int(user.get("cibil_score", 735)), help="Must be between 300 and 900")
            with cred_col2:
                credit_card_usage = st.slider("Credit Utilization (%)", 0, 100, 25) / 100.0
            with cred_col3:
                prev_defaults = st.selectbox("Previous Defaults Count", [0, 1, 2, 3])
            with cred_col4:
                property_area = st.selectbox("Property Location Area", ["Urban", "Semi-Urban", "Rural"])

            st.markdown("<br>", unsafe_allow_html=True)
            submit_btn = st.form_submit_button("⚡ Execute AI Credit Evaluation", use_container_width=True)

    if submit_btn:
        if age < 18:
            st.error("❌ Validation Error: Applicant age must be at least 18 years.")
            return
        if monthly_income <= 0:
            st.error("❌ Validation Error: Monthly income must be greater than 0.")
            return
        if loan_amount <= 0:
            st.error("❌ Validation Error: Loan amount must be greater than 0.")
            return
        if not (300 <= cibil_score <= 900):
            st.error("❌ Validation Error: CIBIL score must be between 300 and 900.")
            return

        payload = {
            "fullName": full_name,
            "Age": age,
            "Gender": gender,
            "MaritalStatus": marital_status,
            "Occupation": occupation,
            "EmploymentType": employment_type,
            "MonthlyIncome": monthly_income,
            "AnnualIncome": annual_income,
            "ExistingLoans": existing_loans,
            "ExistingEMI": existing_emi,
            "LoanAmount": loan_amount,
            "LoanTenure": loan_tenure,
            "LoanTerm": loan_tenure,
            "CIBILScore": cibil_score,
            "Dependents": dependents,
            "Education": education,
            "PropertyArea": property_area,
            "BankBalance": bank_balance,
            "CreditCardUsage": credit_card_usage,
            "PreviousLoanDefaults": prev_defaults
        }

        with st.spinner("Processing applicant parameters through Gradient Boosting AI model..."):
            token = st.session_state.get("token")
            user_id = str(user.get("_id") or user.get("id")) if user else None

            result_data = None
            try:
                try:
                    from frontend.config import API_URL
                except ModuleNotFoundError:
                    from config import API_URL
                headers = {"Authorization": f"Bearer {token}"} if token else {}
                res = requests.post(f"{API_URL}/api/predict/loan", json=payload, headers=headers, timeout=5)
                if res.status_code == 200:
                    result_data = res.json().get("data") or res.json().get("result")
                else:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    res_obj = loop.run_until_complete(create_prediction(payload, user_id))
                    result_data = res_obj.get("data")
            except Exception:
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    res_obj = loop.run_until_complete(create_prediction(payload, user_id))
                    result_data = res_obj.get("data")
                except Exception as ex:
                    st.error(f"Prediction Error: {ex}")
                    return

        if result_data:
            st.markdown("---")
            st.markdown("## 📊 Loan Prediction Executive Report")

            approved = result_data.get("approved", False)
            prob = result_data.get("approval_probability", 50.0)
            status_str = result_data.get("loan_status", "Approved" if approved else "Rejected")
            risk_level = result_data.get("credit_risk_level", "Medium")
            risk_color = result_data.get("credit_risk_color", "#F59E0B")

            # Outcome Cards Row
            res_col1, res_col2, res_col3 = st.columns([1.4, 1, 1])

            with res_col1:
                st.markdown("### Application Outcome:")
                render_status_badge(status_str)
                st.markdown(f"<div style='margin-top: 10px; font-weight: 700; color: #111827;'>Credit Risk: <span style='color:{risk_color};'>{risk_level} Risk</span></div>", unsafe_allow_html=True)
                st.markdown(f"<div style='font-size: 0.85rem; color: #4B5563; margin-top: 4px;'>Model Engine: <code>{result_data.get('model_used', 'Gradient Boosting')}</code></div>", unsafe_allow_html=True)

            with res_col2:
                render_metric_card("Suggested Max Loan", f"₹{result_data.get('suggested_max_loan', 0):,.0f}", "50% Debt-to-Income Cap", "#16A34A", "💵")
            
            with res_col3:
                render_metric_card("Estimated EMI", f"₹{result_data.get('emi_estimate', 0):,.2f}/mo", f"Estimated APR: {result_data.get('interest_rate_estimate', 10.5)}%", "#1E3A8A", "💳")

            st.markdown("---")

            # Plotly Visualizations
            chart_col1, chart_col2 = st.columns(2)
            with chart_col1:
                st.plotly_chart(create_approval_meter(prob), use_container_width=True)
            with chart_col2:
                st.plotly_chart(create_income_vs_emi_chart(monthly_income, existing_emi, result_data.get('emi_estimate', 0)), use_container_width=True)

            # Recommendations & Financial Advice
            st.markdown("### 💡 AI Financial Advisory Diagnostics")
            st.info(result_data.get("recommendation", ""))

            st.markdown("#### 🎯 Actionable Credit Improvement Tips:")
            tips = result_data.get("financial_improvement_tips", [])
            for tip in tips:
                render_tip_box(tip)
