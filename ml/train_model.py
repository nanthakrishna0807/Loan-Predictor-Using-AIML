import os
import sys
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml.feature_engineering import engineer_features
from ml.preprocessing import preprocess_data, FEATURE_COLUMNS
from ml.evaluate import evaluate_model_performance

DATASET_PATH = os.path.join(os.path.dirname(__file__), "dataset.csv")
if not os.path.exists(DATASET_PATH):
    DATASET_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dataset.csv")

def safe_print(text: str):
    try:
        print(text)
    except UnicodeEncodeError:
        clean_text = text.encode('ascii', 'ignore').decode('ascii')
        print(clean_text)

def train_and_evaluate_models():
    safe_print(f"Loading dataset from {DATASET_PATH}...")
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"Dataset file {DATASET_PATH} not found!")

    df = pd.read_csv(DATASET_PATH)
    safe_print(f"Dataset Loaded: {df.shape[0]} rows, {df.shape[1]} columns.")

    # Target column
    target_col = "LoanStatus" if "LoanStatus" in df.columns else ("Loan_Status" if "Loan_Status" in df.columns else "Approved")
    if target_col not in df.columns:
        df["LoanStatus"] = np.where((df.get("CIBILScore", 650) >= 650) & (df.get("PreviousLoanDefaults", 0) == 0), 1, 0)
        target_col = "LoanStatus"
    else:
        df[target_col] = df[target_col].astype(str).map(lambda x: 1 if x.strip() in ['1', 'Y', 'Approved', 'True', '1.0'] else 0)

    y = df[target_col].values

    # Feature Engineering
    df_engineered = engineer_features(df)

    # Preprocessing & Scaling
    X_scaled, df_features, encoders, scaler = preprocess_data(df_engineered, fit_scalers=True)

    # Train / Test Split
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.20, random_state=42, stratify=y)

    safe_print(f"Train samples: {len(X_train)} | Test samples: {len(X_test)}")

    # Candidate Models
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Decision Tree": DecisionTreeClassifier(max_depth=6, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
    }

    best_name = None
    best_model = None
    best_accuracy = 0.0
    evaluation_reports = {}

    safe_print("\n==================================================")
    safe_print("Model Training & Comparison Results")
    safe_print("==================================================")

    for name, model in models.items():
        model.fit(X_train, y_train)
        cv_scores = cross_val_score(model, X_train, y_train, cv=5)
        report = evaluate_model_performance(model, X_test, y_test, model_name=name)
        report["cv_mean_accuracy"] = round(float(np.mean(cv_scores)), 4)
        
        evaluation_reports[name] = report
        safe_print(f"{name:20s} | Test Acc: {report['accuracy']*100:.2f}% | Precision: {report['precision']:.4f} | Recall: {report['recall']:.4f} | F1: {report['f1_score']:.4f} | ROC AUC: {report['roc_auc']:.4f}")

        if report["accuracy"] > best_accuracy:
            best_accuracy = report["accuracy"]
            best_name = name
            best_model = model

    safe_print("==================================================")
    safe_print(f"Best Selected Model: {best_name} ({best_accuracy*100:.2f}% Accuracy)")
    safe_print("==================================================\n")

    # Save artifacts
    artifacts = {
        "model": best_model,
        "scaler": scaler,
        "encoders": encoders,
        "feature_cols": FEATURE_COLUMNS,
        "best_model_name": best_name,
        "accuracy": round(best_accuracy * 100, 2),
        "evaluation_reports": evaluation_reports
    }

    ml_dir = os.path.dirname(__file__)
    model_pkl_path = os.path.join(ml_dir, "model.pkl")
    scaler_pkl_path = os.path.join(ml_dir, "scaler.pkl")
    meta_json_path = os.path.join(ml_dir, "model_meta.json")

    joblib.dump(artifacts, model_pkl_path)
    joblib.dump(scaler, scaler_pkl_path)

    root_dir = os.path.dirname(os.path.dirname(__file__))
    joblib.dump(artifacts, os.path.join(root_dir, "model.pkl"))
    joblib.dump(scaler, os.path.join(root_dir, "scaler.pkl"))

    meta_data = {
        "best_model": best_name,
        "best_accuracy": round(best_accuracy * 100, 2),
        "total_samples": len(df),
        "test_samples": len(X_test),
        "comparison": evaluation_reports,
        "feature_columns": FEATURE_COLUMNS
    }
    with open(meta_json_path, "w") as f:
        json.dump(meta_data, f, indent=2)

    safe_print(f"Saved model.pkl to {model_pkl_path}")
    safe_print(f"Saved scaler.pkl to {scaler_pkl_path}")
    safe_print(f"Saved model_meta.json to {meta_json_path}\n")

    return artifacts

if __name__ == "__main__":
    train_and_evaluate_models()
