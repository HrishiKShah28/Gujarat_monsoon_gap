# PROJECT BRIEF: The Monsoon Recharge Gap

**Groundwater Stress Intelligence for Gujarat, India**  
**Avaloka AI Engineering Internship Hackathon**  
*Organized by Guruvai Sciences (Indu Ganti)*

---

## 1. Regional Context & The Hydrogeological Reality of Gujarat

Gujarat is one of India's most economically dynamic states, leading in industrial manufacturing, dairy cooperatives (Amul), and high-value agriculture (cotton, groundnut, castor, cumin, wheat). However, this economic prosperity rests upon an extraordinarily fragile foundation: **groundwater**.

Over 80% of Gujarat's rural drinking water and more than 60% of its irrigated agriculture depend directly on groundwater extracted via tube wells and dug wells. Yet, Gujarat's hydrogeology is among the most diverse and stressed in South Asia:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   GUJARAT HYDROGEOLOGICAL SUB-REGIONS                  │
├──────────────────────┬────────────────────────┬────────────────────────┤
│ 1. North Gujarat     │ 2. Saurashtra          │ 3. Kutch & Coastal     │
│ (Mehsana, Patan,     │ (Rajkot, Amreli,       │ (Kachchh, Jamnagar,    │
│ Banaskantha, G'nagar)│ Junagadh, Bhavnagar)   │ Porbandar, Dwarka)     │
├──────────────────────┼────────────────────────┼────────────────────────┤
│ • Deep multi-layered │ • Hard-rock basaltic   │ • Arid/semi-arid       │
│   alluvial aquifers  │   Deccan traps         │   sandstone & coastal  │
│ • Excessive tube-well│ • Shallow weathered    │ • Low annual rainfall  │
│   depth (> 100m mbgl)│   zone (low storage)   │ • High risk of marine  │
│ • Over-exploited /   │ • Rapid post-monsoon   │   saline water ingress │
│   critical status    │   depletion in summer  │   into fresh aquifers  │
└──────────────────────┴────────────────────────┴────────────────────────┘
```

---

## 2. The Core Problem: The "Monsoon Recharge Gap"

The Southwest Monsoon (June to September) delivers over 90% of Gujarat's annual precipitation. In an ideal hydrological cycle, monsoonal rainfall infiltrates the soil and recharges the shallow aquifer, causing the water table to rise significantly between the pre-monsoon measurement (May) and the post-monsoon measurement (November).

However, in many districts, the water table **fails to recover adequately**, creating a **"Monsoon Recharge Gap"**:
$$\text{Recharge Gap} = \Delta h_{\text{monsoon}} = h_{\text{pre-monsoon}} - h_{\text{post-monsoon}}$$
*(where $h$ is depth to water level below ground level in meters; a smaller or negative $\Delta h$ signifies failed recharge).*

When this recharge gap persists year after year, it leads to:
1. **Permanent Aquifer Depletion**: Pumping costs soar, smallholder farmers are priced out of deep borewells, and village drinking-water wells run dry before March.
2. **Fluoride and Salinity Contamination**: Deep over-pumping pulls ancient, mineralized water containing toxic fluoride and arsenic concentrations exceeding BIS standards.
3. **Emergency Water Tanker Dependency**: District administrations are forced to deploy thousands of water tankers to water-scarce talukas during the pre-monsoon heat.

---

## 3. Real Decision-Makers & Policy Stakeholders

This investigation is built around concrete public policy decisions:

| Public Stakeholder | Core Operational Decision | How Our Analysis Influences the Decision |
| :--- | :--- | :--- |
| **Gujarat Water Resources Development Corporation (GWRDC)** | Site selection and capital budget allocation for artificial recharge structures (check dams, recharge shafts, percolation tanks). | Identifies monitoring stations with high vadose zone storage capacity that consistently fail to recharge, highlighting ideal recharge sites. |
| **Central Ground Water Board (CGWB - West Central Region)** | Annual National Compilation on Dynamic Ground Water Resources (categorizing assessment units as *Safe, Semi-Critical, Critical, or Over-Exploited*). | Provides granular quarterly station-level trajectory analysis, detecting micro-hotspots before entire blocks are categorized as over-exploited. |
| **Department of Agriculture & Farmers Welfare (Khedut Kalyan)** | Cropping pattern advisories and micro-irrigation subsidy prioritization (drip/sprinkler adoption). | Warns farmers in advance of upcoming summer depletion, advising against water-intensive summer crops (e.g., summer groundnut or sugarcane). |
| **District Collectors & Taluka Development Officers (TDOs)** | Pre-monsoon drought contingency planning and drinking water tanker budgeting. | Flags villages and monitoring wells likely to breach critical depth thresholds ($> 20$ mbgl) months before peak summer arrives. |

---

## 4. The "Avaloka-First" Data Intelligence Philosophy

Rather than building an isolated analysis in Jupyter notebooks, we leverage **Avaloka** ([avaloka.ai](https://avaloka.ai)) as our central AI workforce:
- We upload official government groundwater telemetry directly into Avaloka.
- We observe the **Planner Agent** decompose complex hydrogeological inquiries into multi-stage queries.
- We inspect the Python code authored by the **Coder Agent** to verify that depth measurements (meters below ground level - mbgl) are handled without direction confusion.
- We evaluate the **Visualization Agent's** automated charts in the *Auto Insights* pane.
- We use the **Model Training Agent (MTA)** to test whether historical quarterly patterns can forecast future pre-monsoon water tables with zero target leakage.
- We critically challenge AI-generated assertions (e.g., distinguishing between physical groundwater depth and actual extractable water yield).

---

## 5. Deliverables & Acceptance Criteria

1. **Public Avaloka Project Link**: An active, shareable Avaloka workspace showing dataset profiling, chat prompts, Auto Insights charts, and Model Training Agent cards.
2. **2-Minute Screen Demonstration**: Crisp, focused walkthrough showing the Gujarat groundwater problem, official NWIC dataset, Avaloka code execution, challenging an AI finding, and real-world policy takeaways.
3. **Comprehensive Evidence-Backed Final Report**: A 12-section hydrogeological report featuring verified statistics, maps, district comparisons, and policy recommendations.
4. **Reproducible GitHub Repository**: Complete open-source code, data audits, and validation scripts committed to `https://github.com/HrishiKShah28/Gujarat_monsoon_gap`.

