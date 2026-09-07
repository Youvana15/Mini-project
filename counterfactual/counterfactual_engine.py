"""
Counterfactual Engine.
Simulates and ranks all candidate deception strategies (D1 - D7)
for the active threat context using the scenario simulator and utility engine.
"""

from typing import Dict, List, Any
from deception.deception_simulator import DECEPTION_STRATEGIES
from counterfactual.scenario_simulator import simulate_scenario
from decision.utility_engine import UtilityEngine


class CounterfactualEngine:
    """
    Evaluates 'What-If' scenarios across all candidate strategies and ranks them by expected utility.
    """

    def __init__(self, utility_engine: UtilityEngine = None):
        self.utility_engine = utility_engine or UtilityEngine()

    def evaluate_all_strategies(
        self,
        attack_label: str,
        attacker_state: str,
        risk_score: float,
        sophistication: float,
        asset_criticality: float,
    ) -> Dict[str, Any]:
        """
        Evaluate all 7 deception strategies under current attack context.
        Returns detailed metrics, utilities, delta against baseline (D1), and ranked list.
        """
        scenarios: List[Dict[str, Any]] = []

        # 1. Run simulation for each strategy
        for strat_id in DECEPTION_STRATEGIES.keys():
            raw_scenario = simulate_scenario(
                strategy_id=strat_id,
                attack_label=attack_label,
                attacker_state=attacker_state,
                risk_score=risk_score,
                sophistication=sophistication,
                asset_criticality=asset_criticality,
            )
            # Compute utility
            utility_data = self.utility_engine.compute_utility(raw_scenario)
            raw_scenario.update(utility_data)
            scenarios.append(raw_scenario)

        # 2. Sort by overall utility descending
        ranked_scenarios = sorted(scenarios, key=lambda s: s["utility_score"], reverse=True)

        # 3. Find baseline (D1: No Deception)
        baseline = next((s for s in scenarios if s["strategy_id"] == "D1"), scenarios[-1])
        baseline_util = baseline["utility_score"]

        # 4. Annotate deltas against baseline
        for s in ranked_scenarios:
            s["delta_utility_vs_baseline"] = round(s["utility_score"] - baseline_util, 1)
            s["detection_rate_pct"] = f"{int(s['detection_probability'] * 100)}%"
            s["engagement_rate_pct"] = f"{int(s['attacker_engagement'] * 100)}%"
            s["progression_risk_pct"] = f"{int(s['progression_probability'] * 100)}%"
            s["asset_exposure_pct"] = f"{int(s['asset_exposure_probability'] * 100)}%"
            s["intelligence_level"] = "High" if s["intelligence_value"] >= 0.75 else ("Medium" if s["intelligence_value"] >= 0.40 else "Low")
            s["cost_level"] = "High" if s["deployment_cost"] >= 0.35 else ("Medium" if s["deployment_cost"] >= 0.18 else "Low")
            s["risk_level"] = "High" if s["operational_risk"] >= 0.40 else ("Medium" if s["operational_risk"] >= 0.20 else "Low")

        return {
            "attack_context": {
                "detected_attack": attack_label,
                "attacker_state": attacker_state,
                "risk_score": risk_score,
                "sophistication": sophistication,
                "asset_criticality": asset_criticality,
            },
            "scenarios": ranked_scenarios,
            "baseline_strategy": baseline,
            "top_strategy": ranked_scenarios[0],
            "total_evaluated": len(ranked_scenarios),
        }
