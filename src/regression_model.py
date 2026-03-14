"""
Mastercard IGS Challenge — Regression Model
Which indicators most predict the Inclusive Growth Score?
Uses all 7 tracts × 9 years = up to 63 observations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score, LeaveOneOut
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.inspection import permutation_importance
import os, warnings
warnings.filterwarnings('ignore')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'figure.dpi': 150,
})

MC_RED   = '#C0392B'
BLUE     = '#2980B9'
GREEN    = '#27AE60'
AMBER    = '#E67E22'
DARK     = '#1A1A2E'
GRAY     = '#7F8C8D'

# ── Load All Data ──────────────────────────────────────────────────────────
files = sorted([f for f in os.listdir('igs_exports') if f.endswith('.xlsx')])
all_data = []
for fname in files:
    df = pd.read_excel(os.path.join('igs_exports', fname), sheet_name='Compared to Urban-Rural', header=[0,1])
    df.columns = ['_'.join([str(c) for c in col]).strip() for col in df.columns]
    data_rows = df.iloc[1:].dropna(subset=['META_Census Tract FIPS code'])
    all_data.append(data_rows)

combined = pd.concat(all_data, ignore_index=True)
combined['FIPS'] = combined['META_Census Tract FIPS code'].astype(int)
combined['Year'] = combined['META_Year'].astype(int)

# ── Feature Selection ──────────────────────────────────────────────────────
FEATURES = {
    'Internet Access':        'PLACE_Internet Access Score',
    'Affordable Housing':     'PLACE_Affordable Housing Score',
    'Travel Time to Work':    'PLACE_Travel Time to Work Score',
    'Net Occupancy':          'PLACE_Net Occupancy Score',
    'Park Land':              'PLACE_Acres of Park Land Score',
    'Real Estate Value':      'PLACE_Residential Real Estate Value Score',
    'New Businesses':         'ECONOMY_New Businesses Score',
    'Small Biz Loans':        'ECONOMY_Small Business Loans Score',
    'Min/Women Biz':          'ECONOMY_Minority/Women Owned Businesses Score',
    'Labor Mkt Engagement':   'ECONOMY_Labor Market Engagement Index Score',
    'Commercial Diversity':   'ECONOMY_Commercial Diversity Score',
    'Personal Income':        'COMMUNITY_Personal Income Score',
    'Spending per Capita':    'COMMUNITY_Spending per Capita Score',
    'Female Above Poverty':   'COMMUNITY_Female Above Poverty Score',
    'Gini Coefficient':       'COMMUNITY_Gini Coefficient Score',
    'Early Education':        'COMMUNITY_Early Education Enrollment Score',
    'Health Insurance':       'COMMUNITY_Health Insurance Coverage Score',
}
TARGET = 'SUMMARY_Inclusive Growth Score'

# Build clean dataset
cols_needed = list(FEATURES.values()) + [TARGET]
df_model = combined[[c for c in cols_needed if c in combined.columns]].copy()
df_model.columns = [k for k, v in FEATURES.items() if v in combined.columns] + ['IGS']
df_model = df_model.apply(pd.to_numeric, errors='coerce')

# Drop rows where target is missing; fill feature NaNs with column median
df_model = df_model.dropna(subset=['IGS'])
for col in df_model.columns:
    if col != 'IGS':
        df_model[col] = df_model[col].fillna(df_model[col].median())

feature_names = [c for c in df_model.columns if c != 'IGS']
X = df_model[feature_names].values
y = df_model['IGS'].values

print(f"Dataset: {len(df_model)} observations, {len(feature_names)} features")
print(f"IGS range: {y.min():.0f} – {y.max():.0f}, mean: {y.mean():.1f}\n")

# ── Scale ──────────────────────────────────────────────────────────────────
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ══════════════════════════════════════════════════════════════════════════
# MODEL 1 — Ridge Regression (interpretable coefficients)
# ══════════════════════════════════════════════════════════════════════════
ridge = Ridge(alpha=1.0)
ridge.fit(X_scaled, y)
ridge_cv  = cross_val_score(ridge, X_scaled, y, cv=5, scoring='r2')
ridge_mae = cross_val_score(ridge, X_scaled, y, cv=5,
                            scoring='neg_mean_absolute_error')

print("=" * 55)
print("RIDGE REGRESSION RESULTS")
print("=" * 55)
print(f"  R² (5-fold CV):  {ridge_cv.mean():.3f} ± {ridge_cv.std():.3f}")
print(f"  MAE (5-fold CV): {-ridge_mae.mean():.2f} ± {ridge_mae.std():.2f}")

coef_df = pd.DataFrame({
    'Feature': feature_names,
    'Coefficient': ridge.coef_
}).sort_values('Coefficient', key=abs, ascending=False)
print("\n  Top Coefficients (standardised — impact per 1 SD change):")
print(coef_df.to_string(index=False))

# ══════════════════════════════════════════════════════════════════════════
# MODEL 2 — Random Forest (non-linear, feature importance)
# ══════════════════════════════════════════════════════════════════════════
rf = RandomForestRegressor(n_estimators=300, max_depth=5, random_state=42)
rf.fit(X, y)
rf_cv  = cross_val_score(rf, X, y, cv=5, scoring='r2')
rf_mae = cross_val_score(rf, X, y, cv=5, scoring='neg_mean_absolute_error')

print("\n" + "=" * 55)
print("RANDOM FOREST RESULTS")
print("=" * 55)
print(f"  R² (5-fold CV):  {rf_cv.mean():.3f} ± {rf_cv.std():.3f}")
print(f"  MAE (5-fold CV): {-rf_mae.mean():.2f} ± {rf_mae.std():.2f}")

rf_imp = pd.DataFrame({
    'Feature': feature_names,
    'Importance': rf.feature_importances_
}).sort_values('Importance', ascending=False)
print("\n  Feature Importances:")
print(rf_imp.to_string(index=False))

# ══════════════════════════════════════════════════════════════════════════
# MODEL 3 — Gradient Boosting
# ══════════════════════════════════════════════════════════════════════════
gb = GradientBoostingRegressor(n_estimators=200, max_depth=3,
                                learning_rate=0.1, random_state=42)
gb.fit(X, y)
gb_cv  = cross_val_score(gb, X, y, cv=5, scoring='r2')
gb_mae = cross_val_score(gb, X, y, cv=5, scoring='neg_mean_absolute_error')

print("\n" + "=" * 55)
print("GRADIENT BOOSTING RESULTS")
print("=" * 55)
print(f"  R² (5-fold CV):  {gb_cv.mean():.3f} ± {gb_cv.std():.3f}")
print(f"  MAE (5-fold CV): {-gb_mae.mean():.2f} ± {gb_mae.std():.2f}")

gb_imp = pd.DataFrame({
    'Feature': feature_names,
    'Importance': gb.feature_importances_
}).sort_values('Importance', ascending=False)

# ══════════════════════════════════════════════════════════════════════════
# Franklin Parish — What-If Simulation
# ══════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 55)
print("FRANKLIN PARISH — WHAT-IF SIMULATION")
print("=" * 55)

# Current Franklin 2025 values — loaded from CSV, not hardcoded
_CSV_TO_FEAT = {
    'Internet_Access': 'Internet Access', 'Affordable_Housing': 'Affordable Housing',
    'Travel_Time': 'Travel Time to Work', 'Net_Occupancy': 'Net Occupancy',
    'Park_Land': 'Park Land', 'Real_Estate': 'Real Estate Value',
    'New_Businesses': 'New Businesses', 'Small_Biz_Loans': 'Small Biz Loans',
    'Min_Women_Biz': 'Min/Women Biz', 'Labor_Engagement': 'Labor Mkt Engagement',
    'Comm_Diversity': 'Commercial Diversity', 'Personal_Income': 'Personal Income',
    'Female_Poverty': 'Female Above Poverty', 'Gini': 'Gini Coefficient',
    'Early_Education': 'Early Education', 'Health_Insurance': 'Health Insurance',
}
_fr_csv = pd.read_csv('data/franklin_parish_indicators.csv')
_fr_row  = _fr_csv[_fr_csv['Year'] == _fr_csv['Year'].max()].iloc[0]
_fr_actual_igs = int(_fr_row['IGS'])

franklin_2025_raw = {feat: float(_fr_row[csv_col]) for csv_col, feat in _CSV_TO_FEAT.items()}
franklin_2025_raw['Spending per Capita'] = np.nan  # not in IGS export; filled with median below
# Fill NaN with dataset median
for k in franklin_2025_raw:
    if pd.isna(franklin_2025_raw[k]) and k in feature_names:
        franklin_2025_raw[k] = df_model[k].median()

fr_current = np.array([franklin_2025_raw.get(f, df_model[f].median())
                        for f in feature_names]).reshape(1, -1)

pred_current_ridge = ridge.predict(scaler.transform(fr_current))[0]
pred_current_rf    = rf.predict(fr_current)[0]
pred_current_gb    = gb.predict(fr_current)[0]

print(f"\n  Current Franklin IGS (actual): {_fr_actual_igs}")
print(f"  Ridge prediction:  {pred_current_ridge:.1f}")
print(f"  RF prediction:     {pred_current_rf:.1f}")
print(f"  GB prediction:     {pred_current_gb:.1f}")

# HealthScore scenario
fr_bridgework = franklin_2025_raw.copy()
fr_bridgework['Internet Access']      = 35   # Connectivity hub
fr_bridgework['Labor Mkt Engagement'] = 30   # Remote work pipeline
fr_bridgework['Min/Women Biz']        = 40   # Incubator cohorts
fr_bridgework['Early Education']      = 35   # Childcare co-op
fr_bridgework['Travel Time to Work']  = 25   # Remote work removes commute
fr_bridgework['Commercial Diversity'] = 55   # More business diversity

fr_bw = np.array([fr_bridgework.get(f, df_model[f].median())
                  for f in feature_names]).reshape(1, -1)

pred_bw_ridge = ridge.predict(scaler.transform(fr_bw))[0]
pred_bw_rf    = rf.predict(fr_bw)[0]
pred_bw_gb    = gb.predict(fr_bw)[0]

print(f"\n  HealthScore Scenario IGS predictions:")
print(f"  Ridge: {pred_current_ridge:.1f} -> {pred_bw_ridge:.1f}  (D{pred_bw_ridge-pred_current_ridge:+.1f})")
print(f"  RF:    {pred_current_rf:.1f} -> {pred_bw_rf:.1f}  (D{pred_bw_rf-pred_current_rf:+.1f})")
print(f"  GB:    {pred_current_gb:.1f} -> {pred_bw_gb:.1f}  (D{pred_bw_gb-pred_current_gb:+.1f})")
print(f"  Average predicted IGS: {np.mean([pred_bw_ridge,pred_bw_rf,pred_bw_gb]):.1f}")

# ══════════════════════════════════════════════════════════════════════════
# CHART — 4-panel: Feature importance, Actual vs Predicted,
#                  What-if simulation, Model comparison
# ══════════════════════════════════════════════════════════════════════════
fig = plt.figure(figsize=(16, 14))
fig.suptitle('IGS Regression Analysis — Franklin Parish, LA', fontsize=16,
             fontweight='bold', y=0.98)

# Panel 1: Ridge Coefficients
ax1 = fig.add_subplot(2, 2, 1)
coef_sorted = coef_df.sort_values('Coefficient')
colors = [MC_RED if v < 0 else GREEN for v in coef_sorted['Coefficient']]
ax1.barh(coef_sorted['Feature'], coef_sorted['Coefficient'], color=colors, alpha=0.85)
ax1.axvline(0, color='black', linewidth=0.8)
ax1.set_title('Ridge Regression: Standardised Coefficients\n(impact per 1 SD change in indicator)',
              fontweight='bold', fontsize=11)
ax1.set_xlabel('Coefficient (standardised)')
green_p = mpatches.Patch(color=GREEN, label='Positive -> raises IGS')
red_p   = mpatches.Patch(color=MC_RED, label='Negative -> lowers IGS')
ax1.legend(handles=[green_p, red_p], fontsize=8)

# Panel 2: Random Forest Feature Importance
ax2 = fig.add_subplot(2, 2, 2)
rf_imp_plot = rf_imp.head(12)
bar_colors  = [MC_RED if i < 3 else BLUE if i < 7 else GRAY
               for i in range(len(rf_imp_plot))]
ax2.barh(rf_imp_plot['Feature'][::-1], rf_imp_plot['Importance'][::-1],
         color=bar_colors[::-1], alpha=0.85)
ax2.set_title('Random Forest: Feature Importance\n(top 12 predictors of IGS)',
              fontweight='bold', fontsize=11)
ax2.set_xlabel('Importance Score')

# Panel 3: Actual vs Predicted (RF)
ax3 = fig.add_subplot(2, 2, 3)
y_pred_rf = rf.predict(X)
ax3.scatter(y, y_pred_rf, alpha=0.65, color=BLUE, s=60, edgecolors='white', linewidth=0.5)
lim = [y.min()-3, y.max()+3]
ax3.plot(lim, lim, '--', color=GRAY, linewidth=1.5, label='Perfect prediction')
ax3.axhline(45, color=AMBER, linestyle=':', linewidth=1.3, label='IGS threshold (45)')
ax3.axvline(45, color=AMBER, linestyle=':', linewidth=1.3)
# Highlight Franklin 2025
ax3.scatter([38], [pred_current_rf], color=MC_RED, s=150, zorder=5,
            label=f'Franklin 2025 (pred={pred_current_rf:.1f})')
ax3.scatter([38], [pred_bw_rf], color=GREEN, s=150, marker='*', zorder=5,
            label=f'HealthScore scenario (pred={pred_bw_rf:.1f})')
ax3.annotate('->', xy=(pred_current_rf, pred_current_rf),
             xytext=(pred_bw_rf-2, pred_bw_rf+1), fontsize=12, color=GREEN)
ax3.set_xlabel('Actual IGS Score')
ax3.set_ylabel('Predicted IGS Score')
ax3.set_title(f'Actual vs Predicted IGS — Random Forest\n(R² = {r2_score(y, y_pred_rf):.3f})',
              fontweight='bold', fontsize=11)
ax3.legend(fontsize=8)

# Panel 4: What-If HealthScore simulation
ax4 = fig.add_subplot(2, 2, 4)
scenarios = ['Current\nFranklin (2025)', 'HealthScore\nYear 3 Target']
ridge_vals = [pred_current_ridge, pred_bw_ridge]
rf_vals    = [pred_current_rf,    pred_bw_rf]
gb_vals    = [pred_current_gb,    pred_bw_gb]
avg_vals   = [np.mean([pred_current_ridge, pred_current_rf, pred_current_gb]),
              np.mean([pred_bw_ridge,       pred_bw_rf,       pred_bw_gb])]

x_ = np.arange(2)
w_ = 0.2
ax4.bar(x_-w_*1.5, ridge_vals, w_, label='Ridge', color=BLUE, alpha=0.8)
ax4.bar(x_-w_*0.5, rf_vals,    w_, label='Random Forest', color=GREEN, alpha=0.8)
ax4.bar(x_+w_*0.5, gb_vals,    w_, label='Gradient Boosting', color=AMBER, alpha=0.8)
ax4.bar(x_+w_*1.5, avg_vals,   w_, label='Ensemble Average', color=DARK, alpha=0.9)
ax4.axhline(45, color=MC_RED, linestyle='--', linewidth=2, label='IGS Threshold (45)')
ax4.set_xticks(x_)
ax4.set_xticklabels(scenarios)
ax4.set_ylabel('Predicted IGS Score')
ax4.set_ylim(0, 75)
ax4.set_title('HealthScore What-If Simulation\n(All Models — Predicted IGS After Intervention)',
              fontweight='bold', fontsize=11)
ax4.legend(fontsize=8)

# Annotate average predictions
for i, (sc, av) in enumerate(zip(scenarios, avg_vals)):
    ax4.annotate(f'Avg: {av:.1f}', xy=(i+w_*1.5, av+0.8), fontsize=9,
                 fontweight='bold', color=DARK, ha='center')

plt.tight_layout()
plt.savefig('charts/08_regression_analysis.png', bbox_inches='tight')
plt.close()
print("\nSaved: charts/08_regression_analysis.png")

# ══════════════════════════════════════════════════════════════════════════
# CHART — Model comparison bar
# ══════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle('Model Performance Summary — IGS Prediction', fontweight='bold', fontsize=14)

models = ['Ridge\nRegression', 'Random\nForest', 'Gradient\nBoosting']
r2s    = [ridge_cv.mean(), rf_cv.mean(), gb_cv.mean()]
r2_std = [ridge_cv.std(),  rf_cv.std(),  gb_cv.std()]
maes   = [-ridge_mae.mean(), -rf_mae.mean(), -gb_mae.mean()]
mae_std = [ridge_mae.std(),   rf_mae.std(),   gb_mae.std()]

bar_cols = [BLUE, GREEN, AMBER]

axes[0].bar(models, r2s, color=bar_cols, alpha=0.85,
            yerr=r2_std, capsize=5)
axes[0].set_ylabel('R² Score (higher = better)')
axes[0].set_title('Cross-Validated R² (5-fold)', fontweight='bold')
axes[0].set_ylim(0, 1.1)
for i, (v, s) in enumerate(zip(r2s, r2_std)):
    axes[0].text(i, v+s+0.02, f'{v:.3f}', ha='center', fontweight='bold')

axes[1].bar(models, maes, color=bar_cols, alpha=0.85,
            yerr=mae_std, capsize=5)
axes[1].set_ylabel('Mean Absolute Error (lower = better)')
axes[1].set_title('Cross-Validated MAE (5-fold)', fontweight='bold')
for i, (v, s) in enumerate(zip(maes, mae_std)):
    axes[1].text(i, v+s+0.2, f'{v:.2f}', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('charts/09_model_comparison.png', bbox_inches='tight')
plt.close()
print("Saved: charts/09_model_comparison.png")

# ══════════════════════════════════════════════════════════════════════════
# CHART — Indicator sensitivity for Franklin Parish
# ══════════════════════════════════════════════════════════════════════════
sensitivity = {}
for j, feat in enumerate(feature_names):
    test = fr_current.copy()
    test[0, j] = min(test[0, j] + 20, 100)   # +20 point improvement
    delta = rf.predict(test)[0] - pred_current_rf
    sensitivity[feat] = delta

sens_df = pd.DataFrame.from_dict(sensitivity, orient='index', columns=['IGS_Gain'])
sens_df = sens_df.sort_values('IGS_Gain', ascending=False)

fig, ax = plt.subplots(figsize=(10, 7))
bar_c = [MC_RED if v < 2 else (AMBER if v < 4 else GREEN)
         for v in sens_df['IGS_Gain']]
ax.barh(sens_df.index[::-1], sens_df['IGS_Gain'][::-1], color=bar_c[::-1], alpha=0.85)
ax.axvline(0, color='black', linewidth=0.8)
ax.set_xlabel('Predicted IGS Gain from +20 Points on Each Indicator')
ax.set_title('Franklin Parish — Indicator Sensitivity Analysis\n'
             '(Which improvements would move the needle most?)',
             fontweight='bold', fontsize=13)
gp = mpatches.Patch(color=GREEN, label='>4 pts IGS gain — HIGH impact')
ap = mpatches.Patch(color=AMBER, label='2–4 pts IGS gain — MEDIUM')
rp = mpatches.Patch(color=MC_RED, label='<2 pts IGS gain — LOW')
ax.legend(handles=[gp, ap, rp], fontsize=9)
plt.tight_layout()
plt.savefig('charts/10_sensitivity_analysis.png', bbox_inches='tight')
plt.close()
print("Saved: charts/10_sensitivity_analysis.png")

print("\nAll regression charts saved to ./charts/")
print(f"\nFinal Ensemble HealthScore IGS Prediction: "
      f"{np.mean([pred_bw_ridge, pred_bw_rf, pred_bw_gb]):.1f} "
      f"(up from actual 38)")
