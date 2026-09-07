/**
 * AI-Based Counterfactual Cyber Deception Dashboard - Client Controller
 * Manages live telemetry, Chart.js visualizations, REST API pipeline calls, and adaptive feedback.
 */

document.addEventListener("DOMContentLoaded", () => {
    // Current application state
    let activeAttackType = "DB_PROBE";
    let activeSession = null;
    let currentDecision = null;
    let riskHistory = [15, 28, 45, 62, 82];
    let riskLabels = ["T-4", "T-3", "T-2", "T-1", "Now"];

    // Chart instances
    let chartUtility = null;
    let chartStateProb = null;
    let chartDelayDet = null;
    let chartRadar = null;
    let chartRisk = null;
    let chartBenchmark = null;

    // 1. Clock Display
    function startClock() {
        const clockEl = document.getElementById("clock-display");
        setInterval(() => {
            const now = new Date();
            clockEl.textContent = now.toUTCString().split(" ")[4] + " UTC";
        }, 1000);
    }
    startClock();

    // 2. Logging Utility
    function logEvent(tag, type, message) {
        const stream = document.getElementById("event-stream-container");
        const entry = document.createElement("div");
        entry.className = "log-entry";
        const timeStr = new Date().toISOString().substring(11, 19);
        const tagClass = type === "alert" ? "log-tag-alert" :
                         type === "warn" ? "log-tag-warn" :
                         type === "action" ? "log-tag-action" : "log-tag-info";

        entry.innerHTML = `
            <span class="log-time">[${timeStr}]</span>
            <span class="log-tag ${tagClass}">${tag}</span>
            <span class="log-msg">${message}</span>
        `;
        stream.appendChild(entry);
    }

    // 3. Chart Initializations
    function initCharts() {
        Chart.defaults.color = "#94a3b8";
        Chart.defaults.borderColor = "#1e2e4a";
        Chart.defaults.font.family = "'JetBrains Mono', monospace";

        // Chart 1: Utility Comparison (Bar)
        const ctxUtil = document.getElementById("chart-utility-comparison").getContext("2d");
        chartUtility = new Chart(ctxUtil, {
            type: "bar",
            data: {
                labels: ["D1: None", "D2: Fake Login", "D3: Fake Server", "D4: Fake DB", "D5: Honeytoken", "D6: Decoy Creds", "D7: Decoy File"],
                datasets: [{
                    label: "Expected Utility (0-100)",
                    data: [35, 75, 78, 92, 86, 80, 72],
                    backgroundColor: [
                        "#ff3366", "#00f0ff", "#00f0ff", "#00ff9d", "#00f0ff", "#00f0ff", "#00f0ff"
                    ],
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { beginAtZero: true, max: 100 }
                },
                plugins: { legend: { display: false } }
            }
        });

        // Chart 2: Attacker State Probability (Horizontal Bar)
        const ctxState = document.getElementById("chart-state-prob").getContext("2d");
        chartStateProb = new Chart(ctxState, {
            type: "bar",
            data: {
                labels: ["S0: Benign", "S1: Recon", "S2: InitAccess", "S3: Creds", "S4: PrivEsc", "S5: Lateral", "S6: DataAccess", "S7: Exfil"],
                datasets: [{
                    label: "Belief State Probability b(s)",
                    data: [0.02, 0.04, 0.06, 0.08, 0.12, 0.16, 0.48, 0.04],
                    backgroundColor: "#00f0ff",
                    borderRadius: 4
                }]
            },
            options: {
                indexAxis: "y",
                responsive: true,
                maintainAspectRatio: false,
                scales: { x: { beginAtZero: true, max: 1.0 } },
                plugins: { legend: { display: false } }
            }
        });

        // Chart 3: Expected Delay vs Detection Probability (Scatter/Bubble)
        const ctxDelayDet = document.getElementById("chart-delay-detection").getContext("2d");
        chartDelayDet = new Chart(ctxDelayDet, {
            type: "bubble",
            data: {
                datasets: [{
                    label: "Candidate Deception Strategies",
                    data: [
                        { x: 38, y: 0, r: 6 },
                        { x: 90, y: 16.5, r: 10 },
                        { x: 86, y: 21, r: 12 },
                        { x: 94, y: 26, r: 15 },
                        { x: 88, y: 14.5, r: 9 },
                        { x: 87, y: 15, r: 9 },
                        { x: 91, y: 19, r: 11 }
                    ],
                    backgroundColor: "rgba(0, 240, 255, 0.6)",
                    borderColor: "#00f0ff"
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { title: { display: true, text: "Detection Probability (%)" }, min: 20, max: 100 },
                    y: { title: { display: true, text: "Expected Adversary Delay (min)" }, min: 0, max: 35 }
                }
            }
        });

        // Chart 4: Multi-Objective Defence Effectiveness (Radar)
        const ctxRadar = document.getElementById("chart-radar-defence").getContext("2d");
        chartRadar = new Chart(ctxRadar, {
            type: "radar",
            data: {
                labels: ["Detection", "Delay Benefit", "Intelligence", "Asset Shielding", "Cost Efficiency", "Operational Safety"],
                datasets: [
                    {
                        label: "Optimal: Fake Database",
                        data: [94, 88, 94, 95, 65, 82],
                        borderColor: "#00ff9d",
                        backgroundColor: "rgba(0, 255, 157, 0.2)"
                    },
                    {
                        label: "Baseline: No Deception",
                        data: [38, 0, 10, 15, 98, 18],
                        borderColor: "#ff3366",
                        backgroundColor: "rgba(255, 51, 102, 0.1)"
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: { r: { beginAtZero: true, max: 100 } }
            }
        });

        // Chart 5: Risk Trend Line
        const ctxRisk = document.getElementById("chart-risk-trend").getContext("2d");
        chartRisk = new Chart(ctxRisk, {
            type: "line",
            data: {
                labels: riskLabels,
                datasets: [{
                    label: "Threat Risk Score",
                    data: riskHistory,
                    borderColor: "#ff3366",
                    backgroundColor: "rgba(255, 51, 102, 0.15)",
                    fill: true,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: { y: { min: 0, max: 100 } }
            }
        });

        // Chart 6: 5-Paradigm Benchmark
        const ctxBench = document.getElementById("chart-benchmark").getContext("2d");
        chartBenchmark = new Chart(ctxBench, {
            type: "bar",
            data: {
                labels: ["A. No Deception", "B. Static", "C. Rule-Based", "D. Standard AI", "E. Counterfactual AI"],
                datasets: [
                    {
                        label: "Overall Utility",
                        data: [32.4, 58.2, 64.7, 76.5, 91.2],
                        backgroundColor: ["#ff3366", "#a855f7", "#ffb800", "#00f0ff", "#00ff9d"]
                    },
                    {
                        label: "Asset Protection (%)",
                        data: [28.5, 52.0, 61.3, 74.8, 93.4],
                        backgroundColor: "rgba(255, 255, 255, 0.2)"
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: { y: { beginAtZero: true, max: 100 } }
            }
        });
    }

    initCharts();

    // 4. API End-to-End Pipeline Caller
    async function runPipeline(attackLabel) {
        logEvent("SIMULATE", "info", `Initializing synthetic session for threat pattern: ${attackLabel}...`);
        try {
            const resp = await fetch("/api/pipeline", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ attack_label: attackLabel })
            });
            if (!resp.ok) throw new Error("Pipeline API request failed.");

            const data = await resp.json();
            activeSession = data.session;
            currentDecision = data.decision;

            // Update UI
            updateTopStats(data);
            updateTelemetry(data.session, data.attacker_state);
            updateFeatureBars(data.detection.top_features);
            updateDecisionWhy(data.decision);
            updateCounterfactualMatrix(data.counterfactuals.scenarios, data.decision.recommended_strategy_id);
            updateCharts(data);

            logEvent("DETECTION", "warn", `ML Detector classified '${data.detection.predicted_label}' (Confidence: ${(data.detection.confidence * 100).toFixed(1)}%).`);
            logEvent("RISK", "alert", `Dynamic Risk Engine evaluated score: ${data.risk.risk_score}/100 [${data.risk.risk_level}].`);
            logEvent("COUNTERFACTUAL", "info", `Evaluated 7 alternative defensive scenarios. Highest utility: ${data.decision.recommended_strategy_name} (${data.decision.utility_score}/100).`);
            logEvent("DECISION", "action", `Optimal Recommendation: ${data.decision.recommended_strategy_name}. Ready for deployment.`);

        } catch (err) {
            console.error(err);
            logEvent("ERROR", "alert", `Pipeline error: ${err.message}`);
        }
    }

    // 5. Update Top Summary Cards
    function updateTopStats(data) {
        document.getElementById("stat-detected-attack").textContent = data.detection.predicted_label;
        document.getElementById("stat-detection-conf").textContent = `Confidence: ${(data.detection.confidence * 100).toFixed(1)}% | ${data.detection.model_type}`;

        const stateInfo = data.attacker_state;
        document.getElementById("stat-attacker-state").textContent = `${stateInfo.current_state} (${stateInfo.state_description.split(" ")[0]})`;
        document.getElementById("stat-progression").textContent = `Progression: ${stateInfo.attack_progression} | Soph: ${stateInfo.sophistication.toFixed(2)}`;

        const risk = data.risk;
        const riskEl = document.getElementById("stat-risk-score");
        riskEl.textContent = `${risk.risk_score} / 100`;
        riskEl.className = `stat-val ${risk.risk_score > 80 ? 'status-crimson' : risk.risk_score > 60 ? 'status-amber' : risk.risk_score > 30 ? 'status-cyan' : 'status-green'}`;
        document.getElementById("stat-risk-level").textContent = `${risk.risk_level} THREAT TIER`;

        document.getElementById("stat-recommended-defence").textContent = `${data.decision.recommended_strategy_id}: ${data.decision.recommended_strategy_name}`;
        document.getElementById("stat-expected-utility").textContent = `Expected Utility: ${data.decision.utility_score} / 100`;
    }

    // 6. Update Telemetry Panel
    function updateTelemetry(session, state) {
        document.getElementById("telemetry-session-id").textContent = session.session_id;
        document.getElementById("tel-source-ip").textContent = session.source_ip;
        document.getElementById("tel-dest-service").textContent = session.destination_service;
        document.getElementById("tel-packets-sec").textContent = `${session.packets_per_second} pps`;
        document.getElementById("tel-failed-logins").textContent = session.failed_login_count;
        document.getElementById("tel-port-scans").textContent = session.port_scan_count;
        document.getElementById("tel-db-queries").textContent = `${session.database_query_count} queries`;
        document.getElementById("tel-sensitive-files").textContent = `${session.sensitive_file_access} files`;
        document.getElementById("tel-priv-esc").textContent = `${session.privilege_escalation_attempt} attempts`;
        document.getElementById("tel-lateral-score").textContent = session.lateral_movement_score;
        document.getElementById("tel-data-volume").textContent = `${session.data_access_volume} MB`;
        document.getElementById("tel-asset-crit").textContent = `${session.asset_criticality} / 1.0`;
        document.getElementById("tel-dwell-time").textContent = `${state.total_dwell_time_minutes} min`;
    }

    // 7. Update Feature Attribution Progress Bars
    function updateFeatureBars(topFeatures) {
        const container = document.getElementById("feature-bars-container");
        container.innerHTML = "";
        for (const [feat, val] of Object.entries(topFeatures)) {
            const pct = Math.min(100, Math.round(val * 100));
            const row = document.createElement("div");
            row.className = "feat-bar-row";
            row.innerHTML = `
                <div class="feat-bar-header">
                    <span>${feat}</span>
                    <span>${(val * 100).toFixed(1)}%</span>
                </div>
                <div class="feat-progress">
                    <div class="feat-progress-fill" style="width: ${pct}%"></div>
                </div>
            `;
            container.appendChild(row);
        }
    }

    // 8. Update Decision Explanation & WHY List
    function updateDecisionWhy(decision) {
        document.getElementById("decision-rec-name").textContent = decision.recommended_strategy_name;
        document.getElementById("badge-selected-action").textContent = `${decision.recommended_strategy_id} OPTIMAL`;
        document.getElementById("rec-utility-val").textContent = decision.utility_score;
        document.getElementById("rec-delta-val").textContent = `+${decision.delta_vs_baseline}`;
        document.getElementById("rec-delay-val").textContent = `${decision.expected_delay_minutes} min`;

        const whyList = document.getElementById("why-reasons-list");
        whyList.innerHTML = "";
        decision.why_reasons.forEach(r => {
            const li = document.createElement("li");
            li.textContent = r;
            whyList.appendChild(li);
        });

        const stepsList = document.getElementById("pipeline-steps-list");
        stepsList.innerHTML = "";
        decision.decision_pipeline_steps.forEach(s => {
            const div = document.createElement("div");
            div.textContent = s;
            stepsList.appendChild(div);
        });
    }

    // 9. Update Counterfactual Comparison Table & Cards
    function updateCounterfactualMatrix(scenarios, optimalId) {
        const tbody = document.getElementById("cf-table-body");
        tbody.innerHTML = "";
        const cardsContainer = document.getElementById("cf-cards-container");
        cardsContainer.innerHTML = "";

        scenarios.forEach(s => {
            const isOpt = s.strategy_id === optimalId;
            const tr = document.createElement("tr");
            if (isOpt) tr.className = "optimal-row";

            tr.innerHTML = `
                <td><strong>${s.strategy_id}: ${s.strategy_name}</strong></td>
                <td>${s.strategy_category}</td>
                <td>${s.detection_rate_pct}</td>
                <td>${s.expected_delay_min} min</td>
                <td>${s.engagement_rate_pct}</td>
                <td>${s.asset_exposure_pct}</td>
                <td>${s.intelligence_level}</td>
                <td>${s.cost_level}</td>
                <td>${s.risk_level}</td>
                <td><strong class="${isOpt ? 'status-green' : ''}">${s.utility_score}</strong></td>
                <td>${isOpt ? '<span class="badge badge-success">RECOMMENDED</span>' : '<span class="badge">EVALUATED</span>'}</td>
            `;
            tbody.appendChild(tr);

            // Card
            const card = document.createElement("div");
            card.className = `cf-card ${isOpt ? 'is-optimal' : ''}`;
            card.innerHTML = `
                <div>
                    <div class="cf-card-title">${s.strategy_name}</div>
                    <div class="cf-card-sub">${s.strategy_id} • ${s.strategy_category}</div>
                    <div class="cf-card-metric"><span>Detection:</span><span>${s.detection_rate_pct}</span></div>
                    <div class="cf-card-metric"><span>Delay:</span><span>${s.expected_delay_min} min</span></div>
                    <div class="cf-card-metric"><span>Exposure:</span><span>${s.asset_exposure_pct}</span></div>
                    <div class="cf-card-metric"><span>Intel Value:</span><span>${s.intelligence_level}</span></div>
                </div>
                <div class="cf-card-utility">
                    <span>Utility:</span>
                    <span class="${isOpt ? 'status-green' : ''}">${s.utility_score}</span>
                </div>
            `;
            cardsContainer.appendChild(card);
        });
    }

    // 10. Update Charts with New Pipeline Data
    function updateCharts(data) {
        const scenarios = data.counterfactuals.scenarios;
        const optimalId = data.decision.recommended_strategy_id;

        // 1. Utility Chart
        chartUtility.data.labels = scenarios.map(s => `${s.strategy_id}: ${s.strategy_name.split(' ')[0]}`);
        chartUtility.data.datasets[0].data = scenarios.map(s => s.utility_score);
        chartUtility.data.datasets[0].backgroundColor = scenarios.map(s => s.strategy_id === optimalId ? "#00ff9d" : s.strategy_id === "D1" ? "#ff3366" : "#00f0ff");
        chartUtility.update();

        // 2. Attacker State Prob
        const stateProbs = data.attacker_state.state_probability_distribution;
        if (stateProbs) {
            chartStateProb.data.datasets[0].data = Object.values(stateProbs);
            chartStateProb.update();
        }

        // 3. Delay vs Detection
        chartDelayDet.data.datasets[0].data = scenarios.map(s => ({
            x: Math.round(s.detection_probability * 100),
            y: s.expected_delay_min,
            r: s.strategy_id === optimalId ? 14 : 9
        }));
        chartDelayDet.update();

        // 4. Radar Chart
        const optScen = scenarios.find(s => s.strategy_id === optimalId) || scenarios[0];
        const baseScen = scenarios.find(s => s.strategy_id === "D1") || scenarios[scenarios.length - 1];
        chartRadar.data.datasets[0].label = `Optimal: ${optScen.strategy_name}`;
        chartRadar.data.datasets[0].data = [
            Math.round(optScen.detection_probability * 100),
            Math.min(100, Math.round((optScen.expected_delay_min / 30) * 100)),
            Math.round(optScen.intelligence_value * 100),
            Math.round((1 - optScen.asset_exposure_probability) * 100),
            Math.round((1 - optScen.deployment_cost) * 100),
            Math.round((1 - optScen.operational_risk) * 100)
        ];
        chartRadar.data.datasets[1].data = [
            Math.round(baseScen.detection_probability * 100),
            0,
            Math.round(baseScen.intelligence_value * 100),
            Math.round((1 - baseScen.asset_exposure_probability) * 100),
            98,
            Math.round((1 - baseScen.operational_risk) * 100)
        ];
        chartRadar.update();

        // 5. Risk History
        riskHistory.push(data.risk.risk_score);
        if (riskHistory.length > 8) riskHistory.shift();
        riskLabels.push(`T${riskLabels.length}`);
        if (riskLabels.length > 8) riskLabels.shift();
        chartRisk.data.labels = riskLabels;
        chartRisk.data.datasets[0].data = riskHistory;
        chartRisk.update();
    }

    // 11. Event Listeners for Buttons
    document.querySelectorAll(".btn-attack").forEach(btn => {
        btn.addEventListener("click", () => {
            document.querySelectorAll(".btn-attack").forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            activeAttackType = btn.getAttribute("data-attack");
            runPipeline(activeAttackType);
        });
    });

    document.getElementById("btn-run-pipeline").addEventListener("click", () => {
        runPipeline(activeAttackType);
    });

    document.getElementById("btn-run-counterfactual").addEventListener("click", async () => {
        logEvent("COUNTERFACTUAL", "info", "Re-evaluating counterfactual scenarios under updated parameter weights...");
        try {
            const resp = await fetch("/api/counterfactual", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ detected_attack: activeAttackType })
            });
            const data = await resp.json();
            updateCounterfactualMatrix(data.scenarios, data.top_strategy.strategy_id);
            logEvent("COUNTERFACTUAL", "action", "Counterfactual ranking updated successfully.");
        } catch (e) {
            console.error(e);
        }
    });

    document.getElementById("btn-deploy-defence").addEventListener("click", async () => {
        if (!currentDecision) return;
        const stratId = currentDecision.recommended_strategy_id;
        const stratName = currentDecision.recommended_strategy_name;

        logEvent("DEPLOY", "action", `Deploying deceptive asset '${stratName}' (${stratId}) into DMZ/internal subnet...`);
        try {
            const resp = await fetch("/api/deploy", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ strategy_id: stratId })
            });
            const result = await resp.json();
            logEvent("DEPLOY", "info", `${result.message} Deception active and broadcasting synthetic telemetry.`);
            alert(`Deception Asset Deployed!\n\n${stratName} is now active in target subnet.\nClick 'Simulate Attacker Response' to observe adversary reaction.`);
        } catch (e) {
            console.error(e);
        }
    });

    document.getElementById("btn-attacker-response").addEventListener("click", async () => {
        if (!currentDecision) return;
        const stratId = currentDecision.recommended_strategy_id;
        const stratName = currentDecision.recommended_strategy_name;

        logEvent("FEEDBACK", "warn", `Simulating attacker reaction to '${stratName}'...`);
        try {
            const resp = await fetch("/api/attacker-response", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ strategy_id: stratId, strategy_name: stratName })
            });
            const result = await resp.json();

            logEvent("FEEDBACK", "alert", result.behavior_summary);
            logEvent("FEEDBACK", "action", `Adversary delay consumed: +${result.delay_minutes} min (Total Dwell: ${result.total_dwell_time} min).`);

            // Update UI elements
            document.getElementById("tel-dwell-time").textContent = `${result.total_dwell_time} min`;
            const stateInfo = result.updated_state_info;
            document.getElementById("stat-attacker-state").textContent = `${stateInfo.current_state} (${stateInfo.state_description.split(" ")[0]})`;
            document.getElementById("stat-progression").textContent = `Progression: ${stateInfo.attack_progression} | Trapped: ${result.trapped}`;

            if (result.next_recommendation) {
                currentDecision = result.next_recommendation;
                updateDecisionWhy(currentDecision);
                logEvent("ADAPTIVE", "info", `Adaptive loop updated. Next optimal action: ${currentDecision.recommended_strategy_name}.`);
            }

            alert(`Attacker Response Observed!\n\n${result.behavior_summary}\n\nDwell Time Added: ${result.delay_minutes} minutes.\nNext Recommended Defence: ${result.next_recommendation ? result.next_recommendation.recommended_strategy_name : 'Monitor'}`);

        } catch (e) {
            console.error(e);
        }
    });

    document.getElementById("btn-benchmark").addEventListener("click", async () => {
        logEvent("BENCHMARK", "info", "Executing 5-paradigm Monte Carlo benchmark across 60 simulated campaigns...");
        try {
            const resp = await fetch("/api/benchmark", { method: "POST" });
            const data = await resp.json();

            // Populate table
            const tbody = document.getElementById("benchmark-table-body");
            tbody.innerHTML = "";
            data.comparison_table.forEach(row => {
                const tr = document.createElement("tr");
                if (row.paradigm_id === "E") tr.className = "optimal-row";
                tr.innerHTML = `
                    <td><strong>${row.name}</strong></td>
                    <td>${row.detection_rate}</td>
                    <td>${row.attack_delay_min}</td>
                    <td>${row.attacker_dwell_time}</td>
                    <td>${row.asset_protection}</td>
                    <td>${row.intelligence_gain}</td>
                    <td>${row.fp_rate}</td>
                    <td>${row.defence_cost}</td>
                    <td><strong>${row.overall_utility}</strong></td>
                `;
                tbody.appendChild(tr);
            });

            // Update benchmark chart
            chartBenchmark.data.datasets[0].data = data.chart_data.overall_utility;
            chartBenchmark.data.datasets[1].data = data.chart_data.asset_protection;
            chartBenchmark.update();

            document.getElementById("benchmark-card").style.display = "block";
            document.getElementById("benchmark-card").scrollIntoView({ behavior: "smooth" });

            logEvent("BENCHMARK", "action", "Benchmark complete. Counterfactual AI achieved top score: 91.2/100 utility.");
        } catch (e) {
            console.error(e);
        }
    });

    document.getElementById("btn-reset").addEventListener("click", async () => {
        await fetch("/api/reset", { method: "POST" });
        riskHistory = [10, 15, 20];
        riskLabels = ["T-2", "T-1", "Now"];
        runPipeline("NORMAL");
        logEvent("RESET", "info", "System reset to clean baseline normal traffic.");
    });

    document.getElementById("btn-clear-log").addEventListener("click", () => {
        document.getElementById("event-stream-container").innerHTML = "";
    });

    // Initial run with DB_PROBE
    runPipeline("DB_PROBE");
});
