"""
test_api.py
===========
Integration tests for Flask API endpoints.
"""

import pytest
import json
from app import app


@pytest.fixture
def client():
    """Configures and returns a Flask test client."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_route(client):
    """Test that GET / returns the HTML page."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"SymptomAI" in response.data
    assert b"Understand Your Symptoms with AI" in response.data


def test_health_endpoint(client):
    """Test that GET /health returns status 200 and healthy readiness."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert data["ready"] is True
    assert data["supported_symptoms_count"] == 132
    assert data["supported_diseases_count"] == 41


def test_get_symptoms_endpoint(client):
    """Test that GET /api/symptoms returns 132 symptoms in JSON."""
    response = client.get("/api/symptoms")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["count"] == 132
    assert len(data["symptoms"]) == 132
    first = data["symptoms"][0]
    assert "id" in first
    assert "name" in first


def test_predict_endpoint_valid_input(client):
    """Test that POST /api/predict returns 200 with real prediction."""
    payload = {
        "symptoms": ["itching", "skin_rash", "nodal_skin_eruptions"]
    }
    response = client.post(
        "/api/predict",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    pred = data["prediction"]
    assert pred["disease"] == "Fungal infection"
    assert "display_name" in pred
    assert "explanation" in pred
    assert "precautions" in pred
    assert len(pred["precautions"]) >= 3
    assert "specialist" in pred
    assert 0.0 <= pred["confidence"] <= 1.0
    assert len(pred["matched_symptoms"]) == 3



def test_predict_endpoint_empty_symptoms(client):
    """Test that POST /api/predict with empty symptoms returns 422."""
    payload = {"symptoms": []}
    response = client.post(
        "/api/predict",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 422
    data = response.get_json()
    assert data["success"] is False
    assert "error" in data


def test_predict_endpoint_invalid_symptom(client):
    """Test that POST /api/predict with unsupported symptom returns 400."""
    payload = {"symptoms": ["fake_nonexistent_symptom_xyz"]}
    response = client.post(
        "/api/predict",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "invalid_symptoms" in data


def test_predict_endpoint_missing_symptoms_key(client):
    """Test that POST /api/predict with missing 'symptoms' key returns 400."""
    payload = {"wrong_key": ["itching"]}
    response = client.post(
        "/api/predict",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False


def test_predict_endpoint_non_json_request(client):
    """Test that POST /api/predict with plain text content-type returns 400."""
    response = client.post(
        "/api/predict",
        data="just text",
        content_type="text/plain"
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
