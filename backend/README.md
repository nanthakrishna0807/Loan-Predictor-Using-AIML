# AI Loan Predictor - Production Python FastAPI Backend

Enterprise Python 3.12+ FastAPI backend for the **AI Loan Predictor** application. Built using Machine Learning (Scikit-learn / Joblib), Motor (Async MongoDB Atlas Driver), JWT Authentication, Pydantic data validation, and CIBIL financial scoring engine.

## 🚀 Features

- **FastAPI Core**: Async, high-performance Python 3.12 microservice architecture.
- **MongoDB Atlas Integration**: Motor async driver with startup connection checks & continuous monitoring.
- **Machine Learning Integration**: Auto-loads Scikit-learn `model.pkl` artifacts for real-time loan approval prediction & risk assessment.
- **CIBIL Score Calculator**: Automatic financial rating engine (Excellent, Good, Average, Poor).
- **JWT Security**: Password hashing with `bcrypt` and secure OAuth2/JWT tokens.
- **Robust Validation**: Pydantic schemas validating age (>=18), income (>0), loan amount (>0), and CIBIL score (300-900).
- **Deployment Compatibility**: Tested for local development, Docker, Render, and Railway.

---

## 🛠 Directory Structure

```text
backend/
├── app/
│   ├── main.py                 # FastAPI app entry point & lifespan events
│   ├── config/                 # Pydantic environment configuration
│   ├── database/               # Async Motor MongoDB Atlas connection
│   ├── models/                 # Database Document models
│   ├── schemas/                # Request validation Pydantic schemas
│   ├── routes/                 # Auth, User, Prediction, Health, Admin routers
│   ├── services/               # Core business services
│   ├── auth/                   # JWT & Password security helpers
│   ├── middleware/             # Database connection state monitoring
│   ├── utils/                  # Logger & CIBIL score calculator
│   └── ml/                     # ML Model artifacts & Prediction engine
├── uploads/                    # File uploads directory
├── logs/                       # Application logs directory
├── requirements.txt            # Python dependencies
├── .env.example                # Configuration template
└── README.md                   # Backend documentation
```

---

## 💻 Local Setup Instructions

1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Environment Variables**:
   Copy `.env.example` to `.env` and fill in your MongoDB Atlas connection string:
   ```env
   PORT=5000
   MONGO_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/loanpredictor
   JWT_SECRET=super_secret_key
   ```

5. **Start the FastAPI Development Server**:
   ```bash
   uvicorn app.main:app --port 5000 --reload
   ```

6. **Interactive API Documentation**:
   - Swagger UI: `http://localhost:5000/docs`
   - ReDoc: `http://localhost:5000/redoc`

---

## ☁️ Deployment Instructions

### Render Deployment
1. Connect your GitHub repository to Render.
2. Select **Web Service**.
3. Set **Runtime** to `Python 3`.
4. Set **Build Command**: `pip install -r backend/requirements.txt`
5. Set **Start Command**: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
6. Add Environment Variables (`MONGO_URI`, `JWT_SECRET`, etc.).

### Railway Deployment
1. Create a new project on Railway from GitHub.
2. Add environment variables.
3. Railway automatically detects `requirements.txt` and runs `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.

### Docker Deployment
```bash
docker build -t ai-loan-predictor-backend .
docker run -p 5000:5000 --env-file .env ai-loan-predictor-backend
```
