"""
Unit tests for FastAPI REST Endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_api_status():
    """Verify system health endpoint returns OPERATIONAL."""
    response = client.get("/api/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "OPERATIONAL"
    assert "available_attack_types" in data


def test_api_model_info():
    """Verify model info returns evaluation metrics."""
    response = client.get("/api/model/info")
    assert response.status_code == 200
    data = response.json()
    assert "evaluation_metrics" in data


def test_api_simulate_and_pipeline():
    """Verify end-to-end pipeline execution endpoint."""
    response = client.post("/api/pipeline", json={"attack_label": "DB_PROBE"})
    assert response.status_code == 200
    data = response.json()
    assert "session" in data
    assert "detection" in data
    assert "risk" in data
    assert "counterfactuals" in data
    assert "decision" in data
    assert data["decision"]["recommended_strategy_name"] != ""


def test_api_deploy_and_response():
    """Verify deployment and attacker feedback loop endpoints."""
    # Run pipeline first
    client.post("/api/pipeline", json={"attack_label": "BRUTE_FORCE"})

    # Deploy
    deploy_resp = client.post("/api/deploy", json={"strategy_id": "D2"})
    assert deploy_resp.status_code == 200
    assert deploy_resp.json()["status"] == "DEPLOYED"

    # Attacker response
    resp = client.post(
        "/api/attacker-response",
        json={"strategy_id": "D2", "strategy_name": "Fake Login Portal"},
    )
    assert resp.status_code == 200
    res_data = resp.json()
    assert "delay_minutes" in res_data
    assert "updated_risk" in res_data
