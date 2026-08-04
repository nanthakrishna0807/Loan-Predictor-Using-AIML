const path = require('path');
const dotenv = require('dotenv');

dotenv.config({ path: path.join(__dirname, '../.env') });

const mongoose = require('mongoose');

let isConnectedToMongo = false;

let dbDetails = {
  host: 'N/A',
  databaseName: 'N/A',
  connectionState: 0,
  connectionStateText: 'Disconnected'
};

const stateMap = {
  0: 'Disconnected',
  1: 'Connected',
  2: 'Connecting',
  3: 'Disconnecting'
};

const validateEnv = () => {
  const mongoUri = process.env.MONGO_URI;
  if (!mongoUri || mongoUri.trim() === '') {
    console.error(`\n==================================================`);
    console.error(`❌ CRITICAL CONFIGURATION ERROR: MONGO_URI is missing!`);
    console.error(`Please specify MONGO_URI in your server/.env file.`);
    console.error(`==================================================\n`);
    process.exit(1);
  }
  return mongoUri.trim();
};

const connectDB = async () => {
  const mongoUri = validateEnv();

  try {
    const conn = await mongoose.connect(mongoUri, {
      serverSelectionTimeoutMS: 5000,
    });

    isConnectedToMongo = true;
    dbDetails = {
      host: conn.connection.host,
      databaseName: conn.connection.name,
      connectionState: conn.connection.readyState,
      connectionStateText: stateMap[conn.connection.readyState] || 'Connected'
    };

    console.log(`\n==================================================`);
    console.log(`✅ MongoDB Atlas Connected Successfully!`);
    console.log(`📌 Host: ${dbDetails.host}`);
    console.log(`📌 Database Name: ${dbDetails.databaseName}`);
    console.log(`📌 Connection State: ${dbDetails.connectionStateText} (Code ${dbDetails.connectionState})`);
    console.log(`==================================================\n`);

    return conn;
  } catch (err) {
    isConnectedToMongo = false;
    dbDetails.connectionState = 0;
    dbDetails.connectionStateText = 'Disconnected';

    console.error(`\n==================================================`);
    console.error(`❌ MongoDB Connection Failed!`);
    console.error(`Error: ${err.message}`);
    console.error(`\n🔍 Troubleshooting Checklist:`);
    console.error(`1. Invalid connection string format or typo in MONGO_URI.`);
    console.error(`2. Wrong database username or password in credentials.`);
    console.error(`3. IP address not whitelisted in MongoDB Atlas Network Access (Ensure 0.0.0.0/0 is added for testing).`);
    console.error(`4. MongoDB Atlas Cluster is paused or unavailable.`);
    console.error(`5. Missing or incorrect MONGO_URI environment variable.`);
    console.error(`==================================================\n`);

    // In strict MongoDB mode, exit process if database connection fails
    if (process.env.STRICT_DB === 'true') {
      process.exit(1);
    }
  }
};

const getMongoStatus = () => isConnectedToMongo;
const getDbDetails = () => ({
  ...dbDetails,
  connectionState: mongoose.connection.readyState,
  connectionStateText: stateMap[mongoose.connection.readyState] || (isConnectedToMongo ? 'Connected' : 'Disconnected'),
  databaseName: mongoose.connection.name || dbDetails.databaseName,
  host: mongoose.connection.host || dbDetails.host
});

module.exports = { connectDB, getMongoStatus, getDbDetails };
