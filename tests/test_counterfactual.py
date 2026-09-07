"""
Unit tests for Counterfactual Reasoning Engine and Scenario Simulator.
"""

import pytest
from counterfactual.scenario_simulator import simulate_scenario
from counterfactual.counterfactual_engine import CounterfactualEngine


def test_scenario_simulator_d4_vs_d1():
    """Verify D4 provides higher delay and lower exposure than D1 for DB probe."""
    res_d4 = simulate_scenario("D4", "DB_PROBE", "S6", 82.0, 0.70, 0.85)
    res_d1 = simulate_scenario("D1", "DB_PROBE", "S6", 82.0, 0.70, 0.85)

    assert res_d4["expected_delay_min"] > res_d1["expected_delay_min"]
    assert res_d4["asset_exposure_probability"] < res_d1["asset_exposure_probability"]
    assert res_d4["detection_probability"] > res_d1["detection_probability"]


def test_counterfactual_engine_evaluates_seven_strategies():
    """Verify all 7 strategies are evaluated and sorted by utility."""
    engine = CounterfactualEngine()
    results = engine.evaluate_all_strategies(
        attack_label="DB_PROBE",
        attacker_state="S6",
        risk_score=80.0,
        sophistication=0.70,
        asset_criticality=0.85,
    )
    assert len(results["scenarios"]) == 7
    # Top strategy should have higher utility than baseline D1
    top_strat = results["top_strategy"]
    baseline = results["baseline_strategy"]
    assert top_strat["utility_score"] >= baseline["utility_score"]
