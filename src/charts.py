"""
charts.py — All regression analysis charts.

Chart 08: 4-panel — Ridge coefficients, RF importance, Actual vs Predicted, What-if simulation
Chart 09: Model comparison — CV R² and MAE for all 3 models
Chart 10: Indicator sensitivity for Franklin Parish
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sklearn.metrics import r2_score

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MC_RED = '#C0392B'
BLUE   = '#2980B9'
GREEN  = '#27AE60'
AMBER  = '#E67E22'
DARK   = '#1A1A2E'
GRAY   = '#7F8C8D'

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'figure.dpi': 150,
})


def chart_08_regression_analysis(coef_df, rf_imp, X, y, ridge, rf, gb, scaler,
                                  franklin_vec, sim_results, feature_names):
    """4-panel regression analysis chart."""
    pred_current_rf    = sim_results['current']['RF']
    pred_current_ridge = sim_results['current']['Ridge']
    pred_current_gb    = sim_results['current']['GB']

    # Phase 1 scenario predictions for the what-if panel
    p1_key = 'Phase 1 — Year 1  (HealthScore direct levers)'
    pred_p1_ridge = sim_results[p1_key]['Ridge']
    pred_p1_rf    = sim_results[p1_key]['RF']
    pred_p1_gb    = sim_results[p1_key]['GB']

    fig = plt.figure(figsize=(16, 14))
    fig.suptitle('IGS Regression Analysis — Franklin Parish, LA',
                 fontsize=16, fontweight='bold', y=0.98)

    # Panel 1: Ridge coefficients
    ax1 = fig.add_subplot(2, 2, 1)
    coef_sorted = coef_df.sort_values('Coefficient')
    colors = [MC_RED if v < 0 else GREEN for v in coef_sorted['Coefficient']]
    ax1.barh(coef_sorted['Feature'], coef_sorted['Coefficient'], color=colors, alpha=0.85)
    ax1.axvline(0, color='black', linewidth=0.8)
    ax1.set_title('Ridge Regression: Standardised Coefficients\n(impact per 1 SD change in indicator)',
                  fontweight='bold', fontsize=11)
    ax1.set_xlabel('Coefficient (standardised)')
    ax1.legend(handles=[
        mpatches.Patch(color=GREEN, label='Positive → raises IGS'),
        mpatches.Patch(color=MC_RED, label='Negative → lowers IGS'),
    ], fontsize=8)

    # Panel 2: RF feature importance
    ax2 = fig.add_subplot(2, 2, 2)
    rf_plot = rf_imp.head(12)
    bar_cols = [MC_RED if i < 3 else BLUE if i < 7 else GRAY for i in range(len(rf_plot))]
    ax2.barh(rf_plot['Feature'][::-1], rf_plot['Importance'][::-1],
             color=bar_cols[::-1], alpha=0.85)
    ax2.set_title('Random Forest: Feature Importance\n(top 12 predictors of IGS)',
                  fontweight='bold', fontsize=11)
    ax2.set_xlabel('Importance Score')

    # Panel 3: Actual vs Predicted (RF)
    ax3 = fig.add_subplot(2, 2, 3)
    y_pred_rf = rf.predict(X)
    ax3.scatter(y, y_pred_rf, alpha=0.65, color=BLUE, s=60, edgecolors='white', linewidth=0.5)
    lim = [y.min() - 3, y.max() + 3]
    ax3.plot(lim, lim, '--', color=GRAY, linewidth=1.5, label='Perfect prediction')
    ax3.axhline(45, color=AMBER, linestyle=':', linewidth=1.3, label='IGS threshold (45)')
    ax3.axvline(45, color=AMBER, linestyle=':', linewidth=1.3)
    ax3.scatter([38], [pred_current_rf], color=MC_RED, s=150, zorder=5,
                label=f'Franklin 2025 (pred={pred_current_rf:.1f})')
    ax3.scatter([38], [pred_p1_rf], color=GREEN, s=150, marker='*', zorder=5,
                label=f'HealthScore Phase 1 (pred={pred_p1_rf:.1f})')
    ax3.set_xlabel('Actual IGS Score')
    ax3.set_ylabel('Predicted IGS Score')
    ax3.set_title(f'Actual vs Predicted IGS — Random Forest\n(R² = {r2_score(y, y_pred_rf):.3f})',
                  fontweight='bold', fontsize=11)
    ax3.legend(fontsize=8)

    # Panel 4: What-if simulation
    ax4 = fig.add_subplot(2, 2, 4)
    labels    = ['Current\nFranklin (2025)', 'HealthScore\nPhase 1 Target']
    ridge_vals = [pred_current_ridge, pred_p1_ridge]
    rf_vals    = [pred_current_rf,    pred_p1_rf]
    gb_vals    = [pred_current_gb,    pred_p1_gb]
    avg_vals   = [
        np.mean([pred_current_ridge, pred_current_rf, pred_current_gb]),
        np.mean([pred_p1_ridge, pred_p1_rf, pred_p1_gb]),
    ]
    x_ = np.arange(2)
    w_ = 0.2
    ax4.bar(x_ - w_ * 1.5, ridge_vals, w_, label='Ridge',            color=BLUE,  alpha=0.8)
    ax4.bar(x_ - w_ * 0.5, rf_vals,    w_, label='Random Forest',    color=GREEN, alpha=0.8)
    ax4.bar(x_ + w_ * 0.5, gb_vals,    w_, label='Gradient Boosting', color=AMBER, alpha=0.8)
    ax4.bar(x_ + w_ * 1.5, avg_vals,   w_, label='Ensemble Average', color=DARK,  alpha=0.9)
    ax4.axhline(45, color=MC_RED, linestyle='--', linewidth=2, label='IGS Threshold (45)')
    ax4.set_xticks(x_)
    ax4.set_xticklabels(labels)
    ax4.set_ylabel('Predicted IGS Score')
    ax4.set_ylim(0, 75)
    ax4.set_title('HealthScore What-If Simulation\n(All Models — Predicted IGS After Intervention)',
                  fontweight='bold', fontsize=11)
    ax4.legend(fontsize=8)
    for i, av in enumerate(avg_vals):
        ax4.annotate(f'Avg: {av:.1f}', xy=(i + w_ * 1.5, av + 0.8),
                     fontsize=9, fontweight='bold', color=DARK, ha='center')

    plt.tight_layout()
    out = os.path.join(ROOT, 'charts', '08_regression_analysis.png')
    plt.savefig(out, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out}")


def chart_09_model_comparison(ridge_cv, ridge_mae, rf_cv, rf_mae, gb_cv, gb_mae):
    """Side-by-side CV R² and MAE for all 3 models."""
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle('Model Performance Summary — IGS Prediction',
                 fontweight='bold', fontsize=14)

    models  = ['Ridge\nRegression', 'Random\nForest', 'Gradient\nBoosting']
    r2s     = [ridge_cv.mean(), rf_cv.mean(), gb_cv.mean()]
    r2_std  = [ridge_cv.std(),  rf_cv.std(),  gb_cv.std()]
    maes    = [-ridge_mae.mean(), -rf_mae.mean(), -gb_mae.mean()]
    mae_std = [ridge_mae.std(),   rf_mae.std(),   gb_mae.std()]
    colors  = [BLUE, GREEN, AMBER]

    axes[0].bar(models, r2s, color=colors, alpha=0.85, yerr=r2_std, capsize=5)
    axes[0].set_ylabel('R² Score (higher = better)')
    axes[0].set_title('Cross-Validated R² (5-fold)', fontweight='bold')
    axes[0].set_ylim(0, 1.1)
    for i, (v, s) in enumerate(zip(r2s, r2_std)):
        axes[0].text(i, v + s + 0.02, f'{v:.3f}', ha='center', fontweight='bold')

    axes[1].bar(models, maes, color=colors, alpha=0.85, yerr=mae_std, capsize=5)
    axes[1].set_ylabel('Mean Absolute Error (lower = better)')
    axes[1].set_title('Cross-Validated MAE (5-fold)', fontweight='bold')
    for i, (v, s) in enumerate(zip(maes, mae_std)):
        axes[1].text(i, v + s + 0.2, f'{v:.2f}', ha='center', fontweight='bold')

    plt.tight_layout()
    out = os.path.join(ROOT, 'charts', '09_model_comparison.png')
    plt.savefig(out, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out}")


def chart_10_sensitivity(sensitivity):
    """Indicator sensitivity: IGS gain from +20 pts on each indicator (RF)."""
    import pandas as pd
    sens_df = pd.DataFrame.from_dict(sensitivity, orient='index', columns=['IGS_Gain'])
    sens_df = sens_df.sort_values('IGS_Gain', ascending=False)

    bar_c = [MC_RED if v < 2 else (AMBER if v < 4 else GREEN) for v in sens_df['IGS_Gain']]

    fig, ax = plt.subplots(figsize=(10, 7))
    ax.barh(sens_df.index[::-1], sens_df['IGS_Gain'][::-1], color=bar_c[::-1], alpha=0.85)
    ax.axvline(0, color='black', linewidth=0.8)
    ax.set_xlabel('Predicted IGS Gain from +20 Points on Each Indicator')
    ax.set_title('Franklin Parish — Indicator Sensitivity Analysis\n'
                 '(Which improvements would move the needle most?)',
                 fontweight='bold', fontsize=13)
    ax.legend(handles=[
        mpatches.Patch(color=GREEN, label='>4 pts — HIGH impact'),
        mpatches.Patch(color=AMBER, label='2–4 pts — MEDIUM'),
        mpatches.Patch(color=MC_RED, label='<2 pts — LOW'),
    ], fontsize=9)

    plt.tight_layout()
    out = os.path.join(ROOT, 'charts', '10_sensitivity_analysis.png')
    plt.savefig(out, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out}")
