const LoanApplication = require('../models/LoanApplication');
const Prediction = require('../models/Prediction');
const { getMongoStatus } = require('../config/db');
const { getMLPrediction } = require('../services/mlService');

// Memory fallback predictions & applications
const memoryApplications = [];
const memoryPredictions = [
  {
    _id: 'pred_demo_001',
    applicationId: 'app_demo_001',
    userId: 'user_id_001',
    applicantName: 'Demo Applicant',
    loanStatus: 'Approved',
    probability: 94.2,
    confidence: 96.0,
    riskLevel: 'Low',
    suggestedLoan: 2500000,
    estimatedEMI: 10624,
    interestRate: 8.5,
    recommendation: 'Application satisfies eligibility parameters with strong financial indicators. Recommended for approval up to ₹2,500,000 at 8.5% APR.',
    financialTips: ['Maintain CIBIL score above 750 by paying EMIs on time.', 'Keep credit card utilization under 30%.'],
    cibilScore: 780,
    annualIncome: 1200000,
    loanAmount: 500000,
    loanPurpose: 'Home Loan',
    tenure: 60,
    createdAt: new Date(Date.now() - 86400000 * 2)
  }
];

// POST /api/loan/predict
exports.predictLoan = async (req, res, next) => {
  try {
    const inputData = req.body;
    const userId = req.user ? req.user.id : 'user_id_001';

    const annualInc = Number(inputData.AnnualIncome || inputData.annualIncome || 500000);
    const monthlyInc = Number(inputData.MonthlyIncome || inputData.monthlyIncome || annualInc / 12);
    const cibil = Number(inputData.CIBILScore || inputData.cibilScore || 650);
    const loanAmt = Number(inputData.LoanAmount || inputData.loanAmount || 200000);
    const loanPurpose = inputData.LoanPurpose || inputData.loanPurpose || 'Personal Loan';
    const tenure = Number(inputData.LoanTenure || inputData.tenure || 36);

    // Step 1: Create & Save Loan Application
    const appPayload = {
      userId,
      applicantName: inputData.ApplicantName || inputData.name || (req.user ? req.user.name : 'Applicant'),
      annualIncome: annualInc,
      monthlyIncome: monthlyInc,
      cibilScore: cibil,
      loanAmount: loanAmt,
      loanPurpose,
      tenure,
      employmentType: inputData.EmploymentType || inputData.employmentType || 'Salaried',
      savings: Number(inputData.SavingsAmount || inputData.savings || 50000),
      bankBalance: Number(inputData.BankBalance || inputData.bankBalance || 50000),
      existingLoans: Number(inputData.NumberExistingLoans || inputData.existingLoans || 0),
      previousDefaults: Number(inputData.PreviousLoanDefaults || inputData.previousDefaults || 0),
      debtIncomeRatio: Number(inputData.DebtToIncomeRatio || inputData.debtIncomeRatio || 0.2),
      status: 'Pending',
      createdAt: new Date()
    };

    let savedAppId = 'app_' + Date.now();
    if (getMongoStatus()) {
      const savedApp = await LoanApplication.create(appPayload);
      savedAppId = savedApp._id;
    } else {
      memoryApplications.unshift({ _id: savedAppId, ...appPayload });
    }

    // Step 2: Forward payload to ML service (Flask / fallback engine)
    const mlResult = await getMLPrediction(inputData);

    // Update Application status
    const statusResult = mlResult.loan_status || 'Approved';
    if (getMongoStatus()) {
      await LoanApplication.findByIdAndUpdate(savedAppId, { status: statusResult });
    }

    // Step 3: Create & Save Prediction record
    const predictionPayload = {
      applicationId: savedAppId,
      userId,
      applicantName: appPayload.applicantName,
      loanStatus: statusResult,
      probability: mlResult.probability,
      confidence: mlResult.confidence,
      riskLevel: mlResult.risk,
      recommendation: mlResult.recommendation,
      estimatedEMI: mlResult.estimated_emi,
      interestRate: mlResult.interest_rate,
      suggestedLoan: mlResult.recommended_amount,
      financialTips: mlResult.tips,
      cibilScore: cibil,
      annualIncome: annualInc,
      loanAmount: loanAmt,
      loanPurpose,
      tenure,
      createdAt: new Date()
    };

    let savedPrediction;
    if (getMongoStatus()) {
      savedPrediction = await Prediction.create(predictionPayload);
    } else {
      savedPrediction = { _id: 'pred_' + Date.now(), ...predictionPayload };
      memoryPredictions.unshift(savedPrediction);
    }

    // Step 4: Return Standardized Response Format
    return res.status(201).json({
      success: true,
      message: 'Loan eligibility prediction generated successfully',
      data: {
        prediction: savedPrediction,
        loanStatus: savedPrediction.loanStatus,
        approved: savedPrediction.loanStatus === 'Approved',
        approvalProbability: savedPrediction.probability,
        probability: savedPrediction.probability,
        confidence: savedPrediction.confidence,
        confidenceScore: savedPrediction.confidence,
        riskLevel: savedPrediction.riskLevel,
        creditRiskLevel: savedPrediction.riskLevel,
        creditRiskColor: savedPrediction.loanStatus === 'Approved' ? '#22C55E' : '#EF4444',
        cibilCategory: cibil >= 750 ? 'Excellent' : (cibil >= 650 ? 'Good' : (cibil >= 550 ? 'Fair' : 'Poor')),
        cibilColor: cibil >= 750 ? '#22C55E' : (cibil >= 650 ? '#38BDF8' : (cibil >= 550 ? '#F59E0B' : '#EF4444')),
        suggestedLoan: savedPrediction.suggestedLoan,
        suggestedMaxLoan: savedPrediction.suggestedLoan,
        estimatedEMI: savedPrediction.estimatedEMI,
        emiEstimate: savedPrediction.estimatedEMI,
        interestRate: savedPrediction.interestRate,
        interestRateEstimate: savedPrediction.interestRate,
        recommendation: savedPrediction.recommendation,
        loanRecommendation: savedPrediction.recommendation,
        financialTips: savedPrediction.financialTips,
        financialImprovementTips: savedPrediction.financialTips
      },
      error: null
    });
  } catch (error) {
    next(error);
  }
};

// GET /api/loan/history
exports.getLoanHistory = async (req, res, next) => {
  try {
    const userId = req.user ? req.user.id : 'user_id_001';

    if (getMongoStatus()) {
      const query = req.user && req.user.role === 'admin' ? {} : { userId };
      const history = await Prediction.find(query).sort({ createdAt: -1 });
      return res.json({
        success: true,
        message: 'Loan prediction history retrieved successfully',
        data: { count: history.length, history },
        error: null
      });
    } else {
      let history = memoryPredictions;
      if (req.user && req.user.role !== 'admin') {
        history = memoryPredictions.filter(p => p.userId === userId || p.userId === 'user_id_001');
      }
      return res.json({
        success: true,
        message: 'Loan prediction history retrieved successfully',
        data: { count: history.length, history },
        error: null
      });
    }
  } catch (error) {
    next(error);
  }
};

// GET /api/loan/:id
exports.getPredictionById = async (req, res, next) => {
  try {
    const { id } = req.params;

    if (getMongoStatus()) {
      const prediction = await Prediction.findById(id);
      if (!prediction) {
        return res.status(404).json({
          success: false,
          message: 'Prediction record not found',
          data: null,
          error: { code: 'NOT_FOUND', message: 'No prediction exists with the given ID' }
        });
      }
      return res.json({
        success: true,
        message: 'Prediction record retrieved successfully',
        data: { prediction },
        error: null
      });
    } else {
      const prediction = memoryPredictions.find(p => p._id === id);
      if (!prediction) {
        return res.status(404).json({
          success: false,
          message: 'Prediction record not found',
          data: null,
          error: { code: 'NOT_FOUND', message: 'No prediction exists with the given ID' }
        });
      }
      return res.json({
        success: true,
        message: 'Prediction record retrieved successfully',
        data: { prediction },
        error: null
      });
    }
  } catch (error) {
    next(error);
  }
};

// DELETE /api/loan/:id
exports.deletePrediction = async (req, res, next) => {
  try {
    const { id } = req.params;

    if (getMongoStatus()) {
      await Prediction.findByIdAndDelete(id);
    } else {
      const index = memoryPredictions.findIndex(p => p._id === id);
      if (index !== -1) memoryPredictions.splice(index, 1);
    }

    return res.json({
      success: true,
      message: 'Prediction history record deleted successfully',
      data: { id },
      error: null
    });
  } catch (error) {
    next(error);
  }
};

exports.getMemoryPredictions = () => memoryPredictions;
exports.getMemoryApplications = () => memoryApplications;
