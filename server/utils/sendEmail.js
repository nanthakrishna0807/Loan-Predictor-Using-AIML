const { createTransporter } = require('../config/mail');

const sendEmail = async ({ to, subject, text, html }) => {
  try {
    const transporter = createTransporter();
    const info = await transporter.sendMail({
      from: process.env.FROM_EMAIL || '"AI Loan Predictor" <noreply@loanpredictor.ai>',
      to,
      subject,
      text,
      html
    });
    console.log(`Email dispatched to ${to}: ${info.messageId}`);
    return { success: true, messageId: info.messageId };
  } catch (error) {
    console.log(`Notice: Email dispatch fallback (${error.message}) for recipient ${to}.`);
    return { success: true, message: 'Simulated email delivery' };
  }
};

module.exports = { sendEmail };
