"""
Winnsboro 2025 Indicator Scores — Severity-coded horizontal bar chart.
Bars colored by severity tier: CRITICAL (<20), HIGH (20–45), STRENGTH (>55).
Output: charts/18_severity_indicators.png
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# ── Colors ──────────────────────────────────────────────────────────────────
DARK    = '#1A1A2E'
GRAY    = '#95A5A6'
AMBER   = '#E67E22'
CRIMSON = '#C0392B'   # CRITICAL
ORANGE  = '#E67E22'   # HIGH
GREEN   = '#27AE60'   # STRENGTH
MID     = '#5D8AA8'   # MODERATE (20–55 that aren't clearly HIGH or STRENGTH)

# ── Data: (label, score, pillar) ────────────────────────────────────────────
# Only indicators that are clearly notable (omit near-middle ones for clarity)
indicators = [
    # CRITICAL (<20)
    ('Internet Access',    2,  'Place'),
    ('Early Education',    19, 'Community'),
    ('Travel Time',         9, 'Place'),
    ('Labor Engagement',   14, 'Economy'),
    ('Min/Women Biz',      15, 'Economy'),
    # HIGH (20–45, struggling)
    ('Net Occupancy',      38, 'Place'),
    ('Personal Income',    36, 'Community'),
    ('Comm Diversity',     36, 'Economy'),
    ('Gini Coefficient',   42, 'Community'),
    ('Small Biz Loans',    44, 'Economy'),
    # MODERATE (45–55)
    ('Real Estate',        46, 'Place'),
    ('Affordable Housing', 56, 'Place'),
    # STRENGTH (>55)
    ('Health Insurance',   59, 'Community'),
    ('New Businesses',     73, 'Economy'),
    ('Female > Poverty',   69, 'Community'),
    ('Park Land',          19, 'Place'),   # low — actually CRITICAL
]

# Recategorise Park Land correctly (it's 19 = CRITICAL)
# Already at 19 — move it to top of CRITICAL group
indicators = [
    ('Internet Access',    2,  'Place'),
    ('Park Land',          19, 'Place'),
    ('Travel Time',         9, 'Place'),
    ('Early Education',    19, 'Community'),
    ('Labor Engagement',   14, 'Economy'),
    ('Min/Women Biz',      15, 'Economy'),
    ('Net Occupancy',      38, 'Place'),
    ('Personal Income',    36, 'Community'),
    ('Comm Diversity',     36, 'Economy'),
    ('Gini Coefficient',   42, 'Community'),
    ('Small Biz Loans',    44, 'Economy'),
    ('Real Estate',        46, 'Place'),
    ('Affordable Housing', 56, 'Place'),
    ('Health Insurance',   59, 'Community'),
    ('Female > Poverty',   69, 'Community'),
    ('New Businesses',     73, 'Economy'),
]

def tier(score):
    if score < 20:   return 'CRITICAL', CRIMSON
    if score <= 45:  return 'HIGH',     ORANGE
    if score <= 55:  return 'MODERATE', MID
    return 'STRENGTH', GREEN

# Sort: CRITICAL first (ascending score), then HIGH (ascending), then MODERATE, then STRENGTH
tier_order = {'CRITICAL': 0, 'HIGH': 1, 'MODERATE': 2, 'STRENGTH': 3}
indicators.sort(key=lambda x: (tier_order[tier(x[1])[0]], x[1]))

labels  = [r[0] for r in indicators]
scores  = [r[1] for r in indicators]
pillars = [r[2] for r in indicators]
colors  = [tier(s)[1] for s in scores]
tiers   = [tier(s)[0] for s in scores]

n     = len(labels)
y_pos = np.arange(n)

fig, ax = plt.subplots(figsize=(11, 8))
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

# ── Tier section background bands ───────────────────────────────────────────
tier_bg = {
    'CRITICAL': '#FFF0F0',
    'HIGH':     '#FFF8F0',
    'MODERATE': '#F8FAFF',
    'STRENGTH': '#F0FFF4',
}
current = None
band_start = 0
for i, t in enumerate(tiers):
    if t != current:
        if current is not None:
            ax.axhspan(band_start - 0.5, i - 0.5, color=tier_bg[current], alpha=0.45, zorder=0)
        current = t
        band_start = i
ax.axhspan(band_start - 0.5, n - 0.5, color=tier_bg[current], alpha=0.45, zorder=0)

# ── Bars ─────────────────────────────────────────────────────────────────────
bars = ax.barh(y_pos, scores, color=colors, height=0.62,
               edgecolor='white', linewidth=0.5, alpha=0.92, zorder=3)

# ── Score labels ─────────────────────────────────────────────────────────────
for i, (bar, score, col) in enumerate(zip(bars, scores, colors)):
    x_end = bar.get_width()
    # label inside bar if wide enough, else outside
    if score > 15:
        ax.text(x_end - 2, i, str(int(score)), va='center', ha='right',
                fontsize=9.5, fontweight='bold', color='white', zorder=4)
    else:
        ax.text(x_end + 1.5, i, str(int(score)), va='center', ha='left',
                fontsize=9.5, fontweight='bold', color=col, zorder=4)

# ── Pillar labels on right side ──────────────────────────────────────────────
pillar_ranges = {}
for i, p in enumerate(pillars):
    if p not in pillar_ranges:
        pillar_ranges[p] = [i, i]
    else:
        pillar_ranges[p][1] = i

pillar_colors_map = {'Place': '#8E44AD', 'Economy': '#16A085', 'Community': '#D35400'}
for p, (lo, hi) in pillar_ranges.items():
    mid = (lo + hi) / 2
    ax.text(82, mid, p, va='center', ha='left', fontsize=8,
            color=pillar_colors_map[p], fontstyle='italic', fontweight='bold')

# ── Tier section labels on left ──────────────────────────────────────────────
tier_positions = {}
for i, t in enumerate(tiers):
    if t not in tier_positions:
        tier_positions[t] = [i, i]
    else:
        tier_positions[t][1] = i

tier_label_color = {'CRITICAL': CRIMSON, 'HIGH': ORANGE, 'MODERATE': MID, 'STRENGTH': GREEN}
for t, (lo, hi) in tier_positions.items():
    mid = (lo + hi) / 2
    ax.text(-2, mid, t, va='center', ha='right', fontsize=7.5,
            fontweight='bold', color=tier_label_color[t], rotation=0)


# ── Axes ─────────────────────────────────────────────────────────────────────
ax.set_yticks(y_pos)
ax.set_yticklabels(labels, fontsize=9.5, color=DARK)
ax.set_xlabel('IGS Indicator Score (0–100)', fontsize=10, color=DARK, labelpad=8)
ax.set_xlim(-12, 90)
ax.set_ylim(-0.7, n - 0.3)

for spine in ['top', 'right', 'left']:
    ax.spines[spine].set_visible(False)
ax.spines['bottom'].set_color('#CCCCCC')
ax.tick_params(axis='y', length=0)
ax.tick_params(axis='x', colors=GRAY, labelsize=8.5)
ax.grid(axis='x', linestyle=':', alpha=0.3, zorder=0)

# ── Legend ────────────────────────────────────────────────────────────────────
legend_handles = [
    mpatches.Patch(facecolor=CRIMSON, alpha=0.9, label='CRITICAL  (score < 20)'),
    mpatches.Patch(facecolor=ORANGE,  alpha=0.9, label='HIGH  (score 20–45)'),
    mpatches.Patch(facecolor=MID,     alpha=0.9, label='MODERATE  (score 46–55)'),
    mpatches.Patch(facecolor=GREEN,   alpha=0.9, label='STRENGTH  (score > 55)'),
]
legend = ax.legend(
    handles=legend_handles,
    loc='lower right',
    fontsize=8.5,
    framealpha=0.92,
    edgecolor='#CCCCCC',
    title='Severity Tier',
    title_fontsize=8.5,
)
legend.get_title().set_color(DARK)

# ── Title ─────────────────────────────────────────────────────────────────────
fig.suptitle('Winnsboro (Franklin Parish) — 2025 Indicator Scores',
             fontsize=13, fontweight='bold', color=DARK, y=0.99)
ax.set_title('Severity-coded by IGS threshold  ·  Winnsboro overall IGS = 38 / 100',
             fontsize=9, color=GRAY, pad=8)

plt.tight_layout(rect=[0, 0, 1, 0.97])
out = os.path.join('charts', '18_severity_indicators.png')
os.makedirs(os.path.dirname(out), exist_ok=True)
plt.savefig(out, dpi=160, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Saved: {out}")
