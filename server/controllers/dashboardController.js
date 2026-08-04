const { getMongoStatus } = require('../config/db');
const Prediction = require('../models/Prediction');
const { getMemoryPredictions } = require('./loanController');

// GET /api/dashboard/summary
exports.getSummary = async (req, res, next) => {
  try {
    const userId = req.user ? req.user.id : 'user_id_001';
    let predictions = [];

    if (getMongoStatus()) {
      predictions = await Prediction.find({ userId }).sort({ createdAt: -1 });
    } else {
      predictions = getMemoryPredictions().filter(p => p.userId === userId || p.userId === 'user_id_001');
    }

    const totalApplications = predictions.length;
    const approvedCount = predictions.filter(p => p.loanStatus === 'Approved' || p.approved).length;
    const latestPrediction = predictions[0] || null;

    return res.json({
      success: true,
      message: 'User dashboard summary retrieved successfully',
      data: {
        summary: {
          totalApplications,
          approvedApplications: approvedCount,
          pendingApplications: 0,
          rejectedApplications: totalApplications - approvedCount,
          latestScore: latestPrediction ? latestPrediction.cibilScore : 780,
          creditHealth: 'Strong',
          suggestedMaxCredit: latestPrediction ? latestPrediction.suggestedLoan : 2500000
        }
      },
      error: null
    });
  } catch (error) {
    next(error);
  }
};

// GET /api/dashboard/recent-predictions
exports.getRecentPredictions = async (req, res, next) => {
  try {
    const userId = req.user ? req.user.id : 'user_id_001';
    let predictions = [];

    if (getMongoStatus()) {
      predictions = await Prediction.find({ userId }).sort({ createdAt: -1 }).limit(5);
    } else {
      predictions = getMemoryPredictions()
        .filter(p => p.userId === userId || p.userId === 'user_id_001')
        .slice(0, 5);
    }

    return res.json({
      success: true,
      message: 'Recent predictions retrieved successfully',
      data: { predictions },
      error: null
    });
  } catch (error) {
    next(error);
  }
};

// GET /api/dashboard/loan-history
exports.getLoanHistory = async (req, res, next) => {
  try {
    const userId = req.user ? req.user.id : 'user_id_001';
    let history = [];

    if (getMongoStatus()) {
      history = await Prediction.find({ userId }).sort({ createdAt: -1 });
    } else {
      history = getMemoryPredictions().filter(p => p.userId === userId || p.userId === 'user_id_001');
    }

    return res.json({
      success: true,
      message: 'User loan history retrieved successfully',
      data: { count: history.length, history },
      error: null
    });
  } catch (error) {
    next(error);
  }
};

// GET /api/dashboard/recommendations
exports.getRecommendations = async (req, res, next) => {
  try {
    return res.json({
      success: true,
      message: 'Financial recommendations retrieved successfully',
      data: {
        recommendations: [
          {
            id: 1,
            title: 'Maintain Low Credit Utilization',
            description: 'Keep total credit card balances below 30% of total credit limits to maximize CIBIL score.'
          },
          {
            id: 2,
            title: 'Optimize EMI Tenure',
            description: 'Selecting a 60-month loan tenure balances affordable monthly payments with manageable interest rates.'
          },
          {
            id: 3,
            title: 'Consolidate High-Interest Debts',
            description: 'Refinance existing high-interest credit card debt with a personal loan to improve DTI ratio.'
          }
        ]
      },
      error: null
    });
  } catch (error) {
    next(error);
  }
};
