const axios = require('axios');

const ML_API_URL = process.env.ML_API_URL || 'http://localhost:5001';

const getMLPrediction = async (loanData) => {
  const flaskPayload = {
    cibil_score: Number(loanData.CIBILScore || loanData.cibilScore || 650),
    annual_income: Number(loanData.AnnualIncome || loanData.annualIncome || 500000),
    loan_amount: Number(loanData.LoanAmount || loanData.loanAmount || 200000),
    existing_loans: Number(loanData.NumberExistingLoans || loanData.existingLoans || 0),
    employment: loanData.EmploymentType || loanData.employmentType || 'Salaried',
    
    // Additional parameters for model feature alignment
    Age: Number(loanData.Age || loanData.age || 30),
    Gender: loanData.Gender || loanData.gender || 'Male',
    MaritalStatus: loanData.MaritalStatus || loanData.maritalStatus || 'Single',
    Education: loanData.Education || loanData.education || 'Graduate',
    EmploymentType: loanData.EmploymentType || loanData.employmentType || 'Salaried',
    SelfEmployed: Number(loanData.SelfEmployed || 0),
    AnnualIncome: Number(loanData.AnnualIncome || loanData.annualIncome || 500000),
    MonthlyIncome: Number(loanData.MonthlyIncome || loanData.monthlyIncome || 41666),
    ExistingEMI: Number(loanData.ExistingEMI || loanData.existingEMI || 0),
    CreditCardUsage: Number(loanData.CreditCardUsage || 0.25),
    NumberExistingLoans: Number(loanData.NumberExistingLoans || loanData.existingLoans || 0),
    LoanAmount: Number(loanData.LoanAmount || loanData.loanAmount || 200000),
    LoanPurpose: loanData.LoanPurpose || loanData.loanPurpose || 'Personal Loan',
    LoanTenure: Number(loanData.LoanTenure || loanData.tenure || 36),
    CIBILScore: Number(loanData.CIBILScore || loanData.cibilScore || 650),
    BankBalance: Number(loanData.BankBalance || loanData.bankBalance || 50000),
    PropertyOwnership: loanData.PropertyOwnership || 'Rented',
    Dependents: Number(loanData.Dependents || 0),
    DebtToIncomeRatio: Number(loanData.DebtToIncomeRatio || loanData.debtIncomeRatio || 0.2),
    PreviousLoanDefaults: Number(loanData.PreviousLoanDefaults || loanData.previousDefaults || 0),
    SavingsAmount: Number(loanData.SavingsAmount || loanData.savings || 50000)
  };

  try {
    const response = await axios.post(`${ML_API_URL}/predict`, flaskPayload, { timeout: 4000 });
    if (response.data && response.data.success) {
      const pred = response.data.prediction;
      return {
        loan_status: pred.loan_status || (pred.approved ? 'Approved' : 'Rejected'),
        probability: pred.approval_probability || pred.probability || 85.0,
        confidence: pred.confidence_score || pred.confidence || 90.0,
        risk: pred.credit_risk_level || pred.risk || 'Low',
        recommended_amount: pred.suggested_max_loan || pred.recommended_amount || (flaskPayload.annual_income * 3),
        interest_rate: pred.interest_rate_estimate || pred.interest_rate || 9.5,
        estimated_emi: pred.emi_estimate || 12500,
        recommendation: pred.loan_recommendation || 'Loan application meets standards.',
        tips: pred.financial_improvement_tips || ['Maintain CIBIL score above 750']
      };
    }
  } catch (error) {
    console.log(`ML Flask API connection notice (${error.message}). Running internal heuristic prediction engine.`);
  }

  // Pure JS Fallback Engine matching Python domain rules
  const cibil = flaskPayload.cibil_score;
  const annualInc = flaskPayload.annual_income;
  const monthlyInc = flaskPayload.MonthlyIncome;
  const loanAmt = flaskPayload.loan_amount;
  const tenure = flaskPayload.LoanTenure;
  const prevDefaults = flaskPayload.PreviousLoanDefaults;

  const dti = Number(((flaskPayload.ExistingEMI + (loanAmt / tenure)) / Math.max(monthlyInc, 1)).toFixed(2));

  let score = 0;
  if (cibil >= 750) score += 40;
  else if (cibil >= 650) score += 25;
  else if (cibil >= 550) score += 10;
  else score -= 30;

  if (dti < 0.35) score += 25;
  else if (dti < 0.50) score += 10;
  else score -= 20;

  if (prevDefaults === 0) score += 15;
  else score -= 35;

  let prob = 1 / (1 + Math.exp(-(score - 30) / 12));
  if (cibil < 650) prob = Math.min(prob, 0.45);
  if (prevDefaults >= 1) prob *= 0.4;

  prob = Math.max(0.08, Math.min(0.96, Number(prob.toFixed(4))));
  const approved = prob >= 0.50;

  const interestRate = cibil >= 750 ? 8.5 : (cibil >= 650 ? 11.2 : 14.5);
  const r = (interestRate / 100) / 12;
  const emi = Math.round(loanAmt * r * Math.pow(1 + r, tenure) / (Math.pow(1 + r, tenure) - 1));

  return {
    loan_status: approved ? 'Approved' : 'Rejected',
    probability: Number((prob * 100).toFixed(2)),
    confidence: Number((Math.abs(prob - 0.5) * 200).toFixed(1)),
    risk: approved ? (cibil >= 750 ? 'Low' : 'Medium') : 'High',
    recommended_amount: Math.round(annualInc * 3),
    interest_rate: interestRate,
    estimated_emi: emi,
    recommendation: approved
      ? `Eligible for instant approval up to ₹${(annualInc * 3).toLocaleString()} at ${interestRate}% APR.`
      : `High credit risk detected due to lower CIBIL score (${cibil}). Reduce debt utilization before re-applying.`,
    tips: [
      'Maintain CIBIL score strictly above 750 by making timely EMI payments.',
      'Keep credit card utilization ratio below 30%.',
      'Pay off existing small loan balances to lower DTI ratio.'
    ]
  };
};

module.exports = { getMLPrediction };
