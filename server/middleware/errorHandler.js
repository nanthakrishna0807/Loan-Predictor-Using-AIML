const errorHandler = (err, req, res, next) => {
  console.error('API Error Trace:', err);

  const statusCode = err.statusCode || res.statusCode === 200 ? 500 : res.statusCode;

  return res.status(statusCode).json({
    success: false,
    message: err.message || 'Internal Server Error',
    data: null,
    error: {
      code: err.code || 'SERVER_ERROR',
      message: err.message || 'An unexpected error occurred'
    }
  });
};

module.exports = { errorHandler };
