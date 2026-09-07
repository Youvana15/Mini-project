"""
One-Click Application Launcher.
Ensures synthetic dataset and trained ML models exist, then boots the FastAPI Uvicorn server.
"""

import os
import sys

def main():
    print("\n" + "=" * 80)
    print("AI-BASED COUNTERFACTUAL CYBER DECEPTION FRAMEWORK")
    print("Adaptive Cyber Defense & POMDP Decision Engine")
    print("=" * 80 + "\n")

    # 1. Check or Generate Dataset
    data_file = os.path.join("data", "attack_sessions.csv")
    if not os.path.exists(data_file):
        print("[1/3] Generating synthetic session records (6,000 samples)...")
        from simulation.session_generator import generate_dataset
        generate_dataset(num_samples=6000, output_path=data_file)
    else:
        print("[1/3] Found existing dataset at data/attack_sessions.csv.")

    # 2. Check or Train Models
    model_file = os.path.join("models", "detector.joblib")
    if not os.path.exists(model_file):
        print("[2/3] Training and benchmarking ML detection models...")
        from train_model import train_and_evaluate_models
        train_and_evaluate_models()
    else:
        print("[2/3] Pre-trained detector found at models/detector.joblib.")

    # 3. Launch Uvicorn Server
    print("[3/3] Starting FastAPI SOC Dashboard on http://127.0.0.1:8000 ...")
    print("Press Ctrl+C to terminate.")
    print("-" * 80)

    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()
