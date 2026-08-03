module.exports = {
  accessSecret: process.env.JWT_SECRET || 'super_secret_jwt_access_key_2026',
  refreshSecret: process.env.JWT_REFRESH_SECRET || 'super_secret_jwt_refresh_key_2026',
  accessExpire: process.env.JWT_EXPIRE || '1d',
  refreshExpire: process.env.JWT_REFRESH_EXPIRE || '7d'
};
