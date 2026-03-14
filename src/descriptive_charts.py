"""
descriptive_charts.py — Charts 01–07 and 11–13.

Chart 01: IGS + 3 pillars time series (Winnsboro vs Archibald)
Chart 02: Grouped bar — all indicator scores 2025
Chart 03: Correlation heatmap — Winnsboro 2017–2025
Chart 04: Radar chart — pillar breakdown 2025
Chart 05: Scatter plots — Internet Access vs Economy, Labor Engagement vs IGS
Chart 06: Benchmark gap — where Winnsboro falls behind Archibald (legend fixed)
Chart 07: Box plot — IGS distribution across all 7 tracts
Chart 11: Archibald indicator changes year-on-year (what drove IGS 48→59)
Chart 12: The 5 indicators that diverged most (Archibald improved, Winnsboro did not)
Chart 13: Full comparative snapshot — demographics + IGS indicators
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.titlesize': 13,
    'axes.labelsize': 11,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'figure.dpi': 150,
})

WIN_COLOR  = '#C0392B'   # red  — Winnsboro (target, below threshold)
ARC_COLOR  = '#2980B9'   # blue — Archibald (benchmark, rural peer)
AMBER      = '#E67E22'
GREEN      = '#27AE60'
DARK       = '#1A1A2E'
GRAY       = '#7F8C8D'
THRESHOLD  = '#E67E22'

# ── Load data ──────────────────────────────────────────────────────────────
df = pd.read_csv('data/all_tracts_igs_scores.csv')
fr = df[df['FIPS'] == 22041950100].sort_values('Year').copy()   # Winnsboro/Franklin
ri = df[df['FIPS'] == 22083970600].sort_values('Year').copy()   # Archibald/Richland
years = sorted(fr['Year'].unique())

os.makedirs('charts', exist_ok=True)

# ══════════════════════════════════════════════════════════════════════════
# CHART 01 — IGS + 3 Pillars time series
# ══════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(2, 2, figsize=(14, 9))
fig.suptitle(
    'Winnsboro, LA (Franklin Parish) — IGS Trend 2017–2025\n'
    'vs Archibald, LA (Richland Parish) Benchmark',
    fontsize=15, fontweight='bold', y=1.01
)

metrics = [
    ('IGS',       'Inclusive Growth Score (Overall)'),
    ('Place',     'Place Score'),
    ('Economy',   'Economy Score'),
    ('Community', 'Community Score'),
]

for ax, (col, title) in zip(axes.flatten(), metrics):
    fr_vals = fr[col].values
    ri_vals = ri[col].values

    ax.plot(years, fr_vals, 'o-', color=WIN_COLOR, linewidth=2.2,
            markersize=6, label='Winnsboro / Franklin Parish (target)')
    ax.plot(years, ri_vals, 's--', color=ARC_COLOR, linewidth=2.0,
            markersize=5, alpha=0.8, label='Archibald / Richland Parish (benchmark)')
    ax.axhline(45, color=THRESHOLD, linestyle=':', linewidth=1.8,
               label='Challenge threshold (45)')
    ax.fill_between(years, fr_vals, 45,
                    where=(fr_vals < 45), alpha=0.12, color=WIN_COLOR)
    ax.set_title(title, fontweight='bold')
    ax.set_xlabel('Year')
    ax.set_ylabel('Score (0–100)')
    ax.set_ylim(0, 100)
    ax.set_xticks(years)
    ax.legend(fontsize=8)

plt.tight_layout()
plt.savefig('charts/01_time_series.png', bbox_inches='tight')
plt.close()
print('Saved: charts/01_time_series.png')

# ══════════════════════════════════════════════════════════════════════════
# CHART 02 — Grouped bar: all indicator scores 2025
# ══════════════════════════════════════════════════════════════════════════
fr_2025 = fr[fr['Year'] == 2025].iloc[0]
ri_2025 = ri[ri['Year'] == 2025].iloc[0]

indicator_map = {
    # label: (csv_col, pillar)
    'Internet Access':    ('Internet_Access',  'Place'),
    'Affordable Housing': ('Affordable_Housing','Place'),
    'Travel Time':        ('Travel_Time',       'Place'),
    'Net Occupancy':      ('Net_Occupancy',     'Place'),
    'Park Land':          ('Park_Land',         'Place'),
    'Real Estate':        ('Real_Estate',       'Place'),
    'New Businesses':     ('New_Businesses',    'Economy'),
    'Small Biz Loans':    ('Small_Biz_Loans',   'Economy'),
    'Min/Women Biz':      ('Min_Women_Biz',     'Economy'),
    'Labor Engagement':   ('Labor_Engagement',  'Economy'),
    'Comm Diversity':     ('Comm_Diversity',    'Economy'),
    'Personal Income':    ('Personal_Income',   'Community'),
    'Female > Poverty':   ('Female_Poverty',    'Community'),
    'Health Insurance':   ('Health_Insurance',  'Community'),
    'Early Education':    ('Early_Education',   'Community'),
    'Gini Coefficient':   ('Gini',              'Community'),
}

labels      = list(indicator_map.keys())
fr_scores   = [fr_2025.get(indicator_map[l][0], np.nan) for l in labels]
ri_scores   = [ri_2025.get(indicator_map[l][0], np.nan) for l in labels]
pillars     = [indicator_map[l][1] for l in labels]

pillar_colors = {'Place': '#8E44AD', 'Economy': '#16A085', 'Community': '#D35400'}
bar_colors    = [pillar_colors[p] for p in pillars]

x = np.arange(len(labels))
w = 0.38

fig, ax = plt.subplots(figsize=(16, 7))
ax.bar(x - w/2, fr_scores, w, color=bar_colors, alpha=0.9,  label='Winnsboro / Franklin Parish')
ax.bar(x + w/2, ri_scores, w, color=bar_colors, alpha=0.35, label='Archibald / Richland Parish (benchmark)')
ax.axhline(45, color=THRESHOLD, linestyle='--', linewidth=1.5, label='Threshold (45)')
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=40, ha='right')
ax.set_ylabel('Score (0–100)')
ax.set_ylim(0, 110)
ax.set_title('Winnsboro vs Archibald — All Indicator Scores (2025)',
             fontweight='bold', fontsize=14)

patches = [mpatches.Patch(color=v, label=k) for k, v in pillar_colors.items()]
patches += [mpatches.Patch(color='grey', alpha=0.9,  label='Winnsboro (solid)'),
            mpatches.Patch(color='grey', alpha=0.35, label='Archibald (faded)')]
ax.legend(handles=patches, loc='upper right', fontsize=9)
plt.tight_layout()
plt.savefig('charts/02_grouped_bar_indicators.png', bbox_inches='tight')
plt.close()
print('Saved: charts/02_grouped_bar_indicators.png')

# ══════════════════════════════════════════════════════════════════════════
# CHART 03 — Correlation heatmap (Winnsboro 2017–2025)
# ══════════════════════════════════════════════════════════════════════════
score_cols = {l: c for l, (c, _) in indicator_map.items()}
fr_score_df = fr[[c for c in score_cols.values() if c in fr.columns]].copy()
fr_score_df.columns = [l for l, c in score_cols.items() if c in fr.columns]
fr_score_df = fr_score_df.apply(pd.to_numeric, errors='coerce').dropna(axis=1, how='all')

corr = fr_score_df.corr()
fig, ax = plt.subplots(figsize=(12, 10))
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='RdYlGn',
            center=0, vmin=-1, vmax=1, linewidths=0.5, ax=ax,
            annot_kws={'size': 8})
ax.set_title('Correlation Heatmap — Winnsboro / Franklin Parish Indicator Scores (2017–2025)',
             fontweight='bold', fontsize=13, pad=15)
plt.tight_layout()
plt.savefig('charts/03_correlation_heatmap.png', bbox_inches='tight')
plt.close()
print('Saved: charts/03_correlation_heatmap.png')

# ══════════════════════════════════════════════════════════════════════════
# CHART 04 — Radar chart: pillar breakdown 2025
# ══════════════════════════════════════════════════════════════════════════
radar_labels = ['Place', 'Economy', 'Community']

def get_pillar(row, pillar):
    return float(row.get(pillar, 0) or 0)

fr_radar = [get_pillar(fr_2025, 'Place'), get_pillar(fr_2025, 'Economy'), get_pillar(fr_2025, 'Community')]
ri_radar = [get_pillar(ri_2025, 'Place'), get_pillar(ri_2025, 'Economy'), get_pillar(ri_2025, 'Community')]

N      = len(radar_labels)
angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
angles += angles[:1]
fr_r   = fr_radar + fr_radar[:1]
ri_r   = ri_radar + ri_radar[:1]

fig, ax = plt.subplots(figsize=(9, 9), subplot_kw=dict(polar=True))
ax.plot(angles, fr_r, 'o-', color=WIN_COLOR, linewidth=2.2, label='Winnsboro / Franklin Parish')
ax.fill(angles, fr_r, color=WIN_COLOR, alpha=0.18)
ax.plot(angles, ri_r, 's--', color=ARC_COLOR, linewidth=2.0, label='Archibald / Richland Parish')
ax.fill(angles, ri_r, color=ARC_COLOR, alpha=0.12)
ax.plot(angles, [45] * (N + 1), ':', color=THRESHOLD, linewidth=1.5, label='Threshold (45)')
ax.set_thetagrids(np.degrees(angles[:-1]), radar_labels, fontsize=12)
ax.set_ylim(0, 100)
ax.set_title('Pillar Scores — 2025\nWinnsboro vs Archibald',
             fontweight='bold', fontsize=13, pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.35, 1.1), fontsize=10)
plt.tight_layout()
plt.savefig('charts/04_radar_chart.png', bbox_inches='tight')
plt.close()
print('Saved: charts/04_radar_chart.png')

# ══════════════════════════════════════════════════════════════════════════
# CHART 05 — Scatter: Internet Access vs Economy, Labor Engagement vs IGS
# ══════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

scatter_pairs = [
    ('Internet_Access', 'Economy',  'Internet Access Score', 'Economy Score',
     'Internet Access vs Economy Score'),
    ('Labor_Engagement', 'IGS',     'Labor Market Engagement Score', 'Inclusive Growth Score',
     'Labor Market Engagement vs IGS'),
]

for ax, (xcol, ycol, xlabel, ylabel, title) in zip(axes, scatter_pairs):
    fr_x = pd.to_numeric(fr[xcol], errors='coerce')
    fr_y = pd.to_numeric(fr[ycol], errors='coerce')
    ri_x = pd.to_numeric(ri[xcol], errors='coerce')
    ri_y = pd.to_numeric(ri[ycol], errors='coerce')

    ax.scatter(fr_x, fr_y, c=WIN_COLOR, s=80, zorder=5, label='Winnsboro / Franklin')
    ax.scatter(ri_x, ri_y, c=ARC_COLOR, s=80, marker='s', zorder=5,
               alpha=0.8, label='Archibald / Richland')

    for x_val, y_val, yr in zip(fr_x, fr_y, fr['Year']):
        if pd.notna(x_val) and pd.notna(y_val):
            ax.annotate(str(yr), (x_val, y_val), textcoords='offset points',
                        xytext=(5, 4), fontsize=7, color=WIN_COLOR)

    ax.axhline(45, color=THRESHOLD, linestyle='--', linewidth=1.3, label='IGS Threshold (45)')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title, fontweight='bold')
    ax.legend(fontsize=8)

plt.suptitle('Scatter Analysis — Winnsboro / Franklin Parish Key Drivers', fontweight='bold', fontsize=14)
plt.tight_layout()
plt.savefig('charts/05_scatter_plots.png', bbox_inches='tight')
plt.close()
print('Saved: charts/05_scatter_plots.png')

# ══════════════════════════════════════════════════════════════════════════
# CHART 06 — Benchmark gap (legend moved outside bars)
# ══════════════════════════════════════════════════════════════════════════
gap_data = {}
for label, (col, pillar) in indicator_map.items():
    if col in fr.columns:
        fr_val = pd.to_numeric(fr_2025.get(col), errors='coerce')
        ri_val = pd.to_numeric(ri_2025.get(col), errors='coerce')
        if pd.notna(fr_val) and pd.notna(ri_val):
            gap_data[label] = {'Winnsboro': fr_val, 'Archibald': ri_val,
                               'Gap': ri_val - fr_val, 'Pillar': pillar}

gap_df = pd.DataFrame(gap_data).T.sort_values('Gap', ascending=False)

fig, ax = plt.subplots(figsize=(12, 7))
colors = [pillar_colors[p] for p in gap_df['Pillar']]
bars = ax.barh(gap_df.index, gap_df['Gap'], color=colors, alpha=0.85)

ax.axvline(0, color='black', linewidth=0.8)
ax.set_xlabel('Score Gap (Archibald − Winnsboro)', fontsize=11)
ax.set_title('Benchmark Gap: Where Winnsboro Falls Behind Archibald (2025)\n'
             'Negative values = Winnsboro leads; Positive = Archibald leads',
             fontweight='bold', fontsize=13)

# Value labels — offset further right so they don't overlap bars
for bar, (_, row) in zip(bars, gap_df.iterrows()):
    xpos = bar.get_width()
    offset = 1.5
    ax.text(xpos + offset, bar.get_y() + bar.get_height() / 2,
            f'+{xpos:.0f}' if xpos > 0 else f'{xpos:.0f}',
            va='center', fontsize=9)

# Legend placed below the plot to avoid overlapping bars
patches = [mpatches.Patch(color=v, label=k) for k, v in pillar_colors.items()]
ax.legend(handles=patches, loc='lower center', bbox_to_anchor=(0.5, -0.16),
          ncol=3, fontsize=10, frameon=True)

plt.tight_layout()
plt.savefig('charts/06_benchmark_gap.png', bbox_inches='tight')
plt.close()
print('Saved: charts/06_benchmark_gap.png')

# ══════════════════════════════════════════════════════════════════════════
# CHART 07 — Box plot: IGS distribution across all 7 tracts
# ══════════════════════════════════════════════════════════════════════════
tract_names = {
    6019003104:  'Fresno CA\n(3104)',
    6019003302:  'Fresno CA\n(3302)',
    6019005805:  'Fresno CA\n(5805)',
    22041950100: 'Winnsboro\n(Franklin LA)',
    22083970600: 'Archibald\n(Richland LA)',
    48113018501: 'Dallas TX\n(18501)',
    48113019013: 'Dallas TX\n(19013)',
}

box_data  = {}
box_order = list(tract_names.values())
for fips, name in tract_names.items():
    subset = df[df['FIPS'] == fips]['IGS']
    box_data[name] = pd.to_numeric(subset, errors='coerce').dropna().values

fig, ax = plt.subplots(figsize=(13, 6))
bp = ax.boxplot([box_data[n] for n in box_order],
                tick_labels=box_order,
                patch_artist=True, notch=False,
                medianprops=dict(color='black', linewidth=2))

fill_colors = [ARC_COLOR, ARC_COLOR, ARC_COLOR, WIN_COLOR, ARC_COLOR, ARC_COLOR, ARC_COLOR]
for patch, color in zip(bp['boxes'], fill_colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.6)

ax.axhline(45, color=THRESHOLD, linestyle='--', linewidth=1.8, label='Threshold (45)')
ax.set_ylabel('Inclusive Growth Score (2017–2025)')
ax.set_title('IGS Distribution Across All 7 Tracts — 2017–2025\n'
             '(Winnsboro highlighted in red)',
             fontweight='bold', fontsize=13)
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig('charts/07_boxplot_all_tracts.png', bbox_inches='tight')
plt.close()
print('Saved: charts/07_boxplot_all_tracts.png')

# ══════════════════════════════════════════════════════════════════════════
# CHART 11 — What drove Archibald's IGS from 48 to 59?
# ══════════════════════════════════════════════════════════════════════════
indicators = [
    'Net_Occupancy', 'Real_Estate', 'Affordable_Housing', 'Internet_Access', 'Travel_Time',
    'New_Businesses', 'Small_Biz_Loans', 'Min_Women_Biz', 'Labor_Engagement', 'Comm_Diversity',
    'Personal_Income', 'Female_Poverty', 'Gini', 'Early_Education', 'Health_Insurance',
]

ri_pivot = ri.set_index('Year')[indicators]
ri_delta = ri_pivot.diff()

fig, axes = plt.subplots(3, 5, figsize=(20, 12))
fig.suptitle(
    'Archibald (Richland Parish) — Indicator Changes Year-on-Year (2017–2025)\n'
    'Understanding how IGS rose from 48 to 59',
    fontsize=15, fontweight='bold', y=1.01
)

for ax, col in zip(axes.flatten(), indicators):
    vals   = ri_delta[col].dropna()
    colors = [GREEN if v >= 0 else WIN_COLOR for v in vals]
    ax.bar(vals.index, vals.values, color=colors, alpha=0.85)
    ax.axhline(0, color='black', linewidth=0.8)
    ax.set_title(col.replace('_', ' '), fontweight='bold', fontsize=10)
    ax.set_xticks(vals.index)
    ax.set_xticklabels([str(y)[2:] for y in vals.index], fontsize=7)
    ax.axvline(2023, color=AMBER, linestyle='--', linewidth=1.2, alpha=0.7)

# Last panel: IGS trajectory overlay
ax_igs = axes[2][4]
ax_igs.clear()
ax_igs.plot(years, ri['IGS'].values, 'o-', color=ARC_COLOR, linewidth=2.5,
            markersize=6, label='Archibald IGS')
ax_igs.plot(years, fr['IGS'].values, 's--', color=WIN_COLOR, linewidth=2.0,
            markersize=5, label='Winnsboro IGS')
ax_igs.axhline(45, color=THRESHOLD, linestyle=':', linewidth=1.5, label='Threshold (45)')
ax_igs.axvline(2023, color=AMBER, linestyle='--', linewidth=1.2, alpha=0.7, label='2023 jump')
ax_igs.set_title('IGS Trajectory', fontweight='bold', fontsize=10)
ax_igs.set_ylim(25, 70)
ax_igs.legend(fontsize=7)
ax_igs.set_xticks(years)
ax_igs.set_xticklabels([str(y)[2:] for y in years], fontsize=7)

fig.legend(
    handles=[
        mpatches.Patch(color=GREEN, label='Improved'),
        mpatches.Patch(color=WIN_COLOR, label='Declined'),
        mpatches.Patch(color=AMBER, label='2023 — peak jump year'),
    ],
    loc='lower center', ncol=3, fontsize=10, bbox_to_anchor=(0.5, -0.02)
)
plt.tight_layout()
plt.savefig('charts/11_richland_igs_drivers.png', bbox_inches='tight')
plt.close()
print('Saved: charts/11_richland_igs_drivers.png')

# ══════════════════════════════════════════════════════════════════════════
# CHART 12 — The 5 indicators that diverged most
# ══════════════════════════════════════════════════════════════════════════
diverged = {
    'Travel Time\nto Work':     ('Travel_Time',     fr['Travel_Time'].values,     ri['Travel_Time'].values),
    'Early\nEducation':         ('Early_Education', fr['Early_Education'].values, ri['Early_Education'].values),
    'Net\nOccupancy':           ('Net_Occupancy',   fr['Net_Occupancy'].values,   ri['Net_Occupancy'].values),
    'Labor Market\nEngagement': ('Labor_Engagement',fr['Labor_Engagement'].values,ri['Labor_Engagement'].values),
    'Personal\nIncome':         ('Personal_Income', fr['Personal_Income'].values, ri['Personal_Income'].values),
}

fig, axes = plt.subplots(1, 5, figsize=(18, 6), sharey=False)
fig.suptitle(
    'The 5 Indicators That Diverged Most — Archibald Improved, Winnsboro Did Not\n'
    'Winnsboro was ahead on all five in 2017; these are the lessons to apply',
    fontsize=13, fontweight='bold'
)

for ax, (label, (col, fr_vals, ri_vals)) in zip(axes, diverged.items()):
    ax.plot(years, ri_vals, 'o-', color=ARC_COLOR, linewidth=2.5, markersize=6,
            label='Archibald / Richland')
    ax.plot(years, fr_vals, 's--', color=WIN_COLOR, linewidth=2.0, markersize=5,
            label='Winnsboro / Franklin')
    ax.axhline(45, color=THRESHOLD, linestyle=':', linewidth=1.2)
    ax.set_title(label, fontweight='bold', fontsize=11)
    ax.set_ylim(0, 100)
    ax.set_xticks(years)
    ax.set_xticklabels([str(y)[2:] for y in years], fontsize=7)
    ax.set_xlabel('Year')
    ax.annotate(f'WIN {fr_vals[0]:.0f}', (years[0],  fr_vals[0]),
                textcoords='offset points', xytext=(-5, -14), fontsize=7, color=WIN_COLOR)
    ax.annotate(f'WIN {fr_vals[-1]:.0f}', (years[-1], fr_vals[-1]),
                textcoords='offset points', xytext=(2, 4), fontsize=7, color=WIN_COLOR)
    ax.annotate(f'ARC {ri_vals[0]:.0f}', (years[0],  ri_vals[0]),
                textcoords='offset points', xytext=(-5, 4), fontsize=7, color=ARC_COLOR)
    ax.annotate(f'ARC {ri_vals[-1]:.0f}', (years[-1], ri_vals[-1]),
                textcoords='offset points', xytext=(2, 4), fontsize=7, color=ARC_COLOR)

axes[0].legend(fontsize=9)
plt.tight_layout()
plt.savefig('charts/12_divergence_analysis.png', bbox_inches='tight')
plt.close()
print('Saved: charts/12_divergence_analysis.png')

# ══════════════════════════════════════════════════════════════════════════
# CHART 13 — Full comparative snapshot
# ══════════════════════════════════════════════════════════════════════════
demographics = {
    'Metric': [
        'Population (2023)',
        'Median HH Income',
        'Poverty Rate (%)',
        'Black/African Am. (%)',
        'Median Age',
        'High School+ (%)',
        "Bachelor's+ (%)",
        'Owner-occupied housing (%)',
    ],
    'Winnsboro\n(Franklin Parish)': [19600, 44103, 19.0, 28.7, 40.2, 80.1, 10.2, 66.4],
    'Archibald\n(Richland Parish)': [20200, 37800, 24.1, 54.8, 38.1, 78.9, 13.1, 63.0],
    'US Average':                   [None,  74755, 11.5, 13.6, 38.9, 89.4, 35.7, 64.8],
}
demo_df = pd.DataFrame(demographics)

igs_comparison = {
    'Indicator':  [
        'Overall IGS', 'Place Score', 'Economy Score', 'Community Score',
        'Internet Access', 'Travel Time', 'Net Occupancy',
        'New Businesses', 'Labor Engagement', 'Commercial Diversity',
        'Early Education', 'Health Insurance', 'Female Above Poverty',
    ],
    'Winnsboro': [38, 32, 40, 42, 2,  9,  38, 73, 14, 36, 19, 59, 69],
    'Archibald': [59, 62, 40, 59, 3, 70, 85, 68, 58, 21, 69, 51, 65],
}
igs_df = pd.DataFrame(igs_comparison)
igs_df['Gap'] = igs_df['Archibald'] - igs_df['Winnsboro']

fig, axes = plt.subplots(1, 2, figsize=(16, 8))
fig.suptitle(
    'Winnsboro vs Archibald — Full Comparative Snapshot (2025)\n'
    'Demographics (Census ACS 2023) + IGS Indicator Scores',
    fontsize=13, fontweight='bold'
)

# Left panel: IGS indicators
ax = axes[0]
y_pos = np.arange(len(igs_df))
bar_w = 0.35
ax.barh(y_pos - bar_w/2, igs_df['Winnsboro'], bar_w,
        color=WIN_COLOR, alpha=0.85, label='Winnsboro / Franklin Parish')
ax.barh(y_pos + bar_w/2, igs_df['Archibald'], bar_w,
        color=ARC_COLOR, alpha=0.85, label='Archibald / Richland Parish')
ax.set_yticks(y_pos)
ax.set_yticklabels(igs_df['Indicator'], fontsize=9)
ax.set_xlabel('Score (0–100)')
ax.set_title('IGS Indicator Scores (2025)', fontweight='bold')
ax.axvline(45, color=AMBER, linestyle='--', linewidth=1.3, label='Threshold (45)')
ax.legend(fontsize=9)
ax.set_xlim(0, 110)

for i, row in igs_df.iterrows():
    gap   = row['Gap']
    color = ARC_COLOR if gap > 0 else WIN_COLOR
    label = f'+{gap}' if gap > 0 else str(gap)
    ax.text(max(row['Winnsboro'], row['Archibald']) + 1.5, i,
            label, va='center', fontsize=7.5, color=color, fontweight='bold')

# Right panel: demographics table
ax2 = axes[1]
ax2.axis('off')

col_labels = ['Metric', 'Winnsboro\n(Franklin)', 'Archibald\n(Richland)', 'US Avg']
table_rows = []
for _, row in demo_df.iterrows():
    fr_v = row['Winnsboro\n(Franklin Parish)']
    ri_v = row['Archibald\n(Richland Parish)']
    us_v = row['US Average']
    metric = row['Metric']
    if metric == 'Population (2023)':
        table_rows.append([metric, f'{int(fr_v):,}', f'{int(ri_v):,}', 'n/a'])
    elif metric == 'Median HH Income':
        table_rows.append([metric, f'${int(fr_v):,}', f'${int(ri_v):,}', f'${int(us_v):,}'])
    elif us_v is None:
        table_rows.append([metric, str(fr_v), str(ri_v), 'n/a'])
    else:
        table_rows.append([metric, f'{fr_v}%', f'{ri_v}%', f'{us_v}%'])

table = ax2.table(
    cellText=table_rows,
    colLabels=col_labels,
    cellLoc='center',
    loc='center',
    bbox=[0, 0.15, 1, 0.82]
)
table.auto_set_font_size(False)
table.set_fontsize(9.5)

for j in range(4):
    table[0, j].set_facecolor(DARK)
    table[0, j].set_text_props(color='white', fontweight='bold')

# Highlight Winnsboro-favorable rows (higher income, lower poverty)
highlights_win = {'Median HH Income', 'Poverty Rate (%)'}
highlights_arc = {'Black/African Am. (%)'}
for i, row in enumerate(table_rows, start=1):
    metric = row[0]
    if metric in highlights_win:
        for j in range(4):
            table[i, j].set_facecolor('#FFF0F0')
    elif metric in highlights_arc:
        for j in range(4):
            table[i, j].set_facecolor('#F0F0FF')

ax2.text(
    0.5, 0.07,
    'KEY INSIGHT: Winnsboro has HIGHER median income and LOWER poverty than Archibald.\n'
    'Yet Archibald scores 21 pts higher on IGS. The gap is economic infrastructure —\n'
    'not demographics. Archibald built it. Winnsboro can too.',
    transform=ax2.transAxes, ha='center', va='center',
    fontsize=9.5, style='italic', color=DARK,
    bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFFBEA', edgecolor=AMBER, linewidth=1.5)
)
ax2.set_title('Census ACS 2023 — Demographic Comparison', fontweight='bold')

plt.tight_layout()
plt.savefig('charts/13_comparative_snapshot.png', bbox_inches='tight')
plt.close()
print('Saved: charts/13_comparative_snapshot.png')

print('\nAll charts saved to charts/')
