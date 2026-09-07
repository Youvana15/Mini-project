"""
Unit tests for Feature Extraction and ML Detector.
"""

import pytest
import numpy as np
from simulation.session_generator import generate_single_session
from detection.feature_engineering import extract_features_from_dict, FEATURE_COLUMNS
from detection.detection_model import AttackDetector


def test_feature_extraction():
    """Verify feature vector dimensions and types."""
    session = generate_single_session(attack_label="RECONNAISSANCE")
    feats = extract_features_from_dict(session)
    assert feats.shape == (1, len(FEATURE_COLUMNS))
    assert feats.dtype == np.float32


def test_detector_inference():
    """Verify detector produces predictions and confidence scores without crashing."""
    detector = AttackDetector()
    session = generate_single_session(attack_label="DB_PROBE")
    result = detector.predict_session(session)
    assert "predicted_label" in result
    assert 0.0 <= result["confidence"] <= 1.0
    assert "top_features" in result
    assert isinstance(result["is_malicious"], bool)
