const express = require('express');
const router = express.Router();
const multer = require('multer');
const path = require('path');
const { getSettings, updateSettings, changePassword, uploadAvatar } = require('../controllers/settingsController');
const { protect } = require('../middleware/auth');

// Multer Disk Storage setup
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/');
  },
  filename: (req, file, cb) => {
    cb(null, `avatar-${Date.now()}${path.extname(file.originalname)}`);
  }
});
const upload = multer({ storage });

router.get('/profile', protect, getSettings);
router.put('/profile', protect, updateSettings);
router.put('/password', protect, changePassword);
router.put('/avatar', protect, upload.single('avatar'), uploadAvatar);

module.exports = router;
