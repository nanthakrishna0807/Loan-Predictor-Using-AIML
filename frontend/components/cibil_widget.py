import streamlit as st
from backend.utils.cibil_calculator import calculate_cibil_score
from frontend.components.charts import create_cibil_gauge

def render_cibil_calculator_widget():
    st.markdown("### 🧮 Interactive CIBIL Score Estimator")
    st.markdown("<p style='color: #4B5563; font-size: 0.95rem;'>Adjust your financial parameters below to estimate your credit score.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        on_time = st.slider("On-time Payment History (%)", 0, 100, 95, 5, help="Percentage of bills paid on time")
        utilization = st.slider("Credit Card Utilization (%)", 0, 100, 25, 5, help="Percentage of total credit limit used")
        history_years = st.slider("Credit History Age (Years)", 0.0, 20.0, 4.0, 0.5)

    with col2:
        inquiries = st.number_input("Hard Credit Inquiries (Past 12 Mos)", 0, 15, 1)
        active_accounts = st.number_input("Active Credit Accounts/Loans", 1, 20, 3)
        defaults = st.number_input("Past Defaulted Accounts", 0, 10, 0)

    res = calculate_cibil_score(
        on_time_payment_pct=on_time,
        credit_utilization_pct=utilization,
        credit_history_years=history_years,
        hard_inquiries_past_year=inquiries,
        total_active_accounts=active_accounts,
        past_defaults_count=defaults
    )

    score = res["cibil_score"]
    cat = res["category"]
    color = res["color"]

    st.markdown("---")
    res_col1, res_col2 = st.columns([1.5, 1])

    with res_col1:
        st.plotly_chart(create_cibil_gauge(score), use_container_width=True)

    with res_col2:
        st.markdown(
            f"""
            <div style="background: #FFFFFF; border: 1px solid #E5E7EB; padding: 22px; border-radius: 12px; margin-top: 10px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
                <div style="font-size: 0.85rem; color: #4B5563; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">ESTIMATED SCORE</div>
                <div style="font-size: 2.5rem; font-weight: 800; color: {color}; margin-top: 4px;">{score}</div>
                <div style="display: inline-block; background-color: {color}15; color: {color}; font-weight: 700; padding: 6px 14px; border-radius: 999px; margin-top: 6px; border: 1px solid {color}44;">
                    {cat} Rating
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    return score
