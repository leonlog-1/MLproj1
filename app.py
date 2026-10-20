"""
app.py
======
Flask Web Application & REST API for Disease Prediction from Symptoms.

Endpoints:
- GET  /                : Renders modern interactive web UI
- GET  /api/symptoms    : Returns JSON list of all 132 supported symptoms
- POST /api/predict     : Evaluates symptom input and returns ML prediction
- GET  /health          : Readiness and diagnostic status
"""

import os
import sys
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from predictor import (
    DiseasePredictor,
    ModelNotLoadedError,
    InvalidSymptomError,
    get_predictor
)

# App configuration
app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# Global predictor holder
predictor: DiseasePredictor = None
model_load_error: str = None

try:
    predictor = get_predictor()
except Exception as e:
    model_load_error = str(e)
    print(f"[WARNING] Could not load predictor on startup: {model_load_error}", file=sys.stderr)


@app.route("/")
def index():
    """Serves the main frontend single-page application."""
    return render_template("index.html")


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint indicating model readiness and system status."""
    if predictor is None:
        return jsonify({
            "status": "error",
            "ready": False,
            "message": "Model not loaded. Please ensure train_model.py has been executed.",
            "error_detail": model_load_error
        }), 503

    return jsonify({
        "status": "healthy",
        "ready": True,
        "model_name": predictor.model_name,
        "supported_symptoms_count": predictor.get_supported_symptoms_count(),
        "supported_diseases_count": len(predictor.get_supported_diseases()),
        "supports_confidence": predictor.supports_proba,
        "is_calibrated": predictor.is_calibrated,
        "shap_available": predictor.SHAP_AVAILABLE if hasattr(predictor, "SHAP_AVAILABLE") else False
    }), 200


@app.route("/api/symptoms", methods=["GET"])
def get_symptoms():
    """Returns the alphabetical list of all supported symptoms."""
    if predictor is None:
        return jsonify({
            "success": False,
            "error": "Model not loaded. Please train the model first."
        }), 503

    symptoms = predictor.get_supported_symptoms()
    formatted = [
        {
            "id": s,
            "name": s.replace("_", " ").title()
        }
        for s in symptoms
    ]

    return jsonify({
        "success": True,
        "count": len(symptoms),
        "symptoms": formatted
    }), 200


@app.route("/api/predict", methods=["POST"])
def predict():
    """
    Receives symptom list, validates against model vocabulary,
    and returns ML prediction.

    Expected Request JSON:
        { "symptoms": ["itching", "skin_rash"] }
    """
    if predictor is None:
        return jsonify({
            "success": False,
            "error": "Prediction model is currently unavailable. Ensure training artifacts exist."
        }), 503

    if not request.is_json:
        return jsonify({
            "success": False,
            "error": "Invalid Content-Type. Request body must be JSON."
        }), 400

    data = request.get_json(silent=True)
    if data is None or "symptoms" not in data:
        return jsonify({
            "success": False,
            "error": "Missing 'symptoms' field in request body. Example: {'symptoms': ['itching', 'skin_rash']}"
        }), 400

    symptoms_input = data.get("symptoms")

    if not isinstance(symptoms_input, list):
        return jsonify({
            "success": False,
            "error": "'symptoms' field must be a list of symptom strings."
        }), 400

    if len(symptoms_input) == 0:
        return jsonify({
            "success": False,
            "error": "No symptoms selected. Please select at least one symptom to get a prediction."
        }), 422

    try:
        prediction_result = predictor.predict(symptoms_input)
        return jsonify({
            "success": True,
            "prediction": prediction_result
        }), 200

    except InvalidSymptomError as err:
        return jsonify({
            "success": False,
            "error": "One or more selected symptoms are not recognized by the model.",
            "invalid_symptoms": err.invalid_symptoms,
            "supported_symptoms_count": len(err.supported_symptoms)
        }), 400

    except ValueError as val_err:
        return jsonify({
            "success": False,
            "error": str(val_err)
        }), 422

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Internal prediction engine error: {str(e)}"
        }), 500


if __name__ == "__main__":
    # Standard local development server
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting SymptomAI server on http://127.0.0.1:{port}")
    app.run(host="127.0.0.1", port=port, debug=False)
