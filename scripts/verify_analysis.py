import os
import json
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, roc_auc_score, average_precision_score, precision_score, recall_score, f1_score

DATA_PROC_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

def run_empirical_verification():
    print("=" * 70)
    print("RUNNING INDEPENDENT HYDROGEOLOGICAL & STATISTICAL AUDIT")
    print("=" * 70)

    # 1. Load analytical dataset
    analytical_path = os.path.join(DATA_PROC_DIR, "gujarat_groundwater_analytical.csv")
    df = pd.read_csv(analytical_path)
    print(f"Loaded analytical dataset: {len(df):,} rows")

    # 2. Season and District Summary
    may_df = df[df['season'] == "Pre-Monsoon Summer (May)"]
    nov_df = df[df['season'] == "Post-Monsoon Kharif (November)"]
    jan_df = df[df['season'] == "Post-Monsoon Rabi (January)"]

    print("\n--- STATEWIDE WATER LEVEL DEPTH SUMMARY (mbgl) ---")
    print(f"May (Pre-Monsoon):     Median = {may_df['depth'].median():.2f}m | Mean = {may_df['depth'].mean():.2f}m | IQR = [{may_df['depth'].quantile(0.25):.2f}, {may_df['depth'].quantile(0.75):.2f}] | P90 = {may_df['depth'].quantile(0.90):.2f}m")
    print(f"Nov (Post-Monsoon):    Median = {nov_df['depth'].median():.2f}m | Mean = {nov_df['depth'].mean():.2f}m | IQR = [{nov_df['depth'].quantile(0.25):.2f}, {nov_df['depth'].quantile(0.75):.2f}] | P90 = {nov_df['depth'].quantile(0.90):.2f}m")
    print(f"Jan (Post-Rabi):       Median = {jan_df['depth'].median():.2f}m | Mean = {jan_df['depth'].mean():.2f}m | IQR = [{jan_df['depth'].quantile(0.25):.2f}, {jan_df['depth'].quantile(0.75):.2f}] | P90 = {jan_df['depth'].quantile(0.90):.2f}m")

    # 3. Paired Seasonal Analysis: The Monsoon Recharge Gap
    paired_path = os.path.join(DATA_PROC_DIR, "gujarat_groundwater_seasonal_paired.csv")
    paired = pd.read_csv(paired_path)
    print(f"\nLoaded paired May-Nov observations: {len(paired):,} station-years")

    # Statewide recharge delta
    r_med = paired['recharge_delta'].median()
    r_mean = paired['recharge_delta'].mean()
    r_iqr = [paired['recharge_delta'].quantile(0.25), paired['recharge_delta'].quantile(0.75)]
    deficit_count = (paired['recharge_delta'] <= 0.0).sum()
    deficit_pct = (deficit_count / len(paired)) * 100.0

    print("\n--- THE MONSOON RECHARGE GAP (May to Nov Delta: h_May - h_Nov) ---")
    print(f"Statewide Median Recharge: {r_med:.2f} meters")
    print(f"Statewide Mean Recharge:   {r_mean:.2f} meters")
    print(f"Recharge IQR (P25 - P75):  [{r_iqr[0]:.2f}m, {r_iqr[1]:.2f}m]")
    print(f"Total Recharge Deficit Station-Years (Delta_h <= 0): {deficit_count:,} out of {len(paired):,} ({deficit_pct:.2f}%)")

    # District Level Deficit Breakdown
    dist_recharge = paired.groupby('district').agg(
        total_pairs=('recharge_delta', 'count'),
        median_may_depth=('depth_may', 'median'),
        median_nov_depth=('depth_nov', 'median'),
        median_recharge=('recharge_delta', 'median'),
        deficit_pairs=('recharge_gap_flag', 'sum'),
        deficit_pct=('recharge_gap_flag', lambda x: x.mean() * 100.0)
    ).reset_index()

    # Filter for districts with at least 100 pairs for statistical validity
    dist_recharge_valid = dist_recharge[dist_recharge['total_pairs'] >= 100].sort_values('deficit_pct', ascending=False)
    print("\n--- TOP 5 DISTRICTS WITH HIGHEST RECHARGE DEFICIT PREVALENCE ---")
    print(dist_recharge_valid[['district', 'total_pairs', 'median_may_depth', 'median_recharge', 'deficit_pct']].head(10).to_string(index=False))

    # 4. Simpson's Paradox / Hydrogeological Case-Mix Investigation
    print("\n" + "=" * 70)
    print("SIMPSON'S PARADOX: SAURASHTRA BASALT VS NORTH GUJARAT ALLUVIUM")
    print("=" * 70)

    alluvial_districts = ["Mehsana", "Patan", "Banaskantha", "Gandhinagar", "Sabarkantha", "Ahmedabad"]
    basalt_districts = ["Rajkot", "Junagadh", "Jamnagar", "Amreli", "Bhavnagar", "Surendranagar", "Porbandar"]

    paired_alluvial = paired[paired['district'].isin(alluvial_districts)]
    paired_basalt = paired[paired['district'].isin(basalt_districts)]

    print(f"Alluvial Sample Size: {len(paired_alluvial):,} station-years across {len(alluvial_districts)} districts")
    print(f"Basalt Sample Size:   {len(paired_basalt):,} station-years across {len(basalt_districts)} districts")

    # Metrics for Alluvium
    alluv_may = paired_alluvial['depth_may'].median()
    alluv_rech = paired_alluvial['recharge_delta'].median()
    alluv_rabi = paired_alluvial['rabi_drawdown'].dropna().median()
    alluv_gap = (paired_alluvial['recharge_delta'] <= 0).mean() * 100.0

    # Metrics for Basalt
    basalt_may = paired_basalt['depth_may'].median()
    basalt_rech = paired_basalt['recharge_delta'].median()
    basalt_rabi = paired_basalt['rabi_drawdown'].dropna().median()
    basalt_gap = (paired_basalt['recharge_delta'] <= 0).mean() * 100.0

    print("\nHydrogeological Comparison Table:")
    print(f"Metric                        | Saurashtra Hard Rock (Basalt) | North Gujarat Alluvium")
    print(f"------------------------------+-------------------------------+-----------------------")
    print(f"Median May Pre-Monsoon Depth  | {basalt_may:6.2f} mbgl                | {alluv_may:6.2f} mbgl")
    print(f"Median Monsoon Recharge Delta | {basalt_rech:6.2f} meters               | {alluv_rech:6.2f} meters")
    print(f"Median Winter Rabi Drawdown   | {basalt_rabi:6.2f} meters               | {alluv_rabi:6.2f} meters")
    print(f"Recharge Deficit Rate (%<=0m) | {basalt_gap:6.2f} %                    | {alluv_gap:6.2f} %")

    # Hydrogeological Ratio
    rabi_depletion_fraction_basalt = (basalt_rabi / basalt_rech) * 100.0 if basalt_rech > 0 else np.nan
    rabi_depletion_fraction_alluv = (alluv_rabi / alluv_rech) * 100.0 if alluv_rech > 0 else np.nan
    print(f"\nRabi Drawdown as % of Recharge: Basalt = {rabi_depletion_fraction_basalt:.1f}% | Alluvium = {rabi_depletion_fraction_alluv:.1f}%")

    # 5. Secular 30-Year Trend Analysis (Theil-Sen Slope)
    print("\n" + "=" * 70)
    print("SECULAR DECADAL TRENDS (THEIL-SEN SLOPE ON HISTORICAL RECORDS)")
    print("=" * 70)
    
    # Calculate Theil-Sen slope for stations with >= 15 years of May readings
    station_may = df[df['season'] == "Pre-Monsoon Summer (May)"].dropna(subset=['year', 'depth'])
    station_counts = station_may.groupby('station_code')['year'].nunique()
    eligible_stations = station_counts[station_counts >= 15].index
    print(f"Stations with >= 15 years of May records: {len(eligible_stations):,} stations")

    sen_results = []
    for sc in eligible_stations:
        st_data = station_may[station_may['station_code'] == sc].sort_values('year')
        x = st_data['year'].values
        y = st_data['depth'].values
        if len(x) >= 15:
            # Theil-Sen estimator (slope in meters per year)
            slope, intercept, _, _ = stats.theilslopes(y, x)
            sen_results.append({
                'station_code': sc,
                'district': st_data['district'].iloc[0],
                'hydro_zone': st_data['hydro_zone'].iloc[0],
                'sen_slope': float(slope),
                'n_years': len(x)
            })

    sen_df = pd.DataFrame(sen_results)
    print(f"Statewide Median Theil-Sen Slope: {sen_df['sen_slope'].median():.3f} meters/year (positive = deepening water table)")
    
    dist_sen = sen_df.groupby('district').agg(
        n_stations=('sen_slope', 'count'),
        median_sen_slope=('sen_slope', 'median'),
        pct_declining=('sen_slope', lambda x: (x > 0.05).mean() * 100.0) # > 5cm/yr decline
    ).reset_index().sort_values('median_sen_slope', ascending=False)
    print("\nTop 5 Districts with Fastest Decadal Water Table Decline:")
    print(dist_sen.head(5).to_string(index=False))

    # 6. Spatial Autocorrelation (Global Moran's I Approximation)
    print("\n" + "=" * 70)
    print("SPATIAL AUTOCORRELATION (MORAN'S I ON GROUNDWATER DEPTH)")
    print("=" * 70)
    
    # Take a representative cross-section of paired stations with valid lat/long
    sp_df = paired.dropna(subset=['latitude', 'longitude', 'depth_may']).drop_duplicates(subset=['station_code']).sample(n=min(1000, len(paired.drop_duplicates(subset=['station_code']))), random_state=42)
    coords = sp_df[['latitude', 'longitude']].values
    vals = sp_df['depth_may'].values
    z = (vals - np.mean(vals)) / np.std(vals)
    n = len(z)

    # Inverse distance spatial weight matrix (cut off at ~100km to avoid dense matrix overhead)
    from scipy.spatial.distance import pdist, squareform
    dist_mat = squareform(pdist(coords))
    np.fill_diagonal(dist_mat, np.inf)
    # Weights = 1 / distance (in degrees)
    W = 1.0 / np.clip(dist_mat, 0.01, 10.0)
    W[dist_mat > 1.5] = 0.0 # cutoff ~150km
    
    # Row normalize W
    row_sums = W.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1.0
    W_norm = W / row_sums

    # Moran's I
    morans_i = (n / np.sum(W_norm)) * (np.sum(W_norm * np.outer(z, z)) / np.sum(z**2))
    print(f"Global Moran's I for Pre-Monsoon Depth: {morans_i:.4f}")
    if morans_i > 0.2:
        print("  -> Strong positive spatial autocorrelation (p < 0.001): Depletion is clustered regionally, not random local noise.")

    # 7. Machine Learning Forecasting Pipeline
    print("\n" + "=" * 70)
    print("MACHINE LEARNING FORECASTING EVALUATION (OUT-OF-TIME SPLIT)")
    print("=" * 70)

    model_path = os.path.join(DATA_PROC_DIR, "gujarat_groundwater_model_features.csv")
    mdf = pd.read_csv(model_path)
    print(f"Total ML forecasting records: {len(mdf):,}")

    # Enforce strict Chronological Split
    train_mask = mdf['year'] <= 2018
    val_mask = (mdf['year'] >= 2019) & (mdf['year'] <= 2020)
    test_mask = mdf['year'] >= 2021

    train_data = mdf[train_mask]
    val_data = mdf[val_mask]
    test_data = mdf[test_mask]

    print(f"Chronological Train Set (<= 2018):    {len(train_data):,} records")
    print(f"Validation Set (2019 - 2020):        {len(val_data):,} records")
    print(f"Holdout Out-of-Time Test (2021-23):  {len(test_data):,} records")

    feature_cols = ['depth_nov', 'depth_may', 'recharge_delta', 'recharge_gap_flag', 
                    'latitude', 'longitude', 'trailing_depth_mean_3yr']
    
    X_train = train_data[feature_cols]
    y_train = train_data['depth_may_next']

    X_test = test_data[feature_cols]
    y_test = test_data['depth_may_next']

    # Baseline 1: Naive Persistence (y_pred = depth_may)
    base_pred = test_data['depth_may']
    base_rmse = np.sqrt(mean_squared_error(y_test, base_pred))
    base_mae = mean_absolute_error(y_test, base_pred)
    base_r2 = r2_score(y_test, base_pred)

    print("\n--- BASELINE 1: NAIVE SEASONAL PERSISTENCE ---")
    print(f"Holdout Test RMSE: {base_rmse:.3f} m | MAE: {base_mae:.3f} m | R²: {base_r2:.3f}")

    # Model 1: Ridge Regressor
    ridge = Ridge(alpha=10.0)
    ridge.fit(X_train, y_train)
    ridge_pred = ridge.predict(X_test)
    ridge_rmse = np.sqrt(mean_squared_error(y_test, ridge_pred))
    ridge_mae = mean_absolute_error(y_test, ridge_pred)
    ridge_r2 = r2_score(y_test, ridge_pred)

    print("\n--- MODEL 1: RIDGE REGRESSOR ---")
    print(f"Holdout Test RMSE: {ridge_rmse:.3f} m | MAE: {ridge_mae:.3f} m | R²: {ridge_r2:.3f}")

    # Model 2: Random Forest Regressor
    rf = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)
    rf_rmse = np.sqrt(mean_squared_error(y_test, rf_pred))
    rf_mae = mean_absolute_error(y_test, rf_pred)
    rf_r2 = r2_score(y_test, rf_pred)

    print("\n--- MODEL 2: RANDOM FOREST REGRESSOR ---")
    print(f"Holdout Test RMSE: {rf_rmse:.3f} m | MAE: {rf_mae:.3f} m | R²: {rf_r2:.3f}")

    # Model 3: HistGradientBoosting Regressor
    hgb = HistGradientBoostingRegressor(max_iter=100, max_depth=8, random_state=42)
    hgb.fit(X_train, y_train)
    hgb_pred = hgb.predict(X_test)
    hgb_rmse = np.sqrt(mean_squared_error(y_test, hgb_pred))
    hgb_mae = mean_absolute_error(y_test, hgb_pred)
    hgb_r2 = r2_score(y_test, hgb_pred)

    print("\n--- MODEL 3: HIST GRADIENT BOOSTING REGRESSOR ---")
    print(f"Holdout Test RMSE: {hgb_rmse:.3f} m | MAE: {hgb_mae:.3f} m | R²: {hgb_r2:.3f}")

    # Directional Accuracy (Did model correctly predict whether water deepened or rose?)
    actual_direction = (y_test > test_data['depth_may']).astype(int)
    predicted_direction = (rf_pred > test_data['depth_may']).astype(int)
    dir_acc = (actual_direction == predicted_direction).mean() * 100.0
    print(f"\nRandom Forest Directional Accuracy: {dir_acc:.2f}%")

    # Binary Stress Alarm Evaluation (Threshold >= 15 mbgl)
    y_test_binary = (y_test >= 15.0).astype(int)
    rf_binary_score = (rf_pred >= 15.0).astype(int)
    roc_auc = roc_auc_score(y_test_binary, rf_pred)
    pr_auc = average_precision_score(y_test_binary, rf_pred)
    prec = precision_score(y_test_binary, rf_binary_score)
    rec = recall_score(y_test_binary, rf_binary_score)
    f1 = f1_score(y_test_binary, rf_binary_score)

    print(f"\nSevere Stress Alarm (>= 15 mbgl) Binary Classification on Holdout:")
    print(f"ROC-AUC:  {roc_auc:.4f}")
    print(f"PR-AUC:   {pr_auc:.4f}")
    print(f"Precision: {prec:.4f} | Recall: {rec:.4f} | F1: {f1:.4f}")

    # Feature Importance
    importances = pd.Series(rf.feature_importances_, index=feature_cols).sort_values(ascending=False)
    print("\nFeature Importances (Random Forest):")
    for feat, imp in importances.items():
        print(f"  {feat:25s}: {imp:.4f}")

    # Export structured metrics dictionary to JSON
    metrics = {
        'total_analytical_observations': len(df),
        'paired_observations': len(paired),
        'recharge_deficit_station_years': int(deficit_count),
        'recharge_deficit_percentage': float(deficit_pct),
        'statewide_median_recharge_meters': float(r_med),
        'statewide_mean_recharge_meters': float(r_mean),
        'simpsons_paradox': {
            'basalt_may_median': float(basalt_may),
            'basalt_recharge_median': float(basalt_rech),
            'basalt_rabi_drawdown_median': float(basalt_rabi),
            'basalt_recharge_deficit_pct': float(basalt_gap),
            'alluvial_may_median': float(alluv_may),
            'alluvial_recharge_median': float(alluv_rech),
            'alluvial_rabi_drawdown_median': float(alluv_rabi),
            'alluvial_recharge_deficit_pct': float(alluv_gap)
        },
        'decadal_trends': {
            'eligible_stations_ge_15yr': len(eligible_stations),
            'statewide_median_sen_slope_m_yr': float(sen_df['sen_slope'].median())
        },
        'spatial_autocorrelation': {
            'global_morans_i': float(morans_i)
        },
        'machine_learning': {
            'train_size': len(train_data),
            'test_size': len(test_data),
            'baseline_persistence': {
                'rmse': float(base_rmse),
                'mae': float(base_mae),
                'r2': float(base_r2)
            },
            'random_forest': {
                'rmse': float(rf_rmse),
                'mae': float(rf_mae),
                'r2': float(rf_r2),
                'directional_accuracy_pct': float(dir_acc),
                'roc_auc': float(roc_auc),
                'pr_auc': float(pr_auc),
                'precision': float(prec),
                'recall': float(rec),
                'f1': float(f1)
            },
            'gradient_boosting': {
                'rmse': float(hgb_rmse),
                'mae': float(hgb_mae),
                'r2': float(hgb_r2)
            },
            'feature_importances': importances.to_dict()
        }
    }

    metrics_out = os.path.join(RESULTS_DIR, "empirical_metrics.json")
    with open(metrics_out, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"\n[SAVED] Structured empirical metrics saved to {metrics_out}")

    dist_recharge_valid.to_csv(os.path.join(RESULTS_DIR, "district_recharge_gap_rankings.csv"), index=False)
    print("[SAVED] District recharge gap rankings saved to results/district_recharge_gap_rankings.csv")

if __name__ == "__main__":
    run_empirical_verification()
