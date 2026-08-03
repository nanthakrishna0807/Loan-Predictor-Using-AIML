const { validationResult } = require('express-validator');

const validate = (req, res, next) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    const firstErr = errors.array()[0];
    return res.status(400).json({
      success: false,
      message: 'Validation failed',
      data: null,
      error: {
        field: firstErr.path || firstErr.param,
        message: firstErr.msg
      }
    });
  }
  next();
};

module.exports = { validate };
