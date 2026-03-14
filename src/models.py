"""
models.py — Train Ridge, Random Forest, and Gradient Boosting models.
Returns trained models and CV results.
"""

import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import cross_val_score


def train_ridge(X_scaled, y):
    model = Ridge(alpha=1.0)
    model.fit(X_scaled, y)
    cv_r2  = cross_val_score(model, X_scaled, y, cv=5, scoring='r2')
    cv_mae = cross_val_score(model, X_scaled, y, cv=5, scoring='neg_mean_absolute_error')

    print("=" * 55)
    print("RIDGE REGRESSION  (only valid model at n=63)")
    print("=" * 55)
    print(f"  R² (5-fold CV):  {cv_r2.mean():.3f} ± {cv_r2.std():.3f}")
    print(f"  MAE (5-fold CV): {-cv_mae.mean():.2f} ± {cv_mae.std():.2f}")

    coef_df = pd.DataFrame({
        'Feature': [c for c in range(X_scaled.shape[1])],
        'Coefficient': model.coef_
    })
    return model, cv_r2, cv_mae, coef_df


def train_ridge_named(X_scaled, y, feature_names):
    model = Ridge(alpha=1.0)
    model.fit(X_scaled, y)
    cv_r2  = cross_val_score(model, X_scaled, y, cv=5, scoring='r2')
    cv_mae = cross_val_score(model, X_scaled, y, cv=5, scoring='neg_mean_absolute_error')

    print("=" * 55)
    print("RIDGE REGRESSION  (only valid model at n=63)")
    print("=" * 55)
    print(f"  R² (5-fold CV):  {cv_r2.mean():.3f} ± {cv_r2.std():.3f}")
    print(f"  MAE (5-fold CV): {-cv_mae.mean():.2f} ± {cv_mae.std():.2f}")

    coef_df = pd.DataFrame({
        'Feature': feature_names,
        'Coefficient': model.coef_
    }).sort_values('Coefficient', key=abs, ascending=False)

    print("\n  Top Coefficients (standardised):")
    print(coef_df.to_string(index=False))

    return model, cv_r2, cv_mae, coef_df


def train_random_forest(X, y, feature_names):
    model = RandomForestRegressor(n_estimators=300, max_depth=5, random_state=42)
    model.fit(X, y)
    cv_r2  = cross_val_score(model, X, y, cv=5, scoring='r2')
    cv_mae = cross_val_score(model, X, y, cv=5, scoring='neg_mean_absolute_error')

    print("\n" + "=" * 55)
    print("RANDOM FOREST  (directional only — overfits at n=63)")
    print("=" * 55)
    print(f"  R² (5-fold CV):  {cv_r2.mean():.3f} ± {cv_r2.std():.3f}")
    print(f"  MAE (5-fold CV): {-cv_mae.mean():.2f} ± {cv_mae.std():.2f}")

    imp_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False)

    return model, cv_r2, cv_mae, imp_df


def train_gradient_boosting(X, y, feature_names):
    model = GradientBoostingRegressor(
        n_estimators=200, max_depth=3, learning_rate=0.1, random_state=42
    )
    model.fit(X, y)
    cv_r2  = cross_val_score(model, X, y, cv=5, scoring='r2')
    cv_mae = cross_val_score(model, X, y, cv=5, scoring='neg_mean_absolute_error')

    print("\n" + "=" * 55)
    print("GRADIENT BOOSTING  (directional only — overfits at n=63)")
    print("=" * 55)
    print(f"  R² (5-fold CV):  {cv_r2.mean():.3f} ± {cv_r2.std():.3f}")
    print(f"  MAE (5-fold CV): {-cv_mae.mean():.2f} ± {cv_mae.std():.2f}")

    imp_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False)

    return model, cv_r2, cv_mae, imp_df


def train_all(X, y, X_scaled, feature_names):
    """Train all 3 models and return them together."""
    ridge, ridge_cv, ridge_mae, coef_df = train_ridge_named(X_scaled, y, feature_names)
    rf,    rf_cv,    rf_mae,    rf_imp  = train_random_forest(X, y, feature_names)
    gb,    gb_cv,    gb_mae,    gb_imp  = train_gradient_boosting(X, y, feature_names)
    return (
        ridge, ridge_cv, ridge_mae, coef_df,
        rf,    rf_cv,    rf_mae,    rf_imp,
        gb,    gb_cv,    gb_mae,    gb_imp,
    )
