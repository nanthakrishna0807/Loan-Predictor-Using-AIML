import React, { useState } from 'react';
import { Calculator, DollarSign, Calendar, Percent, ShieldCheck, Activity } from 'lucide-react';
import DynamicCibilMeter from '../components/DynamicCibilMeter';

const LoanCalculator = () => {
  // EMI Calculator State
  const [loanAmt, setLoanAmt] = useState(500000);
  const [interestRate, setInterestRate] = useState(10.5);
  const [tenureMonths, setTenureMonths] = useState(36);

  // Eligibility Calculator State
  const [monthlyIncome, setMonthlyIncome] = useState(75000);
  const [existingEMI, setExistingEMI] = useState(12000);
  const [userCibil, setUserCibil] = useState(720);

  // EMI Math Calculation
  const r = (interestRate / 100) / 12;
  const emi = r > 0 && tenureMonths > 0
    ? Math.round(loanAmt * r * Math.pow(1 + r, tenureMonths) / (Math.pow(1 + r, tenureMonths) - 1))
    : Math.round(loanAmt / tenureMonths);

  const totalPayment = emi * tenureMonths;
  const totalInterest = Math.max(0, totalPayment - loanAmt);

  // Eligibility Math
  const maxAllowableEMI = Math.max(0, (monthlyIncome * 0.5) - existingEMI);
  const eligibleLoanAmt = Math.round(maxAllowableEMI * Math.pow(1 + r, tenureMonths) / (r * Math.pow(1 + r, tenureMonths) || 1));

  // Financial Health Score (out of 100)
  const dti = ((existingEMI + emi) / (monthlyIncome || 1));
  let healthScore = 70;
  if (userCibil >= 750) healthScore += 15;
  else if (userCibil < 650) healthScore -= 20;

  if (dti < 0.3) healthScore += 15;
  else if (dti > 0.5) healthScore -= 20;

  healthScore = Math.max(10, Math.min(100, Math.round(healthScore)));

  return (
    <div className="py-5">
      <div className="container">
        <div className="text-center max-w-2xl mx-auto mb-5">
          <span className="badge bg-blue-900/60 text-cyan-400 border border-cyan-500/30 px-3 py-1.5 rounded-pill text-xs fw-semibold mb-3">
            FINANCIAL SUITE
          </span>
          <h1 className="display-5 fw-bold text-white mb-3">Loan & Financial Calculator</h1>
          <p className="lead text-slate-300">Compute monthly EMIs, maximum loan eligibility limits, and your overall Financial Health Score.</p>
        </div>

        <div className="row g-4">
          {/* EMI Calculator */}
          <div className="col-lg-6">
            <div className="glass-card p-4 h-100">
              <h4 className="fw-bold text-white mb-4 d-flex align-items-center gap-2">
                <Calculator className="text-cyan-400" /> EMI Calculator
              </h4>

              <div className="mb-4">
                <div className="d-flex justify-content-between text-sm text-slate-300 mb-2">
                  <span>Loan Amount</span>
                  <span className="fw-bold text-cyan-400">₹{loanAmt.toLocaleString()}</span>
                </div>
                <input
                  type="range"
                  className="form-range"
                  min="50000"
                  max="5000000"
                  step="25000"
                  value={loanAmt}
                  onChange={(e) => setLoanAmt(Number(e.target.value))}
                />
              </div>

              <div className="mb-4">
                <div className="d-flex justify-content-between text-sm text-slate-300 mb-2">
                  <span>Interest Rate (p.a)</span>
                  <span className="fw-bold text-cyan-400">{interestRate}%</span>
                </div>
                <input
                  type="range"
                  className="form-range"
                  min="6"
                  max="24"
                  step="0.25"
                  value={interestRate}
                  onChange={(e) => setInterestRate(Number(e.target.value))}
                />
              </div>

              <div className="mb-4">
                <div className="d-flex justify-content-between text-sm text-slate-300 mb-2">
                  <span>Loan Tenure</span>
                  <span className="fw-bold text-cyan-400">{tenureMonths} Months ({Math.round(tenureMonths/12 * 10)/10} Yrs)</span>
                </div>
                <input
                  type="range"
                  className="form-range"
                  min="6"
                  max="360"
                  step="6"
                  value={tenureMonths}
                  onChange={(e) => setTenureMonths(Number(e.target.value))}
                />
              </div>

              <div className="p-4 rounded-3 bg-slate-900/80 border border-slate-800 text-white">
                <div className="row text-center g-3">
                  <div className="col-4 border-end border-slate-800">
                    <span className="text-2xs text-slate-400 d-block">Monthly EMI</span>
                    <span className="h4 fw-bold text-emerald-400 mb-0">₹{emi.toLocaleString()}</span>
                  </div>
                  <div className="col-4 border-end border-slate-800">
                    <span className="text-2xs text-slate-400 d-block">Total Interest</span>
                    <span className="h5 fw-semibold text-amber-400 mb-0">₹{totalInterest.toLocaleString()}</span>
                  </div>
                  <div className="col-4">
                    <span className="text-2xs text-slate-400 d-block">Total Payable</span>
                    <span className="h5 fw-semibold text-sky-400 mb-0">₹{totalPayment.toLocaleString()}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Eligibility & Health Score */}
          <div className="col-lg-6">
            <div className="glass-card p-4 h-100 d-flex flex-column justify-content-between">
              <div>
                <h4 className="fw-bold text-white mb-4 d-flex align-items-center gap-2">
                  <Activity className="text-emerald-400" /> Loan Eligibility & Health Score
                </h4>

                <div className="mb-3">
                  <label className="text-xs text-slate-300 mb-1 d-block">Monthly Gross Income (₹)</label>
                  <input
                    type="number"
                    className="fintech-input"
                    value={monthlyIncome}
                    onChange={(e) => setMonthlyIncome(Number(e.target.value))}
                  />
                </div>

                <div className="mb-3">
                  <label className="text-xs text-slate-300 mb-1 d-block">Existing Monthly EMIs (₹)</label>
                  <input
                    type="number"
                    className="fintech-input"
                    value={existingEMI}
                    onChange={(e) => setExistingEMI(Number(e.target.value))}
                  />
                </div>

                <div className="mb-4">
                  <label className="text-xs text-slate-300 mb-1 d-block">Estimated CIBIL Score</label>
                  <input
                    type="number"
                    className="fintech-input"
                    min="300"
                    max="900"
                    value={userCibil}
                    onChange={(e) => setUserCibil(Number(e.target.value))}
                  />
                </div>
              </div>

              <div className="row g-3">
                <div className="col-md-6">
                  <div className="p-3 rounded-3 bg-blue-950/40 border border-blue-500/30 text-white">
                    <span className="text-2xs text-slate-400 d-block">Max Loan Eligibility</span>
                    <span className="h4 fw-bold text-cyan-400">₹{eligibleLoanAmt.toLocaleString()}</span>
                    <span className="text-2xs text-slate-400 d-block">Based on 50% max DTI</span>
                  </div>
                </div>

                <div className="col-md-6">
                  <div className="p-3 rounded-3 bg-emerald-950/40 border border-emerald-500/30 text-white">
                    <span className="text-2xs text-slate-400 d-block">Financial Health Score</span>
                    <span className="h4 fw-bold text-emerald-400">{healthScore} / 100</span>
                    <span className="text-2xs text-emerald-400 d-block">
                      {healthScore >= 75 ? "Excellent Status" : (healthScore >= 50 ? "Moderate Status" : "High Risk Status")}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoanCalculator;
