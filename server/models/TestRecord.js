const mongoose = require('mongoose');

const TestRecordSchema = new mongoose.Schema({
  title: {
    type: String,
    required: [true, 'Title is required for database test record'],
    default: 'Database Health Test'
  },
  status: {
    type: String,
    enum: ['Active', 'Completed', 'Archived'],
    default: 'Active'
  },
  testData: {
    type: Object,
    default: { message: 'MongoDB Atlas Write Verification Passed' }
  },
  createdAt: {
    type: Date,
    default: Date.now
  }
});

module.exports = mongoose.model('TestRecord', TestRecordSchema);
