const mongoose = require('mongoose');

let isConnectedToMongo = false;

const connectDB = async () => {
  try {
    const mongoUri = process.env.MONGO_URI || 'mongodb://localhost:27017/loan_predictor';
    const conn = await mongoose.connect(mongoUri, {
      serverSelectionTimeoutMS: 2500,
    });
    isConnectedToMongo = true;
    console.log(`✅ MongoDB Atlas/Local Connected: ${conn.connection.host}`);
  } catch (err) {
    isConnectedToMongo = false;
    console.log(`Notice: Mongo Connection (${err.message}). Using resilient in-memory fallback data layer.`);
  }
};

const getMongoStatus = () => isConnectedToMongo;

module.exports = { connectDB, getMongoStatus };
