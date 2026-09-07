"""
Model Training and Comparison Script.
Trains Logistic Regression, Random Forest, and SVM models on synthetic cyber telemetry.
Evaluates Accuracy, Precision, Recall, F1-Score, and ROC-AUC, selects the best model,
and saves the artifacts with comprehensive metadata.
"""

import os
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
)
import joblib

from simulation.session_generator import generate_dataset
from detection.feature_engineering import prepare_training_data, FEATURE_COLUMNS, LABEL_MAPPING


def train_and_evaluate_models(data_path: str = "data/attack_sessions.csv", models_dir: str = "models"):
    """
    Train and compare Logistic Regression, Random Forest, and SVM.
    Select and persist the best model.
    """
    os.makedirs(models_dir, exist_ok=True)

    # 1. Check or generate dataset
    if not os.path.exists(data_path):
        print(f"Dataset not found at {data_path}. Generating synthetic dataset...")
        df = generate_dataset(num_samples=6000, output_path=data_path)
    else:
        print(f"Loading existing dataset from {data_path}...")
        df = pd.read_csv(data_path)

    print(f"Dataset loaded: {len(df)} records across {df['attack_label'].nunique()} classes.")

    # 2. Extract features and scale
    X, y, scaler = prepare_training_data(df)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    # 3. Define candidate algorithms
    candidates = {
        "RandomForest": RandomForestClassifier(
            n_estimators=100,
            max_depth=14,
            min_samples_split=4,
            random_state=42,
            n_jobs=-1,
        ),
        "LogisticRegression": LogisticRegression(
            max_iter=1000,
            C=1.0,
            random_state=42,
        ),
        "SVM": SVC(
            kernel="rbf",
            C=1.0,
            probability=True,
            random_state=42,
        ),
    }

    results = {}
    fitted_models = {}

    print("\n" + "=" * 80)
    print("STARTING MODEL TRAINING & BENCHMARKING")
    print("=" * 80)

    for name, model in candidates.items():
        print(f"\nTraining {name}...")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average="weighted", zero_division=0)
        rec = recall_score(y_test, y_pred, average="weighted", zero_division=0)
        f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)

        try:
            auc = roc_auc_score(y_test, y_proba, multi_class="ovr", average="weighted")
        except Exception:
            auc = 0.0

        results[name] = {
            "accuracy": round(float(acc), 4),
            "precision": round(float(prec), 4),
            "recall": round(float(rec), 4),
            "f1_score": round(float(f1), 4),
            "roc_auc": round(float(auc), 4),
        }
        fitted_models[name] = model

        print(
            f"--> {name}: Accuracy={acc:.4f} | Precision={prec:.4f} | Recall={rec:.4f} | F1={f1:.4f} | ROC-AUC={auc:.4f}"
        )

    # 4. Model Selection (Highest F1-score)
    best_model_name = max(results, key=lambda k: results[k]["f1_score"])
    best_model = fitted_models[best_model_name]
    print("\n" + "=" * 80)
    print(f"BEST PERFORMING MODEL: {best_model_name} (F1-Score: {results[best_model_name]['f1_score']})")
    print("=" * 80)

    # 5. Extract Feature Importances if available
    feature_importances = {}
    if hasattr(best_model, "feature_importances_"):
        for col, imp in zip(FEATURE_COLUMNS, best_model.feature_importances_):
            feature_importances[col] = round(float(imp), 4)
    else:
        for col in FEATURE_COLUMNS:
            feature_importances[col] = round(1.0 / len(FEATURE_COLUMNS), 4)

    # Sort feature importances
    feature_importances = dict(
        sorted(feature_importances.items(), key=lambda item: item[1], reverse=True)
    )

    # 6. Save artifacts
    detector_path = os.path.join(models_dir, "detector.joblib")
    scaler_path = os.path.join(models_dir, "scaler.joblib")
    meta_path = os.path.join(models_dir, "model_metadata.json")

    joblib.dump(best_model, detector_path)
    joblib.dump(scaler, scaler_path)

    metadata = {
        "best_model": best_model_name,
        "evaluation_metrics": results,
        "feature_importances": feature_importances,
        "classes": list(LABEL_MAPPING.keys()),
        "test_sample_count": len(y_test),
        "train_sample_count": len(y_train),
    }

    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=4)

    print(f"\nArtifacts successfully persisted:")
    print(f" - Model: {detector_path}")
    print(f" - Scaler: {scaler_path}")
    print(f" - Metadata: {meta_path}")

    return metadata


if __name__ == "__main__":
    train_and_evaluate_models()
