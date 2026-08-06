from pydantic import BaseModel, Field, field_validator
from typing import Optional, Union

class LoanPredictionInputSchema(BaseModel):
    name: Optional[str] = "Applicant"
    age: int = Field(..., ge=18, description="Age must be 18 or older")
    gender: Optional[str] = "Male"
    occupation: Optional[str] = "Professional"
    employmentType: Optional[str] = Field("Salaried", alias="EmploymentType")
    monthlyIncome: float = Field(..., gt=0, description="Monthly income must be greater than 0")
    annualIncome: Optional[float] = None
    existingLoans: Optional[float] = Field(0.0, ge=0, alias="ExistingEMI")
    loanAmount: float = Field(..., gt=0, description="Loan amount must be greater than 0")
    loanTerm: int = Field(36, gt=0, alias="LoanTenure", description="Loan term in months")
    emi: Optional[float] = 0.0
    creditHistory: Optional[float] = Field(3.0, ge=0)
    cibilScore: int = Field(..., ge=300, le=900, description="CIBIL score must be between 300 and 900")
    dependents: Optional[int] = Field(0, ge=0, alias="Dependents")
    education: Optional[str] = Field("Graduate", alias="Education")
    propertyArea: Optional[str] = Field("Urban", alias="PropertyOwnership")
    bankBalance: Optional[float] = Field(50000.0, ge=0)
    previousLoanDefaults: Optional[int] = Field(0, ge=0)
    creditCardUsage: Optional[float] = Field(0.3, ge=0, le=1.0)

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "name": "Alex Johnson",
                "age": 32,
                "gender": "Male",
                "occupation": "Software Engineer",
                "employmentType": "Salaried",
                "monthlyIncome": 85000,
                "loanAmount": 500000,
                "loanTerm": 48,
                "cibilScore": 760,
                "existingLoans": 12000,
                "dependents": 1,
                "education": "Graduate",
                "propertyArea": "Urban"
            }
        }
    }

    @field_validator("monthlyIncome")
    def validate_income(cls, v):
        if v <= 0:
            raise ValueError("Monthly income must be strictly greater than 0")
        return v

    @field_validator("age")
    def validate_age(cls, v):
        if v < 18:
            raise ValueError("Applicant must be at least 18 years of age")
        return v

    @field_validator("loanAmount")
    def validate_loan_amount(cls, v):
        if v <= 0:
            raise ValueError("Loan amount must be strictly greater than 0")
        return v

    @field_validator("cibilScore")
    def validate_cibil(cls, v):
        if v < 300 or v > 900:
            raise ValueError("CIBIL score must be between 300 and 900")
        return v

class EmiCalculationInputSchema(BaseModel):
    loanAmount: float = Field(..., gt=0)
    interestRate: float = Field(..., gt=0)
    tenureMonths: int = Field(..., gt=0)
