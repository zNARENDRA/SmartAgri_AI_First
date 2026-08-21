"""
SmartAgri AI - Crop Recommendation Model Training
Trains and compares multiple ML classifiers:
- Random Forest Classifier
- Gradient Boosting Classifier
- Decision Tree Classifier
- Logistic Regression
Exports the best model, feature importance, and validation metrics (Accuracy, Precision, Recall, F1, Confusion Matrix).
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "crop_recommendation_cleaned.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODELS_DIR, exist_ok=True)

def train_crop_model():
    print("==================================================")
    print("Training Crop Recommendation Models")
    print("==================================================")
    
    from app.core.config import SQLITE_DB_PATH
    
    if os.path.exists(SQLITE_DB_PATH):
        try:
            from app.db import query_as_dataframe
            df = query_as_dataframe("SELECT N, P, K, temperature, humidity, ph, rainfall, label FROM crop_recommendations")
        except Exception as e:
            print(f"[!] Warning loading crop recommendations from SQLite: {e}")
            df = pd.DataFrame()
    else:
        df = pd.DataFrame()
        
    if df.empty and os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
        
    features = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
    target = "label"
    
    X = df[features]
    y = df[target]
    
    # Train-test split (80-20 stratified)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    models = {
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42),
        "Decision Tree": DecisionTreeClassifier(max_depth=10, random_state=42),
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42)
    }
    
    results = {}
    best_name = None
    best_score = -1.0
    best_model = None
    
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    for name, clf in models.items():
        if name in ["Logistic Regression"]:
            cv_scores = cross_val_score(clf, X_train_scaled, y_train, cv=cv, scoring="accuracy")
            clf.fit(X_train_scaled, y_train)
            y_pred = clf.predict(X_test_scaled)
        else:
            cv_scores = cross_val_score(clf, X_train, y_train, cv=cv, scoring="accuracy")
            clf.fit(X_train, y_train)
            y_pred = clf.predict(X_test)
            
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average="weighted")
        rec = recall_score(y_test, y_pred, average="weighted")
        f1 = f1_score(y_test, y_pred, average="weighted")
        
        results[name] = {
            "cv_mean_accuracy": round(float(np.mean(cv_scores)), 4),
            "cv_std": round(float(np.std(cv_scores)), 4),
            "test_accuracy": round(float(acc), 4),
            "precision_weighted": round(float(prec), 4),
            "recall_weighted": round(float(rec), 4),
            "f1_weighted": round(float(f1), 4)
        }
        
        print(f"[{name}] Test Accuracy: {acc:.4f} | F1: {f1:.4f} | 5-Fold CV: {np.mean(cv_scores):.4f}")
        
        if acc > best_score:
            best_score = acc
            best_name = name
            best_model = clf

    # Extract feature importance from best tree model
    rf = models["Random Forest"]
    importances = rf.feature_importances_
    feat_importance_dict = {
        feat: round(float(imp), 4) for feat, imp in zip(features, importances)
    }
    
    # Generate confusion matrix on test set
    y_pred_best = rf.predict(X_test)
    classes = sorted(list(y.unique()))
    cm = confusion_matrix(y_test, y_pred_best, labels=classes)
    
    metrics_export = {
        "algorithm_comparison": results,
        "selected_model": best_name,
        "selected_model_accuracy": round(float(best_score), 4),
        "feature_importances": feat_importance_dict,
        "features": features,
        "classes": classes,
        "confusion_matrix": cm.tolist()
    }
    
    # Save best model pipeline
    model_artifact = {
        "model": rf,
        "scaler": scaler,
        "features": features,
        "classes": classes,
        "metrics": metrics_export
    }
    
    model_path = os.path.join(MODELS_DIR, "crop_recommendation_model.joblib")
    metrics_path = os.path.join(MODELS_DIR, "crop_recommendation_metrics.json")
    
    joblib.dump(model_artifact, model_path)
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics_export, f, indent=2)
        
    print(f"\n--> Best model ({best_name}) successfully exported to {model_path}")
    print(f"--> Evaluation metrics saved to {metrics_path}")

if __name__ == "__main__":
    train_crop_model()
