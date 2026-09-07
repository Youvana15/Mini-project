"""
Utility Calculation Engine.
Calculates multi-objective expected utility for candidate deception strategies.
Configurable weights and normalized explainable scoring.
"""

from typing import Dict, Any


class UtilityEngine:
    """
    Multi-objective utility calculator balancing defensive gain against operational friction.
    """

    DEFAULT_WEIGHTS = {
        "security_benefit": 0.25,
        "detection_benefit": 0.20,
        "delay_benefit": 0.20,
        "intelligence_value": 0.15,
        "deployment_cost": 0.08,
        "operational_risk": 0.12,
    }

    def __init__(self, weights: Dict[str, float] = None):
        self.weights = weights or self.DEFAULT_WEIGHTS.copy()
        # Max delay normalization cap (e.g. 30 minutes = 1.0)
        self.max_delay_scale = 30.0

    def compute_utility(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compute normalized utility score (0 - 100) for a given counterfactual scenario.
        """
        sec_benefit = float(scenario.get("security_benefit", 0.5))
        det_prob = float(scenario.get("detection_probability", 0.5))
        delay_min = float(scenario.get("expected_delay_min", 0.0))
        delay_norm = min(1.0, delay_min / self.max_delay_scale)
        intel_val = float(scenario.get("intelligence_value", 0.1))
        dep_cost = float(scenario.get("deployment_cost", 0.1))
        ops_risk = float(scenario.get("operational_risk", 0.1))

        # Positive Utility Components
        pos_sec = self.weights["security_benefit"] * sec_benefit
        pos_det = self.weights["detection_benefit"] * det_prob
        pos_delay = self.weights["delay_benefit"] * delay_norm
        pos_intel = self.weights["intelligence_value"] * intel_val
        total_positive = pos_sec + pos_det + pos_delay + pos_intel

        # Negative Penalty Components
        neg_cost = self.weights["deployment_cost"] * dep_cost
        neg_risk = self.weights["operational_risk"] * ops_risk
        total_penalties = neg_cost + neg_risk

        # Net raw utility
        net_raw = total_positive - total_penalties

        # Normalized to 0 - 100 range
        # When positive is at maximum (0.80) and penalty at minimum (0.00), net = 0.80
        # Normalize net_raw / sum(positive_weights)
        max_possible_pos = (
            self.weights["security_benefit"]
            + self.weights["detection_benefit"]
            + self.weights["delay_benefit"]
            + self.weights["intelligence_value"]
        )

        norm_score = max(0.0, min(100.0, (net_raw / max_possible_pos) * 100.0))
        norm_score = round(norm_score, 1)

        return {
            "utility_score": norm_score,
            "components": {
                "security_gain": round(pos_sec * 100.0, 1),
                "detection_gain": round(pos_det * 100.0, 1),
                "delay_gain": round(pos_delay * 100.0, 1),
                "intelligence_gain": round(pos_intel * 100.0, 1),
                "cost_penalty": round(neg_cost * 100.0, 1),
                "risk_penalty": round(neg_risk * 100.0, 1),
            },
            "net_positive": round(total_positive * 100.0, 1),
            "net_penalty": round(total_penalties * 100.0, 1),
        }
