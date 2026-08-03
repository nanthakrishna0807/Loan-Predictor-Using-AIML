const mongoose = require('mongoose');

const LoanApplicationSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  applicantName: { type: String, default: '' },
  annualIncome: { type: Number, required: true },
  monthlyIncome: { type: Number, required: true },
  cibilScore: { type: Number, required: true },
  loanAmount: { type: Number, required: true },
  loanPurpose: { type: String, required: true },
  tenure: { type: Number, required: true },
  employmentType: { type: String, default: 'Salaried' },
  savings: { type: Number, default: 0 },
  bankBalance: { type: Number, default: 0 },
  existingLoans: { type: Number, default: 0 },
  previousDefaults: { type: Number, default: 0 },
  debtIncomeRatio: { type: Number, default: 0 },
  status: { type: String, enum: ['Approved', 'Rejected', 'Pending'], default: 'Pending' },
  createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('LoanApplication', LoanApplicationSchema);
