"""
Loan Type Rules Configuration
Central config for all loan types: interest rates, tenure limits, max amounts,
required documents, and eligibility adjustments.
"""

# ── Core loan-type configuration ─────────────────────────────────────
LOAN_CONFIG = {
    "Home Loan": {
        "icon": "🏠",
        "rate": 8.5,
        "min_tenure_years": 5,
        "max_tenure_years": 30,
        "default_tenure_years": 20,
        "max_amount": 50_000_000,       # ₹5 Crore
        "min_amount": 200_000,           # ₹2 Lakh
        "min_cibil": 650,
        "prob_boost": 0.05,             # slight boost for secured loan
        "required_documents": [
            "KYC Documents (Aadhaar / PAN)",
            "6 Months Bank Statements",
            "3 Months Salary Slips",
            "Property Documents / Title Deed",
            "Property Valuation Report",
            "NOC from Builder / Society",
            "IT Returns (2 Years)",
        ],
    },
    "Personal Loan": {
        "icon": "👤",
        "rate": 12.5,
        "min_tenure_years": 1,
        "max_tenure_years": 7,
        "default_tenure_years": 3,
        "max_amount": 4_000_000,        # ₹40 Lakh
        "min_amount": 50_000,            # ₹50k
        "min_cibil": 700,
        "prob_boost": -0.05,            # unsecured — slight penalty
        "required_documents": [
            "KYC Documents (Aadhaar / PAN)",
            "3 Months Salary Slips",
            "6 Months Bank Statements",
            "Employment Letter / Appointment Letter",
            "IT Returns (Last Year)",
        ],
    },
    "Business Loan": {
        "icon": "🏢",
        "rate": 11.0,
        "min_tenure_years": 1,
        "max_tenure_years": 15,
        "default_tenure_years": 5,
        "max_amount": 100_000_000,      # ₹10 Crore
        "min_amount": 500_000,           # ₹5 Lakh
        "min_cibil": 650,
        "prob_boost": 0.0,
        "required_documents": [
            "KYC Documents (Aadhaar / PAN)",
            "Business Registration Certificate",
            "GST Registration & Returns (2 Years)",
            "Audited Financial Statements (2 Years)",
            "ITR with Balance Sheet (2 Years)",
            "Bank Statements (12 Months)",
            "Business Continuity Proof (3+ Years)",
        ],
    },
    "Education Loan": {
        "icon": "🎓",
        "rate": 9.0,
        "min_tenure_years": 5,
        "max_tenure_years": 15,
        "default_tenure_years": 8,
        "max_amount": 20_000_000,       # ₹2 Crore
        "min_amount": 50_000,            # ₹50k
        "min_cibil": 600,
        "prob_boost": 0.08,             # government push — high boost
        "required_documents": [
            "KYC Documents of Student + Co-applicant",
            "Admission Letter from Institution",
            "Fee Structure / Cost Estimate",
            "Academic Mark Sheets (10th, 12th, UG)",
            "Co-applicant Income Proof",
            "Co-applicant Bank Statements (6 Months)",
        ],
    },
    "Vehicle Loan": {
        "icon": "🚗",
        "rate": 9.5,
        "min_tenure_years": 1,
        "max_tenure_years": 7,
        "default_tenure_years": 5,
        "max_amount": 10_000_000,       # ₹1 Crore
        "min_amount": 50_000,            # ₹50k
        "min_cibil": 650,
        "prob_boost": 0.03,             # asset-backed
        "required_documents": [
            "KYC Documents (Aadhaar / PAN)",
            "Driving License",
            "3 Months Salary Slips / ITR",
            "6 Months Bank Statements",
            "Vehicle Quotation / Invoice (from dealer)",
            "Insurance Document (after purchase)",
        ],
    },
}

# ── Convenience helpers ───────────────────────────────────────────────

LOAN_TYPES = list(LOAN_CONFIG.keys())

INTEREST_RATE = {k: v["rate"] for k, v in LOAN_CONFIG.items()}

MAX_TENURE = {k: v["max_tenure_years"] for k, v in LOAN_CONFIG.items()}

MIN_TENURE = {k: v["min_tenure_years"] for k, v in LOAN_CONFIG.items()}

MAX_AMOUNT = {k: v["max_amount"] for k, v in LOAN_CONFIG.items()}


def get_loan_config(loan_type: str) -> dict:
    """Return config dict for a loan type. Falls back to Personal Loan if unknown."""
    return LOAN_CONFIG.get(loan_type, LOAN_CONFIG["Personal Loan"])


def get_required_documents(loan_type: str) -> list:
    return get_loan_config(loan_type).get("required_documents", [])


def get_interest_rate(loan_type: str) -> float:
    return get_loan_config(loan_type)["rate"]


def get_max_tenure(loan_type: str) -> int:
    return get_loan_config(loan_type)["max_tenure_years"]
