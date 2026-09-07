"""
Synthetic Session Generator for Cyber Deception Simulation.
Generates realistic network telemetry and host-activity features based on statistical distributions.
"""

import os
import random
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any
import numpy as np
import pandas as pd

# Define Attack Labels
ATTACK_LABELS = [
    "NORMAL",
    "RECONNAISSANCE",
    "BRUTE_FORCE",
    "CREDENTIAL_ATTACK",
    "DB_PROBE",
    "PRIVILEGE_ESCALATION",
    "LATERAL_MOVEMENT",
    "DATA_ACCESS",
    "EXFILTRATION",
]

# Attacker State Mapping
ATTACK_STATES = {
    "NORMAL": "S0",
    "RECONNAISSANCE": "S1",
    "BRUTE_FORCE": "S2",
    "CREDENTIAL_ATTACK": "S3",
    "PRIVILEGE_ESCALATION": "S4",
    "LATERAL_MOVEMENT": "S5",
    "DB_PROBE": "S6",
    "DATA_ACCESS": "S6",
    "EXFILTRATION": "S7",
}

STATE_DESCRIPTIONS = {
    "S0": "Unknown / Benign Baseline",
    "S1": "Reconnaissance & Scanning",
    "S2": "Initial Access / Infiltration",
    "S3": "Credential Attack & Harvesting",
    "S4": "Privilege Escalation",
    "S5": "Lateral Movement & Spreading",
    "S6": "Sensitive Data / DB Probing",
    "S7": "Exfiltration & Egress Attempt",
}

SERVICES = [
    "HTTPS:443",
    "SSH:22",
    "MySQL:3306",
    "RDP:3389",
    "SMB:445",
    "API:8080",
    "DNS:53",
    "PostgreSQL:5432",
]


def generate_single_session(
    attack_label: str = None,
    sophistication: float = None,
    asset_criticality: float = None,
) -> Dict[str, Any]:
    """
    Generate a single synthetic session record using realistic statistical distributions.
    """
    if attack_label is None or attack_label not in ATTACK_LABELS:
        attack_label = random.choices(
            ATTACK_LABELS,
            weights=[0.35, 0.12, 0.10, 0.08, 0.09, 0.07, 0.07, 0.06, 0.06],
            k=1,
        )[0]

    if sophistication is None:
        if attack_label == "NORMAL":
            sophistication = round(float(np.random.beta(2, 5)), 2)
        elif attack_label in ["RECONNAISSANCE", "BRUTE_FORCE"]:
            sophistication = round(float(np.random.beta(3, 4)), 2)
        elif attack_label in ["CREDENTIAL_ATTACK", "DB_PROBE"]:
            sophistication = round(float(np.random.beta(4, 3)), 2)
        else:
            sophistication = round(float(np.random.beta(5, 2)), 2)

    sophistication = max(0.05, min(1.0, sophistication))

    if asset_criticality is None:
        if attack_label in ["NORMAL", "RECONNAISSANCE"]:
            asset_criticality = round(float(np.random.uniform(0.1, 0.5)), 2)
        elif attack_label in ["DB_PROBE", "DATA_ACCESS", "EXFILTRATION"]:
            asset_criticality = round(float(np.random.uniform(0.7, 1.0)), 2)
        else:
            asset_criticality = round(float(np.random.uniform(0.4, 0.85)), 2)

    session_id = f"SESS-{uuid.uuid4().hex[:8].upper()}"
    timestamp = (
        datetime.utcnow() - timedelta(minutes=random.randint(1, 1440))
    ).isoformat() + "Z"

    if attack_label == "NORMAL":
        source_ip = f"192.168.1.{random.randint(10, 250)}"
        dest_service = random.choice(["HTTPS:443", "DNS:53", "API:8080"])
        connection_count = int(np.random.poisson(lam=12)) + 1
        packets_per_sec = round(float(np.random.gamma(shape=2.0, scale=8.0)), 2)
        failed_login_count = int(np.random.choice([0, 0, 0, 1, 2], p=[0.8, 0.1, 0.05, 0.03, 0.02]))
        successful_login_count = int(np.random.choice([1, 2, 3], p=[0.7, 0.25, 0.05]))
        login_freq = round(failed_login_count / max(1, random.uniform(1.0, 10.0)), 2)
        port_scan_count = 0
        cmd_freq = round(float(np.random.exponential(scale=1.5)), 2)
        db_queries = int(np.random.poisson(lam=5))
        sensitive_files = 0
        priv_esc = 0
        lateral_score = round(float(np.random.beta(1.5, 10.0)), 3)
        data_vol_mb = round(float(np.random.gamma(shape=1.5, scale=4.0)), 2)
        duration_sec = round(float(np.random.uniform(30.0, 900.0)), 1)
        det_conf = round(float(np.random.uniform(0.01, 0.15)), 2)

    elif attack_label == "RECONNAISSANCE":
        source_ip = f"{random.randint(45, 198)}.{random.randint(10, 200)}.{random.randint(1, 254)}.{random.randint(1, 254)}"
        dest_service = random.choice(["HTTPS:443", "SSH:22", "RDP:3389", "API:8080"])
        connection_count = int(np.random.poisson(lam=85)) + 20
        packets_per_sec = round(float(np.random.gamma(shape=4.0, scale=35.0)), 2)
        failed_login_count = int(np.random.choice([0, 1, 2, 3], p=[0.6, 0.25, 0.1, 0.05]))
        successful_login_count = 0
        login_freq = round(failed_login_count / max(1, random.uniform(1.0, 5.0)), 2)
        port_scan_count = int(np.random.poisson(lam=120)) + 30
        cmd_freq = round(float(np.random.exponential(scale=2.0)), 2)
        db_queries = 0
        sensitive_files = 0
        priv_esc = 0
        lateral_score = round(float(np.random.beta(2.0, 6.0)), 3)
        data_vol_mb = round(float(np.random.uniform(0.5, 8.0)), 2)
        duration_sec = round(float(np.random.uniform(15.0, 300.0)), 1)
        det_conf = round(float(np.random.uniform(0.70, 0.95)), 2)

    elif attack_label == "BRUTE_FORCE":
        source_ip = f"{random.randint(50, 210)}.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}"
        dest_service = random.choice(["SSH:22", "RDP:3389", "HTTPS:443"])
        connection_count = int(np.random.poisson(lam=95)) + 40
        packets_per_sec = round(float(np.random.gamma(shape=3.0, scale=25.0)), 2)
        failed_login_count = int(np.random.poisson(lam=80)) + 25
        successful_login_count = int(np.random.choice([0, 1], p=[0.9, 0.1]))
        login_freq = round(float(np.random.gamma(shape=5.0, scale=8.0)), 2)
        port_scan_count = int(np.random.choice([0, 1, 3], p=[0.7, 0.2, 0.1]))
        cmd_freq = round(float(np.random.exponential(scale=1.0)), 2)
        db_queries = 0
        sensitive_files = 0
        priv_esc = 0
        lateral_score = round(float(np.random.beta(1.5, 8.0)), 3)
        data_vol_mb = round(float(np.random.uniform(1.0, 12.0)), 2)
        duration_sec = round(float(np.random.uniform(60.0, 600.0)), 1)
        det_conf = round(float(np.random.uniform(0.78, 0.98)), 2)

    elif attack_label == "CREDENTIAL_ATTACK":
        source_ip = f"{random.randint(60, 220)}.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}"
        dest_service = random.choice(["HTTPS:443", "API:8080", "SSH:22"])
        connection_count = int(np.random.poisson(lam=50)) + 15
        packets_per_sec = round(float(np.random.gamma(shape=2.5, scale=18.0)), 2)
        failed_login_count = int(np.random.poisson(lam=30)) + 10
        successful_login_count = int(np.random.choice([1, 2, 3], p=[0.6, 0.3, 0.1]))
        login_freq = round(float(np.random.gamma(shape=3.5, scale=5.0)), 2)
        port_scan_count = 0
        cmd_freq = round(float(np.random.exponential(scale=3.0)), 2)
        db_queries = int(np.random.choice([0, 2, 5], p=[0.7, 0.2, 0.1]))
        sensitive_files = int(np.random.choice([0, 1, 2], p=[0.6, 0.3, 0.1]))
        priv_esc = 0
        lateral_score = round(float(np.random.beta(2.5, 5.0)), 3)
        data_vol_mb = round(float(np.random.uniform(2.0, 25.0)), 2)
        duration_sec = round(float(np.random.uniform(80.0, 800.0)), 1)
        det_conf = round(float(np.random.uniform(0.75, 0.96)), 2)

    elif attack_label == "DB_PROBE":
        source_ip = f"10.0.{random.randint(1, 10)}.{random.randint(10, 250)}"
        dest_service = random.choice(["MySQL:3306", "PostgreSQL:5432", "API:8080"])
        connection_count = int(np.random.poisson(lam=65)) + 20
        packets_per_sec = round(float(np.random.gamma(shape=3.0, scale=20.0)), 2)
        failed_login_count = int(np.random.choice([0, 1, 2, 4], p=[0.5, 0.3, 0.15, 0.05]))
        successful_login_count = 1
        login_freq = round(failed_login_count / 2.0, 2)
        port_scan_count = 0
        cmd_freq = round(float(np.random.gamma(shape=4.0, scale=3.0)), 2)
        db_queries = int(np.random.poisson(lam=180)) + 40
        sensitive_files = int(np.random.poisson(lam=8)) + 1
        priv_esc = int(np.random.choice([0, 1], p=[0.8, 0.2]))
        lateral_score = round(float(np.random.beta(2.0, 5.0)), 3)
        data_vol_mb = round(float(np.random.gamma(shape=2.5, scale=20.0)), 2)
        duration_sec = round(float(np.random.uniform(120.0, 1200.0)), 1)
        det_conf = round(float(np.random.uniform(0.80, 0.97)), 2)

    elif attack_label == "PRIVILEGE_ESCALATION":
        source_ip = f"10.0.{random.randint(1, 5)}.{random.randint(20, 200)}"
        dest_service = random.choice(["SSH:22", "RDP:3389", "API:8080"])
        connection_count = int(np.random.poisson(lam=40)) + 10
        packets_per_sec = round(float(np.random.gamma(shape=2.0, scale=12.0)), 2)
        failed_login_count = int(np.random.choice([1, 2, 3, 5], p=[0.4, 0.3, 0.2, 0.1]))
        successful_login_count = 1
        login_freq = round(float(np.random.uniform(0.5, 4.0)), 2)
        port_scan_count = 0
        cmd_freq = round(float(np.random.gamma(shape=6.0, scale=5.0)), 2)
        db_queries = int(np.random.choice([0, 3, 8], p=[0.6, 0.3, 0.1]))
        sensitive_files = int(np.random.poisson(lam=12)) + 3
        priv_esc = int(np.random.poisson(lam=3)) + 1
        lateral_score = round(float(np.random.beta(3.0, 4.0)), 3)
        data_vol_mb = round(float(np.random.uniform(5.0, 40.0)), 2)
        duration_sec = round(float(np.random.uniform(100.0, 900.0)), 1)
        det_conf = round(float(np.random.uniform(0.82, 0.98)), 2)

    elif attack_label == "LATERAL_MOVEMENT":
        source_ip = f"10.0.{random.randint(1, 5)}.{random.randint(10, 100)}"
        dest_service = random.choice(["SMB:445", "RDP:3389", "SSH:22"])
        connection_count = int(np.random.poisson(lam=110)) + 30
        packets_per_sec = round(float(np.random.gamma(shape=4.0, scale=28.0)), 2)
        failed_login_count = int(np.random.choice([2, 4, 8, 15], p=[0.3, 0.4, 0.2, 0.1]))
        successful_login_count = int(np.random.choice([1, 2, 4], p=[0.5, 0.35, 0.15]))
        login_freq = round(float(np.random.uniform(2.0, 8.0)), 2)
        port_scan_count = int(np.random.poisson(lam=35)) + 10
        cmd_freq = round(float(np.random.gamma(shape=4.0, scale=4.0)), 2)
        db_queries = int(np.random.choice([0, 5, 12], p=[0.5, 0.3, 0.2]))
        sensitive_files = int(np.random.poisson(lam=10)) + 2
        priv_esc = int(np.random.choice([0, 1, 2], p=[0.5, 0.35, 0.15]))
        lateral_score = round(float(np.random.uniform(0.72, 0.98)), 3)
        data_vol_mb = round(float(np.random.gamma(shape=3.0, scale=30.0)), 2)
        duration_sec = round(float(np.random.uniform(150.0, 1500.0)), 1)
        det_conf = round(float(np.random.uniform(0.81, 0.98)), 2)

    elif attack_label == "DATA_ACCESS":
        source_ip = f"10.0.{random.randint(1, 10)}.{random.randint(50, 220)}"
        dest_service = random.choice(["MySQL:3306", "PostgreSQL:5432", "API:8080", "SMB:445"])
        connection_count = int(np.random.poisson(lam=80)) + 20
        packets_per_sec = round(float(np.random.gamma(shape=3.5, scale=22.0)), 2)
        failed_login_count = int(np.random.choice([0, 1], p=[0.8, 0.2]))
        successful_login_count = 1
        login_freq = 0.5
        port_scan_count = 0
        cmd_freq = round(float(np.random.gamma(shape=3.0, scale=3.5)), 2)
        db_queries = int(np.random.poisson(lam=220)) + 60
        sensitive_files = int(np.random.poisson(lam=35)) + 15
        priv_esc = 0
        lateral_score = round(float(np.random.beta(2.5, 4.5)), 3)
        data_vol_mb = round(float(np.random.gamma(shape=4.0, scale=60.0)), 2)
        duration_sec = round(float(np.random.uniform(200.0, 2400.0)), 1)
        det_conf = round(float(np.random.uniform(0.83, 0.98)), 2)

    else:  # EXFILTRATION
        source_ip = f"10.0.{random.randint(1, 5)}.{random.randint(10, 80)}"
        dest_service = random.choice(["HTTPS:443", "DNS:53", "SSH:22"])
        connection_count = int(np.random.poisson(lam=140)) + 40
        packets_per_sec = round(float(np.random.gamma(shape=6.0, scale=45.0)), 2)
        failed_login_count = 0
        successful_login_count = 1
        login_freq = 0.2
        port_scan_count = 0
        cmd_freq = round(float(np.random.gamma(shape=5.0, scale=4.0)), 2)
        db_queries = int(np.random.poisson(lam=80)) + 10
        sensitive_files = int(np.random.poisson(lam=45)) + 20
        priv_esc = 0
        lateral_score = round(float(np.random.beta(3.0, 4.0)), 3)
        data_vol_mb = round(float(np.random.gamma(shape=6.0, scale=250.0)) + 350.0, 2)
        duration_sec = round(float(np.random.uniform(400.0, 3600.0)), 1)
        det_conf = round(float(np.random.uniform(0.88, 0.99)), 2)

    attack_stage = ATTACK_STATES[attack_label]

    return {
        "session_id": session_id,
        "timestamp": timestamp,
        "source_ip": source_ip,
        "destination_service": dest_service,
        "connection_count": connection_count,
        "packets_per_second": packets_per_sec,
        "failed_login_count": failed_login_count,
        "successful_login_count": successful_login_count,
        "login_frequency": login_freq,
        "port_scan_count": port_scan_count,
        "command_frequency": cmd_freq,
        "database_query_count": db_queries,
        "sensitive_file_access": sensitive_files,
        "privilege_escalation_attempt": priv_esc,
        "lateral_movement_score": lateral_score,
        "data_access_volume": data_vol_mb,
        "session_duration": duration_sec,
        "attacker_sophistication": sophistication,
        "attack_stage": attack_stage,
        "asset_criticality": asset_criticality,
        "detection_confidence": det_conf,
        "attack_label": attack_label,
    }


def generate_dataset(
    num_samples: int = 6000,
    output_path: str = "data/attack_sessions.csv",
    seed: int = 42,
) -> pd.DataFrame:
    """
    Generate bulk synthetic dataset of session records and save to CSV.
    """
    np.random.seed(seed)
    random.seed(seed)

    records = []
    # Balance across categories
    weights = [0.28, 0.11, 0.10, 0.09, 0.09, 0.08, 0.09, 0.08, 0.08]
    counts = np.random.multinomial(num_samples, weights)

    for label, count in zip(ATTACK_LABELS, counts):
        for _ in range(count):
            records.append(generate_single_session(attack_label=label))

    random.shuffle(records)
    df = pd.DataFrame(records)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} synthetic session records at {output_path}")
    return df


if __name__ == "__main__":
    generate_dataset(num_samples=6000)
