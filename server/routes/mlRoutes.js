const express = require('express');
const router = express.Router();
const { predict, getModelInfo, getAccuracy, retrainModel, getHealth } = require('../controllers/mlController');

router.post('/predict', predict);
router.get('/model-info', getModelInfo);
router.get('/accuracy', getAccuracy);
router.post('/retrain', retrainModel);
router.get('/health', getHealth);

module.exports = router;
