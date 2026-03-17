"""
Chart 19a — Strip/Dot Plot
Winnsboro & Archibald in National & Louisiana IGS Distribution (2025)
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── Colors ──────────────────────────────────────────────────────────────────
WIN_COLOR = '#C0392B'
ARC_COLOR = '#2980B9'
DARK      = '#1A1A2E'
GRAY      = '#95A5A6'
AMBER     = '#E67E22'
GREEN     = '#27AE60'
LA_COLOR  = '#8E44AD'

# ── Load data ────────────────────────────────────────────────────────────────
df = pd.read_csv(r'C:/Users/chiny/Code/ms-resrach/data/national_igs_full.csv')

# Filter to 2025
df = df[df['META_Year'] == 2025].copy()

# Filter: missing_count <= 2  (NaN count across PLACE_, ECONOMY_, COMMUNITY_ cols)
sub_cols = [c for c in df.columns if c.startswith('PLACE_') or
            c.startswith('ECONOMY_') or c.startswith('COMMUNITY_')]
df['missing_count'] = df[sub_cols].isna().sum(axis=1)
df = df[df['missing_count'] <= 2].copy()

igs_col  = 'SUMMARY_Inclusive Growth Score'
state_col = 'META_State'

national = df[igs_col].dropna().values
la_mask  = df[state_col].str.strip().str.upper() == 'LA'
louisiana = df.loc[la_mask, igs_col].dropna().values

nat_median = np.median(national)
la_median  = np.median(louisiana)

WIN_IGS = 38
ARC_IGS = 59

# ── Figure ───────────────────────────────────────────────────────────────────
np.random.seed(42)
fig, ax = plt.subplots(figsize=(12, 4), facecolor='white')
ax.set_facecolor('white')

# National dots (plot first so they're underneath)
nat_jitter = np.random.uniform(-0.3, 0.3, size=len(national))
ax.scatter(national, nat_jitter, color=GRAY, alpha=0.05, s=4, zorder=1,
           label='_nolegend_')

# Louisiana dots
la_jitter = np.random.uniform(-0.3, 0.3, size=len(louisiana))
ax.scatter(louisiana, la_jitter, color=LA_COLOR, alpha=0.15, s=8, zorder=2,
           label='Louisiana tracts')

# Winnsboro — red diamond
ax.scatter([WIN_IGS], [0], color=WIN_COLOR, marker='D', s=180, zorder=10,
           edgecolors='white', linewidths=0.8, label='Winnsboro (IGS 38)')

# Archibald — blue circle
ax.scatter([ARC_IGS], [0], color=ARC_COLOR, marker='o', s=180, zorder=10,
           edgecolors='white', linewidths=0.8, label='Archibald (IGS 59)')

# Vertical dashed reference lines
ax.axvline(nat_median, color=GRAY, linestyle='--', linewidth=1.4, zorder=5,
           label=f'National median ({nat_median:.0f})')
ax.axvline(la_median,  color=LA_COLOR, linestyle='--', linewidth=1.4, zorder=5,
           label=f'Louisiana median ({la_median:.0f})')

# Annotations above markers
ax.annotate(f'Winnsboro\nIGS {WIN_IGS}',
            xy=(WIN_IGS, 0), xytext=(WIN_IGS - 1.5, 0.55),
            fontsize=9, color=WIN_COLOR, fontweight='bold', ha='center',
            arrowprops=dict(arrowstyle='->', color=WIN_COLOR, lw=1.2))

ax.annotate(f'Archibald\nIGS {ARC_IGS}',
            xy=(ARC_IGS, 0), xytext=(ARC_IGS + 1.5, 0.55),
            fontsize=9, color=ARC_COLOR, fontweight='bold', ha='center',
            arrowprops=dict(arrowstyle='->', color=ARC_COLOR, lw=1.2))

# Median labels
ax.text(nat_median + 0.8, -0.55, f'Natl median\n{nat_median:.0f}',
        fontsize=8, color=GRAY, ha='left', va='top')
ax.text(la_median + 0.8, 0.55, f'LA median\n{la_median:.0f}',
        fontsize=8, color=LA_COLOR, ha='left', va='bottom')

# Custom legend
handles = [
    mpatches.Patch(color=GRAY, alpha=0.4, label='National tracts'),
    mpatches.Patch(color=LA_COLOR, alpha=0.5, label='Louisiana tracts'),
    plt.Line2D([0],[0], marker='D', color='w', markerfacecolor=WIN_COLOR,
               markersize=9, label='Winnsboro (IGS 38)'),
    plt.Line2D([0],[0], marker='o', color='w', markerfacecolor=ARC_COLOR,
               markersize=9, label='Archibald (IGS 59)'),
    plt.Line2D([0],[0], linestyle='--', color=GRAY, linewidth=1.4,
               label=f'National median ({nat_median:.0f})'),
    plt.Line2D([0],[0], linestyle='--', color=LA_COLOR, linewidth=1.4,
               label=f'LA median ({la_median:.0f})'),
]
ax.legend(handles=handles, loc='upper left', fontsize=8, framealpha=0.9,
          ncol=2, columnspacing=1)

# Axes styling
ax.set_xlim(0, 100)
ax.set_ylim(-0.85, 0.95)
ax.set_xlabel('IGS Score', fontsize=11, color=DARK)
ax.set_yticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.tick_params(axis='x', labelsize=10, colors=DARK)

ax.set_title(
    'Winnsboro & Archibald in National & Louisiana IGS Distribution (2025)',
    fontsize=13, fontweight='bold', color=DARK, pad=10)

plt.tight_layout()
out = r'C:/Users/chiny/Code/Mastercard/charts/19a_bench_strip.png'
plt.savefig(out, dpi=160, bbox_inches='tight', facecolor='white')
print(f'Saved: {out}')
