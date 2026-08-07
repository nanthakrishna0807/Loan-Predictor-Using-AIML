import streamlit as st
import time
import os
import sys

# Ensure the project root is on sys.path so backend imports resolve correctly
_FRONTEND_DIR = os.path.dirname(os.path.abspath(__file__))
_ROOT_DIR = os.path.dirname(_FRONTEND_DIR)
if _ROOT_DIR not in sys.path:
    sys.path.insert(0, _ROOT_DIR)

try:
    from backend.utils.cibil_calculator import calculate_cibil_score
except ModuleNotFoundError:
    from utils.cibil_calculator import calculate_cibil_score

try:
    from frontend.components.charts import create_cibil_gauge
    from frontend.components.cards import render_banner
except ModuleNotFoundError:
    from components.charts import create_cibil_gauge
    from components.cards import render_banner

def render():
    render_banner(
        title="Interactive CIBIL Score Calculator & Credit Rating Diagnostic",
        subtitle="Simulate key credit behavior factors to estimate your CIBIL score (300-900), evaluate credit risk tiers, and receive personalized recommendations.",
        icon="📈"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    
    is_dark = st.session_state.get("theme", "light") == "dark"
    card_bg = "#1E293B" if is_dark else "#FFFFFF"
    border_color = "#475569" if is_dark else "#CBD5E1"
    title_color = "#60A5FA" if is_dark else "#1E3A8A"
    text_primary = "#FFFFFF" if is_dark else "#0F172A"
    text_secondary = "#E2E8F0" if is_dark else "#0F172A"

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown(
            f"""
            <div style="background-color: {card_bg}; border: 2px solid {border_color}; border-radius: 16px; padding: 24px; box-shadow: 0 8px 20px rgba(0,0,0,0.06);">
                <h3 style="margin-top: 0; margin-bottom: 8px; color: {title_color} !important;">🧮 Financial Parameters Input</h3>
                <p style="font-size: 1rem; margin-bottom: 20px; color: {text_secondary} !important; font-weight: 600;">Adjust your credit history and payment variables to calculate your estimated CIBIL score.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)

        with st.form("cibil_calc_form"):
            on_time = st.slider(
                "1. Payment History - On-Time Payments (%)",
                min_value=0, max_value=100, value=95, step=5,
                help="Percentage of loan EMIs and credit card bills paid on or before due date."
            )

            utilization = st.slider(
                "2. Credit Utilization Ratio (%)",
                min_value=0, max_value=100, value=25, step=5,
                help="Total active balance divided by total approved credit card limits. (Ideal: < 30%)"
            )

            history_years = st.slider(
                "3. Credit History Age (Years)",
                min_value=0.0, max_value=20.0, value=5.0, step=0.5,
                help="Total duration since your first credit card or loan account was opened."
            )

            col_sub1, col_sub2 = st.columns(2)
            with col_sub1:
                inquiries = st.number_input(
                    "4. Hard Inquiries (Past 12 M)",
                    min_value=0, max_value=20, value=1, step=1,
                    help="Number of official credit inquiries initiated by lenders."
                )
                active_accounts = st.number_input(
                    "5. Credit Mix (Total Active Accounts)",
                    min_value=1, max_value=30, value=4, step=1,
                    help="Total credit cards, personal loans, and active accounts."
                )

            with col_sub2:
                defaults = st.number_input(
                    "6. Past Defaulted Accounts",
                    min_value=0, max_value=10, value=0, step=1,
                    help="Number of accounts written off or overdue by more than 90 days."
                )

            st.markdown("<br>", unsafe_allow_html=True)

            # Form Action Buttons (📊 Calculate Score & 🏠 Back to Home)
            cibil_b1, cibil_b2 = st.columns(2)
            with cibil_b1:
                submit_cibil = st.form_submit_button("📊 Calculate Score", use_container_width=True)
            with cibil_b2:
                back_btn_cibil = st.form_submit_button("🏠 Back to Home", use_container_width=True)

        if back_btn_cibil:
            st.session_state["current_page"] = "Home"
            st.rerun()

    with col2:
        if submit_cibil:
            # Banking Style CIBIL Loading Animation
            loading_container = st.empty()
            with loading_container.container():
                box_bg = "#1E293B" if is_dark else "#FFFFFF"
                box_border = "#3B82F6" if is_dark else "#1E3A8A"

                st.markdown(
                    f"""
                    <div style="background-color: {box_bg}; border: 3px dashed {box_border}; border-radius: 16px; padding: 24px; text-align: center; margin-bottom: 18px;">
                        <h3 style="color: {title_color} !important; margin: 0; font-weight: 800;">Calculating CIBIL Score...</h3>
                        <p style="font-size: 1rem; margin-top: 6px; font-weight: 700;">Processing bureau scoring metrics...</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                prog_bar = st.progress(0)
                status_box = st.empty()

                steps = [
                    ("Payment History", 20),
                    ("Credit Utilization", 40),
                    ("Credit Age", 60),
                    ("Hard Inquiries", 80),
                    ("Credit Mix", 100)
                ]

                for msg, pct in steps:
                    status_box.markdown(f"<p style='color: #16A34A !important; font-weight: 800; font-size: 1.15rem; text-align: center;'>✔ {msg}</p>", unsafe_allow_html=True)
                    prog_bar.progress(pct)
                    time.sleep(0.25)

            loading_container.empty()

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
            breakdown = res.get("breakdown", {})

            # Display Result Score Card
            st.markdown(
                f"""
                <div style="background-color: {card_bg}; border: 3px solid {color}; border-radius: 18px; padding: 26px; box-shadow: 0 12px 28px rgba(0,0,0,0.1); text-align: center;">
                    <div style="font-size: 0.9rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; color: {text_primary} !important;">ESTIMATED CIBIL SCORE</div>
                    <div style="font-size: 3.8rem; font-weight: 800; color: {color} !important; margin: 4px 0;">{score}</div>
                    <div style="display: inline-block; background-color: {color}; color: #FFFFFF !important; font-weight: 800; font-size: 1.1rem; padding: 8px 24px; border-radius: 999px;">
                        {cat} Credit Rating
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.plotly_chart(create_cibil_gauge(score), use_container_width=True)

            st.markdown(f"<h3 style='color: {text_primary} !important;'>📊 Score Weight Distribution</h3>", unsafe_allow_html=True)
            b_col1, b_col2 = st.columns(2)
            with b_col1:
                st.metric("Payment History (35%)", f"{breakdown.get('payment_history', 0)} pts")
                st.metric("Credit Utilization (30%)", f"{breakdown.get('credit_utilization', 0)} pts")
                st.metric("Credit History Age (15%)", f"{breakdown.get('history_length', 0)} pts")
            with b_col2:
                st.metric("Credit Mix (10%)", f"{breakdown.get('credit_mix', 0)} pts")
                st.metric("Inquiry & Default Penalty (10%)", f"{breakdown.get('behavior', 0)} pts")

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='color: {text_primary} !important;'>💡 Personalized Recommendations</h3>", unsafe_allow_html=True)

            tips = []
            if on_time < 90:
                tips.append("Automate Monthly EMI Payments: Set up standing instructions or auto-debits to avoid payment default marks.")
            if utilization > 30:
                tips.append("Lower Utilization below 30%: Request higher credit limits or clear card balances mid-cycle.")
            if inquiries > 2:
                tips.append("Limit Hard Inquiries: Avoid applying for multiple new credit cards or loan accounts within 6 months.")
            if defaults > 0:
                tips.append("Clear Pending Overdues: Settle defaulted accounts with credit providers to update bureau records.")
            if not tips:
                tips.append("Maintain Excellent Discipline: Keep utilization under 30% and maintain 100% on-time EMI repayments.")

            for t in tips:
                tip_bg = "#064E3B" if is_dark else "#F0FDF4"
                tip_text = "#FFFFFF" if is_dark else "#0F172A"
                st.markdown(
                    f"""
                    <div style="background-color: {tip_bg}; border-left: 6px solid #16A34A; border: 2px solid #16A34A; padding: 14px 18px; border-radius: 12px; margin-bottom: 10px; color: {tip_text} !important; font-weight: 700; font-size: 1rem;">
                        💡 {t}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown("---")
            if st.button("🏠 Back to Home", key="cibil_res_back_home", use_container_width=True):
                st.session_state["current_page"] = "Home"
                st.rerun()

        else:
            placeholder_bg = "#1E293B" if is_dark else "#FFFFFF"
            placeholder_border = "#475569" if is_dark else "#CBD5E1"
            st.markdown(
                f"""
                <div style="background-color: {placeholder_bg}; border: 2px dashed {placeholder_border}; border-radius: 16px; padding: 48px 24px; text-align: center; margin-top: 10px;">
                    <div style="font-size: 3.5rem; margin-bottom: 14px;">📈</div>
                    <h4 style="margin: 0; font-size: 1.3rem; font-weight: 800; color: {title_color} !important;">Calculate Your CIBIL Score Rating</h4>
                    <p style="font-size: 1.05rem; max-width: 440px; margin: 12px auto 0 auto; color: {text_secondary} !important; font-weight: 600; line-height: 1.6;">
                        Adjust your parameters on the left and click <b>Calculate Score</b> to view your credit score breakdown, visual gauge, and personalized recommendations.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🏠 Back to Home", key="cibil_placeholder_back_home", use_container_width=True):
                st.session_state["current_page"] = "Home"
                st.rerun()

    st.markdown("---")
