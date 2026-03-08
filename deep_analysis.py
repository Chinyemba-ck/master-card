import pandas as pd
import numpy as np
import os
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
import warnings; warnings.filterwarnings('ignore')

files = sorted([f for f in os.listdir('.') if f.endswith('.xlsx')])
all_data = []
for fname in files:
    df = pd.read_excel(fname, sheet_name='Compared to Urban-Rural', header=[0,1])
    df.columns = ['_'.join([str(c) for c in col]).strip() for col in df.columns]
    data_rows = df.iloc[1:].dropna(subset=['META_Census Tract FIPS code'])
    all_data.append(data_rows)

combined = pd.concat(all_data, ignore_index=True)
combined['FIPS'] = combined['META_Census Tract FIPS code'].astype(int)
combined['Year'] = combined['META_Year'].astype(int)

FEATURES = {
    'Internet Access':      'PLACE_Internet Access Score',
    'Affordable Housing':   'PLACE_Affordable Housing Score',
    'Travel Time to Work':  'PLACE_Travel Time to Work Score',
    'Net Occupancy':        'PLACE_Net Occupancy Score',
    'Park Land':            'PLACE_Acres of Park Land Score',
    'Real Estate Value':    'PLACE_Residential Real Estate Value Score',
    'New Businesses':       'ECONOMY_New Businesses Score',
    'Small Biz Loans':      'ECONOMY_Small Business Loans Score',
    'Min/Women Biz':        'ECONOMY_Minority/Women Owned Businesses Score',
    'Labor Mkt Engagement': 'ECONOMY_Labor Market Engagement Index Score',
    'Commercial Diversity': 'ECONOMY_Commercial Diversity Score',
    'Personal Income':      'COMMUNITY_Personal Income Score',
    'Spending per Capita':  'COMMUNITY_Spending per Capita Score',
    'Female Above Poverty': 'COMMUNITY_Female Above Poverty Score',
    'Gini Coefficient':     'COMMUNITY_Gini Coefficient Score',
    'Early Education':      'COMMUNITY_Early Education Enrollment Score',
    'Health Insurance':     'COMMUNITY_Health Insurance Coverage Score',
}
TARGET = 'SUMMARY_Inclusive Growth Score'

df_model = combined[[c for c in FEATURES.values() if c in combined.columns] + [TARGET]].copy()
df_model.columns = [k for k,v in FEATURES.items() if v in combined.columns] + ['IGS']
df_model = df_model.apply(pd.to_numeric, errors='coerce').dropna(subset=['IGS'])
for col in df_model.columns:
    if col != 'IGS':
        df_model[col] = df_model[col].fillna(df_model[col].median())

feature_names = [c for c in df_model.columns if c != 'IGS']
X = df_model[feature_names].values
y = df_model['IGS'].values
scaler = StandardScaler()
X_s = scaler.fit_transform(X)
ridge = Ridge(alpha=1.0).fit(X_s, y)

def predict(scenario):
    arr = np.array([scenario.get(f, df_model[f].median()) for f in feature_names]).reshape(1,-1)
    return ridge.predict(scaler.transform(arr))[0]

franklin_2025 = {
    'Internet Access': 2, 'Affordable Housing': 56, 'Travel Time to Work': 9,
    'Net Occupancy': 38, 'Park Land': 19, 'Real Estate Value': 46,
    'New Businesses': 73, 'Small Biz Loans': 44, 'Min/Women Biz': 15,
    'Labor Mkt Engagement': 14, 'Commercial Diversity': 36,
    'Personal Income': 36, 'Spending per Capita': float(df_model['Spending per Capita'].median()),
    'Female Above Poverty': 69, 'Gini Coefficient': 42,
    'Early Education': 19, 'Health Insurance': 59,
}

richland_2025 = {
    'Internet Access': 3, 'Affordable Housing': 72, 'Travel Time to Work': 70,
    'Net Occupancy': 85, 'Park Land': 43, 'Real Estate Value': 72,
    'New Businesses': 68, 'Small Biz Loans': 50, 'Min/Women Biz': 82,
    'Labor Mkt Engagement': 58, 'Commercial Diversity': 21,
    'Personal Income': 56, 'Spending per Capita': 0,
    'Female Above Poverty': 65, 'Gini Coefficient': 56,
    'Early Education': 69, 'Health Insurance': 51,
}

avg_60_vals = {
    'Internet Access': 70, 'Affordable Housing': 44, 'Travel Time to Work': 51,
    'Net Occupancy': 78, 'Park Land': 40, 'Real Estate Value': 74,
    'New Businesses': 75, 'Small Biz Loans': 66, 'Min/Women Biz': 75,
    'Labor Mkt Engagement': 61, 'Commercial Diversity': 98, 'Personal Income': 56,
    'Spending per Capita': 65, 'Female Above Poverty': 50, 'Gini Coefficient': 56,
    'Early Education': 26, 'Health Insurance': 52,
}

print(f"Current Franklin IGS (Ridge model): {predict(franklin_2025):.1f}  (actual: 38)")

# SCENARIO 1 — Conservative: just cross 45
s45 = franklin_2025.copy()
s45.update({'Internet Access':35,'Labor Mkt Engagement':30,'Min/Women Biz':40,
            'Early Education':35,'Travel Time to Work':25,'Commercial Diversity':55})
print(f"Scenario 1 — Cross 45 (BridgeWork basic):          {predict(s45):.1f}")

# SCENARIO 2 — Reach 60 (match Richland-level performance)
s60 = franklin_2025.copy()
s60.update({
    'Internet Access': 70,
    'Labor Mkt Engagement': 47,
    'Min/Women Biz': 67,
    'Commercial Diversity': 80,
    'Small Biz Loans': 66,
    'Net Occupancy': 65,
    'Personal Income': 50,
    'Early Education': 35,
    'Real Estate Value': 60,
    'Travel Time to Work': 35,
    'Spending per Capita': 55,
})
print(f"Scenario 2 — Reach 60 (BridgeWork expanded):       {predict(s60):.1f}")

# SCENARIO 3 — Reach 70 (match Fresno 5805 high performer)
s70 = franklin_2025.copy()
s70.update({
    'Internet Access': 85,
    'Labor Mkt Engagement': 60,
    'Min/Women Biz': 75,
    'Commercial Diversity': 95,
    'Small Biz Loans': 66,
    'Net Occupancy': 75,
    'Personal Income': 56,
    'Early Education': 39,
    'Real Estate Value': 70,
    'Travel Time to Work': 50,
    'Spending per Capita': 65,
    'Park Land': 40,
    'Gini Coefficient': 60,
    'New Businesses': 80,
})
print(f"Scenario 3 — Reach 70 (BridgeWork full scale):     {predict(s70):.1f}")

print("\n=== GAP: Franklin vs Average 60+ Tracts ===")
print(f"{'Indicator':<25} {'Franklin':>8} {'Avg60+':>8} {'Gap':>6}  Priority")
print("-"*65)
gaps = []
for feat, avg in avg_60_vals.items():
    fr_val = float(franklin_2025.get(feat) or 0)
    gap = avg - fr_val
    gaps.append((feat, fr_val, avg, gap))
gaps.sort(key=lambda x: -x[3])
for feat, fr, avg, gap in gaps:
    p = "CRITICAL" if gap > 40 else ("HIGH" if gap > 20 else ("MEDIUM" if gap > 10 else "LOW"))
    print(f"{feat:<25} {fr:>8.0f} {avg:>8.0f} {gap:>8.0f}  {p}")

print("\n=== RICHLAND vs FRANKLIN — LESSON LEARNING ===")
print(f"{'Indicator':<25} {'Franklin':>8} {'Richland':>9} {'Gap':>6}")
print("-"*55)
for feat in sorted(richland_2025.keys(), key=lambda f: richland_2025[f]-float(franklin_2025.get(f) or 0), reverse=True):
    fr = float(franklin_2025.get(feat) or 0)
    ri = richland_2025[feat]
    gap = ri - fr
    print(f"{feat:<25} {fr:>8.0f} {ri:>9.0f} {gap:>6.0f}")

print("\n=== INDICATORS WHERE FRANKLIN ALREADY BEATS OR MATCHES RICHLAND ===")
for feat in richland_2025:
    fr = float(franklin_2025.get(feat) or 0)
    ri = richland_2025[feat]
    if fr >= ri:
        print(f"  {feat:<25} Franklin: {fr:.0f}  Richland: {ri:.0f}  (+{fr-ri:.0f})")

print("\n=== SCENARIO INDICATOR TARGETS SUMMARY ===")
print(f"{'Indicator':<25} {'Current':>8} {'Scen1(45+)':>11} {'Scen2(60)':>10} {'Scen3(70)':>10} {'Richland':>9} {'Avg60+':>7}")
print("-"*85)
all_feats = list(FEATURES.keys())
for feat in all_feats:
    cur = float(franklin_2025.get(feat) or 0)
    sc1 = float(s45.get(feat) or cur)
    sc2 = float(s60.get(feat) or cur)
    sc3 = float(s70.get(feat) or cur)
    ri  = float(richland_2025.get(feat) or 0)
    a60 = float(avg_60_vals.get(feat) or 0)
    print(f"{feat:<25} {cur:>8.0f} {sc1:>11.0f} {sc2:>10.0f} {sc3:>10.0f} {ri:>9.0f} {a60:>7.0f}")
