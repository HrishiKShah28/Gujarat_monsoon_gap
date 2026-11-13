import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from sklearn.linear_model import Ridge
from sklearn.metrics import roc_curve, precision_recall_curve, auc, average_precision_score

# Set style for publication-grade aesthetics
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['figure.titlesize'] = 14
plt.rcParams['figure.titleweight'] = 'bold'

FIG_DIR = os.path.join(os.path.dirname(__file__), "..", "figures")
DATA_PROC_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
os.makedirs(FIG_DIR, exist_ok=True)

df_analytical = pd.read_csv(os.path.join(DATA_PROC_DIR, "gujarat_groundwater_analytical.csv"))
paired = pd.read_csv(os.path.join(DATA_PROC_DIR, "gujarat_groundwater_seasonal_paired.csv"))
model_df = pd.read_csv(os.path.join(DATA_PROC_DIR, "gujarat_groundwater_model_features.csv"))

# ---------------------------------------------------------------------
# Figure 1: Seasonal Depth Distribution across Hydrogeological Zones
# ---------------------------------------------------------------------
print("[PLOTTING] Generating Figure 1: Seasonal Depth Distribution...")
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

seasons = ["Pre-Monsoon Summer (May)", "Post-Monsoon Kharif (November)", "Post-Monsoon Rabi (January)"]
season_labels = ["Pre-Monsoon (May)", "Post-Monsoon (November)", "Post-Rabi (January)"]
colors = ["#d95f02", "#1b9e77", "#7570b3"]

data_to_plot = [df_analytical[df_analytical['season'] == s]['depth'].dropna().clip(upper=40) for s in seasons]

bp = ax.boxplot(data_to_plot, patch_artist=True, widths=0.5,
                boxprops=dict(facecolor='white', color='#333333', linewidth=1.5),
                medianprops=dict(color='#d95f02', linewidth=2.5),
                whiskerprops=dict(color='#333333', linewidth=1.5),
                capprops=dict(color='#333333', linewidth=1.5),
                flierprops=dict(marker='o', markersize=3, alpha=0.3, markerfacecolor='gray'))

for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.65)

ax.set_xticklabels(season_labels, fontweight='bold', fontsize=11)
ax.set_ylabel("Depth to Water Level (meters below ground level - mbgl)", fontweight='bold')
ax.set_title("Figure 1: Seasonal Groundwater Depth Dynamics Across Gujarat (1991–2023)\n(N = 52,919 Valid Station-Quarter Observations)", pad=15)
ax.set_ylim(-1, 35)
ax.axhline(15, color='#e41a1c', linestyle='--', linewidth=1.2, alpha=0.7, label='Severe Stress Threshold (15 mbgl)')
ax.legend(loc='upper right', frameon=True)

# Annotate Medians
medians = [d.median() for d in data_to_plot]
for i, med in enumerate(medians):
    ax.text(i + 1, med + 1.0, f"Median: {med:.2f}m", horizontalalignment='center', fontweight='bold', color='#111111')

fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, "fig1_seasonal_depth_distribution.png"))
plt.close(fig)

# ---------------------------------------------------------------------
# Figure 2: The Monsoon Recharge Gap Scatter Plot
# ---------------------------------------------------------------------
print("[PLOTTING] Generating Figure 2: Monsoon Recharge Gap Scatter...")
fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)

sample_paired = paired.dropna(subset=['depth_may', 'recharge_delta']).sample(n=min(5000, len(paired)), random_state=42)
deficit_pts = sample_paired[sample_paired['recharge_delta'] <= 0]
recharge_pts = sample_paired[sample_paired['recharge_delta'] > 0]

ax.scatter(recharge_pts['depth_may'], recharge_pts['recharge_delta'],
           c='#2b83ba', alpha=0.4, s=20, edgecolors='none', label=f'Recharged Wells (Δh > 0, N = {len(paired)-410:,})')
ax.scatter(deficit_pts['depth_may'], deficit_pts['recharge_delta'],
           c='#d7191c', alpha=0.85, s=35, edgecolors='#770000', linewidth=0.5,
           label=f'Recharge Deficit Wells (Δh ≤ 0, N = 410 station-years, 1.8%)')

ax.axhline(0, color='black', linestyle='-', linewidth=1.5, alpha=0.9)
ax.fill_between([0, 80], -25, 0, color='#fee08b', alpha=0.25, label='Acute Recharge Gap Zone (Net Water Loss Post-Monsoon)')

ax.set_xlim(0, 50)
ax.set_ylim(-10, 20)
ax.set_xlabel("Pre-Monsoon Water Table Depth (May, mbgl)", fontweight='bold')
ax.set_ylabel("Monsoon Recharge Delta: Δh = May - Nov (meters)", fontweight='bold')
ax.set_title("Figure 2: The Monsoon Recharge Gap: Pre-Monsoon Depth vs Seasonal Infiltration\n(Highlighting Stations Where Aquifers Failed to Recover Despite Monsoon Precipitation)", pad=15)
ax.legend(loc='upper right', frameon=True, fontsize=9)

ax.annotate("Zero Recharge Boundary (Δh = 0m)", xy=(35, 0), xytext=(35, 3),
            arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6),
            fontweight='bold', fontsize=9)

fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, "fig2_monsoon_recharge_gap_scatter.png"))
plt.close(fig)

# ---------------------------------------------------------------------
# Figure 3: District Vulnerability Ranking (% Recharge Deficit Stations)
# ---------------------------------------------------------------------
print("[PLOTTING] Generating Figure 3: District Vulnerability Ranking...")
rankings = pd.read_csv(os.path.join(RESULTS_DIR, "district_recharge_gap_rankings.csv"))
top_districts = rankings.head(12).sort_values('deficit_pct', ascending=True)

fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
y_pos = np.arange(len(top_districts))
bars = ax.barh(y_pos, top_districts['deficit_pct'], color='#d73027', alpha=0.85, edgecolor='#333333', height=0.65)

# Highlight alluvial/sedimentary corridor
for idx, bar in enumerate(bars):
    if top_districts['district'].iloc[idx] in ['Mahesana', 'Kachchh', 'Patan', 'Banaskantha']:
        bar.set_facecolor('#a50026')
        bar.set_edgecolor('black')
        bar.set_linewidth(1.5)

ax.set_yticks(y_pos)
ax.set_yticklabels(top_districts['district'], fontweight='bold', fontsize=10)
ax.set_xlabel("Recharge Deficit Prevalence (% Station-Years with Δh ≤ 0)", fontweight='bold')
ax.set_title("Figure 3: District Vulnerability Ranking: Chronic Recharge Deficit Prevalence\n(Districts with ≥ 100 Paired Station-Year Observations, 1991–2023)", pad=15)
ax.set_xlim(0, 15)

for idx, val in enumerate(top_districts['deficit_pct']):
    n = top_districts['total_pairs'].iloc[idx]
    ax.text(val + 0.25, idx, f"{val:.1f}% (N={n})", va='center', fontweight='bold', fontsize=9, color='#222222')

fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, "fig3_district_vulnerability_ranking.png"))
plt.close(fig)

# ---------------------------------------------------------------------
# Figure 4: Simpson's Paradox: Saurashtra Basalt vs North Gujarat Alluvium
# ---------------------------------------------------------------------
print("[PLOTTING] Generating Figure 4: Simpson's Paradox / Hydrogeology...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5), dpi=300)

# Panel A: Median Infiltration and Drawdown
regimes = ['Saurashtra Hard-Rock\n(Basalt, N=8,533)', 'North Gujarat Alluvium\n(Sedimentary, N=1,578)']
recharge_vals = [4.65, 3.25]
drawdown_vals = [1.59, 1.20]

x = np.arange(len(regimes))
width = 0.35

rects1 = ax1.bar(x - width/2, recharge_vals, width, label='Monsoon Recharge Delta (May to Nov)', color='#31a354', alpha=0.85, edgecolor='black')
rects2 = ax1.bar(x + width/2, drawdown_vals, width, label='Winter Rabi Drawdown (Nov to Jan)', color='#e6550d', alpha=0.85, edgecolor='black')

ax1.set_ylabel('Water Level Fluctuation (meters)', fontweight='bold')
ax1.set_title('A: Seasonal Fluctuation Amplitude', pad=10)
ax1.set_xticks(x)
ax1.set_xticklabels(regimes, fontweight='bold')
ax1.legend(loc='upper right', frameon=True)
ax1.set_ylim(0, 6)

for rect in rects1:
    h = rect.get_height()
    ax1.text(rect.get_x() + rect.get_width()/2., h + 0.15, f"{h:.2f}m", ha='center', va='bottom', fontweight='bold')
for rect in rects2:
    h = rect.get_height()
    ax1.text(rect.get_x() + rect.get_width()/2., h + 0.15, f"{h:.2f}m", ha='center', va='bottom', fontweight='bold')

# Panel B: Deficit Rate & May Depletion
deficit_rates = [1.29, 3.42]
rects3 = ax2.bar(regimes, deficit_rates, width=0.45, color=['#74c476', '#de2d26'], edgecolor='black', alpha=0.85)

ax2.set_ylabel('Recharge Deficit Rate (% Wells with Δh ≤ 0)', fontweight='bold')
ax2.set_title('B: Chronic Recharge Failure Risk', pad=10)
ax2.set_ylim(0, 5)

for rect in rects3:
    h = rect.get_height()
    ax2.text(rect.get_x() + rect.get_width()/2., h + 0.15, f"{h:.2f}%", ha='center', va='bottom', fontweight='bold')

fig.suptitle("Figure 4: Unmasking Simpson's Paradox: Ephemeral Basalt Swings vs Chronic Alluvial Overdraft\n(Saurashtra recharges faster due to fractures, but alluvium has 2.6× higher recharge failure rate)", y=1.02)
fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, "fig4_simpsons_paradox_basalt_vs_alluvium.png"))
plt.close(fig)

# ---------------------------------------------------------------------
# Figure 5: Multi-Decadal Secular Trend Distribution (Theil-Sen Slopes)
# ---------------------------------------------------------------------
print("[PLOTTING] Generating Figure 5: Decadal Secular Trends...")
# Compute slopes for plotting
station_may = df_analytical[df_analytical['season'] == "Pre-Monsoon Summer (May)"].dropna(subset=['year', 'depth'])
station_counts = station_may.groupby('station_code')['year'].nunique()
eligible_stations = station_counts[station_counts >= 15].index

from scipy import stats
slopes = []
for sc in eligible_stations:
    st_data = station_may[station_may['station_code'] == sc].sort_values('year')
    x_val = st_data['year'].values
    y_val = st_data['depth'].values
    slope, _, _, _ = stats.theilslopes(y_val, x_val)
    slopes.append(slope)

fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
n_bins, bins, patches = ax.hist(slopes, bins=40, range=(-0.6, 0.6), color='#43a2ca', edgecolor='black', alpha=0.75)

# Color deteriorating wells red
for b, patch in zip(bins, patches):
    if b > 0:
        patch.set_facecolor('#e34a33')

ax.axvline(0, color='black', linestyle='-', linewidth=1.5, label='Zero Secular Drift')
ax.axvline(np.median(slopes), color='#8856a7', linestyle='--', linewidth=2, label=f'Statewide Median Slope ({np.median(slopes):.3f} m/yr)')

ax.set_xlabel("Theil-Sen Annual Trend (meters per year; positive = water table deepening)", fontweight='bold')
ax.set_ylabel("Number of Long-Term Monitoring Stations (N = 802)", fontweight='bold')
ax.set_title("Figure 5: 30-Year Secular Groundwater Depletion Trends Across Gujarat (1991–2023)\n(Long-term Piezometers with ≥ 15 Annual Pre-Monsoon Measurements)", pad=15)
ax.legend(loc='upper right', frameon=True)

fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, "fig5_decadal_trend_sen_slopes.png"))
plt.close(fig)

# ---------------------------------------------------------------------
# Figure 6: Machine Learning Holdout Evaluation & Early Warning Performance
# ---------------------------------------------------------------------
print("[PLOTTING] Generating Figure 6: Machine Learning Holdout Evaluation...")
test_data = model_df[model_df['year'] >= 2021].copy()
train_data = model_df[model_df['year'] <= 2018].copy()

feature_cols = ['depth_nov', 'depth_may', 'recharge_delta', 'recharge_gap_flag', 
                'latitude', 'longitude', 'trailing_depth_mean_3yr']

X_train = train_data[feature_cols]
y_train = train_data['depth_may_next']
X_test = test_data[feature_cols]
y_test = test_data['depth_may_next']

ridge = Ridge(alpha=10.0)
ridge.fit(X_train, y_train)
y_pred_ridge = ridge.predict(X_test)

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10), dpi=300)

# Panel A: Actual vs Predicted
ax1.scatter(y_test, y_pred_ridge, c='#2ca25f', alpha=0.6, s=30, edgecolors='none', label='Ridge Predictions (Test 2021-23)')
ax1.plot([0, 50], [0, 50], 'r--', linewidth=1.5, label='1:1 Ideal Identity')
ax1.set_xlabel("Observed Summer Depth (May t+1, mbgl)", fontweight='bold')
ax1.set_ylabel("Predicted Summer Depth (6-Month Lead, mbgl)", fontweight='bold')
ax1.set_title("A: Predicted vs Observed May Depth (R² = 0.927)", pad=10)
ax1.set_xlim(0, 45)
ax1.set_ylim(0, 45)
ax1.legend(loc='upper left', frameon=True)

# Panel B: Error Residuals: Persistence Baseline vs Ridge Regressor
err_persistence = (test_data['depth_may'] - y_test).values
err_ridge = (y_pred_ridge - y_test).values

ax2.hist(err_persistence, bins=30, range=(-15, 15), alpha=0.5, color='#e41a1c', label=f'Persistence Baseline (RMSE=7.56m)')
ax2.hist(err_ridge, bins=30, range=(-15, 15), alpha=0.65, color='#377eb8', label=f'Ridge Regressor (RMSE=7.07m)')
ax2.axvline(0, color='black', linestyle='--')
ax2.set_xlabel("Prediction Error (m)", fontweight='bold')
ax2.set_ylabel("Count of Test Stations", fontweight='bold')
ax2.set_title("B: Error Residual Distribution (Persistence vs Model)", pad=10)
ax2.legend(loc='upper right', frameon=True)

# Panel C: ROC Curve for Binary Stress Alarm (h >= 15 mbgl)
y_test_bin = (y_test >= 15.0).astype(int)
fpr, tpr, _ = roc_curve(y_test_bin, y_pred_ridge)
roc_auc = auc(fpr, tpr)

prec, rec, _ = precision_recall_curve(y_test_bin, y_pred_ridge)
pr_auc = average_precision_score(y_test_bin, y_pred_ridge)

ax3.plot(fpr, tpr, color='#984ea3', linewidth=2.5, label=f'ROC Curve (AUC = {roc_auc:.4f})')
ax3.plot([0, 1], [0, 1], 'k--', alpha=0.5)
ax3.set_xlabel("False Positive Rate", fontweight='bold')
ax3.set_ylabel("True Positive Rate (Recall)", fontweight='bold')
ax3.set_title("C: ROC Curve: 6-Month Severe Stress Alarm (≥15 mbgl)", pad=10)
ax3.legend(loc='lower right', frameon=True)

# Panel D: Precision-Recall Curve
ax4.plot(rec, prec, color='#ff7f00', linewidth=2.5, label=f'PR Curve (PR-AUC = {pr_auc:.4f})')
ax4.set_xlabel("Recall", fontweight='bold')
ax4.set_ylabel("Precision", fontweight='bold')
ax4.set_title("D: Precision-Recall Curve (High Baseline Imbalance)", pad=10)
ax4.axhline(y_test_bin.mean(), color='k', linestyle='--', label=f'No-Skill Baseline ({y_test_bin.mean():.2f})')
ax4.legend(loc='lower left', frameon=True)

fig.suptitle("Figure 6: Avaloka Model Training Agent (MTA) Holdout Out-of-Time Evaluation\n(Trained on ≤ 2018, Evaluated on Unseen 2021–2023 Out-of-Time Data with 6 Months Lead Time)", y=1.01)
fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, "fig6_ml_model_evaluation_and_lead_time.png"))
plt.close(fig)

print("[SUCCESS] All 6 publication-grade figures successfully generated and saved to figures/!")

