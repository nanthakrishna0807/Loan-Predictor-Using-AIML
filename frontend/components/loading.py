import streamlit as st
import time

def render_loading_screen(title: str = "AI Loan Predictor", subtitle: str = "Initializing Platform & AI Engine..."):
    """
    Renders the professional JIT QR Asset Management-style startup loading animation.
    """
    loading_box = st.empty()
    with loading_box.container():
        is_dark = st.session_state.get("theme", "light") == "dark"
        box_bg = "#1E293B" if is_dark else "#FFFFFF"
        box_border = "#3B82F6" if is_dark else "#1E3A8A"
        title_color = "#60A5FA" if is_dark else "#1E3A8A"
        sub_color = "#FFFFFF" if is_dark else "#0F172A"

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style="background-color: {box_bg}; border: 3px solid {box_border}; border-radius: 20px; padding: 40px 32px; max-width: 620px; margin: 0 auto; box-shadow: 0 16px 36px -6px rgba(0,0,0,0.2); text-align: center;">
                <div style="font-size: 3.5rem; margin-bottom: 10px;">🏦</div>
                <h2 style="color: {title_color} !important; margin: 0; font-size: 2rem; font-weight: 800;">{title}</h2>
                <p style="font-size: 1.1rem; color: {sub_color} !important; margin-top: 8px; font-weight: 700;">{subtitle}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns([1, 2.5, 1])
        with c2:
            prog_bar = st.progress(0)
            status_text = st.empty()

            loading_items = [
                ("Loading AI Gradient Boosting Model...", 35),
                ("Connecting MongoDB Atlas Database...", 70),
                ("Preparing Financial Diagnostics...", 100)
            ]

            for msg, pct in loading_items:
                status_text.markdown(f"<p style='color: {title_color} !important; font-weight: 800; text-align: center; font-size: 1.05rem;'>⚡ {msg}</p>", unsafe_allow_html=True)
                prog_bar.progress(pct)
                time.sleep(0.15)

    loading_box.empty()
    st.session_state["startup_done"] = True
