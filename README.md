# The Monsoon Recharge Gap: Identifying Persistent Groundwater Stress Across Gujarat

[![Avaloka Hackathon](https://img.shields.io/badge/Avaloka-AI%20Engineering%20Internship%20Hackathon-blue.svg)](https://avaloka.ai)
[![Dataset](https://img.shields.io/badge/NWIC%20%2F%20CGWB-National%20Water%20Data%20Portal-green.svg)](https://nwdp.nwic.gov.in)
[![Region](https://img.shields.io/badge/Region-Gujarat%2C%20India-orange.svg)](https://guj-nwrws.gujarat.gov.in)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](LICENSE)

---

## Executive Overview

**"The Monsoon Recharge Gap"** is an empirical hydro-informatics data science investigation developed for the **Avaloka AI Engineering Internship Hackathon** (November 13–15, 2026), hosted by **Guruvai Sciences**.

Groundwater is the invisible backbone of Gujarat's agrarian economy, drinking water security, and industrial expansion. While the state experiences heavy seasonal precipitation during the Southwest Monsoon (June–September), geological heterogeneity—ranging from deep alluvial aquifers in North Gujarat to basaltic hard-rock formations in Saurashtra and coastal saline zones in Kutch—creates profound spatial disparities in how effectively monsoonal precipitation restores the water table.

Using official government telemetry from the **National Water Data Portal (NWDP / NWIC, Ministry of Jal Shakti)** and the **Central Ground Water Board (CGWB)**, this project investigates:
1. Which districts and monitoring stations suffer from **persistent, multi-year groundwater depletion** versus merely seasonal depletion.
2. The magnitude of the **"Monsoon Recharge Gap"**: where does the monsoon fail to recharge the water table despite substantial surface rainfall?
3. Whether historical pre-monsoon and post-monsoon measurements can reliably predict **next summer's pre-monsoon groundwater depth**, enabling proactive municipal and agricultural water rationing.

A central premise of this project is our **Avaloka-first methodology**: Avaloka's multi-agent data intelligence platform ([avaloka.ai](https://avaloka.ai)) serves as the primary engine for dataset profiling, natural language query decomposition, Python code generation, automated charting, and machine learning training.

---

## Repository Structure

```
Gujarat Monsoon gap/
├── README.md                     # Project mission, architectural roadmap, and quickstart
├── PROJECT_BRIEF.md              # Regional context, hydrogeology, stakeholder impact, and objectives
├── DATA_SOURCE_AUDIT.md          # Official NWIC / CGWB data source audit, coverage, and download specs
├── DATA_SCHEMA.md                # 21-field data dictionary, data types, missingness, and derived metrics
├── RESEARCH_QUESTIONS.md         # Five empirical hydrological themes (A–E) and predictive hypotheses
├── ANALYSIS_PLAN.md              # Step-by-step Avaloka prompt playbook and code audit checks
├── MODELLING_PLAN.md             # Time-series regression & stress classification plan with MTA
├── VALIDATION_PLAN.md            # Hydrogeological integrity framework, censoring, and cross-checks
├── AVALOKA_WORKFLOW.md           # Multi-agent platform mapping (Planner, Coder, Validator, MTA)
├── DEMO_PLAN.md                  # 120-second storyboard and spoken narration for video submission
├── AGENTS.md                     # Dual-tier agent specifications (Avaloka vs. Research Team)
│
├── data/                         # Data directory (populated during execution phase)
│   ├── raw/                      # Downloaded NWIC / CGWB CSV files (2021–2025 & historical)
│   ├── processed/                # Standardized, cleaned analysis-ready datasets
│   └── data_dictionary.md        # Comprehensive metadata snapshot
│
├── scripts/                      # Standalone data acquisition and audit scripts
├── validation_scripts/           # Independent sandboxed cross-checking scripts
├── figures/                      # High-resolution charts and hydro-spatial visualizations
└── final_report/                 # Comprehensive final deliverable report and executive summary
```

---

## Target Stakeholders & Real-World Decision Impact

This investigation is designed to provide actionable intelligence for real public-sector decision-makers:
- **Gujarat Water Resources Development Corporation (GWRDC)**: Prioritizing site selection for managed aquifer recharge (MAR), check dams, and percolation tanks.
- **Central Ground Water Board (CGWB - West Central Region, Ahmedabad)**: Identifying critical and over-exploited assessment units requiring statutory groundwater extraction permits.
- **District Collectors & District Agricultural Offices (Khedut Kalyan)**: Advising crop selection (e.g., restricting water-thirsty sugarcane or summer paddy in low-recharge talukas) and coordinating emergency summer tanker supply.

---

## Technical Context: Avaloka 1.6+

Avaloka coordinates a digital workforce of specialized data science agents:
- **Planner Agent**: Decomposes natural language queries into logical stages (spatial aggregations, seasonal deltas, trend regressions).
- **Coder Agent**: Authors vectorized Python/Pandas scripts calculating depth-to-water metrics (meters below ground level - mbgl).
- **Validator Agent**: Pre-execution syntax and schema guardrail checking.
- **Execution Agent**: Sandboxed execution in Ray containerized backend.
- **Visualization Agent**: Automatically populates up to 5 interactive charts in the *Auto Insights* pane.
- **Model Training Agent (MTA)**: Enforces pre-training **Data Leakage Screening**, evaluates against seasonal baselines, and exposes inference APIs.

### Ingestion Specifications:
- **Format**: UTF-8 CSV.
- **File Limits**: Under 100 MB per file (the official NWIC Gujarat 2021–2025 dataset is **~0.81 MB**, and the full 1991–2020 dataset is **~5.38 MB**, uploading instantaneously).
- **Observation Scale**: ~6,700 recent quarterly measurements across **1,069 monitoring stations** spanning all **28 districts** of Gujarat.

---

## Project Status

- [x] Phase 0: Research Topic Formulation, Official Data Audit & Feasibility Assessment
- [x] Phase 0.5: Authoring Core Planning Documents (Architecture locked)
- [ ] Phase 1: Official NWIC/CGWB Dataset Acquisition & Harmonization
- [ ] Phase 2: Avaloka Ingestion, Schema Profiling & Auto Insights Review
- [ ] Phase 3: Spatial Stress Mapping & The Monsoon Recharge Gap Investigation
- [ ] Phase 4: Long-Term Trend Detection & Adversarial AI Claims Audit
- [ ] Phase 5: Predictive Modeling with Model Training Agent (MTA)
- [ ] Phase 6: Independent Local Verification & Report Compilation
- [ ] Phase 7: 2-Minute Screen Recording & Form Submission

> [!IMPORTANT]
> **Planning & Feasibility Phase.** No data pipeline or analysis code has been implemented yet. Awaiting formal user approval before starting execution.
