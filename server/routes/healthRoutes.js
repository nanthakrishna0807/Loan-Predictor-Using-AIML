const express = require('express');
const router = express.Router();
const { getDatabaseHealth, getServerHealth, createTestRecord, getTestRecords } = require('../controllers/healthController');

router.get('/database', getDatabaseHealth);
router.get('/server', getServerHealth);
router.route('/test-db')
  .get(getTestRecords)
  .post(createTestRecord);

module.exports = router;
