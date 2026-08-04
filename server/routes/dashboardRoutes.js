const express = require('express');
const router = express.Router();
const { getSummary, getRecentPredictions, getLoanHistory, getRecommendations } = require('../controllers/dashboardController');
const { protect } = require('../middleware/auth');

router.get('/summary', protect, getSummary);
router.get('/recent-predictions', protect, getRecentPredictions);
router.get('/loan-history', protect, getLoanHistory);
router.get('/recommendations', protect, getRecommendations);

module.exports = router;
