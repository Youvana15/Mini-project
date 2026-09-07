"""
Unit tests for Decision Engine and Utility Optimization.
"""

import pytest
from counterfactual.counterfactual_engine import CounterfactualEngine
from decision.decision_engine import DecisionEngine
from decision.utility_engine import UtilityEngine


def test_utility_engine_bounds():
    """Verify utility engine produces scores strictly between 0 and 100."""
    u_engine = UtilityEngine()
    test_scenario = {
        "security_benefit": 0.85,
        "detection_probability": 0.92,
        "expected_delay_min": 24.0,
        "intelligence_value": 0.90,
        "deployment_cost": 0.20,
        "operational_risk": 0.15,
    }
    res = u_engine.compute_utility(test_scenario)
    assert 0.0 <= res["utility_score"] <= 100.0
    assert "components" in res


def test_decision_engine_recommendation():
    """Verify decision engine selects optimal action and provides WHY reasons."""
    cf_engine = CounterfactualEngine()
    cf_data = cf_engine.evaluate_all_strategies(
        attack_label="DB_PROBE",
        attacker_state="S6",
        risk_score=82.0,
        sophistication=0.70,
        asset_criticality=0.85,
    )
    dec_engine = DecisionEngine()
    decision = dec_engine.select_optimal_defence(cf_data)

    assert "recommended_strategy_id" in decision
    assert decision["recommended_strategy_id"] in ["D4", "D5", "D2", "D3", "D6", "D7"]
    assert len(decision["why_reasons"]) >= 3
    assert len(decision["decision_pipeline_steps"]) == 6
