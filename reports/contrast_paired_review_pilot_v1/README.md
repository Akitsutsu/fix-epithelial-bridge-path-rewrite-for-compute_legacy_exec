# Contrast paired-review pilot v1

## Date
2026-04-10

## Scope
Non-canonical pilot artifact. Not a governance change, not a reference
change, not a comparison-world refresh, not a lifecycle refresh, not a
prediction refresh, not a contrast-registry expansion. No existing
artifact is replaced in this step.

This pilot tests whether contrast-aware row grouping adds enough
interpretive value beyond row-first summaries to justify future work.
It is a decision aid only.

---

## What this pilot is

A single TSV with 9 member-level rows covering the 3 existing contrast
registry skeleton entries:

| Contrast | Type | Member rows | Tranche |
|----------|------|------------|---------|
| C-0001 | paired_perturbation | 2 (WT_YAP, YAP5SA) | GSE221344 |
| C-0002 | directional_gradient | 4 (iAT2_3D, iAT1_3D, iAT1_ALI_p0, iAT1_ALI_p1) | GSE221342 |
| C-0003 | matched_format_series | 3 (iAEC2_3D, iAEC2_3D_insert, iAEC2_MRC5_insert) | GSE193716 |

## What this pilot is NOT

- Not a canonical artifact — does not modify or replace any
  comparison-world, lifecycle, or prediction surface.
- Not a new contrast-registry expansion — uses only existing
  C-0001, C-0002, C-0003 skeleton entries.
- Not a paired-review template canonization step.
- Not a row-first summary replacement.

## Data sourcing

All biology values are sourced from existing canonical or accepted
review artifacts:

| Source | Used for |
|--------|----------|
| `comparison_world_biology_summary_v4.tsv` | Row-level epithelial metrics for all 9 member rows |
| `gse221344_projection_review_v1.tsv` | Supplementary detail for C-0001 rows |
| `gse193716_projection_review_v1.tsv` | Supplementary detail for C-0003 rows |
| `gse221342_query_ready_decisions_v1.tsv` | Supplementary detail for C-0002 rows |
| `contrast_registry_v1.tsv` | Contrast metadata (matching_basis, axis_primary, axis_secondary, member roles) |

No values were re-computed. No values were inferred from prose where
a grounded artifact existed.

## Human gate defaults applied

| Gate | Choice | Effect |
|------|--------|--------|
| 1 (wording) | **1b** | "shows a directional shift toward alveolar commitment"; no stronger causal phrasing |
| 2 (thresholds) | **2b** | Thresholds in README prose only, not in TSV; qualitative language in TSV |
| 3 (GSE221344) | **3a** | GSE221344 remains supportive-only; not upgraded beyond partial positive-arm |

## Indicative thresholds (not encoded in TSV)

The TSV uses qualitative language ("without large worsening of
epithelial off-target or ambiguity"). For evaluation guidance:

- Off-target worsening ≤ 10 percentage points relative to matched
  baseline is considered acceptable.
- Ambiguity ≤ 60% is considered acceptable.

These are indicative, not hard rules. They may be refined in future
work based on actual data distributions across contrasts.

## Pilot findings summary

### C-0001: partial positive-arm, not confirmatory
YAP5SA shows directional CFTR+ enrichment (5.6% SOX2lowCFTR+ vs
0.06% in WT-YAP) but top state remains Proliferating progenitors.
This is supportive but not confirmatory of alveolar commitment
direction. Reviewer confidence: moderate.

### C-0002: clearest directional gradient
Monotonic gradient from Budtip progenitors (iAT2 baseline) to
SOX2lowCFTR+ cells (78.0% at ALI p1). Off-target and ambiguity both
improve along the gradient. This is the strongest within-tranche
evidence that directed conditions show a directional shift toward
alveolar commitment. Reviewer confidence: high.

### C-0003: format-only null confirmed
All 3 format conditions retain Proliferating progenitors. Insert
improves resolution (ambiguity 31.0 → 9.9) without shifting identity.
+MRC5 co-culture has minimal effect. This confirms the null
expectation: format-only variation does not drive commitment shift.
Reviewer confidence: high.

## Does contrast-aware grouping add value?

**Tentative yes**, primarily through C-0002 and C-0003:

- The C-0002 monotonic gradient is substantially more informative as a
  grouped 4-point series than as 4 independent rows. The directional
  shift, improving quality metrics, and cross-line replication are
  visible only in the contrast framing.
- The C-0003 format-only null is important for P-0002 falsification
  logic. Grouping the 3 rows clarifies that format variation does not
  produce the same shift as directed differentiation.
- C-0001 adds less contrast-specific value — the supportive partial
  signal is already captured in P-0001 and the comparison-world
  narrative memo. However, the paired framing does make the
  YAP5SA / WT-YAP comparison more explicit.

Whether this is sufficient to justify a broader contrast-review layer
is a future decision.

## Files in this directory

| File | Description |
|------|-------------|
| `README.md` | This file |
| `contrast_paired_review_pilot_v1.tsv` | Paired/matched review pilot (9 rows, 15 columns, 3 contrasts) |
