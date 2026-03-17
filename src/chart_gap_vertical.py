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
CAT_LABEL_COLORS = {
    'Place':     '#7B5EA7',
    'Economy':   '#2471A3',
    'Community': '#B7770D',
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

# sort ascending: biggest deficits on LEFT, wins on RIGHT
rows.sort(key=lambda r: r['gap'])

labels = [r['label'] for r in rows]
gaps   = [r['gap']   for r in rows]
cats   = [r['cat']   for r in rows]
colors = [GREEN if g >= 0 else ARC_COLOR for g in gaps]

n = len(rows)
x_pos = np.arange(n)

fig, ax = plt.subplots(figsize=(16, 7), dpi=160)
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

# --- category zebra bands (vertical spans) ------------------------------
cat_ranges = {}
for i, cat in enumerate(cats):
    if cat not in cat_ranges:
        cat_ranges[cat] = [i, i]
    else:
        cat_ranges[cat][0] = min(cat_ranges[cat][0], i)
        cat_ranges[cat][1] = max(cat_ranges[cat][1], i)

for cat, (lo, hi) in cat_ranges.items():
    ax.axvspan(lo - 0.5, hi + 0.5, color=CAT_COLORS[cat], zorder=0, alpha=1.0)

# --- horizontal center line at y=0 -------------------------------------
ax.axhline(0, color=DARK, linewidth=1.4, zorder=2)

# --- bars ---------------------------------------------------------------
bars = ax.bar(x_pos, gaps, color=colors, width=0.6, zorder=3,
              edgecolor='white', linewidth=0.4)

# --- bar value labels above/below bar ends ------------------------------
y_min = min(gaps)
y_max = max(gaps)
y_span = y_max - y_min

for i, (bar, gap) in enumerate(zip(bars, gaps)):
    sign = '+' if gap >= 0 else '\u2212'
    txt  = f"{sign}{abs(int(round(gap)))}"
    offset = y_span * 0.03
    if gap >= 0:
        ax.text(i, gap + offset, txt, va='bottom', ha='center',
                fontsize=7.5, fontweight='bold', color=GREEN)
    else:
        ax.text(i, gap - offset, txt, va='top', ha='center',
                fontsize=7.5, fontweight='bold', color=ARC_COLOR)

# --- x-axis labels (indicator names) -----------------------------------
ax.set_xticks(x_pos)
ax.set_xticklabels(labels, fontsize=8, color=DARK, ha='center')

# --- category labels at TOP inside colored boxes -----------------------
y_top = ax.get_ylim()[1]  # will be set after tight_layout; use data coords

# We'll place category labels in the top of the chart after axis limits settle
# Use a generous y value relative to max gap
label_y = y_max + y_span * 0.18

for cat, (lo, hi) in cat_ranges.items():
    mid = (lo + hi) / 2
    bg  = CAT_COLORS[cat]
    fc  = CAT_LABEL_COLORS[cat]
    ax.text(mid, label_y, cat,
            va='center', ha='center', fontsize=9, fontweight='bold',
            color=fc,
            bbox=dict(boxstyle='round,pad=0.35', facecolor=bg,
                      edgecolor=fc, linewidth=1.2))

# --- axes styling -------------------------------------------------------
ax.set_ylabel("Score Gap (Winnsboro \u2212 Archibald)", fontsize=10,
              color=DARK, labelpad=8)
ax.tick_params(axis='y', colors=GRAY, labelsize=8.5)
ax.tick_params(axis='x', length=0)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_color(GRAY)

# adjust y limits to give headroom for category labels
ax.set_ylim(y_min * 1.22, y_max + y_span * 0.30)

# --- legend -------------------------------------------------------------
legend_elements = [
    mpatches.Patch(facecolor=GREEN,     label='Winnsboro leads'),
    mpatches.Patch(facecolor=ARC_COLOR, label='Winnsboro deficit'),
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=8.5,
          framealpha=0.85, edgecolor=GRAY)

# --- title & subtitle ---------------------------------------------------
fig.suptitle("Winnsboro vs Archibald \u2014 Who\u2019s Winning per Indicator (2025)",
             fontsize=14, fontweight='bold', color=DARK, y=1.01)
ax.set_title("Bars above zero = Winnsboro leads \u00b7 Bars below = Winnsboro deficit",
             fontsize=8.5, color=GRAY, pad=10)

plt.tight_layout()

out_path = os.path.join(ROOT, 'charts', '06b_gap_vertical.png')
os.makedirs(os.path.dirname(out_path), exist_ok=True)
plt.savefig(out_path, dpi=160, bbox_inches='tight')
plt.close()
print(f"Saved: {out_path}")
