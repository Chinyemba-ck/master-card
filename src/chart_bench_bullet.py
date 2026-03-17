"""
Chart 19c — Bullet Chart
IGS Score vs National Distribution — Bullet Chart (2025)
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ── Colors ──────────────────────────────────────────────────────────────────
WIN_COLOR = '#C0392B'
ARC_COLOR = '#2980B9'
DARK      = '#1A1A2E'
GRAY      = '#95A5A6'
AMBER     = '#E67E22'
GREEN     = '#27AE60'
LA_COLOR  = '#8E44AD'

# ── Load & filter data ───────────────────────────────────────────────────────
df = pd.read_csv(r'C:/Users/chiny/Code/ms-resrach/data/national_igs_full.csv')
df = df[df['META_Year'] == 2025].copy()

sub_cols = [c for c in df.columns if c.startswith('PLACE_') or
            c.startswith('ECONOMY_') or c.startswith('COMMUNITY_')]
df['missing_count'] = df[sub_cols].isna().sum(axis=1)
df = df[df['missing_count'] <= 2].copy()

igs_col = 'SUMMARY_Inclusive Growth Score'
national = df[igs_col].dropna().values

p10  = np.percentile(national, 10)
p25  = np.percentile(national, 25)
p50  = np.percentile(national, 50)
p75  = np.percentile(national, 75)
p90  = np.percentile(national, 90)

tracts = [
    {
        'label':  'Winnsboro\n(Franklin Parish, LA)',
        'score':  38,
        'color':  WIN_COLOR,
        'y':      1,
    },
    {
        'label':  'Archibald\n(Richland Parish, LA)',
        'score':  59,
        'color':  ARC_COLOR,
        'y':      0,
    },
]

# ── Figure ───────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(11, 4), facecolor='white')
ax.set_facecolor('white')

bar_height_outer = 0.55   # 10th–90th range
bar_height_inner = 0.35   # IQR (25th–75th)
bar_height_score = 0.20   # actual score bar

for t in tracts:
    y    = t['y']
    sc   = t['score']
    col  = t['color']

    # Wide background: 10th–90th percentile range (lightest gray)
    ax.barh(y, p90 - p10, left=p10, height=bar_height_outer,
            color='#E8E8E8', edgecolor='none', align='center', zorder=1)

    # Medium bar: IQR 25th–75th (medium gray)
    ax.barh(y, p75 - p25, left=p25, height=bar_height_inner,
            color='#C0C0C0', edgecolor='none', align='center', zorder=2)

    # Actual score bar (colored, short)
    ax.barh(y, sc, left=0, height=bar_height_score,
            color=col, edgecolor='none', align='center', zorder=3,
            alpha=0.9)

    # Score label
    ax.text(sc + 1.2, y, f'{sc}', va='center', ha='left',
            fontsize=11, fontweight='bold', color=col, zorder=5)

    # Vertical tick at national median
    ax.plot([p50, p50],
            [y - bar_height_outer / 2, y + bar_height_outer / 2],
            color=DARK, linewidth=2.0, zorder=4)

# Median label (once, above top bar)
ax.text(p50, 1 + bar_height_outer / 2 + 0.04,
        f'Natl median\n{p50:.0f}',
        ha='center', va='bottom', fontsize=8, color=DARK, fontweight='bold')

# Range labels (above top bar)
ax.text((p10 + p90) / 2, 1 + bar_height_outer / 2 + 0.04,
        f'10th–90th pct  ({p10:.0f}–{p90:.0f})',
        ha='center', va='bottom', fontsize=7.5, color='#888888',
        style='italic')

# IQR label (below bottom bar)
ax.text((p25 + p75) / 2, 0 - bar_height_outer / 2 - 0.04,
        f'IQR 25th–75th  ({p25:.0f}–{p75:.0f})',
        ha='center', va='top', fontsize=7.5, color='#888888', style='italic')

# ── Legend ────────────────────────────────────────────────────────────────────
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#E8E8E8', edgecolor='none', label=f'10th–90th pct ({p10:.0f}–{p90:.0f})'),
    Patch(facecolor='#C0C0C0', edgecolor='none', label=f'IQR 25th–75th ({p25:.0f}–{p75:.0f})'),
    Patch(facecolor=WIN_COLOR, alpha=0.9, edgecolor='none', label='Winnsboro score (38)'),
    Patch(facecolor=ARC_COLOR, alpha=0.9, edgecolor='none', label='Archibald score (59)'),
    plt.Line2D([0],[0], color=DARK, linewidth=2, label=f'National median ({p50:.0f})'),
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=8,
          framealpha=0.9, ncol=3)

# ── Axes styling ─────────────────────────────────────────────────────────────
ax.set_xlim(0, 100)
ax.set_ylim(-0.65, 1.65)
ax.set_xlabel('IGS Score', fontsize=11, color=DARK)
ax.set_yticks([0, 1])
ax.set_yticklabels(
    ['Archibald\n(Richland Parish, LA)', 'Winnsboro\n(Franklin Parish, LA)'],
    fontsize=10, color=DARK)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(axis='x', labelsize=10, colors=DARK)
ax.tick_params(axis='y', length=0)

ax.set_title(
    'IGS Score vs National Distribution — Bullet Chart (2025)',
    fontsize=13, fontweight='bold', color=DARK, pad=10)

plt.tight_layout()
out = r'C:/Users/chiny/Code/Mastercard/charts/19c_bench_bullet.png'
plt.savefig(out, dpi=160, bbox_inches='tight', facecolor='white')
print(f'Saved: {out}')
