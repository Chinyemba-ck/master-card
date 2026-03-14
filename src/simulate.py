"""
simulate.py — HealthScore what-if scenarios for Franklin Parish.

═══════════════════════════════════════════════════════════════
INDICATOR AUDIT — Number rationale for every target
All 17 IGS indicators assessed. Each number below is justified
by data from the IGS exports, Richland comparison, or external
program evidence. Indicators not touched are held at baseline.
═══════════════════════════════════════════════════════════════

RIDGE COEFF KEY (what moves IGS the most):
  Park Land +3.69 | CommDiversity +2.81 | RealEstate +2.53
  SpendPC   +2.27 | FemAbvPov     +2.09 | NetOcc     +1.93
  LaborEng  +1.44 | HealthIns     -1.41 | SmlBizLoan +1.25
  EarlyEd   +1.13 | NewBiz        +1.10 | Income     +0.83
  TravelTime +0.76 | InternetAcc  -0.73 | Gini       +0.64
  AffHousing +0.40 | MinWomenBiz  +0.27

───────────────────────────────────────────────────────────────
ECONOMY PILLAR — HealthScore's core levers
───────────────────────────────────────────────────────────────

Small Business Loans [current=44, Ridge coeff=+1.25]
  Phase 1: 44 -> 55
    Rationale: HealthScore improves provider financial profile
    (billing cycles, reimbursement rates, denial rates) making
    them eligible for SELAHEC Rural Loan Fund ($10K-$350K,
    start-ups eligible, ruralhealthinfo.org/funding/5965) and
    SBA Community Advantage loans. +11 pts in Year 1 is
    conservative — SELAHEC has an active rolling application.
  Phase 2: 55 -> 60
    Rationale: 50+ providers now scored; lender familiarity with
    HealthScore metrics reduces friction. Approaching the 66
    capital floor shared by all 3 IGS 60+ tracts in our dataset.
  Phase 3: 60 -> 66
    Rationale: 66 is not arbitrary — ALL 3 high-scoring tracts
    (Fresno 5805=70, Fresno 3104=60, Dallas=60) score exactly 66
    on Small Biz Loans. This is the empirically-observed capital
    floor for IGS 60+ communities. HealthScore is built to
    reach this number.

Commercial Diversity [current=36, Ridge coeff=+2.81]
  Phase 1: 36 -> 50
    Rationale: Score was 62 in 2024, crashed to 36 when capital
    flow stopped (loan growth 0% in 2024-2025). This is a
    REVERSAL of a recent collapse, not new growth from scratch.
    HealthScore keeps existing providers open + SELAHEC startup
    loans enable new healthcare business types to launch.
    +14 pts to partially recover toward 2024 level is realistic.
  Phase 2: 50 -> 65
    Rationale: With 50-100 providers scored and capital flowing,
    more types of health-enabling businesses sustain. Childcare,
    dental, mental health, pharmacy, home care all represented.
  Phase 3: 65 -> 80
    Rationale: Richland Parish = 21 (lower than Franklin — they
    are less diverse). 60+ avg = 97. 80 is a mid-path target,
    not the ceiling. Franklin has the entrepreneurial base (New
    Biz=73) — HealthScore provides the financial stability.

Min/Women Owned Businesses [current=15, Ridge coeff=+0.27]
  Phase 1: 15 -> 30
    Rationale: Childcare centers and mental health practices are
    majority minority/women-owned nationally. Franklin's 2.1%
    ownership rate (score=15) vs base 4.1% is a 2x gap.
    HealthScore stabilizes these businesses financially.
    +15 pts doubles the ownership rate to ~4%, reaching base.
  Phase 2: 30 -> 50
    Rationale: Second cohort onboarded; capital access through
    SBA Community Advantage specifically for underserved markets.
    Richland = 82 (long-term benchmark, not Year 2 target).
  Phase 3: 50 -> 67
    Rationale: Richland = 82; 67 is 2/3 of the way there.
    5-year horizon is realistic for this demographic shift.
    Note: Low Ridge coeff (+0.27) means this contributes less
    to IGS than Commercial Diversity — don't over-claim.

Labor Market Engagement [current=14, Ridge coeff=+1.44]
  Phase 1: HELD at 14 (no change)
    Rationale: This is an INDIRECT effect with a 1-2 year lag.
    Healthcare businesses need to be financially stable before
    they hire more staff. Year 1 is too early to claim.
  Phase 2: 14 -> 20
    Rationale: By Year 2-3, stabilized childcare centers allow
    women to re-enter workforce. Richland's 2023 proof: when
    Early Education jumped +22, Female Poverty dropped +32,
    and Labor Engagement rose together. Conservative +6 pts
    (not +16 like Richland) because Franklin's deficit is
    deeper (14 vs Richland's starting point of ~32).
  Phase 3: 20 -> 35
    Rationale: Remote healthcare admin/billing jobs via RHTP
    add to the labor base. 35 is still well below Richland's
    58 or the 60+ avg of 70 — deliberately conservative.

New Businesses [current=73, Ridge coeff=+1.10]
  All phases: HELD at 73 (no change claimed)
    Rationale: Franklin already scores 73, ABOVE Richland (68)
    and 60+ avg (64). HealthScore does not need to create new
    businesses — it sustains existing ones. Score may drift up
    slightly as providers formalize, but we do not claim credit.
    This is a STRENGTH, not a target.

───────────────────────────────────────────────────────────────
COMMUNITY PILLAR — Indirect chain effects
───────────────────────────────────────────────────────────────

Early Education [current=19, Ridge coeff=+1.13]
  Phase 1: 19 -> 28
    Rationale: Childcare centers are a primary HealthScore
    target. Score was 78 in 2017 — this is a fixable collapse,
    not a structural ceiling. +9 pts recovers ~15% of the
    2017-2025 decline. Richland jumped +22 in one year (2023)
    when childcare investment was made — we claim a smaller,
    slower +9 for Year 1 because HealthScore financial stability
    is a prerequisite, not a direct enrollment driver.
  Phase 2: 28 -> 35
    Rationale: More financially stable centers open more slots.
    60+ avg = 23 (already below current 19, meaning the
    benchmark is low). Richland = 69. 35 is modest.
  Phase 3: 35 -> 39
    Rationale: Regional expansion brings more childcare into
    neighboring parishes, increasing supply. Plateau effect
    expected — 39 is realistic without a major public subsidy.

Personal Income [current=36, Ridge coeff=+0.83]
  Phase 1: HELD at 36
    Rationale: Income follows employment; too early for Year 1.
  Phase 2: 36 -> 40
    Rationale: Healthcare staff wages begin to show up in
    aggregate income data. +4 pts is minimal — reflects 50-100
    provider employees earning modest wages.
  Phase 3: 40 -> 48
    Rationale: As labor engagement rises to 35, more residents
    earn wages. Richland = 56; 48 is 2/3 of the way there.

Female Above Poverty [current=69, Ridge coeff=+2.09]
  Phase 1: HELD at 69
    Rationale: Richland's 2023 jump showed Female Poverty moved
    simultaneously with Early Education and New Businesses —
    it's an outcome of childcare opening, not a Year 1 effect.
  Phase 2: 69 -> 75
    Rationale: Childcare access allows women to work. Richland
    jumped this indicator +32 in 2023 when childcare expanded.
    Conservative +6 for Year 2-3. High Ridge coeff (+2.09)
    means even a small improvement has meaningful IGS impact.
  Phase 3: 75 -> 80
    Rationale: Sustained employment path. Franklin already beats
    Richland here (69 vs 65) — we are building on a strength,
    not closing a gap. 80 is conservative ceiling.

Spending per Capita [current=50, Ridge coeff=+2.27]
  Phase 1: HELD at 50
    Rationale: Spending follows income — too early for Year 1.
  Phase 2: 50 -> 58
    Rationale: As personal income rises and providers stabilize,
    local spending increases. High Ridge coeff (+2.27) means
    this matters. +8 pts is modest given income lag.
  Phase 3: 58 -> 65
    Rationale: Full labor engagement chain matures.
    60+ avg = 68; 65 is within striking distance.

Gini Coefficient [current=42, Ridge coeff=+0.64]
  All phases: HELD at 42
    Rationale: Income equality is a slow-moving structural
    indicator. HealthScore does not directly redistribute income.
    Improvement would take 10+ years. Low coeff anyway.

Health Insurance [current=59, Ridge coeff=-1.41]
  All phases: HELD at 59
    Rationale: NEGATIVE Ridge coefficient — adding insurance
    coverage actually correlates with LOWER IGS in this dataset
    (artifact: high-insurance tracts are poor rural areas).
    Franklin is already at 93.5% coverage rate. Do not target.

───────────────────────────────────────────────────────────────
PLACE PILLAR — Infrastructure & slow-moving structural factors
───────────────────────────────────────────────────────────────

Internet Access [current=2, Ridge coeff=-0.73]
  Phase 1: HELD at 2 (no HealthScore credit)
    Rationale: NELPCO/Volt $54M fiber build — this is
    infrastructure, not HealthScore. Negative Ridge coeff
    (-0.73) means the model does not reward this in IGS terms
    (artifact of rural tracts having low internet AND low IGS).
    HealthScore deploys ON TOP of this infrastructure.
  Phase 2: 2 -> 35
    Rationale: NELPCO/Volt build fully live by 2025. 35 is
    conservative — Volt targeted 11,000 homes/businesses.
    Labeled as infrastructure contribution in all presentations.
  Phase 3: 35 -> 70
    Rationale: Full coverage + digital adoption grows over time.
    Richland = 3 (same as Franklin — proves internet is not the
    IGS driver; we include it for completeness not credit).

Net Occupancy [current=38, Ridge coeff=+1.93]
  Phase 1: HELD at 38
    Rationale: Population decline (-9.9%/yr) is a lagging
    indicator. Jobs must appear before people stop leaving.
    Cannot claim this in Year 1.
  Phase 2: HELD at 38
    Rationale: Even with jobs emerging in Year 2-3, population
    stabilization takes longer than the labor market response.
  Phase 3: 38 -> 50
    Rationale: Remote healthcare jobs + stable providers create
    reasons to stay. +12 pts moves from -9.9%/yr decline toward
    stabilization. Still below Richland (85) — realistic 5-year
    ceiling. High coeff (+1.93) means this has significant
    IGS impact when it does move.

Real Estate Value [current=46, Ridge coeff=+2.53]
  Phase 1-2: HELD at 46
    Rationale: Property values follow population and income —
    the slowest-moving indicator. Cannot claim in Years 1-3.
  Phase 3: 46 -> 58
    Rationale: As Net Occupancy stabilizes and income rises,
    property values begin recovery. +12 pts in Years 4-5.
    High coeff (+2.53) — worth capturing even a small move.
    Richland = 72; 58 is modest progress toward that.

Travel Time to Work [current=9, Ridge coeff=+0.76]
  Phase 1: HELD at 9
    Rationale: Remote work takes time to establish.
  Phase 2: HELD at 9
    Rationale: Remote healthcare admin jobs (RHTP pipeline)
    begin to appear but not yet at scale.
  Phase 3: 9 -> 20
    Rationale: RHTP remote healthcare jobs reduce commute need
    for a portion of workers. HealthScore platform creates
    billing/admin roles that are fully remote. +11 pts is
    modest. Richland = 70 (long-term structural gap —
    rural geography limits how far this can move).

Affordable Housing [current=56, Ridge coeff=+0.40]
  All phases: HELD at 56
    Rationale: Franklin already scores 56, above Richland (72)
    on affordability. Low coeff (+0.40). Not a HealthScore lever
    and not a priority gap. Hold steady.

Park Land [current=19, Ridge coeff=+3.69]
  All phases: HELD at 19
    Rationale: Highest Ridge coefficient in the model (+3.69)
    but COMPLETELY outside HealthScore's scope. Physical
    infrastructure requiring municipal investment. Do not claim.
    Note for judges: this coefficient inflates the model's
    apparent sensitivity — it is not actionable for HealthScore.

═══════════════════════════════════════════════════════════════
SUMMARY TABLE — All targets with rationale codes
  D = Direct HealthScore action
  I = Indirect chain effect
  X = Infrastructure / out of scope / held
═══════════════════════════════════════════════════════════════
  Indicator            Current  Ph1  Ph2  Ph3  Type  Key rationale
  Small Biz Loans         44    55   60   66    D    SELAHEC+SBA capital; 66=60+ floor
  Commercial Diversity    36    50   65   80    D    2024 collapse reversal; SELAHEC startups
  Min/Women Biz           15    30   50   67    D    Childcare/MH practices stabilized
  Early Education         19    28   35   39    D    Childcare centers open more slots
  Labor Mkt Engagement    14    14   20   35    I    Childcare->women work chain (Richland proof)
  Personal Income         36    36   40   48    I    Follows labor engagement
  Female Above Poverty    69    69   75   80    I    Richland +32 in 2023 when childcare expanded
  Spending per Capita     50    50   58   65    I    Follows income (coeff +2.27 — high impact)
  Net Occupancy           38    38   38   50    I    Jobs -> population stabilizes (slow, 4-5 yr)
  Real Estate Value       46    46   46   58    I    Follows net occupancy (slow, 4-5 yr)
  Travel Time to Work      9     9    9   20    I    Remote RHTP jobs reduce commute burden
  Internet Access          2     2   35   70    X    NELPCO/Volt infrastructure (not HealthScore)
  New Businesses          73    73   73   73    X    Already strong (73>Richland 68) — maintain
  Affordable Housing      56    56   56   56    X    Already above Richland; not a priority gap
  Gini Coefficient        42    42   42   42    X    Too slow to move; low coeff
  Health Insurance        59    59   59   59    X    NEGATIVE coeff; Franklin 93.5% — do not target
  Park Land               19    19   19   19    X    Highest coeff but out of scope entirely
═══════════════════════════════════════════════════════════════
"""

import numpy as np


# ── Scenario definitions ─────────────────────────────────────────────────────
# Every number here matches the rationale documented above.

PHASE1 = {
    # DIRECT — HealthScore Year 1, 20 providers onboarded
    'Small Biz Loans':      55,   # +11: SELAHEC rolling applications; HealthScore score -> loan eligibility
    'Commercial Diversity': 50,   # +14: Partial recovery from 2024 crash (62->36); capital stops the bleeding
    'Min/Women Biz':        30,   # +15: Childcare/MH practices reach ~4% ownership (national base rate)
    'Early Education':      28,   # +9:  Childcare centers financially stable = more open slots; 15% recovery of 2017 level
    # All other indicators held at baseline — see rationale above
}

PHASE2 = {
    **PHASE1,
    # DIRECT — improved further with 50-100 providers
    'Small Biz Loans':      60,   # +5 from Ph1: lender familiarity; approaching 66 capital floor
    'Commercial Diversity': 65,   # +15 from Ph1: more health-enabling business types sustained
    'Min/Women Biz':        50,   # +20 from Ph1: second cohort; SBA Community Advantage pipeline
    'Early Education':      35,   # +7 from Ph1: more slots as more centers financially stable
    # INDIRECT — chain effects with 1-2 year lag
    'Labor Mkt Engagement': 20,   # +6 from baseline: childcare->women work chain; conservative lag
    'Personal Income':      40,   # +4 from baseline: healthcare staff wages begin appearing
    'Female Above Poverty': 75,   # +6 from baseline: Richland jumped +32 in 2023; conservative +6 for 2-3 yr
    'Spending per Capita':  58,   # +8 from baseline: income rises -> local spending rises (coeff +2.27)
    # INFRASTRUCTURE — NELPCO/Volt fully live (not HealthScore credit)
    'Internet Access':      35,   # NELPCO/Volt build complete; labeled separately in all presentations
}

PHASE3 = {
    **PHASE2,
    # DIRECT — regional scale, 100+ providers
    'Small Biz Loans':      66,   # Hit the empirical 60+ capital floor (all 3 IGS 60+ tracts = exactly 66)
    'Commercial Diversity': 80,   # Richland-level; Franklin has entrepreneurial base (New Biz=73) to support this
    'Min/Women Biz':        67,   # 2/3 path to Richland (82); 5-year horizon is realistic
    'Early Education':      39,   # Plateau effect; 60+ avg=23, Richland=69; 39 without major public subsidy
    # INDIRECT — full chain maturity
    'Labor Mkt Engagement': 35,   # +15 from Ph2: remote RHTP healthcare jobs add to labor base
    'Personal Income':      48,   # +8 from Ph2: 2/3 path to Richland (56)
    'Female Above Poverty': 80,   # +5 from Ph2: building on Franklin's existing strength (already > Richland 65)
    'Spending per Capita':  65,   # +7 from Ph2: approaching 60+ avg (68)
    'Net Occupancy':        50,   # +12 from baseline: population stabilizes as jobs appear (slow; 4-5 yr lag)
    'Real Estate Value':    58,   # +12 from baseline: follows net occupancy recovery (slow; high coeff +2.53)
    'Travel Time to Work':  20,   # +11 from baseline: remote RHTP admin/billing jobs reduce commute need
    # INFRASTRUCTURE — mature
    'Internet Access':      70,   # NELPCO/Volt full coverage + digital adoption growth
}

SCENARIOS = {
    'Phase 1 — Year 1  (HealthScore direct levers)':      PHASE1,
    'Phase 2 — Yr 2-3  (indirect chain + capital floor)': PHASE2,
    'Phase 3 — Yr 4-5  (regional scale + full chain)':    PHASE3,
}


def _apply(baseline, overrides, feature_names, df_model):
    row = baseline.copy()
    row.update(overrides)
    return np.array([row.get(f, df_model[f].median()) for f in feature_names]).reshape(1, -1)


def run_simulations(ridge, rf, gb, scaler, baseline, franklin_vec, feature_names, df_model, actual_igs):
    """Run current baseline + all 3 scenarios. Print and return results dict."""
    pred_current = {
        'Ridge': ridge.predict(scaler.transform(franklin_vec))[0],
        'RF':    rf.predict(franklin_vec)[0],
        'GB':    gb.predict(franklin_vec)[0],
    }

    print("=" * 55)
    print("FRANKLIN PARISH -- WHAT-IF SIMULATION")
    print("=" * 55)
    print(f"\n  Actual IGS 2025:   {actual_igs}")
    print(f"  Ridge prediction:  {pred_current['Ridge']:.1f}")
    print(f"  RF    prediction:  {pred_current['RF']:.1f}")
    print(f"  GB    prediction:  {pred_current['GB']:.1f}")

    results = {'current': pred_current}

    for name, overrides in SCENARIOS.items():
        vec = _apply(baseline, overrides, feature_names, df_model)
        preds = {
            'Ridge': ridge.predict(scaler.transform(vec))[0],
            'RF':    rf.predict(vec)[0],
            'GB':    gb.predict(vec)[0],
        }
        avg = np.mean(list(preds.values()))
        print(f"\n  {name}")
        print(f"    Ridge: {pred_current['Ridge']:.1f} -> {preds['Ridge']:.1f}  ({preds['Ridge']-pred_current['Ridge']:+.1f})")
        print(f"    RF:    {pred_current['RF']:.1f} -> {preds['RF']:.1f}  ({preds['RF']-pred_current['RF']:+.1f})")
        print(f"    GB:    {pred_current['GB']:.1f} -> {preds['GB']:.1f}  ({preds['GB']-pred_current['GB']:+.1f})")
        print(f"    Ensemble avg: {avg:.1f}")
        results[name] = preds

    return results


def sensitivity_analysis(rf, franklin_vec, pred_current_rf, feature_names):
    """For each indicator: +20 pts, measure IGS gain via RF."""
    sensitivity = {}
    for j, feat in enumerate(feature_names):
        test = franklin_vec.copy()
        test[0, j] = min(test[0, j] + 20, 100)
        delta = rf.predict(test)[0] - pred_current_rf
        sensitivity[feat] = delta
    return sensitivity
