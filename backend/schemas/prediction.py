from typing import Optional, List
from pydantic import BaseModel, Field, field_validator

class LoanPredictionInputSchema(BaseModel):
    name: Optional[str] = Field("John Doe", alias="fullName")
    age: int = Field(30, alias="Age", ge=18, description="Age must be at least 18 years")
    gender: Optional[str] = Field("Male", alias="Gender")
    marital_status: Optional[str] = Field("Single", alias="MaritalStatus")
    occupation: Optional[str] = Field("Salaried", alias="Occupation")
    employment_type: Optional[str] = Field("Salaried", alias="EmploymentType")
    monthly_income: float = Field(50000.0, alias="MonthlyIncome", gt=0.0, description="Monthly income must be greater than 0")
    annual_income: Optional[float] = Field(600000.0, alias="AnnualIncome")
    existing_loans: Optional[int] = Field(0, alias="ExistingLoans")
    existing_emi: Optional[float] = Field(0.0, alias="ExistingEMI")
    loan_amount: float = Field(200000.0, alias="LoanAmount", gt=0.0, description="Loan amount must be greater than 0")
    loan_tenure: Optional[int] = Field(36, alias="LoanTenure")
    loan_term: Optional[int] = Field(36, alias="LoanTerm")
    cibil_score: int = Field(720, alias="CIBILScore", ge=300, le=900, description="CIBIL score must be between 300 and 900")
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
    loanAmount: float = Field(..., gt=0)
    interestRate: float = Field(..., ge=0)
    tenureMonths: int = Field(..., gt=0)
