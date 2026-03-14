"""
extract_national.py — One-time extraction of score columns from the raw national Excel export.

Run once to produce data/national_igs_full.csv, then use data_loader.py for all modelling.

Usage:
    python src/extract_national.py  [--xlsx PATH]

Default xlsx path: Downloads/Inclusive_Growth_Score_Data_Export_13-03-2026_184206.xlsx
"""

import os
import sys
import argparse
import pandas as pd

ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT    = os.path.join(ROOT, 'data', 'national_igs_full.csv')

DEFAULT_XLSX = os.path.join(
    os.path.expanduser('~'), 'Downloads',
    'Inclusive_Growth_Score_Data_Export_13-03-2026_184206.xlsx'
)

SCORE_KEEP = [
    'META_Is an Opportunity Zone',
    'META_Census Tract FIPS code',
    'META_County',
    'META_State',
    'META_Year',
    'SUMMARY_Inclusive Growth Score',
    'SUMMARY_Growth',
    'SUMMARY_Inclusion',
    'PLACE_Net Occupancy Score',
    'PLACE_Residential Real Estate Value Score',
    'PLACE_Acres of Park Land Score',
    'PLACE_Affordable Housing Score',
    'PLACE_Internet Access Score',
    'PLACE_Travel Time to Work Score',
    'ECONOMY_New Businesses Score',
    'ECONOMY_Spend Growth Score',
    'ECONOMY_Small Business Loans Score',
    'ECONOMY_Minority/Women Owned Businesses Score',
    'ECONOMY_Labor Market Engagement Index Score',
    'ECONOMY_Commercial Diversity Score',
    'COMMUNITY_Personal Income Score',
    'COMMUNITY_Spending per Capita Score',
    'COMMUNITY_Female Above Poverty Score',
    'COMMUNITY_Gini Coefficient Score',
    'COMMUNITY_Early Education Enrollment Score',
    'COMMUNITY_Health Insurance Coverage Score',
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--xlsx', default=DEFAULT_XLSX)
    args = parser.parse_args()

    if not os.path.exists(args.xlsx):
        print(f"ERROR: Excel file not found at {args.xlsx}")
        print("Provide path with: python src/extract_national.py --xlsx <path>")
        sys.exit(1)

    print(f"Reading: {args.xlsx}")
    print("(This will take ~5 minutes for the full national file)")
    df = pd.read_excel(args.xlsx, sheet_name='Compared to Urban-Rural', header=[0, 1])
    df.columns = ['_'.join([str(c) for c in col]).strip() for col in df.columns]
    rows = df.iloc[1:].dropna(subset=['META_Census Tract FIPS code']).copy()
    rows['META_Year'] = pd.to_numeric(rows['META_Year'], errors='coerce')
    rows['SUMMARY_Inclusive Growth Score'] = pd.to_numeric(
        rows['SUMMARY_Inclusive Growth Score'], errors='coerce'
    )
    rows = rows.dropna(subset=['SUMMARY_Inclusive Growth Score', 'META_Year'])

    keep = [c for c in SCORE_KEEP if c in rows.columns]
    out_df = rows[keep]
    out_df.to_csv(OUT, index=False)
    print(f"Saved {len(out_df):,} rows × {len(keep)} columns to {OUT}")


if __name__ == '__main__':
    main()
