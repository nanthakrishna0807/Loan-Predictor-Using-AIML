from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

class LoanPredictionInputSchema(BaseModel):
    name: Optional[str] = Field("John Doe", alias="fullName")
    age: Optional[int] = Field(32, alias="Age")
    gender: Optional[str] = Field("Male", alias="Gender")
    occupation: Optional[str] = Field("Salaried", alias="Occupation")
    employment_type: Optional[str] = Field("Salaried", alias="EmploymentType")
    monthly_income: Optional[float] = Field(50000.0, alias="MonthlyIncome")
    annual_income: Optional[float] = Field(600000.0, alias="AnnualIncome")
    existing_loans: Optional[int] = Field(0, alias="ExistingLoans")
    existing_emi: Optional[float] = Field(0.0, alias="ExistingEMI")
    loan_amount: Optional[float] = Field(200000.0, alias="LoanAmount")
    loan_tenure: Optional[int] = Field(36, alias="LoanTenure")
    loan_term: Optional[int] = Field(36, alias="LoanTerm")
    cibil_score: Optional[int] = Field(720, alias="CIBILScore")
    dependents: Optional[int] = Field(1, alias="Dependents")
    education: Optional[str] = Field("Graduate", alias="Education")
    property_area: Optional[str] = Field("Urban", alias="PropertyArea")
    property_ownership: Optional[str] = Field("Owned", alias="PropertyOwnership")
    credit_card_usage: Optional[float] = Field(0.25, alias="CreditCardUsage")
    bank_balance: Optional[float] = Field(75000.0, alias="BankBalance")
    previous_loan_defaults: Optional[int] = Field(0, alias="PreviousLoanDefaults")

    class Config:
        populate_by_name = True
        extra = "allow"

class EmiCalculationInputSchema(BaseModel):
    loanAmount: float
    interestRate: float
    tenureMonths: int

class PredictionResponseSchema(BaseModel):
    approved: bool
    loan_status: str
    approval_probability: float
    risk_score: float
    credit_risk_level: str
    credit_risk_color: str
    confidence_score: float
    cibil_score: int
    cibil_category: str
    cibil_color: str
    suggested_max_loan: float
    emi_estimate: float
    interest_rate_estimate: float
    debt_to_income_ratio: float
    recommendation: str
    financial_improvement_tips: List[str]
    model_used: str
