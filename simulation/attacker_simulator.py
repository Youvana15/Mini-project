"""
Attacker Simulator Module.
Maintains stateful attacker session progression and simulates behavior transitions and responses to deception.
"""

import random
from typing import Dict, Any, Optional
from simulation.session_generator import (
    generate_single_session,
    ATTACK_STATES,
    STATE_DESCRIPTIONS,
    ATTACK_LABELS,
)


class AttackerSimulator:
    """
    Simulates an intelligent or scripted attacker traversing an attack chain (S0 -> S7).
    """

    STATE_ORDER = ["S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7"]

    def __init__(
        self,
        session_id: Optional[str] = None,
        attack_label: str = "DB_PROBE",
        sophistication: float = 0.65,
        asset_criticality: float = 0.85,
    ):
        self.attack_label = attack_label if attack_label in ATTACK_LABELS else "DB_PROBE"
        self.sophistication = max(0.05, min(1.0, sophistication))
        self.asset_criticality = max(0.1, min(1.0, asset_criticality))
        self.current_state = ATTACK_STATES.get(self.attack_label, "S1")
        self.total_dwell_time = 0.0  # minutes spent in network
        self.trapped_by_deception = False
        self.deployed_deceptions_encountered = []
        self.history = []

        # Generate initial telemetry session
        self.current_telemetry = generate_single_session(
            attack_label=self.attack_label,
            sophistication=self.sophistication,
            asset_criticality=self.asset_criticality,
        )
        if session_id:
            self.current_telemetry["session_id"] = session_id
        self.session_id = self.current_telemetry["session_id"]

    def get_state_info(self) -> Dict[str, Any]:
        """Return structured summary of the attacker's current state."""
        state_idx = self.STATE_ORDER.index(self.current_state)
        # Probability of reaching critical assets increases with stage progression and sophistication
        reach_prob = round(
            min(0.99, (state_idx / 7.0) * 0.7 + self.sophistication * 0.3), 3
        )
        # Probabilistic state belief vector (POMDP observation belief)
        state_probs = {}
        for idx, s in enumerate(self.STATE_ORDER):
            dist = abs(idx - state_idx)
            raw_p = max(0.02, 1.0 / (1.0 + 3.0 * dist))
            state_probs[s] = raw_p
        # Normalize
        total_p = sum(state_probs.values())
        state_probs = {k: round(v / total_p, 3) for k, v in state_probs.items()}

        confidence = state_probs[self.current_state]

        return {
            "current_state": self.current_state,
            "state_description": STATE_DESCRIPTIONS[self.current_state],
            "state_confidence": round(confidence, 2),
            "state_index": state_idx,
            "attack_progression": f"{int((state_idx / 7.0) * 100)}%",
            "sophistication": self.sophistication,
            "reach_critical_asset_prob": reach_prob,
            "state_probability_distribution": state_probs,
            "total_dwell_time_minutes": round(self.total_dwell_time, 1),
            "trapped_by_deception": self.trapped_by_deception,
        }

    def simulate_deception_response(
        self,
        strategy_id: str,
        strategy_name: str,
        believability: float,
        expected_delay_min: float,
    ) -> Dict[str, Any]:
        """
        Simulate attacker interaction when a deception strategy is deployed.
        High sophistication reduces engagement chance slightly, but targeted decoys have high believability.
        """
        # Engagement likelihood
        engage_prob = believability * (1.1 - 0.25 * self.sophistication)
        engage_prob = max(0.15, min(0.98, engage_prob))

        interacted = random.random() < engage_prob
        delay_generated = 0.0
        state_changed = False
        behavior_change = "Continued baseline activity"

        if strategy_id == "D1":
            # No Deception: Attacker advances directly without impediment!
            interacted = False
            delay_generated = 0.0
            behavior_change = "Attacker proceeded directly toward production targets without delay."
            # Advance state towards exfiltration
            curr_idx = self.STATE_ORDER.index(self.current_state)
            if curr_idx < len(self.STATE_ORDER) - 1:
                self.current_state = self.STATE_ORDER[curr_idx + 1]
                state_changed = True
        elif interacted:
            self.trapped_by_deception = True
            # Random variation around expected delay
            delay_generated = round(
                expected_delay_min * random.uniform(0.85, 1.25), 1
            )
            self.total_dwell_time += delay_generated
            self.deployed_deceptions_encountered.append(strategy_name)

            behavior_change = (
                f"Attacker engaged with '{strategy_name}'. "
                f"Wasted {delay_generated} minutes analyzing decoy telemetry, executing synthetic queries and attempting authentication against fake assets."
            )

            # Deception containment effect: Attacker is misdirected!
            # They stay in decoy exploration or drop back to analyzing credentials
            if self.current_state in ["S5", "S6", "S7"]:
                # Misdirected into decoy environment, stalling progression
                behavior_change += " Attacker lateral movement contained inside isolated deception sandbox."
            elif self.current_state in ["S1", "S2", "S3", "S4"]:
                behavior_change += " Attacker intelligence gathered via honeytoken/decoy telemetry."
        else:
            # Attacker avoided decoy
            delay_generated = round(expected_delay_min * 0.15, 1)
            self.total_dwell_time += delay_generated
            behavior_change = (
                f"Attacker inspected '{strategy_name}' but suspected artificial environment. "
                f"Brief hesitation generated {delay_generated} min delay before seeking alternate paths."
            )

        # Update telemetry to reflect simulated feedback
        self.current_telemetry["session_duration"] += delay_generated * 60.0
        if interacted:
            self.current_telemetry["database_query_count"] = max(
                self.current_telemetry.get("database_query_count", 0), 25
            )
            self.current_telemetry["command_frequency"] = round(
                self.current_telemetry.get("command_frequency", 1.0) * 1.3, 2
            )

        response_summary = {
            "strategy_id": strategy_id,
            "strategy_name": strategy_name,
            "attacker_interacted": interacted,
            "engagement_probability": round(engage_prob, 2),
            "delay_minutes": delay_generated,
            "total_dwell_time": round(self.total_dwell_time, 1),
            "trapped": self.trapped_by_deception,
            "behavior_summary": behavior_change,
            "new_state": self.current_state,
            "state_changed": state_changed,
            "updated_state_info": self.get_state_info(),
        }

        self.history.append(response_summary)
        return response_summary
