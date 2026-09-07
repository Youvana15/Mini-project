"""
Feature Engineering Module for Cyber Attack Telemetry.
Handles feature extraction, normalization, and encoding for ML model inference and training.
"""

from typing import Dict, List, Any, Tuple
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

FEATURE_COLUMNS = [
    "connection_count",
    "packets_per_second",
    "failed_login_count",
    "successful_login_count",
    "login_frequency",
    "port_scan_count",
    "command_frequency",
    "database_query_count",
    "sensitive_file_access",
    "privilege_escalation_attempt",
    "lateral_movement_score",
    "data_access_volume",
    "session_duration",
    "attacker_sophistication",
    "asset_criticality",
    "service_code",
]

SERVICE_MAPPING = {
    "HTTPS:443": 0,
    "SSH:22": 1,
    "MySQL:3306": 2,
    "RDP:3389": 3,
    "SMB:445": 4,
    "API:8080": 5,
    "DNS:53": 6,
    "PostgreSQL:5432": 7,
    "OTHER": 8,
}

LABEL_MAPPING = {
    "NORMAL": 0,
    "RECONNAISSANCE": 1,
    "BRUTE_FORCE": 2,
    "CREDENTIAL_ATTACK": 3,
    "DB_PROBE": 4,
    "PRIVILEGE_ESCALATION": 5,
    "LATERAL_MOVEMENT": 6,
    "DATA_ACCESS": 7,
    "EXFILTRATION": 8,
}

INVERSE_LABEL_MAPPING = {v: k for k, v in LABEL_MAPPING.items()}


def extract_features_from_dict(raw_session: Dict[str, Any]) -> np.ndarray:
    """
    Extract a single feature vector from raw session telemetry dictionary.
    """
    service_str = raw_session.get("destination_service", "OTHER")
    service_code = SERVICE_MAPPING.get(service_str, SERVICE_MAPPING["OTHER"])

    row = [
        float(raw_session.get("connection_count", 0)),
        float(raw_session.get("packets_per_second", 0.0)),
        float(raw_session.get("failed_login_count", 0)),
        float(raw_session.get("successful_login_count", 0)),
        float(raw_session.get("login_frequency", 0.0)),
        float(raw_session.get("port_scan_count", 0)),
        float(raw_session.get("command_frequency", 0.0)),
        float(raw_session.get("database_query_count", 0)),
        float(raw_session.get("sensitive_file_access", 0)),
        float(raw_session.get("privilege_escalation_attempt", 0)),
        float(raw_session.get("lateral_movement_score", 0.0)),
        float(raw_session.get("data_access_volume", 0.0)),
        float(raw_session.get("session_duration", 0.0)),
        float(raw_session.get("attacker_sophistication", 0.5)),
        float(raw_session.get("asset_criticality", 0.5)),
        float(service_code),
    ]
    return np.array(row, dtype=np.float32).reshape(1, -1)


def prepare_training_data(df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, StandardScaler]:
    """
    Extract features and labels from a pandas DataFrame, fit a StandardScaler, and return (X_scaled, y, scaler).
    """
    df = df.copy()
    df["service_code"] = df["destination_service"].apply(
        lambda s: SERVICE_MAPPING.get(s, SERVICE_MAPPING["OTHER"])
    )

    X_raw = df[FEATURE_COLUMNS].values.astype(np.float32)
    y = df["attack_label"].map(LABEL_MAPPING).values.astype(np.int64)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_raw)

    return X_scaled, y, scaler
