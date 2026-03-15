"""
caresignal_divergence_chart.py — Three separate charts for CareSignal presentation.

Chart A: The 5 key indicators — how Archibald and Winnsboro diverged 2017–2025
Chart B: Winnsboro vs National median — gap over time showing where collapse happened
Chart C: Current vs Phase targets — what CareSignal moves, by phase

Outputs:
  charts/14a_divergence_archibald_vs_winnsboro.png
  charts/14b_divergence_vs_national.png
  charts/14c_phase_targets.png

Run: python src/caresignal_divergence_chart.py
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# ── Colors ──────────────────────────────────────────────────────────────────
WIN_COLOR = '#C0392B'    # red  — Winnsboro
ARC_COLOR = '#2980B9'    # blue — Archibald
NAT_COLOR = '#7F8C8D'    # gray — National median
THRESHOLD = '#E67E22'    # amber — 45 threshold
GREEN     = '#27AE60'
DARK      = '#1A1A2E'
P1_COLOR  = '#27AE60'    # Phase 1
P2_COLOR  = '#2980B9'    # Phase 2
P3_COLOR  = '#8E44AD'    # Phase 3

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'figure.dpi': 150,
})

# ── Load tract data ──────────────────────────────────────────────────────────
df = pd.read_csv('data/all_tracts_igs_scores.csv')
fr = df[df['FIPS'] == 22041950100].sort_values('Year').copy()   # Winnsboro/Franklin
ri = df[df['FIPS'] == 22083970600].sort_values('Year').copy()   # Archibald/Richland
years = sorted(fr['Year'].unique())

# Average indicator values for tracts with IGS > 45 ("thriving" benchmark)
# Computed from national_igs_full.csv (524,111 of 757,582 tracts)
# Order: (Personal_Income=0, Net_Occupancy=1, Labor_Engagement=2, Small_Biz_Loans=3, Early_Education=4)
THRIVING_AVG = {
    2017: (56, 57, 62, 55, 54),
    2018: (56, 57, 62, 56, 54),
    2019: (55, 57, 62, 56, 54),
    2020: (55, 58, 62, 55, 54),
    2021: (55, 51, 62, 55, 52),
    2022: (55, 50, 62, 54, 52),
    2023: (56, 50, 62, 52, 51),
    2024: (56, 50, 62, 54, 52),
    2025: (56, 50, 62, 54, 52),
}

# 5 key indicators in model-rank order
KEY_INDICATORS = [
    ('Personal\nIncome',      'Personal_Income',   '#1 IGS lever',  0),
    ('Net\nOccupancy',        'Net_Occupancy',     '#2 IGS lever',  1),
    ('Labor Market\nEngage.', 'Labor_Engagement',  '#3 IGS lever',  2),
    ('Small Biz\nLoans',      'Small_Biz_Loans',   '#4 IGS lever',  3),
    ('Early\nEducation',      'Early_Education',   '#5 IGS lever',  4),
]

# Phase targets (from simulate.py)
TARGETS = {
    'Personal_Income':  (40, 46, 53),
    'Net_Occupancy':    (40, 46, 54),
    'Labor_Engagement': (20, 32, 44),
    'Small_Biz_Loans':  (60, 64, 66),
    'Early_Education':  (36, 46, 55),
}

WIN_2025 = {
    'Personal_Income':  36,
    'Net_Occupancy':    38,
    'Labor_Engagement': 14,
    'Small_Biz_Loans':  44,
    'Early_Education':  19,
}

NAT_2025 = {
    'Personal_Income':  51,
    'Net_Occupancy':    44,
    'Labor_Engagement': 51,
    'Small_Biz_Loans':  52,
    'Early_Education':  49,
}

ARC_2025 = {
    'Personal_Income':  56,
    'Net_Occupancy':    85,
    'Labor_Engagement': 58,
    'Small_Biz_Loans':  50,
    'Early_Education':  69,
}

os.makedirs('charts', exist_ok=True)


# ══════════════════════════════════════════════════════════════════════════════
# CHART A — Archibald vs Winnsboro divergence 2017–2025
# ══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 5, figsize=(20, 6), sharey=False)
fig.suptitle(
    'Five Key Indicators: How Winnsboro and Archibald Diverged  (2017–2025)',
    fontsize=15, fontweight='bold', color=DARK, y=1.02
)

for ax, (label, col, rank_label, nat_col_idx) in zip(axes, KEY_INDICATORS):
    fr_vals     = fr[col].values
    ri_vals     = ri[col].values
    thriving_vals = np.array([THRIVING_AVG[y][nat_col_idx] for y in years])

    # Thriving band (IGS > 45 tracts)
    ax.fill_between(years, thriving_vals - 3, thriving_vals + 3,
                    color=NAT_COLOR, alpha=0.13)
    ax.plot(years, thriving_vals, '--', color=NAT_COLOR, linewidth=1.3, alpha=0.6,
            label='Avg. of tracts with IGS > 45')

    ax.plot(years, ri_vals, 'o-', color=ARC_COLOR, linewidth=2.5,
            markersize=7, label='Archibald / Richland')
    ax.plot(years, fr_vals, 's--', color=WIN_COLOR, linewidth=2.2,
            markersize=6, label='Winnsboro / Franklin')


    ax.set_title(label, fontweight='bold', fontsize=12, pad=6)
    ax.set_ylim(0, 100)
    ax.set_xticks(years)
    ax.set_xticklabels([str(y)[2:] for y in years], fontsize=8)
    ax.set_xlabel('Year', fontsize=10)
    ax.tick_params(axis='y', labelsize=9)

    # Rank badge
    ax.text(0.03, 0.97, rank_label, transform=ax.transAxes,
            fontsize=8, color='white', va='top', ha='left',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=ARC_COLOR, alpha=0.88))

    # Start/end value labels
    offset_fr_start = -18 if fr_vals[0] >= ri_vals[0] - 5 else 5
    ax.annotate(f'WIN {fr_vals[0]:.0f}',
                (years[0], fr_vals[0]), textcoords='offset points',
                xytext=(-4, offset_fr_start), fontsize=8.5,
                color=WIN_COLOR, fontweight='bold')
    ax.annotate(f'WIN {fr_vals[-1]:.0f}',
                (years[-1], fr_vals[-1]), textcoords='offset points',
                xytext=(4, 3), fontsize=8.5, color=WIN_COLOR, fontweight='bold')
    ax.annotate(f'ARC {ri_vals[0]:.0f}',
                (years[0], ri_vals[0]), textcoords='offset points',
                xytext=(-4, 6), fontsize=8.5, color=ARC_COLOR, fontweight='bold')
    ax.annotate(f'ARC {ri_vals[-1]:.0f}',
                (years[-1], ri_vals[-1]), textcoords='offset points',
                xytext=(4, 3), fontsize=8.5, color=ARC_COLOR, fontweight='bold')

legend_elements_a = [
    Line2D([0], [0], color=ARC_COLOR, marker='o', linewidth=2.5, markersize=7,
           label='Archibald / Richland Parish (benchmark)'),
    Line2D([0], [0], color=WIN_COLOR, marker='s', linewidth=2.2, markersize=6,
           linestyle='--', label='Winnsboro / Franklin Parish (target)'),
    Line2D([0], [0], color=NAT_COLOR, linewidth=1.5, linestyle='--',
           label='Avg. of thriving tracts (IGS > 45)'),

]
fig.legend(handles=legend_elements_a, loc='lower center', ncol=4,
           fontsize=10, bbox_to_anchor=(0.5, -0.07), framealpha=0.9,
           edgecolor='#BDC3C7')

plt.tight_layout()
plt.savefig('charts/14a_divergence_archibald_vs_winnsboro.png',
            bbox_inches='tight', dpi=150)
plt.close()
print('Saved: charts/14a_divergence_archibald_vs_winnsboro.png')


# ══════════════════════════════════════════════════════════════════════════════
# CHART B — Winnsboro vs National Median: gap over time
# ══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 5, figsize=(20, 6), sharey=False)
fig.suptitle(
    'Winnsboro vs National Median — How Far Each Indicator Fell Below the National Base',
    fontsize=15, fontweight='bold', color=DARK, y=1.01
)
fig.text(
    0.5, 0.97,
    'Bars show Winnsboro score minus the avg. of thriving tracts (IGS > 45) each year.  '
    'Red = below thriving base.  Blue line = Archibald gap (the peer that recovered).',
    ha='center', fontsize=10.5, color='#555555', style='italic'
)

for ax, (label, col, rank_label, nat_col_idx) in zip(axes, KEY_INDICATORS):
    fr_vals  = fr[col].values
    ri_vals  = ri[col].values
    nat_vals = np.array([THRIVING_AVG[y][nat_col_idx] for y in years])

    fr_gap = fr_vals - nat_vals
    ri_gap = ri_vals - nat_vals

    bar_colors = [WIN_COLOR if g < 0 else GREEN for g in fr_gap]
    ax.bar(years, fr_gap, color=bar_colors, alpha=0.78, width=0.55, zorder=2)
    ax.fill_between(years, 0, fr_gap,
                    where=[g < 0 for g in fr_gap],
                    color=WIN_COLOR, alpha=0.07, zorder=0)

    ax.plot(years, ri_gap, 'o-', color=ARC_COLOR, linewidth=2.2,
            markersize=6, zorder=3, label='Archibald gap')
    ax.fill_between(years, 0, ri_gap,
                    where=[g > 0 for g in ri_gap],
                    color=ARC_COLOR, alpha=0.07, zorder=0)

    ax.axhline(0, color='black', linewidth=1.1, zorder=1)

    ax.set_title(label, fontweight='bold', fontsize=12, pad=6)
    ax.set_xticks(years)
    ax.set_xticklabels([str(y)[2:] for y in years], fontsize=8)
    ax.set_xlabel('Year', fontsize=10)
    ax.tick_params(axis='y', labelsize=9)

    # 2025 end-point labels
    y_off_w = 3 if fr_gap[-1] >= 0 else -13
    y_off_a = 3 if ri_gap[-1] >= 0 else -13
    ax.annotate(f'WIN {fr_gap[-1]:+.0f}',
                (years[-1], fr_gap[-1]), textcoords='offset points',
                xytext=(3, y_off_w), fontsize=8.5, color=WIN_COLOR, fontweight='bold')
    ax.annotate(f'ARC {ri_gap[-1]:+.0f}',
                (years[-1], ri_gap[-1]), textcoords='offset points',
                xytext=(3, y_off_a), fontsize=8.5, color=ARC_COLOR, fontweight='bold')

    # Rank badge
    ax.text(0.03, 0.97, rank_label, transform=ax.transAxes,
            fontsize=8, color='white', va='top', ha='left',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=ARC_COLOR, alpha=0.88))

axes[0].set_ylabel('Score − National Median', fontsize=10)

legend_elements_b = [
    mpatches.Patch(color=WIN_COLOR, alpha=0.78,
                   label='Winnsboro below thriving avg. (IGS > 45)'),
    mpatches.Patch(color=GREEN, alpha=0.78,
                   label='Winnsboro above thriving avg.'),
    Line2D([0], [0], color=ARC_COLOR, marker='o', linewidth=2.2, markersize=6,
           label='Archibald gap vs thriving avg.'),
    Line2D([0], [0], color='black', linewidth=1.1,
           label='Thriving avg. baseline (zero line)'),
]
fig.legend(handles=legend_elements_b, loc='lower center', ncol=4,
           fontsize=10, bbox_to_anchor=(0.5, -0.07), framealpha=0.9,
           edgecolor='#BDC3C7')

plt.tight_layout()
plt.savefig('charts/14b_divergence_vs_national.png',
            bbox_inches='tight', dpi=150)
plt.close()
print('Saved: charts/14b_divergence_vs_national.png')


# ══════════════════════════════════════════════════════════════════════════════
# CHART C — CareSignal Phase Targets
# ══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 5, figsize=(20, 7), sharey=False)
fig.suptitle(
    'CareSignal Phase Targets — Winnsboro 2025 → Recovery',
    fontsize=15, fontweight='bold', color=DARK, y=1.01
)
fig.text(
    0.5, 0.97,
    'Targets drawn from Winnsboro\'s own 2017 history and Archibald validation.  '
    'Gray = national median.  Blue = Archibald 2025 (what a recovered peer looks like).',
    ha='center', fontsize=10.5, color='#555555', style='italic'
)

positions  = [0, 1, 2, 3, 4, 5]
bar_labels = ['Win\n2025', 'Natl\nmed.', 'Phase 1\n(Yr 1)', 'Phase 2\n(Yr 2–3)', 'Phase 3\n(Yr 4–5)', 'Arc\n2025']
colors     = [WIN_COLOR, NAT_COLOR, P1_COLOR, P2_COLOR, P3_COLOR, ARC_COLOR]
alphas     = [0.92, 0.55, 0.88, 0.88, 0.88, 0.65]

for ax, (label, col, rank_label, nat_col_idx) in zip(axes, KEY_INDICATORS):
    current  = WIN_2025[col]
    national = NAT_2025[col]
    arc      = ARC_2025[col]
    p1, p2, p3 = TARGETS[col]

    values = [current, national, p1, p2, p3, arc]

    bars = ax.bar(positions, values, color=colors, width=0.68, zorder=2)
    for bar, alpha in zip(bars, alphas):
        bar.set_alpha(alpha)

    # 45 threshold
    ax.axhline(45, color=THRESHOLD, linestyle=':', linewidth=1.6, alpha=0.9, zorder=3)
    ax.text(5.55, 46.5, '45', fontsize=8, color=THRESHOLD, va='bottom', fontweight='bold')

    # Value labels on bars
    for pos, val in zip(positions, values):
        ax.text(pos, val + 1.8, str(val), ha='center', fontsize=9,
                fontweight='bold', color=DARK)

    # Rank badge
    ax.text(0.03, 0.97, rank_label, transform=ax.transAxes,
            fontsize=8, color='white', va='top', ha='left',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=ARC_COLOR, alpha=0.88))

    ax.set_title(label, fontweight='bold', fontsize=12, pad=6)
    ax.set_ylim(0, 105)
    ax.set_xticks(positions)
    ax.set_xticklabels(bar_labels, fontsize=8.5)
    ax.tick_params(axis='y', labelsize=9)

axes[0].set_ylabel('Indicator Score (0–100)', fontsize=10)

legend_elements_c = [
    mpatches.Patch(color=WIN_COLOR, alpha=0.92, label='Winnsboro 2025 (baseline)'),
    mpatches.Patch(color=NAT_COLOR, alpha=0.55, label='National median'),
    mpatches.Patch(color=P1_COLOR,  alpha=0.88, label='Phase 1 — Year 1  (~10% adoption)'),
    mpatches.Patch(color=P2_COLOR,  alpha=0.88, label='Phase 2 — Yr 2–3  (~50% adoption)'),
    mpatches.Patch(color=P3_COLOR,  alpha=0.88, label='Phase 3 — Yr 4–5  (~90% adoption)'),
    mpatches.Patch(color=ARC_COLOR, alpha=0.65, label='Archibald 2025 (recovered peer)'),
    Line2D([0], [0], color=THRESHOLD, linewidth=1.6, linestyle=':',
           label='Challenge threshold (45)'),
]
fig.legend(handles=legend_elements_c, loc='lower center', ncol=4,
           fontsize=10, bbox_to_anchor=(0.5, -0.1), framealpha=0.9,
           edgecolor='#BDC3C7')

plt.tight_layout()
plt.savefig('charts/14c_phase_targets.png',
            bbox_inches='tight', dpi=150)
plt.close()
print('Saved: charts/14c_phase_targets.png')
