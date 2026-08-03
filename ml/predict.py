import os
import joblib
import numpy as np
import pandas as pd

MODEL_PATH = "model.pkl"

class LoanPredictorEngine:
    def __init__(self, model_path=MODEL_PATH):
        self.model_path = model_path
        self.artifacts = None
        self.load_artifacts()

    def load_artifacts(self):
        if os.path.exists(self.model_path):
            try:
                self.artifacts = joblib.load(self.model_path)
                print(f"Loaded trained model: {self.artifacts.get('best_model_name')}")
            except Exception as e:
                print(f"Error loading model artifacts: {e}")
                self.artifacts = None
        else:
            print("Warning: model.pkl not found. Falling back to heuristic engine.")

    def get_cibil_category(self, score):
        if score >= 750:
            return "Excellent", "#22C55E"
        elif score >= 650:
            return "Good", "#38BDF8"
        elif score >= 550:
            return "Fair", "#F59E0B"
        else:
            return "Poor", "#EF4444"

    def calculate_emi(self, principal, rate_per_annum, tenure_months):
        if tenure_months <= 0:
            return 0.0
        r = (rate_per_annum / 100) / 12
        if r == 0:
            return round(principal / tenure_months, 2)
        emi = principal * r * ((1 + r) ** tenure_months) / (((1 + r) ** tenure_months) - 1)
        return round(float(emi), 2)

    def predict(self, input_data):
        cibil = float(input_data.get("CIBILScore", 650))
        annual_inc = float(input_data.get("AnnualIncome", 500000))
        monthly_inc = float(input_data.get("MonthlyIncome", annual_inc / 12))
        existing_emi = float(input_data.get("ExistingEMI", 0))
        loan_amt = float(input_data.get("LoanAmount", 200000))
        loan_tenure = int(input_data.get("LoanTenure", 36))
        bank_balance = float(input_data.get("BankBalance", 50000))
        prev_defaults = int(input_data.get("PreviousLoanDefaults", 0))
        credit_card_usage = float(input_data.get("CreditCardUsage", 0.3))
        
        # Calculate Debt to Income Ratio
        estimated_emi = self.calculate_emi(loan_amt, 10.5, loan_tenure)
        total_monthly_obligation = existing_emi + estimated_emi
        dti_ratio = round(total_monthly_obligation / max(monthly_inc, 1), 2)

        cibil_cat, cibil_color = self.get_cibil_category(cibil)

        # Base Probability using Machine Learning Model if available
        if self.artifacts and "model" in self.artifacts:
            try:
                feature_cols = self.artifacts["feature_cols"]
                scaler = self.artifacts["scaler"]
                encoders = self.artifacts["encoders"]
                model = self.artifacts["model"]

                row = {}
                for col in feature_cols:
                    val = input_data.get(col, 0)
                    if col in encoders:
                        # Map categorical string to encoded int
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
                
                # Model Prediction
                probs = model.predict_proba(X_scaled)[0]
                # Index 1 corresponds to Approval
                ml_prob = float(probs[1]) if len(probs) > 1 else float(probs[0])
            except Exception as ex:
                print(f"ML execution error: {ex}. Using heuristic.")
                ml_prob = 0.5
        else:
            ml_prob = 0.5

        # Refine prediction with configurable business rules & CIBIL threshold (650)
        prob = ml_prob

        # CIBIL Rule Adjustment
        if cibil < 550:
            prob *= 0.3
        elif cibil < 650:
            # Below 650: lean toward rejection unless strong savings/income
            if bank_balance > (loan_amt * 0.4) and dti_ratio < 0.4 and prev_defaults == 0:
                prob = max(prob, 0.55)
            else:
                prob = min(prob, 0.42)
        elif cibil >= 750:
            prob = max(prob, 0.82)

        # Defaults Adjustment
        if prev_defaults >= 1:
            prob *= 0.4

        # DTI Adjustment
        if dti_ratio > 0.6:
            prob *= 0.6

        # Cap bounds
        prob = round(float(np.clip(prob, 0.05, 0.98)), 4)
        approved = bool(prob >= 0.50)

        # Interest Rate Calculation
        base_rate = 8.5
        if cibil >= 780: rate_adj = 0.0
        elif cibil >= 720: rate_adj = 1.2
        elif cibil >= 650: rate_adj = 2.5
        elif cibil >= 580: rate_adj = 4.5
        else: rate_adj = 7.0

        if dti_ratio > 0.5: rate_adj += 1.5
        interest_rate = round(base_rate + rate_adj, 2)

        # Recalculate actual EMI at predicted interest rate
        final_emi = self.calculate_emi(loan_amt, interest_rate, loan_tenure)

        # Risk Level
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

        # Suggested Maximum Loan Amount
        max_allowable_emi = max(0, (monthly_inc * 0.5) - existing_emi)
        r = (interest_rate / 100) / 12
        if r > 0 and loan_tenure > 0:
            suggested_max_loan = max_allowable_emi * (((1 + r) ** loan_tenure) - 1) / (r * ((1 + r) ** loan_tenure))
            suggested_max_loan = round(max(0, min(suggested_max_loan, annual_inc * 5)), -3)
        else:
            suggested_max_loan = round(annual_inc * 2, -3)

        # Confidence Score
        confidence_score = round(abs(prob - 0.5) * 2 * 100, 1)

        # Loan Recommendation
        if approved:
            recommendation = (f"Application satisfies eligibility parameters with strong financial indicators. "
                              f"Recommended for approval up to {suggested_max_loan:,.0f} at an estimated {interest_rate}% APR.")
        else:
            recommendation = (f"High credit risk detected due to lower CIBIL score ({int(cibil)}) or high debt ratio ({int(dti_ratio*100)}%). "
                              f"We recommend reducing existing EMIs or applying for a lower loan amount (~{suggested_max_loan:,.0f}).")

        # Improvement Tips
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
        if len(tips) == 0:
            tips.append("Maintain your excellent financial track record and keep your debt utilization low.")

        return {
            "approved": approved,
            "loan_status": "Approved" if approved else "Rejected",
            "approval_probability": round(prob * 100, 2),
            "credit_risk_level": risk_level,
            "credit_risk_color": risk_color,
            "confidence_score": confidence_score,
            "cibil_category": cibil_cat,
            "cibil_color": cibil_color,
            "suggested_max_loan": suggested_max_loan,
            "emi_estimate": final_emi,
            "interest_rate_estimate": interest_rate,
            "debt_to_income_ratio": dti_ratio,
            "loan_recommendation": recommendation,
            "financial_improvement_tips": tips,
            "model_used": self.artifacts.get("best_model_name", "AI Ensemble Engine") if self.artifacts else "Rule-based AI Engine"
        }
