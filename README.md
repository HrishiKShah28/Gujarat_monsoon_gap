# The Monsoon Recharge Gap: Identifying Persistent Groundwater Stress Across Gujarat

[![Avaloka Hackathon](https://img.shields.io/badge/Avaloka-AI%20Engineering%20Internship%20Hackathon-blue.svg)](https://avaloka.ai)
[![Dataset](https://img.shields.io/badge/NWIC%20%2F%20CGWB-National%20Water%20Data%20Portal-green.svg)](https://nwdp.nwic.gov.in)
[![Observations](https://img.shields.io/badge/Observations-52%2C919%20Records-blue.svg)](data/processed/gujarat_groundwater_analytical.csv)
[![ROC-AUC](https://img.shields.io/badge/Holdout%20ROC--AUC-0.9675-brightgreen.svg)](results/empirical_metrics.json)
[![Region](https://img.shields.io/badge/Region-Gujarat%2C%20India-orange.svg)](https://guj-nwrws.gujarat.gov.in)

---

## Executive Overview

**"The Monsoon Recharge Gap"** is an empirical hydro-informatics data intelligence system developed for the **Avaloka AI Engineering Internship Hackathon** (November 13–15, 2026), hosted by **Guruvai Sciences** (Indu Ganti).

Groundwater is the invisible backbone of rural India, sustaining over **80% of domestic rural drinking water** and **60% of agricultural irrigation**. In semi-arid Gujarat, the common public assumption is that abundant South-West monsoon rainfall guarantees aquifer recovery for the subsequent year.

This investigation tests that assumption. Using **33 continuous years (1991–2023)** of official piezometric records from the **Central Ground Water Board (CGWB)** and the **National Water Informatics Centre (NWIC / NWDP, Ministry of Jal Shakti)**, we investigated **52,919 valid observations across 2,046 monitoring stations in all 34 districts of Gujarat**.

The entire analytical and modeling lifecycle was driven **Avaloka-first** on the [Avaloka AI Multi-Agent Platform](https://avaloka.ai), leveraging Avaloka's **Planner, Coder, Validator, Execution, Visualization, and Model Training (MTA) agents**.

---

## Key Empirical Findings Dashboard

| Metric / Indicator | Empirical Result | Hydrogeological Significance |
| :--- | :--- | :--- |
| **Analyzed Dataset Scale** | **52,919 valid observations** | 33 years (1991–2023) across 2,046 stations in 34 districts. |
| **Paired Seasonal Records** | **22,820 station-years** | Rigorously paired May pre-monsoon and November post-monsoon readings. |
| **Statewide Median Recharge** | **3.20 meters** | Median water table rise across Gujarat ($\text{IQR}: [1.40\text{m}, 6.00\text{m}]$). |
| **The Recharge Gap Prevalence** | **410 station-years (1.8%)** | Wells where groundwater failed to rise ($\Delta h \le 0$) despite monsoon rain. |
| **Top Deficit Districts** | **Mahesana (12.54%)**<br/>**Kachchh (7.65%)**<br/>**Patan (6.30%)**<br/>**Banaskantha (5.79%)** | Chronic recharge failure concentrates heavily in North Gujarat alluvium and Kachchh sedimentary formations. |
| **Simpson's Paradox Unmasked** | **Basalt vs Alluvium** | Saurashtra hard rock recharges faster ($4.65\text{m}$), but loses **34.2%** by January due to low rock storativity ($S_y \approx 1\text{--}3\%$). North Gujarat alluvium has a **2.6× higher recharge failure rate (3.42%)** and permanent deep depression ($13.5\text{ mbgl}$). |
| **Secular 30-Year Trend** | **Theil-Sen Slopes** | Gandhinagar ($100\%$), Dang ($57\%$), Banaskantha ($50\%$), and Patan ($100\%$) show persistent multi-decadal decline ($0.05\text{--}0.17\text{ m/year}$). |
| **Spatial Clustering** | **Moran's $I = 0.1604$ ($p < 0.001$)** | Statistically proves groundwater stress is clustered regionally, not random well noise. |
| **6-Month Lead-Time Forecasting** | **Holdout RMSE: 7.065 m** ($R^2 = 0.927$) | Decisively beats the seasonal persistence heuristic ($\text{RMSE} = 7.560\text{ m}$). |
| **Severe Stress Alarm ($\ge 15\text{ mbgl}$)** | **ROC-AUC: 0.9675**<br/>**PR-AUC: 0.9045** | Intercepts **81% of true pre-monsoon crises with 89% precision** with 6 months of operational lead time. |

---

## Visual Insights Suite (High-Resolution Figures)

All figures generated directly match Avaloka's Auto Insights pane outputs and are saved in `figures/`:

| Figure | Thumbnail / Focus | Description |
| :--- | :--- | :--- |
| **[Figure 1](figures/fig1_seasonal_depth_distribution.png)** | Seasonal Depth Distribution | Compares May Pre-Monsoon ($10.0\text{m}$), Nov Post-Monsoon ($5.35\text{m}$), and Jan Post-Rabi ($6.50\text{m}$) depths. |
| **[Figure 2](figures/fig2_monsoon_recharge_gap_scatter.png)** | The Recharge Gap Scatter | Scatter plot of Pre-Monsoon Depth vs Infiltration Delta, highlighting $410$ deficit wells ($\Delta h \le 0$). |
| **[Figure 3](figures/fig3_district_vulnerability_ranking.png)** | District Deficit Rankings | Ranked horizontal bar chart showing Mehsana ($12.5\%$), Kachchh ($7.6\%$), Patan ($6.3\%$), and Banaskantha ($5.8\%$). |
| **[Figure 4](figures/fig4_simpsons_paradox_basalt_vs_alluvium.png)** | Simpson's Paradox / Hydrogeology | Contrasts Saurashtra's high seasonal fluctuation and rapid winter depletion with North Gujarat's deep permanent depression. |
| **[Figure 5](figures/fig5_decadal_trend_sen_slopes.png)** | 30-Year Secular Depletion Trends | Distribution of Theil-Sen annual slopes across $802$ long-term stations with $\ge 15$ years of May records. |
| **[Figure 6](figures/fig6_ml_model_evaluation_and_lead_time.png)** | MTA Holdout ML Evaluation | 4-panel evaluation: Actual vs Predicted, Error vs Persistence Baseline, ROC Curve (AUC $0.9675$), and PR Curve ($0.9045$). |

---

## Core Planning & Submission Documents

- **[Master Research Report](final_report/REPORT.md)**: 12-section publication-grade report with complete mathematical formulations, code audits, hydrogeological interpretations, and policy recommendations.
- **[Executive Policy Brief](final_report/EXECUTIVE_SUMMARY.md)**: Concise 2-page brief for GWRDC and district collectors.
- **[Avaloka Session Log](avaloka_execution/SESSION_LOG.md)**: Turn-by-turn execution transcript showing Planner, Coder, Validator, Execution, Visualization, and MTA agents in action.
- **[Avaloka Generated Code](avaloka_execution/AVALOKA_GENERATED_CODE.py)**: Inspectable Python script generated by Avaloka's Coder Agent.
- **[2-Minute Video Demo Script & Storyboard](DEMO_PLAN.md)**: Exact second-by-second storyboard and word-for-word voiceover script for the video submission.
- **[Hackathon Submission Checklist](SUBMISSION_CHECKLIST.md)**: Step-by-step checklist ensuring compliance with all criteria from Guruvai Sciences.
- **[Data Schema & Dictionary](DATA_SCHEMA.md)**: Complete 21-column schema and derived hydrological metrics.
- **[Agent Architecture](AGENTS.md)**: Dual-tier framework (Tier 1 Avaloka Multi-Agent Core vs Tier 2 Human-in-the-Loop Research Team).

---

## Repository Structure

```
Gujarat Monsoon gap/
├── README.md                           # Master project mission, empirical dashboard, and figure links
├── PROJECT_BRIEF.md                    # Regional hydrogeology, stakeholder impact, and research premise
├── DATA_SOURCE_AUDIT.md                # Official NWIC / CGWB provenance, API endpoints, and size audits
├── DATA_SCHEMA.md                      # 21-column data dictionary and derived metrics
├── RESEARCH_QUESTIONS.md               # Five empirical hydrological research themes
├── ANALYSIS_PLAN.md                    # 5-phase Avaloka prompt playbook and code audit checks
├── MODELLING_PLAN.md                   # 6-month lead-time predictive forecasting plan via MTA
├── VALIDATION_PLAN.md                  # Scientific guardrails (depth vs storage volume, specific yield Sy)
├── AVALOKA_WORKFLOW.md                 # Avaloka platform multi-agent integration guide
├── DEMO_PLAN.md                        # 120-second storyboard and spoken narration script
├── AGENTS.md                           # Dual-tier agent collaborative specifications
├── SUBMISSION_CHECKLIST.md             # Complete hackathon deliverable verification
│
├── data/
│   ├── raw/                            # Official NWDP CSV files (2021–2025 & historical 1991–2020)
│   └── processed/
│       ├── gujarat_groundwater_analytical.csv     # 52,919 cleaned observations (10.34 MB)
│       ├── gujarat_groundwater_seasonal_paired.csv# 22,820 paired May-Nov station-years
│       └── gujarat_groundwater_model_features.csv # 21,586 zero-leakage forecasting records
│
├── avaloka_execution/
│   ├── SESSION_LOG.md                  # Multi-agent execution transcript and Validator traces
│   └── AVALOKA_GENERATED_CODE.py       # Full Python scripts from Avaloka Code Drawer
│
├── scripts/
│   ├── acquire_and_process.py          # Automated NWDP download and data harmonization pipeline
│   ├── verify_analysis.py              # Independent sandboxed verification script
│   └── generate_figures.py             # Publication-grade chart generation suite
│
├── figures/                            # 6 High-resolution publication charts
├── results/                            # Structured JSON and CSV metric summaries
└── final_report/
    ├── REPORT.md                       # Master 12-section research report
    └── EXECUTIVE_SUMMARY.md            # 2-page policy brief for GWRDC / CGWB leadership
```

---

## Project Status

- [x] **Phase 0**: Research Topic Formulation, Official Data Audit & Feasibility Assessment (Locked)
- [x] **Phase 0.5**: Authoring Core Planning Documents (All 11 documents completed)
- [x] **Phase 1**: Official NWIC/CGWB Dataset Acquisition & Harmonization (52,919 valid records)
- [x] **Phase 2**: Avaloka Multi-Agent Execution & Code Drawer Verification (Transcripts recorded)
- [x] **Phase 3**: Spatial Stress Mapping & The Monsoon Recharge Gap Investigation (Identified 410 deficit wells)
- [x] **Phase 4**: Long-Term Trend Detection & Simpson's Paradox Audit (Saurashtra vs North Gujarat unmasked)
- [x] **Phase 5**: Predictive Modeling with Model Training Agent (MTA) (ROC-AUC 0.9675, 6 months lead time)
- [x] **Phase 6**: Independent Local Verification & Master Report Compilation (`final_report/REPORT.md`)
- [x] **Phase 7**: 2-Minute Screen Recording Storyboard & Submission Package (`DEMO_PLAN.md` & `SUBMISSION_CHECKLIST.md`)

---

## Quickstart & Replication

To replicate the analysis locally:

```bash
# 1. Clone repository
git clone https://github.com/HrishiKShah28/Gujarat_monsoon_gap.git
cd Gujarat_monsoon_gap

# 2. Install dependencies
pip install pandas numpy scipy scikit-learn matplotlib requests urllib3

# 3. Run data acquisition and harmonization pipeline
python scripts/acquire_and_process.py

# 4. Run independent verification and metrics export
python scripts/verify_analysis.py

# 5. Generate publication figures
python scripts/generate_figures.py
```

*Built with passion and rigor for the Avaloka AI Engineering Internship Evaluation by Hrishi K. Shah.*
