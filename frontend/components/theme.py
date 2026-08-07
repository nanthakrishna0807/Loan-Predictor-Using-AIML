import streamlit as st
import os

try:
    from frontend.config import API_URL
except ModuleNotFoundError:
    try:
        from config import API_URL
    except ModuleNotFoundError:
        API_URL = os.getenv("API_URL", os.getenv("BACKEND_API_URL", "https://loan-predictor-ml-model.onrender.com"))

def get_backend_url() -> str:
    """
    Returns the backend API base URL.
    """
    return API_URL.rstrip('/')

def apply_banking_theme():
    """
    Injects high-contrast Light Mode or Dark Mode banking theme CSS into Streamlit.
    Theme choice is stored in st.session_state.get("theme", "light").
    """
    theme = st.session_state.get("theme", "light").lower()
    is_dark = (theme == "dark")

    if is_dark:
        bg_gradient = "#0F172A"
        card_bg = "#1E293B"
        sidebar_bg = "#0B132B"
        primary_color = "#2563EB"
        primary_hover = "#3B82F6"
        text_primary = "#FFFFFF"
        text_secondary = "#E2E8F0"
        border_color = "#475569"
        hover_bg = "#334155"
        input_bg = "#0F172A"
        input_text = "#FFFFFF"
        input_border = "#64748B"
        banner_bg = "linear-gradient(135deg, #1E3A8A 0%, #1E40AF 60%, #2563EB 100%)"
        card_title_color = "#60A5FA"
        header_box_bg = "#1E293B"
    else:
        bg_gradient = "#F8FAFC"
        card_bg = "#FFFFFF"
        sidebar_bg = "#FFFFFF"
        primary_color = "#1E3A8A"
        primary_hover = "#2563EB"
        text_primary = "#0F172A"
        text_secondary = "#1E293B"
        border_color = "#CBD5E1"
        hover_bg = "#EEF4FF"
        input_bg = "#FFFFFF"
        input_text = "#0F172A"
        input_border = "#64748B"
        banner_bg = "linear-gradient(135deg, #1E3A8A 0%, #1E40AF 60%, #2563EB 100%)"
        card_title_color = "#1E3A8A"
        header_box_bg = "#F1F5F9"

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Poppins:wght@500;600;700;800&display=swap');

        /* Global Typography & Background */
        html, body, [class*="css"] {{
            font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
            background-color: {bg_gradient} !important;
            color: {text_primary} !important;
        }}

        .stApp {{
            background-color: {bg_gradient} !important;
        }}

        /* Universal Strict High Contrast Text Enforcement */
        p, div, span, label, li, small, [data-testid="stMarkdownContainer"] p {{
            color: {text_primary} !important;
            font-weight: 500;
        }}

        /* Headings */
        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Poppins', 'Inter', sans-serif !important;
            color: {text_primary} !important;
            font-weight: 800 !important;
            letter-spacing: -0.02em;
        }}

        /* Sidebar Styling */
        [data-testid="stSidebar"] {{
            background-color: {sidebar_bg} !important;
            border-right: 2px solid {border_color} !important;
            box-shadow: 4px 0 20px rgba(0, 0, 0, 0.08);
        }}
        [data-testid="stSidebar"] * {{
            color: {text_primary} !important;
        }}
        [data-testid="stSidebar"] .stMarkdown p {{
            color: {text_secondary} !important;
            font-weight: 700 !important;
        }}

        /* Enterprise Cards */
        .enterprise-card {{
            background-color: {card_bg} !important;
            border: 2px solid {border_color} !important;
            border-radius: 16px !important;
            padding: 24px !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08) !important;
            position: relative !important;
            overflow: hidden !important;
            transition: all 0.25s ease-in-out !important;
            margin-bottom: 18px !important;
        }}
        .enterprise-card::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
            background: linear-gradient(90deg, #1E3A8A 0%, #2563EB 50%, #16A34A 100%);
        }}
        .enterprise-card:hover {{
            transform: translateY(-3px) scale(1.01) !important;
            box-shadow: 0 16px 32px rgba(0, 0, 0, 0.15) !important;
            border-color: {primary_color} !important;
        }}

        .card-label {{
            font-size: 0.9rem !important;
            color: {card_title_color} !important;
            font-weight: 800 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
        }}
        .card-value {{
            font-size: 2.1rem !important;
            color: {text_primary} !important;
            font-weight: 800 !important;
            margin-top: 6px !important;
            margin-bottom: 4px !important;
        }}
        .card-title-text {{
            font-size: 1.3rem !important;
            font-weight: 800 !important;
            color: {card_title_color} !important;
            margin-bottom: 8px !important;
        }}
        .card-body-text {{
            font-size: 1rem !important;
            font-weight: 600 !important;
            color: {text_primary} !important;
            line-height: 1.55 !important;
        }}

        /* Section Header Box */
        .section-header-box {{
            background-color: {header_box_bg} !important;
            border: 2px solid {border_color} !important;
            border-left: 6px solid {primary_color} !important;
            border-radius: 14px !important;
            padding: 16px 22px !important;
            margin-bottom: 18px !important;
            margin-top: 10px !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
        }}
        .section-header-title {{
            font-size: 1.25rem !important;
            font-weight: 800 !important;
            color: {card_title_color} !important;
            letter-spacing: 0.02em !important;
        }}

        /* Royal Banner Header */
        .enterprise-banner {{
            background: {banner_bg} !important;
            color: #FFFFFF !important;
            padding: 34px 40px !important;
            border-radius: 20px !important;
            margin-bottom: 24px !important;
            box-shadow: 0 14px 30px rgba(30, 58, 138, 0.35) !important;
        }}
        .enterprise-banner h1 {{
            color: #FFFFFF !important;
            margin-bottom: 8px !important;
            font-size: 2.2rem !important;
            font-weight: 800 !important;
        }}
        .enterprise-banner p {{
            color: #FFFFFF !important;
            font-size: 1.1rem !important;
            margin: 0 !important;
            font-weight: 600 !important;
        }}

        /* High-Contrast Interactive Buttons */
        .stButton>button {{
            background-color: {primary_color} !important;
            color: #FFFFFF !important;
            font-weight: 800 !important;
            font-size: 1rem !important;
            border-radius: 14px !important;
            padding: 12px 24px !important;
            border: 2px solid {primary_color} !important;
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15) !important;
            transition: all 0.25s ease-in-out !important;
            width: 100% !important;
            text-align: center !important;
        }}
        .stButton>button:hover {{
            background-color: {primary_hover} !important;
            border-color: {primary_hover} !important;
            color: #FFFFFF !important;
            transform: translateY(-2px) scale(1.02) !important;
            box-shadow: 0 12px 24px rgba(37, 99, 235, 0.4) !important;
        }}
        .stButton>button:active {{
            transform: translateY(0px) scale(0.99) !important;
        }}

        /* Form Submissions Buttons inside Forms */
        .stFormSubmitButton>button {{
            background-color: {primary_color} !important;
            color: #FFFFFF !important;
            font-weight: 800 !important;
            font-size: 1rem !important;
            border-radius: 14px !important;
            padding: 12px 24px !important;
            border: 2px solid {primary_color} !important;
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15) !important;
            width: 100% !important;
        }}
        .stFormSubmitButton>button:hover {{
            background-color: {primary_hover} !important;
            border-color: {primary_hover} !important;
            color: #FFFFFF !important;
            transform: translateY(-2px) scale(1.02) !important;
            box-shadow: 0 12px 24px rgba(37, 99, 235, 0.4) !important;
        }}

        /* Sidebar Navigation Buttons */
        [data-testid="stSidebar"] .stButton>button {{
            background: transparent !important;
            color: {text_primary} !important;
            border: 1px solid transparent !important;
            box-shadow: none !important;
            text-align: left !important;
            justify-content: flex-start !important;
            padding: 12px 18px !important;
            font-size: 1rem !important;
            font-weight: 800 !important;
            border-radius: 12px !important;
        }}
        [data-testid="stSidebar"] .stButton>button:hover {{
            background: {hover_bg} !important;
            border: 1px solid {border_color} !important;
            color: {primary_color} !important;
            transform: translateX(6px) !important;
        }}

        /* Form Controls High Contrast */
        div[data-baseweb="input"] {{
            border-radius: 12px !important;
            border: 2px solid {input_border} !important;
            background-color: {input_bg} !important;
        }}
        div[data-baseweb="input"] input {{
            color: {input_text} !important;
            font-weight: 800 !important;
            font-size: 1.05rem !important;
        }}
        div[data-baseweb="select"] {{
            border-radius: 12px !important;
            border: 2px solid {input_border} !important;
            background-color: {input_bg} !important;
        }}
        div[data-baseweb="select"] * {{
            color: {input_text} !important;
            font-weight: 800 !important;
        }}

        /* Form Input Labels */
        label, [data-testid="stWidgetLabel"] p {{
            color: {text_primary} !important;
            font-weight: 800 !important;
            font-size: 0.98rem !important;
        }}

        /* Hide Streamlit default headers */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        </style>
        """,
        unsafe_allow_html=True
    )

def render_top_header_bar():
    """
    Renders the shared header bar with theme toggle.
    Guard: uses a per-run flag '_header_bar_rendered' so this function
    is safe to call from multiple places — it will only render once per
    Streamlit script execution, preventing DuplicateElementKey errors.
    """
    # Per-run guard: skip if already rendered this execution
    if st.session_state.get("_header_bar_rendered", False):
        return
    st.session_state["_header_bar_rendered"] = True

    theme = st.session_state.get("theme", "light").lower()
    is_dark = (theme == "dark")

    col_logo, col_space, col_toggle = st.columns([2.5, 1, 1.8])
    with col_logo:
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; gap: 12px; padding: 4px 0;">
                <span style="font-size: 2rem;">🏦</span>
                <div>
                    <div style="font-size: 1.35rem; font-weight: 800; line-height: 1.1; color: {'#FFFFFF' if is_dark else '#0F172A'};">AI Loan Predictor</div>
                    <div style="font-size: 0.8rem; font-weight: 700; color: {'#60A5FA' if is_dark else '#1E3A8A'};">Enterprise Banking Intelligence</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col_toggle:
        toggle_label = "☀️ Switch to Light Mode" if is_dark else "🌙 Switch to Dark Mode"
        if st.button(toggle_label, key="header_theme_toggle_btn", use_container_width=True):
            st.session_state["theme"] = "light" if is_dark else "dark"
            st.session_state["_header_bar_rendered"] = False  # reset for next run
            st.rerun()
    hr_color = "#334155" if is_dark else "#CBD5E1"
    st.markdown(
        f"<hr style='margin: 12px 0 20px 0; border: 0; border-top: 2px solid {hr_color};'>",
        unsafe_allow_html=True
    )
