"""
Model wrapper module for estimators requiring integer targets (XGBoost, LightGBM).
Enables seamless serialization and deserialization across scripts and web apps.
"""

import warnings
import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.preprocessing import LabelEncoder


class LabelEncodedClassifier(ClassifierMixin, BaseEstimator):
    """
    Wrapper that encodes string labels to integers before fitting,
    and decodes them back after prediction.
    Required for XGBoost and LightGBM which reject string targets.
    Compatible with CalibratedClassifierCV and scikit-learn cross-validation.
    """
    _estimator_type = "classifier"

    def __init__(self, estimator=None):
        self.estimator = estimator
        self._le = LabelEncoder()

    def fit(self, X, y):
        y_enc = self._le.fit_transform(y)
        self.estimator.fit(X, y_enc)
        self.classes_ = self._le.classes_
        return self

    def predict(self, X):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning)
            y_enc = self.estimator.predict(X)
            return self._le.inverse_transform(np.asarray(y_enc).astype(int))

    def predict_proba(self, X):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning)
            return self.estimator.predict_proba(X)

    def get_params(self, deep=True):
        return {"estimator": self.estimator}

    def set_params(self, **params):
        if "estimator" in params:
            self.estimator = params["estimator"]
        return self

    @property
    def feature_importances_(self):
        return getattr(self.estimator, "feature_importances_", None)
