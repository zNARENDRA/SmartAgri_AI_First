"""
SmartAgri AI - Crop Yield Prediction Model Training
Trains and compares regression algorithms:
- Random Forest Regressor
- Gradient Boosting Regressor
- Ridge Regression
Evaluates MAE, RMSE, R² Score, and exports the best regression pipeline.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score

import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "crop_yield_cleaned.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODELS_DIR, exist_ok=True)

def train_yield_model():
    print("==================================================")
    print("Training Crop Yield Prediction Models")
    print("==================================================")
    
    from app.core.config import SQLITE_DB_PATH
    
    if os.path.exists(SQLITE_DB_PATH):
        try:
            from app.db import query_as_dataframe
            df = query_as_dataframe("SELECT crop as Crop, season as Season, state as State, area as Area, annual_rainfall as Annual_Rainfall, fertilizer as Fertilizer, pesticide as Pesticide, yield as Yield FROM crop_yields")
        except Exception as e:
            print(f"[!] Warning loading crop yields from SQLite: {e}")
            df = pd.DataFrame()
    else:
        df = pd.DataFrame()
        
    if df.empty and os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
        
    categorical_features = ["Crop", "Season", "State"]
    numerical_features = ["Area", "Annual_Rainfall", "Fertilizer", "Pesticide"]
    target = "Yield"
    
    X = df[categorical_features + numerical_features]
    y = df[target]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numerical_features),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_features)
        ]
    )
    
    models = {
        "Random Forest Regressor": RandomForestRegressor(n_estimators=100, max_depth=14, random_state=42, n_jobs=-1),
        "Gradient Boosting Regressor": GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=6, random_state=42),
        "Ridge Regression": Ridge(alpha=1.0, random_state=42)
    }
    
    results = {}
    best_name = None
    best_r2 = -float("inf")
    best_pipeline = None
    
    for name, reg in models.items():
        pipe = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("regressor", reg)
        ])
        
        pipe.fit(X_train, y_train)
        y_pred = pipe.predict(X_test)
        
        mae = mean_absolute_error(y_test, y_pred)
        rmse = root_mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        results[name] = {
            "MAE": round(float(mae), 4),
            "RMSE": round(float(rmse), 4),
            "R2_Score": round(float(r2), 4)
        }
        
        print(f"[{name}] R²: {r2:.4f} | MAE: {mae:.4f} | RMSE: {rmse:.4f}")
        
        if r2 > best_r2:
            best_r2 = r2
            best_name = name
            best_pipeline = pipe

    # Extract feature importances if tree model
    regressor = best_pipeline.named_steps["regressor"]
    if hasattr(regressor, "feature_importances_"):
        cat_encoder = best_pipeline.named_steps["preprocessor"].named_transformers_["cat"]
        encoded_cat_names = list(cat_encoder.get_feature_names_out(categorical_features))
        all_feature_names = numerical_features + encoded_cat_names
        importances = regressor.feature_importances_
        
        # Aggregate importance by main category
        cat_agg_importance = {"Area": 0.0, "Annual_Rainfall": 0.0, "Fertilizer": 0.0, "Pesticide": 0.0, "Crop": 0.0, "Season": 0.0, "State": 0.0}
        for feat_name, imp in zip(all_feature_names, importances):
            for base_feat in cat_agg_importance.keys():
                if feat_name.startswith(base_feat):
                    cat_agg_importance[base_feat] += imp
                    break
                    
        for k in cat_agg_importance:
            cat_agg_importance[k] = round(float(cat_agg_importance[k]), 4)
    else:
        cat_agg_importance = {}

    metrics_export = {
        "algorithm_comparison": results,
        "selected_model": best_name,
        "selected_model_r2": round(float(best_r2), 4),
        "selected_model_mae": results[best_name]["MAE"],
        "selected_model_rmse": results[best_name]["RMSE"],
        "feature_importances": cat_agg_importance,
        "crops": sorted(list(df["Crop"].unique())),
        "states": sorted(list(df["State"].unique())),
        "seasons": sorted(list(df["Season"].unique()))
    }
    
    model_path = os.path.join(MODELS_DIR, "crop_yield_model.joblib")
    metrics_path = os.path.join(MODELS_DIR, "crop_yield_metrics.json")
    
    joblib.dump(best_pipeline, model_path)
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics_export, f, indent=2)
        
    print(f"\n--> Best model ({best_name}) successfully exported to {model_path}")
    print(f"--> Evaluation metrics saved to {metrics_path}")

if __name__ == "__main__":
    train_yield_model()
