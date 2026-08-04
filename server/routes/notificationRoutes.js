const express = require('express');
const router = express.Router();
const { sendPredictionEmail, sendSMSNotification } = require('../controllers/notificationController');

router.post('/email', sendPredictionEmail);
router.post('/sms', sendSMSNotification);

module.exports = router;
