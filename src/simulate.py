"""
simulate.py — HealthScore what-if scenarios for Franklin Parish.

═══════════════════════════════════════════════════════════════════════════
EVIDENCE BASE — Two complementary analyses ground every number below
═══════════════════════════════════════════════════════════════════════════

1. FRANKLIN'S OWN HISTORY (2017-2025)
   What Franklin's indicators looked like when it scored 42 (its best):
     Small Biz Loans:    74  (2017), 72  (2018)  — current 44
     Early Education:    78  (2017), 55  (2018), 65 (2020) — current 19
     Labor Engagement:   48  (2017), 46  (2018)  — current 14
   Franklin has BEEN at these levels. Phase 1-2 targets are restorations,
   not aspirations.

   Franklin year-on-year IGS moves, what drove them:
     2018->2019  IGS -4: Small Biz Loans -42 (72->30) — loans crash = IGS crash
     2019->2020  IGS +4: Small Biz Loans +17 (30->47) — loans recover = IGS recovers
     2020->2021  IGS -8: Loans -22 AND Early Education -44 — double collapse
     2021->2022  IGS +2: Loans +26 — loans alone partially recover IGS
     2022->2023  IGS +3: Loans +9 — incremental loan improvement
     2023->2024  IGS -4: Loans -16; CommDiv spiked 62 but did NOT prevent drop
     2024->2025  IGS +3: CommDiv crashed -26; New Businesses drove recovery

   KEY LESSON: In Franklin's data, Small Biz Loans and Early Education
   are the proven IGS levers. CommDiv was never high in the 42-IGS years.

2. RICHLAND CORRELATION ANALYSIS (what drives Richland's IGS 59)
   Pearson r with Richland IGS across 9 years:
     Personal Income     r=+0.943  <- strongest
     Labor Engagement    r=+0.911
     Female Poverty      r=+0.901
     Travel Time         r=+0.852
     Net Occupancy       r=+0.827
     Early Education     r=+0.712
     Real Estate         r=+0.683
     Comm Diversity      r=+0.419  <- weak
     Small Biz Loans     r=-0.231  <- NEGATIVE (Richland's loans fell as IGS rose)
     Internet Access     r=-0.379  <- NEGATIVE

   What Richland locked in at 2025 (sustained at all-time highs):
     Early Education:  69  | Labor Engagement: 58 | Female Poverty: 65
     Net Occupancy:    85  | Personal Income:  56 | Travel Time:    70
   These 6 indicators explain Richland staying at IGS 58-59.

   Richland's 2023 breakout (+9 in one year):
     Early Education +22, Female Poverty +32, New Businesses +54,
     Personal Income +16, Travel Time +19
     -> Chain: childcare -> women work -> income -> businesses stay

   CRITICAL INSIGHT: Small Biz Loans and CommDiv do NOT drive Richland's
   IGS. The real drivers are Labor/Income/Education/Occupancy — the
   human economic chain, not the business finance chain directly.

═══════════════════════════════════════════════════════════════════════════
REVISED INDICATOR ATTRIBUTION — grounded in both datasets
═══════════════════════════════════════════════════════════════════════════

FRANKLIN HISTORY CORRELATION WITH IGS (r across 9 years):
  New Businesses      r=+0.802 | Early Education  r=+0.776
  Labor Engagement    r=+0.729 | Small Biz Loans  r=+0.720
  Internet Access     r=+0.694 | Travel Time      r=+0.628

  NOTE: In Franklin, CommDiv has r=-0.426 with IGS (negative! — CommDiv
  was highest in 2024 when IGS was 35). Do not claim CommDiv as primary
  lever in Franklin-specific framing.

RIDGE COEFF (cross-tract model, 63 obs):
  Park Land +3.69 | CommDiversity +2.81 | RealEstate +2.53
  SpendPC   +2.27 | FemAbvPov     +2.09 | NetOcc     +1.93
  LaborEng  +1.44 | HealthIns     -1.41 | SmlBizLoan +1.25
  EarlyEd   +1.13 | NewBiz        +1.10 | Income     +0.83
  TravelTime +0.76 | InternetAcc  -0.73 | Gini       +0.64
  AffHousing +0.40 | MinWomenBiz  +0.27

  NOTE: CommDiversity has high Ridge coeff (+2.81) but this is
  cross-tract signal, not Franklin-specific. Use Ridge for magnitude
  estimates; use historical Franklin correlation for causal narrative.

───────────────────────────────────────────────────────────────────────────
ECONOMY PILLAR
───────────────────────────────────────────────────────────────────────────

Small Business Loans [current=44, Franklin r=+0.720, Ridge coeff=+1.25]
  Phase 1: 44 -> 55
    Franklin history: was 72-74 in 2017-18. 55 is partial restoration.
    Mechanism: HealthScore financial profile (billing, reimbursement,
    denial rates) -> SELAHEC Rural Loan Fund ($10K-$350K, start-ups
    eligible, ruralhealthinfo.org/funding/5965) + SBA Community Advantage.
    PROOF: Franklin at 30 (2019) recovered to 47 in one year, 60 in 2023.
    +11 pts is well within Franklin's demonstrated recovery range.
  Phase 2: 55 -> 62
    Lender familiarity with HealthScore scores reduces friction.
    Franklin had 60 in 2023 already — this is not new ground.
  Phase 3: 62 -> 66
    66 = empirical capital floor for all 3 IGS 60+ tracts in dataset.
    Richland sits at 50 (not the loan driver for IGS) — we target 66
    because that is what Fresno+Dallas have, not to match Richland.

Commercial Diversity [current=36, Franklin r=-0.426, Ridge coeff=+2.81]
  Phase 1: 36 -> 42
    REVISED DOWN from 50. Franklin correlation with IGS is NEGATIVE
    (-0.426) — CommDiv was highest (62) in 2024 when IGS was 35.
    Richland's CommDiv is only 21 (lower than Franklin!) and IGS=59.
    Framing: HealthScore keeps providers open, modestly reversing the
    2024->2025 crash (62->36). Claim partial recovery to 42, not 50.
  Phase 2: 42 -> 52
    Some new healthcare business types launch with startup capital.
    Ridge coeff high (+2.81) justifies including this — but per
    Franklin's own data this is NOT the primary lever.
  Phase 3: 52 -> 65
    Regional scale; Ridge cross-tract signal supports this ceiling.
    Present as "structural improvement driven by diverse provider base"
    not as the primary IGS driver.

Min/Women Owned Businesses [current=15, Ridge coeff=+0.27]
  Phase 1: 15 -> 25
    REVISED DOWN from 30. Childcare/MH practices (majority women-owned)
    stabilized financially -> survive, grow, register formally.
    +10 pts moves from 2.1% to ~3% ownership rate (national base=4.1%).
  Phase 2: 25 -> 45
    Second cohort + SBA Community Advantage for underserved markets.
  Phase 3: 45 -> 60
    5-year horizon. Richland=82 is long-term benchmark; 60 is midway.
    Low Ridge coeff (+0.27) — this contributes less to IGS directly.

Labor Market Engagement [current=14, Franklin r=+0.729, Ridge coeff=+1.44]
  Phase 1: HELD at 14
    1-2 year lag before childcare -> women work chain appears in data.
    Franklin was at 48 in 2017 — we know this is reversible.
  Phase 2: 14 -> 28
    REVISED UP from 20. Richland proof: Labor Engagement r=+0.911 with
    its IGS. Franklin's own history: was 48 in 2017. Childcare expansion
    (Early Ed 19->32) enables women to re-enter workforce. 28 is still
    well below Franklin's 2017 level of 48.
  Phase 3: 28 -> 42
    REVISED UP from 35. Remote RHTP healthcare admin/billing jobs add to
    labor base. 42 is close to Franklin's 2017 level (48) and approaching
    Richland 2025 (58). This is a PRIMARY IGS lever — Richland r=+0.91.

New Businesses [current=73, Franklin r=+0.802, Ridge coeff=+1.10]
  All phases: HELD at 73
    Franklin already ABOVE Richland (68) and 60+ avg (64). This is a
    STRENGTH. Note: Franklin's r=+0.802 — when New Businesses was high
    (2023: 73), IGS was 39; in 2024 New Biz collapsed to 16, IGS=35.
    This volatility (73->16->73 in 3 years) suggests it is a lagging
    signal of business survival, not a direct HealthScore lever.

───────────────────────────────────────────────────────────────────────────
COMMUNITY PILLAR
───────────────────────────────────────────────────────────────────────────

Early Education [current=19, Franklin r=+0.776, Ridge coeff=+1.13]
  Phase 1: 19 -> 30
    REVISED UP from 28. Franklin was at 78 (2017), 55 (2018), 65 (2020).
    The current 19 is a constructed collapse, not a structural limit.
    Richland Proof: jumped +22 in one year (2023) when childcare invested.
    We claim +11 for Year 1 — half of what Richland achieved in one year.
    Mechanism: HealthScore stabilizes childcare centers financially ->
    they stay open, add slots, attract enrollment.
  Phase 2: 30 -> 42
    REVISED UP from 35. Franklin's own 2020 level was 65. Richland
    r=+0.71 — this feeds directly into labor and income chain.
    More financially stable centers = more open slots. 42 is still well
    below Franklin's 2020 level (65) and Richland 2025 (69).
  Phase 3: 42 -> 55
    REVISED UP from 39. Richland is at 69; 55 is a realistic 5-year
    target given Franklin's proven 65 in 2020. This is RESTORATION.

Personal Income [current=36, Richland r=+0.943, Ridge coeff=+0.83]
  Phase 1: HELD at 36
    Income follows employment; too early for Year 1.
  Phase 2: 36 -> 43
    REVISED UP from 40. Richland r=+0.943 — strongest single Richland
    driver. Healthcare staff at stabilized providers earn wages.
    Richland jumped Personal Income +16 in 2023 when labor chain fired.
    Conservative +7 for Year 2-3.
  Phase 3: 43 -> 52
    REVISED UP from 48. As labor engagement reaches 42, more residents
    earn wages. Richland=56; 52 is close. This is a PRIMARY indicator
    for reaching Richland-level IGS — r=0.94 in Richland's data.

Female Above Poverty [current=69, Richland r=+0.901, Ridge coeff=+2.09]
  Phase 1: HELD at 69
    Outcome of childcare chain; 1-2 year lag.
  Phase 2: 69 -> 75
    Childcare access allows women to work. Richland jumped +32 in 2023.
    Conservative +6 for Year 2-3. Franklin already beats Richland (65).
    High Ridge coeff (+2.09) — meaningful IGS impact from small gain.
  Phase 3: 75 -> 80
    Building on existing strength. 80 is conservative given Richland
    r=+0.901 and Franklin's starting advantage.

Spending per Capita [current=50, Ridge coeff=+2.27]
  Phase 1: HELD at 50
  Phase 2: 50 -> 58
    Follows income chain. High Ridge coeff (+2.27) — even modest gain
    has meaningful model impact. +8 pts reflects 50-100 employed workers.
  Phase 3: 58 -> 65
    Full labor chain matures. 60+ tract avg = 68; 65 approaches it.

Gini Coefficient [current=42, Ridge coeff=+0.64]
  All phases: HELD at 42
    Structural inequality indicator; 10+ year horizon. Low coeff.

Health Insurance [current=59, Ridge coeff=-1.41]
  All phases: HELD at 59
    NEGATIVE Ridge coefficient. Franklin=93.5% coverage — do not target.

───────────────────────────────────────────────────────────────────────────
PLACE PILLAR
───────────────────────────────────────────────────────────────────────────

Internet Access [current=2, Richland r=-0.379, Ridge coeff=-0.73]
  Phase 1: HELD at 2
    NELPCO/Volt $54M fiber — not HealthScore. ALSO: in Richland's data,
    Internet Access has NEGATIVE correlation with IGS (-0.379). Richland
    went from 8 -> 3 as IGS rose 48->59. Label clearly as infrastructure.
  Phase 2: 2 -> 35
    NELPCO/Volt build live by 2025. Infrastructure contribution only.
  Phase 3: 35 -> 70
    Full adoption growth. Not a HealthScore credit line.

Net Occupancy [current=38, Richland r=+0.827, Ridge coeff=+1.93]
  Phase 1: HELD at 38
    Population stabilization lags job creation by 2-3 years.
  Phase 2: 38 -> 42
    REVISED UP slightly — Richland r=+0.827 confirms this matters.
    Jobs emerging in Year 2-3 begin to slow outmigration.
  Phase 3: 42 -> 52
    REVISED UP from 50. Remote healthcare jobs + stable providers create
    reasons to stay. Richland=85 (peak). 52 is realistic 5-year target.
    High Ridge coeff (+1.93) — population stabilization has strong IGS
    impact when it does move.

Real Estate Value [current=46, Richland r=+0.683, Ridge coeff=+2.53]
  Phase 1-2: HELD at 46
    Slowest-moving indicator. Follows net occupancy and income.
  Phase 3: 46 -> 58
    As net occupancy stabilizes and income rises, property values recover.
    Richland r=+0.683 — moderate relationship. +12 pts in Years 4-5.
    High Ridge coeff (+2.53) makes even a small move meaningful.

Travel Time to Work [current=9, Richland r=+0.852, Ridge coeff=+0.76]
  Phase 1: HELD at 9
  Phase 2: 9 -> 18
    REVISED UP from held. Richland r=+0.852 — 4th strongest Richland
    driver. Remote RHTP healthcare admin/billing jobs begin to reduce
    commute burden. Richland went from 24 (2021) to 70 (2023) in 2 years.
    Cautious +9 for Year 2-3 given Franklin's structural geography gap.
  Phase 3: 18 -> 28
    Remote-work adoption grows. Note: Travel Time r=+0.628 in Franklin
    too. This is a real lever — Richland's clearest evidence.
    Richland=70; 28 is very conservative given the Richland trajectory.

Affordable Housing [current=56, Ridge coeff=+0.40]
  All phases: HELD at 56
    Above Richland; not a priority gap. Low coeff.

Park Land [current=19, Ridge coeff=+3.69]
  All phases: HELD at 19
    Highest Ridge coeff but completely out of HealthScore's scope.
    Municipal infrastructure investment required. Do not claim.

═══════════════════════════════════════════════════════════════════════════
FINAL SCENARIO TABLE — revised numbers with dual evidence base
  D = Direct HealthScore | I = Indirect chain | X = Infrastructure/OOS
  F-corr = Franklin 9yr correlation | R-corr = Richland 9yr correlation
═══════════════════════════════════════════════════════════════════════════
  Indicator            Cur  Ph1  Ph2  Ph3  Type  F-corr  R-corr  Key rationale
  Small Biz Loans       44   55   62   66    D    +0.72   -0.23   Franklin restoration (was 74); SELAHEC
  Early Education       19   30   42   55    D    +0.78   +0.71   Franklin restoration (was 78/65); childcare
  Labor Mkt Eng         14   14   28   42    I    +0.73   +0.91   Richland's #2 driver; childcare chain lag
  Personal Income       36   36   43   52    I    -0.66   +0.94   Richland's #1 driver; follows labor chain
  Female Above Pov      69   69   75   80    I    -0.71   +0.90   Richland's #3 driver; Franklin already strong
  Net Occupancy         38   38   42   52    I    +0.24   +0.83   Richland's #5 driver; jobs->people stay
  Travel Time to Work    9    9   18   28    I    +0.63   +0.85   Richland's #4 driver; remote RHTP jobs
  Spending per Cap      50   50   58   65    I    N/A     N/A     Follows income (Ridge +2.27)
  Real Estate Value     46   46   46   58    I    -0.15   +0.68   Follows net occupancy (slow; Ridge +2.53)
  Comm Diversity        36   42   52   65    D    -0.43   +0.42   NOT a Franklin IGS driver; modest recovery
  Min/Women Biz         15   25   45   60    D    -0.99   -0.54   New ground; low Ridge coeff (+0.27)
  Internet Access        2    2   35   70    X    +0.69   -0.38   NELPCO/Volt infra; Richland fell as IGS rose
  New Businesses        73   73   73   73    X    +0.80   +0.15   Strength; volatile (73->16->73); hold
  Affordable Housing    56   56   56   56    X    N/A     N/A     Already strong; low coeff
  Gini Coefficient      42   42   42   42    X    N/A     N/A     Structural; 10+ yr horizon
  Health Insurance      59   59   59   59    X    N/A     N/A     Negative Ridge coeff; 93.5% coverage
  Park Land             19   19   19   19    X    N/A     N/A     Highest Ridge coeff; out of scope
═══════════════════════════════════════════════════════════════════════════
"""

import numpy as np


# ── Scenario definitions ─────────────────────────────────────────────────────
# Every number matches the evidence-base documented above.
# Franklin history + Richland correlation = dual validation per indicator.

PHASE1 = {
    # DIRECT — HealthScore Year 1, ~20 providers onboarded
    'Small Biz Loans':      55,   # Franklin restoration: was 72-74 in 2017-18; SELAHEC pipeline
    'Commercial Diversity': 42,   # Modest crash recovery (62->36->42); NOT a primary Franklin lever
    'Min/Women Biz':        25,   # Childcare/MH practices reach ~3% ownership (up from 2.1%)
    'Early Education':      30,   # Franklin restoration: was 78/65; Richland gained +22 in 1 yr
    # All other indicators held — see rationale above
}

PHASE2 = {
    **PHASE1,
    # DIRECT — 50-100 providers scored
    'Small Biz Loans':      62,   # Franklin had 60 in 2023 already; approaching 66 capital floor
    'Commercial Diversity': 52,   # New healthcare types sustained; Ridge coeff high but F-corr negative
    'Min/Women Biz':        45,   # Second cohort + SBA Community Advantage
    'Early Education':      42,   # Franklin had 65 in 2020; Richland r=+0.71; childcare expansion
    # INDIRECT — chain effects with 1-2 year lag; Richland-validated
    'Labor Mkt Engagement': 28,   # Richland r=+0.91; childcare->women work chain; Franklin was 48 in 2017
    'Personal Income':      43,   # Richland r=+0.94; Richland jumped +16 in 2023 when chain fired
    'Female Above Poverty': 75,   # Richland r=+0.90; Richland +32 in 2023; Franklin already strong (69)
    'Spending per Capita':  58,   # Follows income; Ridge coeff +2.27
    'Net Occupancy':        42,   # Richland r=+0.83; jobs emerging slow outmigration
    'Travel Time to Work':  18,   # Richland r=+0.85; remote RHTP jobs begin reducing commute burden
    # INFRASTRUCTURE — NELPCO/Volt fully live (not HealthScore)
    'Internet Access':      35,   # NELPCO/Volt; Richland's internet FELL as IGS rose — label separately
}

PHASE3 = {
    **PHASE2,
    # DIRECT — regional scale, 100+ providers
    'Small Biz Loans':      66,   # Empirical 60+ capital floor (Fresno+Dallas all score exactly 66)
    'Commercial Diversity': 65,   # Ridge cross-tract signal; provider base diversified at scale
    'Min/Women Biz':        60,   # Midway to Richland (82); 5-year horizon
    'Early Education':      55,   # Franklin had 65 in 2020; Richland=69; 55 is realistic restoration
    # INDIRECT — full chain maturity; primary Richland-validated drivers
    'Labor Mkt Engagement': 42,   # Richland r=+0.91; approaching Franklin's 2017 level (48); RHTP jobs
    'Personal Income':      52,   # Richland r=+0.94; Richland=56; approaching parity
    'Female Above Poverty': 80,   # Richland r=+0.90; building on Franklin's existing strength
    'Spending per Capita':  65,   # 60+ tract avg=68; within reach
    'Net Occupancy':        52,   # Richland r=+0.83; Richland=85; 52 is conservative 5-year target
    'Real Estate Value':    58,   # Richland r=+0.68; follows net occupancy (slow; high Ridge coeff)
    'Travel Time to Work':  28,   # Richland r=+0.85; Richland=70; 28 is very conservative
    # INFRASTRUCTURE — mature
    'Internet Access':      70,   # NELPCO/Volt full coverage + digital adoption
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
