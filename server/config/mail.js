const nodemailer = require('nodemailer');

const createTransporter = () => {
  return nodemailer.createTransport({
    host: process.env.SMTP_HOST || 'smtp.mailtrap.io',
    port: process.env.SMTP_PORT || 2525,
    auth: {
      user: process.env.SMTP_USER || 'demo_user',
      pass: process.env.SMTP_PASS || 'demo_pass'
    }
  });
};

module.exports = { createTransporter };
