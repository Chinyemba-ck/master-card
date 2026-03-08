"""
Comparative Analysis — Franklin Parish vs Richland Parish
Why did Richland's IGS rise from 48 (2017) to 59 (2025)?
What can Franklin learn?
Source data: data/all_tracts_igs_scores.csv
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

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

FR_COLOR  = '#C0392B'   # red
RI_COLOR  = '#2980B9'   # blue
AMBER     = '#E67E22'
GREEN     = '#27AE60'
DARK      = '#1A1A2E'
GRAY      = '#7F8C8D'
THRESHOLD = '#E67E22'

df = pd.read_csv('data/all_tracts_igs_scores.csv')
fr = df[df['FIPS'] == 22041950100].sort_values('Year').copy()
ri = df[df['FIPS'] == 22083970600].sort_values('Year').copy()
years = sorted(fr['Year'].unique())

os.makedirs('charts', exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
# CHART 11 — What drove Richland's IGS from 48 to 59?
# Year-on-year change in each indicator for Richland Parish
# ─────────────────────────────────────────────────────────────────────────────
indicators = [
    'Net_Occupancy','Real_Estate','Affordable_Housing','Internet_Access','Travel_Time',
    'New_Businesses','Small_Biz_Loans','Min_Women_Biz','Labor_Engagement','Comm_Diversity',
    'Personal_Income','Female_Poverty','Gini','Early_Education','Health_Insurance'
]

ri_pivot = ri.set_index('Year')[indicators]
ri_delta = ri_pivot.diff()  # year-on-year change

fig, axes = plt.subplots(3, 5, figsize=(20, 12))
fig.suptitle(
    "Richland Parish — Indicator Changes Year-on-Year (2017–2025)\n"
    "Understanding how IGS rose from 48 to 59",
    fontsize=15, fontweight='bold', y=1.01
)

for ax, col in zip(axes.flatten(), indicators):
    vals = ri_delta[col].dropna()
    colors = [GREEN if v >= 0 else FR_COLOR for v in vals]
    ax.bar(vals.index, vals.values, color=colors, alpha=0.85)
    ax.axhline(0, color='black', linewidth=0.8)
    ax.set_title(col.replace('_', ' '), fontweight='bold', fontsize=10)
    ax.set_xlabel('')
    ax.set_xticks(vals.index)
    ax.set_xticklabels([str(y)[2:] for y in vals.index], fontsize=7)
    # Mark 2023 as the big jump year
    ax.axvline(2023, color=AMBER, linestyle='--', linewidth=1.2, alpha=0.7)

# Add IGS trajectory as last panel
ax_igs = axes.flatten()[-1] if len(indicators) < 15 else fig.add_subplot(3, 5, 16) if False else axes[2][4]
ax_igs.clear()
ax_igs.plot(years, ri['IGS'].values, 'o-', color=RI_COLOR, linewidth=2.5, markersize=6, label='Richland IGS')
ax_igs.plot(years, fr['IGS'].values, 's--', color=FR_COLOR, linewidth=2.0, markersize=5, label='Franklin IGS')
ax_igs.axhline(45, color=THRESHOLD, linestyle=':', linewidth=1.5, label='Threshold (45)')
ax_igs.axvline(2023, color=AMBER, linestyle='--', linewidth=1.2, alpha=0.7, label='2023 jump')
ax_igs.set_title('IGS Trajectory', fontweight='bold', fontsize=10)
ax_igs.set_ylim(25, 70)
ax_igs.legend(fontsize=7)
ax_igs.set_xticks(years)
ax_igs.set_xticklabels([str(y)[2:] for y in years], fontsize=7)

green_p = mpatches.Patch(color=GREEN, label='Improved')
red_p   = mpatches.Patch(color=FR_COLOR, label='Declined')
amber_p = mpatches.Patch(color=AMBER, label='2023 — peak jump year')
fig.legend(handles=[green_p, red_p, amber_p], loc='lower center',
           ncol=3, fontsize=10, bbox_to_anchor=(0.5, -0.02))

plt.tight_layout()
plt.savefig('charts/11_richland_igs_drivers.png', bbox_inches='tight')
plt.close()
print('Saved: charts/11_richland_igs_drivers.png')


# ─────────────────────────────────────────────────────────────────────────────
# CHART 12 — Side-by-side: The 5 indicators that diverged most
# (What Richland improved that Franklin did not)
# ─────────────────────────────────────────────────────────────────────────────

# Indicators with biggest Richland improvement AND Franklin stagnation
diverged = {
    'Travel Time\nto Work':    ('Travel_Time',     fr['Travel_Time'].values,     ri['Travel_Time'].values),
    'Early\nEducation':        ('Early_Education', fr['Early_Education'].values, ri['Early_Education'].values),
    'Net\nOccupancy':          ('Net_Occupancy',   fr['Net_Occupancy'].values,   ri['Net_Occupancy'].values),
    'Labor Market\nEngagement':('Labor_Engagement',fr['Labor_Engagement'].values,ri['Labor_Engagement'].values),
    'Personal\nIncome':        ('Personal_Income', fr['Personal_Income'].values, ri['Personal_Income'].values),
}

fig, axes = plt.subplots(1, 5, figsize=(18, 6), sharey=False)
fig.suptitle(
    'The 5 Indicators That Diverged Most — Richland Improved, Franklin Did Not\n'
    'These are the lessons Franklin Parish can directly apply',
    fontsize=13, fontweight='bold'
)

for ax, (label, (col, fr_vals, ri_vals)) in zip(axes, diverged.items()):
    ax.plot(years, ri_vals, 'o-', color=RI_COLOR, linewidth=2.5, markersize=6, label='Richland')
    ax.plot(years, fr_vals, 's--', color=FR_COLOR, linewidth=2.0, markersize=5, label='Franklin')
    ax.axhline(45, color=THRESHOLD, linestyle=':', linewidth=1.2)
    ax.set_title(label, fontweight='bold', fontsize=11)
    ax.set_ylim(0, 100)
    ax.set_xticks(years)
    ax.set_xticklabels([str(y)[2:] for y in years], fontsize=7)
    ax.set_xlabel('Year')

    # Annotate 2017 and 2025 values
    ax.annotate(f'FR {fr_vals[0]:.0f}', (years[0], fr_vals[0]),
                textcoords='offset points', xytext=(-5, -14), fontsize=7, color=FR_COLOR)
    ax.annotate(f'FR {fr_vals[-1]:.0f}', (years[-1], fr_vals[-1]),
                textcoords='offset points', xytext=(2, 4), fontsize=7, color=FR_COLOR)
    ax.annotate(f'RI {ri_vals[0]:.0f}', (years[0], ri_vals[0]),
                textcoords='offset points', xytext=(-5, 4), fontsize=7, color=RI_COLOR)
    ax.annotate(f'RI {ri_vals[-1]:.0f}', (years[-1], ri_vals[-1]),
                textcoords='offset points', xytext=(2, 4), fontsize=7, color=RI_COLOR)

axes[0].legend(fontsize=9)
plt.tight_layout()
plt.savefig('charts/12_divergence_analysis.png', bbox_inches='tight')
plt.close()
print('Saved: charts/12_divergence_analysis.png')


# ─────────────────────────────────────────────────────────────────────────────
# CHART 13 — Comparative demographic & economic snapshot
# Franklin vs Richland: population, income, poverty, key IGS indicators
# ─────────────────────────────────────────────────────────────────────────────

# Census / ACS demographic data (US Census Bureau QuickFacts 2023)
demographics = {
    'Metric': [
        'Population (2023)',
        'Median HH Income',
        'Poverty Rate (%)',
        'Black/African Am. (%)',
        'Median Age',
        'High School+ (%)',
        'Bachelor\'s+ (%)',
        'Owner-occupied housing (%)',
    ],
    'Franklin Parish': [19600, 44103, 19.0, 28.7, 40.2, 80.1, 10.2, 66.4],
    'Richland Parish': [20200, 37800, 24.1, 54.8, 38.1, 78.9, 13.1, 63.0],
    'US Average':      [None,  74755, 11.5, 13.6, 38.9, 89.4, 35.7, 64.8],
}
demo_df = pd.DataFrame(demographics)

# IGS 2025 snapshot comparison
igs_comparison = {
    'Indicator': [
        'Overall IGS', 'Place Score', 'Economy Score', 'Community Score',
        'Internet Access', 'Travel Time', 'Net Occupancy',
        'New Businesses', 'Labor Engagement', 'Commercial Diversity',
        'Early Education', 'Health Insurance', 'Female Above Poverty'
    ],
    'Franklin': [38, 32, 40, 42, 2, 9, 38, 73, 14, 36, 19, 59, 69],
    'Richland': [59, 62, 40, 59, 3, 70, 85, 68, 58, 21, 69, 51, 65],
}
igs_df = pd.DataFrame(igs_comparison)
igs_df['Gap'] = igs_df['Richland'] - igs_df['Franklin']
igs_df['Franklin_Leads'] = igs_df['Franklin'] > igs_df['Richland']

fig, axes = plt.subplots(1, 2, figsize=(16, 8))
fig.suptitle(
    'Franklin Parish vs Richland Parish — Full Comparative Snapshot (2025)\n'
    'Demographics (Census ACS 2023) + IGS Indicator Scores',
    fontsize=13, fontweight='bold'
)

# Left panel: IGS indicators
ax = axes[0]
y_pos = np.arange(len(igs_df))
bar_w = 0.35
bars_fr = ax.barh(y_pos - bar_w/2, igs_df['Franklin'], bar_w,
                  color=FR_COLOR, alpha=0.85, label='Franklin Parish')
bars_ri = ax.barh(y_pos + bar_w/2, igs_df['Richland'], bar_w,
                  color=RI_COLOR, alpha=0.85, label='Richland Parish')

ax.set_yticks(y_pos)
ax.set_yticklabels(igs_df['Indicator'], fontsize=9)
ax.set_xlabel('Score (0–100)')
ax.set_title('IGS Indicator Scores (2025)', fontweight='bold')
ax.axvline(45, color=AMBER, linestyle='--', linewidth=1.3, label='Threshold (45)')
ax.legend(fontsize=9)
ax.set_xlim(0, 110)

# Add gap annotations
for i, row in igs_df.iterrows():
    gap = row['Gap']
    color = RI_COLOR if gap > 0 else FR_COLOR
    label = f'+{gap}' if gap > 0 else str(gap)
    ax.text(max(row['Franklin'], row['Richland']) + 1.5, i,
            label, va='center', fontsize=7.5, color=color, fontweight='bold')

# Right panel: demographics table as a visual
ax2 = axes[1]
ax2.axis('off')

# Build table data
table_data = [['Metric', 'Franklin', 'Richland', 'US Avg']]
for _, row in demo_df.iterrows():
    fr_v = row['Franklin Parish']
    ri_v = row['Richland Parish']
    us_v = row['US Average']
    # Format
    if row['Metric'] == 'Population (2023)':
        row_data = [row['Metric'], f"{int(fr_v):,}", f"{int(ri_v):,}", 'n/a']
    elif row['Metric'] == 'Median HH Income':
        row_data = [row['Metric'], f"${int(fr_v):,}", f"${int(ri_v):,}", f"${int(us_v):,}"]
    elif us_v is None:
        row_data = [row['Metric'], str(fr_v), str(ri_v), 'n/a']
    else:
        row_data = [row['Metric'], f"{fr_v}%", f"{ri_v}%", f"{us_v}%"]
    table_data.append(row_data)

# Key finding notes
notes = [
    '',
    'Franklin HIGHER income',
    'Franklin LOWER poverty',
    'Richland more diverse',
    'Similar ages',
    'Similar education',
    'Richland more degree',
    'Franklin more owners',
]

table = ax2.table(
    cellText=table_data[1:],
    colLabels=table_data[0],
    cellLoc='center',
    loc='center',
    bbox=[0, 0.15, 1, 0.82]
)
table.auto_set_font_size(False)
table.set_fontsize(9.5)

# Color header row
for j in range(4):
    table[0, j].set_facecolor(DARK)
    table[0, j].set_text_props(color='white', fontweight='bold')

# Highlight Franklin-favorable rows
for i, note in enumerate(notes[1:], start=1):
    if 'Franklin HIGHER' in note or 'Franklin LOWER' in note:
        for j in range(4):
            table[i, j].set_facecolor('#FFF0F0')
    elif 'Richland' in note:
        for j in range(4):
            table[i, j].set_facecolor('#F0F0FF')

ax2.text(0.5, 0.07,
    'KEY INSIGHT: Franklin has HIGHER income and LOWER poverty than Richland.\n'
    'Yet Richland scores 21 pts higher on IGS. The gap is economic infrastructure —\n'
    'not demographics. Richland built it. Franklin can too.',
    transform=ax2.transAxes, ha='center', va='center',
    fontsize=9.5, style='italic', color=DARK,
    bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFFBEA', edgecolor=AMBER, linewidth=1.5)
)
ax2.set_title('Census ACS 2023 — Demographic Comparison', fontweight='bold')

plt.tight_layout()
plt.savefig('charts/13_comparative_snapshot.png', bbox_inches='tight')
plt.close()
print('Saved: charts/13_comparative_snapshot.png')

print('\nAll comparative analysis charts saved to charts/')
print('\n=== RICHLAND KEY INSIGHT: What changed 2017-2023 ===')
print('Richland IGS: 48 (2017) -> 42 (2018) -> 46 (2021) -> 50 (2022) -> 59 (2023)')
print()

# Print the biggest Richland changes 2022->2023 (the year of the big jump)
ri_set = ri.set_index('Year')
cols_to_check = ['IGS','Travel_Time','New_Businesses','Personal_Income',
                 'Female_Poverty','Early_Education','Net_Occupancy','Labor_Engagement']
print('Richland 2022 -> 2023 changes (the +9 IGS jump year):')
print(f"{'Indicator':<25} {'2022':>7} {'2023':>7} {'Change':>8}")
print('-' * 50)
for col in cols_to_check:
    v22 = ri_set.loc[2022, col]
    v23 = ri_set.loc[2023, col]
    chg = v23 - v22
    print(f"{col:<25} {v22:>7.0f} {v23:>7.0f} {chg:>+8.0f}")
