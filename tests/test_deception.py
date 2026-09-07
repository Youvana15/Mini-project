"""
Unit tests for Deception Deployment and Attacker Response.
"""

import pytest
from simulation.attacker_simulator import AttackerSimulator
from deception.deception_simulator import DeceptionSimulator, DECEPTION_STRATEGIES


def test_deception_registry():
    """Verify all 7 deception strategies are registered with positive delay."""
    sim = DeceptionSimulator()
    strats = sim.get_all_strategies()
    assert len(strats) == 7
    d4 = sim.get_strategy("D4")
    assert d4["name"] == "Fake Database"
    assert d4["base_expected_delay_min"] > 10.0


def test_attacker_interaction_response():
    """Verify attacker reacts to deception and records dwell time."""
    attacker = AttackerSimulator(attack_label="DB_PROBE", sophistication=0.6)
    initial_dwell = attacker.total_dwell_time

    response = attacker.simulate_deception_response(
        strategy_id="D4",
        strategy_name="Fake Database",
        believability=0.92,
        expected_delay_min=24.0,
    )

    assert "attacker_interacted" in response
    assert "delay_minutes" in response
    assert attacker.total_dwell_time >= initial_dwell
