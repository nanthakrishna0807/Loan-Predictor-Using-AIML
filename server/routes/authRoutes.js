const express = require('express');
const router = express.Router();
const { body } = require('express-validator');
const { register, login, logout, forgotPassword, resetPassword, getProfile, updateProfile, deleteProfile } = require('../controllers/authController');
const { protect } = require('../middleware/auth');
const { validate } = require('../middleware/validator');

router.post(
  '/register',
  [
    body('name').notEmpty().withMessage('Full Name is required'),
    body('email').isEmail().withMessage('Please provide a valid email address'),
    body('password').isLength({ min: 6 }).withMessage('Password must be at least 6 characters long'),
    validate
  ],
  register
);

router.post(
  '/login',
  [
    body('email').isEmail().withMessage('Please provide a valid email address'),
    body('password').notEmpty().withMessage('Password is required'),
    validate
  ],
  login
);

router.post('/logout', logout);

router.post(
  '/forgot-password',
  [
    body('email').isEmail().withMessage('Please provide a valid email address'),
    validate
  ],
  forgotPassword
);

router.post(
  '/reset-password',
  [
    body('password').isLength({ min: 6 }).withMessage('Password must be at least 6 characters long'),
    validate
  ],
  resetPassword
);

router.get('/profile', protect, getProfile);
router.put('/profile', protect, updateProfile);
router.delete('/profile', protect, deleteProfile);

module.exports = router;

