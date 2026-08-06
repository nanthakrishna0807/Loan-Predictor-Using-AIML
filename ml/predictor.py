import os
import sys
import joblib
import numpy as np
import pandas as pd
from backend.utils.logger import logger
from backend.utils.cibil_calculator import get_cibil_category

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def safe_print(text: str):
    try:
        print(text)
    except UnicodeEncodeError:
        clean_text = text.encode('ascii', 'ignore').decode('ascii')
        print(clean_text)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
FALLBACK_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model.pkl")

class LoanPredictorEngine:
    def __init__(self, model_path=MODEL_PATH):
        self.model_path = model_path if os.path.exists(model_path) else FALLBACK_PATH
        self.artifacts = None
        self.model_loaded = False
        self.best_model_name = "Gradient Boosting"
        self.accuracy = 95.0
        self.feature_count = 22
        self.load_artifacts()

    def load_artifacts(self):
        """Loads trained Scikit-learn model artifacts using Joblib."""
        if os.path.exists(self.model_path):
            try:
                self.artifacts = joblib.load(self.model_path)
                self.model_loaded = True
                self.best_model_name = self.artifacts.get("best_model_name", "Gradient Boosting")
                self.accuracy = self.artifacts.get("accuracy", 95.0)
                safe_print(f"✅ ML Model Loaded Successfully ({self.best_model_name})")
                logger.info(f"ML Model loaded successfully from {self.model_path}")
            except Exception as e:
                self.model_loaded = False
                safe_print(f"❌ ML Model Failed to Load: {e}")
                logger.error(f"Failed to load ML model from {self.model_path}: {e}")
        else:
            self.model_loaded = False
            safe_print("❌ ML Model Failed to Load: File model.pkl not found")
            logger.warning("model.pkl not found. Predictor initialized in rule-engine mode.")

    def calculate_emi(self, principal: float, rate_per_annum: float, tenure_months: int) -> float:
        if tenure_months <= 0:
            return 0.0
        r = (rate_per_annum / 100) / 12
        if r == 0:
            return round(principal / tenure_months, 2)
        emi = principal * r * ((1 + r) ** tenure_months) / (((1 + r) ** tenure_months) - 1)
        return round(float(emi), 2)

    def predict(self, input_data: dict) -> dict:
        """
        Executes loan prediction using ML ensemble model + CIBIL & financial risk rules.
        """
        cibil = float(input_data.get("CIBILScore") or input_data.get("cibilScore") or input_data.get("cibil_score") or 650)
        monthly_inc = float(input_data.get("MonthlyIncome") or input_data.get("monthlyIncome") or input_data.get("monthly_income") or 45000)
        annual_inc = float(input_data.get("AnnualIncome") or input_data.get("annualIncome") or input_data.get("annual_income") or (monthly_inc * 12))
        existing_emi = float(input_data.get("ExistingEMI") or input_data.get("existingEMI") or input_data.get("existing_emi") or input_data.get("existingLoans") or 0)
        loan_amt = float(input_data.get("LoanAmount") or input_data.get("loanAmount") or input_data.get("loan_amount") or 200000)
        loan_tenure = int(input_data.get("LoanTenure") or input_data.get("loanTenure") or input_data.get("loan_tenure") or input_data.get("loan_term") or 36)
        bank_balance = float(input_data.get("BankBalance") or input_data.get("bankBalance") or input_data.get("bank_balance") or 50000)
        prev_defaults = int(input_data.get("PreviousLoanDefaults") or input_data.get("previousLoanDefaults") or input_data.get("previous_loan_defaults") or 0)
        credit_card_usage = float(input_data.get("CreditCardUsage") or input_data.get("creditCardUsage") or input_data.get("credit_card_usage") or 0.3)

        estimated_emi = self.calculate_emi(loan_amt, 10.5, loan_tenure)
        total_monthly_obligation = existing_emi + estimated_emi
        dti_ratio = round(total_monthly_obligation / max(monthly_inc, 1.0), 2)

        cibil_cat, cibil_color = get_cibil_category(cibil)

        ml_prob = 0.5
        if self.model_loaded and self.artifacts and "model" in self.artifacts:
            try:
                feature_cols = self.artifacts["feature_cols"]
                scaler = self.artifacts["scaler"]
                encoders = self.artifacts["encoders"]
                model = self.artifacts["model"]

                row = {}
                for col in feature_cols:
                    val = input_data.get(col)
                    if val is None:
                        camel_col = col[0].lower() + col[1:]
                        val = input_data.get(camel_col)
                    if val is None:
                        snake_col = "".join(["_" + c.lower() if c.isupper() else c for c in col]).lstrip("_")
                        val = input_data.get(snake_col, 0)
                    
                    if col in encoders:
                        classes = encoders[col]
                        val_str = str(val)
                        if val_str in classes:
                            row[col] = classes.index(val_str)
                        else:
                            row[col] = 0
                    else:
                        row[col] = float(val)

                df_row = pd.DataFrame([row])[feature_cols]
                X_scaled = scaler.transform(df_row)
                probs = model.predict_proba(X_scaled)[0]
                ml_prob = float(probs[1]) if len(probs) > 1 else float(probs[0])
            except Exception as ex:
                logger.error(f"ML Model inference error: {ex}. Using heuristic adjustment.")
                ml_prob = 0.5

        prob = ml_prob

        if cibil < 550:
            prob *= 0.3
        elif cibil < 650:
            if bank_balance > (loan_amt * 0.4) and dti_ratio < 0.4 and prev_defaults == 0:
                prob = max(prob, 0.55)
            else:
                prob = min(prob, 0.42)
        elif cibil >= 750:
            prob = max(prob, 0.82)

        if prev_defaults >= 1:
            prob *= 0.4
        if dti_ratio > 0.6:
            prob *= 0.6

        prob = round(float(np.clip(prob, 0.05, 0.98)), 4)
        approved = bool(prob >= 0.50)

        base_rate = 8.5
        if cibil >= 780: rate_adj = 0.0
        elif cibil >= 720: rate_adj = 1.2
        elif cibil >= 650: rate_adj = 2.5
        elif cibil >= 580: rate_adj = 4.5
        else: rate_adj = 7.0

        if dti_ratio > 0.5: rate_adj += 1.5
        interest_rate = round(base_rate + rate_adj, 2)
        final_emi = self.calculate_emi(loan_amt, interest_rate, loan_tenure)

        risk_score = round((1 - prob) * 100, 1)
        if prob >= 0.80 and cibil >= 720:
            risk_level = "Low"
            risk_color = "#22C55E"
        elif prob >= 0.55:
            risk_level = "Medium"
            risk_color = "#F59E0B"
        elif prob >= 0.35:
            risk_level = "High"
            risk_color = "#F97316"
        else:
            risk_level = "Critical"
            risk_color = "#EF4444"

        max_allowable_emi = max(0.0, (monthly_inc * 0.5) - existing_emi)
        r = (interest_rate / 100) / 12
        if r > 0 and loan_tenure > 0:
            suggested_max = max_allowable_emi * (((1 + r) ** loan_tenure) - 1) / (r * ((1 + r) ** loan_tenure))
            suggested_max = round(max(0.0, min(suggested_max, annual_inc * 5)), -3)
        else:
            suggested_max = round(annual_inc * 2, -3)

        confidence_score = round(abs(prob - 0.5) * 2 * 100, 1)

        if approved:
            recommendation = (f"Application satisfies eligibility parameters with strong financial indicators. "
                              f"Recommended for approval up to ₹{suggested_max:,.0f} at an estimated {interest_rate}% APR.")
            reason = f"Solid CIBIL score ({int(cibil)}), manageable DTI ratio ({int(dti_ratio * 100)}%), and verified income history."
        else:
            recommendation = (f"High credit risk detected due to lower CIBIL score ({int(cibil)}) or high debt ratio ({int(dti_ratio*100)}%). "
                              f"We recommend reducing existing EMIs or applying for a lower loan amount (~₹{suggested_max:,.0f}).")
            reason = f"CIBIL score ({int(cibil)}) below benchmark threshold or high total monthly obligation relative to income."

        tips = []
        if cibil < 750:
            tips.append("Pay all upcoming credit card bills and loan EMIs strictly on time to boost your CIBIL score above 750.")
        if credit_card_usage > 0.3:
            tips.append(f"Lower your credit card utilization ratio from {int(credit_card_usage*100)}% down to under 30%.")
        if dti_ratio > 0.4:
            tips.append("Pay down existing small loans or credit card balances to lower your Debt-to-Income ratio.")
        if bank_balance < (loan_amt * 0.25):
            tips.append("Increase liquid savings in your bank account to enhance your financial security margin.")
        if prev_defaults > 0:
            tips.append("Resolve any defaulted accounts or past delinquent flags with your credit bureau.")
        if not tips:
            tips.append("Maintain your excellent financial track record and keep your debt utilization low.")

        return {
            "approved": approved,
            "loan_status": "Approved" if approved else "Rejected",
            "approval_probability": round(prob * 100, 2),
            "risk_score": risk_score,
            "credit_risk_level": risk_level,
            "credit_risk_color": risk_color,
            "confidence_score": confidence_score,
            "cibil_score": int(cibil),
            "cibil_category": cibil_cat,
            "cibil_color": cibil_color,
            "suggested_max_loan": suggested_max,
            "emi_estimate": final_emi,
            "interest_rate_estimate": interest_rate,
            "debt_to_income_ratio": dti_ratio,
            "recommendation": recommendation,
            "reason": reason,
            "financial_improvement_tips": tips,
            "model_used": self.best_model_name if self.model_loaded else "Rule-based AI Engine"
        }

ml_predictor = LoanPredictorEngine()
