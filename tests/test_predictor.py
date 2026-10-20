"""
test_predictor.py
=================
Unit tests for DiseasePredictor engine.
"""

import pytest
import os
from predictor import (
    DiseasePredictor,
    ModelNotLoadedError,
    InvalidSymptomError,
    get_predictor
)


@pytest.fixture
def predictor():
    """Fixture returning an initialized DiseasePredictor instance."""
    return get_predictor()


def test_predictor_initialization(predictor):
    """Test that predictor initializes with valid feature and disease counts."""
    assert predictor is not None
    assert predictor.get_supported_symptoms_count() == 132
    assert len(predictor.get_supported_diseases()) == 41
    assert predictor.model_name in ["Random Forest", "Decision Tree", "Gaussian Naive Bayes", "LightGBM", "XGBoost"]


def test_get_supported_symptoms_structure(predictor):
    """Test supported symptoms list is alphabetical and contains expected symptoms."""
    symptoms = predictor.get_supported_symptoms()
    assert isinstance(symptoms, list)
    assert len(symptoms) == 132
    assert "itching" in symptoms
    assert "skin_rash" in symptoms
    assert "high_fever" in symptoms
    assert symptoms == sorted(symptoms)


def test_predict_with_valid_symptoms(predictor):
    """Test prediction with a valid set of symptoms."""
    res = predictor.predict(["itching", "skin_rash", "nodal_skin_eruptions"])
    assert isinstance(res, dict)
    assert "disease" in res
    assert "display_name" in res
    assert "explanation" in res
    assert len(res["explanation"]) > 20
    assert "precautions" in res
    assert len(res["precautions"]) >= 3
    assert "specialist" in res
    assert "severity" in res
    assert "confidence" in res
    assert "confidence_percent" in res
    assert "matched_symptoms" in res
    assert "model_name" in res
    assert res["disease"] == "Fungal infection"
    assert 0.0 <= res["confidence"] <= 1.0
    assert len(res["matched_symptoms"]) == 3



def test_predict_normalization(predictor):
    """Test that inputs with capital letters and spaces are normalized."""
    res = predictor.predict(["Itching", "Skin Rash"])
    assert "itching" in res["matched_symptoms"]
    assert "skin_rash" in res["matched_symptoms"]
    assert res["disease"] is not None


def test_predict_empty_list_raises_error(predictor):
    """Test that an empty symptoms list raises ValueError."""
    with pytest.raises(ValueError, match="No symptoms provided"):
        predictor.predict([])


def test_predict_invalid_symptoms_raises_error(predictor):
    """Test that unsupported symptom names raise InvalidSymptomError."""
    with pytest.raises(InvalidSymptomError) as exc_info:
        predictor.predict(["completely_fake_symptom_123"])
    assert "completely_fake_symptom_123" in exc_info.value.invalid_symptoms


def test_predict_mixed_valid_and_invalid_symptoms(predictor):
    """Test that mixing valid and invalid symptoms catches the invalid one."""
    with pytest.raises(InvalidSymptomError) as exc_info:
        predictor.predict(["itching", "not_a_real_symptom"])
    assert "not_a_real_symptom" in exc_info.value.invalid_symptoms


def test_missing_model_path_raises_error():
    """Test that pointing to non-existent model files raises ModelNotLoadedError."""
    with pytest.raises(ModelNotLoadedError):
        DiseasePredictor(model_path="non_existent_model.joblib", metadata_path="non_existent_meta.joblib")
