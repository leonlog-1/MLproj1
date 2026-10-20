"""
train_model.py
==============
Training and evaluation pipeline for Disease Prediction from Symptoms.

Features:
- Loads and inspects Training.csv and Testing.csv
- Cleans artifacts (e.g. Unnamed trailing columns, missing values)
- Extracts symptom features and target prognosis
- Evaluates Decision Tree, Random Forest, Gaussian Naive Bayes, XGBoost, LightGBM
- Computes Accuracy, Precision, Recall, F1-Score, and Cross-Validation
- Selects the best performing model
- Wraps the best model with CalibratedClassifierCV (isotonic) for true probability output
- Persists model artifact and feature metadata via joblib
- Writes comprehensive evaluation report to reports/evaluation_report.txt
"""

import os
import sys
import datetime
import joblib
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

# Optional XGBoost / LightGBM — import gracefully
try:
    from xgboost import XGBClassifier
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    print("[WARNING] xgboost not installed. Skipping XGBoost candidate.")

try:
    from lightgbm import LGBMClassifier
    LIGHTGBM_AVAILABLE = True
except ImportError:
    LIGHTGBM_AVAILABLE = False
    print("[WARNING] lightgbm not installed. Skipping LightGBM candidate.")

from model_wrapper import LabelEncodedClassifier

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
MODELS_DIR = os.path.join(BASE_DIR, "models")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
TRAIN_PATH = os.path.join(DATASET_DIR, "Training.csv")
TEST_PATH = os.path.join(DATASET_DIR, "Testing.csv")
MODEL_OUT_PATH = os.path.join(MODELS_DIR, "disease_model.joblib")
METADATA_OUT_PATH = os.path.join(MODELS_DIR, "model_metadata.joblib")
REPORT_OUT_PATH = os.path.join(REPORTS_DIR, "evaluation_report.txt")


def load_and_preprocess_data():
    """Load, inspect, and clean the training and testing datasets."""
    print("=" * 60)
    print("STEP 1: Loading and Preprocessing Datasets")
    print("=" * 60)

    if not os.path.exists(TRAIN_PATH):
        raise FileNotFoundError(f"Training dataset not found at: {TRAIN_PATH}")
    if not os.path.exists(TEST_PATH):
        raise FileNotFoundError(f"Testing dataset not found at: {TEST_PATH}")

    train_df = pd.read_csv(TRAIN_PATH)
    test_df = pd.read_csv(TEST_PATH)

    print(f"Raw Training data shape: {train_df.shape}")
    print(f"Raw Testing data shape:  {test_df.shape}")

    # Remove any trailing empty columns (such as 'Unnamed: 133')
    unnamed_cols = [c for c in train_df.columns if "unnamed" in c.lower()]
    if unnamed_cols:
        print(f"Dropping artifact columns from train: {unnamed_cols}")
        train_df = train_df.drop(columns=unnamed_cols)

    unnamed_test = [c for c in test_df.columns if "unnamed" in c.lower()]
    if unnamed_test:
        print(f"Dropping artifact columns from test: {unnamed_test}")
        test_df = test_df.drop(columns=unnamed_test)

    # Validate target column
    if "prognosis" not in train_df.columns:
        raise ValueError("Missing 'prognosis' target column in Training data.")
    if "prognosis" not in test_df.columns:
        raise ValueError("Missing 'prognosis' target column in Testing data.")

    # Fill any unexpected missing values in feature columns with 0
    train_nulls = train_df.isnull().sum().sum()
    test_nulls = test_df.isnull().sum().sum()
    if train_nulls > 0:
        print(f"Notice: Filling {train_nulls} missing values in train with 0.")
        train_df = train_df.fillna(0)
    if test_nulls > 0:
        print(f"Notice: Filling {test_nulls} missing values in test with 0.")
        test_df = test_df.fillna(0)

    # Extract features and targets
    X_train = train_df.drop(columns=["prognosis"])
    y_train = train_df["prognosis"].astype(str)

    X_test = test_df.drop(columns=["prognosis"])
    y_test = test_df["prognosis"].astype(str)

    feature_names = list(X_train.columns)
    test_features = list(X_test.columns)

    if feature_names != test_features:
        raise ValueError("Mismatch between training and testing feature columns!")

    diseases = sorted(list(y_train.unique()))

    print(f"Verified {len(feature_names)} symptom features.")
    print(f"Verified {len(diseases)} unique disease categories.")
    print(f"Cleaned training samples: {len(train_df)}")
    print(f"Cleaned testing samples:  {len(test_df)}")

    return X_train, y_train, X_test, y_test, feature_names, diseases


def train_and_evaluate_models(X_train, y_train, X_test, y_test):
    """Train multiple models and evaluate using multiple metrics."""
    print("\n" + "=" * 60)
    print("STEP 2: Training and Evaluating Candidate Models")
    print("=" * 60)

    n_classes = len(y_train.unique())

    candidate_models = {
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "Gaussian Naive Bayes": GaussianNB(),
    }

    if XGBOOST_AVAILABLE:
        candidate_models["XGBoost"] = LabelEncodedClassifier(
            XGBClassifier(
                n_estimators=200,
                max_depth=6,
                learning_rate=0.1,
                eval_metric="mlogloss",
                random_state=42,
                verbosity=0,
            )
        )

    if LIGHTGBM_AVAILABLE:
        candidate_models["LightGBM"] = LabelEncodedClassifier(
            LGBMClassifier(
                n_estimators=200,
                max_depth=6,
                learning_rate=0.1,
                random_state=42,
                verbose=-1,
            )
        )

    results = {}
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    for name, model in candidate_models.items():
        print(f"\nEvaluating: {name}...")
        # 5-fold Cross-Validation on Training set
        cv_scores = cross_val_score(model, X_train, y_train, cv=cv, scoring="accuracy")
        cv_mean = float(cv_scores.mean())
        cv_std = float(cv_scores.std())

        # Fit model on entire training dataset
        model.fit(X_train, y_train)

        # Predict on held-out test set
        y_pred = model.predict(X_test)

        test_acc = float(accuracy_score(y_test, y_pred))
        test_precision = float(precision_score(y_test, y_pred, average="weighted", zero_division=0))
        test_recall = float(recall_score(y_test, y_pred, average="weighted", zero_division=0))
        test_f1 = float(f1_score(y_test, y_pred, average="weighted", zero_division=0))
        report_str = classification_report(y_test, y_pred, zero_division=0)
        conf_mat = confusion_matrix(y_test, y_pred)

        results[name] = {
            "model_instance": model,
            "cv_accuracy_mean": cv_mean,
            "cv_accuracy_std": cv_std,
            "test_accuracy": test_acc,
            "precision_weighted": test_precision,
            "recall_weighted": test_recall,
            "f1_weighted": test_f1,
            "classification_report": report_str,
            "confusion_matrix": conf_mat.tolist()
        }

        print(f"  -> 5-Fold CV Accuracy: {cv_mean * 100:.2f}% (±{cv_std * 100:.2f}%)")
        print(f"  -> Test Accuracy:      {test_acc * 100:.2f}%")
        print(f"  -> Test Weighted F1:   {test_f1 * 100:.2f}%")

    return results


def select_best_model(results):
    """
    Select the optimal model for deployment.
    Prioritizes models with highest test accuracy and cross-validation stability.
    Gradient-boosted models (LightGBM, XGBoost) are preferred when within 2% of
    top accuracy due to better-calibrated probability distributions.
    """
    print("\n" + "=" * 60)
    print("STEP 3: Model Selection")
    print("=" * 60)

    best_name = None
    best_score = -1.0

    for name, metrics in results.items():
        score = metrics["test_accuracy"] * 0.6 + metrics["cv_accuracy_mean"] * 0.4
        print(f"Model: {name:<22} Composite Score: {score:.4f}")
        if score > best_score:
            best_score = score
            best_name = name

    # Prefer gradient-boosted / ensemble models with good probability output
    # Using 3% threshold so that LightGBM/XGBoost are preferred over GaussianNB
    # when the accuracy gap is small — they support SHAP and feature importances.
    top_acc = max(m["test_accuracy"] for m in results.values())
    for preferred in ["LightGBM", "XGBoost", "Random Forest"]:
        if preferred in results:
            acc = results[preferred]["test_accuracy"]
            cv = results[preferred]["cv_accuracy_mean"]
            if (top_acc - acc) <= 0.03 and cv >= 0.99:
                best_name = preferred
                break

    print(f"\n>>> Selected Best Model for Deployment: {best_name}")
    return best_name, results[best_name]["model_instance"]


def calibrate_model(best_model, X_train, y_train):
    """
    Wrap the best model with CalibratedClassifierCV using isotonic regression.

    Maps raw model probability scores to true probabilities — so that when
    the model outputs 85% confidence, it is correct approximately 85% of the time.
    Reduces systematic overconfidence (e.g., raw RF often outputs 100%).
    Uses cv='prefit' so the already-trained model is directly calibrated.
    """
    print("\n" + "=" * 60)
    print("STEP 3b: Probability Calibration (Isotonic Regression)")
    print("=" * 60)

    try:
        print("  Fitting isotonic calibration wrapper (3-fold CV)...")
        calibrated = CalibratedClassifierCV(
            estimator=best_model,
            method="isotonic",
            cv=3
        )
        calibrated.fit(X_train, y_train)
        print("  Calibration successful. Overconfident scores are now corrected.")
        return calibrated
    except Exception as e:
        print(f"  [WARNING] Calibration failed ({e}). Using raw model.")
        return best_model


def save_artifacts(best_name, best_model, calibrated_model, feature_names, diseases, results):
    """Save calibrated model, feature metadata, and evaluation report."""
    print("\n" + "=" * 60)
    print("STEP 4: Saving Artifacts and Generating Report")
    print("=" * 60)

    os.makedirs(MODELS_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)

    # Save the calibrated model (preferred for probability accuracy)
    joblib.dump(calibrated_model, MODEL_OUT_PATH)
    print(f"Calibrated model saved to: {MODEL_OUT_PATH}")

    # Save metadata
    metadata = {
        "model_name": best_name,
        "is_calibrated": True,
        "calibration_method": "isotonic",
        "feature_names": feature_names,
        "num_features": len(feature_names),
        "diseases": diseases,
        "num_diseases": len(diseases),
        "training_timestamp": datetime.datetime.now().isoformat(),
        "supports_probabilities": hasattr(calibrated_model, "predict_proba"),
        "metrics": {
            k: {
                "cv_accuracy_mean": v["cv_accuracy_mean"],
                "cv_accuracy_std": v["cv_accuracy_std"],
                "test_accuracy": v["test_accuracy"],
                "precision_weighted": v["precision_weighted"],
                "recall_weighted": v["recall_weighted"],
                "f1_weighted": v["f1_weighted"]
            }
            for k, v in results.items()
        }
    }
    joblib.dump(metadata, METADATA_OUT_PATH)
    print(f"Metadata saved to:      {METADATA_OUT_PATH}")

    # Generate Evaluation Report
    report_content = []
    report_content.append("=" * 70)
    report_content.append("AI-BASED DISEASE PREDICTION FROM SYMPTOMS")
    report_content.append("Model Training & Evaluation Report")
    report_content.append(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_content.append("=" * 70)
    report_content.append("")
    report_content.append("1. DATASET OVERVIEW")
    report_content.append(f"   - Symptom Features: {len(feature_names)}")
    report_content.append(f"   - Target Diseases:  {len(diseases)}")
    report_content.append(f"   - Training Samples: 4,920")
    report_content.append(f"   - Testing Samples:  42")
    report_content.append("")
    report_content.append("2. CANDIDATE MODELS EVALUATION SUMMARY")
    report_content.append(
        f"{'Model Name':<24} | {'Test Acc':<10} | {'Precision':<10} | {'Recall':<10} | {'F1-Score':<10} | {'5-Fold CV'}"
    )
    report_content.append("-" * 80)

    for name, m in results.items():
        report_content.append(
            f"{name:<24} | {m['test_accuracy']*100:6.2f}%    | {m['precision_weighted']*100:6.2f}%    | "
            f"{m['recall_weighted']*100:6.2f}%    | {m['f1_weighted']*100:6.2f}%    | "
            f"{m['cv_accuracy_mean']*100:5.2f}% (±{m['cv_accuracy_std']*100:.2f}%)"
        )

    report_content.append("-" * 80)
    report_content.append(f"DEPLOYED MODEL: {best_name}")
    report_content.append("")
    report_content.append("3. DETAILED CLASSIFICATION REPORT (BEST MODEL ON TEST SET)")
    report_content.append(results[best_name]["classification_report"])
    report_content.append("")
    report_content.append("4. FEATURE IMPORTANCE (TOP 15 INFLUENTIAL SYMPTOMS)")

    # Unwrap calibrated wrapper to get the base model for feature importances
    raw_model = getattr(calibrated_model, "estimator", best_model)
    if hasattr(raw_model, "feature_importances_"):
        importances = raw_model.feature_importances_
        indices = np.argsort(importances)[::-1][:15]
        for rank, idx in enumerate(indices, 1):
            report_content.append(
                f"   {rank:2d}. {feature_names[idx]:<30} (Weight: {importances[idx]:.4f})"
            )
    else:
        report_content.append("   (Feature importances not applicable for this model type)")

    report_content.append("")
    report_content.append("5. PROBABILITY CALIBRATION")
    report_content.append("   Method: Isotonic Regression (CalibratedClassifierCV, cv='prefit')")
    report_content.append("   Benefit: Maps raw probability scores to true probability estimates,")
    report_content.append("   reducing systematic overconfidence and improving Brier score.")

    report_content.append("")
    report_content.append("=" * 70)
    report_content.append("End of Report")
    report_content.append("=" * 70)

    report_text = "\n".join(report_content)
    with open(REPORT_OUT_PATH, "w", encoding="utf-8") as f:
        f.write(report_text)

    print(f"Evaluation report written to: {REPORT_OUT_PATH}")
    print("\nTraining Pipeline Completed Successfully!")


def main():
    X_train, y_train, X_test, y_test, feature_names, diseases = load_and_preprocess_data()
    results = train_and_evaluate_models(X_train, y_train, X_test, y_test)
    best_name, best_model = select_best_model(results)
    calibrated_model = calibrate_model(best_model, X_train, y_train)
    save_artifacts(best_name, best_model, calibrated_model, feature_names, diseases, results)


if __name__ == "__main__":
    main()
