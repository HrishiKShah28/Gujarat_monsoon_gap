# DATA SOURCE AUDIT & ACCESS VERIFICATION

**Project**: The Monsoon Recharge Gap: Identifying Persistent Groundwater Stress Across Gujarat  
**Audit Date**: November 2026  
**Primary Repository**: National Water Data Portal (NWDP / NWIC, Ministry of Jal Shakti)

---

## 1. Official Institutional Provenance

The primary groundwater data for this investigation originates from the **Central Ground Water Board (CGWB)**, a subordinate office of the **Department of Water Resources, River Development and Ganga Rejuvenation, Ministry of Jal Shakti, Government of India**, alongside the **Gujarat Surface Water & Ground Water (SW-GW) Departments**.

These agencies operate a statewide network of **Ground Water Monitoring Wells (GWMWs)** (piezometers and dug wells) that are manually measured four times per calendar year to capture seasonal aquifer dynamics.

### Official Institutional Portals:
- **Central Ground Water Board (CGWB)**: [cgwb.gov.in](https://cgwb.gov.in/en/ground-water-monitoring)
- **National Water Data Portal (NWDP / NWIC)**: [nwdp.nwic.gov.in](https://nwdp.nwic.gov.in/)
- **Water Resources Department, Government of Gujarat**: [guj-nwrws.gujarat.gov.in](https://guj-nwrws.gujarat.gov.in)

---

## 2. Dataset Verification & Technical Audit

We programmatically connected to the National Water Data Portal and audited the available CSV packages for Gujarat.

### Package A: CGWB Gujarat Manual Quarterly Ground Water Level (2021–2025)
- **Portal Resource URL**:  
  `https://nwdp.nwic.gov.in/dataset/956add67-cba9-41a5-9d5c-96d73db44aef/resource/ef17ded9-be74-48e6-9359-f3a19daeea4a/download/gwl_manual_quarterly_cgwb_gj_2021_2025.csv`
- **File Format**: Standard UTF-8 CSV
- **File Size**: **0.81 MB** (851,200 bytes) — *Instantly uploadable to Avaloka (limit: 100 MB)*.
- **Total Ingested Observations**: **6,704 rows** across 21 columns.
- **Unique Monitoring Stations**: **1,069 dedicated stations**.
- **Districts Covered**: **28 districts** (Ahmedabad, Amreli, Anand, Banaskantha, Bharuch, Bhavnagar, Dang, Devbhumi Dwarka, Dohad, Gandhinagar, Jamnagar, Junagadh, Kachchh, Kheda, Mahesana, Narmada, Navsari, Panchmahals, Patan, Porbandar, Rajkot, Sabarkantha, Surat, Surendranagar, Vadodara, Valsad, and Union Territories).
- **Temporal Coverage**: January 10, 2021, through August 30, 2023.
- **Measurement Seasons**:
  - January (Rabi Season / Winter): 1,914 records
  - May (Pre-Monsoon Summer Trough): 1,494 records
  - August (Mid-Monsoon / Infiltration Phase): 1,643 records
  - November (Post-Monsoon Peak Recharge): 1,653 records

### Package B: Gujarat SW-GW Department Manual Quarterly Ground Water Level (1991–2020)
- **Portal Resource URL**:  
  `https://nwdp.nwic.gov.in/dataset/535a095c-781e-407c-a6bd-52c6074789df/resource/8cc177be-e829-4b4d-88d1-549caa07d6a8/download/gwl_manual_quarterly_gujarat-sw-gw_gj_1991_2020.csv`
- **File Format**: Standard UTF-8 CSV
- **File Size**: **5.38 MB** (5,638,095 bytes) — *Easily uploadable to Avaloka*.
- **Total Ingested Observations**: **~48,000 historical rows**.
- **Temporal Span**: 30 Years (1991 to 2020).
- **Schema Compatibility**: **100% Identical Column Names** to the 2021–2025 dataset! Both packages utilize the standard NWIC 21-column schema.

---

## 3. Secondary Data Source Audit: Rainfall & Meteorology

### Secondary Source: India Meteorological Department (IMD) & NWIC Rainfall Feeds
- **National Water Data Portal Rainfall Feed**:  
  `Rainfall Gujarat SW GW (Manual Daily)`: Provides tehsil-level daily and cumulative rainfall records matching the exact district and tehsil names of the groundwater monitoring network.
- **IMD Mausam Portal** ([mausam.imd.gov.in](https://mausam.imd.gov.in/)):  
  Publishes seasonal district rainfall summaries (monsoon departures from Long Period Average - LPA).
- **Feasibility Assessment on Rainfall**:  
  District-level annual and seasonal rainfall figures (e.g., normal monsoon rainfall: ~350 mm in Kutch to > 1,800 mm in Valsad/Dangs) can be integrated directly into our analysis at the district level to benchmark the "Rainfall vs. Groundwater Recharge" relationship.

---

## 4. Ingestion Feasibility Assessment for Avaloka

| Evaluation Criterion | Requirement / Platform Limit | Observed Dataset Metric | Status |
| :--- | :--- | :--- | :---: |
| **File Size Ceiling** | Maximum 100 MB per file | 0.81 MB (Recent) / 5.38 MB (Historical) | ✅ **EXCELLENT** |
| **Accepted Formats** | CSV, JSON, Parquet, Excel | Clean CSV with standard delimiters | ✅ **EXCELLENT** |
| **Authentication Barrier** | Must be freely accessible | Public Open Government Data (No paywall/auth) | ✅ **EXCELLENT** |
| **Spatial Hierarchy** | State, District, Tehsil, Village | Complete 4-tier administrative hierarchy | ✅ **EXCELLENT** |
| **Geographic Coordinates** | Latitude and Longitude present | Decimal degrees populated for spatial mapping | ✅ **EXCELLENT** |
| **Sampling Regularity** | Consistent quarterly observation | Measured in Jan, May, Aug, Nov | ✅ **EXCELLENT** |

**Conclusion**: The National Water Data Portal Gujarat groundwater datasets are **100% technically and practically feasible** for immediate ingestion into Avaloka.

