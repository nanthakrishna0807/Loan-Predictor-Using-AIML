const mongoose = require('mongoose');

const SystemLogSchema = new mongoose.Schema({
  event: String,
  user: String,
  details: String,
  ip: String,
  timestamp: { type: Date, default: Date.now }
});

module.exports = mongoose.model('SystemLog', SystemLogSchema);
