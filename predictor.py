"""
predictor.py
============
Independent Prediction Engine for Disease Prediction from Symptoms.

Responsibilities:
- Loads the persisted ML model and metadata artifacts once at initialization.
- Validates input symptoms against the supported symptom vocabulary.
- Builds the exact binary feature vector DataFrame expected by the model.
- Computes the predicted disease and calibrated confidence score.
- Exposes clean methods for API and CLI integration without Flask dependencies.
"""

import os
import joblib
import numpy as np
import pandas as pd
import sys
from typing import List, Dict, Any, Optional

import model_wrapper
from model_wrapper import LabelEncodedClassifier
# Ensure __main__ has LabelEncodedClassifier in case model was saved from __main__
if "__main__" in sys.modules:
    setattr(sys.modules["__main__"], "LabelEncodedClassifier", LabelEncodedClassifier)

from disease_info import get_disease_details

# SHAP for per-prediction explainability (optional — graceful fallback)
try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False

DEFAULT_MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "disease_model.joblib")
DEFAULT_METADATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "model_metadata.joblib")



class ModelNotLoadedError(Exception):
    """Raised when the model or metadata files cannot be loaded."""
    pass


class InvalidSymptomError(ValueError):
    """Raised when one or more symptoms provided are invalid or unsupported."""
    def __init__(self, invalid_symptoms: List[str], supported_symptoms: List[str]):
        self.invalid_symptoms = invalid_symptoms
        self.supported_symptoms = supported_symptoms
        super().__init__(
            f"Unsupported symptoms encountered: {invalid_symptoms}. "
            f"Must be from the supported list of {len(supported_symptoms)} symptoms."
        )


class DiseasePredictor:
    """Production-grade prediction engine."""

    def __init__(
        self,
        model_path: str = DEFAULT_MODEL_PATH,
        metadata_path: str = DEFAULT_METADATA_PATH
    ):
        self.model_path = model_path
        self.metadata_path = metadata_path
        self.model = None
        self.metadata = None
        self.feature_names = []
        self.diseases = []
        self.model_name = "Unknown"
        self.supports_proba = False
        self.is_calibrated = False
        self._symptom_set = set()
        self._shap_explainer = None  # Lazy-initialized on first SHAP call

        self._load_artifacts()

    def _load_artifacts(self):
        """Loads and verifies the saved joblib artifacts."""
        if not os.path.exists(self.model_path):
            raise ModelNotLoadedError(f"Model file not found at: {self.model_path}. Please run train_model.py first.")
        if not os.path.exists(self.metadata_path):
            raise ModelNotLoadedError(f"Metadata file not found at: {self.metadata_path}. Please run train_model.py first.")

        try:
            self.model = joblib.load(self.model_path)
            self.metadata = joblib.load(self.metadata_path)

            self.feature_names = self.metadata.get("feature_names", [])
            self.diseases = self.metadata.get("diseases", [])
            self.model_name = self.metadata.get("model_name", "Random Forest")
            self.is_calibrated = self.metadata.get("is_calibrated", False)
            self.supports_proba = hasattr(self.model, "predict_proba")
            self._symptom_set = set(self.feature_names)

            if not self.feature_names:
                raise ValueError("Metadata contains empty feature_names list.")

        except Exception as e:
            raise ModelNotLoadedError(f"Failed to load model artifacts: {str(e)}") from e

    def get_supported_symptoms(self) -> List[str]:
        """Returns sorted list of all supported symptom feature names."""
        return sorted(self.feature_names)

    def get_supported_symptoms_count(self) -> int:
        """Returns total count of supported symptoms."""
        return len(self.feature_names)

    def get_supported_diseases(self) -> List[str]:
        """Returns sorted list of all target disease categories."""
        return sorted(self.diseases)

    def validate_symptoms(self, symptoms: List[str]) -> List[str]:
        """
        Validates symptoms list.
        Returns cleaned/normalized list of symptoms.
        Raises ValueError on empty input or InvalidSymptomError on unknown symptoms.
        """
        if not isinstance(symptoms, (list, tuple, set)):
            raise ValueError("Symptoms must be provided as a list of strings.")

        # Clean and strip names
        cleaned = [str(s).strip().lower().replace(" ", "_") for s in symptoms if str(s).strip()]

        if not cleaned:
            raise ValueError("No symptoms provided. Please select at least one symptom.")

        # Check for unsupported symptoms
        invalid = [s for s in cleaned if s not in self._symptom_set]
        if invalid:
            raise InvalidSymptomError(invalid_symptoms=invalid, supported_symptoms=self.get_supported_symptoms())

        # Deduplicate while preserving order
        seen = set()
        deduped = []
        for s in cleaned:
            if s not in seen:
                seen.add(s)
                deduped.append(s)

        return deduped

    def predict(self, symptoms: List[str]) -> Dict[str, Any]:
        """
        Generates a disease prediction for the provided symptoms list.

        Parameters:
            symptoms: List of symptom string identifiers (e.g. ['itching', 'skin_rash'])

        Returns:
            Dict containing:
                - disease: predicted disease name
                - confidence: float score between 0.0 and 1.0
                - confidence_percent: formatted percentage string
                - matched_symptoms: list of symptoms recognized and used
                - model_name: algorithm name
                - top_probabilities: list of top 3 possibilities with scores
        """
        valid_symptoms = self.validate_symptoms(symptoms)

        # Build feature vector DataFrame with exact column names and ordering
        vec_zeros = np.zeros((1, len(self.feature_names)), dtype=int)
        input_df = pd.DataFrame(vec_zeros, columns=self.feature_names)

        # Set 1 for active symptoms
        input_df.loc[0, valid_symptoms] = 1

        # Predict primary disease
        raw_pred = self.model.predict(input_df)[0]
        predicted_disease = str(raw_pred)

        # Estimate confidence
        confidence = 0.0
        top_probabilities = []

        if self.supports_proba:
            probabilities = self.model.predict_proba(input_df)[0]
            classes = list(self.model.classes_)

            # Top class confidence
            pred_idx = classes.index(predicted_disease) if predicted_disease in classes else np.argmax(probabilities)
            confidence = float(probabilities[pred_idx])

            # Top 3 candidates
            sorted_indices = np.argsort(probabilities)[::-1][:3]
            for idx in sorted_indices:
                prob = float(probabilities[idx])
                if prob > 0.001:  # Filter out negligible zeroes
                    top_probabilities.append({
                        "disease": classes[idx],
                        "confidence": round(prob, 4),
                        "confidence_percent": f"{prob * 100:.1f}%"
                    })
        else:
            confidence = 1.0
            top_probabilities.append({
                "disease": predicted_disease,
                "confidence": 1.0,
                "confidence_percent": "100.0%"
            })

        # Retrieve clinical knowledge and explanations
        details = get_disease_details(predicted_disease)

        # Compute SHAP per-symptom explanations
        shap_explanations = self._compute_shap_explanation(input_df, predicted_disease)

        return {
            "disease": predicted_disease,
            "display_name": details.get("display_name", predicted_disease),
            "category": details.get("category", "General Clinical"),
            "system": details.get("system", "Systemic"),
            "severity": details.get("severity", "Moderate"),
            "urgency_color": details.get("urgency_color", "#0284c7"),
            "specialist": details.get("specialist", "General Physician"),
            "explanation": details.get("explanation", ""),
            "precautions": details.get("precautions", []),
            "confidence": round(confidence, 4),
            "confidence_percent": f"{confidence * 100:.1f}%",
            "matched_symptoms": valid_symptoms,
            "symptom_count": len(valid_symptoms),
            "model_name": self.model_name,
            "is_calibrated": self.is_calibrated,
            "top_probabilities": top_probabilities,
            "shap_explanations": shap_explanations
        }

    def _compute_shap_explanation(self, input_df: pd.DataFrame, predicted_disease: str) -> List[Dict]:
        """
        Compute SHAP values for the current prediction to explain which symptoms
        contributed most to the predicted disease class.

        Returns a list of dicts: [{symptom, display_name, shap_value, contribution_pct}]
        sorted by absolute contribution descending. Only includes active symptoms.
        """
        if not SHAP_AVAILABLE:
            return []

        try:
            # Build a background summary for TreeExplainer (use zero-vector as baseline)
            background = pd.DataFrame(
                np.zeros((1, len(self.feature_names))),
                columns=self.feature_names
            )

            # Unwrap CalibratedClassifierCV to get the underlying tree model
            raw_model = getattr(self.model, "estimator", self.model)

            # Build or reuse SHAP explainer (TreeExplainer supports RF, XGB, LGBM)
            if self._shap_explainer is None:
                try:
                    self._shap_explainer = shap.TreeExplainer(
                        raw_model,
                        data=background,
                        feature_perturbation="interventional"
                    )
                except Exception:
                    # Fallback: LinearExplainer or KernelExplainer
                    self._shap_explainer = shap.KernelExplainer(
                        raw_model.predict_proba if hasattr(raw_model, "predict_proba") else raw_model.predict,
                        background
                    )

            # Get SHAP values — shape: (n_classes, n_features) for multi-class
            shap_vals = self._shap_explainer.shap_values(input_df)

            # For multi-class: select SHAP values for the predicted class
            if isinstance(shap_vals, list):
                classes = list(raw_model.classes_) if hasattr(raw_model, "classes_") else self.diseases
                if predicted_disease in classes:
                    class_idx = classes.index(predicted_disease)
                    class_shap = shap_vals[class_idx][0]  # shape (n_features,)
                else:
                    class_shap = shap_vals[0][0]
            else:
                class_shap = shap_vals[0]  # shape (n_features,)

            # Extract only the active symptoms (those set to 1)
            active_indices = np.where(input_df.values[0] == 1)[0]
            if len(active_indices) == 0:
                return []

            active_shap = [(self.feature_names[i], float(class_shap[i])) for i in active_indices]

            # Sort by absolute SHAP value descending
            active_shap.sort(key=lambda x: abs(x[1]), reverse=True)

            # Normalize to percentage contribution
            total_abs = sum(abs(v) for _, v in active_shap) or 1.0
            result = []
            for sym, val in active_shap:
                result.append({
                    "symptom": sym,
                    "display_name": sym.replace("_", " ").title(),
                    "shap_value": round(val, 4),
                    "contribution_pct": round(abs(val) / total_abs * 100, 1)
                })

            return result

        except Exception as e:
            # SHAP is optional — never crash the prediction
            print(f"[SHAP] Explanation skipped: {e}")
            return []



# Singleton helper for easy reuse
_instance: Optional[DiseasePredictor] = None


def get_predictor(force_reload: bool = False) -> DiseasePredictor:
    """Returns singleton instance of DiseasePredictor."""
    global _instance
    if _instance is None or force_reload:
        _instance = DiseasePredictor()
    return _instance
