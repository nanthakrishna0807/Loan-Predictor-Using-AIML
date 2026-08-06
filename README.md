# AI Loan Predictor using Machine Learning (Python Stack)

An AI-powered Loan Prediction and Financial Credit Assessment System built entirely in Python using **FastAPI**, **Streamlit**, **Scikit-learn**, and **MongoDB Atlas**.

---

## 🌟 Architecture & Features

- **Frontend**: Interactive Streamlit web interface with custom banking CSS theme, Plotly charts, CIBIL scoring widget, user profile management, prediction history audit logs, and admin analytics dashboard.
- **Backend**: Async FastAPI REST API server with JWT authentication, Pydantic v2 validation, Passlib bcrypt password hashing, and CORS middleware.
- **Machine Learning**: Gradient Boosting ensemble model trained on financial indicators, calculating approval probability %, credit risk levels, DTI ratios, interest rates, recommended maximum loan amounts, and personalized financial improvement recommendations.
- **Database**: Async Motor client for MongoDB Atlas cloud database persistence with fallback local execution.

---

## 📁 Directory Structure

```
loan-predictor/
│
├── app/
│   ├── api/
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── predict.py
│   │   ├── admin.py
│   │   └── health.py
│   ├── auth/
│   │   ├── jwt.py
│   │   └── security.py
│   ├── database/
│   │   └── connection.py
│   ├── models/
│   │   ├── user.py
│   │   └── prediction.py
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── prediction.py
│   │   └── health.py
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   └── prediction_service.py
│   ├── ml/
│   │   ├── model.pkl
│   │   └── predictor.py
│   ├── utils/
│   │   ├── logger.py
│   │   └── cibil_calculator.py
│   ├── config.py
│   └── main.py
│
├── frontend/
│   ├── Home.py
│   ├── Login.py
│   ├── Register.py
│   ├── Dashboard.py
│   ├── LoanPrediction.py
│   ├── PredictionHistory.py
│   ├── Profile.py
│   ├── AdminDashboard.py
│   ├── components/
│   │   ├── theme.py
│   │   ├── cards.py
│   │   ├── charts.py
│   │   └── cibil_widget.py
│   └── assets/
│
├── uploads/
├── logs/
├── requirements.txt
├── .env.example
├── README.md
└── run.py
```

---

## 🚀 Quick Start & Running the Project

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment (Optional)

Copy `.env.example` to `.env` and set your MongoDB Atlas URI:

```bash
cp .env.example .env
```

### 3. Launch Both Backend & Streamlit App

Run the unified runner script:

```bash
python run.py
```

Or launch services separately:

**FastAPI Backend:**
```bash
python -m uvicorn app.main:app --port 5000 --reload
```

**Streamlit Frontend:**
```bash
streamlit run frontend/Home.py
```

- **Frontend App**: `http://localhost:8501`
- **FastAPI Interactive Docs**: `http://localhost:5000/docs`
