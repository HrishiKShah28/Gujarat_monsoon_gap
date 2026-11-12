import os
import sys
import urllib3
import requests
import pandas as pd
import numpy as np

# Suppress insecure SSL warnings for government portal certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DATA_RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
DATA_PROC_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")

os.makedirs(DATA_RAW_DIR, exist_ok=True)
os.makedirs(DATA_PROC_DIR, exist_ok=True)

URL_RECENT = "https://nwdp.nwic.gov.in/dataset/956add67-cba9-41a5-9d5c-96d73db44aef/resource/ef17ded9-be74-48e6-9359-f3a19daeea4a/download/gwl_manual_quarterly_cgwb_gj_2021_2025.csv"
URL_HISTORICAL = "https://nwdp.nwic.gov.in/dataset/535a095c-781e-407c-a6bd-52c6074789df/resource/8cc177be-e829-4b4d-88d1-549caa07d6a8/download/gwl_manual_quarterly_gujarat-sw-gw_gj_1991_2020.csv"

FILE_RECENT = os.path.join(DATA_RAW_DIR, "gwl_manual_quarterly_cgwb_gj_2021_2025.csv")
FILE_HISTORICAL = os.path.join(DATA_RAW_DIR, "gwl_manual_quarterly_gujarat-sw-gw_gj_1991_2020.csv")

def download_file(url, target_path, label):
    if os.path.exists(target_path) and os.path.getsize(target_path) > 100000:
        print(f"[CACHE] {label} already downloaded ({os.path.getsize(target_path) / 1024 / 1024:.2f} MB): {target_path}")
        return
    print(f"[DOWNLOAD] Sourcing {label} from NWDP...")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) GroundwaterResearch/1.0"}
    resp = requests.get(url, headers=headers, verify=False, timeout=60)
    resp.raise_for_status()
    with open(target_path, "wb") as f:
        f.write(resp.content)
    print(f"[SUCCESS] Saved {label} ({len(resp.content) / 1024 / 1024:.2f} MB) to {target_path}")

def assign_hydro_zone(district_name):
    d = str(district_name).strip().title()
    alluvial = ["Mehsana", "Patan", "Banaskantha", "Gandhinagar", "Sabarkantha", "Aravalli", "Ahmedabad"]
    saurashtra = ["Rajkot", "Junagadh", "Jamnagar", "Amreli", "Bhavnagar", "Porbandar", 
                  "Devbhumi Dwarka", "Gir Somnath", "Botad", "Surendranagar", "Morbi"]
    kachchh = ["Kachchh", "Kutch"]
    if d in alluvial:
        return "North Gujarat Alluvium"
    elif d in saurashtra:
        return "Saurashtra Hard-Rock Basalt"
    elif d in kachchh:
        return "Kachchh Arid Sedimentary"
    else:
        return "South & Central Gujarat Plain"

def harmonize_and_process():
    download_file(URL_RECENT, FILE_RECENT, "Recent Dataset (2021-2025)")
    download_file(URL_HISTORICAL, FILE_HISTORICAL, "Historical Dataset (1991-2020)")

    print("[PROCESSING] Reading CSVs...")
    df_recent = pd.read_csv(FILE_RECENT)
    df_hist = pd.read_csv(FILE_HISTORICAL)

    print(f"  Raw recent rows: {len(df_recent):,}")
    print(f"  Raw historical rows: {len(df_hist):,}")

    df_combined = pd.concat([df_hist, df_recent], ignore_index=True)
    print(f"  Combined total rows: {len(df_combined):,}")

    # Standardize column mapping
    col_map = {
        'Station': 'station_name',
        'District': 'district',
        'Tehsil': 'tehsil',
        'Block': 'block',
        'Village': 'village',
        'Latitude': 'latitude',
        'Longitude': 'longitude',
        'Agency': 'agency',
        'Basin': 'basin',
        'River': 'river',
        'Data Acquisition Time': 'data_collection_date',
        'Groundwater Level Quarterly Manual (meter)': 'depth'
    }
    df_combined = df_combined.rename(columns=col_map)

    # Standardize remaining column names
    df_combined.columns = [c.strip().lower().replace(" ", "_") for c in df_combined.columns]

    # Parse datetime (dayfirst=True for DD-MM-YYYY)
    df_combined['data_collection_date'] = pd.to_datetime(df_combined['data_collection_date'], dayfirst=True, errors='coerce')
    df_combined = df_combined.dropna(subset=['data_collection_date'])

    df_combined['year'] = df_combined['data_collection_date'].dt.year.astype(int)
    df_combined['month'] = df_combined['data_collection_date'].dt.month.astype(int)

    # Standardize district
    df_combined['district'] = df_combined['district'].astype(str).str.strip().str.title()
    # Correct common misspellings or aliases
    district_clean_map = {
        'Kutch': 'Kachchh',
        'Panch Mahals': 'Panchmahal',
        'Panchmahal': 'Panchmahal',
        'Sabarkantha': 'Sabarkantha',
        'Sabar Kantha': 'Sabarkantha',
        'Banaskantha': 'Banaskantha',
        'Banas Kantha': 'Banaskantha',
        'The Dangs': 'Dang',
        'Dangs': 'Dang'
    }
    df_combined['district'] = df_combined['district'].replace(district_clean_map)

    # Assign hydrogeological zones
    df_combined['hydro_zone'] = df_combined['district'].apply(assign_hydro_zone)

    # Map month to season
    def get_season(m):
        if m in [4, 5, 6]:
            return "Pre-Monsoon Summer (May)"
        elif m in [7, 8, 9]:
            return "Mid-Monsoon (August)"
        elif m in [10, 11, 12]:
            return "Post-Monsoon Kharif (November)"
        elif m in [1, 2, 3]:
            return "Post-Monsoon Rabi (January)"
        return "Other"

    df_combined['season'] = df_combined['month'].apply(get_season)

    # Create unique station_code
    df_combined['station_code'] = (
        df_combined['district'].astype(str).str.upper() + "_" + 
        df_combined['station_name'].astype(str).str.strip().str.upper().str.replace(" ", "_")
    )

    # Clean depth
    df_combined['depth'] = pd.to_numeric(df_combined['depth'], errors='coerce')

    # Remove invalid / non-physical depths (< 0 or > 250 mbgl)
    valid_mask = (df_combined['depth'] >= 0.0) & (df_combined['depth'] <= 250.0)
    df_clean = df_combined[valid_mask].copy()

    # Deduplicate: if station has multiple readings in same year & season, take last
    df_clean = df_clean.sort_values(['station_code', 'data_collection_date'])
    df_clean = df_clean.drop_duplicates(subset=['station_code', 'year', 'season'], keep='last')

    print(f"  Cleaned deduplicated valid observations: {len(df_clean):,}")
    print(f"  Unique monitoring stations: {df_clean['station_code'].nunique():,}")
    print(f"  Districts represented: {df_clean['district'].nunique():,}")
    print(f"  Years span: {df_clean['year'].min()} to {df_clean['year'].max()}")

    # Save master analytical dataset
    analytical_path = os.path.join(DATA_PROC_DIR, "gujarat_groundwater_analytical.csv")
    df_clean.to_csv(analytical_path, index=False)
    print(f"[SAVED] Analytical dataset saved: {analytical_path} ({os.path.getsize(analytical_path) / 1024 / 1024:.2f} MB)")

    # -------------------------------------------------------------
    # Build Paired Seasonal Recharge Dataset (Station-Year Level)
    # -------------------------------------------------------------
    print("[PROCESSING] Building paired May-November recharge dataset...")
    df_may = df_clean[df_clean['season'] == "Pre-Monsoon Summer (May)"].copy()
    df_nov = df_clean[df_clean['season'] == "Post-Monsoon Kharif (November)"].copy()
    df_jan = df_clean[df_clean['season'] == "Post-Monsoon Rabi (January)"].copy()

    # Pair May and Nov in same hydrological year
    paired = pd.merge(
        df_may[['station_code', 'station_name', 'district', 'hydro_zone', 'latitude', 'longitude', 'year', 'depth']],
        df_nov[['station_code', 'year', 'depth']],
        on=['station_code', 'year'],
        suffixes=('_may', '_nov')
    )

    # Calculate Monsoon Recharge Delta: Delta_h = depth_may - depth_nov
    # (Since depth is mbgl, higher depth = lower water table; May depth > Nov depth when recharged)
    paired['recharge_delta'] = paired['depth_may'] - paired['depth_nov']
    paired['recharge_gap_flag'] = (paired['recharge_delta'] <= 0.0).astype(int)
    paired['relative_recovery_ratio'] = (paired['recharge_delta'] / paired['depth_may']).replace([np.inf, -np.inf], np.nan)

    # Next year January (for Rabi drawdown): year t+1 January
    df_jan_next = df_jan.copy()
    df_jan_next['prev_year'] = df_jan_next['year'] - 1
    paired = pd.merge(
        paired,
        df_jan_next[['station_code', 'prev_year', 'depth']].rename(columns={'prev_year': 'year', 'depth': 'depth_jan_next'}),
        on=['station_code', 'year'],
        how='left'
    )
    # Rabi Drawdown = depth_jan_next - depth_nov (positive = water table deepened during winter)
    paired['rabi_drawdown'] = paired['depth_jan_next'] - paired['depth_nov']

    # Next year May (for predictive modeling target): year t+1 May
    df_may_next = df_may.copy()
    df_may_next['prev_year'] = df_may_next['year'] - 1
    paired = pd.merge(
        paired,
        df_may_next[['station_code', 'prev_year', 'depth']].rename(columns={'prev_year': 'year', 'depth': 'depth_may_next'}),
        on=['station_code', 'year'],
        how='left'
    )

    paired['stress_alarm_next'] = (paired['depth_may_next'] >= 15.0).astype(float)
    # If depth_may_next is null, stress_alarm_next should be NaN
    paired.loc[paired['depth_may_next'].isna(), 'stress_alarm_next'] = np.nan

    paired_path = os.path.join(DATA_PROC_DIR, "gujarat_groundwater_seasonal_paired.csv")
    paired.to_csv(paired_path, index=False)
    print(f"[SAVED] Seasonal paired dataset saved: {paired_path} ({len(paired):,} pairs)")

    # -------------------------------------------------------------
    # Build Predictive Model Feature Matrix
    # -------------------------------------------------------------
    print("[PROCESSING] Building ML feature matrix with zero data leakage...")
    # Keep only rows where depth_may_next is available
    model_df = paired.dropna(subset=['depth_may_next', 'depth_may', 'depth_nov', 'latitude', 'longitude']).copy()
    
    # Sort for trailing calculations
    model_df = model_df.sort_values(['station_code', 'year'])
    
    # Calculate 3-year trailing mean depth strictly up to year t
    model_df['trailing_depth_mean_3yr'] = model_df.groupby('station_code')['depth_nov'].transform(
        lambda x: x.shift(1).rolling(3, min_periods=1).mean()
    )
    # If trailing is NaN (first year for station), fill with current depth_nov
    model_df['trailing_depth_mean_3yr'] = model_df['trailing_depth_mean_3yr'].fillna(model_df['depth_nov'])

    # Baseline persistence error
    model_df['baseline_persistence_pred'] = model_df['depth_may']
    model_df['baseline_persistence_abs_err'] = (model_df['depth_may_next'] - model_df['depth_may']).abs()

    model_path = os.path.join(DATA_PROC_DIR, "gujarat_groundwater_model_features.csv")
    model_df.to_csv(model_path, index=False)
    print(f"[SAVED] ML feature dataset saved: {model_path} ({len(model_df):,} complete forecasting records)")
    print("[DONE] Ingestion and harmonization pipeline completed successfully!")

if __name__ == "__main__":
    harmonize_and_process()
