# GSE193716 Decision Prep v1

## Date
2026-04-07

## Purpose
Prepare structured decision artifacts for GSE193716 query-ready promotion
review. This document does NOT execute a promotion decision — it
organizes the evidence and provisional recommendations so that an
explicit reviewer decision can be made cleanly.

## Inputs
- Registration manifest + sample sheet
- Gene-space audit (87.4% overlap confirmed, GRCh38_tdtomato_10X)
- Conversion report (7/7 H5AD, all verified)
- Projection review (7/7 whole-lung + epithelial complete on v1)
- Existing tranche decision precedents (GSE221343, GSE289846, GSE308817)

---

## Current evidence summary

### All 7 rows passed Gate C (projection smoke test)
- Whole-lung + epithelial projections completed without errors on v1
- All 7 map to **late_GW17_19 / week_18** — same stage as GSE221343 and
  most of GSE289846
- 87.4% gene overlap did not degrade projection quality; alignment scores
  (0.69–0.82) are within or above the range of existing query-ready tranches

### Biology gradient is internally coherent (Gate D partial)

| Group | Epi% | State_fine | Epi OT | Ambiguity | Alignment |
|-------|-----:|------------|-------:|----------:|----------:|
| Primary pre-culture | 94–96% | Budtip progenitors | 4.4–5.7% | 22–33% | 0.70–0.74 |
| Primary cultured | 84–90% | Tip cells / Budtip | 9.9–15.6% | 19–21% | 0.75–0.77 |
| iAEC2 | 98–99% | Proliferating progenitors | 0.9–2.1% | 10–31% | 0.69–0.82 |

Three distinct epithelial states emerge:
1. **Budtip progenitors** — fresh primary AEC2 identity
2. **Tip cells** — culture-shifted primary identity (PL2 only)
3. **Proliferating progenitors** — iPSC-derived iAEC2 identity

---

## What supports eventual promotion

1. **iAEC2 rows are technically strong**: 98–99% epithelial, 0.9–2.1%
   off-target, alignment 0.69–0.82. These metrics match or exceed
   existing query-ready tranches.
2. **Proliferating progenitors replicates cross-dataset**: GSE193716
   iAEC2 3D/insert and +MRC5/insert match GSE289846 3i_Day7 (Kyoto).
   Same state, independent dataset.
3. **Same lab + line as GSE221343**: controlled comparison. GSE221343
   CK+DCI → Stromal-like cells 1; GSE193716 iAEC2 3D → Proliferating
   progenitors. Different state for same line in different culture
   format — biologically interpretable.
4. **Culture-format comparison is unique**: 3D vs 3D/insert vs +MRC5/insert
   produces graded alignment and ambiguity differences. No other tranche
   provides this.
5. **Primary AEC2 would be first adult tissue in the comparison world**:
   novel biology axis not covered by any existing tranche.

## What blocks immediate all-7 promotion

1. **Adult-primary-vs-fetal caveat (primary rows)**: fresh adult AEC2
   mapping to fetal Budtip progenitors is technically interpretable but
   biologically ambiguous. Is this (a) a genuine retained progenitor
   signature, (b) an artifact of limited adult representation in the
   fetal reference, or (c) a closest-neighbor default? Domain judgment
   required — this is outside what the projection can determine.
2. **Cultured primary off-target (9.9–15.6%)**: the two cultured rows
   (GSM5819129, GSM5819130) have epi off-target 2–3x higher than any
   existing query-ready row (max 4.7% in GSE221343). MRC5 co-culture
   likely contributes non-epithelial signal despite EPCAM+ sorting.
3. **Donor effect in cultured primary**: PL2 → Tip, PL1 → Budtip.
   N=1 per condition per donor is insufficient to separate donor effect
   from culture stochasticity.
4. **intended_analysis_role enum**: `primary_benchmark_candidate` is
   not in `data_contract.yaml`. Promoting primary rows would require
   an enum decision.

---

## Options considered

### Option A: promote all 7
- **Pros**: maximizes information; preserves full biology gradient
- **Cons**: promotes adult primary rows whose biological interpretability
  on the fetal reference is unvalidated; promotes cultured rows with
  elevated off-target; mixes fundamentally different evidence quality
  (strong iAEC2 vs uncertain primary)
- **Verdict**: not recommended at this time

### Option B: promote iAEC2 subset (3 rows)
- **Scope**: GSM5819133_iAEC2_3D, GSM5819134_iAEC2_3D_insert,
  GSM5819135_iAEC2_MRC5_insert
- **Pros**: technically strongest subset; no adult-primary caveat; same
  iPSC line as GSE221343 (controlled comparison); Proliferating
  progenitors replicates cross-dataset; culture-format comparison is
  unique and valuable
- **Cons**: loses the primary-vs-iPSC benchmarking value that motivates
  this dataset; primary rows remain in limbo
- **Verdict**: recommended as the most defensible first step

### Option C: hold all 7 as benchmark-only / not query-ready
- **Pros**: avoids any premature commitment; preserves option value
- **Cons**: iAEC2 rows are technically ready and meet all existing
  gates; holding them gains nothing that the evidence doesn't already
  support
- **Verdict**: overly conservative for the iAEC2 subset

---

## Preferred provisional option

**Option B: promote the 3 iAEC2 rows in a first-pass decision, then
revisit the 4 primary rows once the adult-primary-vs-fetal question
has domain-expert input.**

Rationale:
- The iAEC2 rows pass every gate that existing query-ready tranches
  passed (Gate A–D).
- They add unique culture-format comparison value (3D vs insert vs
  +MRC5) that no other tranche provides.
- Proliferating progenitors identity is cross-dataset replicated
  (GSE289846).
- The adult-primary caveat does not apply to iPSC-derived rows.
- Promoting the iAEC2 subset does not block later promotion of the
  primary rows.

---

## Per-row provisional recommendations

| Row | Recommendation | Confidence | Group |
|-----|---------------|------------|-------|
| GSM5819131 primary pre-cult PL2 | hold_pending_biological_review | moderate | primary |
| GSM5819132 primary pre-cult PL1 | hold_pending_biological_review | moderate | primary |
| GSM5819129 primary cultured PL2 | not_recommended_now | low | primary_cultured |
| GSM5819130 primary cultured PL1 | not_recommended_now | low | primary_cultured |
| GSM5819133 iAEC2 3D | candidate_for_subset_promotion | moderate | iAEC2 |
| GSM5819134 iAEC2 3D/insert | candidate_for_subset_promotion | high | iAEC2 |
| GSM5819135 iAEC2 +MRC5/insert | candidate_for_subset_promotion | high | iAEC2 |

### Row-level notes

**Primary pre-culture (hold)**: Technically clean projections
(Epi OT 4.4–5.7%, within existing-tranche range). The blocker is
the adult-primary-vs-fetal biological interpretation question, which
is outside the scope of projection-based evidence. These rows could be
reconsidered after domain-expert input on the Budtip mapping.

**Primary cultured (not recommended now)**: Epi off-target 9.9–15.6%
exceeds all existing query-ready rows (max 4.7%). The MRC5 co-culture
signal is not fully resolvable by EPCAM+ sorting. Donor-level state
divergence (Tip vs Budtip) adds interpretive uncertainty. These rows
need either (a) a lower off-target threshold justification or (b)
acceptance that cultured-primary is inherently noisier.

**iAEC2 (candidate)**: All three are technically ready. 3D/insert
(CG13) is the strongest single row (alignment 0.814, ambiguity 9.9%).
+MRC5/insert (CG14) is nearly as strong (0.819, 15.7%) and adds
co-culture comparison value. 3D Matrigel (CG12) has higher ambiguity
(31.0%) but is the format baseline for comparison.

---

## Missing evidence before final promotion decision

### For iAEC2 subset (if Option B is chosen)
1. **Explicit reviewer sign-off** on the iAEC2 subset promotion
2. **Decision on tranche role**: is GSE193716 a
   `nearest_external_validation` (same lab as GSE221343) or a new role?
   Current placeholder uses `nearest_external_validation`.
3. **decision_log.md entry** for the promotion (D-00XX)
4. **data_contract.yaml update** if a new role enum is needed
5. **Sample sheet update**: query_ready_flag → true for the 3 iAEC2 rows

### For primary rows (if revisited later)
1. **Domain-expert assessment** of "adult AEC2 → fetal Budtip" mapping
2. **Separate decision** on whether primary rows get their own role
   enum (e.g., `primary_benchmark_candidate`)
3. **Cultured-primary off-target threshold** — is 10–16% acceptable
   for this specific use case?
4. **Potential MRC5 deconvolution** — could the off-target fraction be
   analyzed for fibroblast markers?

---

## Explicit stop line

- **query_ready_flag**: NOT changed — all 7 rows remain false
- **decision_log.md**: NOT edited
- **data_contract.yaml**: NOT edited
- **research_scope.md**: NOT edited
- **comparison_world_biology_summary**: NOT edited
- **metadata/external/**: NOT edited

This artifact prepares the decision but does not execute it.

## Files in this directory

| File | Description |
|------|-------------|
| `README.md` | This file |
| `gse193716_decision_prep_v1.tsv` | Per-row decision prep with provisional recommendations (7 rows, 19 columns) |
