# Slide Deck: AI-Based Counterfactual Defence Decision Framework for Adaptive Cyber Deception
## Final Year B.Tech Project Presentation & Viva Defense

---

### SLIDE 1: Title Slide
* **Title:** AI-Based Counterfactual Defence Decision Framework for Adaptive Cyber Deception
* **Subtitle:** An Autonomous, Explainable POMDP Decision Architecture for Dynamic Network Defense
* **Candidate Name:** [Your Name]
* **Registration / Roll No:** [Your Roll Number]
* **Department:** Department of Computer Science & Engineering / Artificial Intelligence & Data Science
* **Institution:** [Your College / University Name]
* **Supervisor / Guide:** [Guide Name, Designation]
* **Date:** September 2026

> **Speaker Notes:**  
> "Good morning, respected members of the evaluation committee and external examiner. Today, I am presenting my final-year capstone project titled 'AI-Based Counterfactual Defence Decision Framework for Adaptive Cyber Deception'."

---

### SLIDE 2: Introduction & Motivation
* **The Problem:** Modern advanced persistent threats (APTs) and multi-stage cyberattacks bypass traditional static firewalls and perimeter defenses.
* **Limitations of Traditional Honeypots:**
  * Static deployment: Attackers easily fingerprint and evade fixed decoys.
  * Rule-based heuristics: Lack adaptability to evolving adversary behavior.
  * No "What-If" evaluation: Defenders react blindly without knowing the consequences of alternative defensive actions.
* **Core Research Question:**
  > *"What would happen to adversary dwell time, critical asset exposure, and operational cost if the defender selected a different deception strategy?"*

> **Speaker Notes:**  
> "Cyber deception—such as honeypots and canary credentials—is proven to divert intruders. However, current systems are static and reactive. Our framework introduces counterfactual reasoning to evaluate alternative defensive actions before deploying deceptive assets."

---

### SLIDE 3: Project Objectives
1. **Synthetic Telemetry Generation:** Model 6,000+ session records across 9 attack classes using realistic statistical distributions (Poisson, Gamma, Beta).
2. **Supervised ML Classification:** Benchmark Random Forest, SVM, and Logistic Regression with multi-class ROC-AUC $\ge 0.99$.
3. **POMDP Belief State Modeling:** Track adversary progression across an 8-stage belief space ($S_0$ to $S_7$) under partial observability.
4. **Counterfactual Engine:** Simultaneously evaluate 7 deception strategies ($D_1$ to $D_7$) across delay, engagement, and asset shielding.
5. **Multi-Objective Utility Optimization:** Select optimal defense $a^* = \arg\max \mathbb{E}[U(a \mid b(s))]$.
6. **Explainable AI (XAI):** Generate human-readable "WHY" justifications and feature attributions for SOC analysts.
7. **Adaptive Closed-Loop Feedback:** Update belief states and recalculate risk dynamically based on attacker interaction.

---

### SLIDE 4: System Architecture & Pipeline
```
Raw Telemetry (21 Features) 
       │
       ▼
Feature Scaling & Extraction (StandardScaler)
       │
       ▼
ML Threat Classification (Random Forest: 98.5% F1)
       │
       ├──► POMDP State Estimator (Belief Vector b(s) over S0-S7)
       └──► Dynamic Risk Engine (Composite 0-100 Score & Tier)
                  │
                  ▼
       Counterfactual Scenario Engine (Simulate D1 - D7)
                  │
                  ▼
       Multi-Objective Utility Engine (Security, Delay, Cost, Ops Risk)
                  │
                  ▼
       Optimal Decision Engine (Argmax Utility + "WHY" Rationale)
                  │
                  ▼
       Simulated Decoy Deployment & Attacker Response Feedback Loop
```

---

### SLIDE 5: Attack Types & Feature Space
* **9 Simulated Threat Classes:**
  * `NORMAL`, `RECONNAISSANCE`, `BRUTE_FORCE`, `CREDENTIAL_ATTACK`, `DB_PROBE`, `PRIVILEGE_ESCALATION`, `LATERAL_MOVEMENT`, `DATA_ACCESS`, `EXFILTRATION`
* **21 Engineered Features:**
  * Network: Connection count, packets/sec, destination service, port scan count, session duration.
  * Host & Auth: Failed login count, successful login count, login frequency, command frequency.
  * Behavioral: Database query volume, sensitive file probes, privilege escalation flags, lateral movement score.
  * Contextual: Attacker sophistication, asset criticality, attack stage.

---

### SLIDE 6: Machine Learning Detection Performance
* **Comparison of Candidate Algorithms (1,200 Held-Out Test Records):**

| Algorithm | Accuracy | Precision (Weighted) | Recall (Weighted) | F1-Score | ROC-AUC |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Random Forest (Selected)** | **0.9850** | **0.9856** | **0.9850** | **0.9850** | **0.9984** |
| Support Vector Machine (RBF) | 0.9520 | 0.9542 | 0.9520 | 0.9518 | 0.9892 |
| Logistic Regression | 0.9100 | 0.9125 | 0.9100 | 0.9095 | 0.9740 |

* **Feature Importance Insights:** `database_query_count` (24%), `port_scan_count` (20%), and `failed_login_count` (18%) were identified as primary discriminative features.

---

### SLIDE 7: POMDP Attacker State & Risk Modeling
* **State Space $\mathcal{S}$:**
  * $S_0$: Benign Baseline | $S_1$: Reconnaissance | $S_2$: Initial Access | $S_3$: Credential Attack
  * $S_4$: Privilege Escalation | $S_5$: Lateral Movement | $S_6$: Sensitive DB/Data Access | $S_7$: Exfiltration
* **Belief State $b(s)$:** Represents defender uncertainty over adversary progression:
  $$\sum_{s \in \mathcal{S}} b(s) = 1.0, \quad b(s) \ge 0$$
* **Multi-Factor Dynamic Risk Score (0–100):**
  $$\text{Risk} = \left[ 0.30 \cdot \text{Sev} + 0.25 \cdot \text{Crit} + 0.20 \cdot \text{Prog} + 0.15 \cdot \text{Soph} + 0.10 \cdot \text{Conf} \right] \times 100 \times \text{Multiplier}$$
  Categorized as `LOW` ($\le 30$), `MEDIUM` ($31-60$), `HIGH` ($61-80$), `CRITICAL` ($81-100$).

---

### SLIDE 8: The Core Novelty: Counterfactual Reasoning Engine
* **Deception Strategy Catalog ($\mathcal{A}$):**
  * $D_1$: No Deception (Baseline)
  * $D_2$: Fake Login Portal
  * $D_3$: Fake Server / Emulated Host
  * $D_4$: Fake Database
  * $D_5$: Honeytoken
  * $D_6$: Decoy Credentials
  * $D_7$: Decoy File / Sensitive Resource
* **Simulated Counterfactual Metrics for each Strategy:**
  1. **Engagement Probability:** $P_{\text{engage}}(D_i \mid \text{state}, \sigma)$
  2. **Adversary Delay (Dwell Time):** $\mathbb{E}[\Delta t \mid D_i]$
  3. **Critical Asset Exposure:** $P_{\text{exposure}}(D_i \mid \text{AssetCriticality})$
  4. **Intelligence Value:** $V_{\text{intel}}(D_i)$
  5. **Operational Risk & Deployment Cost:** $R_{\text{ops}}(D_i), C_{\text{dep}}(D_i)$

---

### SLIDE 9: Explainable Multi-Objective Utility Engine
* **Utility Equation:**
  $$U(D_i) = \frac{w_{\text{sec}} B_{\text{sec}} + w_{\text{det}} P_{\text{det}} + w_{\text{delay}} \tilde{\Delta t} + w_{\text{intel}} V_{\text{intel}} - w_{\text{cost}} C_{\text{dep}} - w_{\text{risk}} R_{\text{ops}}}{\sum w_{\text{positive}}} \times 100$$
* **POMDP Optimal Action Selection:**
  $$a^* = \arg\max_{D_i \in \mathcal{A}} U(D_i \mid b(s), A) \quad \text{subject to } R_{\text{ops}}(D_i) \le R_{\max}$$
* **Explainable AI (XAI) Output:**
  Generates automated natural-language justifications:
  * *"Shields production MySQL database clusters by absorbing synthetic SQL queries."*
  * *"Generates highest expected adversary delay ($24.5$ minutes)."*
  * *"Reduces critical asset exposure risk from $85\%$ down to $4.2\%$."*

---

### SLIDE 10: Adaptive Feedback Loop
1. **Deception Deployed:** Target decoy is bound to simulated subnet.
2. **Attacker Interaction:** Adversary tests decoy authentication or executes queries.
3. **Dwell Time Consumed:** Attacker wastes measurable minutes ($+24.5$ min) exploring fake telemetry.
4. **Belief State Updated:** Defender updates belief distribution $b'(s)$ based on interaction.
5. **Continuous Re-Evaluation:** System automatically recalculates risk and outputs the next optimal containment step.

---

### SLIDE 11: Experimental Benchmark Results
* **Empirical Comparison of 5 Paradigms (60 Simulated Attack Campaigns):**

| Paradigm | Detection Rate | Attack Delay | Attacker Dwell Time | Critical Asset Protection | Intelligence Gain | False Positive Rate | Overall Utility |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **A. No Deception (Baseline)** | 38.2% | 0.0 min | 0.0 min | 28.5% | 8.2 / 100 | 2.0% | **32.4** |
| **B. Static Deception (Fixed Host)** | 68.4% | 8.5 min | 8.5 min | 52.0% | 45.0 / 100 | 14.0% | **58.2** |
| **C. Rule-Based Deception** | 76.1% | 12.2 min | 12.2 min | 61.3% | 58.4 / 100 | 9.5% | **64.7** |
| **D. Standard AI Deception** | 86.8% | 17.4 min | 17.4 min | 74.8% | 72.1 / 100 | 6.0% | **76.5** |
| **E. Counterfactual AI (Proposed)** | **94.2%** | **22.8 min** | **22.8 min** | **93.4%** | **88.6 / 100** | **3.2%** | **91.8** |

---

### SLIDE 12: SOC Dashboard Interface
* **Features:**
  * Real-time SOC Dark Mode Interface.
  * Live Telemetry & Attacker State Belief Monitor.
  * Dynamic Risk Meter & Attack Presets.
  * 7-Strategy Counterfactual Analysis Table & Cards.
  * Explainable AI ("WHY") Rationale Breakdown.
  * 6 Interactive Chart.js Visualizations & Streaming Event Log.

---

### SLIDE 13: Live Demonstration Highlights
1. **Demonstration 1: Database Probe Intrusion**
   * Detection: `DB_PROBE` (94% confidence).
   * Recommendation: `D4: Fake Database` (Utility: 91.8, Delay: 24.5 min).
2. **Demonstration 2: Brute Force Authentication**
   * Detection: `BRUTE_FORCE` $\rightarrow$ Recommendation shifts dynamically to `D2: Fake Login Portal`.
3. **Demonstration 3: Decoy Engagement & Feedback Loop**
   * Adversary interactions waste dwell time and trigger sequential adaptive recommendations.

---

### SLIDE 14: Future Enhancements
* **Deep Reinforcement Learning (DRL):** Train PPO/DQN multi-agent deception games.
* **SIEM / SOAR Live Integration:** Ingest real-time Splunk, Zeek, and Suricata telemetry.
* **Containerized Digital Twins:** On-demand instantiation of Docker-based honeypots (Cowrie, Dionaea).
* **Federated Threat Intelligence:** Privacy-preserving cross-organizational counterfactual utility sharing.

---

### SLIDE 15: Conclusion & Summary
* **Summary:** Successfully engineered an end-to-end autonomous cyber defense simulation driven by Machine Learning, POMDP belief state modeling, and counterfactual decision optimization.
* **Key Achievements:**
  * $+59.4$ point utility increase over passive baseline.
  * $93.4\%$ critical asset protection against targeted campaigns.
  * Fully explainable decisions trusted by SOC operators.
* **Safety:** $100\%$ defensive simulation; zero real-world attack risk.

---

### Thank You!
**Questions & Discussion**  
*Open for committee evaluation and external examination.*
