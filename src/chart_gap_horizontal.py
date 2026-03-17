import pandas as pd, numpy as np, matplotlib.pyplot as plt, matplotlib.patches as mpatches, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
df = pd.read_csv('data/all_tracts_igs_scores.csv')
win = df[df['FIPS'] == 22041950100].sort_values('Year')
arc = df[df['FIPS'] == 22083970600].sort_values('Year')
win25 = win[win['Year'] == win['Year'].max()].iloc[0]
arc25 = arc[arc['Year'] == arc['Year'].max()].iloc[0]

# --- palette -----------------------------------------------------------
WIN_COLOR = '#C0392B'
ARC_COLOR = '#2980B9'
AMBER     = '#E67E22'
DARK      = '#1A1A2E'
GRAY      = '#7F8C8D'
GREEN     = '#27AE60'

CAT_COLORS = {
    'Place':     '#F8F0FF',
    'Economy':   '#F0F8FF',
    'Community': '#FFF8F0',
}

indicators = [
    ('Internet_Access',   'Internet\nAccess',    'Place'),
    ('Travel_Time',       'Travel\nTime',         'Place'),
    ('Net_Occupancy',     'Net\nOccupancy',       'Place'),
    ('Real_Estate',       'Real\nEstate',         'Place'),
    ('Affordable_Housing','Affordable\nHousing',  'Place'),
    ('Park_Land',         'Park\nLand',           'Place'),
    ('New_Businesses',    'New\nBusinesses',      'Economy'),
    ('Small_Biz_Loans',   'Small Biz\nLoans',     'Economy'),
    ('Min_Women_Biz',     'Min/Women\nBiz',       'Economy'),
    ('Labor_Engagement',  'Labor\nEngagement',    'Economy'),
    ('Comm_Diversity',    'Comm\nDiversity',      'Economy'),
    ('Personal_Income',   'Personal\nIncome',     'Community'),
    ('Female_Poverty',    'Female >\nPoverty',    'Community'),
    ('Gini',              'Gini\nCoefficient',    'Community'),
    ('Early_Education',   'Early\nEducation',     'Community'),
    ('Health_Insurance',  'Health\nInsurance',    'Community'),
]

valid = [(k, l, c) for k, l, c in indicators if k in win25.index]

rows = []
for key, label, cat in valid:
    gap = float(win25[key]) - float(arc25[key])
    rows.append({'key': key, 'label': label, 'cat': cat, 'gap': gap})

# sort ascending: biggest Winnsboro deficits at BOTTOM, wins at TOP
rows.sort(key=lambda r: r['gap'])

labels = [r['label'] for r in rows]
gaps   = [r['gap']   for r in rows]
cats   = [r['cat']   for r in rows]
colors = [GREEN if g >= 0 else WIN_COLOR for g in gaps]

n = len(rows)
y_pos = np.arange(n)

fig, ax = plt.subplots(figsize=(11, 9), dpi=160)
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

# --- category zebra bands (horizontal spans across y-axis) -------------
# Each row occupies [i-0.5, i+0.5]; group bands cover their full range
cat_ranges = {}
for i, cat in enumerate(cats):
    if cat not in cat_ranges:
        cat_ranges[cat] = [i, i]
    else:
        cat_ranges[cat][0] = min(cat_ranges[cat][0], i)
        cat_ranges[cat][1] = max(cat_ranges[cat][1], i)

pass  # no category bands — plain white background

# --- center line --------------------------------------------------------
ax.axvline(0, color=DARK, linewidth=1.4, zorder=2)

# --- bars ---------------------------------------------------------------
bars = ax.barh(y_pos, gaps, color=colors, height=0.6, zorder=3,
               edgecolor='white', linewidth=0.4)

# --- bar labels ---------------------------------------------------------
for i, (bar, gap) in enumerate(zip(bars, gaps)):
    sign = '+' if gap >= 0 else '\u2212'  # minus sign
    txt  = f"{sign}{abs(int(round(gap)))}"
    x_offset = 1.5 if gap >= 0 else -1.5
    ha = 'left' if gap >= 0 else 'right'
    ax.text(gap + x_offset, i, txt, va='center', ha=ha,
            fontsize=8.5, fontweight='bold',
            color=GREEN if gap >= 0 else WIN_COLOR)

# --- y-axis labels ------------------------------------------------------
ax.set_yticks(y_pos)
ax.set_yticklabels(labels, fontsize=9, color=DARK)

# --- category side labels (right margin) --------------------------------
ax.set_xlim(min(gaps) * 1.22, max(gaps) * 1.22 + 20)

# annotate category on the right side
for cat, (lo, hi) in cat_ranges.items():
    mid = (lo + hi) / 2
    ax.text(ax.get_xlim()[1] * 0.98, mid, cat,
            va='center', ha='right', fontsize=8,
            color=GRAY, fontstyle='italic', fontweight='bold')

# --- axes styling -------------------------------------------------------
ax.set_xlabel("Score Gap (Winnsboro \u2212 Archibald)", fontsize=10, color=DARK, labelpad=8)
ax.tick_params(axis='x', colors=GRAY, labelsize=8.5)
ax.tick_params(axis='y', length=0)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_color(GRAY)
ax.xaxis.set_tick_params(color=GRAY)

# --- legend -------------------------------------------------------------
legend_elements = [
    mpatches.Patch(facecolor=GREEN,     label='Winnsboro leads'),
    mpatches.Patch(facecolor=WIN_COLOR, label='Winnsboro deficit'),
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=8.5,
          framealpha=0.85, edgecolor=GRAY)

# --- title & subtitle ---------------------------------------------------
fig.suptitle("Winnsboro vs Archibald \u2014 Gap by Indicator (2025)",
             fontsize=14, fontweight='bold', color=DARK, y=0.98)
ax.set_title("Positive = Winnsboro leads \u00b7 Negative = Winnsboro deficit \u00b7 Same rural NE Louisiana region",
             fontsize=8.5, color=GRAY, pad=8)

plt.tight_layout(rect=[0, 0, 1, 0.96])

out_path = os.path.join(ROOT, 'charts', '06a_gap_horizontal.png')
os.makedirs(os.path.dirname(out_path), exist_ok=True)
plt.savefig(out_path, dpi=160, bbox_inches='tight')
plt.close()
print(f"Saved: {out_path}")
