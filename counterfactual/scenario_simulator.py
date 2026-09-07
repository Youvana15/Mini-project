"""
Counterfactual Scenario Simulator.
Generates hypothetical outcomes for defensive strategies D1 - D7 under specific attack context.
Computes counterfactual metrics using deterministic mathematical modeling rather than static constants.
"""

from typing import Dict, Any
from deception.deception_simulator import DECEPTION_STRATEGIES

STATE_INDEX = {
    "S0": 0, "S1": 1, "S2": 2, "S3": 3,
    "S4": 4, "S5": 5, "S6": 6, "S7": 7
}


def simulate_scenario(
    strategy_id: str,
    attack_label: str,
    attacker_state: str,
    risk_score: float,
    sophistication: float,
    asset_criticality: float,
) -> Dict[str, Any]:
    """
    Simulate counterfactual scenario:
    "What would happen if the defender selected strategy_id for this attack?"
    """
    strat = DECEPTION_STRATEGIES.get(strategy_id, DECEPTION_STRATEGIES["D1"])
    state_idx = STATE_INDEX.get(attacker_state, 1)

    # 1. Target and State Affinity Alpha
    attack_match = 1.0 if attack_label in strat["targeted_attacks"] else (0.2 if strategy_id == "D1" else 0.45)
    state_match = 1.0 if attacker_state in strat["primary_states"] else (0.3 if strategy_id == "D1" else 0.50)
    affinity = round(0.60 * attack_match + 0.40 * state_match, 3)

    # 2. Attacker Engagement Probability
    if strategy_id == "D1":
        p_engage = 0.0
    else:
        p_engage = strat["base_attacker_engagement"] * (0.65 + 0.35 * affinity) * (1.08 - 0.20 * sophistication)
        p_engage = round(max(0.12, min(0.97, p_engage)), 3)

    # 3. Expected Delay (Attacker Dwell Time Wasted in Decoy) in minutes
    if strategy_id == "D1":
        expected_delay = 0.0
    else:
        expected_delay = strat["base_expected_delay_min"] * (0.50 + 0.50 * affinity) * p_engage * (1.1 - 0.2 * sophistication)
        expected_delay = round(max(1.0, expected_delay), 1)

    # 4. Detection & Attribution Probability
    if strategy_id == "D1":
        p_detect = round(0.35 + 0.10 * sophistication, 3)
    else:
        p_detect = strat["base_detection_probability"] * (0.78 + 0.22 * affinity)
        p_detect = round(max(0.30, min(0.99, p_detect)), 3)

    # 5. Attack Progression Probability (chance attacker successfully moves deeper)
    if strategy_id == "D1":
        p_progress = round(min(0.98, 0.45 + 0.35 * sophistication + 0.18 * (state_idx / 7.0)), 3)
    else:
        # Decoy traps or misdirects adversary
        p_progress = 0.48 * (1.0 - 0.75 * p_engage * affinity) + 0.22 * sophistication
        p_progress = round(max(0.04, min(0.85, p_progress)), 3)

    # 6. Critical Asset Exposure Probability
    if strategy_id == "D1":
        p_exposure = round(min(0.99, asset_criticality * (0.45 + 0.50 * sophistication)), 3)
    else:
        # Active decoy shields real assets by absorbing queries/probes
        shielding_factor = 1.0 - (0.88 * p_engage * affinity)
        p_exposure = asset_criticality * (0.45 + 0.50 * sophistication) * shielding_factor
        p_exposure = round(max(0.02, min(0.95, p_exposure)), 3)

    # 7. Intelligence Value
    if strategy_id == "D1":
        v_intel = 0.05
    else:
        v_intel = strat["base_intelligence_value"] * (0.55 + 0.45 * affinity) * (0.75 + 0.25 * sophistication)
        v_intel = round(max(0.08, min(0.98, v_intel)), 3)

    # 8. Deployment Cost and Operational Risk
    cost = strat["base_deployment_cost"]
    if strategy_id == "D1":
        # Passive baseline incurs massive operational vulnerability risk
        ops_risk = round(min(0.95, 0.70 + 0.25 * asset_criticality), 3)
    else:
        ops_risk = strat["base_operational_risk"] * (1.1 - 0.2 * affinity) + 0.05 * (1.0 - p_engage)
        ops_risk = round(max(0.05, min(0.80, ops_risk)), 3)

    # 9. Security Benefit
    sec_benefit = round((1.0 - p_exposure) * 0.60 + (1.0 - p_progress) * 0.40, 3)

    return {
        "strategy_id": strategy_id,
        "strategy_name": strat["name"],
        "strategy_category": strat["category"],
        "affinity_score": affinity,
        "detection_probability": p_detect,
        "attacker_engagement": p_engage,
        "expected_delay_min": expected_delay,
        "progression_probability": p_progress,
        "asset_exposure_probability": p_exposure,
        "intelligence_value": v_intel,
        "deployment_cost": cost,
        "operational_risk": ops_risk,
        "security_benefit": sec_benefit,
    }
