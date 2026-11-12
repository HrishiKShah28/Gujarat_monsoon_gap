# PREDICTIVE MODELLING PLAN: EARLY WARNING GROUNDWATER STRESS FORECASTING

**Project**: The Monsoon Recharge Gap: Identifying Persistent Groundwater Stress Across Gujarat  
**Platform**: Avaloka Model Training Agent (MTA) & Scikit-Learn Verification Engine  
**Objective**: Predict upcoming pre-monsoon water table depth ($h_{\text{May}, t+1}$) and classify acute stress risk with 6 months of operational lead time.

---

## 1. Problem Formulation & Operational Value

### Decision Timeline & Stakeholder Utility
In Gujarat, agricultural water allocations and municipal tanker emergency supplies are locked during the winter Rabi season. If district authorities (such as the Gujarat Water Resources Development Corporation - GWRDC, and District Disaster Management Authorities) wait until summer heatwaves in April/May to detect water depletion, intervention is impossible.

- **Prediction Moment ($t$)**: Late November (end of post-monsoon monitoring cycle).
- **Target Event ($t+1$)**: Mid-May (pre-monsoon summer maximum depletion).
- **Lead Time**: **6 months**.
- **Actionable Interventions Enabled**:
  1. Early rationing and timed supply of agricultural 3-phase electricity (Jyotigram Yojana) to curb overdraft in high-risk talukas.
  2. Targeted deployment of mobile artificial recharge filter shafts in recharge-gap zones.
  3. Pre-emptive budgeting and routing of drinking water tankers before village borewells run dry.

### Mathematical Formulation
We frame the modelling framework under two complementary objectives:

1. **Continuous Regression**:
   $$\text{Predict } \hat{h}_{\text{May}, t+1} \in \mathbb{R}^+ \quad \text{using only information available up to November of year } t.$$

2. **Binary Risk Classification (Severe Stress Alarm)**:
   $$\text{Predict } P(Y_{i, t+1} = 1 \mid \mathcal{F}_t) \quad \text{where } Y_{i, t+1} = \mathbb{I}(h_{\text{May}, t+1} \ge 15.0\text{ mbgl} \lor h_{\text{May}, t+1} \ge P_{75,\text{district}})$$

---

## 2. Feature Engineering & Anti-Leakage Protocol

To ensure 100% scientific honesty, every feature must be strictly computable prior to December 1st of year $t$.

### Permissible Feature Matrix ($\mathcal{F}_t$)

| Feature Group | Column / Formula | Description | Leakage Screening |
| :--- | :--- | :--- | :--- |
| **Current State** | `depth_nov_t` ($h_{\text{Nov}, t}$) | Water depth recorded in November of year $t$ | Permissible (Current) |
| **Seasonal Baseline** | `depth_may_t` ($h_{\text{May}, t}$) | Water depth recorded in May of year $t$ | Permissible (Past) |
| **Recharge Recovery** | `recharge_delta_t` ($\Delta h = h_{\text{May}, t} - h_{\text{Nov}, t}$) | Infiltration achieved during current monsoon | Permissible (Past) |
| **Recharge Ratio** | `rrr_t` ($\Delta h / h_{\text{May}, t}$) | Relative percentage recovery of the water column | Permissible (Past) |
| **Deficit Flag** | `recharge_gap_flag_t` ($\mathbb{I}(\Delta h \le 0)$) | Binary indicator of zero or negative recharge | Permissible (Past) |
| **Historical Baseline** | `rolling_mean_3yr_nov` | 3-year trailing average November water level | Permissible (Strictly historical) |
| **Secular Trend** | `sen_slope_historical` | Theil-Sen annual rate of change ($\text{m/year}$) | Permissible (Calculated up to year $t$) |
| **Spatial Coordinates** | `latitude`, `longitude` | WGS84 coordinates of monitoring station | Permissible (Static) |
| **Hydrogeology** | `hydro_zone` | Alluvial Plains vs Hard Rock Basalt vs Coastal | Permissible (Static) |
| **District Encoding** | `district_id` | Categorical one-hot or target encoded prior to split | Permissible (No future leaks) |

### Strict Anti-Leakage Safeguards (Automated Verification by MTA)
- **Forbidden Variables**:
  - NO Post-November measurements from year $t$ (e.g., January $t+1$ Rabi drawdown).
  - NO rainfall observations from year $t+1$.
  - NO future station-level targets in aggregation windows.
  - NO random K-Fold cross-validation shuffling across time.

---

## 3. Validation & Splitting Architecture: Out-Of-Time Chronological Split

Groundwater aquifers exhibit strong temporal autocorrelation and long-term climate memory. Using standard random cross-validation randomly leaks future hydrological conditions into past training data, yielding inflated, ungeneralizable performance scores.

We implement an **Out-Of-Time (OOT) Chronological Split**:

```
Time Horizon (34 Years of CGWB / NWIC Records)
├─────────────────────────────────────────┼───────────────────┼────────────────────┤
│  Historical Train Set (1991 – 2018)     │ Validation Set    │ Holdout OOT Test   │
│  ~35,000 station-year records           │ (2019 – 2020)     │ (2021 – 2023)      │
│  Model fitting & hyperparameter search   │ Model selection   │ Final evaluation   │
└─────────────────────────────────────────┴───────────────────┴────────────────────┘
```

- **Training Window (1991–2018)**: Long-term patterns, dry monsoon years (e.g., 2002, 2012 droughts), and wet cycles.
- **Validation Window (2019–2020)**: Tuning regularization penalties ($\alpha$), tree depth, and classification thresholds.
- **Holdout Test Window (2021–2023)**: Modern post-pandemic data from the newly digitized NWDP portal. **Untouched until final model lock.**

---

## 4. Benchmark Baselines & Candidate Architectures

A complex machine learning model is only justified if it decisively outperforms simple, zero-cost operational heuristics.

### Baseline Heuristics
1. **Seasonal Persistence Baseline (Trivial Heuristic)**:
   $$\hat{h}_{\text{May}, t+1} = h_{\text{May}, t}$$
   *Premise*: Assumes summer water depth next year will simply equal summer water depth this year.
2. **Post-Monsoon Scaling Baseline**:
   $$\hat{h}_{\text{May}, t+1} = h_{\text{Nov}, t} + \overline{\text{Drawdown}}_{\text{district}}$$
   *Premise*: Projects next summer's level by adding the historical mean winter/summer drawdown to current November levels.

### Candidate Machine Learning Models (Evaluated via Avaloka MTA)
1. **Regularized Linear Models (Ridge / Lasso)**:
   - Evaluates linear elasticity between recharge magnitude, historical drift, and summer depletion.
   - Provides clear, interpretable coefficients for policy stakeholders.
2. **Random Forest Regressor / Classifier**:
   - Captures non-linear thresholds (e.g., hard-rock basalt aquifers where drawdown accelerates non-linearly once water drops below fracture zones).
   - Robust against localized spatial outliers.
3. **Gradient Boosted Decision Trees (LightGBM / XGBoost / HistGradientBoosting)**:
   - Handles mixed continuous and categorical hydrogeological features efficiently.
   - Optimizes asymmetric loss functions (penalizing underestimating water depletion more heavily than overestimating).

---

## 5. Quantitative Evaluation Metrics

### For Continuous Regression ($\hat{h}_{\text{May}, t+1}$)
- **Root Mean Squared Error (RMSE)**: Penalizes severe prediction misses (in meters).
- **Mean Absolute Error (MAE)**: Median expected error in water level prediction (in meters).
- **Coefficient of Determination ($R^2$)**: Proportion of variance explained compared to the mean baseline.
- **Directional Accuracy**: Percentage of stations where the model correctly predicts whether water will rise or fall relative to year $t$.

### For Binary Stress Classification ($Y_{i, t+1} = 1$)
- **Area Under ROC Curve (ROC-AUC)**: Overall discriminative ability across all potential decision thresholds.
- **Precision-Recall AUC (PR-AUC)**: Crucial metric given class imbalance (stressed vs normal stations).
- **Recall at 80% Precision**: How many true stress emergencies can we intercept without swamping district officials with false alarms?
- **Brier Score**: Calibrated probabilistic accuracy ($\frac{1}{N}\sum (\hat{p}_i - y_i)^2$).

---

## 6. Avaloka Model Training Agent (MTA) Interaction Protocol

The user triggers the MTA in Avaloka using the following structured instructions:

```text
Avaloka MTA Request:
1. Load dataset 'gujarat_groundwater_model_features.csv'.
2. Set target variable: 'depth_may_next' (continuous) and 'stress_alarm' (binary threshold >= 15 mbgl).
3. Enforce Chronological Split:
   - Training years: <= 2018
   - Validation years: 2019 - 2020
   - Test years: 2021 - 2023
4. Verify zero data leakage: confirm no features contain data from after November of observation year t.
5. Benchmark against the Persistence Baseline (depth_may_next = depth_may_current).
6. Train and tune:
   - Ridge Regressor (with standard scaling)
   - Random Forest Regressor (n_estimators=100, max_depth=8)
   - Gradient Boosting Regressor
7. Compare holdout RMSE, MAE, R², and feature importances.
8. Output the model evaluation card and inference prediction table.
```
