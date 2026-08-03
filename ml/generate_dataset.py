import pandas as pd
import numpy as np
import random

def generate_loan_dataset(num_samples=1500, output_path="dataset.csv"):
    np.random.seed(42)
    random.seed(42)

    names = ["Aarav Sharma", "Priya Patel", "Rahul Verma", "Ananya Iyer", "Vikram Singh",
             "Neha Gupta", "Rohan Mehta", "Kavya Reddy", "Aditya Joshi", "Sneha Nair",
             "Amit Kumar", "Pooja Deshmukh", "Siddharth Rao", "Divya Agarwal", "Karan Malhotra",
             "Riya Sen", "Deepak Choudhury", "Meera Pillai", "Manish Tiwari", "Tanvi Bhatia"]
    
    genders = ["Male", "Female"]
    marital_statuses = ["Single", "Married", "Divorced"]
    educations = ["Graduate", "Post Graduate", "High School", "Doctorate"]
    employment_types = ["Salaried", "Self-Employed", "Business", "Freelancer"]
    loan_purposes = ["Home Loan", "Personal Loan", "Education Loan", "Car Loan", "Business Loan", "Medical Emergency"]
    property_ownerships = ["Owned", "Rented", "Mortgaged"]

    data = []

    for i in range(num_samples):
        name = random.choice(names)
        age = int(np.random.randint(21, 65))
        gender = random.choice(genders)
        marital_status = random.choice(marital_statuses)
        education = random.choice(educations)
        employment_type = random.choice(employment_types)
        self_employed = 1 if employment_type in ["Self-Employed", "Business", "Freelancer"] else 0
        
        # Financial metrics
        annual_income = round(float(np.random.lognormal(mean=13.0, sigma=0.6)), -3) # ~200k to 5M INR/USD
        annual_income = max(180000, min(10000000, annual_income))
        monthly_income = round(annual_income / 12, 2)
        
        existing_emi = round(random.uniform(0, 0.45) * monthly_income, 2)
        credit_card_usage = round(random.uniform(0.05, 0.95), 2)
        num_existing_loans = int(np.random.poisson(lam=1.2))
        
        # Loan Request details
        loan_amount = round(random.uniform(0.5, 6.0) * annual_income, -3)
        loan_purpose = random.choice(loan_purposes)
        loan_tenure = random.choice([12, 24, 36, 48, 60, 120, 180, 240, 360]) # months
        
        # CIBIL Score (300 to 900)
        cibil_score = int(np.random.normal(loc=680, scale=90))
        cibil_score = max(300, min(900, cibil_score))
        
        bank_balance = round(random.uniform(0.1, 2.5) * annual_income, 2)
        property_ownership = random.choice(property_ownerships)
        dependents = int(np.random.randint(0, 5))
        
        # Ratios
        estimated_new_emi = loan_amount / loan_tenure
        dti_ratio = round((existing_emi + estimated_new_emi) / monthly_income, 2)
        credit_utilization_ratio = credit_card_usage
        savings_amount = bank_balance
        
        # Defaults
        prev_defaults = 1 if cibil_score < 580 and random.random() > 0.3 else (1 if random.random() < 0.08 else 0)

        # Realistic Domain Logic for Approval Ground Truth
        # CIBIL < 600 or prev_defaults > 0 or DTI > 0.65 makes approval unlikely unless savings are huge
        score = 0
        if cibil_score >= 750: score += 40
        elif cibil_score >= 650: score += 25
        elif cibil_score >= 550: score += 10
        else: score -= 30

        if dti_ratio < 0.35: score += 25
        elif dti_ratio < 0.50: score += 10
        else: score -= 20

        if prev_defaults == 0: score += 15
        else: score -= 35

        if bank_balance > (loan_amount * 0.3): score += 15
        if annual_income > 600000: score += 10
        if property_ownership == "Owned": score += 10

        # Approval probability threshold
        approval_prob = 1 / (1 + np.exp(-(score - 30) / 12))
        loan_status = 1 if (approval_prob > 0.5 and cibil_score >= 550 and prev_defaults == 0) else 0
        if cibil_score >= 780 and dti_ratio <= 0.45:
            loan_status = 1
        if prev_defaults >= 1 and bank_balance < (loan_amount * 0.5):
            loan_status = 0

        data.append({
            "ApplicantName": name,
            "Age": age,
            "Gender": gender,
            "MaritalStatus": marital_status,
            "Education": education,
            "EmploymentType": employment_type,
            "SelfEmployed": self_employed,
            "AnnualIncome": annual_income,
            "MonthlyIncome": monthly_income,
            "ExistingEMI": existing_emi,
            "CreditCardUsage": credit_card_usage,
            "NumberExistingLoans": num_existing_loans,
            "LoanAmount": loan_amount,
            "LoanPurpose": loan_purpose,
            "LoanTenure": loan_tenure,
            "CIBILScore": cibil_score,
            "BankBalance": bank_balance,
            "PropertyOwnership": property_ownership,
            "Dependents": dependents,
            "DebtToIncomeRatio": dti_ratio,
            "CreditUtilizationRatio": credit_utilization_ratio,
            "SavingsAmount": savings_amount,
            "PreviousLoanDefaults": prev_defaults,
            "LoanStatus": loan_status
        })

    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    print(f"Generated {num_samples} records in {output_path}")
    return df

if __name__ == "__main__":
    generate_loan_dataset()
