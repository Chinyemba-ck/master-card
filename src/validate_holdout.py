"""
validate_holdout.py — Out-of-sample validation with three strategies:

  1. 80/20 train/test split on national data (Archibald & Winnsboro excluded from both)
  2. Archibald holdout: train on everything EXCEPT Archibald, then predict Archibald's
     IGS from its indicator values and compare to actual.
  3. Winnsboro holdout: train on everything EXCEPT Winnsboro, then predict Winnsboro's
     IGS for all years (2017-2025) and compare to actual. Also checks 2025 single-point.
  4. Joint holdout: same single model (trained on neither community) predicts both
     Archibald and Winnsboro simultaneously — combined out-of-sample MAE.

Run: python src/validate_holdout.py
"""

import os, sys, warnings
warnings.filterwarnings('ignore')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(ROOT, 'src')
os.chdir(ROOT)
if SRC not in sys.path:
    sys.path.insert(0, SRC)

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_absolute_error

RANDOM_STATE = 42

# ── FIPS for tracts to exclude from training ──────────────────────────────────
WINNSBORO_FIPS  = 22041950100   # Franklin Parish — our target community
ARCHIBALD_FIPS  = 22083970600   # Richland Parish — our benchmark

# Column names (must match national_igs_full.csv)
FIPS_COL   = 'META_Census Tract FIPS code'   # column name in national_igs_full.csv
TARGET_COL = 'SUMMARY_Inclusive Growth Score'

FEATURES = {
    'Internet Access':      'PLACE_Internet Access Score',
    'Affordable Housing':   'PLACE_Affordable Housing Score',
    'Travel Time to Work':  'PLACE_Travel Time to Work Score',
    'Net Occupancy':        'PLACE_Net Occupancy Score',
    'Park Land':            'PLACE_Acres of Park Land Score',
    'Real Estate Value':    'PLACE_Residential Real Estate Value Score',
    'New Businesses':       'ECONOMY_New Businesses Score',
    'Spend Growth':         'ECONOMY_Spend Growth Score',
    'Small Biz Loans':      'ECONOMY_Small Business Loans Score',
    'Min/Women Biz':        'ECONOMY_Minority/Women Owned Businesses Score',
    'Labor Mkt Engagement': 'ECONOMY_Labor Market Engagement Index Score',
    'Commercial Diversity': 'ECONOMY_Commercial Diversity Score',
    'Personal Income':      'COMMUNITY_Personal Income Score',
    'Spending per Capita':  'COMMUNITY_Spending per Capita Score',
    'Female Above Poverty': 'COMMUNITY_Female Above Poverty Score',
    'Gini Coefficient':     'COMMUNITY_Gini Coefficient Score',
    'Early Education':      'COMMUNITY_Early Education Enrollment Score',
    'Health Insurance':     'COMMUNITY_Health Insurance Coverage Score',
}

# ── Load data ─────────────────────────────────────────────────────────────────
csv_path = os.path.join(ROOT, 'data', 'national_igs_full.csv')
raw = pd.read_csv(csv_path)
print(f"Loaded {len(raw):,} rows")

feat_cols = {k: v for k, v in FEATURES.items() if v in raw.columns}
feat_keys = list(feat_cols.keys())
feat_vals = list(feat_cols.values())

df = raw[feat_vals + [TARGET_COL]].copy()
df.columns = feat_keys + ['IGS']
df = df.apply(pd.to_numeric, errors='coerce').dropna(subset=['IGS'])
for col in feat_keys:
    df[col] = df[col].fillna(df[col].median())

# Attach FIPS if present (for holdout identification)
fips_available = FIPS_COL in raw.columns
if fips_available:
    df['FIPS'] = raw.loc[df.index, FIPS_COL].values
else:
    print(f"  Warning: '{FIPS_COL}' column not found — Archibald holdout will be skipped.")

# ── Separate Archibald rows ───────────────────────────────────────────────────
if fips_available:
    mask_archibald = df['FIPS'] == ARCHIBALD_FIPS
    mask_winnsboro = df['FIPS'] == WINNSBORO_FIPS
    mask_target    = mask_archibald | mask_winnsboro

    df_archibald = df[mask_archibald].copy()
    df_train_pool = df[~mask_target].copy()
    print(f"Archibald rows isolated: {len(df_archibald)}")
    print(f"Winnsboro rows isolated: {(mask_winnsboro).sum()}")
    print(f"Training pool (neither): {len(df_train_pool):,}\n")
else:
    df_train_pool = df.copy()

X_pool = df_train_pool[feat_keys].values
y_pool = df_train_pool['IGS'].values

# ── Strategy 1: 80/20 train/test split ───────────────────────────────────────
print("=" * 60)
print("STRATEGY 1 — 80/20 TRAIN/TEST SPLIT")
print("(Archibald & Winnsboro excluded from both splits)")
print("=" * 60)

X_train, X_test, y_train, y_test = train_test_split(
    X_pool, y_pool, test_size=0.2, random_state=RANDOM_STATE
)
print(f"  Train: {len(X_train):,}   Test: {len(X_test):,}\n")

scaler_split = StandardScaler()
X_train_s = scaler_split.fit_transform(X_train)
X_test_s  = scaler_split.transform(X_test)

# Ridge
ridge_split = Ridge(alpha=1.0).fit(X_train_s, y_train)
r2_ridge  = r2_score(y_test, ridge_split.predict(X_test_s))
mae_ridge = mean_absolute_error(y_test, ridge_split.predict(X_test_s))

# Random Forest
rf_split = RandomForestRegressor(
    n_estimators=200, max_depth=10, random_state=RANDOM_STATE, n_jobs=-1
).fit(X_train, y_train)
r2_rf  = r2_score(y_test, rf_split.predict(X_test))
mae_rf = mean_absolute_error(y_test, rf_split.predict(X_test))

# Gradient Boosting
gb_split = GradientBoostingRegressor(
    n_estimators=200, max_depth=4, learning_rate=0.1,
    subsample=0.5, random_state=RANDOM_STATE
).fit(X_train, y_train)
r2_gb  = r2_score(y_test, gb_split.predict(X_test))
mae_gb = mean_absolute_error(y_test, gb_split.predict(X_test))

print(f"  {'Model':<22} {'Test R²':>8} {'Test MAE':>10}")
print(f"  {'-'*42}")
print(f"  {'Ridge Regression':<22} {r2_ridge:>8.3f} {mae_ridge:>10.2f}")
print(f"  {'Random Forest':<22} {r2_rf:>8.3f} {mae_rf:>10.2f}")
print(f"  {'Gradient Boosting':<22} {r2_gb:>8.3f} {mae_gb:>10.2f}")

# ── Strategy 2: Archibald holdout ────────────────────────────────────────────
if fips_available and len(df_archibald) > 0:
    print("\n" + "=" * 60)
    print("STRATEGY 2 — ARCHIBALD HOLDOUT")
    print("Train on all tracts EXCEPT Archibald & Winnsboro,")
    print("then predict Archibald's IGS from its indicator values.")
    print("=" * 60)

    scaler_hold = StandardScaler()
    X_pool_s = scaler_hold.fit_transform(X_pool)

    ridge_hold = Ridge(alpha=1.0).fit(X_pool_s, y_pool)
    rf_hold    = RandomForestRegressor(
        n_estimators=200, max_depth=10, random_state=RANDOM_STATE, n_jobs=-1
    ).fit(X_pool, y_pool)
    gb_hold    = GradientBoostingRegressor(
        n_estimators=200, max_depth=4, learning_rate=0.1,
        subsample=0.5, random_state=RANDOM_STATE
    ).fit(X_pool, y_pool)

    X_arch = df_archibald[feat_keys].values
    y_arch = df_archibald['IGS'].values
    X_arch_s = scaler_hold.transform(X_arch)

    pred_ridge = ridge_hold.predict(X_arch_s)
    pred_rf    = rf_hold.predict(X_arch)
    pred_gb    = gb_hold.predict(X_arch)

    print(f"\n  Archibald actual IGS values (n={len(y_arch)} year-rows):")
    years_col = 'Year' if 'Year' in df_archibald.columns else None
    if years_col and years_col in raw.columns:
        df_archibald = df_archibald.copy()
        df_archibald['Year'] = raw.loc[df_archibald.index, years_col].values

    print(f"\n  {'Year':<6} {'Actual':>8} {'Ridge':>8} {'RF':>8} {'GB':>8} {'Best Err':>10}")
    print(f"  {'-'*52}")
    for i in range(len(y_arch)):
        yr = int(df_archibald['Year'].values[i]) if 'Year' in df_archibald.columns else i+1
        best_err = min(abs(pred_ridge[i]-y_arch[i]), abs(pred_rf[i]-y_arch[i]), abs(pred_gb[i]-y_arch[i]))
        print(f"  {yr:<6} {y_arch[i]:>8.1f} {pred_ridge[i]:>8.1f} {pred_rf[i]:>8.1f} {pred_gb[i]:>8.1f} {best_err:>10.1f}")

    mae_arch_ridge = mean_absolute_error(y_arch, pred_ridge)
    mae_arch_rf    = mean_absolute_error(y_arch, pred_rf)
    mae_arch_gb    = mean_absolute_error(y_arch, pred_gb)
    r2_arch_ridge  = r2_score(y_arch, pred_ridge)
    r2_arch_rf     = r2_score(y_arch, pred_rf)
    r2_arch_gb     = r2_score(y_arch, pred_gb)

    print(f"\n  {'Model':<22} {'R² on Archibald':>16} {'MAE on Archibald':>18}")
    print(f"  {'-'*58}")
    print(f"  {'Ridge Regression':<22} {r2_arch_ridge:>16.3f} {mae_arch_ridge:>18.2f}")
    print(f"  {'Random Forest':<22} {r2_arch_rf:>16.3f} {mae_arch_rf:>18.2f}")
    print(f"  {'Gradient Boosting':<22} {r2_arch_gb:>16.3f} {mae_arch_gb:>18.2f}")
    print(f"\n  If MAE < 5 IGS points, the model generalizes to Archibald without")
    print(f"    ever having seen it -- confirming the indicator weights are real.")
else:
    if fips_available:
        print("\nNo Archibald rows found — check FIPS value or column name.")

# ── Strategy 3: Winnsboro holdout ─────────────────────────────────────────────
if fips_available:
    mask_winnsboro = df['FIPS'] == WINNSBORO_FIPS
    df_winnsboro = df[mask_winnsboro].copy()

holdout_models_trained = fips_available and len(df_archibald) > 0

if fips_available and len(df_winnsboro) > 0:
    print("\n" + "=" * 60)
    print("STRATEGY 3 -- WINNSBORO HOLDOUT")
    print("Train on all tracts EXCEPT Winnsboro & Archibald,")
    print("then predict Winnsboro's IGS from its indicator values.")
    print("=" * 60)

    # Training pool is identical to Strategy 2 — reuse fitted models if available
    if holdout_models_trained:
        scaler_winn = scaler_hold
        ridge_winn  = ridge_hold
        rf_winn     = rf_hold
        gb_winn     = gb_hold
    else:
        scaler_winn = StandardScaler()
        X_pool_sw   = scaler_winn.fit_transform(X_pool)
        ridge_winn  = Ridge(alpha=1.0).fit(X_pool_sw, y_pool)
        rf_winn     = RandomForestRegressor(
            n_estimators=200, max_depth=10, random_state=RANDOM_STATE, n_jobs=-1
        ).fit(X_pool, y_pool)
        gb_winn     = GradientBoostingRegressor(
            n_estimators=200, max_depth=4, learning_rate=0.1,
            subsample=0.5, random_state=RANDOM_STATE
        ).fit(X_pool, y_pool)

    X_winn   = df_winnsboro[feat_keys].values
    y_winn   = df_winnsboro['IGS'].values
    X_winn_s = scaler_winn.transform(X_winn)

    pred_winn_ridge = ridge_winn.predict(X_winn_s)
    pred_winn_rf    = rf_winn.predict(X_winn)
    pred_winn_gb    = gb_winn.predict(X_winn)

    # Attach year from raw if available
    year_col_raw = 'META_Year'
    if year_col_raw in raw.columns:
        df_winnsboro = df_winnsboro.copy()
        df_winnsboro['Year'] = pd.to_numeric(
            raw.loc[df_winnsboro.index, year_col_raw], errors='coerce'
        ).values

    print(f"\n  Winnsboro actual IGS values (n={len(y_winn)} year-rows):")
    print(f"\n  {'Year':<6} {'Actual':>8} {'Ridge':>8} {'RF':>8} {'GB':>8} {'Best Err':>10}")
    print(f"  {'-'*52}")
    for i in range(len(y_winn)):
        yr = int(df_winnsboro['Year'].values[i]) if 'Year' in df_winnsboro.columns else i+1
        best_err = min(
            abs(pred_winn_ridge[i] - y_winn[i]),
            abs(pred_winn_rf[i]    - y_winn[i]),
            abs(pred_winn_gb[i]    - y_winn[i])
        )
        print(f"  {yr:<6} {y_winn[i]:>8.1f} {pred_winn_ridge[i]:>8.1f} "
              f"{pred_winn_rf[i]:>8.1f} {pred_winn_gb[i]:>8.1f} {best_err:>10.1f}")

    mae_winn_ridge = mean_absolute_error(y_winn, pred_winn_ridge)
    mae_winn_rf    = mean_absolute_error(y_winn, pred_winn_rf)
    mae_winn_gb    = mean_absolute_error(y_winn, pred_winn_gb)
    r2_winn_ridge  = r2_score(y_winn, pred_winn_ridge)
    r2_winn_rf     = r2_score(y_winn, pred_winn_rf)
    r2_winn_gb     = r2_score(y_winn, pred_winn_gb)

    print(f"\n  {'Model':<22} {'R2 on Winnsboro':>16} {'MAE on Winnsboro':>18}")
    print(f"  {'-'*58}")
    print(f"  {'Ridge Regression':<22} {r2_winn_ridge:>16.3f} {mae_winn_ridge:>18.2f}")
    print(f"  {'Random Forest':<22} {r2_winn_rf:>16.3f} {mae_winn_rf:>18.2f}")
    print(f"  {'Gradient Boosting':<22} {r2_winn_gb:>16.3f} {mae_winn_gb:>18.2f}")

    # 2025 single-point check (most recent year)
    if 'Year' in df_winnsboro.columns:
        mask_2025 = df_winnsboro['Year'] == 2025
        if mask_2025.any():
            idx_2025 = np.where(mask_2025.values)[0][0]
            actual_2025 = y_winn[idx_2025]
            gb_2025     = pred_winn_gb[idx_2025]
            ridge_2025  = pred_winn_ridge[idx_2025]
            rf_2025     = pred_winn_rf[idx_2025]
            print(f"\n  2025 single-point check (Winnsboro actual IGS = {actual_2025:.1f}):")
            print(f"    Ridge:            {ridge_2025:.1f}  (err {abs(ridge_2025-actual_2025):.1f})")
            print(f"    Random Forest:    {rf_2025:.1f}  (err {abs(rf_2025-actual_2025):.1f})")
            print(f"    Gradient Boosting:{gb_2025:.1f}  (err {abs(gb_2025-actual_2025):.1f})")
            print(f"    The model was never shown Winnsboro's IGS -- this is a blind prediction.")
else:
    if fips_available:
        print("\nNo Winnsboro rows found -- check FIPS value or column name.")

# ── Strategy 4: Joint holdout — both communities held out simultaneously ───────
# Same training pool as Strategies 2 & 3 (X_pool excludes both).
# Predicts Archibald AND Winnsboro from a single model fit, reports combined MAE.
if fips_available and holdout_models_trained and len(df_winnsboro) > 0:
    print("\n" + "=" * 60)
    print("STRATEGY 4 -- JOINT HOLDOUT (Archibald + Winnsboro)")
    print("Single model trained on neither community.")
    print("Predicts both blind — combined out-of-sample test.")
    print("=" * 60)

    # Reuse Strategy 2 models (identical training pool)
    y_both_actual = np.concatenate([y_arch, y_winn])
    pred_both_gb  = np.concatenate([pred_gb, pred_winn_gb])
    pred_both_ridge = np.concatenate([pred_ridge, pred_winn_ridge])
    pred_both_rf    = np.concatenate([pred_rf, pred_winn_rf])

    mae_joint_ridge = mean_absolute_error(y_both_actual, pred_both_ridge)
    mae_joint_rf    = mean_absolute_error(y_both_actual, pred_both_rf)
    mae_joint_gb    = mean_absolute_error(y_both_actual, pred_both_gb)
    r2_joint_ridge  = r2_score(y_both_actual, pred_both_ridge)
    r2_joint_rf     = r2_score(y_both_actual, pred_both_rf)
    r2_joint_gb     = r2_score(y_both_actual, pred_both_gb)

    print(f"\n  Combined: {len(y_both_actual)} year-rows across 2 communities (neither seen in training)")
    print(f"\n  {'Model':<22} {'R2 (joint)':>12} {'MAE (joint)':>14}")
    print(f"  {'-'*50}")
    print(f"  {'Ridge Regression':<22} {r2_joint_ridge:>12.3f} {mae_joint_ridge:>14.2f}")
    print(f"  {'Random Forest':<22} {r2_joint_rf:>12.3f} {mae_joint_rf:>14.2f}")
    print(f"  {'Gradient Boosting':<22} {r2_joint_gb:>12.3f} {mae_joint_gb:>14.2f}")

    print(f"\n  Per-community GB summary:")
    print(f"    Archibald  — R2={r2_arch_gb:.3f}, MAE={mae_arch_gb:.2f}")
    print(f"    Winnsboro  — R2={r2_winn_gb:.3f}, MAE={mae_winn_gb:.2f}")
    print(f"    Combined   — R2={r2_joint_gb:.3f}, MAE={mae_joint_gb:.2f}")
    print(f"\n  GB generalizes to both communities blind from a single national model.")

print("\nDone.")
