def get_cibil_category(score: float):
    """
    Returns the classification label and HEX color code for a given CIBIL score.
    """
    if score >= 750:
        return "Excellent", "#22C55E"
    elif score >= 650:
        return "Good", "#38BDF8"
    elif score >= 550:
        return "Fair", "#F59E0B"
    else:
        return "Poor", "#EF4444"

def calculate_cibil_score(
    on_time_payment_pct: float = 100.0,
    credit_utilization_pct: float = 30.0,
    credit_history_years: float = 5.0,
    hard_inquiries_past_year: int = 1,
    total_active_accounts: int = 3,
    past_defaults_count: int = 0
) -> dict:
    """
    Calculates estimated CIBIL score (range 300 to 900) based on financial behaviors.
    """
    base_score = 300
    max_score = 900
    
    # 1. Payment History Weight (35%) - Max 210 points
    payment_points = (on_time_payment_pct / 100.0) * 210.0
    
    # 2. Credit Utilization Weight (30%) - Max 180 points
    if credit_utilization_pct <= 10:
        util_points = 180.0
    elif credit_utilization_pct <= 30:
        util_points = 160.0
    elif credit_utilization_pct <= 50:
        util_points = 110.0
    elif credit_utilization_pct <= 70:
        util_points = 70.0
    else:
        util_points = 30.0

    # 3. Credit History Length Weight (15%) - Max 90 points
    history_points = min(90.0, credit_history_years * 15.0)

    # 4. Credit Mix & Accounts Weight (10%) - Max 60 points
    mix_points = min(60.0, total_active_accounts * 15.0)

    # 5. Inquiries & Defaults Weight (10%) - Max 60 points
    inquiry_penalty = hard_inquiries_past_year * 10.0
    default_penalty = past_defaults_count * 75.0
    behavior_points = max(0.0, 60.0 - inquiry_penalty - default_penalty)

    calculated_score = base_score + payment_points + util_points + history_points + mix_points + behavior_points
    score = int(round(min(max_score, max(base_score, calculated_score))))

    category, color = get_cibil_category(score)

    return {
        "cibil_score": score,
        "category": category,
        "color": color,
        "breakdown": {
            "payment_history": round(payment_points, 1),
            "credit_utilization": round(util_points, 1),
            "history_length": round(history_points, 1),
            "credit_mix": round(mix_points, 1),
            "behavior": round(behavior_points, 1)
        }
    }
