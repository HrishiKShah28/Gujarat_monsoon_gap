# AVALOKA MULTI-AGENT WORKFLOW & PLATFORM INTEGRATION GUIDE

**Platform**: Avaloka AI Multi-Agent Data Intelligence Platform ([avaloka.ai](https://avaloka.ai))  
**Repository**: [guruvaidev/avaloka](https://github.com/guruvaidev/avaloka)  
**Hackathon Target**: Avaloka AI Engineering Internship Evaluation (Guruvai Sciences)  

---

## 1. Avaloka System Architecture & Multi-Agent Graph

Avaloka is an autonomous digital workforce platform designed to transform natural language user inquiries into rigorous, executed data science workflows. Unlike simple code-completion LLMs or static chatbots, Avaloka operates an internal multi-agent graph with specialized roles, pre-execution validation gates, sandboxed compute, and automated visualization engines.

```mermaid
graph TD
    User(["Lead Investigator (UI Chat)"]) -->|Natural Language Prompt| Planner["Planner Agent<br/>(Intent Decomposition & DAG Routing)"]
    
    subgraph MultiAgentCore["Avaloka Multi-Agent Core Engine"]
        Planner -->|Analytical Subtask| Coder["Coder Agent<br/>(Vectorized Python Authoring)"]
        Coder -->|Raw Python Script| Validator["Validator Agent<br/>(Schema & Syntax Guard)"]
        Validator -->|Syntax/Schema Failure: Retry Loop| Coder
        Validator -->|Validation Pass| Exec["Execution Agent<br/>(Sandboxed Ray / Containerized Compute)"]
        Exec -->|Output Tables & DataFrames| Viz["Visualization Agent<br/>(Auto Insights Pane: Plotly/Vega)"]
        Planner -->|ML Training Request| MTA["Model Training Agent (MTA)<br/>(Leakage Screen, Baselines & Tuning)"]
        MTA --> Exec
    end

    Exec -->|Execution Logs & Tables| UI_Response["Chat Response & Table View"]
    Viz -->|Interactive Charts (Max 5)| UI_AutoInsights["Auto Insights Pane"]
    MTA -->|Model Card & Evaluation Metrics| UI_ModelCard["Model Registry & Inference Card"]
    Coder -->|Full Python Scripts| UI_CodeDrawer["Inspectable Code Drawer"]

    UI_Response & UI_AutoInsights & UI_ModelCard & UI_CodeDrawer --> User
```

---

## 2. Deep Dive: Avaloka Agent Roles & Behavioral Contracts

### 1. Planner Agent (Decomposition & Routing)
- **Role**: Parses multi-part analytical prompts, validates domain entity alignment (e.g., distinguishing administrative `district` from hydrogeological `zone`), constructs a Directed Acyclic Graph (DAG) of analytical operations, and delegates tasks to worker agents.
- **Key Capability**: Maintains session state across iterative conversational turns, remembering earlier filtered subsets without requiring the user to re-upload data.

### 2. Coder Agent (High-Performance Python Authoring)
- **Role**: Translates the Planner's logical instructions into idiomatic, vectorized Python code using `pandas`, `numpy`, `scipy`, and `scikit-learn`.
- **Quality Standards**: Avoids deprecated Pandas syntax, handles NaN values explicitly without silent zero-filling, and enforces vectorized aggregations for speed.

### 3. Validator Agent (Pre-Execution Safety & Schema Gate)
- **Role**: Serves as the automated quality assurance firewall before any script touches the execution sandbox.
- **Checks Performed**:
  - Verifies that all referenced columns exist in the active dataset schema.
  - Checks for data type compatibility (e.g., ensuring `data_collection_date` is parsed as `datetime64` before extracting `.dt.year`).
  - Detects infinite loops, dangerous shell commands, or unconstrained memory allocations.
  - If a check fails, returns a precise error trace to the Coder Agent for self-correction without exposing raw errors to the user.

### 4. Execution Agent (Sandboxed Distributed Runtime)
- **Role**: Safely executes validated scripts inside an isolated containerized environment (backed by Ray distributed execution).
- **Outputs Captured**: Standard output, computed DataFrames, structured metric dictionaries, memory usage, and execution elapsed time.

### 5. Visualization Agent (Auto Insights Engine)
- **Role**: Inspects tabular outputs and automatically selects, formats, and renders up to 5 interactive data visualizations in Avaloka's dedicated **Auto Insights** pane.
- **Chart Selection Logic**:
  - Continuous distribution $\to$ Boxplots, violin plots, KDE curves.
  - Seasonal time series $\to$ Multi-line quarterly trend plots.
  - Bivariate associations $\to$ Scatter plots with trendlines.
  - Geospatial rankings $\to$ Ranked horizontal bar charts and geographical heatmaps.

### 6. Model Training Agent (MTA)
- **Role**: Orchestrates end-to-end predictive machine learning workflows within the chat session.
- **Key Modules**:
  - *Automated Leakage Screen*: Audits candidate features against target timestamp boundaries.
  - *Data Splitting Engine*: Enforces chronological or stratified train/test partitions.
  - *Baseline Engine*: Fits trivial heuristics (e.g., persistence model) to establish non-zero benchmark thresholds.
  - *Candidate Model Suite*: Fits regularized linear models, Random Forests, and Gradient Boosting ensembles.
  - *Evaluation & Inference Suite*: Produces interactive ROC/PR curves, confusion matrices, feature importance rankings, and an interactive prediction card.

---

## 3. Step-by-Step UI Execution Protocol for Gujarat Groundwater

Follow this step-by-step workflow in the Avaloka web interface ([avaloka.ai](https://avaloka.ai)):

### Step 1: Account Login & Dataset Registration
1. Navigate to [avaloka.ai](https://avaloka.ai) and sign in.
2. Click **New Analysis Session** or **Upload Dataset**.
3. Upload the curated file: `gujarat_groundwater_analytical.csv` (~6.2 MB).
4. Allow Avaloka to inspect the file: observe the automated schema recognition and profiling card (confirming 28 districts, quarterly dates from 1991 to 2023, and depth in mbgl).

### Step 2: Phase 1 Profiling & Spatial Distribution
- **Submit Prompt**:
  > *"Analyze the spatial and seasonal distribution of groundwater depths across Gujarat. Compute the median, 25th percentile, 75th percentile, and 90th percentile of depth (mbgl) grouped by district and season (January, May, August, November). Show a summary table and generate a comparative visualization of summer (May) vs post-monsoon (November) depths."*
- **UI Inspection**:
  - Open the **Code Drawer** (click `View Code` or code icon).
  - Verify that Coder Agent used `.groupby(['district', 'quarter'])['depth'].quantile(...)`.
  - Check the **Auto Insights** pane for the comparative bar chart.

### Step 3: Phase 2 The Monsoon Recharge Gap Investigation
- **Submit Prompt**:
  > *"For each monitoring station and hydrological year, pair the May pre-monsoon reading with the November post-monsoon reading to calculate the Monsoon Recharge Delta: Delta_h = May_depth - November_depth (in meters). Identify stations where Delta_h <= 0 (indicating a Recharge Deficit where groundwater failed to rise after the monsoon). What percentage of stations in each district experience a recharge deficit? Rank the top 5 most vulnerable districts."*
- **UI Inspection**:
  - Check how the Validator Agent ensured inner joins on `station_code` and `year`.
  - Review the ranked district table and scatter plot in the Auto Insights pane.

### Step 4: Phase 3 Multi-Decadal Secular Trend Estimation
- **Submit Prompt**:
  > *"Using the historical records for stations with at least 15 annual May observations, calculate the multi-decadal rate of groundwater table change (in meters per year) using the Theil-Sen slope estimator. Which districts show statistically significant long-term depletion, and which show stability or recovery?"*
- **UI Inspection**:
  - Verify that Coder used `scipy.stats.theil_sen` or `mktemp`.
  - Inspect output distribution of Sen's slopes across Gujarat districts.

### Step 5: Phase 4 Simpson's Paradox Hydrogeological Audit
- **Submit Prompt**:
  > *"Compare the groundwater dynamics between North Gujarat Alluvial districts (Mehsana, Patan, Banaskantha, Gandhinagar) and Saurashtra Hard-Rock Basalt districts (Rajkot, Junagadh, Jamnagar, Amreli, Bhavnagar). Compute the median pre-monsoon depth, median monsoon recharge, and median post-monsoon Rabi drawdown for both groups. Do Saurashtra hard-rock aquifers show higher seasonal recharge but faster winter depletion than North Gujarat alluvium?"*
- **UI Inspection**:
  - Observe how Avaloka decomposes the query across geological zones.
  - Examine the comparative boxplot demonstrating the rapid recharge and rapid drawdown of Saurashtra vs deep depression in North Gujarat.

### Step 6: Phase 5 Predictive Modelling via MTA
- **Submit Prompt**:
  > *"Train a machine learning model to predict next summer's pre-monsoon water depth (May depth at t+1) using only data available up to November of year t. Use a strict chronological split (train on data <= 2018, test on 2021-2023). Benchmark against a persistence baseline (May depth t+1 = May depth t). Train a Random Forest and Gradient Boosting regressor, compare RMSE and MAE, and show feature importances."*
- **UI Inspection**:
  - Observe the Model Training Agent launching its workflow.
  - Review the Model Evaluation Card, comparing candidate models to the persistence heuristic.
  - Inspect the top predictive features (e.g., current November depth, prior May depth, recharge delta).

### Step 7: Artifact Capture & Public Report Generation
1. Click **Share / Export** in Avaloka to generate the public read-only link.
2. Download the high-resolution charts from the Auto Insights pane.
3. Copy the Python execution snippets from the Code Drawer into our documentation suite.
4. Record the 2-minute walkthrough showing these exact steps in action.

