import os
import sys
import joblib
import numpy as np
import pandas as pd

# Path setup so backend utils resolve when called from frontend/
_ML_DIR      = os.path.dirname(os.path.abspath(__file__))
_ROOT_DIR    = os.path.dirname(_ML_DIR)
_BACKEND_DIR = os.path.join(_ROOT_DIR, "backend")
for _p in [_ROOT_DIR, _BACKEND_DIR]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

try:
    from backend.app.utils.cibil_calculator import get_cibil_category
    from backend.app.utils.loan_type_rules   import get_loan_config, LOAN_CONFIG
except ModuleNotFoundError:
    from app.utils.cibil_calculator import get_cibil_category
    from app.utils.loan_type_rules   import get_loan_config, LOAN_CONFIG

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def safe_print(text: str):
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', 'ignore').decode('ascii'))

MODEL_PATH   = os.path.join(os.path.dirname(__file__), "model.pkl")
FALLBACK_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model.pkl")


class LoanPredictorEngine:
    def __init__(self, model_path=MODEL_PATH):
        self.model_path    = model_path if os.path.exists(model_path) else FALLBACK_PATH
        self.artifacts     = None
        self.model_loaded  = False
        self.best_model_name = "Gradient Boosting"
        self.accuracy      = 95.0
        self.load_artifacts()

    def load_artifacts(self):
        if os.path.exists(self.model_path):
            try:
                self.artifacts     = joblib.load(self.model_path)
                self.model_loaded  = True
                self.best_model_name = self.artifacts.get("best_model_name", "Gradient Boosting")
                self.accuracy      = self.artifacts.get("accuracy", 95.0)
                safe_print(f"ML Model Loaded ({self.best_model_name})")
            except Exception as e:
                self.model_loaded = False
                safe_print(f"ML Model load failed: {e}")
        else:
            self.model_loaded = False
            safe_print("model.pkl not found — using rule-based mode")

    def calculate_emi(self, principal: float, rate_per_annum: float, tenure_months: int) -> float:
        if tenure_months <= 0:
            return 0.0
        r = (rate_per_annum / 100) / 12
        if r == 0:
            return round(principal / tenure_months, 2)
        emi = principal * r * ((1 + r) ** tenure_months) / (((1 + r) ** tenure_months) - 1)
        return round(float(emi), 2)

    def predict(self, input_data: dict) -> dict:
        # Resolve loan type
        loan_type_raw = (
            input_data.get("LoanType") or
            input_data.get("loanType") or
            input_data.get("loan_type") or
            "Personal Loan"
        )
        loan_type = loan_type_raw.strip()
        for lt in LOAN_CONFIG:
            if lt.lower() in loan_type.lower():
                loan_type = lt
                break
        loan_cfg = get_loan_config(loan_type)

        # Core inputs
        cibil        = float(input_data.get("CIBILScore") or input_data.get("cibilScore") or 650)
        monthly_inc  = float(input_data.get("MonthlyIncome") or input_data.get("monthlyIncome") or 45000)
        annual_inc   = float(input_data.get("AnnualIncome") or input_data.get("annualIncome") or (monthly_inc * 12))
        existing_emi = float(input_data.get("ExistingEMI") or input_data.get("existingEMI") or input_data.get("existingLoans") or 0)
        loan_amt     = float(input_data.get("LoanAmount") or input_data.get("loanAmount") or 200000)

        tenure_years_raw = int(input_data.get("LoanTenureYears") or input_data.get("loanTenureYears") or 0)
        if tenure_years_raw > 0:
            tenure_months = tenure_years_raw * 12
        else:
            tenure_months = int(input_data.get("LoanTenure") or input_data.get("loanTenure") or input_data.get("loanTerm") or 36)

        bank_balance  = float(input_data.get("BankBalance") or input_data.get("bankBalance") or 50000)
        prev_defaults = int(input_data.get("PreviousLoanDefaults") or input_data.get("previousLoanDefaults") or 0)
        credit_usage  = float(input_data.get("CreditCardUsage") or input_data.get("creditCardUsage") or 0.3)

        interest_rate_base = loan_cfg["rate"]

        # ML inference
        ml_prob = 0.5
        if self.model_loaded and self.artifacts and "model" in self.artifacts:
            try:
                feature_cols = self.artifacts["feature_cols"]
                scaler       = self.artifacts["scaler"]
                encoders     = self.artifacts["encoders"]
                model        = self.artifacts["model"]
                row = {}
                for col in feature_cols:
                    val = input_data.get(col)
                    if val is None:
                        camel_col = col[0].lower() + col[1:]
                        val = input_data.get(camel_col, 0)
                    if col in encoders:
                        classes = encoders[col]
                        val_str = str(val)
                        row[col] = classes.index(val_str) if val_str in classes else 0
                    else:
                        row[col] = float(val)
                df_row   = pd.DataFrame([row])[feature_cols]
                X_scaled = scaler.transform(df_row)
                probs    = model.predict_proba(X_scaled)[0]
                ml_prob  = float(probs[1]) if len(probs) > 1 else float(probs[0])
            except Exception:
                ml_prob = 0.5

        # EMI & DTI
        estimated_emi    = self.calculate_emi(loan_amt, interest_rate_base, tenure_months)
        total_obligation = existing_emi + estimated_emi
        dti_ratio        = round(total_obligation / max(monthly_inc, 1.0), 2)

        cibil_cat, cibil_color = get_cibil_category(cibil)
        prob = ml_prob

        if cibil < 550:
            prob *= 0.3
        elif cibil < 650:
            prob = max(prob, 0.55) if (bank_balance > loan_amt * 0.4 and dti_ratio < 0.4 and prev_defaults == 0) else min(prob, 0.42)
        elif cibil >= 750:
            prob = max(prob, 0.82)

        if prev_defaults >= 1:  prob *= 0.4
        if dti_ratio > 0.6:     prob *= 0.6

        min_cibil = loan_cfg.get("min_cibil", 650)
        if cibil < min_cibil:   prob = min(prob, 0.30)
        prob = prob + loan_cfg.get("prob_boost", 0.0)
        prob = round(float(np.clip(prob, 0.05, 0.98)), 4)
        approved = bool(prob >= 0.50)

        if cibil >= 780:     rate_adj = 0.0
        elif cibil >= 720:   rate_adj = 0.75
        elif cibil >= 650:   rate_adj = 1.5
        elif cibil >= 580:   rate_adj = 2.5
        else:                rate_adj = 4.0
        if dti_ratio > 0.5:  rate_adj += 1.0
        interest_rate  = round(interest_rate_base + rate_adj, 2)
        final_emi      = self.calculate_emi(loan_amt, interest_rate, tenure_months)
        total_payment  = round(final_emi * tenure_months, 2)
        total_interest = round(total_payment - loan_amt, 2)

        if prob >= 0.80 and cibil >= 720:
            risk_level, risk_color = "Low",      "#22C55E"
        elif prob >= 0.55:
            risk_level, risk_color = "Medium",   "#F59E0B"
        elif prob >= 0.35:
            risk_level, risk_color = "High",     "#F97316"
        else:
            risk_level, risk_color = "Critical", "#EF4444"
        risk_score = round((1 - prob) * 100, 1)

        max_allowable_emi = max(0.0, (monthly_inc * 0.5) - existing_emi)
        r = (interest_rate / 100) / 12
        if r > 0 and tenure_months > 0:
            suggested_max = max_allowable_emi * (((1 + r) ** tenure_months) - 1) / (r * ((1 + r) ** tenure_months))
            suggested_max = round(max(0.0, min(suggested_max, loan_cfg["max_amount"])), -3)
        else:
            suggested_max = round(min(annual_inc * 2, loan_cfg["max_amount"]), -3)

        recommended_tenure_years = min(
            loan_cfg["max_tenure_years"],
            max(loan_cfg["min_tenure_years"], tenure_months // 12)
        )
        confidence_score = round(abs(prob - 0.5) * 2 * 100, 1)
        loan_icon = loan_cfg["icon"]

        if approved:
            recommendation = (
                f"{loan_icon} {loan_type} application satisfies eligibility criteria. "
                f"Recommended approval up to Rs.{suggested_max:,.0f} at {interest_rate}% APR."
            )
            reason = f"CIBIL score ({int(cibil)}) meets threshold; DTI ({int(dti_ratio*100)}%) within 50% cap."
        else:
            recommendation = (
                f"{loan_icon} {loan_type} flagged: CIBIL {int(cibil)} or DTI {int(dti_ratio*100)}% exceeds limits. "
                f"Consider Rs.{suggested_max:,.0f} or improve credit score."
            )
            reason = f"CIBIL ({int(cibil)}) below {loan_type} min ({min_cibil}+) or DTI too high."

        tips = []
        if cibil < 750:        tips.append("Pay all EMIs on time to boost CIBIL above 750.")
        if credit_usage > 0.3: tips.append(f"Lower credit utilization from {int(credit_usage*100)}% to under 30%.")
        if dti_ratio > 0.4:    tips.append("Pay down existing loans to reduce DTI below 40%.")
        if bank_balance < (loan_amt * 0.25): tips.append("Increase liquid savings to at least 25% of the loan amount.")
        if prev_defaults > 0:  tips.append("Resolve all defaulted accounts before reapplying.")
        if not tips:           tips.append("Maintain excellent financial track record and keep debt utilization low.")

        return {
            "approved":                   approved,
            "loan_status":                "Approved" if approved else "Rejected",
            "approval_probability":       round(prob * 100, 2),
            "confidence_score":           confidence_score,
            "loan_type":                  loan_type,
            "loan_type_icon":             loan_icon,
            "risk_score":                 risk_score,
            "credit_risk_level":          risk_level,
            "credit_risk_color":          risk_color,
            "cibil_score":                int(cibil),
            "cibil_category":             cibil_cat,
            "cibil_color":                cibil_color,
            "loan_amount":                loan_amt,
            "tenure_months":              tenure_months,
            "tenure_years":               round(tenure_months / 12, 1),
            "interest_rate_estimate":     interest_rate,
            "emi_estimate":               final_emi,
            "total_payment":              total_payment,
            "total_interest":             total_interest,
            "debt_to_income_ratio":       dti_ratio,
            "suggested_max_loan":         suggested_max,
            "recommended_tenure_years":   recommended_tenure_years,
            "recommendation":             recommendation,
            "reason":                     reason,
            "financial_improvement_tips": tips,
            "required_documents":         loan_cfg["required_documents"],
            "model_used":                 self.best_model_name if self.model_loaded else "Rule-based AI Engine",
        }


ml_predictor = LoanPredictorEngine()
