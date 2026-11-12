# DATA SCHEMA & FIELD DICTIONARY

**Dataset**: Manual Quarterly Ground Water Level Telemetry  
**Source**: National Water Data Portal (NWDP / NWIC, Ministry of Jal Shakti)  
**Jurisdiction**: State of Gujarat, India (State LGD Code: 24)

---

## 1. Native NWIC 21-Column Data Dictionary

The Central Ground Water Board (CGWB) and Gujarat Surface Water & Ground Water Departments record groundwater levels using a standardized 21-column schema:

| Column Name | Raw Type | Null % | Description & Hydrogeological Role | Modeling Utility |
| :--- | :--- | :---: | :--- | :--- |
| `SlNo` | Integer | 0.0% | Serial record index. | Primary Key (Excluded from features) |
| `Station` | String | 0.0% | Unique name/identifier of the observation well or piezometer. | Categorical Entity / Grouping key |
| `Agency` | String | 0.0% | Responding monitoring agency (`CGWB` or `Gujarat SW GW`). | Source control |
| `State LGD Code` | Integer | 0.0% | Official Local Government Directory code for Gujarat (`24`). | Constant (Excluded) |
| `State` | String | 0.0% | State name (`Gujarat`). | Constant (Excluded) |
| `District LGD Code`| Integer | 0.0% | Official Ministry of Panchayati Raj district code. | Administrative key |
| `District` | String | 0.0% | Administrative district name (28 unique districts). | **Primary Spatial Stratum** |
| `Tehsil` | String | < 0.5% | Sub-district / Taluka administrative division. | High-resolution spatial feature |
| `Block` | String | ~15% | Community development block. | Spatial feature |
| `Village` | String | ~15% | Revenue village location of the well. | Spatial identifier |
| `River` | String | > 85% | Nearest major river system (mostly unpopulated). | Excluded (Sparse) |
| `Basin` | String | > 85% | Hydrographic river basin (mostly unpopulated). | Excluded (Sparse) |
| `Tributary` | String | > 90% | River tributary. | Excluded (Sparse) |
| `Subtributary` | String | > 95% | River sub-tributary. | Excluded (Sparse) |
| `SubSubtributary`| String | > 98% | Minor drainage branch. | Excluded (Sparse) |
| `Local River` | String | > 95% | Local seasonal stream name. | Excluded (Sparse) |
| `Latitude` | Float | < 0.2% | WGS84 geographic coordinate (decimal degrees). | **Spatial Feature & GIS Mapping** |
| `Longitude` | Float | < 0.2% | WGS84 geographic coordinate (decimal degrees). | **Spatial Feature & GIS Mapping** |
| `RL_MSL` | Float | > 90% | Reduced Level of well mouth relative to Mean Sea Level. | Excluded (Sparse) |
| `Data Acquisition Time`| String | 0.0% | Measurement timestamp formatted as `DD-MM-YYYY HH:MM`. | **Temporal Index** |
| `Groundwater Level Quarterly Manual (meter)` | Float | < 0.6% | **Depth to groundwater table below ground level (mbgl)** in meters. Larger numbers indicate deeper, more depleted water tables. | **Core Continuous Response Variable ($h$)** |

---

## 2. Derived & Engineered Hydrogeological Features

To analyze seasonal recharge dynamics and build predictive models in Avaloka, the pipeline derives the following standardized metrics:

### 2.1 Temporal & Seasonal Identifiers
- `measurement_date`: Clean datetime parsed from `Data Acquisition Time`.
- `year`: Integer calendar year (e.g., 2021, 2022, 2023).
- `month`: Integer calendar month (1, 5, 8, 11).
- `season_name`: Standardized CGWB hydrological season:
  - `Pre-Monsoon` (May / Month 5): Summer trough, maximum annual depletion.
  - `Mid-Monsoon` (August / Month 8): Infiltration phase during active rains.
  - `Post-Monsoon` (November / Month 11): Peak aquifer recovery after monsoon cessation.
  - `Rabi / Winter` (January / Month 1): Post-monsoon recession during winter wheat/mustard irrigation.

### 2.2 Hydrogeological Recharge Dynamics
- `water_depth_mbgl`: Normalized depth to water table in meters below ground level:
  $$\text{depth} = \text{Groundwater Level Quarterly Manual (meter)}$$
- `monsoon_recharge_recovery` ($\Delta h$): The vertical rise in the water table achieved between pre-monsoon and post-monsoon at the same monitoring station:
  $$\Delta h_t = h_{\text{Pre-Monsoon}, t} - h_{\text{Post-Monsoon}, t}$$
  - $\Delta h > 0$: Healthy aquifer recovery (water table rose closer to the surface).
  - $\Delta h \le 0$: **Recharge Deficit / Recharge Failure** (water table actually dropped deeper despite monsoon rainfall).
- `recharge_gap_flag`: Binary indicator of recharge failure ($\mathbb{I}(\Delta h \le 0.5\text{ m})$).
- `critical_depletion_flag`: Binary indicator of severe pre-monsoon stress:
  $$\text{critical\_flag} = \begin{cases} 1 & \text{if } h_{\text{Pre-Monsoon}} > 20.0\text{ mbgl} \\ 0 & \text{if } h_{\text{Pre-Monsoon}} \le 20.0\text{ mbgl} \end{cases}$$
- `hydrogeological_zone`: Regional geological grouping:
  - `North Gujarat Alluvial`: Deep alluvial multi-tier aquifer (Mehsana, Patan, Banaskantha, Gandhinagar, Sabarkantha).
  - `Saurashtra Hard-Rock`: Deccan basalt traps with low specific yield (Rajkot, Amreli, Junagadh, Jamnagar, Bhavnagar, Surendranagar).
  - `Kutch Arid`: Mesozoic sandstones and coastal saline boundary (Kachchh).
  - `South/Central Gujarat`: High-rainfall alluvial plain (Surat, Navsari, Valsad, Bharuch, Vadodara, Anand, Kheda).

---

## 3. Strict Predictive Anti-Leakage Guardrails

When training models with Avaloka's Model Training Agent (MTA) to forecast **next summer's pre-monsoon depth** ($h_{\text{Pre-Monsoon}, t+1}$):

| Permissible Features (Available Before Summer $t+1$) | Prohibited Features (Post-Event Target Leakage) |
| :--- | :--- |
| • Historical pre-monsoon depth from previous years ($h_{\text{Pre}, t}$) | • Pre-monsoon depth of year $t+1$ (The target itself) |
| • Post-monsoon depth from preceding November ($h_{\text{Post}, t}$) | • Monsoon rainfall or water levels of year $t+1$ |
| • Historical monsoon recharge delta ($\Delta h_t$) | • Any measurement taken after May 1 of year $t+1$ |
| • Station latitude, longitude, elevation, and hydro-zone | • Future station re-classifications or retrospective edits |
| • Historical seasonal precipitation anomaly of year $t$ | - |

