import pandas as pd
import numpy as np

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes financial ratios (DTI, Credit Utilization Ratio, Savings Amount, Loan-to-Income ratio).
    """
    df = df.copy()

    # Ensure required base columns
    monthly_inc = df.get("MonthlyIncome", df.get("AnnualIncome", 500000) / 12)
    df["MonthlyIncome"] = monthly_inc
    df["AnnualIncome"] = df.get("AnnualIncome", df["MonthlyIncome"] * 12)
    df["ExistingEMI"] = df.get("ExistingEMI", 0.0)
    df["LoanAmount"] = df.get("LoanAmount", 200000.0)
    df["LoanTenure"] = df.get("LoanTenure", 36)
    
    # Calculate estimated EMI if missing
    r = (10.5 / 100) / 12
    n = df["LoanTenure"]
    p = df["LoanAmount"]
    estimated_emi = p * r * ((1 + r) ** n) / (((1 + r) ** n) - 1)
    
    # Debt-to-Income Ratio
    if "DebtToIncomeRatio" not in df.columns:
        total_monthly_debt = df["ExistingEMI"] + estimated_emi
        df["DebtToIncomeRatio"] = np.round(total_monthly_debt / np.maximum(df["MonthlyIncome"], 1.0), 2)

    # Credit Utilization Ratio
    if "CreditUtilizationRatio" not in df.columns:
        df["CreditUtilizationRatio"] = df.get("CreditCardUsage", 0.3)

    # Savings Amount
    if "SavingsAmount" not in df.columns:
        df["SavingsAmount"] = df.get("BankBalance", df["MonthlyIncome"] * 2)

    # Self Employed flag
    if "SelfEmployed" not in df.columns:
        emp = df.get("EmploymentType", "Salaried")
        df["SelfEmployed"] = emp.astype(str).map(lambda x: "Yes" if "self" in x.lower() else "No")

    return df
