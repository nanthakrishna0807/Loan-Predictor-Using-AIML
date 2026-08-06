def get_cibil_category(score: float) -> tuple[str, str]:
    """
    Returns (category_name, hex_color) based on CIBIL score.
    """
    if score >= 750:
        return "Excellent", "#22C55E"
    elif score >= 650:
        return "Good", "#38BDF8"
    elif score >= 550:
        return "Average", "#F59E0B"
    else:
        return "Poor", "#EF4444"

def calculate_estimated_cibil(
    monthly_income: float,
    existing_emi: float,
    credit_history_years: float,
    loan_amount: float,
    previous_defaults: int = 0,
    credit_card_utilization: float = 0.3
) -> dict:
    """
    Calculates estimated CIBIL financial score and breakdown based on financial metrics.
    """
    base_score = 650.0

    # 1. Income to Debt Ratio
    dti = existing_emi / max(monthly_income, 1.0)
    if dti <= 0.2:
        base_score += 60
    elif dti <= 0.4:
        base_score += 25
    elif dti > 0.6:
        base_score -= 80

    # 2. Credit History Length
    if credit_history_years >= 5:
        base_score += 50
    elif credit_history_years >= 2:
        base_score += 20
    else:
        base_score -= 20

    # 3. Payment Behaviour / Past Defaults
    if previous_defaults == 0:
        base_score += 40
    else:
        base_score -= (previous_defaults * 90)

    # 4. Credit Utilization
    if credit_card_utilization <= 0.3:
        base_score += 30
    elif credit_card_utilization > 0.7:
        base_score -= 50

    cibil_score = int(max(300, min(900, round(base_score))))
    category, color = get_cibil_category(cibil_score)

    return {
        "calculated_cibil_score": cibil_score,
        "category": category,
        "color": color,
        "dti_ratio": round(dti, 2)
    }
