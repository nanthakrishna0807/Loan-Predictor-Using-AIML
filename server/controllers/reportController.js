const { getMongoStatus } = require('../config/db');
const Prediction = require('../models/Prediction');
const { getMemoryPredictions } = require('./loanController');

// GET /api/report/pdf/:id
exports.downloadPDF = async (req, res, next) => {
  try {
    const { id } = req.params;
    let prediction = null;

    if (getMongoStatus()) {
      prediction = await Prediction.findById(id);
    } else {
      prediction = getMemoryPredictions().find(p => p._id === id) || getMemoryPredictions()[0];
    }

    if (!prediction) {
      return res.status(404).json({
        success: false,
        message: 'Prediction record not found for PDF export',
        data: null,
        error: { code: 'NOT_FOUND', message: 'No prediction found with given ID' }
      });
    }

    // Return structured report metadata ready for client PDF renderer / stream
    return res.json({
      success: true,
      message: 'PDF prediction report data generated successfully',
      data: {
        reportType: 'PDF_LOAN_PREDICTION_SUMMARY',
        predictionId: prediction._id,
        applicantName: prediction.applicantName,
        loanStatus: prediction.loanStatus,
        approvalProbability: prediction.probability,
        confidenceScore: prediction.confidence,
        riskLevel: prediction.riskLevel,
        loanAmount: prediction.loanAmount,
        cibilScore: prediction.cibilScore,
        estimatedEMI: prediction.estimatedEMI,
        interestRate: prediction.interestRate,
        generatedAt: new Date()
      },
      error: null
    });
  } catch (error) {
    next(error);
  }
};

// GET /api/report/excel
exports.exportExcel = async (req, res, next) => {
  try {
    let predictions = [];
    if (getMongoStatus()) {
      predictions = await Prediction.find({}).sort({ createdAt: -1 });
    } else {
      predictions = getMemoryPredictions();
    }

    return res.json({
      success: true,
      message: 'Excel export report dataset generated successfully',
      data: {
        fileName: `Loan_Predictions_Export_${Date.now()}.xlsx`,
        format: 'xlsx',
        recordsCount: predictions.length,
        records: predictions
      },
      error: null
    });
  } catch (error) {
    next(error);
  }
};

// GET /api/report/csv
exports.exportCSV = async (req, res, next) => {
  try {
    let predictions = [];
    if (getMongoStatus()) {
      predictions = await Prediction.find({}).sort({ createdAt: -1 });
    } else {
      predictions = getMemoryPredictions();
    }

    const csvHeaders = 'ID,Applicant Name,Loan Status,Probability,Confidence,Risk Level,CIBIL Score,Loan Amount,EMI,Created At\n';
    const csvRows = predictions.map(p => 
      `"${p._id}","${p.applicantName}","${p.loanStatus}",${p.probability},${p.confidence},"${p.riskLevel}",${p.cibilScore},${p.loanAmount},${p.estimatedEMI},"${p.createdAt}"`
    ).join('\n');

    res.setHeader('Content-Type', 'text/csv');
    res.setHeader('Content-Disposition', `attachment; filename=loan_predictions_${Date.now()}.csv`);
    return res.status(200).send(csvHeaders + csvRows);
  } catch (error) {
    next(error);
  }
};
