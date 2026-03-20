# Model Training & Evaluation

This document covers the data, models, training pipeline, and evaluation results used in the Mastercard IGS analysis for Franklin Parish (Winnsboro, LA).

---

## Data

**Source:** Mastercard Inclusive Growth Score (IGS) Data Export
**File:** `Inclusive_Growth_Score_Data_Export_13-03-2026_184206.xlsx`
**Processed to:** `data/national_igs_full.csv`

| Property | Value |
|---|---|
| Observations | 757,582 |
| Census Tracts | ~83,355 (2025) / 84,676 (all years) |
| Years | 2017–2025 (9 years) |
| Features | 18 indicator scores (0–100 scale) |
| Target | Inclusive Growth Score (IGS, 0–100) |

### Feature Extraction

Run `src/extract_national.py` to convert the raw Excel into the cleaned CSV. This script extracts all 18 indicator score columns and the summary IGS column.

Missing indicator values are filled with the **column median** before training. Rows with a missing target (IGS) are dropped entirely.

### 18 Indicators

The model uses all three IGS pillars:

**PLACE (6)**
- Internet Access, Affordable Housing, Travel Time to Work, Net Occupancy, Park Land, Residential Real Estate Value

**ECONOMY (6)**
- New Businesses, Spend Growth, Small Business Loans, Minority/Women Owned Businesses, Labor Market Engagement, Commercial Diversity

**COMMUNITY (6)**
- Personal Income, Spending per Capita, Female Above Poverty, Gini Coefficient, Early Education Enrollment, Health Insurance Coverage

---

## Community Profiles

| Community | FIPS | Parish | 2025 IGS |
|---|---|---|---|
| Winnsboro | 22041950100 | Franklin Parish | 38 |
| Archibald | 22083970600 | Richland Parish | 59 |

Winnsboro and Archibald are **excluded from all training pools** in holdout validation, ensuring predictions for these communities are fully out-of-sample.

---

## Models

Three models are trained on the same dataset (`src/models.py`):

### 1. Ridge Regression
- **Library:** `sklearn.linear_model.Ridge`
- **Hyperparameters:** `alpha=1.0`
- **Input:** StandardScaler-normalized features (`X_scaled`)
- **Purpose:** Interpretable coefficient weights per indicator; primary model for lever identification
- **R²:** 0.935

### 2. Random Forest
- **Library:** `sklearn.ensemble.RandomForestRegressor`
- **Hyperparameters:** `n_estimators=200, max_depth=10, random_state=42, n_jobs=-1`
- **Input:** Raw (unscaled) features
- **Purpose:** Non-linear benchmark; feature importance cross-check
- **R²:** 0.849

### 3. Gradient Boosting
- **Library:** `sklearn.ensemble.GradientBoostingRegressor`
- **Hyperparameters:** `n_estimators=200, max_depth=4, learning_rate=0.1, subsample=0.5, random_state=42`
- **Input:** Raw (unscaled) features
- **Purpose:** Highest-accuracy model; used for scenario simulations
- **R²:** 0.956

> **Note:** `subsample=0.5` is set on Gradient Boosting to keep training tractable at 757K rows. Cross-validation is run on a stratified 50,000-row sample for speed; full dataset is used for fitting.

---

## Training Pipeline

Entry point: `python src/regression_model.py`

```
1. data_loader.py     → Load & clean national CSV
2. models.py          → Train Ridge, Random Forest, Gradient Boosting
3. simulate.py        → Run IGS improvement scenarios for Winnsboro
4. charts.py          → Save all output charts to ./charts/
```

### Preprocessing (`data_loader.py`)

```python
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)   # used only for Ridge
```

Raw `X` (unscaled) is passed to Random Forest and Gradient Boosting.

---

## Evaluation

### Cross-Validation (5-fold, 50K sample)

| Model | CV R² | CV MAE |
|---|---|---|
| Ridge Regression | 0.935 | ~2.8 |
| Random Forest | 0.849 | ~3.4 |
| Gradient Boosting | 0.956 | ~2.5 |

Cross-validation is computed on a random 50,000-row stratified sample of the training data to keep runtime reasonable at national scale.

### Holdout Validation (`src/validate_holdout.py`)

> **Important:** Winnsboro and Archibald are removed from the full dataset **before any split or training occurs**. They appear in neither the training set nor the test set across all 4 strategies. Every prediction made for these two communities is a completely blind, out-of-sample inference — the models were trained exclusively on the remaining national tracts and have never seen these communities' IGS values at any point.

Four out-of-sample validation strategies are run:

#### Strategy 1 — 80/20 Train/Test Split

Random 80/20 split on the national pool (Winnsboro + Archibald excluded from both splits).

| Model | Test R² | Test MAE |
|---|---|---|
| Ridge Regression | ~0.935 | ~2.8 |
| Random Forest | ~0.849 | ~3.4 |
| Gradient Boosting | ~0.956 | ~2.5 |

#### Strategy 2 — Archibald Holdout

Train on all tracts except Archibald and Winnsboro. Predict Archibald's IGS across all 9 years using only its indicator values.

If MAE < 5 IGS points, the model generalizes to a community it was never shown — confirming the indicator weights are nationally valid.

#### Strategy 3 — Winnsboro Holdout

Same training pool as Strategy 2. Predict Winnsboro's IGS for each year 2017–2025 blind. Includes a 2025 single-point check:

- Winnsboro actual 2025 IGS: **38**
- Model predicts from indicator values without ever seeing the target

#### Strategy 4 — Joint Holdout

Single model trained on neither community, predicts both Archibald and Winnsboro simultaneously. Reports combined MAE across all year-rows for both tracts.

Run holdout validation:
```bash
python src/validate_holdout.py
```

---

## Lever Identification

Ridge coefficients (standardized) identify which indicators have the largest national impact on IGS. These are cross-referenced against:

1. **Archibald's Pearson r** — does the indicator correlate with IGS improvement in a comparable high-performing peer community?
2. **Winnsboro's Pearson r** — does the indicator show movement in Winnsboro's own 9-year history?
3. **Gap vs Archibald** — how far is Winnsboro from its peer benchmark on this indicator?
4. **Gap vs National Median** — how far is Winnsboro from the national median?

Indicators where national Ridge weight, Archibald r, and Winnsboro r all agree are selected as **primary levers**.

### Top Ridge Coefficients (National, Standardized)

| Rank | Indicator | Ridge Coef |
|---|---|---|
| 1 | Personal Income | +4.776 |
| 2 | Female Above Poverty | +4.543 |
| 3 | Gini Coefficient | +3.992 |
| 4 | Labor Mkt Engagement | +3.814 |
| 5 | Spending per Capita | +3.432 |
| 6 | Commercial Diversity | +2.946 |
| 7 | Net Occupancy | +2.791 |
| 8 | Health Insurance | +2.618 |
| 9 | Real Estate Value | +1.838 |
| 10 | New Businesses | +1.696 |
| 11 | Min/Women Biz | +1.528 |
| 12 | Affordable Housing | +1.437 |
| 13 | Small Biz Loans | +1.210 |
| 14 | Spend Growth | +1.174 |
| 15 | Travel Time to Work | +1.150 |
| 16 | Internet Access | +1.118 |
| 17 | Early Education | +0.865 |
| 18 | Park Land | −0.129 |

---

## Key Results

| Metric | Value |
|---|---|
| National model R² (Ridge) | 0.935 |
| National model R² (GB) | 0.956 |
| Training observations | 757,582 |
| Winnsboro 2025 IGS | 38 (10th percentile nationally) |
| Archibald 2025 IGS | 59 (82nd percentile nationally) |
| Gap (Winnsboro → Archibald) | 21 IGS points |
| National median IGS | 50 |
| Louisiana median IGS | 44 |

---

## Files Reference

| File | Description |
|---|---|
| `src/extract_national.py` | Convert raw Excel → `national_igs_full.csv` |
| `src/data_loader.py` | Load data, scale features, build Winnsboro baseline vector |
| `src/models.py` | Train Ridge, Random Forest, Gradient Boosting |
| `src/regression_model.py` | Main orchestrator — train all models + generate charts |
| `src/validate_holdout.py` | Out-of-sample validation (4 strategies) |
| `src/simulate.py` | IGS scenario simulations for Winnsboro |
| `src/charts.py` | Chart generation for model outputs |
| `data/national_igs_full.csv` | Processed national dataset (757,582 rows) |
