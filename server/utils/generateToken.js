const jwt = require('jsonwebtoken');
const jwtConfig = require('../config/jwt');

const generateAccessToken = (user) => {
  return jwt.sign(
    { id: user._id || user.id, email: user.email, role: user.role, name: user.name },
    jwtConfig.accessSecret,
    { expiresIn: jwtConfig.accessExpire }
  );
};

const generateRefreshToken = (user) => {
  return jwt.sign(
    { id: user._id || user.id, email: user.email },
    jwtConfig.refreshSecret,
    { expiresIn: jwtConfig.refreshExpire }
  );
};

module.exports = { generateAccessToken, generateRefreshToken };
