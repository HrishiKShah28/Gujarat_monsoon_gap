# The Monsoon Recharge Gap: Identifying Persistent Groundwater Stress Across Gujarat

[![Avaloka Hackathon](https://img.shields.io/badge/Avaloka-AI%20Engineering%20Internship%20Hackathon-blue.svg)](https://avaloka.ai)
[![Dataset](https://img.shields.io/badge/NWIC%20%2F%20CGWB-National%20Water%20Data%20Portal-green.svg)](https://nwdp.nwic.gov.in)
[![Observations](https://img.shields.io/badge/Observations-52%2C919%20Records-blue.svg)](data/processed/gujarat_groundwater_analytical.csv)
[![Avaloka Model R2](https://img.shields.io/badge/Avaloka%20Model%20R%C2%B2-0.9665-brightgreen.svg)](avaloka-model/executive_report.html)
[![Validation](https://img.shields.io/badge/Validation%20Verdict-PASS%20(Level%204)-success.svg)](avaloka-model/validation_report.json)
[![Region](https://img.shields.io/badge/Region-Gujarat%2C%20India-orange.svg)](https://guj-nwrws.gujarat.gov.in)

> **Evaluation Target**: Avaloka AI Engineering Internship Hackathon (Guruvai Sciences / Indu Ganti)  
> **Applicant / Lead Investigator**: Hrishi K. Shah  
> **Project Repository**: [github.com/HrishiKShah28/Gujarat_monsoon_gap](https://github.com/HrishiKShah28/Gujarat_monsoon_gap)  
> **Live Avaloka Workspace**: [app.avaloka.ai](https://app.avaloka.ai)  

---

## Table of Contents
1. [Executive Summary & The Real Indian Problem](#1-executive-summary--the-real-indian-problem)
2. [Dataset Architecture & Official Provenance (33 Years of Telemetry)](#2-dataset-architecture--official-provenance-33-years-of-telemetry)
3. [Phase 1: Local Agentic Execution via the Avaloka Open-Source CLI Engine](#3-phase-1-local-agentic-execution-via-the-avaloka-open-source-cli-engine)
   - [Running `avaloka analyze` & The Swarm of Fireflies](#running-avaloka-analyze--the-swarm-of-fireflies)
   - [Official Generated Deliverable 1: Analysis Executive Report](#official-generated-deliverable-1-analysis-executive-report)
   - [Official Generated Deliverable 2: Model Training Executive Report & Model Card](#official-generated-deliverable-2-model-training-executive-report--model-card)
4. [Phase 2: Live Cloud Multi-Agent Workspace on Avaloka AI (`app.avaloka.ai`)](#4-phase-2-live-cloud-multi-agent-workspace-on-avaloka-ai-appavalokaai)
   - [Multi-Dataset Project Workspace Setup](#multi-dataset-project-workspace-setup)
   - [Turn-by-Turn Chat Transcript & Findings](#turn-by-turn-chat-transcript--findings)
   - [Auditing Avaloka's Self-Checking Calibration & Safety Gates](#auditing-avalokas-self-checking-calibration--safety-gates)
5. [Core Hydrogeological & Empirical Findings](#5-core-hydrogeological--empirical-findings)
   - [Finding 1: The Monsoon Recharge Gap (Zero/Negative Recovery)](#finding-1-the-monsoon-recharge-gap-zeronegative-recovery)
   - [Finding 2: Unmasking Simpson's Paradox (Basalt vs Alluvium)](#finding-2-unmasking-simpsons-paradox-basalt-vs-alluvium)
   - [Finding 3: Decadal Secular Trends (Theil-Sen) & Spatial Autocorrelation](#finding-3-decadal-secular-trends-theil-sen--spatial-autocorrelation)
   - [Finding 4: 6-Month Lead-Time Early Warning Forecasting](#finding-4-6-month-lead-time-early-warning-forecasting)
6. [Actionable Policy Interventions for GWRDC & District Water Authorities](#6-actionable-policy-interventions-for-gwrdc--district-water-authorities)
7. [Repository File Map & Local Reproduction Guide](#7-repository-file-map--local-reproduction-guide)

---

## 1. Executive Summary & The Real Indian Problem

### The Context: India's Invisible Resource Backbone
In India, **over 80% of rural domestic drinking water** and **more than 60% of agricultural irrigation** are pumped directly from groundwater aquifers. In semi-arid Gujarat, an agrarian powerhouse and industrial corridor, water is the single most critical constraint on human livelihoods and regional stability.

### The Conventional Myth vs. The Hydrogeological Reality
Public discourse and district administrations routinely rely on a simplistic heuristic:  
> *"If Gujarat experiences a bountiful South-West monsoon, our water reservoirs are filled, aquifers are recharged, and water security is guaranteed for the coming agricultural year."*

**This research proves that assumption is dangerously flawed.**

### The Research Question: "The Monsoon Recharge Gap"
> *"Which districts and monitoring stations in Gujarat exhibit a **'Monsoon Recharge Gap'**—failing to recover their water table elevation despite recorded seasonal monsoon precipitation—and can we predict pre-monsoon summer water depletion **six months in advance** using data available at the close of the monsoon?"*

### Real-World Public Stakeholders & Decision Impact
- **Gujarat Water Resources Development Corporation (GWRDC)**: Targeting site selection for Managed Aquifer Recharge (MAR), check dams, and sub-surface percolation filter shafts.
- **Central Ground Water Board (CGWB - West Central Region)**: Pinpointing over-exploited assessment blocks to regulate industrial extraction licenses.
- **District Collectors & District Agricultural Offices**: Gaining a **6-month operational window** (in November) to ration 3-phase agricultural electricity feeders, restrict water-intensive summer crops (paddy, sugarcane), and pre-budget municipal water tanker logistics long before April/May heatwaves.

---

## 2. Dataset Architecture & Official Provenance (33 Years of Telemetry)

All telemetry was extracted from official, open Government of India repositories maintained by the **National Water Informatics Centre (NWIC / NWDP)** under the **Ministry of Jal Shakti** and the **Central Ground Water Board (CGWB)**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    OFFICIAL GOVERNMENT DATA SOURCES                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. Recent Ingestion (2021–2025): Resource ID ef17ded9-be74-48e6-9359       │
│    - gwl_manual_quarterly_cgwb_gj_2021_2025.csv (0.81 MB | 6,704 rows)     │
│ 2. Historical Baseline (1991–2020): Resource ID 8cc177be-e829-4b4d-88d1     │
│    - gwl_manual_quarterly_gujarat-sw-gw_gj_1991_2020.csv (5.38 MB | 46,426)│
│                                                                             │
│ TOTAL EXTENT: 52,919 valid observations across 2,046 monitoring stations    │
│ spanning 33 continuous years (1991–2023) across all 34 districts of Gujarat.│
└─────────────────────────────────────────────────────────────────────────────┘
```

To empower Avaloka's multi-agent system, the raw telemetry was sanitized and structured into three linked datasets:

| Dataset File | Rows | Columns | Purpose in Avaloka |
| :--- | :--- | :--- | :--- |
| **`data/processed/gujarat_groundwater_analytical.csv`** | 52,919 | 26 | Master analytical file: depth ($h$, mbgl), date, district, hydrogeological zone, season. |
| **`data/processed/gujarat_groundwater_seasonal_paired.csv`** | 22,820 | 16 | Paired May-Nov station-years: computes $\Delta h_{\text{recharge}} = h_{\text{May}} - h_{\text{Nov}}$ and flags deficit stations ($\Delta h \le 0$). |
| **`data/processed/gujarat_groundwater_model_features.csv`** | 21,586 | 19 | Predictive matrix: targets summer depth ($h_{\text{May}, t+1}$) using only post-monsoon features up to year $t$ (zero leakage). |

---

## 3. Phase 1: Local Agentic Execution via the Avaloka Open-Source CLI Engine

Rather than interacting with Avaloka solely through a browser interface, we cloned the official open-source repository ([github.com/guruvaidev/avaloka](https://github.com/guruvaidev/avaloka)) and executed its **agentic CLI runtime** directly against our sanitized datasets.

### Running `avaloka analyze` & The Swarm of Fireflies
When invoked, Avaloka clones itself into a swarm of specialized agent fireflies, each assuming a specialized role:

```mermaid
graph TD
    User["Terminal CLI Command"] --> Orchestrator["Avaloka Swarm Orchestrator"]
    Orchestrator --> Scout["✦ Ava-Scout (Data Analyst)<br/>Profiles 25 columns, distributions & anomalies"]
    Orchestrator --> Sampler["✦ Ava-Sampler (Data Scientist)<br/>Extracts truth-preserving working samples"]
    Orchestrator --> Engineer["✦ Ava-Engineer (Data Engineer)<br/>Writes reproducible pipeline & transformed parquet"]
    Orchestrator --> Planner["✦ Ava-Planner (Senior Data Scientist)<br/>Structures analytical task & approval gates"]
    Orchestrator --> Scientist["✦ Ava-Scientist (ML Scientist)<br/>Trains candidate models & benchmarks baselines"]
    Orchestrator --> Skeptic["✦ Ava-Skeptic (Model-Risk Specialist)<br/>Validates leakage & tests against trivial heuristics"]
    Orchestrator --> FinOps["✦ Ava-FinOps (Infrastructure Engineer)<br/>Weighs compute cost vs accuracy return"]
    Orchestrator --> Voice["✦ Ava-Voice (Consultant / Reporter)<br/>Compiles HTML executive reports & lineage"]
```

### Official Generated Deliverable 1: Analysis Executive Report
**Execution Command**:
```bash
avaloka analyze "data/processed/gujarat_groundwater_seasonal_paired.csv" --goal "how does recharge_delta vary by district"
```
- **Mission Artifact Folder**: `avaloka-analysis/d09332a26617/`
- **Generated Report**: **[`avaloka-analysis/d09332a26617/executive_report.html`](avaloka-analysis/d09332a26617/executive_report.html)**

#### Key Results Extracted by Ava-Voice:
- **Mission Economics**: Replaced **11.6 hours** of senior manual data analysis in **0.3 seconds** with an **11.1x economic multiplier** at $0 compute cost.
- **Top Recharge Districts Identified**:
  - `district=Rajkot`: mean recharge delta = **8.25 m**
  - `district=Junagadh`: mean recharge delta = **7.44 m**
  - `district=Aravalli`: mean recharge delta = **6.51 m**
  - `district=Porbandar`: mean recharge delta = **5.93 m**
  - `district=Amreli`: mean recharge delta = **5.81 m**
- **Validation Verdict**: **PASS** (Safe deployment level: 1 of 4).

---

### Official Generated Deliverable 2: Model Training Executive Report & Model Card
**Execution Command**:
```bash
avaloka train "data/processed/gujarat_groundwater_model_features.csv" --target depth_may_next
```
- **Mission Artifact Folder**: `avaloka-model/`
- **Generated Reports**: **[`avaloka-model/executive_report.html`](avaloka-model/executive_report.html)** & **[`avaloka-model/evaluation_report.html`](avaloka-model/evaluation_report.html)**
- **Model Card**: **[`avaloka-model/model_card.md`](avaloka-model/model_card.md)**

#### Key Results Extracted by Ava-Scientist & Ava-Skeptic:
- **Trained 3 Candidate Architectures** across 21,586 records.
- **Selected Champion Architecture**: **`random_forest`** achieving an **$R^2$ of 0.9665** on unseen holdout records.
- **Baseline Verification Gate**: Decisively defeated the trivial persistence baseline (`-0.0000` $R^2$) by a margin far exceeding fold noise.
- **Validation Verdict**: **PASS** with maximum safe deployment rating: **Level 4 of 4**.
- **Mission Economics**: Replaced **20.7 hours** of ML engineering in **4.0 minutes** ($148.95 equivalent human value created).

---

## 4. Phase 2: Live Cloud Multi-Agent Workspace on Avaloka AI (`app.avaloka.ai`)

In addition to the CLI runtime, we registered our project in the cloud web workspace at [app.avaloka.ai](https://app.avaloka.ai) under the project **`Environmental/Hydrology`**.

### Multi-Dataset Project Workspace Setup
By attaching all three curated datasets simultaneously (`Gujarat Groundwater Analytical`, `Model Features`, and `Seasonal Paired`), Avaloka's cloud core ingested **52,919 records** and automatically rendered **9 multi-dimensional Auto Insights charts**.

```
Selected Datasets in Workspace:
[ Gujarat Groundwater Analytical ]  [ Gujarat Groundwater Model Features ]  [ Gujarat Groundwater Seasonal Paired ]
Auto Insights Generated: 9 Interactive Charts | Features: Planner Graph, Data Sample, Analysis Results (3)
```

---

### Turn-by-Turn Chat Transcript & Findings

Below is the verified record of our session with Avaloka's multi-agent chat core:

#### Turn 1: Seasonal Depth Dynamics & Post-Monsoon Recovery
> **User Prompt**:  
> *"Compare the groundwater depth between Pre-Monsoon Summer (May) and Post-Monsoon (November) across the hydrogeological zones. Which zone has the deepest water table, and how much does each zone recover after the monsoon?"*

- **Planner Agent Plan Generated**:
  - `Plan`: Profile datasets $\to$ Join shared columns $\to$ Synthesize seasonal delta $\to$ Test on sample $\to$ Await human approval.
- **Avaloka Agent Output**:
  - *"The Saurashtra Hard-Rock Basalt zone has the deepest water table in May (21.04 m) and recovers the most after monsoon, dropping 7.08 m to 13.97 m in November."*
  - *"North Gujarat Alluvium: depth falls from 8.04 m to 5.68 m (2.35 m change, 32.7% recovery)."*
  - *"Saurashtra Hard-Rock Basalt: depth falls from 21.04 m to 13.97 m (7.08 m change, 39% recovery)."*
  - *"Despite having a deeper May depth, the Hard-Rock zone's absolute drop is more than three times that of Alluvium."*

---

#### Turn 2: Identifying Critical Stressed Districts & Deficit Stations
> **User Prompt**:  
> *"Which specific districts show the highest water table depth, and are there stations where the water level fails to recharge or actually deepens after the monsoon?"*

- **Avaloka Agent Output**:
  - *"The district with the deepest water table is Gandhinagar at 198.83 m, followed by Ahmedabad (97.72 m) and Kachchh (104.57 m)."*
  - *"Gandhinagar shows the greatest depth, while Banaskantha (179.8 m) and Mahesana (176.5 m) are close behind."*
  - *"Only Ahmedabad has stations where the water level does not recharge; four stations recorded a negative recharge delta (e.g., AD-04B: -3.5 m)."*
  - *"The deepest hydro-zone is consistently North Gujarat Alluvium across all districts."*

---

#### Turn 3: Stress-Testing Winter Rabi Depletion (Data Integrity Gate)
> **User Prompt**:  
> *"Looking at the chart 'Depth by Hydrogeological Zone', Saurashtra Hard-Rock Basalt shows seasonal recovery, but what happens during the winter Rabi season (January)? Does the water table drop rapidly due to low rock storativity compared to North Gujarat Alluvium?"*

- **Avaloka Agent Safety Gate Activated**:
  - *"I could write code for this, but the result it produced didn't match what the analysis was supposed to return, so I haven't used it: `mean_depth_jan` was declared non-null but has 3 missing values. Rephrasing the request — especially naming the grouping and the figure you want per group — usually resolves this."*
  - **Significance**: Rather than outputting corrupted metrics, Avaloka's pre-execution contract guard refused to execute unvalidated code on missing values!

---

#### Turn 4: 30-Year Secular Groundwater Depletion Trends
> **User Prompt**:  
> *"Based on the 30-year historical trend of depth over years, which districts exhibit continuous multi-year groundwater depletion, and what are the top critical stress zones requiring intervention?"*

- **Avaloka Agent Output**:
  - *"Ahmedabad, Banaskantha, Gandhinagar, and Patan exhibit continuous multi-year groundwater depletion, with Gandhinagar's 2017–2023 period showing the steepest rise."*
  - *"Critical stress zones: Gandhinagar, Ahmedabad, and Banaskantha (all North Gujarat Alluvium) rank in the top two for stress score."*
  - *"Largest recent jumps: Gandhinagar's 82 m increase (2017–2023) and Banaskantha's 28 m rise (2016–2022)."*
  - *"High stress alarm: Amreli has a stress score of 1.05 despite only a 3.5 m depth increase, indicating a disproportionate alarm."*
  - *"Overall trend: The North Gujarat Alluvium zones dominate the most severe depletion and stress rankings."*

---

### Auditing Avaloka's Self-Checking Calibration & Safety Gates

A standout capability of Avaloka is its autonomous **calibration layer**—checking generated natural language claims against computed numerical tables before displaying them:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 AVALOKA SELF-CHECKING VERIFICATION NOTICE                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ "Some numbers or claims in this answer did not check out:                   │
│  1 of 5 claims in this answer did not match the computed results.           │
│  Treat this answer as unchecked.                                            │
│                                                                             │
│  Contradicts the result's ordering · Contradicted by computed results:      │
│  says 'greatest' at 179.8, but max of 'max_depth' is 198.83."              │
└─────────────────────────────────────────────────────────────────────────────┘
```

This transparency is invaluable for public policy engineering. Most generative AI tools silently hallucinate false numbers; **Avaloka actively flagged its own ordering discrepancy**, warning the investigator that Gandhinagar (198.83m) was greater than Banaskantha (179.8m).

---

## 5. Core Hydrogeological & Empirical Findings

### Finding 1: The Monsoon Recharge Gap (Zero/Negative Recovery)
Across Gujarat's 22,820 paired station-years, the median seasonal water table rise is **3.20 meters** ($\text{IQR}: [1.40\text{m}, 6.00\text{m}]$). However, aggregate averages conceal severe regional distress:
- **410 Station-Years** exhibited an acute **Recharge Deficit** ($\Delta h \le 0$), where water levels either stagnated or dropped deeper following the monsoon.
- **Top Vulnerability Corridors**:
  1. **Mahesana (Mehsana)**: **12.54%** of station-years suffer outright recharge failure ($N = 606$).
  2. **Kachchh**: **7.65%** recharge deficit prevalence ($N = 1,229$).
  3. **Patan**: **6.30%** recharge deficit prevalence ($N = 127$).
  4. **Banaskantha**: **5.79%** recharge deficit prevalence ($N = 484$).

---

### Finding 2: Unmasking Simpson's Paradox (Basalt vs Alluvium)
An unstratified evaluation would suggest Saurashtra's aquifers are healthier than North Gujarat's because their seasonal water table rise is larger ($4.65\text{m}$ vs $3.25\text{m}$).

However, hydrogeological stratification reveals **Simpson's Paradox**:
- **Saurashtra Hard-Rock Basalts ($N = 8,533$)**: Crystalline basalt fractures allow rapid seasonal water level jumps ($4.65\text{m}$). But because basalt has negligible storativity (**Specific Yield $S_y \approx 1\text{--}3\%$**), the water column lacks volumetric depth: **34.2% of total monsoon recovery is depleted by January** ($\Delta h_{\text{Rabi}} = 1.59\text{m}$) as winter farming begins.
- **North Gujarat Alluvial Plains ($N = 1,578$)**: Multi-layered clay lenses impede vertical infiltration, leading to lower recharge ($3.25\text{m}$) and a **2.6× higher recharge failure rate (3.42% vs 1.29%)**. Tube-well mining for dairy and cash crops has depressed water tables into deep cones of depression exceeding $100\text{--}198\text{ mbgl}$.

---

### Finding 3: Decadal Secular Trends (Theil-Sen) & Spatial Autocorrelation
- **Theil-Sen Robust Slopes**: Across 802 monitoring wells with $\ge 15$ continuous years of May records, secular depletion is heavily concentrated in North Gujarat: Gandhinagar ($100\%$ of wells declining), Dang ($57\%$), Banaskantha ($50\%$), and Patan ($100\%$) show multi-decadal decline rates between $0.05\text{--}0.17\text{ meters/year}$.
- **Spatial Autocorrelation**: A Global Moran's $I$ test of pre-monsoon depths yielded **$I = 0.1604$ ($p < 0.001$)**, confirming that groundwater depletion is a continuous spatial phenomenon rather than localized sensor noise.

---

### Finding 4: 6-Month Lead-Time Early Warning Forecasting
Evaluating predictive performance on unseen holdout modern records ($2021\text{--}2023$) strictly using information available up to November of year $t$:
- **Continuous Depth Regression**: Avaloka's models achieved an **RMSE of 7.065 m** ($R^2 = 0.927$), decisively outperforming the seasonal persistence baseline heuristic ($\text{RMSE} = 7.560\text{ m}$).
- **Severe Stress Alarm ($\ge 15.0\text{ mbgl}$)**:
  - **ROC-AUC**: **0.9675**
  - **PR-AUC**: **0.9045**
  - **Precision**: **89.09%**
  - **Recall**: **80.99%**

This empowers disaster management agencies to intercept **over 80% of true pre-monsoon summer water crises with 89% precision half a year in advance**.

---

## 6. Actionable Policy Interventions for GWRDC & District Water Authorities

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   OPERATIONAL POLICY INTERVENTION MATRIX                    │
├───────────────────┬───────────────────────────────────┬─────────────────────┤
│ Hydrogeological   │ Vulnerability Mechanism           │ Actionable Policy   │
│ Regime            │                                   │ Prescription        │
├───────────────────┼───────────────────────────────────┼─────────────────────┤
│ North Gujarat     │ Low vertical recharge rate;       │ Construct deep sub- │
│ Alluvium          │ permanent alluvial cone of        │ surface injection   │
│ (Mehsana, Patan,  │ depression; 12.5% recharge        │ recharge shafts;    │
│ Banaskantha)      │ failure rate in Mehsana.          │ freeze new deep tube│
│                   │                                   │ well energization.  │
├───────────────────┼───────────────────────────────────┼─────────────────────┤
│ Saurashtra        │ High seasonal rise, but rapid     │ Enforce timed       │
│ Hard-Rock Basalts │ winter depletion due to low rock  │ 3-phase electricity │
│ (Rajkot, Amreli,  │ storativity (Sy 1–3%). 34% lost   │ rationing on farm   │
│ Junagadh)         │ by January Rabi season.           │ feeders; check dams.│
├───────────────────┼───────────────────────────────────┼─────────────────────┤
│ Kachchh Arid      │ Chronic recharge deficit rate     │ Pre-budget drinking │
│ Sedimentary       │ (7.65%) paired with erratic rain; │ water tanker routes │
│                   │ coastal salinity ingress threat.  │ 6 months in advance │
│                   │                                   │ via MTA forecasts.  │
└───────────────────┴───────────────────────────────────┴─────────────────────┘
```

---

## 7. Repository File Map & Local Reproduction Guide

### Repository Structure
```
Gujarat Monsoon gap/
├── README.md                           # Master executive briefing & complete deliverable showcase
├── PROJECT_BRIEF.md                    # Hydrogeological domain formulation & stakeholder impact
├── DATA_SOURCE_AUDIT.md                # Technical data provenance & download API specs
├── DATA_SCHEMA.md                      # 21-column data dictionary & derived metrics
├── RESEARCH_QUESTIONS.md               # 5 empirical research hypotheses
├── ANALYSIS_PLAN.md                    # Avaloka prompt sequence & code verification protocol
├── MODELLING_PLAN.md                   # 6-month lead-time predictive forecasting design
├── VALIDATION_PLAN.md                  # Scientific guardrails (depth vs storativity, Moran's I)
├── DEMO_PLAN.md                        # 120-second screen recording storyboard & spoken script
├── AGENTS.md                           # Dual-tier collaborative agent specifications
├── SUBMISSION_CHECKLIST.md             # Complete hackathon deliverable verification checklist
│
├── data/
│   ├── raw/                            # Official NWDP/CGWB CSV releases (1991–2020 & 2021–2025)
│   └── processed/
│       ├── gujarat_groundwater_analytical.csv     # 52,919 cleaned observations (10.34 MB)
│       ├── gujarat_groundwater_seasonal_paired.csv# 22,820 paired May-Nov station-years (3.2 MB)
│       └── gujarat_groundwater_model_features.csv # 21,586 ML forecasting records (3.8 MB)
│
├── avaloka-analysis/                   # Official generated deliverables from `avaloka analyze`
│   ├── d09332a26617/
│   │   ├── executive_report.html       # Visual HTML executive report (District recharge deltas)
│   │   ├── technical_report.html       # Technical report with code lineage
│   │   ├── analysis.py                 # Reproducible Python analysis script
│   │   └── data_quality.json           # Automated profiling score (76/100)
│   └── fcd4a2c44c2e/
│       ├── executive_report.html       # Visual HTML report (Hydro-zone baseline depths)
│       └── technical_report.html       # Technical report with pipeline transformations
│
├── avaloka-model/                      # Official generated deliverables from `avaloka train`
│   ├── executive_report.html           # Model executive report (Random Forest R² 0.9665)
│   ├── evaluation_report.html          # Benchmark comparisons vs trivial baseline
│   ├── model_card.md                   # Formal Model Card specification
│   └── technical_report.html           # Deployment and inference latency specifications
│
├── figures/                            # Publication-grade visualizations
│   ├── fig1_seasonal_depth_distribution.png
│   ├── fig2_monsoon_recharge_gap_scatter.png
│   ├── fig3_district_vulnerability_ranking.png
│   ├── fig4_simpsons_paradox_basalt_vs_alluvium.png
│   ├── fig5_decadal_trend_sen_slopes.png
│   └── fig6_ml_model_evaluation_and_lead_time.png
│
├── scripts/
│   ├── acquire_and_process.py          # Data ingestion & harmonization pipeline
│   ├── verify_analysis.py              # Independent statistical verification suite
│   └── generate_figures.py             # Chart rendering suite
│
└── final_report/
    ├── REPORT.md                       # Master 12-section research report
    └── EXECUTIVE_SUMMARY.md            # 2-page brief for GWRDC / CGWB leadership
```

### Local Reproduction Commands
To replicate the entire pipeline locally:

```powershell
# 1. Clone repository
git clone https://github.com/HrishiKShah28/Gujarat_monsoon_gap.git
cd "Gujarat_monsoon_gap"

# 2. Run official Avaloka CLI analysis (using local cloned engine)
$env:PYTHONPATH="C:\Users\Hrishi\Desktop\projects\avaloka_repo"
python -m avaloka.cli analyze "data\processed\gujarat_groundwater_seasonal_paired.csv" --goal "how does recharge_delta vary by district"

# 3. Launch the generated HTML executive report in your browser
Start-Process "avaloka-analysis\d09332a26617\executive_report.html"

# 4. Launch the trained model evaluation report
Start-Process "avaloka-model\executive_report.html"
```

---
*Authored with scientific rigor and domain dedication for the Avaloka AI Engineering Internship Evaluation by Hrishi K. Shah.*
