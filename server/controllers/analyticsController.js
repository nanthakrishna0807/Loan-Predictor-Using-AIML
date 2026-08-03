// GET /api/analytics/cibil
exports.getCibilAnalytics = async (req, res, next) => {
  try {
    return res.json({
      success: true,
      message: 'CIBIL distribution analytics retrieved',
      data: {
        distribution: {
          poor: 12,      // 300 - 549
          fair: 24,      // 550 - 649
          good: 42,      // 650 - 749
          excellent: 22  // 750 - 900
        }
      },
      error: null
    });
  } catch (error) {
    next(error);
  }
};

// GET /api/analytics/monthly
exports.getMonthlyAnalytics = async (req, res, next) => {
  try {
    return res.json({
      success: true,
      message: 'Monthly analytics retrieved',
      data: {
        monthly: [
          { month: 'Jan', count: 45, approved: 32, rejected: 13 },
          { month: 'Feb', count: 52, approved: 38, rejected: 14 },
          { month: 'Mar', count: 68, approved: 49, rejected: 19 },
          { month: 'Apr', count: 80, approved: 58, rejected: 22 },
          { month: 'May', count: 95, approved: 70, rejected: 25 },
          { month: 'Jun', count: 110, approved: 82, rejected: 28 },
          { month: 'Jul', count: 142, approved: 98, rejected: 44 }
        ]
      },
      error: null
    });
  } catch (error) {
    next(error);
  }
};

// GET /api/analytics/income
exports.getIncomeAnalytics = async (req, res, next) => {
  try {
    return res.json({
      success: true,
      message: 'Income statistics analytics retrieved',
      data: {
        incomeStats: [
          { bracket: '₹3L Inc', avgLoan: 400000 },
          { bracket: '₹6L Inc', avgLoan: 1200000 },
          { bracket: '₹9L Inc', avgLoan: 1500000 },
          { bracket: '₹12L Inc', avgLoan: 2500000 },
          { bracket: '₹18L Inc', avgLoan: 3500000 },
          { bracket: '₹24L Inc', avgLoan: 5000000 }
        ]
      },
      error: null
    });
  } catch (error) {
    next(error);
  }
};

// GET /api/analytics/loan-purpose
exports.getLoanPurposeAnalytics = async (req, res, next) => {
  try {
    return res.json({
      success: true,
      message: 'Loan purpose analytics retrieved',
      data: {
        purposes: {
          homeLoan: 38,
          personalLoan: 25,
          educationLoan: 15,
          carLoan: 12,
          businessLoan: 10
        }
      },
      error: null
    });
  } catch (error) {
    next(error);
  }
};

// GET /api/analytics/risk
exports.getRiskAnalytics = async (req, res, next) => {
  try {
    return res.json({
      success: true,
      message: 'Risk distribution analytics retrieved',
      data: {
        riskDistribution: {
          low: 54,
          medium: 26,
          high: 14,
          critical: 6
        }
      },
      error: null
    });
  } catch (error) {
    next(error);
  }
};
