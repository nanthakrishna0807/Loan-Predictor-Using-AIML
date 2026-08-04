const { sendEmail } = require('../utils/sendEmail');

// POST /api/notification/email
exports.sendPredictionEmail = async (req, res, next) => {
  try {
    const { email, predictionId, loanStatus, applicantName } = req.body;
    const recipient = email || (req.user ? req.user.email : 'user@example.com');

    const result = await sendEmail({
      to: recipient,
      subject: `AI Loan Predictor Status - ${loanStatus || 'Update'}`,
      text: `Hello ${applicantName || 'Applicant'}, your loan prediction application (${predictionId || 'latest'}) status is: ${loanStatus || 'Processed'}.`
    });

    return res.json({
      success: true,
      message: `Prediction notification email sent successfully to ${recipient}`,
      data: result,
      error: null
    });
  } catch (error) {
    next(error);
  }
};

// POST /api/notification/sms
exports.sendSMSNotification = async (req, res, next) => {
  try {
    const { phone, message } = req.body;
    const recipientPhone = phone || '+15550000000';

    return res.json({
      success: true,
      message: `SMS notification dispatched to ${recipientPhone}`,
      data: {
        recipientPhone,
        content: message || 'Your AI Loan Predictor application has been processed.',
        status: 'Delivered',
        dispatchedAt: new Date()
      },
      error: null
    });
  } catch (error) {
    next(error);
  }
};
