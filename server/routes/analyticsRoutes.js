const express = require('express');
const router = express.Router();
const { getCibilAnalytics, getMonthlyAnalytics, getIncomeAnalytics, getLoanPurposeAnalytics, getRiskAnalytics } = require('../controllers/analyticsController');
const { protect } = require('../middleware/auth');
const { admin } = require('../middleware/admin');

router.get('/cibil', protect, admin, getCibilAnalytics);
router.get('/monthly', protect, admin, getMonthlyAnalytics);
router.get('/income', protect, admin, getIncomeAnalytics);
router.get('/loan-purpose', protect, admin, getLoanPurposeAnalytics);
router.get('/risk', protect, admin, getRiskAnalytics);

module.exports = router;
