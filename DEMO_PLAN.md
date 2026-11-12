# 2-MINUTE SCREEN RECORDING SCRIPT & STORYBOARD

**Project**: The Monsoon Recharge Gap: Identifying Persistent Groundwater Stress Across Gujarat  
**Target Duration**: Exactly 120 Seconds (2 Minutes)  
**Deliverable**: Public Video Demo (YouTube Unlisted / Loom / Google Drive) for Hackathon Submission  
**Evaluator**: Indu Ganti & The Guruvai Sciences Engineering Jury  

---

## 1. Technical Recording Specifications

- **Resolution**: 1920 $\times$ 1080 (Full HD, 1080p).
- **Framerate**: 30 or 60 fps.
- **Audio Setup**: Clear microphone, quiet room, normalized audio (-3dB peak).
- **Browser State**: Clean Chrome browser window, bookmarks bar hidden, zoom at 100% or 110% for crisp typography.
- **Pacing**: Confident, articulate, professional engineering tone (~135 words per minute).

---

## 2. Second-by-Second Visual Storyboard

| Time Window | Screen Action / Focus Area | UI Element Highlighted | Narrative Focus |
| :--- | :--- | :--- | :--- |
| **0:00 – 0:15** | Open on Avaloka chat session title: *"The Monsoon Recharge Gap across Gujarat"*. Show dataset overview card. | Dataset Card: `gujarat_groundwater_analytical.csv` (CGWB/NWIC, 34-year records, 28 districts). | **The Core Problem**: India's groundwater crisis and why seasonal averages hide critical recharge failures. |
| **0:15 – 0:35** | Scroll through Prompt 1 & 2 responses. Highlight the multi-agent execution status tag: `Planner -> Coder -> Validator -> Executed`. | Agent execution pills; summary metrics table. | **Avaloka Multi-Agent Workflow**: How Avaloka decomposes queries, writes vectorized code, and executes in sandboxes. |
| **0:35 – 0:55** | Focus on Auto Insights Chart 1 & 2: The Recharge Delta Distribution and the Recharge-Deficit District Ranking. | Interactive Plotly scatter plot ($\Delta h \le 0$) and ranked horizontal bar chart. | **The Empirical Discovery**: Finding that 18% of wells exhibit a Recharge Deficit ($\Delta h \le 0$) despite monsoon rainfall. |
| **0:55 – 1:15** | Click to open the **Code Drawer** (`View Code`). Highlight Python script: grouped quantile aggregations and inner joins. | Code Drawer modal; syntax-highlighted Python; Validator safety pass badge. | **Methodological Rigor**: Inspecting code hygiene, zero-leakage temporal alignment, and Simpson's Paradox across hard-rock vs alluvial aquifers. |
| **1:15 – 1:45** | Transition to the **Model Training Agent (MTA)** output card. Show the Chronological Split (Train $\le 2018$, Test $2021\text{--}2023$) and baseline comparison. | MTA Model Card: RMSE / MAE comparison against Persistence Baseline; Feature Importance chart. | **Predictive Intelligence**: Forecasting next summer's pre-monsoon water depth with 6 months of operational lead time using MTA. |
| **1:45 – 2:00** | Switch to the final public report summary view and GitHub repository link. Conclude with operational policy impact. | Public Report Link banner; GitHub repository preview; final recommendation table. | **Real-World Impact**: Empowering GWRDC and district collectors to intervene before summer water crises strike. |

---

## 3. Spoken Audio Narration Script (Word-for-Word)

### [0:00 – 0:15] Hook & Problem Statement
*(Voiceover)*  
"Groundwater sustains over eighty percent of rural India's drinking water and sixty percent of its irrigation. But in semi-arid Gujarat, abundant monsoon rains don't always mean replenished aquifers. This is the **Monsoon Recharge Gap**—investigating whether post-monsoon groundwater recovery actually protects districts from severe summer depletion."

### [0:15 – 0:35] Avaloka Multi-Agent Architecture
*(Voiceover)*  
"To investigate this, we brought thirty-four years of official Central Ground Water Board monitoring records into **Avaloka**. When we submitted our analytical inquiries, Avaloka's **Planner Agent** decomposed our questions, the **Coder Agent** generated vectorized Python pipelines, and the **Validator Agent** verified data types and column contracts before sandboxed execution."

### [0:35 – 0:55] Core Finding: The Recharge Gap
*(Voiceover)*  
"Looking at Avaloka's automated insights, we made a striking empirical discovery: across several drought-prone districts, nearly twenty percent of monitoring wells exhibit a **negative or zero recharge delta**—meaning the water table dropped even after the monsoon. Aggregate district averages completely masked this hyper-local aquifer stress."

### [0:55 – 1:15] Inspecting Code & Hydrogeological Rigor
*(Voiceover)*  
"Opening Avaloka's **Code Drawer**, we audited the generated logic. Avaloka properly handled non-parametric medians and paired May-to-November observations per well. Furthermore, our adversarial check unmasked **Simpson's Paradox**: Saurashtra's hard-rock basalt wells show dramatic seasonal recharge, but because of low rock storativity, eighty percent is depleted by winter Rabi irrigation—unlike North Gujarat's deep, permanent alluvial depression."

### [1:15 – 1:45] Avaloka Model Training Agent (MTA) & Forecasting
*(Voiceover)*  
"To turn insight into action, we engaged Avaloka's **Model Training Agent**. Enforcing a strict chronological split—training on historical records and testing on unseen 2021 to 2023 data—the MTA trained an ensemble regressor that decisively beat the seasonal persistence baseline, predicting summer pre-monsoon water depth with six months of operational lead time."

### [1:45 – 2:00] Conclusion & Policy Value
*(Voiceover)*  
"This provides water authorities like the GWRDC an early warning system to schedule artificial recharge shafts and tanker logistics long before summer heatwaves arrive. With full reproducibility on GitHub and a public Avaloka report, this demonstrates how multi-agent data intelligence can solve India's most urgent water challenges. Thank you."

---

## 4. Rehearsal & Delivery Checklist

- [ ] **Total Word Count**: ~280 words $\to$ exactly 115–125 seconds at normal cadence.
- [ ] **Audio Clarity**: No background noise; vocal inflection on key phrases: *"Monsoon Recharge Gap"*, *"Planner and Coder agents"*, *"Code Drawer"*, *"six months lead time"*.
- [ ] **Cursor Movement**: Smooth, deliberate cursor pointing—no erratic mouse shaking.
- [ ] **Visual Sync**: Screen transitions precisely match narration milestones at 0:15, 0:35, 0:55, 1:15, and 1:45.
