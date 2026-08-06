import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def create_cibil_gauge(score: int):
    """
    Creates a gauge chart for CIBIL Score visualization with high contrast labels.
    """
    if score >= 750: color = "#16A34A"
    elif score >= 650: color = "#0EA5E9"
    elif score >= 550: color = "#F59E0B"
    else: color = "#DC2626"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "CIBIL Credit Score", 'font': {'size': 18, 'color': "#111827", 'family': "Inter, sans-serif"}},
        gauge={
            'axis': {'range': [300, 900], 'tickwidth': 1, 'tickcolor': "#4B5563"},
            'bar': {'color': color, 'thickness': 0.35},
            'bgcolor': "#FFFFFF",
            'borderwidth': 1,
            'bordercolor': "#E5E7EB",
            'steps': [
                {'range': [300, 550], 'color': '#FEE2E2'},
                {'range': [550, 650], 'color': '#FEF3C7'},
                {'range': [650, 750], 'color': '#E0F2FE'},
                {'range': [750, 900], 'color': '#DCFCE7'}
            ]
        }
    ))
    fig.update_layout(
        height=250,
        margin=dict(l=25, r=25, t=45, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#111827", family="Inter, sans-serif")
    )
    return fig

def create_approval_meter(probability: float):
    """
    Creates a probability meter gauge (0 to 100%).
    """
    color = "#16A34A" if probability >= 50 else "#DC2626"
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=probability,
        number={'suffix': "%", 'font': {'color': color, 'size': 36, 'family': "Inter, sans-serif"}},
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "AI Approval Probability", 'font': {'size': 18, 'color': "#111827"}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': "#4B5563"},
            'bar': {'color': color, 'thickness': 0.35},
            'bgcolor': "#FFFFFF",
            'borderwidth': 1,
            'bordercolor': "#E5E7EB",
            'steps': [
                {'range': [0, 50], 'color': '#FEE2E2'},
                {'range': [50, 100], 'color': '#DCFCE7'}
            ]
        }
    ))
    fig.update_layout(
        height=250,
        margin=dict(l=25, r=25, t=45, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#111827", family="Inter, sans-serif")
    )
    return fig

def create_income_vs_emi_chart(monthly_income: float, existing_emi: float, new_emi: float):
    """
    Creates cashflow bar chart with high contrast colors.
    """
    categories = ['Monthly Income', 'Existing EMI', 'New Loan EMI', 'Net Surplus']
    surplus = max(0, monthly_income - existing_emi - new_emi)
    values = [monthly_income, existing_emi, new_emi, surplus]
    colors = ['#1E3A8A', '#F59E0B', '#2563EB', '#16A34A']

    fig = go.Figure(data=[go.Bar(
        x=categories,
        y=values,
        marker_color=colors,
        text=[f"₹{v:,.0f}" for v in values],
        textposition='auto',
        textfont=dict(color='#FFFFFF', size=13, family="Inter, sans-serif")
    )])
    fig.update_layout(
        title="Monthly Cashflow Breakdown (₹)",
        title_font=dict(color="#111827", size=16),
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#111827", family="Inter, sans-serif"),
        yaxis=dict(gridcolor="#E5E7EB", tickfont=dict(color="#111827")),
        xaxis=dict(tickfont=dict(color="#111827", size=12))
    )
    return fig

def create_risk_distribution_pie(approved_count: int, rejected_count: int):
    """
    Creates risk breakdown donut chart.
    """
    labels = ['Approved Applications', 'Rejected Applications']
    values = [approved_count, rejected_count]
    colors = ['#16A34A', '#DC2626']

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.45,
        marker_colors=colors,
        textinfo='label+percent',
        textfont=dict(size=13, color='#FFFFFF', family="Inter, sans-serif")
    )])
    fig.update_layout(
        title="Loan Decision Distribution",
        title_font=dict(color="#111827", size=16),
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#111827", family="Inter, sans-serif"),
        legend=dict(font=dict(color="#111827", size=12))
    )
    return fig

def create_cibil_distribution_bar(predictions: list):
    """
    Creates bar chart distribution of applicant CIBIL score brackets.
    """
    brackets = {"Poor (<550)": 0, "Fair (550-649)": 0, "Good (650-749)": 0, "Excellent (750+)": 0}
    for p in predictions:
        score = p.get("result", {}).get("cibil_score") or p.get("inputData", {}).get("CIBILScore", 650)
        score = int(score)
        if score >= 750: brackets["Excellent (750+)"] += 1
        elif score >= 650: brackets["Good (650-749)"] += 1
        elif score >= 550: brackets["Fair (550-649)"] += 1
        else: brackets["Poor (<550)"] += 1

    fig = go.Figure(data=[go.Bar(
        x=list(brackets.keys()),
        y=list(brackets.values()),
        marker_color=['#DC2626', '#F59E0B', '#0EA5E9', '#16A34A'],
        text=list(brackets.values()),
        textposition='auto',
        textfont=dict(color='#FFFFFF', size=13)
    )])
    fig.update_layout(
        title="Applicant CIBIL Score Distribution",
        title_font=dict(color="#111827", size=16),
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#111827", family="Inter, sans-serif"),
        yaxis=dict(gridcolor="#E5E7EB", tickfont=dict(color="#111827")),
        xaxis=dict(tickfont=dict(color="#111827", size=12))
    )
    return fig
