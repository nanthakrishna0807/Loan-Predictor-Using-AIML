const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const rateLimit = require('express-rate-limit');
const dotenv = require('dotenv');
const { errorHandler } = require('./middleware/errorHandler');

dotenv.config();

const app = express();

// Security Helmet Middleware
app.use(helmet());

// CORS Config
app.use(
  cors({
    origin: ['http://localhost:5173', 'http://localhost:3000', 'http://127.0.0.1:5173', 'http://127.0.0.1:3000'],
    credentials: true,
  })
);


// Morgan API Logger
app.use(morgan('dev'));

// Rate Limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 300, // 300 requests per window
  message: {
    success: false,
    message: 'Too many requests from this IP, please try again after 15 minutes',
    data: null,
    error: { code: 'RATE_LIMIT_EXCEEDED' }
  }
});
app.use('/api', limiter);

// Body Parsing
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Serve static uploads if needed
app.use('/uploads', express.static('uploads'));

// Health Endpoint
app.get('/health', (req, res) => {
  res.json({
    success: true,
    message: 'AI Loan Predictor API Server is Healthy',
    data: { timestamp: new Date() },
    error: null
  });
});

// API Routes
app.use('/api/health', require('./routes/healthRoutes'));
app.use('/api/auth', require('./routes/authRoutes'));
app.use('/api/loan', require('./routes/loanRoutes'));
app.use('/api/ml', require('./routes/mlRoutes'));
app.use('/api/admin', require('./routes/adminRoutes'));
app.use('/api/analytics', require('./routes/analyticsRoutes'));
app.use('/api/dashboard', require('./routes/dashboardRoutes'));
app.use('/api/report', require('./routes/reportRoutes'));
app.use('/api/notification', require('./routes/notificationRoutes'));
app.use('/api/settings', require('./routes/settingsRoutes'));



// 404 Handler
app.use((req, res, next) => {
  res.status(404).json({
    success: false,
    message: `Cannot ${req.method} ${req.url}`,
    data: null,
    error: { code: 'NOT_FOUND', message: 'API route not found' }
  });
});

// Centralized Error Handler
app.use(errorHandler);

module.exports = app;
