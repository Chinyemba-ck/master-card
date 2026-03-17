"""
Redesigned Winnsboro vs Archibald benchmark chart.
Vertical grouped bars — one cluster per indicator, actual scores (0–100),
sorted by Archibald advantage (biggest gap last).
Winner label above each cluster for instant readability.
Output: charts/06_benchmark_gap.png  (overwrites old diverging-bar version)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# ── Colors ────────────────────────────────────────────────────────────────────
WIN_COLOR  = '#C0392B'   # red  — Winnsboro
ARC_COLOR  = '#2980B9'   # blue — Archibald
WIN_LEAD   = '#E8F8EE'   # pale green bg when Winnsboro wins
ARC_LEAD   = '#EBF5FB'   # pale blue  bg when Archibald wins
AMBER      = '#E67E22'
DARK       = '#1A1A2E'
GRAY       = '#7F8C8D'

# ── Load data ─────────────────────────────────────────────────────────────────
df = pd.read_csv('data/all_tracts_igs_scores.csv')
win = df[df['FIPS'] == 22041950100].sort_values('Year')
arc = df[df['FIPS'] == 22083970600].sort_values('Year')

win25 = win[win['Year'] == win['Year'].max()].iloc[0]
arc25 = arc[arc['Year'] == arc['Year'].max()].iloc[0]

# ── Indicator mapping: (column_name, display_label, category) ─────────────────
indicators = [
    ('Internet_Access',  'Internet\nAccess',    'Place'),
    ('Travel_Time',      'Travel\nTime',         'Place'),
    ('Net_Occupancy',    'Net\nOccupancy',       'Place'),
    ('Real_Estate',      'Real\nEstate',         'Place'),
    ('Affordable_Housing','Affordable\nHousing', 'Place'),
    ('Park_Land',        'Park\nLand',           'Place'),
    ('New_Businesses',   'New\nBusinesses',      'Economy'),
    ('Small_Biz_Loans',  'Small Biz\nLoans',     'Economy'),
    ('Min_Women_Biz',    'Min/Women\nBiz',       'Economy'),
    ('Labor_Engagement', 'Labor\nEngagement',    'Economy'),
    ('Comm_Diversity',   'Comm\nDiversity',      'Economy'),
    ('Personal_Income',  'Personal\nIncome',     'Community'),
    ('Female_Poverty',   'Female >\nPoverty',    'Community'),
    ('Gini',             'Gini\nCoefficient',    'Community'),
    ('Early_Education',  'Early\nEducation',     'Community'),
    ('Health_Insurance', 'Health\nInsurance',    'Community'),
]

# Filter to columns that exist
indicators = [(col, lbl, cat) for col, lbl, cat in indicators if col in win25.index]

# Build records
records = []
for col, lbl, cat in indicators:
    w = int(round(win25[col]))
    a = int(round(arc25[col]))
    gap = a - w   # positive = Archibald leads
    records.append({'col': col, 'label': lbl, 'cat': cat,
                    'win': w, 'arc': a, 'gap': gap})

data = pd.DataFrame(records).sort_values('gap')   # ascending: Winnsboro wins on left

n = len(data)
x = np.arange(n)
bar_w = 0.36

# ── Figure ────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(18, 8))
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

# Shaded background bands by category
cat_order = ['Place', 'Economy', 'Community']
cat_colors = {'Place': '#F8F0FF', 'Economy': '#F0F8FF', 'Community': '#FFF8F0'}

current_cat = None
band_start = 0
for i, row in enumerate(data.itertuples()):
    if row.cat != current_cat:
        if current_cat is not None:
            ax.axvspan(band_start - 0.5, i - 0.5,
                       color=cat_colors[current_cat], alpha=0.45, zorder=0)
        current_cat = row.cat
        band_start = i
ax.axvspan(band_start - 0.5, n - 0.5,
           color=cat_colors[current_cat], alpha=0.45, zorder=0)

# Bars
bars_w = ax.bar(x - bar_w/2, data['win'], bar_w,
                color=WIN_COLOR, alpha=0.88, label='Winnsboro (IGS 38)', zorder=3)
bars_a = ax.bar(x + bar_w/2, data['arc'], bar_w,
                color=ARC_COLOR, alpha=0.88, label='Archibald (IGS 59)', zorder=3)

# Score labels inside bars
for bar, val in zip(bars_w, data['win']):
    if val > 12:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() - 5,
                str(val), ha='center', va='top', fontsize=8,
                color='white', fontweight='bold')
    else:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
                str(val), ha='center', va='bottom', fontsize=8,
                color=WIN_COLOR, fontweight='bold')

for bar, val in zip(bars_a, data['arc']):
    if val > 12:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() - 5,
                str(val), ha='center', va='top', fontsize=8,
                color='white', fontweight='bold')
    else:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
                str(val), ha='center', va='bottom', fontsize=8,
                color=ARC_COLOR, fontweight='bold')

# Winner label above each cluster
for i, row in enumerate(data.itertuples()):
    if row.gap > 0:
        lbl = f'+{row.gap}'
        col = ARC_COLOR
    elif row.gap < 0:
        lbl = f'{row.gap}'
        col = WIN_COLOR
    else:
        lbl = '='
        col = GRAY
    ax.text(i, max(row.win, row.arc) + 2.5, lbl,
            ha='center', va='bottom', fontsize=8.5,
            color=col, fontweight='bold')

# Category labels at top
cat_label_positions = {}
prev_cat = None
for i, row in enumerate(data.itertuples()):
    if row.cat != prev_cat:
        cat_label_positions[row.cat] = [i, i]
        prev_cat = row.cat
    else:
        cat_label_positions[row.cat][1] = i

for cat, (start, end) in cat_label_positions.items():
    mid = (start + end) / 2
    ax.text(mid, 103, cat.upper(), ha='center', va='bottom',
            fontsize=9, fontweight='bold', color=DARK,
            bbox=dict(boxstyle='round,pad=0.3', fc=cat_colors[cat], ec='#CCCCCC', alpha=0.9))

# Threshold line
ax.axhline(45, color=AMBER, linestyle='--', linewidth=1.4, zorder=2, alpha=0.8)
ax.text(n - 0.4, 45.8, 'IGS threshold (45)', color=AMBER,
        fontsize=8.5, va='bottom', ha='right', style='italic')

# Axes
ax.set_xticks(x)
ax.set_xticklabels(data['label'], fontsize=9)
ax.set_ylabel('IGS Indicator Score (0–100)', fontsize=11)
ax.set_ylim(0, 112)
ax.set_xlim(-0.6, n - 0.4)
ax.tick_params(axis='x', length=0)
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
ax.spines['left'].set_color('#CCCCCC')
ax.spines['bottom'].set_color('#CCCCCC')
ax.yaxis.set_tick_params(color='#CCCCCC')
ax.grid(axis='y', linestyle=':', alpha=0.4, zorder=0)

# Title + subtitle
fig.suptitle('Winnsboro vs Archibald — Indicator-by-Indicator Comparison (2025)',
             fontsize=15, fontweight='bold', color=DARK, y=0.99)
ax.set_title(
    'Gap labels show Archibald advantage (+) or Winnsboro lead (−)  ·  '
    'Winnsboro IGS 38  ·  Archibald IGS 59  ·  Same rural NE Louisiana region',
    fontsize=9.5, color=GRAY, pad=6)

# Legend
legend_patches = [
    mpatches.Patch(color=WIN_COLOR, alpha=0.88, label='Winnsboro — Franklin Parish (IGS 38)'),
    mpatches.Patch(color=ARC_COLOR, alpha=0.88, label='Archibald — Richland Parish (IGS 59)'),
]
ax.legend(handles=legend_patches, loc='upper left', fontsize=10,
          framealpha=0.9, edgecolor='#CCCCCC')

plt.tight_layout(rect=[0, 0, 1, 0.97])
out = os.path.join('charts', '06_benchmark_gap.png')
plt.savefig(out, dpi=160, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Saved: {out}")
