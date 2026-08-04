const express = require('express');
const router = express.Router();
const { getDashboardOverview, getLoanStatusAnalytics, getCibilAnalytics, getMonthlyAnalytics, getIncomeAnalytics, getLoanPurposeAnalytics, getRiskAnalytics, getEmploymentAnalytics } = require('../controllers/analyticsController');
const { protect } = require('../middleware/auth');
const { admin } = require('../middleware/admin');

router.get('/dashboard', protect, admin, getDashboardOverview);
router.get('/loan-status', protect, admin, getLoanStatusAnalytics);
router.get('/monthly', protect, admin, getMonthlyAnalytics);
router.get('/income', protect, admin, getIncomeAnalytics);
router.get('/cibil', protect, admin, getCibilAnalytics);
router.get('/risk', protect, admin, getRiskAnalytics);
router.get('/loan-purpose', protect, admin, getLoanPurposeAnalytics);
router.get('/employment', protect, admin, getEmploymentAnalytics);

module.exports = router;

