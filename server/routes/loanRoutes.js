const express = require('express');
const router = express.Router();
const { predictLoan, calculateEMI, updateLoanApplication, getLoanHistory, getPredictionById, deletePrediction } = require('../controllers/loanController');
const { protect } = require('../middleware/auth');

router.post('/predict', protect, predictLoan);
router.post('/calculate-emi', calculateEMI);
router.get('/history', protect, getLoanHistory);
router.get('/:id', protect, getPredictionById);
router.put('/:id', protect, updateLoanApplication);
router.delete('/:id', protect, deletePrediction);

module.exports = router;

