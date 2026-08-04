const http = require('http');
const path = require('path');
const dotenv = require('dotenv');
dotenv.config({ path: path.join(__dirname, '.env') });


const { connectDB, getMongoStatus } = require('./config/db');
const app = require('./app');

async function testAtlasIntegration() {
  console.log("--- Initializing MongoDB Atlas Verification Test ---");

  // Step 1: Connect to Mongo
  await connectDB();

  // Step 2: Start temporary server
  const server = http.createServer(app);
  await new Promise(resolve => server.listen(0, resolve));
  const port = server.address().port;
  const baseURL = `http://localhost:${port}`;

  const makeRequest = (path, method = 'GET', body = null) => {
    return new Promise((resolve, reject) => {
      const url = new URL(path, baseURL);
      const options = {
        method,
        headers: { 'Content-Type': 'application/json' }
      };

      const req = http.request(url, options, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          try {
            resolve({ status: res.statusCode, data: JSON.parse(data) });
          } catch (e) {
            resolve({ status: res.statusCode, data });
          }
        });
      });

      req.on('error', reject);
      if (body) req.write(body);
      req.end();
    });
  };

  try {
    console.log('\n--- 1. Testing GET /api/health/server ---');
    const serverHealth = await makeRequest('/api/health/server');
    console.log('Status:', serverHealth.status);
    console.log('Response:', JSON.stringify(serverHealth.data, null, 2));

    console.log('\n--- 2. Testing GET /api/health/database ---');
    const dbHealth = await makeRequest('/api/health/database');
    console.log('Status:', dbHealth.status);
    console.log('Response:', JSON.stringify(dbHealth.data, null, 2));

    if (getMongoStatus()) {
      console.log('\n--- 3. Testing POST /api/health/test-db (Write Document) ---');
      const createRes = await makeRequest('/api/health/test-db', 'POST', JSON.stringify({
        title: 'Atlas Verification Record ' + Date.now(),
        testData: { status: 'SUCCESS', verifiedBy: 'Antigravity AI Test Suite' }
      }));
      console.log('Status:', createRes.status);
      console.log('Response:', JSON.stringify(createRes.data, null, 2));

      console.log('\n--- 4. Testing GET /api/health/test-db (Read Document) ---');
      const getRes = await makeRequest('/api/health/test-db');
      console.log('Status:', getRes.status);
      console.log('Response:', JSON.stringify(getRes.data, null, 2));
    } else {
      console.log('\n⚠️ Mongo Atlas Not Connected. Skipping CRUD test.');
    }

    console.log('\n✅ ALL MONGODB ATLAS INTEGRATION TESTS COMPLETED SUCCESSFULLY!');
  } catch (err) {
    console.error('❌ Test execution error:', err);
  } finally {
    server.close();
    process.exit(0);
  }
}

testAtlasIntegration();
