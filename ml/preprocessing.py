import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder

FEATURE_COLUMNS = [
    "Age",
    "Gender",
    "MaritalStatus",
    "Education",
    "EmploymentType",
    "SelfEmployed",
    "AnnualIncome",
    "MonthlyIncome",
    "ExistingEMI",
    "CreditCardUsage",
    "NumberExistingLoans",
    "LoanAmount",
    "LoanPurpose",
    "LoanTenure",
    "CIBILScore",
    "BankBalance",
    "PropertyOwnership",
    "Dependents",
    "DebtToIncomeRatio",
    "CreditUtilizationRatio",
    "SavingsAmount",
    "PreviousLoanDefaults"
]

def preprocess_data(df: pd.DataFrame, fit_scalers: bool = False, encoders: dict = None, scaler: StandardScaler = None):
    """
    Cleans data, handles missing values, encodes categorical variables, and scales numerical features.
    """
    df = df.copy()

    # Fill missing values safely according to data type
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].median())
        else:
            mode_val = df[col].mode()[0] if not df[col].mode().empty else "Unknown"
            df[col] = df[col].fillna(mode_val)

    # Categorical Columns to Encode
    categorical_cols = ["Gender", "MaritalStatus", "Education", "EmploymentType", "SelfEmployed", "LoanPurpose", "PropertyOwnership"]
    
    if fit_scalers:
        encoders = {}
        for col in categorical_cols:
            if col in df.columns:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))
                encoders[col] = list(le.classes_)
    else:
        if encoders:
            for col in categorical_cols:
                if col in df.columns and col in encoders:
                    classes = encoders[col]
                    df[col] = df[col].astype(str).map(lambda x: classes.index(x) if x in classes else 0)

    # Ensure all feature columns exist and are numeric
    for col in FEATURE_COLUMNS:
        if col not in df.columns:
            df[col] = 0.0
        else:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)

    df_features = df[FEATURE_COLUMNS]

    if fit_scalers:
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(df_features)
        return X_scaled, df_features, encoders, scaler
    else:
        if scaler:
            X_scaled = scaler.transform(df_features)
            return X_scaled, df_features
        return df_features.values, df_features
