const { getMongoStatus, getDbDetails } = require('../config/db');
const TestRecord = require('../models/TestRecord');

const startTime = Date.now();

// GET /api/health/database
exports.getDatabaseHealth = async (req, res, next) => {
  try {
    const isConnected = getMongoStatus();
    const details = getDbDetails();

    const statusCode = isConnected ? 200 : 503;

    return res.status(statusCode).json({
      success: isConnected,
      message: isConnected ? 'MongoDB Atlas is connected and healthy' : 'MongoDB Atlas is disconnected',
      data: {
        status: isConnected ? 'connected' : 'disconnected',
        databaseName: details.databaseName,
        connectionState: details.connectionState,
        connectionStateText: details.connectionStateText,
        host: details.host,
        uptimeSeconds: Math.floor((Date.now() - startTime) / 1000),
        timestamp: new Date()
      },
      error: isConnected ? null : { code: 'DATABASE_DISCONNECTED', message: 'Database connection inactive' }
    });
  } catch (error) {
    next(error);
  }
};

// GET /api/health/server
exports.getServerHealth = async (req, res, next) => {
  try {
    return res.json({
      success: true,
      message: 'Express backend server is running and healthy',
      data: {
        status: 'online',
        environment: process.env.NODE_ENV || 'development',
        uptimeSeconds: Math.floor((Date.now() - startTime) / 1000),
        memoryUsage: process.memoryUsage(),
        timestamp: new Date()
      },
      error: null
    });
  } catch (error) {
    next(error);
  }
};

// POST /api/health/test-db
exports.createTestRecord = async (req, res, next) => {
  try {
    const { title, testData } = req.body;
    
    if (getMongoStatus()) {
      const record = await TestRecord.create({
        title: title || 'MongoDB Atlas Live CRUD Verification',
        testData: testData || { verifiedAt: new Date(), source: 'Express Backend Health Suite' }
      });

      return res.status(201).json({
        success: true,
        message: 'Sample record created in MongoDB Atlas successfully',
        data: { record },
        error: null
      });
    } else {
      return res.status(503).json({
        success: false,
        message: 'Cannot create record: MongoDB Atlas is not connected',
        data: null,
        error: { code: 'DATABASE_DISCONNECTED', message: 'Database connection inactive' }
      });
    }
  } catch (error) {
    next(error);
  }
};

// GET /api/health/test-db
exports.getTestRecords = async (req, res, next) => {
  try {
    if (getMongoStatus()) {
      const records = await TestRecord.find({}).sort({ createdAt: -1 }).limit(10);
      return res.json({
        success: true,
        message: 'Sample records retrieved from MongoDB Atlas successfully',
        data: { count: records.length, records },
        error: null
      });
    } else {
      return res.status(503).json({
        success: false,
        message: 'Cannot retrieve records: MongoDB Atlas is not connected',
        data: null,
        error: { code: 'DATABASE_DISCONNECTED', message: 'Database connection inactive' }
      });
    }
  } catch (error) {
    next(error);
  }
};
