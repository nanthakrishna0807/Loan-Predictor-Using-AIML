import streamlit as st

def apply_banking_theme():
    """
    Injects a modern light enterprise fintech design system into Streamlit.
    Palette:
    - Primary Background: #F8FAFC
    - Sidebar Background: #FFFFFF (White)
    - Primary Navy: #1E3A8A
    - Secondary Blue: #2563EB
    - Accent Sky: #0EA5E9
    - Success: #16A34A
    - Warning: #F59E0B
    - Danger: #DC2626
    - Text Primary: #111827 (Maximum Contrast)
    - Text Secondary: #4B5563
    - Card Background: #FFFFFF
    - Card Border: #E5E7EB
    - Hover: #EEF4FF
    """
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Poppins:wght@500;600;700&display=swap');

        /* Global Font & Background */
        html, body, [class*="css"] {
            font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
            background-color: #F8FAFC !important;
            color: #111827 !important;
            font-size: 16px;
        }

        .stApp {
            background-color: #F8FAFC !important;
        }

        /* Fixed White Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            border-right: 1px solid #E5E7EB !important;
            box-shadow: 2px 0 12px rgba(0, 0, 0, 0.03);
        }
        [data-testid="stSidebar"] * {
            color: #111827 !important;
        }
        [data-testid="stSidebar"] .stMarkdown p {
            color: #4B5563 !important;
        }
        
        /* Sidebar Navigation Radio Buttons */
        [data-testid="stSidebar"] div[role="radiogroup"] > label {
            background-color: #FFFFFF;
            border-radius: 10px;
            padding: 10px 14px;
            margin-bottom: 6px;
            border: 1px solid transparent;
            transition: all 0.2s ease-in-out;
            cursor: pointer;
        }
        [data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
            background-color: #EEF4FF !important;
            border-color: #BFDBFE !important;
        }
        [data-testid="stSidebar"] div[role="radiogroup"] > label[data-baseweb="radio"] div {
            color: #111827 !important;
            font-weight: 600 !important;
        }

        /* Headings */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Poppins', 'Inter', sans-serif !important;
            color: #111827 !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em;
        }

        /* High-Contrast Enterprise Card */
        .enterprise-card {
            background-color: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 14px;
            padding: 22px 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            position: relative;
            overflow: hidden;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            margin-bottom: 16px;
        }
        .enterprise-card::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #1E3A8A 0%, #2563EB 50%, #0EA5E9 100%);
        }
        .enterprise-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.04);
            border-color: #CBD5E1;
        }

        .card-label {
            font-size: 0.85rem;
            color: #4B5563 !important;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .card-value {
            font-size: 1.85rem;
            color: #111827 !important;
            font-weight: 800;
            margin-top: 4px;
            margin-bottom: 2px;
        }
        .card-subtext {
            font-size: 0.825rem;
            color: #16A34A !important;
            font-weight: 600;
        }

        /* Enterprise Header Banner */
        .enterprise-banner {
            background: linear-gradient(135deg, #1E3A8A 0%, #1E40AF 60%, #2563EB 100%);
            color: #FFFFFF !important;
            padding: 32px 36px;
            border-radius: 16px;
            margin-bottom: 28px;
            box-shadow: 0 10px 25px -5px rgba(30, 58, 138, 0.25);
        }
        .enterprise-banner h1 {
            color: #FFFFFF !important;
            margin-bottom: 8px;
            font-size: 2.1rem;
        }
        .enterprise-banner p {
            color: #E0F2FE !important;
            font-size: 1.05rem;
            margin: 0;
            font-weight: 400;
        }

        /* High-Contrast Status Badges */
        .badge-approved {
            background-color: #DCFCE7;
            color: #15803D !important;
            border: 1px solid #86EFAC;
            padding: 6px 16px;
            border-radius: 9999px;
            font-weight: 700;
            font-size: 0.875rem;
            display: inline-block;
        }
        .badge-rejected {
            background-color: #FEE2E2;
            color: #B91C1C !important;
            border: 1px solid #FCA5A5;
            padding: 6px 16px;
            border-radius: 9999px;
            font-weight: 700;
            font-size: 0.875rem;
            display: inline-block;
        }
        .badge-warning {
            background-color: #FEF3C7;
            color: #B45309 !important;
            border: 1px solid #FDE68A;
            padding: 6px 16px;
            border-radius: 9999px;
            font-weight: 700;
            font-size: 0.875rem;
            display: inline-block;
        }

        /* High-Contrast Buttons */
        .stButton>button {
            background-color: #1E3A8A !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            border-radius: 10px !important;
            padding: 10px 24px !important;
            border: 1px solid #1E3A8A !important;
            box-shadow: 0 4px 6px -1px rgba(30, 58, 138, 0.2);
            transition: all 0.2s ease-in-out !important;
        }
        .stButton>button:hover {
            background-color: #2563EB !important;
            border-color: #2563EB !important;
            transform: translateY(-1px);
            box-shadow: 0 6px 12px -2px rgba(37, 99, 235, 0.3);
        }

        /* Form Labels & Inputs */
        div[data-baseweb="input"] {
            border-radius: 10px !important;
            border: 1px solid #D1D5DB !important;
            background-color: #FFFFFF !important;
        }
        div[data-baseweb="input"] input {
            color: #111827 !important;
            font-weight: 500 !important;
        }
        div[data-baseweb="select"] {
            border-radius: 10px !important;
        }
        label {
            color: #111827 !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
        }

        /* High-Contrast Tables with Zebra Striping */
        .stDataFrame {
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            overflow: hidden;
        }
        div[data-testid="stTable"] table, div[data-testid="stDataFrame"] table {
            color: #111827 !important;
        }

        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True
    )
