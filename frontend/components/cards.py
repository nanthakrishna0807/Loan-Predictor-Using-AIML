import streamlit as st

def render_metric_card(title: str, value: str, subtext: str = "", border_color: str = "#1E3A8A", icon: str = ""):
    """
    Renders a High-Contrast Enterprise Metric Card.
    """
    is_dark = st.session_state.get("theme", "light") == "dark"
    sub_color = "#60A5FA" if is_dark else "#1E3A8A"
    
    icon_html = f"<span style='font-size: 1.4rem; margin-right: 8px;'>{icon}</span>" if icon else ""
    st.markdown(
        f"""
        <div class="enterprise-card">
            <div class="card-label">{icon_html}{title}</div>
            <div class="card-value">{value}</div>
            {"<div style='color: " + sub_color + " !important; font-weight: 800 !important; font-size: 0.95rem !important; margin-top: 6px;'>" + subtext + "</div>" if subtext else ""}
        </div>
        """,
        unsafe_allow_html=True
    )

def render_status_badge(status: str):
    """
    Renders a high-contrast status badge pill.
    """
    is_approved = status.lower() == "approved" or "approved" in status.lower()
    bg_color = "#16A34A" if is_approved else "#DC2626"
    icon = "✅" if is_approved else "❌"
    st.markdown(
        f"""
        <span style="background-color: {bg_color}; color: #FFFFFF !important; font-weight: 800; font-size: 0.9rem; padding: 8px 18px; border-radius: 999px; display: inline-block; letter-spacing: 0.05em; text-transform: uppercase; box-shadow: 0 4px 10px rgba(0,0,0,0.15);">
            {icon} {status.upper()}
        </span>
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
            <h1 style="color: #FFFFFF !important;">{icon} {title}</h1>
            <p style="color: #FFFFFF !important; font-weight: 600; font-size: 1.1rem;">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_tip_box(tip_text: str):
    """
    Renders a high-contrast recommendation tip box.
    """
    is_dark = st.session_state.get("theme", "light") == "dark"
    bg_color = "#064E3B" if is_dark else "#F0FDF4"
    border_color = "#22C55E" if is_dark else "#16A34A"
    text_color = "#FFFFFF" if is_dark else "#0F172A"
    label_color = "#4ADE80" if is_dark else "#15803D"

    st.markdown(
        f"""
        <div style="background-color: {bg_color}; border-left: 6px solid {border_color}; border: 2px solid {border_color}; padding: 16px 20px; border-radius: 12px; margin-bottom: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.04);">
            <span style="color: {label_color} !important; font-weight: 800; font-size: 1.05rem;">💡 Recommendation:</span>
            <span style="color: {text_color} !important; font-size: 1rem; font-weight: 700; margin-left: 8px;">{tip_text}</span>
        </div>
        """,
        unsafe_allow_html=True
    )
