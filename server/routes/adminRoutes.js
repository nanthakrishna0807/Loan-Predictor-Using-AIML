const express = require('express');
const router = express.Router();
const { getDashboardStats, getUsers, deleteUser, updateUser, getApplications, getPredictions, getReports, updateApplicationStatus } = require('../controllers/adminController');
const { protect } = require('../middleware/auth');
const { admin } = require('../middleware/admin');

router.get('/dashboard', protect, admin, getDashboardStats);
router.get('/users', protect, admin, getUsers);
router.delete('/user/:id', protect, admin, deleteUser);
router.put('/user/:id', protect, admin, updateUser);
router.get('/applications', protect, admin, getApplications);
router.get('/predictions', protect, admin, getPredictions);
router.get('/reports', protect, admin, getReports);
router.put('/application/:id', protect, admin, updateApplicationStatus);

module.exports = router;

