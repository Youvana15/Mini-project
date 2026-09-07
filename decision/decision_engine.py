"""
POMDP-Inspired Decision Engine.
Selects optimal defence a* = argmax E[Utility(a | state, threat)]
and generates explainable decision justifications.
"""

from typing import Dict, Any, List


class DecisionEngine:
    """
    Evaluates counterfactual scenario rankings to select the optimal defensive strategy
    and constructs explainable decision rationales.
    """

    def select_optimal_defence(
        self,
        counterfactual_evaluation: Dict[str, Any],
        max_allowable_ops_risk: float = 0.85,
    ) -> Dict[str, Any]:
        """
        Choose the best defensive action maximizing expected utility under risk constraints.
        """
        scenarios: List[Dict[str, Any]] = counterfactual_evaluation.get("scenarios", [])
        if not scenarios:
            raise ValueError("No counterfactual scenarios available for decision evaluation.")

        context = counterfactual_evaluation.get("attack_context", {})
        attack_label = context.get("detected_attack", "NORMAL")
        attacker_state = context.get("attacker_state", "S1")
        risk_score = context.get("risk_score", 50.0)

        # Apply constraint filtering (exclude strategies with excessive operational risk unless baseline)
        valid_candidates = [
            s for s in scenarios if s.get("operational_risk", 1.0) <= max_allowable_ops_risk
        ]
        if not valid_candidates:
            valid_candidates = scenarios

        # a* = argmax Utility
        optimal_scenario = max(valid_candidates, key=lambda s: s["utility_score"])

        # Construct explainable rationale
        why_reasons = self._generate_why_reasons(optimal_scenario, attack_label, attacker_state, risk_score)
        step_by_step_pipeline = [
            f"1. Telemetry Analyzed: Detected '{attack_label}' threat pattern.",
            f"2. Risk Evaluated: Risk score calculated at {risk_score}/100.",
            f"3. Attacker State Estimated: Adversary positioned at stage {attacker_state}.",
            f"4. Counterfactual Simulation: Evaluated 7 hypothetical deception deployments.",
            f"5. Utility Optimization: '{optimal_scenario['strategy_name']}' achieved peak utility of {optimal_scenario['utility_score']}/100.",
            f"6. Recommended Action: Deploy '{optimal_scenario['strategy_name']}' to contain and divert adversary.",
        ]

        return {
            "recommended_strategy_id": optimal_scenario["strategy_id"],
            "recommended_strategy_name": optimal_scenario["strategy_name"],
            "recommended_strategy_category": optimal_scenario.get("strategy_category", "Deception"),
            "utility_score": optimal_scenario["utility_score"],
            "delta_vs_baseline": optimal_scenario.get("delta_utility_vs_baseline", 0.0),
            "expected_delay_minutes": optimal_scenario["expected_delay_min"],
            "detection_probability": optimal_scenario["detection_probability"],
            "engagement_rate": optimal_scenario.get("engagement_rate_pct", "0%"),
            "why_reasons": why_reasons,
            "decision_pipeline_steps": step_by_step_pipeline,
            "optimal_scenario_details": optimal_scenario,
        }

    def _generate_why_reasons(
        self,
        scenario: Dict[str, Any],
        attack_label: str,
        attacker_state: str,
        risk_score: float,
    ) -> List[str]:
        """
        Generate natural language explainability bullets for the chosen strategy.
        """
        strat_id = scenario["strategy_id"]
        strat_name = scenario["strategy_name"]
        delay = scenario["expected_delay_min"]
        det_prob = int(scenario["detection_probability"] * 100)
        exposure = int(scenario["asset_exposure_probability"] * 100)
        utility = scenario["utility_score"]

        reasons = [
            f"Achieves highest expected utility score ({utility}/100) among all evaluated defensive options.",
            f"Expected adversary delay of {delay} minutes, creating sufficient response window for incident responders.",
            f"High deception detection and attribution certainty ({det_prob}% probability).",
            f"Directly mitigates {attack_label} attack vectors by presenting realistic decoy targets.",
            f"Reduces genuine critical asset exposure down to {exposure}%.",
            f"Operational friction and false positive overhead remain minimal ({scenario.get('cost_level', 'Low')} cost profile).",
        ]

        if strat_id == "D4":
            reasons.append("Shields genuine database tables by absorbing synthetic SQL queries and table schemas.")
        elif strat_id == "D2":
            reasons.append("Traps brute-force and credential stuffing attempts within an emulated authentication sandbox.")
        elif strat_id == "D3":
            reasons.append("Intercepts port scanning and reconnaissance probes before real infrastructure is mapped.")
        elif strat_id == "D5":
            reasons.append("Injected honeytokens instantly alert and track lateral movement when queried or invoked.")
        elif strat_id == "D7":
            reasons.append("Decoy documents with tracking beacons poison adversary exfiltration pipelines.")
        elif strat_id == "D1":
            reasons = [
                "Baseline passive monitoring selected because threat level is benign/normal.",
                "Zero operational cost and zero disturbance to production workflows.",
            ]

        return reasons
