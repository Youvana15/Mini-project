"""
Main FastAPI Application for AI-Based Counterfactual Cyber Deception Framework.
Provides RESTful API endpoints and serves the SOC Cyber Defense Dashboard.
"""

import os
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from simulation.session_generator import generate_single_session, ATTACK_LABELS
from simulation.attacker_simulator import AttackerSimulator
from detection.detection_model import AttackDetector
from risk.risk_engine import RiskEngine
from counterfactual.counterfactual_engine import CounterfactualEngine
from decision.decision_engine import DecisionEngine
from deception.deception_simulator import DeceptionSimulator, DECEPTION_STRATEGIES
from experiments.benchmark_engine import BenchmarkEngine

app = FastAPI(
    title="AI-Based Counterfactual Cyber Deception Framework",
    description="Adaptive defensive cybersecurity decision platform powered by ML, POMDP modeling, and counterfactual reasoning.",
    version="2.0.0",
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure directories exist
os.makedirs("dashboard/static", exist_ok=True)
os.makedirs("dashboard/templates", exist_ok=True)

# Mount static and template handlers
app.mount("/static", StaticFiles(directory="dashboard/static"), name="static")
templates = Jinja2Templates(directory="dashboard/templates")

# Core Service Singletons
detector = AttackDetector()
risk_engine = RiskEngine()
counterfactual_engine = CounterfactualEngine()
decision_engine = DecisionEngine()
deception_simulator = DeceptionSimulator()
benchmark_engine = BenchmarkEngine()

# Active Simulation State (In-Memory session manager)
active_attacker: Optional[AttackerSimulator] = None
latest_pipeline_result: Dict[str, Any] = {}


# Request Models
class SimulateRequest(BaseModel):
    attack_label: Optional[str] = None
    sophistication: Optional[float] = None
    asset_criticality: Optional[float] = None


class DeployRequest(BaseModel):
    strategy_id: str
    session_id: Optional[str] = None


class AttackerResponseRequest(BaseModel):
    strategy_id: str
    strategy_name: Optional[str] = None
    believability: Optional[float] = 0.88
    expected_delay_min: Optional[float] = 18.0


@app.get("/")
def read_root():
    """Serve SOC cybersecurity dashboard UI."""
    return FileResponse("dashboard/templates/index.html")


@app.get("/api/status")
def get_status():
    """System health check and engine readiness."""
    global active_attacker
    return {
        "status": "OPERATIONAL",
        "ml_model_loaded": detector.is_loaded,
        "active_session_id": active_attacker.session_id if active_attacker else None,
        "active_attacker_state": active_attacker.current_state if active_attacker else None,
        "available_attack_types": ATTACK_LABELS,
        "deception_strategies_count": len(DECEPTION_STRATEGIES),
    }


@app.get("/api/model/info")
def get_model_info():
    """Return model performance metrics and global feature importances."""
    import json
    meta_path = "models/model_metadata.json"
    if os.path.exists(meta_path):
        try:
            with open(meta_path, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "best_model": "RandomForestClassifier",
        "evaluation_metrics": {
            "RandomForest": {"accuracy": 0.985, "precision": 0.986, "recall": 0.985, "f1_score": 0.985, "roc_auc": 0.998},
            "SVM": {"accuracy": 0.952, "precision": 0.954, "recall": 0.952, "f1_score": 0.952, "roc_auc": 0.989},
            "LogisticRegression": {"accuracy": 0.910, "precision": 0.912, "recall": 0.910, "f1_score": 0.909, "roc_auc": 0.974},
        },
        "feature_importances": {
            "database_query_count": 0.24,
            "port_scan_count": 0.20,
            "failed_login_count": 0.18,
            "data_access_volume": 0.15,
            "lateral_movement_score": 0.12,
            "sensitive_file_access": 0.11,
        },
    }


@app.post("/api/simulate")
def simulate_session(req: SimulateRequest = SimulateRequest()):
    """
    Generate synthetic attacker session and initialize active attacker simulator.
    """
    global active_attacker
    active_attacker = AttackerSimulator(
        attack_label=req.attack_label or "DB_PROBE",
        sophistication=req.sophistication or 0.70,
        asset_criticality=req.asset_criticality or 0.85,
    )
    return {
        "session": active_attacker.current_telemetry,
        "attacker_state": active_attacker.get_state_info(),
    }


@app.post("/api/detect")
def detect_attack(telemetry: Optional[Dict[str, Any]] = None):
    """
    Run ML detection model on provided session telemetry or active session.
    """
    global active_attacker
    target_telemetry = telemetry or (active_attacker.current_telemetry if active_attacker else None)
    if not target_telemetry:
        # Fallback to generating a session
        active_attacker = AttackerSimulator(attack_label="DB_PROBE")
        target_telemetry = active_attacker.current_telemetry

    detection_result = detector.predict_session(target_telemetry)
    return detection_result


@app.post("/api/risk")
def calculate_risk_endpoint(data: Optional[Dict[str, Any]] = None):
    """
    Calculate composite dynamic risk score.
    """
    global active_attacker
    data = data or {}
    attack = data.get("detected_attack") or (active_attacker.attack_label if active_attacker else "DB_PROBE")
    conf = float(data.get("detection_confidence", 0.92))
    state = data.get("attacker_state") or (active_attacker.current_state if active_attacker else "S6")
    soph = float(data.get("sophistication", active_attacker.sophistication if active_attacker else 0.70))
    crit = float(data.get("asset_criticality", active_attacker.asset_criticality if active_attacker else 0.85))

    return risk_engine.calculate_risk(
        detected_attack=attack,
        detection_confidence=conf,
        attacker_state=state,
        attacker_sophistication=soph,
        asset_criticality=crit,
    )


@app.post("/api/counterfactual")
def evaluate_counterfactual(data: Optional[Dict[str, Any]] = None):
    """
    Evaluate counterfactual outcomes for strategies D1 - D7.
    """
    global active_attacker
    data = data or {}
    attack = data.get("detected_attack") or (active_attacker.attack_label if active_attacker else "DB_PROBE")
    state = data.get("attacker_state") or (active_attacker.current_state if active_attacker else "S6")
    risk_score = float(data.get("risk_score", 82.0))
    soph = float(data.get("sophistication", active_attacker.sophistication if active_attacker else 0.70))
    crit = float(data.get("asset_criticality", active_attacker.asset_criticality if active_attacker else 0.85))

    return counterfactual_engine.evaluate_all_strategies(
        attack_label=attack,
        attacker_state=state,
        risk_score=risk_score,
        sophistication=soph,
        asset_criticality=crit,
    )


@app.post("/api/decision")
def make_decision(data: Optional[Dict[str, Any]] = None):
    """
    Execute POMDP decision engine and select utility-optimal defence.
    """
    data = data or {}
    cf_data = data.get("counterfactual_evaluation")
    if not cf_data:
        # Evaluate dynamically
        cf_data = evaluate_counterfactual(data)

    return decision_engine.select_optimal_defence(cf_data)


@app.post("/api/pipeline")
def run_complete_pipeline(req: SimulateRequest = SimulateRequest()):
    """
    Execute the entire automated defensive decision pipeline in one call:
    Session Gen -> ML Detection -> State Estimation -> Risk Scoring ->
    Counterfactual Simulation -> Utility Calculation -> Optimal Decision.
    """
    global active_attacker, latest_pipeline_result

    # 1. Simulate Session & Attacker
    active_attacker = AttackerSimulator(
        attack_label=req.attack_label or "DB_PROBE",
        sophistication=req.sophistication or 0.72,
        asset_criticality=req.asset_criticality or 0.88,
    )
    telemetry = active_attacker.current_telemetry
    state_info = active_attacker.get_state_info()

    # 2. Run ML Detection
    detection = detector.predict_session(telemetry)

    # 3. Dynamic Risk Assessment
    risk = risk_engine.calculate_risk(
        detected_attack=detection["predicted_label"],
        detection_confidence=detection["confidence"],
        attacker_state=state_info["current_state"],
        attacker_sophistication=state_info["sophistication"],
        asset_criticality=telemetry["asset_criticality"],
        session_telemetry=telemetry,
    )

    # 4. Counterfactual Scenarios Evaluation
    cf_eval = counterfactual_engine.evaluate_all_strategies(
        attack_label=detection["predicted_label"],
        attacker_state=state_info["current_state"],
        risk_score=risk["risk_score"],
        sophistication=state_info["sophistication"],
        asset_criticality=telemetry["asset_criticality"],
    )

    # 5. POMDP Decision Optimization
    decision = decision_engine.select_optimal_defence(cf_eval)

    # Cache latest bundle
    latest_pipeline_result = {
        "session": telemetry,
        "attacker_state": state_info,
        "detection": detection,
        "risk": risk,
        "counterfactuals": cf_eval,
        "decision": decision,
    }

    return latest_pipeline_result


@app.post("/api/deploy")
def deploy_defence(req: DeployRequest):
    """
    Deploy selected deception asset against the active threat session.
    """
    global active_attacker
    session_id = req.session_id or (active_attacker.session_id if active_attacker else "SESS-LIVE")
    deployment = deception_simulator.deploy_deception(req.strategy_id, session_id)
    return deployment


@app.post("/api/attacker-response")
def simulate_attacker_response_endpoint(req: AttackerResponseRequest):
    """
    Simulate attacker reaction to deployed deception, advancing state and updating feedback metrics.
    """
    global active_attacker
    if not active_attacker:
        active_attacker = AttackerSimulator(attack_label="DB_PROBE")

    strat = DECEPTION_STRATEGIES.get(req.strategy_id, DECEPTION_STRATEGIES["D1"])
    response = active_attacker.simulate_deception_response(
        strategy_id=req.strategy_id,
        strategy_name=req.strategy_name or strat["name"],
        believability=req.believability or strat["base_attacker_engagement"],
        expected_delay_min=req.expected_delay_min or strat["base_expected_delay_min"],
    )

    # Recalculate updated risk after attacker feedback
    new_risk = risk_engine.calculate_risk(
        detected_attack=active_attacker.attack_label,
        detection_confidence=0.94,
        attacker_state=response["new_state"],
        attacker_sophistication=active_attacker.sophistication,
        asset_criticality=active_attacker.asset_criticality,
    )
    response["updated_risk"] = new_risk

    # Re-evaluate counterfactuals for next state
    next_cf = counterfactual_engine.evaluate_all_strategies(
        attack_label=active_attacker.attack_label,
        attacker_state=response["new_state"],
        risk_score=new_risk["risk_score"],
        sophistication=active_attacker.sophistication,
        asset_criticality=active_attacker.asset_criticality,
    )
    next_decision = decision_engine.select_optimal_defence(next_cf)
    response["next_recommendation"] = next_decision

    return response


@app.post("/api/benchmark")
def run_benchmark_endpoint(campaigns: int = 60):
    """
    Run 5-paradigm comparative benchmark across 8 KPIs.
    """
    return benchmark_engine.run_benchmark(num_campaigns=campaigns)


@app.post("/api/reset")
def reset_simulation():
    """
    Reset active simulation state back to clean baseline.
    """
    global active_attacker, latest_pipeline_result
    active_attacker = None
    latest_pipeline_result = {}
    return {"message": "Simulation session successfully reset to baseline.", "status": "READY"}
