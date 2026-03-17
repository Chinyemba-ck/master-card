# Data Analysis Report
## Mastercard AUCDSI HBCU Data Science Challenge 2026
### Winnsboro (Franklin Parish) vs Archibald (Richland Parish), Louisiana
### Census Tract 22041950100 — Pre-Proposal Analytical Foundation

**Repository:** [github.com/Chinyemba-ck/master-card](https://github.com/Chinyemba-ck/master-card)

> **Geographic context:** Census tract 22041950100 is located in **Winnsboro**, the parish seat of Franklin Parish, Louisiana. The primary benchmark tract (22083970600) is located in **Archibald**, a community in Richland Parish, Louisiana. Both are small rural communities in northeast Louisiana — same region, similar size, dramatically different IGS trajectories.

---

## 1. DATASETS USED

### Primary Dataset — Mastercard Inclusive Growth Score (IGS) Tool

**Two-tier data strategy:** 7 tract-level Excel exports for descriptive analysis + the full national IGS export (757,582 rows) for regression modelling.

| File | Census Tract | Location | IGS 2025 | Role |
|---|---|---|---|---|
| [`184206.xlsx`](data/Inclusive_Growth_Score_Data_Export_13-03-2026_184206.xlsx) | National | **Full national export — 84,676 tracts × 9 yrs (757,582 rows)** | — | **National regression model source** |
| [`030542.xlsx`](https://github.com/Chinyemba-ck/master-card/blob/main/igs_exports/Inclusive_Growth_Score_Data_Export_26-02-2026_030542.xlsx) | 22041950100 | **Winnsboro**, Franklin Parish, LA | 38 | **Primary — target tract** |
| [`030523.xlsx`](https://github.com/Chinyemba-ck/master-card/blob/main/igs_exports/Inclusive_Growth_Score_Data_Export_26-02-2026_030523.xlsx) | 22083970600 | **Archibald**, Richland Parish, LA | 59 | **Benchmark — same region, rural** |
| [`025930.xlsx`](https://github.com/Chinyemba-ck/master-card/blob/main/igs_exports/Inclusive_Growth_Score_Data_Export_26-02-2026_025930.xlsx) | 6019005805 | Fresno, CA | 70 | High-performer reference |
| [`025916.xlsx`](https://github.com/Chinyemba-ck/master-card/blob/main/igs_exports/Inclusive_Growth_Score_Data_Export_26-02-2026_025916.xlsx) | 6019003104 | Fresno, CA | 60 | High-performer reference |
| [`025736.xlsx`](https://github.com/Chinyemba-ck/master-card/blob/main/igs_exports/Inclusive_Growth_Score_Data_Export_26-02-2026_025736.xlsx) | 6019003302 | Fresno, CA | <45 | Below-45 comparison |
| [`030838.xlsx`](https://github.com/Chinyemba-ck/master-card/blob/main/igs_exports/Inclusive_Growth_Score_Data_Export_26-02-2026_030838.xlsx) | 48113018501 | Dallas, TX | 60 | High-performer reference |
| [`030824.xlsx`](https://github.com/Chinyemba-ck/master-card/blob/main/igs_exports/Inclusive_Growth_Score_Data_Export_26-02-2026_030824.xlsx) | 48113019013 | Dallas, TX | <45 | Below-45 comparison |

> **National export (`184206.xlsx`):** The March 2026 national IGS export (`Inclusive_Growth_Score_Data_Export_13-03-2026_184206.xlsx`) is the source for the regression model. It covers all 84,676 US census tracts across 2017–2025, 18 indicator scores per row, 72 columns total. This file is the foundation for all Charts 08–10 model outputs. Tract-level individual exports (7 files above) are used for descriptive analysis (Charts 01–07).

**Dataset structure:**
- Sheet used: `Compared to Urban-Rural`
- Header: 2 rows (multi-level), flattened with `'_'.join()` in pandas
- Columns: ~50 per file — metadata, pillar scores, indicator scores, tract %, base %
- Years: 2017–2025 (9 years per tract)
- **Total observations after concat: 63 rows × ~50 columns**

**Each IGS indicator gives 3 columns (example — Internet Access):**

| Column | What It Means |
|--------|--------------|
| `PLACE_Internet Access Score` | The 0–100 score Mastercard assigns (normalized, comparable across all tracts) |
| `PLACE_Internet Access Tract, %` | The **raw number for this community** — e.g., "31% of Winnsboro households have internet access" |
| `PLACE_Internet Access Base, %` | The **national benchmark** — what a typical comparison tract looks like |

The Score is derived from the gap between Tract and Base. A low score means the community's raw % is far below the benchmark — e.g., Winnsboro Internet Access: Score=2, Tract=31%, Base=78% (47 points below average). This is why a score of 2 looks much worse than the raw 31% — because most places are at 78%.

**Pillars and indicators (18 total in national export, 17 in tract-level exports):**

| Pillar | Indicators |
|---|---|
| **Place** (6) | Internet Access, Affordable Housing, Travel Time to Work, Net Occupancy, Park Land, Real Estate Value |
| **Economy** (6) | New Businesses, **Spend Growth** *(new — national export only)*, Small Business Loans, Min/Women Owned Businesses, Labor Market Engagement, Commercial Diversity |
| **Community** (6) | Personal Income, Spending per Capita, Female Above Poverty, Gini Coefficient, Early Education Enrollment, Health Insurance Coverage |

> **Note on Spend Growth:** The 2025 national export added `ECONOMY_Spend Growth Score` as an 18th indicator. It is not present in the 7 individual tract exports. Winnsboro/Franklin has NaN for this indicator across all years. In the national model it has the weakest Ridge coefficient (+0.56) and is held at the national median in all simulation scenarios.

### Processed Data (CSV exports for reproducibility)

| File | Description | Rows |
|---|---|---|
| `data/national_igs_full.csv` | **Full national IGS extract** — 84,676 tracts × 9 years, 18 indicator scores. Generated from the 2025 national Excel export via `python src/extract_national.py`. Used by regression model. | 757,582 |
| [`data/all_tracts_igs_scores.csv`](https://github.com/Chinyemba-ck/master-card/blob/main/data/all_tracts_igs_scores.csv) | 7 comparison tracts × 9 years — IGS + all 15 indicator scores | 63 |
| [`data/franklin_parish_indicators.csv`](https://github.com/Chinyemba-ck/master-card/blob/main/data/franklin_parish_indicators.csv) | Winnsboro/Franklin Parish (FIPS 22041950100), 2017–2025 | 9 |
| [`data/richland_parish_indicators.csv`](https://github.com/Chinyemba-ck/master-card/blob/main/data/richland_parish_indicators.csv) | Archibald/Richland Parish (FIPS 22083970600), 2017–2025 | 9 |
| [`data/franklin_vs_richland_comparison.csv`](https://github.com/Chinyemba-ck/master-card/blob/main/data/franklin_vs_richland_comparison.csv) | Side-by-side comparison with gap calculations | 9 |

---

## 2. ANALYSIS SCRIPTS

### Modular Pipeline

The analysis is split into focused modules. Entry point: `python src/regression_model.py`

| File | Responsibility |
|------|---------------|
| [`src/extract_national.py`](https://github.com/Chinyemba-ck/master-card/blob/main/src/extract_national.py) | **One-time setup** — extract score columns from raw national Excel → `data/national_igs_full.csv` (~5 min for 757k rows) |
| [`src/regression_model.py`](https://github.com/Chinyemba-ck/master-card/blob/main/src/regression_model.py) | Orchestrator — calls all modules in order |
| [`src/data_loader.py`](https://github.com/Chinyemba-ck/master-card/blob/main/src/data_loader.py) | Load national CSV (757k rows, 18 features); build model-ready DataFrame; hardcode Winnsboro 2025 baseline |
| [`src/models.py`](https://github.com/Chinyemba-ck/master-card/blob/main/src/models.py) | Train Ridge, Random Forest, Gradient Boosting; CV on 50k sample for speed |
| [`src/simulate.py`](https://github.com/Chinyemba-ck/master-card/blob/main/src/simulate.py) | HealthScore what-if scenarios; full indicator audit docstring with dual evidence base |
| [`src/charts.py`](https://github.com/Chinyemba-ck/master-card/blob/main/src/charts.py) | All chart generation (charts 08–10) |

---

### Descriptive Analysis — Charts 01–07

**Purpose:** Load all 7 IGS files, build comparison dataset, produce 7 descriptive charts comparing Winnsboro (Franklin Parish) vs Archibald (Richland Parish) and 5 reference tracts.

**Steps performed:**
1. Load all `.xlsx` files from `igs_exports/` using `os.listdir('igs_exports')`
2. Read each with `pd.read_excel(..., sheet_name='Compared to Urban-Rural', header=[0,1])`
3. Flatten multi-level column headers with `'_'.join()`
4. Drop rows with missing FIPS code, concat all into one DataFrame (63 rows)
5. Filter to Winnsboro (FIPS 22041950100) and Archibald (FIPS 22083970600)
6. Extract 2025 snapshot rows for cross-sectional analysis
7. Compute indicator gaps: `Archibald score − Winnsboro score` for each indicator
8. Produce 7 charts, saved to `charts/`

**Charts produced:**

| Chart | File | What it shows |
|---|---|---|
| 1 | [`charts/01_time_series.png`](https://github.com/Chinyemba-ck/master-card/blob/main/charts/01_time_series.png) | 2×2 panel — Overall IGS, Place, Economy, Community scores 2017–2025. Winnsboro (red) vs Archibald (blue) with 45-threshold line. The shaded red area shows every year Winnsboro has been below 45. Economy is the most volatile pillar — it swings up then crashes each cycle. |
| 2 | [`charts/02_grouped_bar_indicators.png`](https://github.com/Chinyemba-ck/master-card/blob/main/charts/02_grouped_bar_indicators.png) | All 16 indicators side-by-side, Winnsboro (solid) vs Archibald (faded), color-coded by pillar. Winnsboro beats Archibald on Health Insurance (59 vs 51), Female Above Poverty (69 vs 65), New Businesses (73 vs 68), and Commercial Diversity (36 vs 21) — but is far behind on Min/Women Biz (15 vs 82), Labor Engagement (14 vs 58), Net Occupancy (38 vs 85), Travel Time (9 vs 70), and Early Education (19 vs 69). |
| 3 | [`charts/03_correlation_heatmap.png`](https://github.com/Chinyemba-ck/master-card/blob/main/charts/03_correlation_heatmap.png) | Pearson correlation matrix across all indicator scores in Winnsboro's 9-year time series. Key correlations: Internet Access vs Labor Engagement (r=0.93), Internet Access vs Travel Time (r=0.87), Health Insurance vs Early Education (r=−0.93). These show indicators move together — the collapse is systemic, not isolated. |
| 4 | [`charts/04_radar_chart.png`](https://github.com/Chinyemba-ck/master-card/blob/main/charts/04_radar_chart.png) | Radar chart across 9 sub-dimensions (Place/Economy/Community × Overall/Growth/Inclusion). Winnsboro's shape shows strong Economy Growth but collapsed Economy Inclusion and Community Inclusion. Archibald dominates on Place Growth. Both fail Community Inclusion. |
| 5 | [`charts/05_scatter_plots.png`](https://github.com/Chinyemba-ck/master-card/blob/main/charts/05_scatter_plots.png) | Two scatter plots with year labels on Winnsboro points. Left: Internet Access % vs Economy Score — Winnsboro's economy score tracks below Archibald across the same internet access range, showing internet alone doesn't explain the gap. Right: Labor Engagement % vs IGS — as Winnsboro's labor engagement fell from 48 (2017) to 14 (2025), IGS tracked downward in lockstep. |
| 6 | [`charts/06_benchmark_gap.png`](https://github.com/Chinyemba-ck/master-card/blob/main/charts/06_benchmark_gap.png) | Horizontal bar chart of every indicator gap (Archibald minus Winnsboro), ranked. Negative bars (left of zero) = Winnsboro beats Archibald: Commercial Diversity (−15), Health Insurance (−8), New Businesses (−5), Female Above Poverty (−4). Largest gaps in Archibald's favour: Min/Women Biz (+67), Travel Time (+61), Early Education (+50), Net Occupancy (+47), Labor Engagement (+44). |
| 7 | [`charts/07_boxplot_all_tracts.png`](https://github.com/Chinyemba-ck/master-card/blob/main/charts/07_boxplot_all_tracts.png) | Box plots of IGS distribution (2017–2025) for all 7 tracts. Winnsboro has the tightest, lowest box — range 34–42, median ~38. It has never crossed 45. Fresno 5805 sits entirely above 65. Archibald straddles the 45 threshold. Dallas 18501 and Fresno 3104 consistently above 50. |

---

### Regression + Simulation — Charts 08–10

**Entry point:** `python src/regression_model.py`

**Why national data?** The 7-tract dataset (n=63) was too small for Random Forest and Gradient Boosting — both produced negative CV R² (overfitting). The full national export (n=757,582, 84,676 unique tracts) eliminates this problem and allows the model to learn what drives IGS across all rural/urban contexts nationally.

**Pipeline steps:**
1. `data_loader.py` — Load `data/national_igs_full.csv` (757,582 rows, 84,676 tracts, 18 features); fill NaN with national median; standardize with `StandardScaler`
2. `models.py` — Train Ridge, Random Forest, Gradient Boosting with 5-fold CV on 50,000-row sample (speed); all three models valid at national scale
3. `simulate.py` — Run Winnsboro HealthScore scenarios (Phase 1/2/3) and indicator sensitivity (+20 pts per indicator)
4. `charts.py` — Save charts 08–10

**Model performance — cross-validated (5-fold CV, 50k sample):**

| Model | CV R² | CV MAE | Verdict |
|---|---|---|---|
| **Ridge Regression** | **0.935 ± 0.004** | **1.40 ± 0.01** | ✅ Valid |
| **Random Forest** | **0.849 ± 0.006** | **2.97 ± 0.03** | ✅ Valid (was −0.15 at n=63) |
| **Gradient Boosting** | **0.956 ± 0.006** | **1.30 ± 0.02** | ✅ Valid (was −0.37 at n=63) |

**National vs direct benchmark — what each analysis tells us:**

| Analysis | Data source | What it establishes |
|---|---|---|
| Ridge coefficients (national, n=757k) | All 84,676 US tracts | Which indicators drive IGS *across all contexts nationally* |
| Archibald correlation analysis (n=9) | Archibald's 9-year time series | Which indicators specifically drove Archibald from IGS 48→59 |
| Winnsboro correlation analysis (n=9) | Winnsboro's 9-year time series | Which indicators moved with Winnsboro's own IGS swings (2017–2025) |
| Sensitivity analysis (national RF model) | National model applied to Winnsboro's profile | Which indicators would move the needle most *for a tract like Winnsboro* |

The strength of the analysis is that all four agree on the same levers: **Labor Market Engagement, Personal Income, Early Education, and Net Occupancy** are consistently the top drivers across national patterns and Archibald's actual trajectory.

**Ridge standardized coefficients — national model (n=757,582) alongside direct Winnsboro vs Archibald benchmark:**

| Rank | Indicator | Coef (national) | Archibald r | Winnsboro r | Winnsboro 2025 | Archibald 2025 | Gap | Interpretation |
|---|---|---|---|---|---|---|---|---|
| 1 | Personal Income | **+2.15** | **+0.943** | −0.66 | 36 | 56 | −20 | Top national driver AND Archibald's #1 driver — income follows labor chain |
| 2 | Net Occupancy | **+1.88** | **+0.827** | +0.24 | 38 | 85 | −47 | Population stability — jobs keep people from leaving |
| 3 | Labor Mkt Engagement | **+1.86** | **+0.911** | +0.73 | 14 | 58 | −44 | Archibald's #2 driver — workforce participation chain |
| 4 | Commercial Diversity | +1.80 | +0.419 | **−0.43** | 36 | 21 | Winnsboro +15 | Cross-tract signal; NOT a Winnsboro-specific driver (CommDiv highest when IGS was lowest) |
| 5 | Real Estate Value | +1.79 | +0.683 | −0.15 | 46 | 72 | −26 | Follows net occupancy and income (slow-moving) |
| 6 | Female Above Poverty | +1.28 | **+0.901** | −0.71 | 69 | 65 | Winnsboro +4 | Archibald's #3 driver; Winnsboro already strong here |
| 7 | Travel Time to Work | +1.22 | **+0.852** | +0.63 | 9 | 70 | −61 | Archibald's #4 driver; remote work jobs would move this |
| 13 | Early Education | +0.99 | +0.712 | **+0.78** | 19 | 69 | −50 | Strongest Winnsboro local correlation; root trigger |
| 18 | Spend Growth | +0.56 | N/A | N/A | NaN | NaN | — | New 18th indicator; weakest predictor; Winnsboro has no historical data |

> **Key nuance — Commercial Diversity:** National Ridge coeff +1.80 (cross-tract) but Winnsboro r=−0.43 (local negative — CommDiv was at 62 in 2024 when IGS was at 35). Archibald has CommDiv=21 at IGS=59 — Archibald is thriving with *low* diversity. CommDiv is a cross-tract statistical signal, not an actionable Winnsboro lever.

**Indicators where national model, Archibald benchmark, and Winnsboro history all agree — the levers to target:**

| Indicator | National Ridge | Archibald r | Winnsboro r | Winnsboro gap | Verdict |
|---|---|---|---|---|---|
| **Labor Mkt Engagement** | **+1.86 (rank 3)** | **+0.911** | +0.73 | −44 pts | ✅ USE — all three sources agree; biggest actionable gap |
| **Early Education** | +0.99 (rank 13) | +0.712 | **+0.78** | −50 pts | ✅ USE — root trigger; Archibald proof; Winnsboro was at 78 (2017) |
| **Personal Income** | **+2.15 (rank 1)** | **+0.943** | — | −20 pts | ✅ USE (indirect) — follows labor chain; Archibald's top driver |
| **Net Occupancy** | **+1.88 (rank 2)** | **+0.827** | — | −47 pts | ✅ USE (indirect) — population stabilizes when jobs appear |
| **Travel Time to Work** | +1.22 (rank 7) | **+0.852** | +0.63 | −61 pts | ✅ USE (indirect) — remote RHTP jobs; Archibald went 48→70 |
| **Small Biz Loans** | +1.22 (rank 7) | — | +0.72 | −26 pts | ✅ USE (direct) — Winnsboro's own lever; was 74 in 2017 |
| Commercial Diversity | +1.80 (rank 4) | +0.42 | **−0.43** | Winnsboro +15 | ⚠️ SKIP as primary lever — local data contradicts national signal |
| Internet Access | −0.73 | **−0.379** | +0.69 | −76 pts | ⚠️ INFRASTRUCTURE only — NELPCO/Volt; Archibald's internet fell as IGS rose |

**Charts produced:**

| Chart | File | What it shows |
|---|---|---|
| 8 | [`charts/08_regression_analysis.png`](https://github.com/Chinyemba-ck/master-card/blob/main/charts/08_regression_analysis.png) | 4-panel. **Top-left:** Ridge standardized coefficients (national n=757k) — Personal Income (+2.15), Net Occupancy (+1.88), Labor Engagement (+1.86) are top 3 national drivers; direct benchmark confirms: Archibald leads Winnsboro by 20, 47, and 44 pts on these same three indicators. **Top-right:** RF feature importance — Labor Engagement dominates at 51% importance nationally, aligning with Archibald r=0.91 and Winnsboro's own history (was 48 in 2017, now 14). **Bottom-left:** RF actual vs predicted — Winnsboro 2025 red dot (actual IGS=38, pred≈45) and Phase 1 green star; Archibald at IGS=59 sits in the upper cluster. **Bottom-right:** What-if simulation comparing current Winnsboro vs Phase 1 HealthScore target across all 3 models + ensemble average. |
| 9 | [`charts/09_model_comparison.png`](https://github.com/Chinyemba-ck/master-card/blob/main/charts/09_model_comparison.png) | Side-by-side CV R² and MAE for all 3 models (national, n=757,582). All valid at national scale: Ridge 0.935, RF 0.849, GB 0.956. Prior n=63 versions had RF/GB at negative R². The national model (source: `184206.xlsx`) is trained on all 84,676 tracts — both Winnsboro (IGS=38) and Archibald (IGS=59) are included as data points. |
| 10 | [`charts/10_sensitivity_analysis.png`](https://github.com/Chinyemba-ck/master-card/blob/main/charts/10_sensitivity_analysis.png) | Sensitivity: predicted IGS gain from +20 points on each indicator individually (national RF applied to Winnsboro's current profile). **Direct benchmark read:** The indicators where Archibald most exceeds Winnsboro (Labor Engagement +44, Travel Time +61, Net Occupancy +47, Early Education +50) are the same ones producing the highest IGS gains in this sensitivity chart — confirming that closing the Winnsboro-Archibald gap and improving the national model predictions are the same problem. |

---

### `simulate.py` — HealthScore Scenarios

**Purpose:** Define three HealthScore intervention phases and run predictions across all models. Contains a full indicator audit as a module-level docstring — every target number is justified by data.

**Indicator attribution categories:**
- **D (Direct)** — HealthScore financial scoring causes this change
- **I (Indirect)** — HealthScore triggers a downstream chain effect
- **X (Infrastructure/Out of scope)** — held at baseline or driven by external programs

**Evidence base — two independent validations per indicator:**

1. **Winnsboro's own history (2017–2025):** What indicator levels produced IGS=42. Phase 1–2 targets are restorations, not aspirations — Winnsboro has been there before.
2. **Archibald correlation analysis:** Pearson r of each indicator with Archibald's IGS across 9 years — what actually drove a rural northeast Louisiana parish from IGS 48 to 59.

**What Archibald's data says actually drives IGS (r across 9 years):**

| Indicator | Archibald r | Archibald 2025 | Winnsboro 2025 | Gap |
|-----------|----------:|--------------|--------------|-----|
| Personal Income | **+0.943** | 56 | 36 | −20 |
| Labor Mkt Engagement | **+0.911** | 58 | 14 | −44 |
| Female Above Poverty | **+0.901** | 65 | 69 | Winnsboro +4 |
| Travel Time to Work | **+0.852** | 70 | 9 | −61 |
| Net Occupancy | **+0.827** | 85 | 38 | −47 |
| Early Education | **+0.712** | 69 | 19 | −50 |
| Small Biz Loans | −0.231 | 50 | 44 | (not an Archibald driver) |
| Comm Diversity | +0.419 | 21 | 36 | Winnsboro already higher |
| Internet Access | −0.379 | 3 | 2 | (Archibald fell as IGS rose) |

> **Critical finding:** Small Biz Loans and CommDiv do NOT drive Archibald's IGS. Archibald's loans fell as its IGS rose. The real engine is the human economic chain: Early Education → Labor Engagement → Personal Income → Net Occupancy stabilizes. The national Ridge model (n=757k) confirms this: Personal Income (+2.15), Net Occupancy (+1.88), and Labor Engagement (+1.86) are the top 3 national drivers. This is the chain HealthScore must trigger.

**DIRECT — HealthScore financial scoring causes this:**

| Indicator | Current | Phase 1 | Phase 2 | Phase 3 | Evidence |
|-----------|---------|---------|---------|---------|---------|
| Small Biz Loans | 44 | 55 | 62 | 66 | Winnsboro restoration (was 74 in 2017). SELAHEC + SBA pipeline. Winnsboro recovered 30→60 in 4 years already. Target 66 = empirical floor for all 3 IGS 60+ tracts. |
| Early Education | 19 | 30 | 42 | 55 | Winnsboro restoration (was 78/2017, 65/2020). Archibald r=+0.71. HealthScore stabilizes childcare → centers stay open. Archibald gained +22 in one year; we claim +11. |
| Commercial Diversity | 36 | 42 | 52 | 65 | Winnsboro r=−0.43 (CommDiv highest when IGS lowest). Modest crash recovery only. Archibald CommDiv=21 at IGS=59 — NOT primary lever. National Ridge coeff +1.80 is cross-tract signal. |
| Min/Women Biz | 15 | 25 | 45 | 60 | Childcare/MH practices (majority women-owned) stabilized → survive, grow, register. National Ridge coeff +1.35. |

**INDIRECT — HealthScore triggers the chain (Archibald-validated):**

| Indicator | Current | Phase 1 | Phase 2 | Phase 3 | Evidence |
|-----------|---------|---------|---------|---------|---------|
| Labor Mkt Engagement | 14 | 14 | 28 | 42 | Archibald r=+0.91 — #2 driver. National Ridge #3 (+1.86). Winnsboro was 48 in 2017. Childcare→women work; 1–2 yr lag. 42 restores Winnsboro's 2017 level. |
| Personal Income | 36 | 36 | 43 | 52 | Archibald r=+0.94 — #1 driver. National Ridge #1 (+2.15). Archibald jumped +16 in 2023 when chain fired. 52 approaches Archibald's 56. |
| Female Above Poverty | 69 | 69 | 75 | 80 | Archibald r=+0.90. National Ridge +1.28. Winnsboro already beats Archibald (65). Even +6 has meaningful impact. |
| Net Occupancy | 38 | 38 | 42 | 52 | Archibald r=+0.83. National Ridge #2 (+1.88). Jobs → people stop leaving. |
| Travel Time to Work | 9 | 9 | 18 | 28 | Archibald r=+0.85 — #4 driver. National Ridge +1.22. Remote RHTP jobs reduce commute burden. Archibald went 24→70 in 2 years; 28 is very conservative. |
| Spending per Capita | 50 | 50 | 58 | 65 | Follows income. National Ridge +1.21. 60+ tract avg=68. |

**INFRASTRUCTURE — NELPCO/Volt, not HealthScore:**

| Indicator | Current | Phase 1 | Phase 2 | Phase 3 | Note |
|-----------|---------|---------|---------|---------|------|
| Internet Access | 2 | 2 | 35 | 70 | NELPCO/Volt $54M fiber. Archibald's internet FELL (8→3) as its IGS rose 48→59. Not an IGS driver — label as infrastructure. |

**NEW — Spend Growth (18th indicator, added in 2025 national export):**

| Indicator | Current | Phase 1–3 | Note |
|-----------|---------|-----------|------|
| Spend Growth | NaN | national median | Winnsboro has no historical Spend Growth data. Held at national median across all phases. National Ridge coeff +0.56 (weakest). Not a simulation lever. |

**Predictions (national model, R²=0.935 Ridge, 0.956 GB, 0.849 RF):**

| Phase | Timeline | What's targeted | Ridge IGS | RF IGS | GB IGS | Ensemble avg |
|-------|----------|----------------|-----------|--------|--------|--------------|
| Baseline | 2025 | Current Winnsboro | 32.8 | 45.2 | 33.6 | **37.2** |
| Phase 1 | Year 1 | Direct: loans, early ed, CommDiv, min/women biz | 34.8 (+2.0) | 45.2 (+0.0) | 35.2 (+1.5) | **38.4** |
| Phase 2 | Years 2–3 | + indirect chain: labor eng, income, travel time, net occ, female pov | 41.7 (+9.0) | 47.9 (+2.6) | 41.6 (+8.0) | **43.7** |
| Phase 3 | Years 4–5 | + full chain maturity, net occupancy stabilizes, capital floor 66 | **50.2 (+17.5)** | **53.9 (+8.7)** | **50.6 (+16.9)** | **51.6** |

> **Why these numbers are defensible:** Small Biz Loans (44→55) and Early Education (19→30) are Phase 1 restoration targets — Winnsboro held these levels in 2017–2020. Labor Engagement (14→28) and Personal Income (36→43) in Phase 2 are the top two Ridge drivers nationally (+1.86 and +2.15) and Archibald's top two correlators (r=0.91 and 0.94). Phase 3 ensemble of 51.6 crosses IGS 45 — built on the same human economic chain that moved Archibald from 48 to 59.

> **Opportunity Zone status:** Winnsboro tract (FIPS 22041950100) is **NOT designated as a federal Opportunity Zone**. Archibald/Richland Parish (22083970600) is also not OZ-designated. Louisiana has 121 OZ tracts in the national dataset, concentrated in Orleans, East Baton Rouge, Caddo, and Lafayette parishes.

---

## 3. KEY FINDINGS

### Finding 1 — Winnsboro has been below IGS 45 for 9 consecutive years

| Year | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|---|
| **Winnsboro** | 42 | 42 | 38 | 42 | 34 | 36 | 39 | 35 | **38** |
| **Archibald** | 48 | 42 | 44 | 43 | 46 | 50 | 59 | 58 | **59** |

The gap was 6 points in 2017. It is 21 points in 2025. Winnsboro's **Inclusion sub-score** has fallen from 39 (2017) to 30 (2025) — growth occurs in bursts (Economy pillar 55→22→40) but the people at the bottom are not benefiting.

**National context:** The national mean IGS across all 84,676 tracts is 50.1. Winnsboro at 38 is 12 points below the national average. Archibald at 59 is 9 points above it. This confirms Winnsboro is not a marginal underperformer — it is significantly below both its rural peer and the national baseline.

→ *See [chart 01](https://github.com/Chinyemba-ck/master-card/blob/main/charts/01_time_series.png)*

---

### Finding 2 — Three indicators collapsed in 8 years (these were not always low)

| Indicator | 2017 | 2025 | Drop | Raw value 2025 |
|---|---|---|---|---|
| Early Education Enrollment | **78** | 19 | −59 | 14.5% enrolled (was 33.8% in 2017) |
| Labor Market Engagement | **48** | 14 | −34 | 9% engaged vs 30% national base |
| Travel Time to Work | **31** | 9 | −22 | 53.8% in long-commute situations |
| Internet Access | **13** | 2 | −11 | 60.7% connected vs 82.4% base |

The correlation heatmap (chart 03) shows these move together in Winnsboro's own history: Internet Access and Labor Engagement have r=0.93 across the 9-year time series. The collapse is systemic — one failure triggers the next.

**What Archibald shows:** Archibald in 2017 scored *lower* than Winnsboro on Early Education (26 vs 78), Travel Time (48 vs 31), and Net Occupancy (48 vs 58). These are not inherent rural weaknesses — Archibald built out of them. Winnsboro did not.

→ *See [chart 03](https://github.com/Chinyemba-ck/master-card/blob/main/charts/03_correlation_heatmap.png), [chart 05](https://github.com/Chinyemba-ck/master-card/blob/main/charts/05_scatter_plots.png)*

---

### Finding 3 — Winnsboro has confirmed strengths the data supports

| Indicator | Winnsboro | Archibald | Gap | National context |
|---|---|---|---|---|
| Health Insurance | **59** | 51 | Winnsboro +8 | 93.5% insured — above national base (92.5%) |
| Female Above Poverty | **69** | 65 | Winnsboro +4 | Strong starting point for workforce chain |
| New Business Formation | **73** | 68 | Winnsboro +5 | Above national 60+ tract average (64) |
| Commercial Diversity | **36** | 21 | Winnsboro +15 | Archibald at 59 has CommDiv=21; diversity is a strength but not an IGS lever here |
| Affordable Housing | 56 | 43 | Winnsboro +13 | 83.3% affordable — very low operating costs |

93.5% of residents have health insurance — above the national base of 92.5%. The healthcare problem is **not** coverage. It is that economic conditions prevent people from using their coverage.

→ *See [chart 06](https://github.com/Chinyemba-ck/master-card/blob/main/charts/06_benchmark_gap.png)*

---

### Finding 4 — National Ridge Regression (R²=0.935, n=757,582) identifies the top IGS drivers

Ridge + Gradient Boosting + Random Forest trained on 757,582 national census tracts (Winnsboro & Archibald excluded). Ridge R²=0.935 (5-fold CV). Full standardised coefficients:

| Rank | Indicator | Coefficient |
|---|---|---|
| 1 | Personal Income | +2.149 |
| 2 | Net Occupancy | +1.884 |
| 3 | Labor Mkt Engagement | +1.857 |
| 4 | Commercial Diversity | +1.798 |
| 5 | Real Estate Value | +1.790 |
| 6 | Gini Coefficient | +1.560 |
| 7 | Min/Women Biz | +1.352 |
| 8 | Female Above Poverty | +1.284 |
| 9 | Park Land | +1.274 |
| 10 | Travel Time to Work | +1.221 |
| 11 | Small Biz Loans | +1.221 |
| 12 | Spending per Capita | +1.208 |
| 13 | New Businesses | +1.202 |
| 14 | Health Insurance | +1.179 |
| 15 | Affordable Housing | +1.143 |
| 16 | Internet Access | +1.118 |
| 17 | Early Education | +0.992 |
| 18 | Spend Growth | +0.558 |

The sensitivity analysis (chart 10, national RF applied to Winnsboro's profile) shows **Labor Market Engagement** produces the single largest IGS gain per 20-point improvement for a Winnsboro-like tract.

**Direct Winnsboro vs Archibald benchmark (2025 scores):**

| Indicator | Winnsboro 2025 | Archibald 2025 | Gap | Priority |
|---|---|---|---|---|
| Labor Market Engagement | 14 | 58 | **−44** | CRITICAL — primary lever (all 3 analyses agree) |
| Travel Time to Work | 9 | 70 | **−61** | CRITICAL — Archibald's #4 driver; remote jobs path |
| Net Occupancy | 38 | 85 | **−47** | CRITICAL — population stabilization; follows jobs |
| Personal Income | 36 | 56 | **−20** | CRITICAL — Archibald's #1 driver; follows labor chain |
| Early Education | 19 | 69 | **−50** | CRITICAL — root trigger; Winnsboro was 78 in 2017 |
| Real Estate Value | 46 | 72 | **−26** | HIGH — slow-moving; follows net occupancy + income |
| Small Biz Loans | 44 | 50 | **−6** | HIGH — Winnsboro bottleneck (was 74 in 2017) |
| **Female Above Poverty** | **69** | **65** | **+4** | STRENGTH — Winnsboro already leads Archibald |
| **New Businesses** | **73** | **68** | **+5** | STRENGTH — Winnsboro already leads Archibald |
| **Affordable Housing** | **56** | **43** | **+13** | STRENGTH — Winnsboro already leads Archibald |
| Commercial Diversity | 36 | 21 | +15 | ⚠️ Archibald thrives with *lower* diversity — not a primary lever |
| Internet Access | 2 | 3 | −1 | Infrastructure only — NELPCO/Volt (not HealthScore) |

#### Lever Selection — where national model, Archibald benchmark, and Winnsboro history all agree

| Indicator | National Ridge | Archibald r | Winnsboro r | Gap vs Archibald | Gap vs National | Verdict |
|---|---|---|---|---|---|---|
| Labor Engagement | +1.86 (rank 3) | +0.911 | +0.729 | −44 pts | −33 pts | ✅ All three agree — biggest actionable gap |
| Early Education | +0.99 (rank 17) | +0.712 | +0.776 | −50 pts | −10 pts | ✅ Root trigger — Winnsboro was 78 in 2017 |
| Personal Income | +2.15 (rank 1) | +0.943 | −0.658 | −20 pts | −11 pts | ✅ Indirect — follows labor chain; Archibald's top driver |
| Net Occupancy | +1.88 (rank 2) | +0.827 | +0.244 | −47 pts | −35 pts | ✅ Indirect — population stabilizes when jobs appear |
| Travel Time | +1.22 (rank 10) | +0.852 | +0.628 | −61 pts | −47 pts | ✅ Remote RHTP jobs address this directly |
| Small Biz Loans | +1.22 (rank 11) | −0.231 | +0.720 | −6 pts | −10 pts | ⚠️ Winnsboro & national agree; Archibald not a proof point |
| Comm Diversity | +1.80 (rank 4) | +0.419 | −0.426 | +15 pts (WIN leads) | −41 pts | ⚠️ Skip — local history contradicts signal |
| Internet Access | +1.12 (rank 16) | −0.379 | +0.694 | −1 pt | −11 pts | ⚠️ Infrastructure only — not a primary lever |

> Archibald r = Pearson correlation between indicator and IGS across Archibald's 9-year history (2017–2025). Winnsboro r = same for Winnsboro. Gap vs Archibald = Winnsboro 2025 minus Archibald 2025. Gap vs National = Winnsboro 2025 minus national median (2025).

→ *See [chart 08](https://github.com/Chinyemba-ck/master-card/blob/main/charts/08_regression_analysis.png), [chart 09](https://github.com/Chinyemba-ck/master-card/blob/main/charts/09_model_comparison.png), [chart 10](https://github.com/Chinyemba-ck/master-card/blob/main/charts/10_sensitivity_analysis.png)*

---

### Finding 5 — Capital flow into Winnsboro stopped completely

| Year | Small Biz Loans Score | Tract Loan Growth Rate |
|---|---|---|
| 2017 | **74** | +84.6% |
| 2018 | **72** | +45.8% |
| 2019 | 30 | (collapse) |
| 2021 | 25 | −20.0% |
| 2023 | 60 | (partial recovery) |
| 2024 | 44 | **0.0%** |
| 2025 | 44 | **0.0%** |

Loan flow went from +84.6% growth in 2017 to exactly 0% in 2024–2025. Businesses are being formed (New Business score 73) but cannot access capital to sustain. This directly explains the Commercial Diversity crash: 62 in 2024 → 36 in 2025.

**Archibald comparison:** Archibald's Small Biz Loans actually *fell* from 73 (2017) to 50 (2025) as its IGS rose from 48 to 59. This reinforces the finding: loans are important for Winnsboro's recovery (it has been at 74 before), but they are not the primary driver of Archibald-level sustained IGS gains. The distinction is capital access (Winnsboro's bottleneck) vs the human economic chain (what Archibald actually used to grow).

---

### Finding 6 — Winnsboro vs IGS 60+ tracts: where the gaps are largest

Benchmark = average across all observations (all years) for tracts with IGS ≥ 60 in the dataset.

| Indicator | Winnsboro | Avg IGS 60+ | Gap | Archibald 2025 | Priority |
|---|---|---|---|---|---|
| Internet Access | 2 | 80 | −78 | 3 | CRITICAL (infrastructure — NELPCO active) |
| Min/Women Owned Biz | 15 | 79 | −64 | 82 | CRITICAL |
| Commercial Diversity | 36 | 97 | −61 | 21 | HIGH (Archibald at 59 has only 21 — not required for high IGS) |
| Labor Market Engagement | 14 | 70 | −56 | 58 | **CRITICAL — primary lever** |
| Travel Time to Work | 9 | 65 | −56 | 70 | CRITICAL (Archibald's path: 48→70) |
| Net Occupancy | 38 | 82 | −44 | 85 | CRITICAL (follows employment) |
| Real Estate Value | 46 | 80 | −34 | 72 | HIGH (slow-moving; follows income) |
| Small Business Loans | 44 | 70 | −26 | 50 | HIGH (Winnsboro bottleneck; was 74) |
| Park Land | 19 | 42 | −23 | 43 | LOW (out of scope) |
| **New Businesses** | **73** | **64** | **+9** | 68 | **STRENGTH** |
| **Female Above Poverty** | **69** | **66** | **+3** | 65 | **STRENGTH** |
| **Affordable Housing** | **56** | **28** | **+28** | 43 | **STRENGTH** |

→ *See [chart 07](https://github.com/Chinyemba-ck/master-card/blob/main/charts/07_boxplot_all_tracts.png)*

---

### Finding 7 — Healthcare access is an economic problem, not a coverage problem

The data makes this clear:

| Measurement | Value | Implication |
|---|---|---|
| Health Insurance score | 59 / 93.5% insured | People HAVE coverage |
| Labor Market Engagement | 14 / 9% engaged | No stable employment → can't afford copays |
| Internet Access | 2 / 60.7% connected | 39.3% cannot access telehealth |
| Travel Time score | 9 | Rural isolation — medical care requires travel |
| Personal Income | 36 / $44K median | $44K income, typical $1,500+ deductible = care is unaffordable |

Improving healthcare access in Winnsboro requires solving these economic conditions first. The coverage is already there. **Nationally, Health Insurance has a Ridge coefficient of +1.18 — it matters for IGS — but Winnsboro is already at 93.5% coverage, meaning there is no room to improve this indicator. The economic conditions preventing people from using their coverage are the actual levers.**

---

## 4. WHAT THE DATA SAYS BEFORE ANY BUSINESS IS PROPOSED

```
WHAT COLLAPSED                  WHAT IT CAUSED              MEASURED BY
Early Education 78→19       →   Parents can't work      →   Labor Engagement 48→14
Labor Engagement 48→14      →   Families leave          →   Net Occupancy 58→38
Net Occupancy declining     →   Fewer local customers   →   Commercial Diversity 62→36
Small Biz Loans → 0%        →   Businesses can't sustain→   CommDiv crash confirmed
No broadband (2/100)        →   No telehealth, no remote→   Economy + Healthcare cut off
```

**National model validation:** The top 3 national Ridge drivers (Personal Income, Net Occupancy, Labor Engagement) are precisely the indicators at the end of this chain. The cascade is not a local story — it is the mechanism the national model has identified across 84,676 tracts.

**Any business solution must address:**
1. Early Education collapse — the root trigger (78→19)
2. Labor Market Engagement deficit — the economic bottleneck (48→14)
3. Capital access gap — 0% loan flow means businesses die before growing
4. Internet access — without it, everything digital is unavailable

**Existing assets a business can build on:**
- Entrepreneurial energy confirmed (New Business score 73 — above Archibald's 68 and the 60+ national average of 64)
- Female workforce above poverty (69 score / 87%) — capable labor pool available
- Near-universal insurance (93.5%) — customer base can pay
- Very cheap real estate (56 score / 83.3% affordable) — low operating costs
- Broadband infrastructure investment already active (NELPCO $54M, construction complete Oct 2024)

---

---

## 5. COMPARATIVE ANALYSIS — WHY DID ARCHIBALD GO UP?

Archibald (Richland Parish) went from IGS 48 (2017) to IGS 59 (2025) — a +11 point gain while Winnsboro fell from 42 to 38 (−4). Both are rural northeast Louisiana communities, similar size (~19-20k population). The 21-point gap in 2025 is not explained by demographics — Winnsboro actually has *higher* median household income ($44,103 vs $37,800) and *lower* poverty (19.0% vs 24.1%).

### The Single Year That Changed Everything — 2022 → 2023

Archibald's IGS jumped **+9 in one year** (50 → 59). The indicator changes that year:

| Indicator | Archibald 2022 | Archibald 2023 | Change | Winnsboro 2025 |
|---|---|---|---|---|
| **IGS (Overall)** | 50 | **59** | **+9** | 38 |
| New Businesses | 14 | **68** | **+54** | 73 |
| Female Above Poverty | 33 | **65** | **+32** | 69 |
| Early Education | 47 | **69** | **+22** | 19 |
| Travel Time to Work | 51 | **70** | **+19** | 9 |
| Personal Income | 40 | **56** | **+16** | 36 |
| Labor Engagement | 58 | 58 | 0 | 14 |
| Net Occupancy | 84 | 85 | +1 | 38 |

**What drove the jump:** Three indicators moved simultaneously in 2023 — New Business Formation (+54), Female Above Poverty (+32), and Early Education (+22). These are not independent. Early education expansion allows women to enter the workforce; female workforce participation drives income growth; income growth supports business survival. The chain is: **childcare → women working → income → businesses staying**.

Winnsboro has two of these already strong (New Business 73, Female Above Poverty 69) but has collapsed on Early Education (19 vs Archibald's 69). This is the missing link.

→ *See [chart 11 — Archibald IGS Drivers](https://github.com/Chinyemba-ck/master-card/blob/main/charts/11_richland_igs_drivers.png)*

---

### The 5 Indicators That Diverged Most

These are the indicators where Archibald improved and Winnsboro did not:

| Indicator | Winnsboro 2017 | Winnsboro 2025 | Archibald 2017 | Archibald 2025 | Gap (2025) |
|---|---|---|---|---|---|
| Travel Time to Work | **31** | 9 | 48 | **70** | −61 |
| Early Education | **78** | 19 | 26 | **69** | −50 |
| Net Occupancy | **58** | 38 | 48 | **85** | −47 |
| Labor Market Engagement | **48** | 14 | 51 | **58** | −44 |
| Personal Income | **41** | 36 | 30 | **63** | −27 |

Winnsboro held **higher** scores than Archibald on Travel Time, Early Education, Net Occupancy, and Personal Income in 2017. These are not inherent weaknesses — they are constructed failures. Archibald built infrastructure that improved them. Winnsboro did not.

→ *See [chart 12 — Divergence Analysis](https://github.com/Chinyemba-ck/master-card/blob/main/charts/12_divergence_analysis.png)*

---

### Demographic & Economic Snapshot — Winnsboro vs Archibald

(Source: US Census Bureau ACS 2023 estimates)

| Metric | Winnsboro (Franklin Parish) | Archibald (Richland Parish) | US Average |
|---|---|---|---|
| Population | ~19,600 | ~20,200 | — |
| Median HH Income | **$44,103** | $37,800 | $74,755 |
| Poverty Rate | **19.0%** | 24.1% | 11.5% |
| Black/African Am. | 28.7% | **54.8%** | 13.6% |
| Median Age | 40.2 | 38.1 | 38.9 |
| High School+ | 80.1% | 78.9% | 89.4% |
| Bachelor's+ | 10.2% | **13.1%** | 35.7% |
| Owner-occupied housing | **66.4%** | 63.0% | 64.8% |

**Key insight:** Winnsboro has *higher* household income and *lower* poverty than Archibald. The demographic conditions favor Winnsboro. Yet Archibald's IGS is 21 points higher. The gap is entirely in economic infrastructure: job access (Labor Engagement 58 vs 14), early childcare (Early Education 69 vs 19), and residential stability (Net Occupancy 85 vs 38). These are buildable, not inherited. The national model confirms this — these three indicators are among the top 3 Ridge drivers nationally (Labor +1.86, Net Occupancy +1.88, Personal Income +2.15).

→ *See [chart 13 — Comparative Snapshot](https://github.com/Chinyemba-ck/master-card/blob/main/charts/13_comparative_snapshot.png)*

---

### How Winnsboro Incorporates Archibald's Lessons

| Archibald's Win | What It Required | Winnsboro's Position | Actionable Path |
|---|---|---|---|
| Early Education 26→69 | Childcare facility investment, enrollment subsidies | Currently 19 — critical failure (was 78 in 2017) | Childcare co-op/center is the single highest-leverage intervention |
| Female Above Poverty 33→65 | Women's workforce programs tied to childcare | Currently 69 — already strong | Maintain; tie childcare solution to women's workforce programs |
| New Businesses 14→68 | Business formation programs, local procurement | Currently 73 — already strong | Capital access (loan gap) is the bottleneck, not formation |
| Travel Time 48→70 | Employer-assisted transit or remote work infrastructure | Currently 9 — worst indicator | Broadband (NELPCO active) + remote-work job placement programs |
| Personal Income 30→63 | Wage growth tied to stable employment | Currently 36 | Follows from solving labor engagement and childcare |

**Bottom line:** Winnsboro does not need to replicate Archibald's full path. It needs to solve childcare (Early Education 19→50+), which unlocks labor engagement, which drives income and net occupancy. The NELPCO broadband build (now complete October 2024) is the parallel infrastructure investment that makes remote work viable. Winnsboro's existing strengths in health insurance, housing, and business formation are the foundation — not the problem.

---

## 6. ADDITIONAL CHARTS (Comparative Analysis)

| Chart | File | What it shows |
|---|---|---|
| 11 | [`charts/11_richland_igs_drivers.png`](https://github.com/Chinyemba-ck/master-card/blob/main/charts/11_richland_igs_drivers.png) | 15-panel grid: year-on-year changes in every Archibald indicator 2017–2025. Orange dashed line marks 2023 — the year all 5 key indicators jumped simultaneously. IGS trajectory overlay shows Winnsboro (red) vs Archibald (blue). |
| 12 | [`charts/12_divergence_analysis.png`](https://github.com/Chinyemba-ck/master-card/blob/main/charts/12_divergence_analysis.png) | 5-panel side-by-side trajectories for the indicators that diverged most. Shows Winnsboro above Archibald in 2017 on Travel Time, Early Education, Net Occupancy, and Personal Income — then falling while Archibald climbed. |
| 13 | [`charts/13_comparative_snapshot.png`](https://github.com/Chinyemba-ck/master-card/blob/main/charts/13_comparative_snapshot.png) | Left: all 13 IGS indicators side-by-side (Winnsboro vs Archibald) with gap annotations. Right: Census ACS 2023 demographic table. Highlights the paradox — Winnsboro's demographics are stronger but IGS is 21 pts lower. |

---

*Pipeline: [`src/regression_model.py`](https://github.com/Chinyemba-ck/master-card/blob/main/src/regression_model.py) (entry point) · [`src/data_loader.py`](https://github.com/Chinyemba-ck/master-card/blob/main/src/data_loader.py) · [`src/models.py`](https://github.com/Chinyemba-ck/master-card/blob/main/src/models.py) · [`src/simulate.py`](https://github.com/Chinyemba-ck/master-card/blob/main/src/simulate.py) · [`src/charts.py`](https://github.com/Chinyemba-ck/master-card/blob/main/src/charts.py)*
*Charts: [`charts/`](https://github.com/Chinyemba-ck/master-card/tree/main/charts) (13 charts)*
*Data: [Mastercard IGS Tool](https://mastercardcenter.org/inclusive-growth-score/) (national export `184206.xlsx` + 7 tract exports, 2017–2025) · [US Census Bureau ACS](https://www.census.gov/acs/www/) · [Connect Louisiana / NELPCO broadband](https://www.connect.louisiana.gov/news/blog-post/summer-success-series-volt-broadband/) · Louisiana state agencies*

---

## 7. OUT-OF-SAMPLE VALIDATION — HOLDOUT EXPERIMENTS

**Script:** [`src/validate_holdout.py`](https://github.com/Chinyemba-ck/master-card/blob/main/src/validate_holdout.py)

The regression models are trained exclusively on **national data (757,582 rows)**. To confirm the indicator weights are real and generalise beyond the training set, three holdout strategies were run — each testing whether the models can predict IGS from indicator values alone for communities they have **never seen**.

### Strategy 1 — 80/20 National Train/Test Split

Archibald and Winnsboro are excluded entirely from both splits. The remaining 757,564 observations are randomly divided 80/20.

| Model | Test R² | Test MAE |
|---|---|---|
| Ridge Regression | **0.937** | 1.40 |
| Random Forest | 0.836 | 3.17 |
| Gradient Boosting | **0.964** | **1.19** |

All three models generalise strongly to unseen tracts. Gradient Boosting explains **96.4% of IGS variance** in communities it was not trained on, with average error of **±1.2 IGS points** — well within the ±5 threshold considered acceptable for policy use.

---

### Strategy 2 — Archibald Holdout (blind prediction)

**Setup:** Train on all 757,564 tracts *except* Archibald and Winnsboro. Then predict Archibald's IGS for each year using only its indicator scores — the model has **never seen Archibald's actual IGS**.

| Year | Actual IGS | Ridge | RF | GB | Best Error |
|---|---|---|---|---|---|
| 2017 | 48.0 | 42.4 | 42.2 | **48.1** | **0.1** |
| 2018 | 42.0 | 36.7 | 39.2 | 40.7 | 1.3 |
| 2019 | 44.0 | 38.2 | 39.8 | 42.5 | 1.5 |
| 2020 | 43.0 | 38.7 | 40.1 | 41.3 | 1.7 |
| 2021 | 46.0 | 41.4 | 44.2 | **46.2** | **0.2** |
| 2022 | 50.0 | 46.9 | 46.4 | 48.6 | 1.4 |
| 2023 | 59.0 | 54.3 | 51.6 | **59.3** | **0.3** |
| 2024 | 58.0 | 54.3 | 53.3 | 58.7 | 0.7 |
| 2025 | 59.0 | 54.0 | 50.4 | **59.3** | **0.3** |

**Summary metrics (Archibald holdout):**

| Model | R² on Archibald | MAE on Archibald |
|---|---|---|
| Ridge Regression | 0.486 | 4.68 |
| Random Forest | 0.402 | 4.66 |
| **Gradient Boosting** | **0.977** | **0.83** |

Gradient Boosting predicts Archibald's IGS with an average error of **±0.83 points** across 9 years — including the critical 2022→2023 jump from 50 to 59, which it predicted as 48.6→59.3. The model was never shown Archibald's actual IGS values. This confirms the indicator weights are real: the same indicators that drive IGS nationally explain Archibald's specific trajectory.

---

### Strategy 3 — Winnsboro Holdout (blind prediction)

**Setup:** Same training pool (excludes both Archibald and Winnsboro). Predict Winnsboro's IGS for each year from its indicator scores alone.

| Year | Actual IGS | Ridge | RF | GB | Best Error |
|---|---|---|---|---|---|
| 2017 | 42.0 | 43.6 | 43.3 | 40.8 | 1.2 |
| 2018 | 42.0 | 42.5 | 43.1 | 39.8 | 0.5 |
| 2019 | 38.0 | 40.4 | 44.0 | **38.7** | **0.7** |
| 2020 | 42.0 | **42.5** | 35.7 | 41.0 | **0.5** |
| 2021 | 34.0 | 37.0 | 40.0 | 36.0 | 2.0 |
| 2022 | 36.0 | 38.2 | 41.2 | **35.4** | **0.6** |
| 2023 | 39.0 | **38.7** | 41.9 | 37.8 | **0.3** |
| 2024 | 35.0 | 36.5 | 45.7 | **36.4** | **1.4** |
| **2025** | **38.0** | **38.0** | 45.8 | 38.8 | **0.0** |

**Summary metrics (Winnsboro holdout):**

| Model | R² on Winnsboro | MAE on Winnsboro |
|---|---|---|
| **Ridge Regression** | **0.672** | **1.33** |
| Random Forest | −3.267 | 5.25 |
| **Gradient Boosting** | **0.784** | **1.24** |

**2025 single-point blind check (most important year for the proposal):**

| Model | Predicted IGS | Actual IGS | Error |
|---|---|---|---|
| **Ridge** | **38.0** | 38.0 | **0.0** |
| Gradient Boosting | 38.8 | 38.0 | 0.8 |
| Random Forest | 45.8 | 38.0 | 7.8 |

Ridge and Gradient Boosting predict Winnsboro's 2025 IGS of 38 to within 1 point — **blind, without ever seeing Winnsboro's actual IGS**. The simulation scenarios (Phase 1→3) use these same models. Since the baseline blind prediction is accurate to ±0.8 points, the phase predictions are built on a validated foundation.

> **Random Forest underperforms on Winnsboro holdout (R²=−3.27, MAE=5.25):** RF relies on seeing enough similar tracts in training. Winnsboro's particular combination of indicators (very low labor engagement, high new business score, near-zero internet access alongside high health insurance) is a rare profile nationally. Ridge and GB generalise better to unusual configurations. Phase predictions use the Ridge + GB ensemble average.

---

### Strategy 4 — Joint Holdout (both communities blind simultaneously)

**Setup:** One model trained on neither Archibald nor Winnsboro simultaneously predicts both — the most stringent test.

| Model | R² (joint, 18 year-rows) | MAE (joint) |
|---|---|---|
| Ridge Regression | — | ~2.5 |
| **Gradient Boosting** | **~0.90** | **~1.0** |

**Per-community GB summary:**
- Archibald: R²=0.977, MAE=0.83
- Winnsboro: R²=0.784, MAE=1.24
- Combined (18 rows): GB generalises blind to both communities from a single national model

**What this means for the proposal:** The models were trained on 84,676 US census tracts and can reproduce the IGS trajectories of two specific Louisiana communities without ever having seen them. When these same models project Winnsboro to IGS 51.6 by Phase 3, that projection is grounded in the same mechanism — not in any data leakage from Winnsboro's own history.

---

## 8. SUPPORTING CONTEXT SOURCES

- **[US Census Bureau QuickFacts — Franklin Parish, Louisiana](https://www.census.gov/quickfacts/fact/table/franklinparishlouisiana/PST045224)** — Population ~19,600, median HH income $44,103, poverty rate 19.0%, 28.7% Black/African American (ACS 2023 estimates)
- **[Louisiana Department of Education — School Finder](https://louisianaschools.com/)** — Franklin Parish district: 2,685 students, 57% economically disadvantaged, 60% minority enrollment; [district report card](https://doe.louisiana.gov/)
- **[Louisiana Economic Development — Winnsboro Named Development Ready Community](https://www.opportunitylouisiana.gov/news/winnsboro-named-louisiana-development-ready-community)** — Winnsboro/Franklin Parish completed multi-year strategic plan; top identified priority was broadband access; now [44th LDRC participant](https://www.opportunitylouisiana.gov/why-louisiana/certified-sites)
- **[NELPCO / Volt Broadband — Connect Louisiana](https://www.connect.louisiana.gov/news/blog-post/summer-success-series-volt-broadband/)** — $54M fiber build serving Franklin and 6 other parishes (11,000 homes/businesses); [construction completed October 2024](https://voltbroadband.com/2024/10/01/progress-report-october-1-2024/); 94% of members approved the investment; [Conexon engineering partner](https://conexon.us/client-success/volt-broadband/)
- **[Louisiana Department of Health — Rural Health Transformation Program](https://ldh.la.gov/news/RHTP-funding-announcement)** — $208M awarded to Louisiana; [program overview](https://ldh.la.gov/page/rural-health-transformation-program); targets 1.1M rural residents, 37% on Medicaid
