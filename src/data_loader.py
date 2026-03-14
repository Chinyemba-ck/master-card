"""
data_loader.py — Load and clean IGS Excel exports into a model-ready DataFrame.
Returns: X (features), y (IGS target), df_model, feature_names, scaler
"""

import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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

# CSV column name → model feature name (for Franklin baseline lookup)
CSV_TO_FEAT = {
    'Internet_Access':  'Internet Access',
    'Affordable_Housing': 'Affordable Housing',
    'Travel_Time':      'Travel Time to Work',
    'Net_Occupancy':    'Net Occupancy',
    'Park_Land':        'Park Land',
    'Real_Estate':      'Real Estate Value',
    'New_Businesses':   'New Businesses',
    'Small_Biz_Loans':  'Small Biz Loans',
    'Min_Women_Biz':    'Min/Women Biz',
    'Labor_Engagement': 'Labor Mkt Engagement',
    'Comm_Diversity':   'Commercial Diversity',
    'Personal_Income':  'Personal Income',
    'Female_Poverty':   'Female Above Poverty',
    'Gini':             'Gini Coefficient',
    'Early_Education':  'Early Education',
    'Health_Insurance': 'Health Insurance',
}


def load_all():
    """Load all IGS Excel exports, return combined DataFrame."""
    igs_dir = os.path.join(ROOT, 'igs_exports')
    files = sorted([f for f in os.listdir(igs_dir) if f.endswith('.xlsx')])
    all_data = []
    for fname in files:
        df = pd.read_excel(
            os.path.join(igs_dir, fname),
            sheet_name='Compared to Urban-Rural',
            header=[0, 1]
        )
        df.columns = ['_'.join([str(c) for c in col]).strip() for col in df.columns]
        rows = df.iloc[1:].dropna(subset=['META_Census Tract FIPS code'])
        all_data.append(rows)
    return pd.concat(all_data, ignore_index=True)


def build_model_df(combined):
    """Extract features + target, drop nulls, fill with median."""
    cols_needed = list(FEATURES.values()) + [TARGET]
    df = combined[[c for c in cols_needed if c in combined.columns]].copy()
    df.columns = [k for k, v in FEATURES.items() if v in combined.columns] + ['IGS']
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.dropna(subset=['IGS'])
    for col in df.columns:
        if col != 'IGS':
            df[col] = df[col].fillna(df[col].median())
    return df


def load_franklin_2025(df_model, feature_names):
    """Load Franklin Parish 2025 baseline from CSV, aligned to feature_names."""
    csv_path = os.path.join(ROOT, 'data', 'franklin_parish_indicators.csv')
    fr_csv = pd.read_csv(csv_path)
    fr_row = fr_csv[fr_csv['Year'] == fr_csv['Year'].max()].iloc[0]
    actual_igs = int(fr_row['IGS'])

    baseline = {feat: float(fr_row[csv_col]) for csv_col, feat in CSV_TO_FEAT.items()}
    baseline['Spending per Capita'] = np.nan  # not in CSV; use median

    for k in baseline:
        if pd.isna(baseline[k]) and k in feature_names:
            baseline[k] = df_model[k].median()

    vec = np.array([baseline.get(f, df_model[f].median()) for f in feature_names]).reshape(1, -1)
    return baseline, vec, actual_igs


def get_data():
    """Full pipeline: returns X, y, df_model, feature_names, X_scaled, scaler, franklin_baseline, franklin_vec, actual_igs."""
    combined = load_all()
    df_model = build_model_df(combined)
    feature_names = [c for c in df_model.columns if c != 'IGS']
    X = df_model[feature_names].values
    y = df_model['IGS'].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    franklin_baseline, franklin_vec, actual_igs = load_franklin_2025(df_model, feature_names)

    print(f"Dataset: {len(df_model)} observations, {len(feature_names)} features")
    print(f"IGS range: {y.min():.0f}–{y.max():.0f}, mean: {y.mean():.1f}\n")

    return X, y, df_model, feature_names, X_scaled, scaler, franklin_baseline, franklin_vec, actual_igs
