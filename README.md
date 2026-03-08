# Data Analysis Report
## Mastercard AUCDSI HBCU Data Science Challenge 2026
### Franklin Parish, Louisiana — Census Tract 22041950100
### Pre-Proposal Analytical Foundation

**Repository:** [github.com/Chinyemba-ck/master-card](https://github.com/Chinyemba-ck/master-card)

---

## 1. DATASETS USED

### Primary Dataset — Mastercard Inclusive Growth Score (IGS) Tool

7 Excel files exported from the Mastercard IGS Tool, one per census tract.

| File | Census Tract | Location | IGS 2025 | Role |
|---|---|---|---|---|
| [`030542.xlsx`](https://github.com/Chinyemba-ck/master-card/blob/main/igs_exports/Inclusive_Growth_Score_Data_Export_26-02-2026_030542.xlsx) | 22041950100 | Franklin Parish, LA | 38 | **Primary — target tract** |
| [`030523.xlsx`](https://github.com/Chinyemba-ck/master-card/blob/main/igs_exports/Inclusive_Growth_Score_Data_Export_26-02-2026_030523.xlsx) | 22083970600 | Richland Parish, LA | 59 | Benchmark — same state, rural |
| [`025930.xlsx`](https://github.com/Chinyemba-ck/master-card/blob/main/igs_exports/Inclusive_Growth_Score_Data_Export_26-02-2026_025930.xlsx) | 6019005805 | Fresno, CA | 70 | High-performer reference |
| [`025916.xlsx`](https://github.com/Chinyemba-ck/master-card/blob/main/igs_exports/Inclusive_Growth_Score_Data_Export_26-02-2026_025916.xlsx) | 6019003104 | Fresno, CA | 60 | High-performer reference |
| [`025736.xlsx`](https://github.com/Chinyemba-ck/master-card/blob/main/igs_exports/Inclusive_Growth_Score_Data_Export_26-02-2026_025736.xlsx) | 6019003302 | Fresno, CA | <45 | Below-45 comparison |
| [`030838.xlsx`](https://github.com/Chinyemba-ck/master-card/blob/main/igs_exports/Inclusive_Growth_Score_Data_Export_26-02-2026_030838.xlsx) | 48113018501 | Dallas, TX | 60 | High-performer reference |
| [`030824.xlsx`](https://github.com/Chinyemba-ck/master-card/blob/main/igs_exports/Inclusive_Growth_Score_Data_Export_26-02-2026_030824.xlsx) | 48113019013 | Dallas, TX | <45 | Below-45 comparison |

**Dataset structure:**
- Sheet used: `Compared to Urban-Rural`
- Header: 2 rows (multi-level), flattened with `'_'.join()` in pandas
- Columns: ~50 per file — metadata, pillar scores, indicator scores, tract %, base %
- Years: 2017–2025 (9 years per tract)
- **Total observations after concat: 63 rows × ~50 columns**

**Columns extracted per indicator (example — Internet Access):**
- `PLACE_Internet Access Score` — 0–100 score
- `PLACE_Internet Access Tract, %` — raw % in this community
- `PLACE_Internet Access Base, %` — benchmark comparison group %

**Pillars and indicators extracted:**

| Pillar | Indicators (17 total) |
|---|---|
| **Place** (6) | Internet Access, Affordable Housing, Travel Time to Work, Net Occupancy, Park Land, Real Estate Value |
| **Economy** (5) | New Businesses, Small Business Loans, Min/Women Owned Businesses, Labor Market Engagement, Commercial Diversity |
| **Community** (6) | Personal Income, Spending per Capita, Female Above Poverty, Gini Coefficient, Early Education Enrollment, Health Insurance Coverage |

### Supporting Context Sources
- **[US Census Bureau QuickFacts — Franklin Parish, Louisiana](https://www.census.gov/quickfacts/fact/table/franklinparishlouisiana/PST045224)** — Population ~19,600, median HH income $44,103, poverty rate 19.0%, 28.7% Black/African American (ACS 2023 estimates)
- **[Louisiana Department of Education — School Finder](https://louisianaschools.com/)** — Franklin Parish district: 2,685 students, 57% economically disadvantaged, 60% minority enrollment; [district report card](https://doe.louisiana.gov/)
- **[Louisiana Economic Development — Winnsboro Named Development Ready Community](https://www.opportunitylouisiana.gov/news/winnsboro-named-louisiana-development-ready-community)** — Winnsboro/Franklin Parish completed multi-year strategic plan; top identified priority was broadband access; now [44th LDRC participant](https://www.opportunitylouisiana.gov/why-louisiana/certified-sites)
- **[NELPCO / Volt Broadband — Connect Louisiana](https://www.connect.louisiana.gov/news/blog-post/summer-success-series-volt-broadband/)** — $54M fiber build serving Franklin and 6 other parishes (11,000 homes/businesses); [construction completed October 2024](https://voltbroadband.com/2024/10/01/progress-report-october-1-2024/); 94% of members approved the investment; [Conexon engineering partner](https://conexon.us/client-success/volt-broadband/)
- **[Louisiana Department of Health — Rural Health Transformation Program](https://ldh.la.gov/news/RHTP-funding-announcement)** — $208M awarded to Louisiana; [program overview](https://ldh.la.gov/page/rural-health-transformation-program); targets 1.1M rural residents, 37% on Medicaid

### Processed Data (CSV exports for reproducibility)

| File | Description | Rows |
|---|---|---|
| [`data/all_tracts_igs_scores.csv`](https://github.com/Chinyemba-ck/master-card/blob/main/data/all_tracts_igs_scores.csv) | All 7 tracts × 9 years — IGS + all 15 indicator scores | 63 |
| [`data/franklin_parish_indicators.csv`](https://github.com/Chinyemba-ck/master-card/blob/main/data/franklin_parish_indicators.csv) | Franklin Parish only (FIPS 22041950100), 2017–2025 | 9 |
| [`data/richland_parish_indicators.csv`](https://github.com/Chinyemba-ck/master-card/blob/main/data/richland_parish_indicators.csv) | Richland Parish only (FIPS 22083970600), 2017–2025 | 9 |
| [`data/franklin_vs_richland_comparison.csv`](https://github.com/Chinyemba-ck/master-card/blob/main/data/franklin_vs_richland_comparison.csv) | Side-by-side comparison with gap calculations | 9 |

---

## 2. ANALYSIS SCRIPTS

### [`analysis.py`](https://github.com/Chinyemba-ck/master-card/blob/main/src/analysis.py)
**Purpose:** Load all 7 IGS files, build comparison dataset, produce 7 descriptive charts.

**Steps performed:**
1. Load all `.xlsx` files from `igs_exports/` using `os.listdir('igs_exports')`
2. Read each with `pd.read_excel(..., sheet_name='Compared to Urban-Rural', header=[0,1])`
3. Flatten multi-level column headers with `'_'.join()`
4. Drop rows with missing FIPS code, concat all into one DataFrame (63 rows)
5. Filter to Franklin (FIPS 22041950100) and Richland (FIPS 22083970600)
6. Extract 2025 snapshot rows for cross-sectional analysis
7. Compute indicator gaps: `Richland score − Franklin score` for each indicator
8. Produce 7 charts, saved to `charts/`

**Charts produced:**

| Chart | File | What it shows |
|---|---|---|
| 1 | [`charts/01_time_series.png`](https://github.com/Chinyemba-ck/master-card/blob/main/charts/01_time_series.png) | 2×2 panel — Overall IGS, Place, Economy, Community scores 2017–2025. Franklin (red) vs Richland (blue) with 45-threshold line. The shaded red area shows every year Franklin has been below 45. Economy is the most volatile pillar — it swings up then crashes each cycle. |
| 2 | [`charts/02_grouped_bar_indicators.png`](https://github.com/Chinyemba-ck/master-card/blob/main/charts/02_grouped_bar_indicators.png) | All 16 indicators side-by-side, Franklin (solid) vs Richland (faded), color-coded by pillar. Visually shows Franklin beats Richland on Health Insurance, Female Above Poverty, New Businesses, and Commercial Diversity — but is far behind on Min/Women Biz, Labor Engagement, Net Occupancy, Travel Time, and Early Education. |
| 3 | [`charts/03_correlation_heatmap.png`](https://github.com/Chinyemba-ck/master-card/blob/main/charts/03_correlation_heatmap.png) | Pearson correlation matrix across all indicator scores in Franklin's 9-year time series. Key correlations: Internet Access vs Labor Engagement (r=0.93), Internet Access vs Travel Time (r=0.87), Health Insurance vs Early Education (r=−0.93). These show indicators move together — the collapse is systemic, not isolated. |
| 4 | [`charts/04_radar_chart.png`](https://github.com/Chinyemba-ck/master-card/blob/main/charts/04_radar_chart.png) | Radar chart across 9 sub-dimensions (Place/Economy/Community × Overall/Growth/Inclusion). Franklin's shape shows strong Economy Growth but collapsed Economy Inclusion and Community Inclusion. Richland dominates on Place Growth. Both fail Community Inclusion. |
| 5 | [`charts/05_scatter_plots.png`](https://github.com/Chinyemba-ck/master-card/blob/main/charts/05_scatter_plots.png) | Two scatter plots with year labels on Franklin points. Left: Internet Access % vs Economy Score — Franklin's economy score tracks below Richland across the same internet access range, showing internet alone doesn't explain the gap. Right: Labor Engagement % vs IGS — as Franklin's labor engagement fell from 33% to 9%, IGS tracked downward in lockstep. |
| 6 | [`charts/06_benchmark_gap.png`](https://github.com/Chinyemba-ck/master-card/blob/main/charts/06_benchmark_gap.png) | Horizontal bar chart of every indicator gap (Richland minus Franklin), ranked. Negative bars (left of zero) = Franklin beats Richland: Commercial Diversity (−15), Health Insurance (−8), New Businesses (−5), Female Above Poverty (−4). Largest gaps in Richland's favour: Min/Women Biz (+67), Travel Time (+61), Early Education (+50), Net Occupancy (+47), Labor Engagement (+44). |
| 7 | [`charts/07_boxplot_all_tracts.png`](https://github.com/Chinyemba-ck/master-card/blob/main/charts/07_boxplot_all_tracts.png) | Box plots of IGS distribution (2017–2025) for all 7 tracts. Franklin has the tightest, lowest box — range 34–42, median ~38. It has never crossed 45. Fresno 5805 sits entirely above 65. Richland straddles the 45 threshold. Dallas 18501 and Fresno 3104 consistently above 50. |

---

### [`regression_model.py`](https://github.com/Chinyemba-ck/master-card/blob/main/src/regression_model.py)
**Purpose:** Train three ML models on the 63-observation dataset, identify IGS drivers, run what-if simulation.

**Steps performed:**
1. Build model dataset: 63 rows, 17 feature columns, target = `SUMMARY_Inclusive Growth Score`
2. Drop rows where target is missing; fill feature NaN with column median
3. Standardize features with `StandardScaler` (for Ridge coefficients to be comparable)
4. Train three models with 5-fold cross-validation
5. Compute feature importance (RF) and standardized coefficients (Ridge)
6. Run Franklin Parish what-if simulation
7. Run indicator sensitivity: test +20 points on each indicator individually

**Model performance — cross-validated (5-fold CV):**

| Model | CV R² | CV MAE | Verdict |
|---|---|---|---|
| **Ridge Regression** | **0.805 ± 0.186** | **2.45 ± 1.25** | ✅ **Valid — use this** |
| Random Forest | **−0.151 ± 1.318** | 5.28 ± 1.53 | ❌ Overfitting — CV R² is negative |
| Gradient Boosting | **−0.366 ± 1.368** | 5.96 ± 1.42 | ❌ Overfitting — CV R² is negative |

> **Critical note:** With only 63 observations, Random Forest and Gradient Boosting overfit. Their training R² looks good (RF training R²=0.987 visible in chart 08) but cross-validated R² is negative — meaning they fail to generalize. **Ridge Regression is the only statistically valid model for this dataset.** RF and GB are shown for directional reference only.

**Charts produced:**

| Chart | File | What it shows |
|---|---|---|
| 8 | [`charts/08_regression_analysis.png`](https://github.com/Chinyemba-ck/master-card/blob/main/charts/08_regression_analysis.png) | 4-panel. Top-left: Ridge standardized coefficients — Commercial Diversity (+2.81) and Net Occupancy (+1.93) are the top positive drivers. Health Insurance (−1.41) has a negative coefficient (artifact of small dataset, not causal). Top-right: RF feature importance — Net Occupancy (0.354) and Labor Engagement (0.242) dominate. Bottom-left: RF actual vs predicted — training R²=0.987 (misleadingly high, this is train-set overfitting). Bottom-right: What-if simulation — BridgeWork scenario lifts ensemble average from 38.0 to 44.6. |
| 9 | [`charts/09_model_comparison.png`](https://github.com/Chinyemba-ck/master-card/blob/main/charts/09_model_comparison.png) | Side-by-side CV R² and CV MAE for all 3 models. Shows RF and GB with negative CV R² — confirming they overfit on n=63. Ridge is the clear winner with R²=0.805, MAE=2.45. |
| 10 | [`charts/10_sensitivity_analysis.png`](https://github.com/Chinyemba-ck/master-card/blob/main/charts/10_sensitivity_analysis.png) | Sensitivity: predicted IGS gain from +20 points on each indicator individually (using RF). Top single-indicator impact: **Labor Market Engagement (+2.3 pts)** far above all others, then Small Business Loans (+1.5), Internet Access (+0.9), Net Occupancy (+0.5). Everything else under +0.3. Health Insurance and Min/Women Biz show slight negative — overfitting artifact. Read with caution given RF overfitting issue. |

---

### [`deep_analysis.py`](https://github.com/Chinyemba-ck/master-card/blob/main/src/deep_analysis.py)
**Purpose:** Ridge-only simulation with three planning scenarios and benchmark gap tables.

**Steps performed:**
1. Re-trains Ridge model (same dataset, same parameters)
2. Hardcodes current Franklin 2025 values from IGS exports
3. Defines three intervention scenarios with explicit indicator targets
4. Predicts IGS for each scenario
5. Prints gap table: Franklin vs average of 3 IGS 60+ tracts
6. Prints lesson table: Franklin vs Richland on every indicator

**Three scenarios and Ridge predictions:**

| Scenario | Indicators changed | Ridge IGS prediction |
|---|---|---|
| Scenario 1 — Conservative | Internet→35, LaborEng→30, MinWomen→40, EarlyEd→35, TravelTime→25, CommDiv→55 | **40.6** |
| Scenario 2 — Expanded | + SmBizLoans→66, NetOcc→65, PersonalIncome→50, RealEstate→60, SpendPC→55 | **51.0** |
| Scenario 3 — Full scale | All indicators adjusted toward IGS 60+ levels | **63.9** |

> These are **Ridge-only** predictions. Given that RF and GB overfit, the RF/GB scenario estimates previously cited (45.5, 47.7) are not reliable for n=63. Ridge predictions (40.6, 51.0, 63.9) are the valid numbers.

---

## 3. KEY FINDINGS

### Finding 1 — Franklin Parish has been below IGS 45 for 9 consecutive years

| Year | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|---|
| Franklin | 42 | 42 | 38 | 42 | 34 | 36 | 39 | 35 | **38** |
| Richland | 48 | 42 | 44 | 43 | 46 | 50 | 59 | 58 | **59** |

The gap was 6 points in 2017. It is 21 points in 2025. Franklin's **Inclusion sub-score** has fallen from 39 (2017) to 30 (2025) — growth is occurring in bursts but the people at the bottom are not benefiting.

→ *See [chart 01](https://github.com/Chinyemba-ck/master-card/blob/main/charts/01_time_series.png)*

---

### Finding 2 — Three indicators collapsed in 8 years (these were not always low)

| Indicator | 2017 | 2025 | Drop | Raw value 2025 |
|---|---|---|---|---|
| Early Education Enrollment | 78 | **19** | −59 | 14.5% enrolled (was 33.8% in 2017) |
| Labor Market Engagement | 48 | **14** | −34 | 9% engaged vs 30% national base |
| Travel Time to Work | 31 | **9** | −22 | 53.8% in long-commute situations |
| Internet Access | 13 | **2** | −11 | 60.7% connected vs 82.4% base |

The correlation heatmap (chart 03) shows these move together: Internet Access and Labor Engagement have r=0.93 across Franklin's 9 years. The collapse is systemic — one failure triggers the next.

→ *See [chart 03](https://github.com/Chinyemba-ck/master-card/blob/main/charts/03_correlation_heatmap.png), [chart 05](https://github.com/Chinyemba-ck/master-card/blob/main/charts/05_scatter_plots.png)*

---

### Finding 3 — Franklin has confirmed strengths the data supports

| Indicator | Franklin | Richland | Gap |
|---|---|---|---|
| Health Insurance | **59** | 51 | Franklin +8 |
| Female Above Poverty | **69** | 65 | Franklin +4 |
| New Business Formation | **73** | 68 | Franklin +5 |
| Commercial Diversity | **36** | 21 | Franklin +15 |
| Affordable Housing | **56** | 72 | Richland +16 |

93.5% of residents have health insurance — above the national base of 92.5%. The healthcare problem is **not** coverage. It is that economic conditions prevent people from using their coverage.

→ *See [chart 06](https://github.com/Chinyemba-ck/master-card/blob/main/charts/06_benchmark_gap.png)*

---

### Finding 4 — Ridge Regression (R²=0.805) identifies the top IGS drivers

Ridge is the only cross-validated model that generalizes on this dataset (n=63). Top standardized coefficients:

| Rank | Indicator | Coefficient | Implication |
|---|---|---|---|
| 1 | Commercial Diversity | +2.81 | Most actionable lever — diverse business base drives IGS |
| 2 | Net Occupancy | +1.93 | Population staying = growth is stable, not just bursts |
| 3 | Labor Market Engagement | +1.44 | More people working = more economic activity across all pillars |
| 4 | Small Business Loans | +1.25 | Capital access is prerequisite for business survival |
| 5 | Early Education | +1.13 | Childcare enrollment unlocks parental workforce participation |

Sensitivity analysis (chart 10, using RF — treat as directional) shows **Labor Market Engagement** produces the single largest IGS gain per 20-point improvement: +2.3 predicted points. Small Business Loans is second (+1.5).

→ *See [chart 08](https://github.com/Chinyemba-ck/master-card/blob/main/charts/08_regression_analysis.png), [chart 09](https://github.com/Chinyemba-ck/master-card/blob/main/charts/09_model_comparison.png), [chart 10](https://github.com/Chinyemba-ck/master-card/blob/main/charts/10_sensitivity_analysis.png)*

---

### Finding 5 — Capital flow into Franklin Parish stopped completely

| Year | Small Biz Loans Score | Tract Loan Growth Rate |
|---|---|---|
| 2017 | 74 | +84.6% |
| 2018 | 72 | +45.8% |
| 2021 | 25 | −20.0% |
| 2024 | 44 | **0.0%** |
| 2025 | 44 | **0.0%** |

Loan flow went from +84.6% growth in 2017 to exactly 0% in 2024–2025. Businesses are being formed (New Business score 73) but cannot access capital to sustain. This directly explains the Commercial Diversity crash: 62 in 2024 → 36 in 2025.

---

### Finding 6 — Franklin vs IGS 60+ tracts: where the gaps are largest

| Indicator | Franklin | Avg IGS 60+ | Gap | Priority |
|---|---|---|---|---|
| Internet Access | 2 | 70 | −68 | CRITICAL |
| Commercial Diversity | 36 | 98 | −62 | CRITICAL |
| Min/Women Owned Biz | 15 | 75 | −60 | CRITICAL |
| Labor Market Engagement | 14 | 61 | −47 | CRITICAL |
| Travel Time to Work | 9 | 51 | −42 | CRITICAL |
| Net Occupancy | 38 | 78 | −40 | HIGH |
| Small Business Loans | 44 | 66 | −22 | HIGH |
| **Health Insurance** | **59** | **52** | **+7** | STRENGTH |
| **Female Above Poverty** | **69** | **50** | **+19** | STRENGTH |
| **Affordable Housing** | **56** | **44** | **+12** | STRENGTH |

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

Improving healthcare access in Franklin Parish requires solving these economic conditions first. The coverage is already there.

---

## 4. WHAT THE DATA SAYS BEFORE ANY BUSINESS IS PROPOSED

```
WHAT COLLAPSED               WHAT IT CAUSED              MEASURED BY
Early Education 78→19    →   Parents can't work      →   Labor Engagement 48→14
Labor Engagement 48→14   →   Families leave          →   Net Occupancy −9.9%/yr
Net Occupancy declining  →   Fewer local customers   →   Commercial Diversity 62→36
Small Biz Loans → 0%     →   Businesses can't sustain→   CommDiv crash confirmed
No broadband (2/100)     →   No telehealth, no remote→   Economy + Healthcare cut off
```

**Any business solution must address:**
1. Early Education collapse — the root trigger (78→19)
2. Labor Market Engagement deficit — the economic bottleneck (48→14)
3. Capital access gap — 0% loan flow means businesses die before growing
4. Internet access — without it, everything digital is unavailable

**Existing assets a business can build on:**
- Entrepreneurial energy confirmed (New Business score 73)
- Female workforce above poverty (87%) — capable labor pool available
- Near-universal insurance (93.5%) — customer base can pay
- Very cheap real estate (83.3% affordable) — low operating costs
- Broadband infrastructure investment already active (NELPCO $54M)

---

---

## 5. COMPARATIVE ANALYSIS — WHY DID RICHLAND GO UP?

### Script: [`comparative_analysis.py`](https://github.com/Chinyemba-ck/master-card/blob/main/src/comparative_analysis.py)

Richland Parish went from IGS 48 (2017) to IGS 59 (2025) — a +11 point gain while Franklin fell from 42 to 38 (−4). Both are rural, same state, same size. The 21-point gap in 2025 is not explained by demographics.

### The Single Year That Changed Everything — 2022 → 2023

Richland's IGS jumped **+9 in one year** (50 → 59). The indicator changes that year:

| Indicator | Richland 2022 | Richland 2023 | Change | Franklin 2025 |
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

Franklin has two of these already strong (New Business 73, Female Above Poverty 69) but has collapsed on Early Education (19 vs Richland's 69). This is the missing link.

→ *See [chart 11 — Richland IGS Drivers](https://github.com/Chinyemba-ck/master-card/blob/main/charts/11_richland_igs_drivers.png)*

---

### The 5 Indicators That Diverged Most

These are the indicators where Richland improved and Franklin did not — the direct lessons Franklin can apply:

| Indicator | Franklin 2017 | Franklin 2025 | Richland 2017 | Richland 2025 | Gap (2025) |
|---|---|---|---|---|---|
| Travel Time to Work | 31 | **9** | 17 | **70** | −61 |
| Early Education | 78 | **19** | 26 | **69** | −50 |
| Net Occupancy | 49 | **38** | 46 | **85** | −47 |
| Labor Market Engagement | 48 | **14** | 51 | **58** | −44 |
| Personal Income | 41 | **36** | 30 | **63** | −27 |

Franklin held **higher** scores than Richland on Travel Time, Early Education, and Net Occupancy in 2017. These are not inherent weaknesses — they are constructed failures. Richland built infrastructure that improved them. Franklin did not.

→ *See [chart 12 — Divergence Analysis](https://github.com/Chinyemba-ck/master-card/blob/main/charts/12_divergence_analysis.png)*

---

### Demographic & Economic Snapshot — Franklin vs Richland

(Source: US Census Bureau ACS 2023 estimates)

| Metric | Franklin Parish | Richland Parish | US Average |
|---|---|---|---|
| Population | ~19,600 | ~20,200 | — |
| Median HH Income | **$44,103** | $37,800 | $74,755 |
| Poverty Rate | **19.0%** | 24.1% | 11.5% |
| Black/African Am. | 28.7% | **54.8%** | 13.6% |
| Median Age | 40.2 | 38.1 | 38.9 |
| High School+ | 80.1% | 78.9% | 89.4% |
| Bachelor's+ | 10.2% | **13.1%** | 35.7% |
| Owner-occupied housing | **66.4%** | 63.0% | 64.8% |

**Key insight:** Franklin has *higher* household income and *lower* poverty than Richland. The demographic conditions favor Franklin. Yet Richland's IGS is 21 points higher. The gap is entirely in economic infrastructure: job access (Labor Engagement 58 vs 14), early childcare (Early Education 69 vs 19), and residential stability (Net Occupancy 85 vs 38). These are buildable, not inherited.

→ *See [chart 13 — Comparative Snapshot](https://github.com/Chinyemba-ck/master-card/blob/main/charts/13_comparative_snapshot.png)*

---

### How Franklin Incorporates Richland's Lessons

| Richland's Win | What It Required | Franklin's Position | Actionable Path |
|---|---|---|---|
| Early Education 26→69 | Childcare facility investment, enrollment subsidies | Currently 19 — critical failure | Childcare co-op/center is the single highest-leverage intervention |
| Female Above Poverty 33→65 | Women's workforce programs tied to childcare | Currently 69 — already strong | Maintain; tie childcare solution to women's workforce programs |
| New Businesses 14→68 | Business formation programs, local procurement | Currently 73 — already strong | Capital access (loan gap) is the bottleneck, not formation |
| Travel Time 17→70 | Employer-assisted transit or remote work infrastructure | Currently 9 — worst indicator | Broadband (NELPCO active) + remote-work job placement programs |
| Personal Income 30→63 | Wage growth tied to stable employment | Currently 36 | Follows from solving labor engagement and childcare |

**Bottom line:** Franklin does not need to replicate Richland's full path. It needs to solve childcare (Early Education 19→50+), which unlocks labor engagement, which drives income and net occupancy. The NELPCO broadband build (now complete) is the parallel infrastructure investment that makes remote work viable. Franklin's existing strengths in health insurance, housing, and business formation are the foundation — not the problem.

---

## 6. ADDITIONAL CHARTS (Comparative Analysis)

| Chart | File | What it shows |
|---|---|---|
| 11 | [`charts/11_richland_igs_drivers.png`](https://github.com/Chinyemba-ck/master-card/blob/main/charts/11_richland_igs_drivers.png) | 15-panel grid: year-on-year changes in every Richland indicator 2017–2025. Orange dashed line marks 2023 — the year all 5 key indicators jumped simultaneously. IGS trajectory overlay shows Franklin (red) vs Richland (blue). |
| 12 | [`charts/12_divergence_analysis.png`](https://github.com/Chinyemba-ck/master-card/blob/main/charts/12_divergence_analysis.png) | 5-panel side-by-side trajectories for the indicators that diverged most. Shows Franklin above Richland in 2017 on several, then falling while Richland climbed. |
| 13 | [`charts/13_comparative_snapshot.png`](https://github.com/Chinyemba-ck/master-card/blob/main/charts/13_comparative_snapshot.png) | Left: all 13 IGS indicators side-by-side with gap annotations. Right: Census ACS 2023 demographic table. Highlights the paradox — Franklin's demographics are stronger but IGS is 21 pts lower. |

---

*Scripts: [`analysis.py`](https://github.com/Chinyemba-ck/master-card/blob/main/src/analysis.py) · [`regression_model.py`](https://github.com/Chinyemba-ck/master-card/blob/main/src/regression_model.py) · [`deep_analysis.py`](https://github.com/Chinyemba-ck/master-card/blob/main/src/deep_analysis.py) · [`comparative_analysis.py`](https://github.com/Chinyemba-ck/master-card/blob/main/src/comparative_analysis.py)*
*Charts: [`charts/`](https://github.com/Chinyemba-ck/master-card/tree/main/charts) (13 charts)*
*Data: [Mastercard IGS Tool](https://mastercardcenter.org/inclusive-growth-score/) (7 exports, 2017–2025) · [US Census Bureau ACS](https://www.census.gov/acs/www/) · [Connect Louisiana / NELPCO broadband](https://www.connect.louisiana.gov/news/blog-post/summer-success-series-volt-broadband/) · Louisiana state agencies*
