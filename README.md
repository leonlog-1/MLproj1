# 🏥 SymptomAI — Disease Prediction from Symptoms Using Machine Learning

An end-to-end Machine Learning web application that predicts possible medical conditions from patient-reported symptoms. Built as an academic mini-project featuring a trained **Random Forest** classifier, a decoupled **Python Flask** REST API, and an interactive, responsive healthcare-themed frontend.

---

## 📌 Project Architecture

```
disease-prediction/
│
├── app.py                          # Flask REST API & Web Server
├── train_model.py                  # Training pipeline & model benchmark
├── predictor.py                    # Standalone prediction engine
├── requirements.txt                # Pinned Python dependencies
├── pytest.ini                      # Pytest runner configuration
├── README.md                       # Setup & usage documentation
│
├── dataset/                        # Dataset directory
│   ├── Training.csv                # 4,920 balanced training samples
│   └── Testing.csv                 # 42 evaluation test samples
│
├── models/                         # Serialized ML artifacts
│   ├── disease_model.joblib        # Best trained model (Random Forest)
│   └── model_metadata.joblib       # 132 feature names & 41 class mappings
│
├── reports/                        # Evaluation reports
│   └── evaluation_report.txt       # Benchmarking metrics & classification report
│
├── docs/                           # Documentation
│   └── DATASET_DOCUMENTATION.md    # In-depth dataset reference & symptom dictionary
│
├── templates/
│   └── index.html                  # Responsive Single-Page Application (SPA)
│
├── static/
│   ├── css/
│   │   └── style.css               # Modern healthcare design system
│   └── js/
│       └── script.js               # Dynamic multi-select search & AJAX controller
│
└── tests/
    ├── test_predictor.py           # Unit tests for prediction logic (8 tests)
    └── test_api.py                 # Integration tests for Flask endpoints (8 tests)
```

---

## 📊 Machine Learning Pipeline & Results

The model was trained and evaluated against three standard supervised learning classifiers using 5-Fold Stratified Cross-Validation on the training set and evaluated on the held-out test set:

| Model | Test Accuracy | Precision (Weighted) | Recall (Weighted) | F1-Score (Weighted) | 5-Fold CV Accuracy |
|---|---|---|---|---|---|
| **Random Forest (Selected)** | **97.62%** | **98.81%** | **97.62%** | **97.62%** | **100.00% (±0.00%)** |
| Decision Tree | 97.62% | 98.81% | 97.62% | 97.62% | 100.00% (±0.00%) |
| Gaussian Naive Bayes | 100.00% | 100.00% | 100.00% | 100.00% | 100.00% (±0.00%) |

### Why Random Forest Was Selected for Production:
1. **Calibrated Probabilities:** Generates true multi-class probability distributions via ensemble tree voting (`predict_proba`), allowing the UI to present model-estimated confidence scores and differential alternatives.
2. **Feature Interdependence:** Naive Bayes assumes symptoms are mutually independent—an assumption that fails in clinical medicine where symptoms like `high_fever` and `chills` strongly correlate.
3. **Overfitting Resistance:** An ensemble of 100 decision trees minimizes variance and prevents single-tree over-specialization.

---

## 🚀 Setup & Execution Guide (Windows / VS Code)

### Prerequisites
- Python 3.9+ installed (`python --version`)
- Visual Studio Code (or any IDE)

### 1. Clone or Open Workspace
Open the project directory in VS Code or PowerShell:
```powershell
cd "d:\ML proj"
```

### 2. (Optional) Create & Activate Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Train the Model
Run the automated training and evaluation pipeline:
```powershell
python train_model.py
```
*Output artifacts will be saved to `models/` and evaluation results to `reports/evaluation_report.txt`.*

### 5. Run the Automated Test Suite
Execute the 16 unit and integration tests:
```powershell
pytest -v
```

### 6. Launch the Web Application
Start the Flask local development server:
```powershell
python app.py
```
Open your web browser and navigate to:
👉 **[http://localhost:5000](http://localhost:5000)**

---

## 🌐 API Reference

### 1. Health Status
- **Method:** `GET`
- **Path:** `/health`
- **Response:**
```json
{
  "model_name": "Random Forest",
  "ready": true,
  "status": "healthy",
  "supported_diseases_count": 41,
  "supported_symptoms_count": 132,
  "supports_confidence": true
}
```

### 2. Supported Symptoms List
- **Method:** `GET`
- **Path:** `/api/symptoms`
- **Response:**
```json
{
  "count": 132,
  "success": true,
  "symptoms": [
    { "id": "abdominal_pain", "name": "Abdominal Pain" },
    { "id": "itching", "name": "Itching" },
    ...
  ]
}
```

### 3. Disease Prediction
- **Method:** `POST`
- **Path:** `/api/predict`
- **Headers:** `Content-Type: application/json`
- **Request Body:**
```json
{
  "symptoms": ["itching", "skin_rash", "nodal_skin_eruptions"]
}
```
- **Response (200 OK):**
```json
{
  "prediction": {
    "confidence": 1.0,
    "confidence_percent": "100.0%",
    "disease": "Fungal infection",
    "matched_symptoms": ["itching", "skin_rash", "nodal_skin_eruptions"],
    "model_name": "Random Forest",
    "symptom_count": 3,
    "top_probabilities": [
      {
        "confidence": 1.0,
        "confidence_percent": "100.0%",
        "disease": "Fungal infection"
      }
    ]
  },
  "success": true
}
```

---

## 🧪 Testing Coverage

The automated test suite in `tests/` validates:
- **Model Loading:** Verification of 132 symptom features and 41 disease classes.
- **Normalization:** Converts user input with spaces or uppercase characters (e.g. `"Skin Rash"` → `"skin_rash"`).
- **Validation:** Handles empty lists (HTTP 422) and unrecognized symptoms (HTTP 400).
- **Endpoint Security & Formatting:** Checks JSON content-type enforcement and API schema compliance.

---

## ⚠️ Academic Disclaimer
*SymptomAI is created strictly as an academic college demonstration project. The predictions produced by this machine learning system are statistical estimations and must **never** be interpreted as clinical diagnoses or medical advice. Consult a licensed healthcare professional for medical concerns.*
