"""
models.py — Train Ridge, Random Forest, and Gradient Boosting models.

Dataset: 757,582 observations (national IGS, 2017–2025).
With n>>10,000 all three models are statistically valid.
CV is computed on a 50,000-row stratified sample to keep runtime reasonable.
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import cross_val_score

CV_SAMPLE = 50_000   # rows used for cross-validation (speed)
RANDOM_STATE = 42


def _cv_sample(X, y, n=CV_SAMPLE):
    """Return a random sample of (X, y) for CV."""
    rng = np.random.default_rng(RANDOM_STATE)
    idx = rng.choice(len(X), min(n, len(X)), replace=False)
    return X[idx], y[idx]


def train_ridge(X_scaled, y, feature_names):
    model = Ridge(alpha=1.0)
    model.fit(X_scaled, y)
    Xs, ys = _cv_sample(X_scaled, y)
    cv_r2  = cross_val_score(model, Xs, ys, cv=5, scoring='r2')
    cv_mae = cross_val_score(model, Xs, ys, cv=5, scoring='neg_mean_absolute_error')

    print("=" * 60)
    print(f"RIDGE REGRESSION  (n={len(y):,})")
    print("=" * 60)
    print(f"  R² (5-fold CV, {len(Xs):,}-sample):  {cv_r2.mean():.3f} ± {cv_r2.std():.3f}")
    print(f"  MAE (5-fold CV):                  {-cv_mae.mean():.2f} ± {cv_mae.std():.2f}")

    coef_df = pd.DataFrame({
        'Feature': feature_names,
        'Coefficient': model.coef_
    }).sort_values('Coefficient', key=abs, ascending=False)
    print("\n  Top Coefficients (standardised):")
    print(coef_df.to_string(index=False))

    return model, cv_r2, cv_mae, coef_df


def train_random_forest(X, y, feature_names):
    model = RandomForestRegressor(
        n_estimators=200, max_depth=10, random_state=RANDOM_STATE, n_jobs=-1
    )
    # Train on full dataset
    model.fit(X, y)
    Xs, ys = _cv_sample(X, y)
    cv_r2  = cross_val_score(model, Xs, ys, cv=5, scoring='r2')
    cv_mae = cross_val_score(model, Xs, ys, cv=5, scoring='neg_mean_absolute_error')

    print("\n" + "=" * 60)
    print(f"RANDOM FOREST  (n={len(y):,})")
    print("=" * 60)
    print(f"  R² (5-fold CV, {len(Xs):,}-sample):  {cv_r2.mean():.3f} ± {cv_r2.std():.3f}")
    print(f"  MAE (5-fold CV):                  {-cv_mae.mean():.2f} ± {cv_mae.std():.2f}")

    imp_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False)

    return model, cv_r2, cv_mae, imp_df


def train_gradient_boosting(X, y, feature_names):
    # Use subsample to keep training fast on large dataset
    model = GradientBoostingRegressor(
        n_estimators=200, max_depth=4, learning_rate=0.1,
        subsample=0.5, random_state=RANDOM_STATE
    )
    model.fit(X, y)
    Xs, ys = _cv_sample(X, y)
    cv_r2  = cross_val_score(model, Xs, ys, cv=5, scoring='r2')
    cv_mae = cross_val_score(model, Xs, ys, cv=5, scoring='neg_mean_absolute_error')

    print("\n" + "=" * 60)
    print(f"GRADIENT BOOSTING  (n={len(y):,})")
    print("=" * 60)
    print(f"  R² (5-fold CV, {len(Xs):,}-sample):  {cv_r2.mean():.3f} ± {cv_r2.std():.3f}")
    print(f"  MAE (5-fold CV):                  {-cv_mae.mean():.2f} ± {cv_mae.std():.2f}")

    imp_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False)

    return model, cv_r2, cv_mae, imp_df


def train_all(X, y, X_scaled, feature_names):
    """Train all 3 models and return them together."""
    ridge, ridge_cv, ridge_mae, coef_df = train_ridge(X_scaled, y, feature_names)
    rf,    rf_cv,    rf_mae,    rf_imp  = train_random_forest(X, y, feature_names)
    gb,    gb_cv,    gb_mae,    gb_imp  = train_gradient_boosting(X, y, feature_names)
    return (
        ridge, ridge_cv, ridge_mae, coef_df,
        rf,    rf_cv,    rf_mae,    rf_imp,
        gb,    gb_cv,    gb_mae,    gb_imp,
    )
