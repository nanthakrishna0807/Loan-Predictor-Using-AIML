const jwt = require('jsonwebtoken');
const jwtConfig = require('../config/jwt');

const protect = (req, res, next) => {
  let token;
  if (req.headers.authorization && req.headers.authorization.startsWith('Bearer')) {
    token = req.headers.authorization.split(' ')[1];
  }

  if (!token) {
    return res.status(401).json({
      success: false,
      message: 'Authentication failed: No token provided',
      data: null,
      error: { code: 'UNAUTHORIZED', message: 'Bearer token is missing' }
    });
  }

  try {
    const decoded = jwt.verify(token, jwtConfig.accessSecret);
    req.user = decoded;
    next();
  } catch (error) {
    return res.status(401).json({
      success: false,
      message: 'Authentication failed: Invalid or expired token',
      data: null,
      error: { code: 'INVALID_TOKEN', message: error.message }
    });
  }
};

module.exports = { protect };
