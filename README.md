# AI Loan Predictor – Smart Loan Eligibility Prediction System

An end-to-end modern FinTech web application that predicts loan eligibility (`Approved` or `Rejected`) using Machine Learning algorithms (Random Forest, XGBoost / Gradient Boosting, Decision Trees, Logistic Regression). 

Features dynamic **CIBIL score meter** analytics, credit risk gauge, automated financial tips, PDF report generation, Excel export, and JWT-authenticated User & Admin dashboards.

---

## 🏗️ Architecture & Tech Stack

```
AI Loan Predictor/
├── ml/             # Python Flask ML Microservice (Port 5001)
├── server/         # Express.js Node Backend API (Port 5000)
└── client/         # React.js Vite Glassmorphism Frontend (Port 3000)
```

- **Frontend**: React 18, Vite, Bootstrap 5, Glassmorphic Vanilla CSS, Framer Motion, Chart.js, Lucide Icons, jsPDF, XLSX.
- **Backend**: Node.js, Express.js, JWT Authentication, Bcrypt, Mongoose (MongoDB Atlas / Local MongoDB, with built-in resilient fallback data store).
- **Machine Learning**: Python 3.x, Flask, Pandas, NumPy, Scikit-Learn, Joblib, GradientBoosting/XGBoost, Matplotlib.

---

## ⚡ Quick Start Instructions

### 1. Train ML Model & Start Flask API (Port 5001)
```bash
cd ml
python generate_dataset.py
python train_model.py
python app.py
```

### 2. Start Express Backend (Port 5000)
```bash
cd server
npm install
npm run dev
```

### 3. Start React Frontend (Port 3000)
```bash
cd client
npm install
npm run dev
```

---

## 🎯 Demo User Credentials

- **Applicant User**:
  - **Email**: `demo@loanpredictor.ai`
  - **Password**: `password`
- **System Admin**:
  - **Email**: `admin@loanpredictor.ai`
  - **Password**: `admin123`

---

## 📊 CIBIL Score Logic & Thresholds

| Range | Rating | Status & Rule |
| :--- | :--- | :--- |
| **750 – 900** | **Excellent** | Prime approval eligibility, lowest interest rates (~9.2% APR). |
| **650 – 749** | **Good** | Standard approval eligibility, competitive terms. |
| **550 – 649** | **Fair** | Below threshold (650). Rejection bias unless offset by high liquid savings. |
| **300 – 549** | **Poor** | Automated rejection lean due to high credit risk. |

---

## 🌐 Key API Endpoints

### Authentication (`/api/auth`)
- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/auth/logout`
- `POST /api/auth/forgot-password`
- `POST /api/auth/reset-password`

### Loan Predictions (`/api/loan`)
- `POST /api/loan/predict`
- `GET /api/loan/history`
- `GET /api/loan/:id`
- `DELETE /api/loan/:id`

### Admin Management (`/api/admin`)
- `GET /api/admin/users`
- `GET /api/admin/dashboard`
- `GET /api/admin/analytics`
- `DELETE /api/admin/user/:id`

### Flask ML Microservice (`http://localhost:5001`)
- `POST /predict`
- `GET /model-info`
- `GET /accuracy`
- `POST /retrain`
