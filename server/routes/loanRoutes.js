const express = require('express');
const router = express.Router();
const { body } = require('express-validator');
const { predictLoan, getLoanHistory, getPredictionById, deletePrediction } = require('../controllers/loanController');
const { protect } = require('../middleware/auth');
const { validate } = require('../middleware/validator');

router.post(
  '/predict',
  protect,
  [
    body('AnnualIncome').notEmpty().withMessage('Annual Income is required'),
    body('LoanAmount').notEmpty().withMessage('Loan Amount is required'),
    body('CIBILScore').notEmpty().withMessage('CIBIL Score is required'),
    validate
  ],
  predictLoan
);

router.get('/history', protect, getLoanHistory);
router.get('/:id', protect, getPredictionById);
router.delete('/:id', protect, deletePrediction);

module.exports = router;
