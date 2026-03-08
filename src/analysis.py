"""
Mastercard IGS Challenge - Franklin Parish, LA Analysis
Census Tract 22041950100 vs Richland Parish Benchmark (22083970600)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import os
from matplotlib.gridspec import GridSpec

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# ── Style ──────────────────────────────────────────────────────────────────
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
FRANKLIN_COLOR = '#C0392B'   # red  – low IGS
RICHLAND_COLOR = '#2980B9'   # blue – benchmark
THRESHOLD_COLOR = '#E67E22'  # orange – challenge threshold

# ── Load Data ──────────────────────────────────────────────────────────────
files = sorted([f for f in os.listdir('igs_exports') if f.endswith('.xlsx')])
all_data = []
for fname in files:
    df = pd.read_excel(os.path.join('igs_exports', fname), sheet_name='Compared to Urban-Rural', header=[0, 1])
    df.columns = ['_'.join([str(c) for c in col]).strip() for col in df.columns]
    data_rows = df.iloc[1:].dropna(subset=['META_Census Tract FIPS code'])
    all_data.append(data_rows)

combined = pd.concat(all_data, ignore_index=True)
combined['FIPS'] = combined['META_Census Tract FIPS code'].astype(int)
combined['Year'] = combined['META_Year'].astype(int)

franklin = combined[combined['FIPS'] == 22041950100].sort_values('Year').copy()
richland = combined[combined['FIPS'] == 22083970600].sort_values('Year').copy()

# Latest year snapshots
fr_2025 = franklin[franklin['Year'] == 2025].iloc[0]
ri_2025 = richland[richland['Year'] == 2025].iloc[0]

os.makedirs('charts', exist_ok=True)

# ══════════════════════════════════════════════════════════════════════════
# CHART 1 – Time Series: IGS + 3 Pillars over time
# ══════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(2, 2, figsize=(14, 9))
fig.suptitle('Franklin Parish, LA — IGS Trend 2017–2025\nvs Richland Parish Benchmark', fontsize=15, fontweight='bold', y=1.01)

metrics = [
    ('SUMMARY_Inclusive Growth Score', 'Inclusive Growth Score (Overall)'),
    ('PLACE_Place',                    'Place Score'),
    ('ECONOMY_Economy',                'Economy Score'),
    ('COMMUNITY_Community',            'Community Score'),
]

for ax, (col, title) in zip(axes.flatten(), metrics):
    fr_vals = franklin[col].values
    ri_vals = richland[col].values
    years   = franklin['Year'].values

    ax.plot(years, fr_vals, 'o-', color=FRANKLIN_COLOR, linewidth=2.2,
            markersize=6, label='Franklin Parish (target)')
    ax.plot(years, ri_vals, 's--', color=RICHLAND_COLOR, linewidth=2.0,
            markersize=5, alpha=0.8, label='Richland Parish (benchmark)')
    ax.axhline(45, color=THRESHOLD_COLOR, linestyle=':', linewidth=1.8,
               label='Challenge threshold (45)')
    ax.fill_between(years, fr_vals, 45,
                    where=(fr_vals < 45), alpha=0.12, color=FRANKLIN_COLOR)
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
# CHART 2 – Grouped Bar: All indicator scores Franklin vs Richland (2025)
# ══════════════════════════════════════════════════════════════════════════
indicator_scores = {
    # PLACE
    'Internet Access':          ('PLACE_Internet Access Score',             'Place'),
    'Affordable Housing':       ('PLACE_Affordable Housing Score',          'Place'),
    'Travel Time to Work':      ('PLACE_Travel Time to Work Score',         'Place'),
    'Net Occupancy':            ('PLACE_Net Occupancy Score',               'Place'),
    'Park Land':                ('PLACE_Acres of Park Land Score',          'Place'),
    'Real Estate Value':        ('PLACE_Residential Real Estate Value Score','Place'),
    # ECONOMY
    'New Businesses':           ('ECONOMY_New Businesses Score',            'Economy'),
    'Small Biz Loans':          ('ECONOMY_Small Business Loans Score',      'Economy'),
    'Min/Women Biz':            ('ECONOMY_Minority/Women Owned Businesses Score','Economy'),
    'Labor Mkt Engagement':     ('ECONOMY_Labor Market Engagement Index Score','Economy'),
    'Commercial Diversity':     ('ECONOMY_Commercial Diversity Score',      'Economy'),
    # COMMUNITY
    'Personal Income':          ('COMMUNITY_Personal Income Score',         'Community'),
    'Female Above Poverty':     ('COMMUNITY_Female Above Poverty Score',    'Community'),
    'Health Insurance':         ('COMMUNITY_Health Insurance Coverage Score','Community'),
    'Early Education':          ('COMMUNITY_Early Education Enrollment Score','Community'),
    'Gini Coefficient':         ('COMMUNITY_Gini Coefficient Score',        'Community'),
}

labels   = list(indicator_scores.keys())
fr_scores = [fr_2025.get(indicator_scores[l][0], np.nan) for l in labels]
ri_scores = [ri_2025.get(indicator_scores[l][0], np.nan) for l in labels]
pillars   = [indicator_scores[l][1] for l in labels]

pillar_colors = {'Place': '#8E44AD', 'Economy': '#16A085', 'Community': '#D35400'}
bar_colors    = [pillar_colors[p] for p in pillars]

x  = np.arange(len(labels))
w  = 0.38

fig, ax = plt.subplots(figsize=(16, 7))
bars1 = ax.bar(x - w/2, fr_scores, w, color=bar_colors, alpha=0.9,  label='Franklin Parish')
bars2 = ax.bar(x + w/2, ri_scores, w, color=bar_colors, alpha=0.35, label='Richland Parish (benchmark)')

ax.axhline(45, color=THRESHOLD_COLOR, linestyle='--', linewidth=1.5, label='Threshold (45)')
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=40, ha='right')
ax.set_ylabel('Score (0–100)')
ax.set_ylim(0, 110)
ax.set_title('Franklin Parish vs Richland Parish — All Indicator Scores (2025)',
             fontweight='bold', fontsize=14)

# Pillar legend patches
patches = [mpatches.Patch(color=v, label=k) for k, v in pillar_colors.items()]
patches += [mpatches.Patch(color='grey', alpha=0.9,  label='Franklin (solid)'),
            mpatches.Patch(color='grey', alpha=0.35, label='Richland (faded)')]
ax.legend(handles=patches, loc='upper right', fontsize=9)

plt.tight_layout()
plt.savefig('charts/02_grouped_bar_indicators.png', bbox_inches='tight')
plt.close()
print('Saved: charts/02_grouped_bar_indicators.png')

# ══════════════════════════════════════════════════════════════════════════
# CHART 3 – Correlation Heatmap (Franklin all years, score columns)
# ══════════════════════════════════════════════════════════════════════════
score_cols = {k: v[0] for k, v in indicator_scores.items()}
fr_scores_df = franklin[[c for c in score_cols.values() if c in franklin.columns]].copy()
fr_scores_df.columns = [k for k, v in score_cols.items() if v in franklin.columns]
fr_scores_df = fr_scores_df.apply(pd.to_numeric, errors='coerce').dropna(axis=1, how='all')

corr = fr_scores_df.corr()

fig, ax = plt.subplots(figsize=(12, 10))
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='RdYlGn',
            center=0, vmin=-1, vmax=1, linewidths=0.5, ax=ax,
            annot_kws={'size': 8})
ax.set_title('Correlation Heatmap — Franklin Parish Indicator Scores (2017–2025)',
             fontweight='bold', fontsize=13, pad=15)
plt.tight_layout()
plt.savefig('charts/03_correlation_heatmap.png', bbox_inches='tight')
plt.close()
print('Saved: charts/03_correlation_heatmap.png')

# ══════════════════════════════════════════════════════════════════════════
# CHART 4 – Radar / Spider Chart: Pillar breakdown 2025
# ══════════════════════════════════════════════════════════════════════════
radar_labels = ['Place', 'Place\nGrowth', 'Place\nInclusion',
                'Economy', 'Economy\nGrowth', 'Economy\nInclusion',
                'Community', 'Community\nGrowth', 'Community\nInclusion']
radar_cols_fr = [
    float(fr_2025.get('PLACE_Place', 0) or 0),
    float(fr_2025.get('PLACE_Place Growth', 0) or 0),
    float(fr_2025.get('PLACE_Place Inclusion', 0) or 0),
    float(fr_2025.get('ECONOMY_Economy', 0) or 0),
    float(fr_2025.get('ECONOMY_Economy Growth', 0) or 0),
    float(fr_2025.get('ECONOMY_Economy Inclusion', 0) or 0),
    float(fr_2025.get('COMMUNITY_Community', 0) or 0),
    float(fr_2025.get('COMMUNITY_Community Growth', 0) or 0),
    float(fr_2025.get('COMMUNITY_Community Inclusion', 0) or 0),
]
radar_cols_ri = [
    float(ri_2025.get('PLACE_Place', 0) or 0),
    float(ri_2025.get('PLACE_Place Growth', 0) or 0),
    float(ri_2025.get('PLACE_Place Inclusion', 0) or 0),
    float(ri_2025.get('ECONOMY_Economy', 0) or 0),
    float(ri_2025.get('ECONOMY_Economy Growth', 0) or 0),
    float(ri_2025.get('ECONOMY_Economy Inclusion', 0) or 0),
    float(ri_2025.get('COMMUNITY_Community', 0) or 0),
    float(ri_2025.get('COMMUNITY_Community Growth', 0) or 0),
    float(ri_2025.get('COMMUNITY_Community Inclusion', 0) or 0),
]

N     = len(radar_labels)
angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
angles += angles[:1]
fr_vals_r = radar_cols_fr + radar_cols_fr[:1]
ri_vals_r = radar_cols_ri + radar_cols_ri[:1]

fig, ax = plt.subplots(figsize=(9, 9), subplot_kw=dict(polar=True))
ax.plot(angles, fr_vals_r, 'o-', color=FRANKLIN_COLOR, linewidth=2.2, label='Franklin Parish')
ax.fill(angles, fr_vals_r, color=FRANKLIN_COLOR, alpha=0.18)
ax.plot(angles, ri_vals_r, 's--', color=RICHLAND_COLOR, linewidth=2.0, label='Richland Parish')
ax.fill(angles, ri_vals_r, color=RICHLAND_COLOR, alpha=0.12)
ax.plot(angles, [45] * (N + 1), ':', color=THRESHOLD_COLOR, linewidth=1.5, label='Threshold (45)')

ax.set_thetagrids(np.degrees(angles[:-1]), radar_labels, fontsize=10)
ax.set_ylim(0, 100)
ax.set_title('Pillar & Sub-dimension Scores — 2025\nFranklin vs Richland Parish',
             fontweight='bold', fontsize=13, pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=10)
plt.tight_layout()
plt.savefig('charts/04_radar_chart.png', bbox_inches='tight')
plt.close()
print('Saved: charts/04_radar_chart.png')

# ══════════════════════════════════════════════════════════════════════════
# CHART 5 – Scatter: Economy Score vs Internet Access (all years, both tracts)
# ══════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

scatter_pairs = [
    ('PLACE_Internet Access Tract, %',          'ECONOMY_Economy',
     'Internet Access (%)', 'Economy Score',
     'Internet Access vs Economy Score'),
    ('ECONOMY_Labor Market Engagement Index Tract', 'SUMMARY_Inclusive Growth Score',
     'Labor Market Engagement (%)', 'Inclusive Growth Score',
     'Labor Market Engagement vs IGS'),
]

for ax, (xcol, ycol, xlabel, ylabel, title) in zip(axes, scatter_pairs):
    fr_x = pd.to_numeric(franklin[xcol], errors='coerce')
    fr_y = pd.to_numeric(franklin[ycol], errors='coerce')
    ri_x = pd.to_numeric(richland[xcol], errors='coerce')
    ri_y = pd.to_numeric(richland[ycol], errors='coerce')

    sc1 = ax.scatter(fr_x, fr_y, c=FRANKLIN_COLOR, s=80, zorder=5, label='Franklin Parish')
    sc2 = ax.scatter(ri_x, ri_y, c=RICHLAND_COLOR, s=80, marker='s', zorder=5,
                     alpha=0.8, label='Richland Parish')

    # Year labels on Franklin points
    for x_val, y_val, yr in zip(fr_x, fr_y, franklin['Year']):
        if pd.notna(x_val) and pd.notna(y_val):
            ax.annotate(str(yr), (x_val, y_val), textcoords='offset points',
                        xytext=(5, 4), fontsize=7, color=FRANKLIN_COLOR)

    ax.axhline(45, color=THRESHOLD_COLOR, linestyle='--', linewidth=1.3,
               label='IGS Threshold (45)')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title, fontweight='bold')
    ax.legend(fontsize=8)

plt.suptitle('Scatter Analysis — Franklin Parish Key Drivers', fontweight='bold', fontsize=14)
plt.tight_layout()
plt.savefig('charts/05_scatter_plots.png', bbox_inches='tight')
plt.close()
print('Saved: charts/05_scatter_plots.png')

# ══════════════════════════════════════════════════════════════════════════
# CHART 6 – Bottom-indicator bar chart (biggest gaps vs benchmark)
# ══════════════════════════════════════════════════════════════════════════
gap_data = {}
for label, (col, pillar) in indicator_scores.items():
    if col in franklin.columns:
        fr_val = pd.to_numeric(fr_2025.get(col), errors='coerce')
        ri_val = pd.to_numeric(ri_2025.get(col), errors='coerce')
        if pd.notna(fr_val) and pd.notna(ri_val):
            gap_data[label] = {'Franklin': fr_val, 'Richland': ri_val,
                               'Gap': ri_val - fr_val, 'Pillar': pillar}

gap_df = pd.DataFrame(gap_data).T.sort_values('Gap', ascending=False)

fig, ax = plt.subplots(figsize=(12, 7))
colors = [pillar_colors[p] for p in gap_df['Pillar']]
bars = ax.barh(gap_df.index, gap_df['Gap'], color=colors, alpha=0.85)

ax.axvline(0, color='black', linewidth=0.8)
ax.set_xlabel('Score Gap (Richland − Franklin)', fontsize=11)
ax.set_title('Benchmark Gap: Where Franklin Parish Falls Behind Richland Parish (2025)',
             fontweight='bold', fontsize=13)

# Add value labels
for bar, (_, row) in zip(bars, gap_df.iterrows()):
    xpos = bar.get_width()
    ax.text(xpos + 0.5, bar.get_y() + bar.get_height() / 2,
            f"+{xpos:.0f}" if xpos > 0 else f"{xpos:.0f}",
            va='center', fontsize=9)

patches = [mpatches.Patch(color=v, label=k) for k, v in pillar_colors.items()]
ax.legend(handles=patches, loc='lower right', fontsize=9)
plt.tight_layout()
plt.savefig('charts/06_benchmark_gap.png', bbox_inches='tight')
plt.close()
print('Saved: charts/06_benchmark_gap.png')

# ══════════════════════════════════════════════════════════════════════════
# CHART 7 – Box Plot: Score distributions across all 7 tracts (all years)
# ══════════════════════════════════════════════════════════════════════════
tract_names = {
    6019003104: 'Fresno CA\n(3104)',
    6019003302: 'Fresno CA\n(3302)',
    6019005805: 'Fresno CA\n(5805)',
    22041950100: 'Franklin\nParish LA',
    22083970600: 'Richland\nParish LA',
    48113018501: 'Dallas TX\n(18501)',
    48113019013: 'Dallas TX\n(19013)',
}

box_data = {}
for fips, name in tract_names.items():
    subset = combined[combined['FIPS'] == fips]['SUMMARY_Inclusive Growth Score']
    box_data[name] = pd.to_numeric(subset, errors='coerce').dropna().values

fig, ax = plt.subplots(figsize=(13, 6))
bp = ax.boxplot(list(box_data.values()), tick_labels=list(box_data.keys()),
                patch_artist=True, notch=False,
                medianprops=dict(color='black', linewidth=2))

box_fill_colors = [
    '#2980B9', FRANKLIN_COLOR, '#2980B9',   # Fresno tracts
    FRANKLIN_COLOR, '#2980B9',               # LA tracts (Franklin red, Richland blue)
    '#2980B9', FRANKLIN_COLOR,               # Dallas tracts
]
for patch, color in zip(bp['boxes'], box_fill_colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.6)

ax.axhline(45, color=THRESHOLD_COLOR, linestyle='--', linewidth=1.8, label='Threshold (45)')
ax.set_ylabel('Inclusive Growth Score (2017–2025)')
ax.set_title('IGS Distribution Across All 7 Tracts — 2017–2025',
             fontweight='bold', fontsize=13)
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig('charts/07_boxplot_all_tracts.png', bbox_inches='tight')
plt.close()
print('Saved: charts/07_boxplot_all_tracts.png')

# ══════════════════════════════════════════════════════════════════════════
# Print key stats summary
# ══════════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("FRANKLIN PARISH — KEY STATS SUMMARY (2025)")
print("="*60)
critical = [
    ('Internet Access',         'PLACE_Internet Access Score',               'PLACE_Internet Access Tract, %',   'PLACE_Internet Access Base, %'),
    ('Travel Time to Work',     'PLACE_Travel Time to Work Score',           'PLACE_Travel Time to Work Tract, %','PLACE_Travel Time to Work Base, %'),
    ('Min/Women Owned Biz',     'ECONOMY_Minority/Women Owned Businesses Score','ECONOMY_Minority/Women Owned Businesses Tract, %','ECONOMY_Minority/Women Owned Businesses Base, %'),
    ('Labor Mkt Engagement',    'ECONOMY_Labor Market Engagement Index Score','ECONOMY_Labor Market Engagement Index Tract','ECONOMY_Labor Market Engagement Index Base'),
    ('Small Biz Loans',         'ECONOMY_Small Business Loans Score',        'ECONOMY_Small Business Loans Tract, %','ECONOMY_Small Business Loans Base, %'),
    ('Early Education',         'COMMUNITY_Early Education Enrollment Score','COMMUNITY_Early Education Enrollment Tract, %','COMMUNITY_Early Education Enrollment Base, %'),
    ('Health Insurance',        'COMMUNITY_Health Insurance Coverage Score', 'COMMUNITY_Health Insurance Coverage Tract, %','COMMUNITY_Health Insurance Coverage Base, %'),
    ('Female Above Poverty',    'COMMUNITY_Female Above Poverty Score',      'COMMUNITY_Female Above Poverty Tract, %','COMMUNITY_Female Above Poverty Base, %'),
]
print(f"\n{'Indicator':<25} {'Score':>6} {'Tract %':>9} {'Base %':>9} {'Richland Score':>15}")
print("-"*70)
for label, sc_col, tr_col, ba_col in critical:
    sc  = fr_2025.get(sc_col, 'N/A')
    tr  = fr_2025.get(tr_col, 'N/A')
    ba  = fr_2025.get(ba_col, 'N/A')
    ri_sc = ri_2025.get(sc_col, 'N/A')
    print(f"{label:<25} {str(sc):>6} {str(tr):>9} {str(ba):>9} {str(ri_sc):>15}")

print("\nAll charts saved to ./charts/")
