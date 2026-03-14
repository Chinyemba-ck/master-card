"""
data_loader.py — Load national IGS dataset into a model-ready DataFrame.

Data source: national_igs_full.csv (757,582 rows, 84,676 tracts, 2017–2025)
Generated from: Inclusive_Growth_Score_Data_Export_13-03-2026_184206.xlsx
18 indicator features + target IGS.

Returns: X, y, df_model, feature_names, X_scaled, scaler,
         franklin_baseline, franklin_vec, actual_igs
"""

import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 18 indicators (17 original + Spend Growth, new in 2025 export)
FEATURES = {
    'Internet Access':      'PLACE_Internet Access Score',
    'Affordable Housing':   'PLACE_Affordable Housing Score',
    'Travel Time to Work':  'PLACE_Travel Time to Work Score',
    'Net Occupancy':        'PLACE_Net Occupancy Score',
    'Park Land':            'PLACE_Acres of Park Land Score',
    'Real Estate Value':    'PLACE_Residential Real Estate Value Score',
    'New Businesses':       'ECONOMY_New Businesses Score',
    'Spend Growth':         'ECONOMY_Spend Growth Score',
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

# Franklin Parish 2025 baseline — from franklin_parish_indicators.csv
# Spend Growth not available for Franklin (NaN → filled with national median)
FRANKLIN_2025 = {
    'Internet Access':      2,
    'Affordable Housing':   19,
    'Travel Time to Work':  9,
    'Net Occupancy':        38,
    'Park Land':            19,
    'Real Estate Value':    46,
    'New Businesses':       9,
    'Spend Growth':         np.nan,   # not in Franklin CSV — use national median
    'Small Biz Loans':      44,
    'Min/Women Biz':        15,
    'Labor Mkt Engagement': 14,
    'Commercial Diversity': 36,
    'Personal Income':      36,
    'Spending per Capita':  np.nan,   # not in Franklin CSV — use national median
    'Female Above Poverty': 69,
    'Gini Coefficient':     42,
    'Early Education':      19,
    'Health Insurance':     59,
}
FRANKLIN_ACTUAL_IGS = 38


def load_national():
    """Load national IGS CSV (pre-extracted score columns only)."""
    csv_path = os.path.join(ROOT, 'data', 'national_igs_full.csv')
    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"National CSV not found at {csv_path}.\n"
            "Run: python src/extract_national.py  to generate it from the raw Excel."
        )
    return pd.read_csv(csv_path)


def build_model_df(df):
    """Extract features + target, fill NaN with column median."""
    feat_vals = [v for v in FEATURES.values() if v in df.columns]
    feat_keys = [k for k, v in FEATURES.items() if v in df.columns]
    cols = feat_vals + [TARGET]
    model_df = df[[c for c in cols if c in df.columns]].copy()
    model_df.columns = [k for k, v in FEATURES.items() if v in df.columns] + ['IGS']
    model_df = model_df.apply(pd.to_numeric, errors='coerce')
    model_df = model_df.dropna(subset=['IGS'])
    for col in feat_keys:
        if col in model_df.columns:
            model_df[col] = model_df[col].fillna(model_df[col].median())
    return model_df


def load_franklin_2025(df_model, feature_names):
    """Build Franklin 2025 baseline vector aligned to feature_names."""
    baseline = dict(FRANKLIN_2025)
    for k in baseline:
        if pd.isna(baseline[k]) and k in feature_names:
            baseline[k] = float(df_model[k].median())

    vec = np.array([baseline.get(f, float(df_model[f].median()))
                    for f in feature_names]).reshape(1, -1)
    return baseline, vec, FRANKLIN_ACTUAL_IGS


def get_data():
    """Full pipeline.

    Returns
    -------
    X, y, df_model, feature_names, X_scaled, scaler,
    franklin_baseline, franklin_vec, actual_igs
    """
    raw = load_national()
    df_model = build_model_df(raw)
    feature_names = [c for c in df_model.columns if c != 'IGS']
    X = df_model[feature_names].values
    y = df_model['IGS'].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    franklin_baseline, franklin_vec, actual_igs = load_franklin_2025(df_model, feature_names)

    print(f"Dataset: {len(df_model):,} observations, {len(feature_names)} features")
    print(f"IGS range: {y.min():.0f}–{y.max():.0f}, mean: {y.mean():.1f}\n")

    return X, y, df_model, feature_names, X_scaled, scaler, franklin_baseline, franklin_vec, actual_igs
