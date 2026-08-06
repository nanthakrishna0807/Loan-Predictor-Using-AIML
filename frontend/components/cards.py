import streamlit as st

def render_metric_card(title: str, value: str, subtext: str = "", border_color: str = "#1E3A8A", icon: str = ""):
    """
    Renders an Enterprise Metric KPI card with top gradient line and high contrast text.
    """
    icon_html = f"<span style='font-size: 1.3rem; margin-right: 6px;'>{icon}</span>" if icon else ""
    st.markdown(
        f"""
        <div class="enterprise-card">
            <div class="card-label">{icon_html}{title}</div>
            <div class="card-value">{value}</div>
            {"<div class='card-subtext' style='color: " + border_color + " !important;'>" + subtext + "</div>" if subtext else ""}
        </div>
        """,
        unsafe_allow_html=True
    )

def render_status_badge(status: str):
    """
    Renders high-contrast status badge pill.
    """
    is_approved = status.lower() == "approved"
    pill_class = "badge-approved" if is_approved else "badge-rejected"
    icon = "✅" if is_approved else "❌"
    st.markdown(
        f"""
        <span class="{pill_class}">{icon} {status.upper()}</span>
        """,
        unsafe_allow_html=True
    )

def render_banner(title: str, subtitle: str, icon: str = "🏦"):
    """
    Renders an Enterprise Header Banner.
    """
    st.markdown(
        f"""
        <div class="enterprise-banner">
            <h1>{icon} {title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_tip_box(tip_text: str):
    """
    Renders a high-contrast recommendation tip box.
    """
    st.markdown(
        f"""
        <div style="background-color: #F0FDF4; border-left: 5px solid #16A34A; padding: 14px 18px; border-radius: 10px; margin-bottom: 10px; border-top: 1px solid #DCFCE7; border-right: 1px solid #DCFCE7; border-bottom: 1px solid #DCFCE7;">
            <span style="color: #15803D; font-weight: 700; font-size: 0.95rem;">💡 Recommendation:</span>
            <span style="color: #111827; font-size: 0.95rem; font-weight: 500; margin-left: 6px;">{tip_text}</span>
        </div>
        """,
        unsafe_allow_html=True
    )
