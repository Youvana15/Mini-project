"""
Unit tests for Synthetic Dataset and Session Generation.
"""

import pytest
import pandas as pd
from simulation.session_generator import (
    generate_single_session,
    generate_dataset,
    ATTACK_LABELS,
    ATTACK_STATES,
)


def test_single_session_generation():
    """Verify single session structure and mandatory features."""
    session = generate_single_session(attack_label="DB_PROBE")
    assert session["attack_label"] == "DB_PROBE"
    assert session["attack_stage"] == "S6"
    assert session["database_query_count"] > 20
    assert 0.0 <= session["attacker_sophistication"] <= 1.0
    assert 0.0 <= session["asset_criticality"] <= 1.0
    assert session["session_id"].startswith("SESS-")


def test_all_attack_labels_supported():
    """Verify all 9 attack labels produce valid states."""
    for label in ATTACK_LABELS:
        session = generate_single_session(attack_label=label)
        assert session["attack_label"] == label
        assert session["attack_stage"] in ATTACK_STATES.values()


def test_bulk_dataset_generation(tmp_path):
    """Verify dataset generation creates expected CSV file with all columns."""
    test_csv = str(tmp_path / "test_sessions.csv")
    df = generate_dataset(num_samples=100, output_path=test_csv, seed=123)
    assert len(df) == 100
    assert "attack_label" in df.columns
    assert "session_id" in df.columns
    assert df["attack_label"].nunique() > 5
