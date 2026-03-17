"""
Chart 19d — IGS Trajectory Line Chart
IGS Trajectory: Winnsboro vs Archibald (2017–2025)
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ── Colors ──────────────────────────────────────────────────────────────────
WIN_COLOR = '#C0392B'
ARC_COLOR = '#2980B9'
DARK      = '#1A1A2E'
GRAY      = '#95A5A6'
AMBER     = '#E67E22'
GREEN     = '#27AE60'
LA_COLOR  = '#8E44AD'

# ── Load data ────────────────────────────────────────────────────────────────
df = pd.read_csv(r'C:/Users/chiny/Code/Mastercard/data/all_tracts_igs_scores.csv')

win = df[df['FIPS'] == 22041950100].sort_values('Year').copy()
arc = df[df['FIPS'] == 22083970600].sort_values('Year').copy()

win_years = win['Year'].values
win_igs   = win['IGS'].values
arc_years = arc['Year'].values
arc_igs   = arc['IGS'].values

# Align to common year range
years = np.intersect1d(win_years, arc_years)
win_vals = win.set_index('Year').loc[years, 'IGS'].values
arc_vals = arc.set_index('Year').loc[years, 'IGS'].values

# 2025 endpoint values
win_2025 = win_vals[-1]   # should be 38
arc_2025 = arc_vals[-1]   # should be 59
gap = arc_2025 - win_2025

# ── Figure ───────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(11, 5), facecolor='white')
ax.set_facecolor('white')

# Fill between
ax.fill_between(years, win_vals, arc_vals, alpha=0.12, color=GRAY, zorder=1)

# Challenge threshold line
ax.axhline(45, color=AMBER, linestyle='--', linewidth=1.5, zorder=2)
ax.text(years[-1] + 0.15, 45.5, 'Challenge\nthreshold (45)',
        fontsize=8.5, color=AMBER, va='bottom', ha='left')

# Winnsboro line — red dashed with square markers
ax.plot(years, win_vals, color=WIN_COLOR, linestyle='--', linewidth=2.2,
        marker='s', markersize=7, zorder=5, label='Winnsboro (Franklin Parish)')

# Archibald line — blue solid with circle markers
ax.plot(years, arc_vals, color=ARC_COLOR, linestyle='-', linewidth=2.2,
        marker='o', markersize=7, zorder=5, label='Archibald (Richland Parish)')

# 2025 endpoint annotations
ax.annotate(f'IGS {win_2025:.0f}',
            xy=(years[-1], win_2025),
            xytext=(years[-1] - 0.8, win_2025 - 5),
            fontsize=10, color=WIN_COLOR, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=WIN_COLOR, lw=1.2))

ax.annotate(f'IGS {arc_2025:.0f}',
            xy=(years[-1], arc_2025),
            xytext=(years[-1] - 0.8, arc_2025 + 4),
            fontsize=10, color=ARC_COLOR, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=ARC_COLOR, lw=1.2))

# Gap arrow annotation between 2025 endpoints
mid_y = (win_2025 + arc_2025) / 2
ax.annotate(
    '', xy=(years[-1], arc_2025), xytext=(years[-1], win_2025),
    arrowprops=dict(arrowstyle='<->', color=DARK, lw=1.5)
)
ax.text(years[-1] + 0.3, mid_y, f'Gap:\n{gap:.0f} pts',
        fontsize=9, color=DARK, fontweight='bold', va='center', ha='left')

# ── Styling ───────────────────────────────────────────────────────────────────
ax.set_xlim(years[0] - 0.3, years[-1] + 1.4)
ax.set_ylim(0, 80)
ax.set_xticks(years)
ax.set_xlabel('Year', fontsize=11, color=DARK)
ax.set_ylabel('IGS Score', fontsize=11, color=DARK)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(axis='both', labelsize=10, colors=DARK)
ax.yaxis.set_minor_locator(ticker.MultipleLocator(5))
ax.grid(axis='y', linestyle=':', linewidth=0.6, color='#DDDDDD', zorder=0)

ax.legend(loc='upper left', fontsize=10, framealpha=0.9)

# Title + subtitle
ax.set_title(
    'IGS Trajectory: Winnsboro vs Archibald (2017–2025)',
    fontsize=13, fontweight='bold', color=DARK, pad=4)
fig.text(0.5, 0.93,
         'Same rural NE Louisiana region — divergent paths',
         ha='center', fontsize=10, color=GRAY, style='italic')

plt.tight_layout(rect=[0, 0, 1, 0.93])
out = r'C:/Users/chiny/Code/Mastercard/charts/19d_bench_trajectory.png'
plt.savefig(out, dpi=160, bbox_inches='tight', facecolor='white')
print(f'Saved: {out}')
