const bcrypt = require('bcryptjs');
const { getMongoStatus } = require('../config/db');
const User = require('../models/User');
const { getMemoryUsers } = require('./authController');

// GET /api/settings/profile
exports.getSettings = async (req, res, next) => {
  try {
    const userId = req.user ? req.user.id : 'user_id_001';

    if (getMongoStatus()) {
      const user = await User.findById(userId).select('-password');
      return res.json({
        success: true,
        message: 'User settings retrieved successfully',
        data: {
          settings: {
            theme: 'dark',
            emailNotifications: true,
            smsAlerts: false,
            twoFactorAuth: false,
            user
          }
        },
        error: null
      });
    } else {
      const user = getMemoryUsers().find(u => u._id === userId) || getMemoryUsers()[1];
      return res.json({
        success: true,
        message: 'User settings retrieved successfully',
        data: {
          settings: {
            theme: 'dark',
            emailNotifications: true,
            smsAlerts: false,
            twoFactorAuth: false,
            user: { id: user._id, name: user.name, email: user.email, phone: user.phone, role: user.role }
          }
        },
        error: null
      });
    }
  } catch (error) {
    next(error);
  }
};

// PUT /api/settings/profile
exports.updateSettings = async (req, res, next) => {
  try {
    const userId = req.user ? req.user.id : 'user_id_001';
    const { name, phone, theme, emailNotifications, smsAlerts } = req.body;

    if (getMongoStatus()) {
      const user = await User.findByIdAndUpdate(userId, { name, phone }, { new: true }).select('-password');
      return res.json({
        success: true,
        message: 'User settings updated successfully',
        data: {
          settings: { theme, emailNotifications, smsAlerts, user }
        },
        error: null
      });
    } else {
      const user = getMemoryUsers().find(u => u._id === userId) || getMemoryUsers()[1];
      if (name) user.name = name;
      if (phone) user.phone = phone;

      return res.json({
        success: true,
        message: 'User settings updated successfully',
        data: {
          settings: {
            theme: theme || 'dark',
            emailNotifications: emailNotifications ?? true,
            smsAlerts: smsAlerts ?? false,
            user: { id: user._id, name: user.name, email: user.email, phone: user.phone, role: user.role }
          }
        },
        error: null
      });
    }
  } catch (error) {
    next(error);
  }
};

// PUT /api/settings/password
exports.changePassword = async (req, res, next) => {
  try {
    const userId = req.user ? req.user.id : 'user_id_001';
    const { currentPassword, newPassword } = req.body;

    if (!newPassword || newPassword.length < 6) {
      return res.status(400).json({
        success: false,
        message: 'Password change failed',
        data: null,
        error: { field: 'newPassword', message: 'New password must be at least 6 characters long' }
      });
    }

    const salt = await bcrypt.genSalt(10);
    const hashedPassword = await bcrypt.hash(newPassword, salt);

    if (getMongoStatus()) {
      await User.findByIdAndUpdate(userId, { password: hashedPassword });
    }

    return res.json({
      success: true,
      message: 'Password changed successfully',
      data: {},
      error: null
    });
  } catch (error) {
    next(error);
  }
};

// PUT /api/settings/avatar
exports.uploadAvatar = async (req, res, next) => {
  try {
    const avatarUrl = req.file ? `/uploads/${req.file.filename}` : '/uploads/default-avatar.png';
    const userId = req.user ? req.user.id : 'user_id_001';

    if (getMongoStatus()) {
      await User.findByIdAndUpdate(userId, { avatar: avatarUrl });
    } else {
      const user = getMemoryUsers().find(u => u._id === userId) || getMemoryUsers()[1];
      if (user) user.avatar = avatarUrl;
    }

    return res.json({
      success: true,
      message: 'Profile avatar uploaded successfully',
      data: { avatarUrl },
      error: null
    });
  } catch (error) {
    next(error);
  }
};
