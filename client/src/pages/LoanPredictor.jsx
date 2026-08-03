import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { AuthContext } from '../context/AuthContext';
import DynamicCibilMeter from '../components/DynamicCibilMeter';
import { Cpu, User, DollarSign, Briefcase, FileText, CheckCircle2, AlertCircle } from 'lucide-react';

const LoanPredictor = () => {
  const { user } = useContext(AuthContext);
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    ApplicantName: user ? user.name : 'Aarav Sharma',
    Age: 32,
    Gender: 'Male',
    MaritalStatus: 'Married',
    Education: 'Graduate',
    EmploymentType: 'Salaried',
    SelfEmployed: 0,
    AnnualIncome: 1200000,
    MonthlyIncome: 100000,
    ExistingEMI: 15000,
    CreditCardUsage: 0.25,
    NumberExistingLoans: 1,
    LoanAmount: 500000,
    LoanPurpose: 'Home Loan',
    LoanTenure: 60,
    CIBILScore: 780,
    BankBalance: 350000,
    PropertyOwnership: 'Owned',
    Dependents: 2,
    PreviousLoanDefaults: 0,
    SavingsAmount: 350000,
    CreditUtilizationRatio: 0.25
  });

  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    let val = value;
    if (type === 'number' || name === 'CIBILScore' || name === 'AnnualIncome' || name === 'LoanAmount' || name === 'LoanTenure') {
      val = Number(value);
    }
    
    setFormData(prev => {
      const updated = { ...prev, [name]: val };
      // Auto compute monthly income if annual income changes
      if (name === 'AnnualIncome') {
        updated.MonthlyIncome = Math.round(Number(val) / 12);
      }
      if (name === 'BankBalance') {
        updated.SavingsAmount = Number(val);
      }
      if (name === 'CreditCardUsage') {
        updated.CreditUtilizationRatio = Number(val);
      }
      if (name === 'EmploymentType') {
        updated.SelfEmployed = (val === 'Self-Employed' || val === 'Business' || val === 'Freelancer') ? 1 : 0;
      }
      return updated;
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMsg('');

    try {
      const res = await axios.post('/api/loan/predict', formData);
      if (res.data && res.data.success) {
        const payloadData = res.data.data || res.data;
        const pred = payloadData.prediction || payloadData;
        navigate(`/result/${pred._id || 'demo'}`, { state: { prediction: pred } });
      } else {
        setErrorMsg(res.data.message || 'Prediction evaluation failed.');
      }
    } catch (err) {
      setErrorMsg(err.response?.data?.message || err.message || 'Error processing loan prediction.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="py-5">
      <div className="container">
        <div className="text-center max-w-2xl mx-auto mb-5">
          <span className="badge bg-blue-900/60 text-cyan-400 border border-cyan-500/30 px-3 py-1.5 rounded-pill text-xs fw-semibold mb-3">
            AI ML PREDICTION FORM
          </span>
          <h1 className="display-5 fw-bold text-white mb-2">Loan Application Predictor</h1>
          <p className="text-slate-300">Fill in applicant personal & financial metrics for instant ML evaluation.</p>
        </div>

        {errorMsg && (
          <div className="alert alert-danger glass-card border-rose-500/50 text-rose-300 d-flex align-items-center gap-2 mb-4">
            <AlertCircle size={20} />
            <span>{errorMsg}</span>
          </div>
        )}

        <div className="row g-4">
          {/* Main Application Form */}
          <div className="col-lg-8">
            <form onSubmit={handleSubmit} className="glass-card p-4 p-md-5">
              <h5 className="fw-bold text-cyan-400 border-b border-slate-800 pb-3 mb-4 d-flex align-items-center gap-2">
                <User size={20}/> 1. Personal & Demographics
              </h5>
              
              <div className="row g-3 mb-4">
                <div className="col-md-6">
                  <label className="text-xs text-slate-300 mb-1 d-block">Applicant Full Name *</label>
                  <input
                    type="text"
                    name="ApplicantName"
                    className="fintech-input"
                    value={formData.ApplicantName}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div className="col-md-3">
                  <label className="text-xs text-slate-300 mb-1 d-block">Age (Years) *</label>
                  <input
                    type="number"
                    name="Age"
                    className="fintech-input"
                    min="18"
                    max="80"
                    value={formData.Age}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div className="col-md-3">
                  <label className="text-xs text-slate-300 mb-1 d-block">Gender *</label>
                  <select name="Gender" className="fintech-input" value={formData.Gender} onChange={handleChange}>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                  </select>
                </div>
                <div className="col-md-4">
                  <label className="text-xs text-slate-300 mb-1 d-block">Marital Status *</label>
                  <select name="MaritalStatus" className="fintech-input" value={formData.MaritalStatus} onChange={handleChange}>
                    <option value="Single">Single</option>
                    <option value="Married">Married</option>
                    <option value="Divorced">Divorced</option>
                  </select>
                </div>
                <div className="col-md-4">
                  <label className="text-xs text-slate-300 mb-1 d-block">Education *</label>
                  <select name="Education" className="fintech-input" value={formData.Education} onChange={handleChange}>
                    <option value="Graduate">Graduate</option>
                    <option value="Post Graduate">Post Graduate</option>
                    <option value="High School">High School</option>
                    <option value="Doctorate">Doctorate</option>
                  </select>
                </div>
                <div className="col-md-4">
                  <label className="text-xs text-slate-300 mb-1 d-block">Dependents *</label>
                  <input
                    type="number"
                    name="Dependents"
                    className="fintech-input"
                    min="0"
                    max="10"
                    value={formData.Dependents}
                    onChange={handleChange}
                  />
                </div>
              </div>

              <h5 className="fw-bold text-cyan-400 border-b border-slate-800 pb-3 mb-4 d-flex align-items-center gap-2">
                <Briefcase size={20}/> 2. Employment & Income Details
              </h5>

              <div className="row g-3 mb-4">
                <div className="col-md-4">
                  <label className="text-xs text-slate-300 mb-1 d-block">Employment Type *</label>
                  <select name="EmploymentType" className="fintech-input" value={formData.EmploymentType} onChange={handleChange}>
                    <option value="Salaried">Salaried</option>
                    <option value="Self-Employed">Self-Employed</option>
                    <option value="Business">Business Owner</option>
                    <option value="Freelancer">Freelancer</option>
                  </select>
                </div>
                <div className="col-md-4">
                  <label className="text-xs text-slate-300 mb-1 d-block">Annual Gross Income (₹) *</label>
                  <input
                    type="number"
                    name="AnnualIncome"
                    className="fintech-input"
                    min="100000"
                    value={formData.AnnualIncome}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div className="col-md-4">
                  <label className="text-xs text-slate-300 mb-1 d-block">Monthly Income (₹)</label>
                  <input
                    type="number"
                    name="MonthlyIncome"
                    className="fintech-input"
                    value={formData.MonthlyIncome}
                    onChange={handleChange}
                  />
                </div>
                <div className="col-md-4">
                  <label className="text-xs text-slate-300 mb-1 d-block">Existing EMIs (₹) *</label>
                  <input
                    type="number"
                    name="ExistingEMI"
                    className="fintech-input"
                    min="0"
                    value={formData.ExistingEMI}
                    onChange={handleChange}
                  />
                </div>
                <div className="col-md-4">
                  <label className="text-xs text-slate-300 mb-1 d-block">Bank Liquid Savings (₹) *</label>
                  <input
                    type="number"
                    name="BankBalance"
                    className="fintech-input"
                    min="0"
                    value={formData.BankBalance}
                    onChange={handleChange}
                  />
                </div>
                <div className="col-md-4">
                  <label className="text-xs text-slate-300 mb-1 d-block">Property Ownership *</label>
                  <select name="PropertyOwnership" className="fintech-input" value={formData.PropertyOwnership} onChange={handleChange}>
                    <option value="Owned">Owned</option>
                    <option value="Rented">Rented</option>
                    <option value="Mortgaged">Mortgaged</option>
                  </select>
                </div>
              </div>

              <h5 className="fw-bold text-cyan-400 border-b border-slate-800 pb-3 mb-4 d-flex align-items-center gap-2">
                <DollarSign size={20}/> 3. Requested Loan & Credit History
              </h5>

              <div className="row g-3 mb-4">
                <div className="col-md-4">
                  <label className="text-xs text-slate-300 mb-1 d-block">Requested Loan Amount (₹) *</label>
                  <input
                    type="number"
                    name="LoanAmount"
                    className="fintech-input"
                    min="10000"
                    value={formData.LoanAmount}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div className="col-md-4">
                  <label className="text-xs text-slate-300 mb-1 d-block">Loan Purpose *</label>
                  <select name="LoanPurpose" className="fintech-input" value={formData.LoanPurpose} onChange={handleChange}>
                    <option value="Home Loan">Home Loan</option>
                    <option value="Personal Loan">Personal Loan</option>
                    <option value="Education Loan">Education Loan</option>
                    <option value="Car Loan">Car Loan</option>
                    <option value="Business Loan">Business Loan</option>
                    <option value="Medical Emergency">Medical Emergency</option>
                  </select>
                </div>
                <div className="col-md-4">
                  <label className="text-xs text-slate-300 mb-1 d-block">Tenure (Months) *</label>
                  <select name="LoanTenure" className="fintech-input" value={formData.LoanTenure} onChange={handleChange}>
                    <option value={12}>12 Months (1 Yr)</option>
                    <option value={24}>24 Months (2 Yrs)</option>
                    <option value={36}>36 Months (3 Yrs)</option>
                    <option value={48}>48 Months (4 Yrs)</option>
                    <option value={60}>60 Months (5 Yrs)</option>
                    <option value={120}>120 Months (10 Yrs)</option>
                  </select>
                </div>

                <div className="col-md-4">
                  <label className="text-xs text-slate-300 mb-1 d-block">CIBIL Score (300 – 900) *</label>
                  <input
                    type="number"
                    name="CIBILScore"
                    className="fintech-input"
                    min="300"
                    max="900"
                    value={formData.CIBILScore}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div className="col-md-4">
                  <label className="text-xs text-slate-300 mb-1 d-block">Credit Card Usage (%)</label>
                  <input
                    type="number"
                    step="0.05"
                    min="0"
                    max="1"
                    name="CreditCardUsage"
                    className="fintech-input"
                    value={formData.CreditCardUsage}
                    onChange={handleChange}
                  />
                </div>
                <div className="col-md-4">
                  <label className="text-xs text-slate-300 mb-1 d-block">Previous Defaults? *</label>
                  <select name="PreviousLoanDefaults" className="fintech-input" value={formData.PreviousLoanDefaults} onChange={handleChange}>
                    <option value={0}>No (0 Defaults)</option>
                    <option value={1}>Yes (1+ Past Default)</option>
                  </select>
                </div>
              </div>

              <div className="pt-3 border-t border-slate-800">
                <button type="submit" disabled={loading} className="btn btn-fintech btn-lg w-100 py-3 text-base">
                  {loading ? (
                    <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                  ) : (
                    <Cpu size={20} className="me-2"/>
                  )}
                  {loading ? "Evaluating Machine Learning Model..." : "Evaluate Loan Eligibility Now"}
                </button>
              </div>
            </form>
          </div>

          {/* Side Live CIBIL Meter Preview & Guidelines */}
          <div className="col-lg-4">
            <div className="sticky-top" style={{ top: 90 }}>
              <DynamicCibilMeter score={formData.CIBILScore} threshold={650} />

              <div className="glass-card p-4 text-white mt-4">
                <h6 className="fw-semibold text-slate-200 mb-3">Model Verification Parameters</h6>
                <ul className="list-unstyled text-xs text-slate-400 d-flex flex-column gap-2 mb-0">
                  <li className="d-flex align-items-center gap-2"><CheckCircle2 size={16} className="text-cyan-400"/> CIBIL Score threshold: 650</li>
                  <li className="d-flex align-items-center gap-2"><CheckCircle2 size={16} className="text-cyan-400"/> Debt-to-Income cap target: &lt; 50%</li>
                  <li className="d-flex align-items-center gap-2"><CheckCircle2 size={16} className="text-cyan-400"/> Liquid reserve buffer check</li>
                  <li className="d-flex align-items-center gap-2"><CheckCircle2 size={16} className="text-cyan-400"/> ML Classifier: Random Forest</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoanPredictor;
