# RESEARCH QUESTIONS & INVESTIGATIVE FRAMEWORK

**Project**: The Monsoon Recharge Gap: Identifying Persistent Groundwater Stress Across Gujarat  
**Analytical Engine**: Avaloka Multi-Agent Data Intelligence Platform

---

## Overview

This investigation is organized into five core descriptive and inferential hydrogeological themes (Themes A through E) and one primary predictive machine learning inquiry. Each theme defines the exact operational question, underlying hypotheses, mathematical formulations, confounding hydrogeological variables, and the natural language prompts crafted for Avaloka.

---

## Theme A: Groundwater Stress Mapping & Spatial Disparities

### Core Questions:
1. Which districts and monitoring stations in Gujarat exhibit the deepest groundwater tables (highest meters below ground level - mbgl)?
2. What proportion of monitoring stations exceed critical depth thresholds:
   - Moderately Stressed: $> 10.0\text{ mbgl}$
   - Severely Depleted: $> 20.0\text{ mbgl}$
   - Critically Over-Exploited: $> 40.0\text{ mbgl}$
3. Do regional hydrogeological zones (North Gujarat alluvial vs. Saurashtra hard-rock vs. South Gujarat plains) exhibit statistically distinct depth distributions?

### Hypotheses:
- $H_{A1}$: North Gujarat districts (Mehsana, Patan, Banaskantha, Gandhinagar) exhibit the deepest water tables in Western India (medians $> 25\text{–}40\text{ mbgl}$, with extremes $> 100\text{ mbgl}$), driven by decades of intensive deep tube-well extraction for dairy farming and cash crops.
- $H_{A2}$: South Gujarat (Surat, Navsari, Valsad) maintains shallow water tables ($< 5\text{–}8\text{ mbgl}$) due to heavy coastal precipitation and extensive canal networks from Ukai and Sardar Sarovar dams.

### Avaloka Prompt Formulation:
> *"Analyze the spatial distribution of groundwater depth (`Groundwater Level Quarterly Manual (meter)`) across Gujarat districts. Group by District and calculate the median depth, 75th percentile, 90th percentile, and the percentage of monitoring stations with water depth > 20 meters below ground level. Create a ranked horizontal bar chart of districts by median groundwater depth."*

---

## Theme B: Monsoon Recharge Effectiveness & The "Recharge Gap"

### Core Questions:
1. How effectively does the Southwest Monsoon restore the water table between the pre-monsoon summer trough (May) and the post-monsoon peak (November)?
2. What is the state-wide distribution of net monsoon recovery ($\Delta h = h_{\text{pre}} - h_{\text{post}}$)?
3. What percentage of monitoring wells suffer from a **"Recharge Deficit"** ($\Delta h \le 0.0\text{ m}$), where the water level fails to rise or actually drops deeper despite the monsoon?
4. Which districts have the highest prevalence of failed recharge?

### Hypotheses:
- $H_{B1}$: While the majority of stations recover by 1 to 5 meters after the monsoon, a significant subset (15% to 25% of stations in arid and hard-rock belts) exhibits a **Recharge Gap** ($\Delta h \le 0.5\text{ m}$), indicating that surface precipitation is lost to rapid runoff, high evapotranspiration, or blocked infiltration.
- $H_{B2}$: Hard-rock basaltic aquifers in Saurashtra exhibit high seasonal volatility (sharp rise during monsoon, followed by rapid summer exhaustion due to low specific yield), whereas North Gujarat deep alluvial aquifers show muted seasonal recharge due to thick confining clay layers (aquitards).

### Metric Definition:
$$\Delta h_{s, t} = h_{\text{Pre-Monsoon} (s, t)} - h_{\text{Post-Monsoon} (s, t)}$$
*(calculated strictly for paired observations at the identical monitoring station $s$ in year $t$).*

### Avaloka Prompt Formulation:
> *"Filter for stations that have paired measurements in both May (Pre-Monsoon) and November (Post-Monsoon) within the same calendar year. Calculate the net monsoon recharge recovery as (Pre-Monsoon depth - Post-Monsoon depth). What is the median recharge across Gujarat? What percentage of stations exhibit a Recharge Deficit (recovery <= 0 meters)? Compare the average recharge recovery across districts."*

---

## Theme C: Multi-Year Groundwater Trajectories & Secular Decline

### Core Questions:
1. Are groundwater levels in stressed districts stabilizing, improving, or experiencing persistent secular depletion over time?
2. Which specific monitoring stations show statistically significant long-term downward trends ($dh/dt > 0$, water table getting deeper)?
3. Can we distinguish temporary meteorological drought fluctuations from permanent, non-recovering aquifer depletion?

### Hypotheses:
- $H_{C1}$: In over-exploited alluvial zones, seasonal monsoon recovery does not offset annual extraction, resulting in a persistent multi-year decline of 0.5 to 1.5 meters per year.
- $H_{C2}$: In Saurashtra, water levels fluctuate with annual monsoon rainfall but show long-term equilibrium around the base of the shallow weathered zone.

### Avaloka Prompt Formulation:
> *"For stations with observations spanning multiple years, compute the year-over-year trajectory of the pre-monsoon water table. Identify the top 20 monitoring stations with the steepest rate of groundwater depletion (fastest deepening of the water table). Plot the time-series trajectory of pre-monsoon water levels for the top 5 most critical stations."*

---

## Theme D: Rainfall vs. Groundwater Recovery Disconnect

### Core Questions:
1. Does high surface rainfall automatically guarantee proportional groundwater recharge?
2. In which districts is the correlation between rainfall volume and groundwater level recovery weakest?
3. Where does geological impermeability or urban hardscaping prevent rainwater from infiltrating the aquifer?

### Hypotheses:
- $H_{D1}$: The correlation between surface rainfall and aquifer recovery is strongly mediated by local geology: high in permeable alluvial unconfined zones, but weak in compact basalt or clay-heavy areas where excess rainfall produces surface flooding rather than groundwater recharge.

### Avaloka Prompt Formulation:
> *"Investigate the relationship between district rainfall and average monsoon groundwater recovery. Are there districts where high rainfall yields low groundwater recharge? Highlight regions where rainfall and recharge appear disconnected."*

---

## Theme E: Groundwater Vulnerability Index & Policy Prioritization

### Core Questions:
1. How can district administrations objectively prioritize villages for artificial recharge structures, check dams, and tanker deployment?
2. Can we synthesize depth, recharge failure, and trajectory into a transparent, reproducible **Groundwater Stress Index (GSI)**?

### Stress Index Formulation:
$$\text{GSI}_s = w_1 \cdot \text{DepthScore}(h_{\text{pre}}) + w_2 \cdot \text{RechargeGapScore}(\Delta h) + w_3 \cdot \text{TrendScore}\left(\frac{dh}{dt}\right)$$

### Avaloka Prompt Formulation:
> *"Develop a groundwater stress prioritization ranking across all Gujarat districts. Combine three empirical factors: (1) median pre-monsoon depth, (2) percentage of stations with a recharge deficit (recovery <= 0m), and (3) multi-year depletion rate. Classify districts into Critical, Stressed, and Stable, and generate an executive summary table for state water planners."*

---

## Predictive Modeling Question: Next-Summer Water Table Forecasting

### Core Question:
> *"Can we accurately forecast next summer's pre-monsoon groundwater depth ($h_{\text{Pre-Monsoon}, t+1}$) using only post-monsoon measurements ($h_{\text{Post-Monsoon}, t}$), station coordinates, and historical recharge dynamics?"*

### Operational Value:
If water planners know in **December** which talukas will face water table collapse by **May**, district collectors can:
1. Enforce agricultural power rationing on summer tube-wells.
2. Advance funding for village community recharge tanks.
3. Pre-contract emergency summer drinking-water tankers 4 months in advance.

### Avaloka MTA Prompt Formulation:
> *"We want to build a machine learning model to predict next summer's pre-monsoon groundwater depth (`pre_monsoon_depth_next_year`). Use ONLY features available in November: post_monsoon_depth, latitude, longitude, district, and historical average recharge. Enforce strict chronological splitting (training on earlier years, testing on the most recent year). Compare against a seasonal historical baseline and evaluate MAE, RMSE, and R²."*
