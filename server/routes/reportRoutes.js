const express = require('express');
const router = express.Router();
const { downloadPDF, exportExcel, exportCSV } = require('../controllers/reportController');
const { protect } = require('../middleware/auth');

router.get('/pdf/:id', protect, downloadPDF);
router.get('/excel', protect, exportExcel);
router.get('/csv', protect, exportCSV);

module.exports = router;
