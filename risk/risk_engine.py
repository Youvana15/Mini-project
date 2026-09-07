"""
Dynamic Risk Assessment Engine.
Computes quantifiable risk scores (0–100) and classifications based on multi-factor threat dynamics.
"""

from typing import Dict, Any

ATTACK_SEVERITY_WEIGHTS = {
    "NORMAL": 0.05,
    "RECONNAISSANCE": 0.35,
    "BRUTE_FORCE": 0.55,
    "CREDENTIAL_ATTACK": 0.65,
    "DB_PROBE": 0.82,
    "PRIVILEGE_ESCALATION": 0.85,
    "LATERAL_MOVEMENT": 0.80,
    "DATA_ACCESS": 0.90,
    "EXFILTRATION": 0.98,
}

STATE_PROGRESSION_WEIGHTS = {
    "S0": 0.05,
    "S1": 0.20,
    "S2": 0.35,
    "S3": 0.50,
    "S4": 0.68,
    "S5": 0.78,
    "S6": 0.88,
    "S7": 0.98,
}


class RiskEngine:
    """
    Evaluates dynamic risk combining probabilistic detection, asset criticality,
    attacker stage, and adversary capability.
    """

    def calculate_risk(
        self,
        detected_attack: str,
        detection_confidence: float,
        attacker_state: str,
        attacker_sophistication: float,
        asset_criticality: float,
        session_telemetry: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """
        Calculate composite risk score (0-100) and factor breakdowns.
        """
        severity = ATTACK_SEVERITY_WEIGHTS.get(detected_attack, 0.40)
        progression = STATE_PROGRESSION_WEIGHTS.get(attacker_state, 0.30)
        conf = max(0.1, min(1.0, detection_confidence))
        soph = max(0.05, min(1.0, attacker_sophistication))
        crit = max(0.1, min(1.0, asset_criticality))

        if detected_attack == "NORMAL":
            # Normal baseline risk stays low
            base_risk = 10.0 * crit + 5.0 * soph
            risk_score = round(max(2.0, min(25.0, base_risk)), 1)
        else:
            # Multi-factor mathematical formula:
            # Weighted combination of Severity (30%), Criticality (25%), Progression (20%),
            # Sophistication (15%), and Confidence (10%)
            raw_factor = (
                0.30 * severity
                + 0.25 * crit
                + 0.20 * progression
                + 0.15 * soph
                + 0.10 * conf
            )
            # Apply non-linear multiplier for high-criticality data exfiltration/probing
            if detected_attack in ["DB_PROBE", "DATA_ACCESS", "EXFILTRATION"] and crit > 0.7:
                multiplier = 1.15
            else:
                multiplier = 1.0

            risk_score = round(min(100.0, max(5.0, raw_factor * 100.0 * multiplier)), 1)

        # Classification
        if risk_score <= 30.0:
            level = "LOW"
            color = "#00ff9d"  # Green
        elif risk_score <= 60.0:
            level = "MEDIUM"
            color = "#00f0ff"  # Cyan
        elif risk_score <= 80.0:
            level = "HIGH"
            color = "#ffb800"  # Amber
        else:
            level = "CRITICAL"
            color = "#ff3366"  # Crimson

        # Potential impact estimation
        potential_impact = round(crit * severity * 100.0, 1)

        return {
            "risk_score": risk_score,
            "risk_level": level,
            "color": color,
            "factors": {
                "attack_severity": severity,
                "asset_criticality": crit,
                "state_progression": progression,
                "attacker_sophistication": soph,
                "detection_confidence": conf,
                "potential_impact": potential_impact,
            },
            "summary": (
                f"Threat Level {level} (Score {risk_score}/100) calculated from "
                f"{detected_attack} on criticality {crit:.2f} target at stage {attacker_state}."
            ),
        }
