"""
Unit tests for Dynamic Risk Engine.
"""

import pytest
from risk.risk_engine import RiskEngine


def test_normal_traffic_risk():
    """Verify normal traffic produces LOW risk score."""
    engine = RiskEngine()
    res = engine.calculate_risk(
        detected_attack="NORMAL",
        detection_confidence=0.95,
        attacker_state="S0",
        attacker_sophistication=0.2,
        asset_criticality=0.3,
    )
    assert 0.0 <= res["risk_score"] <= 30.0
    assert res["risk_level"] == "LOW"


def test_critical_attack_risk():
    """Verify DB Probe or Exfiltration against critical asset yields HIGH or CRITICAL risk."""
    engine = RiskEngine()
    res = engine.calculate_risk(
        detected_attack="EXFILTRATION",
        detection_confidence=0.98,
        attacker_state="S7",
        attacker_sophistication=0.85,
        asset_criticality=0.95,
    )
    assert res["risk_score"] >= 70.0
    assert res["risk_level"] in ["HIGH", "CRITICAL"]
