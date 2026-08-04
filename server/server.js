const app = require('./app');
const { connectDB } = require('./config/db');

const startServer = async () => {
  // Connect to MongoDB Atlas first before starting Express listener
  await connectDB();

  const PORT = process.env.PORT || 5000;

  app.listen(PORT, () => {
    console.log(`🚀 Production Express Backend running on port ${PORT} in ${process.env.NODE_ENV || 'development'} mode`);
    console.log(`🌐 Health API exposed at http://localhost:${PORT}/api/health/database`);
    console.log(`🌐 Server Health exposed at http://localhost:${PORT}/api/health/server`);
    console.log(`🧪 Test DB CRUD API exposed at http://localhost:${PORT}/api/health/test-db\n`);
  });
};

startServer();
