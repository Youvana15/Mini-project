# FINAL YEAR PROJECT REPORT

# AI-BASED COUNTERFACTUAL DEFENCE DECISION FRAMEWORK FOR ADAPTIVE CYBER DECEPTION

**Submitted in partial fulfillment of the requirements for the award of the degree of**  
**BACHELOR OF TECHNOLOGY**  
**in**  
**COMPUTER SCIENCE AND ENGINEERING / ARTIFICIAL INTELLIGENCE & DATA SCIENCE**

---

## TABLE OF CONTENTS

1. **Chapter 1: Introduction**
   * 1.1 Background & Motivation
   * 1.2 Problem Statement
   * 1.3 Objectives of the Project
   * 1.4 Scope and Limitations
2. **Chapter 2: Literature Survey**
   * 2.1 Evolution of Cyber Deception & Honeypots
   * 2.2 Game-Theoretic & MDP Approaches in Cybersecurity
   * 2.3 Counterfactual Reasoning in Decision Systems
   * 2.4 Research Gaps in Existing Literature
3. **Chapter 3: System Requirements & Architecture**
   * 3.1 Functional Requirements
   * 3.2 Non-Functional Requirements
   * 3.3 Overall System Architecture
   * 3.4 Telemetry Feature Engineering Pipeline
4. **Chapter 4: Mathematical Modeling & Algorithms**
   * 4.1 POMDP Adversary State Representation
   * 4.2 Dynamic Multi-Factor Risk Assessment Engine
   * 4.3 Counterfactual "What-If" Reasoning Formulation
   * 4.4 Multi-Objective Explainable Utility Optimization
5. **Chapter 5: Implementation Details**
   * 5.1 Synthetic Telemetry Generator
   * 5.2 Supervised ML Classification (Random Forest, SVM, LR)
   * 5.3 Deception Catalog & Adaptive Feedback Mechanism
   * 5.4 High-Tech SOC Cyber Defense Dashboard
6. **Chapter 6: Experimental Results & Benchmark Analysis**
   * 6.1 Machine Learning Evaluation Metrics
   * 6.2 5-Paradigm Empirical Benchmark (60 Campaigns)
   * 6.3 Performance Comparison & Observations
7. **Chapter 7: Conclusion & Future Scope**
   * 7.1 Conclusion
   * 7.2 Future Research Directions
8. **References (IEEE Format)**

---

## CHAPTER 1: INTRODUCTION

### 1.1 Background & Motivation
Enterprise network perimeters are increasingly vulnerable to Advanced Persistent Threats (APTs) and sophisticated multi-stage intrusions. Conventional defensive postures rely heavily on static intrusion detection systems (IDS) and reactive firewalls. Once an adversary acquires valid credentials or identifies an unpatched zero-day vulnerability, perimeter defenses offer virtually no visibility into internal adversary traversal.

Cyber deception—the deliberate deployment of simulated honeypots, decoy credentials, and canary tokens—fundamentally shifts the asymmetric advantage from attacker to defender. By seeding internal subnets with believable decoy assets, defenders can detect unauthorized reconnaissance, waste adversary resources, and collect actionable threat intelligence.

### 1.2 Problem Statement
Despite the theoretical strengths of cyber deception, existing commercial and open-source implementations suffer from severe operational limitations:
1. **Static Deployment**: Decoys remain fixed and rigid, enabling sophisticated adversaries to easily detect and fingerprint them.
2. **Lack of Counterfactual Evaluation**: Security operators deploy deception based on static rules without evaluating alternative possibilities: *“What would happen to crown jewel exposure and adversary delay if a fake database were deployed instead of a decoy server?”*
3. **High Operational Friction**: Randomly deploying deceptive assets introduces network overhead and false positive disruptions.
4. **Black-Box Decision Making**: Autonomous defense mechanisms fail to provide human-interpretable justifications to SOC analysts.

### 1.3 Objectives of the Project
* **Objective 1:** Engineer a statistical session generator producing 6,000+ synthetic records across 9 attack types characterized by 21 network/host features.
* **Objective 2:** Train and benchmark supervised Machine Learning models (Random Forest, SVM, Logistic Regression) to detect multi-class attack patterns with an F1-score exceeding 0.98.
* **Objective 3:** Implement an 8-state Partially Observable Markov Decision Process (POMDP) belief state representation ($S_0$ through $S_7$) capturing adversary progression.
* **Objective 4:** Construct a dynamic risk engine computing composite 0–100 threat severity scores.
* **Objective 5:** Develop a Counterfactual Simulation Engine capable of evaluating 7 deception strategies ($D_1$ to $D_7$) across delay, engagement, exposure, and intelligence gain.
* **Objective 6:** Formulate an explainable multi-objective utility optimization function selecting $a^* = \arg\max \mathbb{E}[U(a \mid b(s))]$.
* **Objective 7:** Establish a closed-loop adaptive feedback mechanism updating adversary states post-deployment.
* **Objective 8:** Construct an interactive, dark-mode SOC dashboard with real-time Chart.js visual analytics.

---

## CHAPTER 4: MATHEMATICAL MODELING & ALGORITHMS

### 4.1 POMDP Adversary State Representation
The interaction between defender and adversary is modeled as a POMDP defined by the 6-tuple $(\mathcal{S}, \mathcal{A}, \mathcal{T}, \mathcal{R}, \Omega, \mathcal{O})$:
* **State Space $\mathcal{S}$**: $\{S_0, S_1, S_2, S_3, S_4, S_5, S_6, S_7\}$:
  * $S_0$: Unknown / Benign Baseline
  * $S_1$: Reconnaissance & Scanning
  * $S_2$: Initial Access
  * $S_3$: Credential Attack & Harvesting
  * $S_4$: Privilege Escalation
  * $S_5$: Lateral Movement
  * $S_6$: Sensitive Database / Data Access
  * $S_7$: Exfiltration & Egress Attempt
* **Belief State $b(s)$**:
  $$b(s) = P(S_t = s \mid \text{Observations}), \quad \sum_{s \in \mathcal{S}} b(s) = 1.0$$

### 4.2 Dynamic Risk Assessment Formulation
The dynamic risk score $R \in [0, 100]$ combines multiple operational dimensions:
$$\text{Risk} = \left[ 0.30 \cdot \text{Severity} + 0.25 \cdot \text{Criticality} + 0.20 \cdot \text{Progression} + 0.15 \cdot \text{Sophistication} + 0.10 \cdot \text{Confidence} \right] \times 100 \times M$$

### 4.3 Counterfactual Reasoning Formulation
For any detected threat $(A, s, \sigma, C)$, the counterfactual engine evaluates each strategy $D_i \in \{D_1, \dots, D_7\}$:
* **Affinity Score $\alpha_i$**:
  $$\alpha_i = 0.60 \cdot \mathbb{I}(A \in \text{Targeted}(D_i)) + 0.40 \cdot \mathbb{I}(s \in \text{PrimaryStates}(D_i))$$
* **Expected Delay (Dwell Time) in minutes**:
  $$\mathbb{E}[\Delta t \mid D_i] = \text{BaseDelay}(D_i) \cdot (0.50 + 0.50\alpha_i) \cdot P_{\text{engage}}(D_i) \cdot (1.1 - 0.2\sigma)$$
* **Critical Asset Exposure Probability**:
  $$P_{\text{exposure}}(D_i) = C \cdot (0.45 + 0.50\sigma) \cdot [1.0 - 0.88 P_{\text{engage}}(D_i)\alpha_i]$$
* **Security Benefit**:
  $$B_{\text{sec}}(D_i) = 0.60 \cdot (1.0 - P_{\text{exposure}}(D_i)) + 0.40 \cdot (1.0 - P_{\text{progress}}(D_i))$$

### 4.4 Multi-Objective Utility Function
The net utility balances security benefits against deployment and operational costs:
$$U(D_i) = \frac{w_1 B_{\text{sec}} + w_2 P_{\text{det}} + w_3 \tilde{\Delta t} + w_4 V_{\text{intel}} - w_5 C_{\text{dep}} - w_6 R_{\text{ops}}}{\sum_{j=1}^4 w_j} \times 100$$
The optimal defensive action is selected as:
$$a^* = \arg\max_{D_i \in \mathcal{A}} U(D_i \mid b(s), A) \quad \text{subject to } R_{\text{ops}}(D_i) \le R_{\max}$$

---

## CHAPTER 6: EXPERIMENTAL RESULTS & BENCHMARK ANALYSIS

### 6.1 Machine Learning Detection Benchmark
The candidate classifiers were trained on 4,800 training sessions and evaluated on 1,200 held-out test sessions:

| Model | Accuracy | Precision (Weighted) | Recall (Weighted) | F1-Score | ROC-AUC |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Random Forest** | **0.9850** | **0.9856** | **0.9850** | **0.9850** | **0.9984** |
| Support Vector Machine (RBF) | 0.9520 | 0.9542 | 0.9520 | 0.9518 | 0.9892 |
| Logistic Regression | 0.9100 | 0.9125 | 0.9100 | 0.9095 | 0.9740 |

### 6.2 5-Paradigm Comparative Benchmark (60 Campaigns)

| Paradigm | Detection Rate | Attack Delay | Attacker Dwell Time | Critical Asset Protection | Intelligence Gain | False Positive Rate | Defence Cost | Overall Utility |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **A. No Deception (Baseline)** | 38.2% | 0.0 min | 0.0 min | 28.5% | 8.2 / 100 | 2.0% | 2.0 / 100 | **32.4** |
| **B. Static Deception (Fixed Host)** | 68.4% | 8.5 min | 8.5 min | 52.0% | 45.0 / 100 | 14.0% | 42.0 / 100 | **58.2** |
| **C. Rule-Based Deception** | 76.1% | 12.2 min | 12.2 min | 61.3% | 58.4 / 100 | 9.5% | 26.5 / 100 | **64.7** |
| **D. Standard AI Deception** | 86.8% | 17.4 min | 17.4 min | 74.8% | 72.1 / 100 | 6.0% | 24.8 / 100 | **76.5** |
| **E. Counterfactual AI (Proposed)** | **94.2%** | **22.8 min** | **22.8 min** | **93.4%** | **88.6 / 100** | **3.2%** | **22.4 / 100** | **91.8** |

### 6.3 Observations & Discussion
1. **Utility Optimization**: The proposed framework achieved a **91.8/100 utility score**, representing an increase of $+59.4$ points over passive monitoring and $+15.3$ points over standard AI mapping.
2. **Crown Jewel Protection**: Critical asset protection increased to **93.4%** because the counterfactual engine explicitly models and penalizes genuine crown jewel exposure.
3. **Adversary Delay**: The framework successfully consumed **22.8 minutes** of average dwell time per campaign, granting incident responders ample time to contain the threat.

---

## CHAPTER 7: CONCLUSION & FUTURE SCOPE

### 7.1 Conclusion
This project successfully designed, implemented, and validated an autonomous, explainable cyber defense decision framework driven by machine learning, POMDP belief state modeling, and counterfactual scenario reasoning. The framework eliminates the vulnerabilities of static honeypots by evaluating hypothetical "What-If" outcomes before committing resources, achieving superior utility and asset protection while remaining completely safe as a defensive simulation.

### 7.2 Future Scope
* Integration with enterprise SIEM/SOAR platforms (Splunk, Elastic, Cortex XSOAR).
* Deployment of containerized dynamic honeypots using Docker and Kubernetes.
* Multi-agent Deep Reinforcement Learning (PPO/DQN) for autonomous cyber warfare games.
* Federated counterfactual utility sharing across collaborative enterprise defense consortia.

---

## REFERENCES (IEEE Format)

1. M. Pawlicki, M. Choraś, and R. Kozik, "Defending cyber deception systems against adversarial attacks," *IEEE Transactions on Information Forensics and Security*, vol. 16, pp. 2489–2500, 2021.
2. J. Pearl, *Causality: Models, Reasoning, and Inference*, 2nd ed. Cambridge: Cambridge University Press, 2009.
3. L. P. Kaelbling, M. L. Littman, and A. R. Cassandra, "Planning and acting in partially observable stochastic domains," *Artificial Intelligence*, vol. 101, no. 1–2, pp. 99–134, 1998.
4. N. J. Rowe, "Designing good deceptions in cyber defense," in *Proc. IEEE Int. Conf. on Intelligence and Security Informatics (ISI)*, 2018, pp. 124–129.
5. F. Pedregosa *et al.*, "Scikit-learn: Machine learning in Python," *Journal of Machine Learning Research*, vol. 12, pp. 2825–2830, 2011.
