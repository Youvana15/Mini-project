"""
Deception Strategies Specification & Deployment Simulator.
Defines profiles, operational parameters, and deployment mechanics for strategies D1 - D7.
"""

from typing import Dict, Any, List

DECEPTION_STRATEGIES: Dict[str, Dict[str, Any]] = {
    "D1": {
        "id": "D1",
        "name": "No Deception",
        "category": "Passive Baseline",
        "description": "Rely solely on conventional perimeter detection without deploying deceptive assets.",
        "base_deployment_cost": 0.02,
        "base_detection_probability": 0.38,
        "base_attacker_engagement": 0.05,
        "base_expected_delay_min": 0.0,
        "base_containment_value": 0.08,
        "base_intelligence_value": 0.05,
        "base_operational_risk": 0.88,
        "targeted_attacks": ["NORMAL"],
        "primary_states": ["S0"],
    },
    "D2": {
        "id": "D2",
        "name": "Fake Login Portal",
        "category": "Authentication Decoy",
        "description": "High-fidelity simulated SSH/Web/RDP authentication portal capturing credential dumps and brute-force iterations.",
        "base_deployment_cost": 0.22,
        "base_detection_probability": 0.90,
        "base_attacker_engagement": 0.88,
        "base_expected_delay_min": 16.5,
        "base_containment_value": 0.78,
        "base_intelligence_value": 0.86,
        "base_operational_risk": 0.15,
        "targeted_attacks": ["BRUTE_FORCE", "CREDENTIAL_ATTACK"],
        "primary_states": ["S2", "S3"],
    },
    "D3": {
        "id": "D3",
        "name": "Fake Server / Emulated Host",
        "category": "Network Decoy",
        "description": "Emulated host responding to scanning, service enumeration, and internal port sweeps in the DMZ/LAN.",
        "base_deployment_cost": 0.42,
        "base_detection_probability": 0.86,
        "base_attacker_engagement": 0.83,
        "base_expected_delay_min": 21.0,
        "base_containment_value": 0.82,
        "base_intelligence_value": 0.80,
        "base_operational_risk": 0.24,
        "targeted_attacks": ["RECONNAISSANCE", "LATERAL_MOVEMENT"],
        "primary_states": ["S1", "S5"],
    },
    "D4": {
        "id": "D4",
        "name": "Fake Database",
        "category": "Data Decoy",
        "description": "Shadow database populated with synthetic customer tables, deceptive schemas, and honey-records triggering query telemetry.",
        "base_deployment_cost": 0.36,
        "base_detection_probability": 0.94,
        "base_attacker_engagement": 0.92,
        "base_expected_delay_min": 26.0,
        "base_containment_value": 0.92,
        "base_intelligence_value": 0.94,
        "base_operational_risk": 0.18,
        "targeted_attacks": ["DB_PROBE", "DATA_ACCESS"],
        "primary_states": ["S6"],
    },
    "D5": {
        "id": "D5",
        "name": "Honeytoken",
        "category": "Breadcrumb Credential",
        "description": "Canary API keys, cloud access tokens, and fake session tokens injected into environment variables and configs.",
        "base_deployment_cost": 0.12,
        "base_detection_probability": 0.88,
        "base_attacker_engagement": 0.85,
        "base_expected_delay_min": 14.5,
        "base_containment_value": 0.72,
        "base_intelligence_value": 0.90,
        "base_operational_risk": 0.10,
        "targeted_attacks": ["CREDENTIAL_ATTACK", "PRIVILEGE_ESCALATION", "LATERAL_MOVEMENT"],
        "primary_states": ["S3", "S4", "S5"],
    },
    "D6": {
        "id": "D6",
        "name": "Decoy Credentials",
        "category": "Credential Decoy",
        "description": "Planted privileged account hashes in LSASS/memory or bash history enticing attackers down false escalation routes.",
        "base_deployment_cost": 0.16,
        "base_detection_probability": 0.87,
        "base_attacker_engagement": 0.84,
        "base_expected_delay_min": 15.0,
        "base_containment_value": 0.74,
        "base_intelligence_value": 0.84,
        "base_operational_risk": 0.14,
        "targeted_attacks": ["BRUTE_FORCE", "CREDENTIAL_ATTACK", "PRIVILEGE_ESCALATION"],
        "primary_states": ["S3", "S4"],
    },
    "D7": {
        "id": "D7",
        "name": "Decoy File / Resource",
        "category": "Content Decoy",
        "description": "Enticing fake documents (e.g. 'financial_audit_2026.xlsx', 'pki_backup.zip') embedded with beaconing tracking macros.",
        "base_deployment_cost": 0.15,
        "base_detection_probability": 0.91,
        "base_attacker_engagement": 0.89,
        "base_expected_delay_min": 19.0,
        "base_containment_value": 0.84,
        "base_intelligence_value": 0.88,
        "base_operational_risk": 0.12,
        "targeted_attacks": ["DATA_ACCESS", "EXFILTRATION"],
        "primary_states": ["S6", "S7"],
    },
}


class DeceptionSimulator:
    """
    Manages active deception assets and deployment validation.
    """

    def __init__(self):
        self.active_deceptions: List[Dict[str, Any]] = []

    def get_all_strategies(self) -> List[Dict[str, Any]]:
        """Return static registry of all 7 deception strategies."""
        return list(DECEPTION_STRATEGIES.values())

    def get_strategy(self, strategy_id: str) -> Dict[str, Any]:
        """Fetch strategy definition by ID (D1 - D7)."""
        return DECEPTION_STRATEGIES.get(strategy_id, DECEPTION_STRATEGIES["D1"])

    def deploy_deception(self, strategy_id: str, target_session_id: str) -> Dict[str, Any]:
        """
        Deploy simulated deception against an active attacker session.
        """
        strat = self.get_strategy(strategy_id)
        deployment_record = {
            "strategy_id": strat["id"],
            "strategy_name": strat["name"],
            "target_session_id": target_session_id,
            "status": "DEPLOYED",
            "message": f"Successfully initialized {strat['name']} in target subnet.",
            "operational_parameters": {
                "expected_delay_min": strat["base_expected_delay_min"],
                "engagement_rating": f"{int(strat['base_attacker_engagement'] * 100)}%",
                "intelligence_value": strat["base_intelligence_value"],
                "operational_cost": strat["base_deployment_cost"],
            },
        }
        self.active_deceptions.append(deployment_record)
        return deployment_record
