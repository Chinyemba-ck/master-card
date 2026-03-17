"""
Chart 19b — Percentile Band Chart
IGS Percentile Bands — Where Winnsboro & Archibald Stand (2025)
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

# ── Load & filter data ───────────────────────────────────────────────────────
df = pd.read_csv(r'C:/Users/chiny/Code/ms-resrach/data/national_igs_full.csv')
df = df[df['META_Year'] == 2025].copy()

sub_cols = [c for c in df.columns if c.startswith('PLACE_') or
            c.startswith('ECONOMY_') or c.startswith('COMMUNITY_')]
df['missing_count'] = df[sub_cols].isna().sum(axis=1)
df = df[df['missing_count'] <= 2].copy()

igs_col   = 'SUMMARY_Inclusive Growth Score'
state_col = 'META_State'

national  = df[igs_col].dropna().values
la_mask   = df[state_col].str.strip().str.upper() == 'LA'
louisiana = df.loc[la_mask, igs_col].dropna().values

# Compute percentile cutoffs from national data
p10  = np.percentile(national, 10)
p25  = np.percentile(national, 25)
p50  = np.percentile(national, 50)   # national median
p75  = np.percentile(national, 75)
p90  = np.percentile(national, 90)
la_median = np.median(louisiana)

WIN_IGS = 38
ARC_IGS = 59

# ── Figure ───────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(13, 3), facecolor='white')
ax.set_facecolor('white')

# Band definitions: (x_start, x_end, face_color, label, label_x_offset)
bands = [
    (0,    p10,  '#FADBD8', 'Bottom 10%',   0),
    (p10,  p25,  '#FAE5D3', 'Bottom 25%',   0),
    (p25,  p50,  '#FEF9E7', 'Below Median', 0),
    (p50,  p75,  '#EAFAF1', 'Above Median', 0),
    (p75,  p90,  '#A9DFBF', 'Top 25%',      0),
    (p90,  100,  '#27AE60', 'Top 10%',      0),
]

y_bot, y_top = 0.0, 1.0
for (x0, x1, color, label, _) in bands:
    ax.barh(0.5, x1 - x0, left=x0, height=y_top - y_bot,
            color=color, edgecolor='white', linewidth=0.5, align='center',
            zorder=1)
    mid_x = (x0 + x1) / 2
    # label inside band
    txt_color = 'white' if label == 'Top 10%' else '#555555'
    ax.text(mid_x, 0.82, label, ha='center', va='center',
            fontsize=7.5, color=txt_color, fontweight='bold', zorder=3)
    # percentile values below band
    ax.text(x1, 0.05, f'{x1:.0f}', ha='center', va='bottom',
            fontsize=7, color='#777777', zorder=3)

# Left edge label
ax.text(0, 0.05, '0', ha='center', va='bottom', fontsize=7, color='#777777')

# ── Markers at y=0.5 ────────────────────────────────────────────────────────
marker_y = 0.5
marker_size = 200
label_y_above = 0.72   # annotation y

# National median — gray square
ax.scatter([p50], [marker_y], color=GRAY, marker='s', s=marker_size,
           zorder=10, edgecolors='white', linewidths=0.8)
ax.text(p50, 0.25, f'Natl median\n{p50:.0f}', ha='center', va='top',
        fontsize=8, color=GRAY, fontweight='bold', zorder=11)

# Louisiana median — purple triangle
ax.scatter([la_median], [marker_y], color=LA_COLOR, marker='^', s=marker_size,
           zorder=10, edgecolors='white', linewidths=0.8)
ax.text(la_median, 0.25, f'LA median\n{la_median:.0f}', ha='center', va='top',
        fontsize=8, color=LA_COLOR, fontweight='bold', zorder=11)

# Winnsboro — red diamond
ax.scatter([WIN_IGS], [marker_y], color=WIN_COLOR, marker='D', s=marker_size,
           zorder=12, edgecolors='white', linewidths=0.8)
ax.text(WIN_IGS, label_y_above, f'Winnsboro\nIGS {WIN_IGS}',
        ha='center', va='bottom', fontsize=8.5, color=WIN_COLOR,
        fontweight='bold', zorder=13)

# Archibald — blue circle
ax.scatter([ARC_IGS], [marker_y], color=ARC_COLOR, marker='o', s=marker_size,
           zorder=12, edgecolors='white', linewidths=0.8)
ax.text(ARC_IGS, label_y_above, f'Archibald\nIGS {ARC_IGS}',
        ha='center', va='bottom', fontsize=8.5, color=ARC_COLOR,
        fontweight='bold', zorder=13)

# ── Legend ────────────────────────────────────────────────────────────────────
handles = [
    plt.Line2D([0],[0], marker='D', color='w', markerfacecolor=WIN_COLOR,
               markersize=9, label='Winnsboro (IGS 38)'),
    plt.Line2D([0],[0], marker='o', color='w', markerfacecolor=ARC_COLOR,
               markersize=9, label='Archibald (IGS 59)'),
    plt.Line2D([0],[0], marker='^', color='w', markerfacecolor=LA_COLOR,
               markersize=9, label=f'LA median ({la_median:.0f})'),
    plt.Line2D([0],[0], marker='s', color='w', markerfacecolor=GRAY,
               markersize=9, label=f'National median ({p50:.0f})'),
]
ax.legend(handles=handles, loc='lower right', fontsize=8, framealpha=0.9,
          ncol=4)

# ── Axes styling ─────────────────────────────────────────────────────────────
ax.set_xlim(0, 100)
ax.set_ylim(0, 1)
ax.set_xlabel('IGS Score', fontsize=11, color=DARK)
ax.set_yticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.tick_params(axis='x', labelsize=10, colors=DARK)

ax.set_title(
    'IGS Percentile Bands — Where Winnsboro & Archibald Stand (2025)',
    fontsize=13, fontweight='bold', color=DARK, pad=10)

plt.tight_layout()
out = r'C:/Users/chiny/Code/Mastercard/charts/19b_bench_percentile.png'
plt.savefig(out, dpi=160, bbox_inches='tight', facecolor='white')
print(f'Saved: {out}')
