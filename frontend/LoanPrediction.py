import streamlit as st
import requests
import time
import os
import sys

# Ensure the project root is on sys.path
_FRONTEND_DIR = os.path.dirname(os.path.abspath(__file__))
_ROOT_DIR     = os.path.dirname(_FRONTEND_DIR)
if _ROOT_DIR not in sys.path:
    sys.path.insert(0, _ROOT_DIR)

try:
    from frontend.components.cards import render_banner, render_status_badge, render_metric_card, render_tip_box
    from frontend.components.charts import create_approval_meter, create_income_vs_emi_chart
    from frontend.config import get_api_url
except ModuleNotFoundError:
    from components.cards import render_banner, render_status_badge, render_metric_card, render_tip_box
    from components.charts import create_approval_meter, create_income_vs_emi_chart
    from config import get_api_url

# ── Loan type configuration (mirrors backend LOAN_CONFIG) ────────────────────
LOAN_CONFIG = {
    "🏠 Home Loan":      {"key": "Home Loan",      "rate": 8.5,  "min_yr": 5,  "max_yr": 30, "default_yr": 20, "max_amt": 50_000_000,  "icon": "🏠"},
    "👤 Personal Loan":  {"key": "Personal Loan",  "rate": 12.5, "min_yr": 1,  "max_yr": 7,  "default_yr": 3,  "max_amt": 4_000_000,   "icon": "👤"},
    "🏢 Business Loan":  {"key": "Business Loan",  "rate": 11.0, "min_yr": 1,  "max_yr": 15, "default_yr": 5,  "max_amt": 100_000_000, "icon": "🏢"},
    "🎓 Education Loan": {"key": "Education Loan", "rate": 9.0,  "min_yr": 5,  "max_yr": 15, "default_yr": 8,  "max_amt": 20_000_000,  "icon": "🎓"},
    "🚗 Vehicle Loan":   {"key": "Vehicle Loan",   "rate": 9.5,  "min_yr": 1,  "max_yr": 7,  "default_yr": 5,  "max_amt": 10_000_000,  "icon": "🚗"},
}

def _emi(principal: float, rate_pa: float, tenure_months: int) -> float:
    if tenure_months <= 0 or principal <= 0:
        return 0.0
    r = (rate_pa / 100) / 12
    if r == 0:
        return round(principal / tenure_months, 2)
    return round(principal * r * (1 + r) ** tenure_months / ((1 + r) ** tenure_months - 1), 2)

def _section(title: str):
    st.markdown(
        f"""<div class="section-header-box"><div class="section-header-title">{title}</div></div>""",
        unsafe_allow_html=True
    )

def _emi_preview(is_dark: bool, loan_amt: float, rate: float, tenure_months: int):
    """Renders a live EMI breakdown card."""
    emi          = _emi(loan_amt, rate, tenure_months)
    total_pay    = round(emi * tenure_months, 2)
    total_int    = round(total_pay - loan_amt, 2)
    card_bg      = "#1E293B" if is_dark else "#F0F9FF"
    border_color = "#3B82F6" if is_dark else "#1E3A8A"
    title_color  = "#60A5FA" if is_dark else "#1E3A8A"
    text_color   = "#FFFFFF" if is_dark else "#0F172A"
    st.markdown(
        f"""
        <div style="background:{card_bg}; border:2px solid {border_color}; border-radius:16px;
                    padding:20px 24px; margin:18px 0 8px 0; box-shadow:0 6px 18px rgba(0,0,0,0.08);">
            <div style="font-size:0.9rem;font-weight:800;text-transform:uppercase;
                        letter-spacing:0.05em;color:{title_color};margin-bottom:14px;">
                ⚡ Live EMI Estimate
            </div>
            <div style="display:flex;gap:24px;flex-wrap:wrap;">
                <div style="text-align:center;flex:1;">
                    <div style="font-size:0.8rem;font-weight:700;color:{title_color};">Monthly EMI</div>
                    <div style="font-size:1.8rem;font-weight:800;color:{title_color};">₹{emi:,.2f}</div>
                </div>
                <div style="text-align:center;flex:1;">
                    <div style="font-size:0.8rem;font-weight:700;color:{text_color};">Total Interest</div>
                    <div style="font-size:1.4rem;font-weight:800;color:#F59E0B;">₹{total_int:,.0f}</div>
                </div>
                <div style="text-align:center;flex:1;">
                    <div style="font-size:0.8rem;font-weight:700;color:{text_color};">Total Payment</div>
                    <div style="font-size:1.4rem;font-weight:800;color:{text_color};">₹{total_pay:,.0f}</div>
                </div>
                <div style="text-align:center;flex:1;">
                    <div style="font-size:0.8rem;font-weight:700;color:{text_color};">Interest Rate</div>
                    <div style="font-size:1.4rem;font-weight:800;color:{text_color};">{rate}% p.a.</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ─────────────────────────────────────────────────────────────────────────────
# Form builders per loan type
# ─────────────────────────────────────────────────────────────────────────────
def _form_home(cfg, is_dark) -> dict:
    _section("1. Personal & Income Details")
    c1, c2, c3 = st.columns(3)
    with c1:
        full_name = st.text_input("Full Name *", value="John Doe")
        age       = st.number_input("Age *", min_value=18, max_value=80, value=35)
    with c2:
        monthly_income = st.number_input("Monthly Net Income (₹) *", min_value=1000.0, value=80000.0, step=5000.0)
        annual_income  = st.number_input("Annual Income (₹)", min_value=0.0, value=monthly_income * 12, step=50000.0)
    with c3:
        employment_type = st.selectbox("Employment Type *", ["Salaried", "Self-Employed", "Government", "Business Owner"])
        cibil_score     = st.slider("CIBIL Score *", 300, 900, 750)

    _section("2. Property & Loan Details")
    p1, p2, p3, p4 = st.columns(4)
    with p1:
        property_value = st.number_input("Property Value (₹) *", min_value=100000.0, value=5000000.0, step=100000.0)
    with p2:
        down_payment = st.number_input("Down Payment (₹) *", min_value=0.0, value=1000000.0, step=50000.0)
    with p3:
        loan_amount = st.number_input("Loan Amount (₹) *", min_value=100000.0, value=min(property_value - down_payment, cfg["max_amt"]), step=50000.0)
    with p4:
        existing_emi = st.number_input("Existing EMI (₹/month)", min_value=0.0, value=0.0, step=1000.0)

    tenure_years = st.slider("Loan Tenure (Years)", cfg["min_yr"], cfg["max_yr"], cfg["default_yr"])
    property_type = st.selectbox("Property Type", ["Apartment", "Independent House", "Villa", "Plot", "Commercial"])
    _emi_preview(is_dark, loan_amount, cfg["rate"], tenure_years * 12)

    return {
        "LoanType": cfg["key"], "fullName": full_name, "Age": age,
        "MonthlyIncome": monthly_income, "AnnualIncome": annual_income,
        "EmploymentType": employment_type, "CIBILScore": cibil_score,
        "LoanAmount": loan_amount, "LoanTenureYears": tenure_years,
        "ExistingEMI": existing_emi, "BankBalance": down_payment,
        "PropertyValue": property_value, "PropertyType": property_type,
        "PreviousLoanDefaults": 0, "CreditCardUsage": 0.2,
    }

def _form_personal(cfg, is_dark) -> dict:
    _section("1. Personal & Employment Details")
    c1, c2, c3 = st.columns(3)
    with c1:
        full_name     = st.text_input("Full Name *", value="Jane Smith")
        age           = st.number_input("Age *", min_value=21, max_value=65, value=30)
    with c2:
        monthly_income = st.number_input("Monthly Salary (₹) *", min_value=1000.0, value=60000.0, step=5000.0)
        employer_type  = st.selectbox("Employer Type *", ["Private Sector", "Government", "PSU", "MNC", "Startup"])
    with c3:
        cibil_score   = st.slider("CIBIL Score *", 300, 900, 720)
        existing_emi  = st.number_input("Existing EMI (₹/month)", min_value=0.0, value=5000.0, step=500.0)

    _section("2. Loan Details")
    l1, l2, l3 = st.columns(3)
    with l1:
        loan_amount = st.number_input("Loan Amount (₹) *", min_value=50000.0, max_value=float(cfg["max_amt"]), value=500000.0, step=25000.0)
    with l2:
        loan_purpose = st.selectbox("Loan Purpose *", ["Medical Emergency", "Wedding", "Travel", "Debt Consolidation", "Home Renovation", "Electronics", "Other"])
    with l3:
        tenure_years = st.slider("Tenure (Years)", cfg["min_yr"], cfg["max_yr"], cfg["default_yr"])

    prev_defaults   = st.selectbox("Previous Loan Defaults", [0, 1, 2, 3])
    credit_card_use = st.slider("Credit Card Utilization (%)", 0, 100, 25) / 100.0
    _emi_preview(is_dark, loan_amount, cfg["rate"], tenure_years * 12)

    return {
        "LoanType": cfg["key"], "fullName": full_name, "Age": age,
        "MonthlyIncome": monthly_income, "AnnualIncome": monthly_income * 12,
        "EmploymentType": employer_type, "CIBILScore": cibil_score,
        "LoanAmount": loan_amount, "LoanTenureYears": tenure_years,
        "ExistingEMI": existing_emi, "BankBalance": monthly_income * 3,
        "LoanPurpose": loan_purpose,
        "PreviousLoanDefaults": prev_defaults, "CreditCardUsage": credit_card_use,
    }

def _form_business(cfg, is_dark) -> dict:
    _section("1. Business Information")
    c1, c2, c3 = st.columns(3)
    with c1:
        full_name       = st.text_input("Business Owner Name *", value="Rajesh Kumar")
        business_name   = st.text_input("Business Name *", value="Kumar Enterprises")
    with c2:
        business_vintage = st.number_input("Business Vintage (Years) *", min_value=1, max_value=50, value=5)
        annual_turnover  = st.number_input("Annual Turnover (₹) *", min_value=100000.0, value=5000000.0, step=100000.0)
    with c3:
        net_profit  = st.number_input("Net Profit (₹) *", min_value=0.0, value=1200000.0, step=100000.0)
        gst_filed   = st.selectbox("GST Returns Filed", ["Yes — 2+ Years", "Yes — 1 Year", "No"])

    _section("2. Financial & Loan Details")
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        loan_amount = st.number_input("Loan Amount (₹) *", min_value=500000.0, max_value=float(cfg["max_amt"]), value=2000000.0, step=100000.0)
    with f2:
        cibil_score  = st.slider("Promoter CIBIL *", 300, 900, 700)
    with f3:
        existing_emi = st.number_input("Existing EMI (₹/month)", min_value=0.0, value=0.0, step=5000.0)
    with f4:
        tenure_years = st.slider("Tenure (Years)", cfg["min_yr"], cfg["max_yr"], cfg["default_yr"])

    itr_available = st.checkbox("ITR Available (2 Years)", value=True)
    prev_defaults = st.selectbox("Previous Defaults", [0, 1, 2])
    _emi_preview(is_dark, loan_amount, cfg["rate"], tenure_years * 12)

    monthly_income = net_profit / 12
    return {
        "LoanType": cfg["key"], "fullName": full_name, "BusinessName": business_name,
        "Age": 40, "MonthlyIncome": monthly_income, "AnnualIncome": annual_turnover,
        "EmploymentType": "Business Owner", "CIBILScore": cibil_score,
        "LoanAmount": loan_amount, "LoanTenureYears": tenure_years,
        "ExistingEMI": existing_emi, "BankBalance": net_profit * 0.5,
        "BusinessVintage": business_vintage, "AnnualTurnover": annual_turnover,
        "NetProfit": net_profit, "GSTFiled": gst_filed, "ITRAvailable": itr_available,
        "PreviousLoanDefaults": prev_defaults, "CreditCardUsage": 0.2,
    }

def _form_education(cfg, is_dark) -> dict:
    _section("1. Student & Course Details")
    c1, c2, c3 = st.columns(3)
    with c1:
        full_name = st.text_input("Student Name *", value="Priya Sharma")
        course    = st.selectbox("Course *", ["B.Tech / BE", "M.Tech / ME", "MBA", "MBBS / MD", "BCA / MCA", "B.Sc / M.Sc", "PhD", "Diploma", "Other"])
    with c2:
        college     = st.text_input("College / University *", value="IIT Bombay")
        study_country = st.selectbox("Study Country *", ["India", "USA", "UK", "Canada", "Australia", "Germany", "Singapore", "Other"])
    with c3:
        annual_family_income = st.number_input("Annual Family Income (₹) *", min_value=50000.0, value=800000.0, step=50000.0)
        co_applicant         = st.selectbox("Co-Applicant *", ["Father", "Mother", "Spouse", "Guardian"])

    _section("2. Loan Details")
    l1, l2 = st.columns(2)
    with l1:
        loan_amount  = st.number_input("Loan Amount (₹) *", min_value=50000.0, max_value=float(cfg["max_amt"]), value=1500000.0, step=50000.0)
    with l2:
        tenure_years = st.slider("Repayment Tenure (Years, starts after course)", cfg["min_yr"], cfg["max_yr"], cfg["default_yr"])

    cibil_score = st.slider("Co-Applicant CIBIL Score *", 300, 900, 680)
    _emi_preview(is_dark, loan_amount, cfg["rate"], tenure_years * 12)

    monthly_income = annual_family_income / 12
    return {
        "LoanType": cfg["key"], "fullName": full_name, "Course": course,
        "College": college, "StudyCountry": study_country,
        "Age": 22, "MonthlyIncome": monthly_income, "AnnualIncome": annual_family_income,
        "EmploymentType": "Salaried", "CIBILScore": cibil_score,
        "LoanAmount": loan_amount, "LoanTenureYears": tenure_years,
        "ExistingEMI": 0.0, "BankBalance": annual_family_income * 0.2,
        "CoApplicant": co_applicant,
        "PreviousLoanDefaults": 0, "CreditCardUsage": 0.1,
    }

def _form_vehicle(cfg, is_dark) -> dict:
    _section("1. Vehicle & Personal Details")
    c1, c2, c3 = st.columns(3)
    with c1:
        full_name     = st.text_input("Full Name *", value="Arjun Patel")
        vehicle_type  = st.selectbox("Vehicle Type *", ["New Car", "Used Car", "New Bike / Two-Wheeler", "Used Bike", "Electric Vehicle", "Commercial Vehicle"])
    with c2:
        vehicle_price = st.number_input("Vehicle Price / On-Road Price (₹) *", min_value=50000.0, value=1200000.0, step=50000.0)
        down_payment  = st.number_input("Down Payment (₹) *", min_value=0.0, value=200000.0, step=25000.0)
    with c3:
        monthly_income = st.number_input("Monthly Income (₹) *", min_value=1000.0, value=55000.0, step=5000.0)
        existing_emi   = st.number_input("Existing EMI (₹/month)", min_value=0.0, value=5000.0, step=500.0)

    _section("2. Loan Details")
    v1, v2, v3 = st.columns(3)
    with v1:
        loan_amount  = st.number_input("Loan Amount (₹) *", min_value=50000.0, max_value=float(cfg["max_amt"]), value=min(vehicle_price - down_payment, float(cfg["max_amt"])), step=25000.0)
    with v2:
        cibil_score  = st.slider("CIBIL Score *", 300, 900, 700)
    with v3:
        tenure_years = st.slider("Tenure (Years)", cfg["min_yr"], cfg["max_yr"], cfg["default_yr"])

    prev_defaults   = st.selectbox("Previous Defaults", [0, 1, 2])
    credit_card_use = st.slider("Credit Card Utilization (%)", 0, 100, 20) / 100.0
    _emi_preview(is_dark, loan_amount, cfg["rate"], tenure_years * 12)

    return {
        "LoanType": cfg["key"], "fullName": full_name, "VehicleType": vehicle_type,
        "Age": 30, "MonthlyIncome": monthly_income, "AnnualIncome": monthly_income * 12,
        "EmploymentType": "Salaried", "CIBILScore": cibil_score,
        "LoanAmount": loan_amount, "LoanTenureYears": tenure_years,
        "ExistingEMI": existing_emi, "BankBalance": down_payment + monthly_income,
        "VehiclePrice": vehicle_price, "DownPayment": down_payment,
        "PreviousLoanDefaults": prev_defaults, "CreditCardUsage": credit_card_use,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Main render
# ─────────────────────────────────────────────────────────────────────────────
def render():
    render_banner(
        title="AI Credit Risk & Loan Approval Assessment",
        subtitle="Select your loan type, complete the form, and get an instant AI-powered approval decision with full EMI breakdown.",
        icon="📝"
    )

    is_dark = st.session_state.get("theme", "light") == "dark"

    # Show result view if we have a result
    if st.session_state.get("show_loan_result") and st.session_state.get("last_prediction_result"):
        render_prediction_result_view(st.session_state["last_prediction_result"], is_dark)
        return

    # ── Step 1: Loan Type Selector ────────────────────────────────────────────
    title_color = "#60A5FA" if is_dark else "#1E3A8A"
    text_color  = "#FFFFFF" if is_dark else "#0F172A"
    card_bg     = "#1E293B" if is_dark else "#FFFFFF"
    border_c    = "#334155" if is_dark else "#CBD5E1"

    st.markdown(
        f"""
        <div style="background:{card_bg};border:2px solid {border_c};border-radius:16px;
                    padding:22px 28px;margin-bottom:24px;box-shadow:0 6px 20px rgba(0,0,0,0.06);">
            <div style="font-size:0.9rem;font-weight:800;text-transform:uppercase;
                        letter-spacing:0.05em;color:{title_color};margin-bottom:6px;">
                Step 1 — Choose Your Loan Type
            </div>
            <div style="font-size:1rem;color:{text_color};font-weight:600;">
                Select a loan type to see the relevant form with auto-calculated interest rates and tenure limits.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    loan_type_label = st.selectbox(
        "Loan Type *",
        list(LOAN_CONFIG.keys()),
        key="loan_type_selector"
    )
    cfg = LOAN_CONFIG[loan_type_label]

    # Info banner for selected loan type
    st.markdown(
        f"""
        <div style="background:linear-gradient(135deg,#1E3A8A,#2563EB);color:#fff;
                    border-radius:14px;padding:16px 24px;margin:12px 0 20px 0;
                    display:flex;gap:24px;flex-wrap:wrap;align-items:center;">
            <div style="font-size:2.5rem;">{cfg['icon']}</div>
            <div>
                <div style="font-size:1.2rem;font-weight:800;">{cfg['key']}</div>
                <div style="font-size:0.95rem;opacity:0.9;">
                    Interest: <b>{cfg['rate']}% p.a.</b> &nbsp;|&nbsp;
                    Tenure: <b>{cfg['min_yr']}–{cfg['max_yr']} Years</b> &nbsp;|&nbsp;
                    Max: <b>₹{cfg['max_amt']:,.0f}</b>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ── Step 2: Dynamic Form ─────────────────────────────────────────────────
    st.markdown(
        f"""<div style="font-size:0.9rem;font-weight:800;text-transform:uppercase;
                        letter-spacing:0.05em;color:{title_color};margin-bottom:12px;">
                Step 2 — Fill Application Details</div>""",
        unsafe_allow_html=True
    )

    form_builders = {
        "🏠 Home Loan":      _form_home,
        "👤 Personal Loan":  _form_personal,
        "🏢 Business Loan":  _form_business,
        "🎓 Education Loan": _form_education,
        "🚗 Vehicle Loan":   _form_vehicle,
    }

    with st.form("loan_application_form"):
        payload = form_builders[loan_type_label](cfg, is_dark)

        st.markdown("<br>", unsafe_allow_html=True)
        b1, b2 = st.columns(2)
        with b1:
            submit_btn = st.form_submit_button("🔮 Run AI Prediction", use_container_width=True)
        with b2:
            back_btn = st.form_submit_button("🏠 Back to Home", use_container_width=True)

    if back_btn:
        st.session_state["current_page"] = "Home"
        st.rerun()

    if submit_btn:
        _run_prediction(payload, is_dark)


def _run_prediction(payload: dict, is_dark: bool):
    """Executes the API call with loading animation."""
    box_bg     = "#1E293B" if is_dark else "#FFFFFF"
    box_border = "#3B82F6" if is_dark else "#1E3A8A"
    title_color = "#60A5FA" if is_dark else "#1E3A8A"

    loading_box = st.empty()
    with loading_box.container():
        st.markdown(
            f"""
            <div style="background:{box_bg};border:3px dashed {box_border};border-radius:18px;
                        padding:28px;text-align:center;margin:20px 0;box-shadow:0 12px 30px rgba(0,0,0,0.15);">
                <div style="font-size:2.8rem;margin-bottom:6px;">⚡</div>
                <h3 style="color:{title_color} !important;margin:0;font-weight:800;">
                    Analyzing {payload.get('LoanType', 'Loan')} Application...
                </h3>
                <p style="font-size:1rem;margin-top:6px;font-weight:700;">
                    Executing Gradient Boosting Scoring Engine
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        prog_bar  = st.progress(0)
        step_text = st.empty()
        for msg, pct in [
            ("Validating financial profile", 20),
            ("Checking CIBIL eligibility", 40),
            ("Computing DTI ratio", 60),
            ("Running Gradient Boosting Model", 80),
            ("Preparing recommendation", 100),
        ]:
            step_text.markdown(
                f"<p style='color:#16A34A !important;font-weight:800;font-size:1.1rem;text-align:center;'>✔ {msg}</p>",
                unsafe_allow_html=True
            )
            prog_bar.progress(pct)
            time.sleep(0.3)

    loading_box.empty()

    # API call → fallback
    parsed_res = None
    api_base   = get_api_url()
    try:
        res = requests.post(f"{api_base}/api/predict/public", json=payload, timeout=8)
        if res.status_code == 200:
            outer = res.json().get("data", {})
            parsed_res = outer.get("result") or outer.get("prediction")
    except Exception:
        pass

    if not parsed_res:
        try:
            from ml.predictor import ml_predictor
            parsed_res = ml_predictor.predict(payload)
        except Exception as ex:
            st.error(f"❌ Prediction Error: {ex}")
            return

    if parsed_res:
        st.session_state["last_prediction_result"]  = parsed_res
        st.session_state["show_loan_result"]         = True
        st.session_state["last_monthly_income"]      = payload.get("MonthlyIncome", 45000)
        st.session_state["last_existing_emi"]        = payload.get("ExistingEMI", 0)
        st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# Result View
# ─────────────────────────────────────────────────────────────────────────────
def render_prediction_result_view(result_data: dict, is_dark: bool):
    approved      = result_data.get("approved", False)
    prob          = result_data.get("approval_probability", 50.0)
    status_str    = "Loan Approved ✅" if approved else "Loan Declined ❌"
    risk_level    = result_data.get("credit_risk_level", "Medium")
    risk_color    = "#16A34A" if approved else "#DC2626"
    loan_type     = result_data.get("loan_type", "Loan")
    loan_icon     = result_data.get("loan_type_icon", "💰")
    emi           = result_data.get("emi_estimate", 0)
    total_int     = result_data.get("total_interest", 0)
    total_pay     = result_data.get("total_payment", 0)
    tenure_years  = result_data.get("tenure_years", 0)
    interest_rate = result_data.get("interest_rate_estimate", 0)
    loan_amount   = result_data.get("loan_amount", 0)
    suggested_max = result_data.get("suggested_max_loan", 0)

    outcome_bg = (
        "#064E3B" if (is_dark and approved) else
        "#7F1D1D" if is_dark else
        "#F0FDF4" if approved else "#FEF2F2"
    )
    card_bg    = "#1E293B" if is_dark else "#FFFFFF"
    border_c   = "#475569" if is_dark else "#CBD5E1"
    title_color = "#60A5FA" if is_dark else "#1E3A8A"
    text_color  = "#FFFFFF" if is_dark else "#0F172A"

    st.markdown(f"<h2 style='color:{text_color} !important;'>📊 Prediction Result</h2>", unsafe_allow_html=True)

    # ── Status Banner ────────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div style="background:{outcome_bg};border:3px solid {risk_color};border-radius:18px;
                    padding:28px 32px;margin-bottom:24px;display:flex;align-items:center;
                    justify-content:space-between;flex-wrap:wrap;gap:16px;
                    box-shadow:0 12px 28px rgba(0,0,0,0.15);">
            <div>
                <div style="font-size:0.9rem;font-weight:800;text-transform:uppercase;
                            letter-spacing:0.05em;color:#FFFFFF !important;">{loan_icon} {loan_type} — DECISION</div>
                <div style="font-size:2.4rem;font-weight:800;color:{risk_color} !important;margin-top:4px;">{status_str}</div>
                <div style="font-size:1.05rem;color:#FFFFFF !important;margin-top:4px;">
                    Approval Probability: <b>{prob:.1f}%</b> &nbsp;|&nbsp;
                    Interest Rate: <b>{interest_rate}% p.a.</b> &nbsp;|&nbsp;
                    Tenure: <b>{tenure_years} Years</b>
                </div>
            </div>
            <div style="background:{risk_color};color:#FFFFFF !important;font-size:1.1rem;
                        font-weight:800;padding:12px 28px;border-radius:999px;box-shadow:0 6px 16px rgba(0,0,0,0.2);">
                {risk_level} Risk Tier
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ── Key Metrics Row ───────────────────────────────────────────────────────
    m1, m2, m3 = st.columns(3)
    with m1:
        render_metric_card("Approval Probability", f"{prob:.1f}%", "Gradient Boosting Score", risk_color, "🎯")
    with m2:
        render_metric_card("Max Eligible Amount", f"₹{suggested_max:,.0f}", "50% DTI Cap Ceiling", "#16A34A", "💵")
    with m3:
        render_metric_card("Monthly EMI", f"₹{emi:,.2f}", f"@ {interest_rate}% APR", "#2563EB", "💳")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── EMI Full Breakdown Card ───────────────────────────────────────────────
    st.markdown(f"<h3 style='color:{text_color} !important;'>💰 EMI & Cost Breakdown</h3>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="background:{card_bg};border:2px solid {border_c};border-radius:16px;
                    padding:24px 28px;margin-bottom:24px;box-shadow:0 6px 18px rgba(0,0,0,0.06);">
            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:20px;">
                <div style="text-align:center;padding:16px;background:{'#0F172A' if is_dark else '#F8FAFC'};border-radius:12px;">
                    <div style="font-size:0.8rem;font-weight:800;color:{title_color};text-transform:uppercase;letter-spacing:0.05em;">Loan Amount</div>
                    <div style="font-size:1.8rem;font-weight:800;color:{text_color};">₹{loan_amount:,.0f}</div>
                </div>
                <div style="text-align:center;padding:16px;background:{'#0F172A' if is_dark else '#F8FAFC'};border-radius:12px;">
                    <div style="font-size:0.8rem;font-weight:800;color:{title_color};text-transform:uppercase;letter-spacing:0.05em;">Interest Rate</div>
                    <div style="font-size:1.8rem;font-weight:800;color:{text_color};">{interest_rate}% p.a.</div>
                </div>
                <div style="text-align:center;padding:16px;background:{'#0F172A' if is_dark else '#F8FAFC'};border-radius:12px;">
                    <div style="font-size:0.8rem;font-weight:800;color:{title_color};text-transform:uppercase;letter-spacing:0.05em;">Tenure</div>
                    <div style="font-size:1.8rem;font-weight:800;color:{text_color};">{tenure_years} Yrs</div>
                </div>
                <div style="text-align:center;padding:16px;background:linear-gradient(135deg,#1E3A8A,#2563EB);border-radius:12px;">
                    <div style="font-size:0.8rem;font-weight:800;color:#93C5FD;text-transform:uppercase;letter-spacing:0.05em;">Monthly EMI</div>
                    <div style="font-size:1.8rem;font-weight:800;color:#FFFFFF;">₹{emi:,.2f}</div>
                </div>
                <div style="text-align:center;padding:16px;background:{'#0F172A' if is_dark else '#F8FAFC'};border-radius:12px;">
                    <div style="font-size:0.8rem;font-weight:800;color:#F59E0B;text-transform:uppercase;letter-spacing:0.05em;">Total Interest</div>
                    <div style="font-size:1.8rem;font-weight:800;color:#F59E0B;">₹{total_int:,.0f}</div>
                </div>
                <div style="text-align:center;padding:16px;background:{'#0F172A' if is_dark else '#F8FAFC'};border-radius:12px;">
                    <div style="font-size:0.8rem;font-weight:800;color:{title_color};text-transform:uppercase;letter-spacing:0.05em;">Total Payment</div>
                    <div style="font-size:1.8rem;font-weight:800;color:{text_color};">₹{total_pay:,.0f}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ── Charts ────────────────────────────────────────────────────────────────
    monthly_inc  = st.session_state.get("last_monthly_income", 45000.0)
    exist_emi    = st.session_state.get("last_existing_emi", 0.0)
    ch1, ch2 = st.columns(2)
    with ch1:
        st.plotly_chart(create_approval_meter(prob), use_container_width=True)
    with ch2:
        st.plotly_chart(create_income_vs_emi_chart(monthly_inc, exist_emi, emi), use_container_width=True)

    # ── Required Documents ────────────────────────────────────────────────────
    req_docs = result_data.get("required_documents", [])
    if req_docs:
        st.markdown(f"<h3 style='color:{text_color} !important;'>📋 Required Documents</h3>", unsafe_allow_html=True)
        docs_html = "".join([
            f"<div style='display:flex;align-items:center;gap:10px;padding:10px 16px;"
            f"border-radius:10px;margin-bottom:8px;"
            f"background:{'#1E293B' if is_dark else '#F8FAFC'};"
            f"border:1px solid {'#334155' if is_dark else '#E2E8F0'};'>"
            f"<span style='color:#16A34A;font-size:1.1rem;'>✅</span>"
            f"<span style='color:{text_color};font-weight:700;font-size:0.95rem;'>{doc}</span></div>"
            for doc in req_docs
        ])
        st.markdown(
            f"<div style='background:{card_bg};border:2px solid {border_c};border-radius:16px;padding:20px 24px;margin-bottom:20px;'>{docs_html}</div>",
            unsafe_allow_html=True
        )

    # ── Recommendation & Tips ─────────────────────────────────────────────────
    st.markdown(f"<h3 style='color:{text_color} !important;'>💡 AI Recommendation & Financial Tips</h3>", unsafe_allow_html=True)
    st.info(result_data.get("recommendation", ""))

    tips = result_data.get("financial_improvement_tips", [])
    for tip in tips:
        render_tip_box(tip)

    st.markdown("---")

    # ── Action Buttons ────────────────────────────────────────────────────────
    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("📈 Calculate CIBIL Score", key="res_btn_cibil", use_container_width=True):
            st.session_state["show_loan_result"] = False
            st.session_state["current_page"]     = "CibilCalculator"
            st.rerun()
    with b2:
        if st.button("📝 New Loan Application", key="res_btn_new", use_container_width=True):
            st.session_state["show_loan_result"] = False
            st.rerun()
    with b3:
        if st.button("🏠 Back to Home", key="res_btn_home", use_container_width=True):
            st.session_state["show_loan_result"] = False
            st.session_state["current_page"]     = "Home"
            st.rerun()
