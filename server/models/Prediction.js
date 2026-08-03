const mongoose = require('mongoose');

const PredictionSchema = new mongoose.Schema({
  applicationId: { type: mongoose.Schema.Types.ObjectId, ref: 'LoanApplication' },
  userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
  applicantName: { type: String, default: '' },
  loanStatus: { type: String, enum: ['Approved', 'Rejected'], required: true },
  probability: { type: Number, required: true },
  confidence: { type: Number, required: true },
  riskLevel: { type: String, required: true },
  recommendation: { type: String, required: true },
  estimatedEMI: { type: Number, required: true },
  interestRate: { type: Number, required: true },
  suggestedLoan: { type: Number, required: true },
  financialTips: [{ type: String }],
  cibilScore: Number,
  annualIncome: Number,
  loanAmount: Number,
  loanPurpose: String,
  tenure: Number,
  createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Prediction', PredictionSchema);
