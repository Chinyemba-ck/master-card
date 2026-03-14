"""
regression_model.py — Orchestrator.

Run this file to:
  1. Load & clean data          (data_loader.py)
  2. Train all 3 models         (models.py)
  3. Run HealthScore scenarios  (simulate.py)
  4. Save all charts            (charts.py)
"""

import os
import sys
import warnings
warnings.filterwarnings('ignore')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(ROOT, 'src')
os.chdir(ROOT)
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from data_loader import get_data
from models      import train_all
from simulate    import run_simulations, sensitivity_analysis
from charts      import chart_08_regression_analysis, chart_09_model_comparison, chart_10_sensitivity

# ── 1. Data ─────────────────────────────────────────────────────────────────
X, y, df_model, feature_names, X_scaled, scaler, baseline, franklin_vec, actual_igs = get_data()

# ── 2. Models ────────────────────────────────────────────────────────────────
(ridge, ridge_cv, ridge_mae, coef_df,
 rf,    rf_cv,    rf_mae,    rf_imp,
 gb,    gb_cv,    gb_mae,    gb_imp) = train_all(X, y, X_scaled, feature_names)

# ── 3. Simulations ───────────────────────────────────────────────────────────
sim_results = run_simulations(
    ridge, rf, gb, scaler,
    baseline, franklin_vec, feature_names, df_model, actual_igs
)
sensitivity = sensitivity_analysis(rf, franklin_vec, sim_results['current']['RF'], feature_names)

# ── 4. Charts ────────────────────────────────────────────────────────────────
print("\nGenerating charts...")
chart_08_regression_analysis(coef_df, rf_imp, X, y, ridge, rf, gb, scaler,
                              franklin_vec, sim_results, feature_names)
chart_09_model_comparison(ridge_cv, ridge_mae, rf_cv, rf_mae, gb_cv, gb_mae)
chart_10_sensitivity(sensitivity)

print("\nDone. All charts saved to ./charts/")
