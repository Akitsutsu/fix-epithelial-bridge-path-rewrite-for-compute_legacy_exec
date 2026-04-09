# Contrast registry design note v1

## Date
2026-04-09

## Scope
Repo-state design note. Not a governance change, not a reference change,
not an implementation PR. No existing artifact is replaced in this step.
This note proposes a minimal schema and sequencing plan for a future
contrast-first extension to the current row/tranche comparison world.

---

## 1. Why now

The current row/tranche-centric design has worked well. It supports
reproducible intake, gate-based review, and versioned comparison-world
summaries. Nothing here criticizes that foundation.

However, certain evidence forms that now recur are awkward to express
in row-only artifacts:

- **Paired perturbation** (GSE221344): the 100x CFTR+ enrichment in
  YAP5SA is only meaningful relative to WT-YAP. The pair was promoted
  together, but the comparison-world summary records them as two
  independent rows.
- **Matched format series** (GSE221342): iAT2 3D -> iAT1 3D -> ALI p0
  -> ALI p1 is a monotonic gradient. The four rows together define one
  interpretive axis, but the summary treats each as standalone.
- **Culture-format comparison** (GSE193716 iAEC2): 3D vs insert vs
  +MRC5 are matched conditions. Their within-tranche coherence was
  evaluated during review but is not captured in a normalized form.
- **Cross-tranche replication** (SOX2lowCFTR+ across GSE221343,
  GSE289846, GSE221342): the state replicates across 3 lines and 2
  labs, but this is narrated in memos rather than structured as a
  queryable fact.

This is a design-sequencing issue: the existing infrastructure is
correct but incomplete for contrast-level evidence.

## 2. Design goal

Add a normalized layer for paired, matched, and directional evidence
without replacing the current tranche governance. The contrast registry
would sit alongside (not above) the existing comparison-world summary,
lifecycle registry, and prediction registry.

It should handle:
- paired perturbations (control vs treatment)
- matched culture-format series (baseline -> condition1 -> condition2)
- within-tranche directional evidence (monotonic gradients)
- cross-tranche replication statements (same state, different lines/labs)

---

## 3. Proposed minimal contrast registry schema

All fields below are **proposed**. None are canonical until implemented
and logged in a future decision.

| Field | Type | Description |
|-------|------|-------------|
| contrast_id | string | Unique ID (e.g., C-0001) |
| contrast_type | enum | `paired_perturbation`, `matched_format_series`, `cross_tranche_replication`, `directional_gradient` |
| tranche_ids | list | Source tranche(s); single-element for within-tranche contrasts, multi-element for cross-tranche replication |
| member_row_ids | list | All row IDs in the contrast unit |
| control_row_ids | list | Control/baseline row IDs (if applicable) |
| comparison_row_ids | list | Treatment/comparison row IDs |
| matching_basis | string | What is held constant (e.g., "same line, same medium, same timepoint") |
| axis_primary | string | Primary variable (e.g., "YAP transgene", "culture format") |
| axis_secondary | string | Secondary variable if present |
| expected_direction | string | What the contrast is expected to show |
| observed_direction_summary | string | What was actually observed |
| supports_prediction_id | string | P-0001 etc., or "none" |
| evidence_scope | string | `within_tranche`, `cross_tranche`, `cross_lab` |
| current_status | string | `proposed`, `accepted`, `superseded` |
| notes | string | Free text |

**What stays in existing row-level artifacts:** per-row gate results,
per-row top calls, per-row off-target/ambiguity/alignment. The contrast
registry records the *relationship between rows*, not the rows themselves.

---

## 4. Proposed paired/matched evidence unit review TSV format

For future review artifacts that evaluate contrasts (not just individual
rows), the minimum fields would be:

| Field | Description |
|-------|-------------|
| contrast_unit_id | Links to contrast registry |
| member_row_id | One row per member |
| member_role | `control`, `treatment`, `baseline`, `condition_N` |
| matching_basis | What is held constant |
| axis_primary | Primary variable |
| axis_secondary | Secondary variable |
| whole_lung_top_state_fine | Per-row top call |
| epithelial_top_state_fine | Per-row top call |
| epithelial_lineage_off_target_fraction | Per-row metric |
| epithelial_ambiguous_fraction | Per-row metric |
| contrast_delta_note | What changed between control and comparison |
| control_interpretability_note | Caveats on the control row |
| reviewer_confidence | Per-row confidence |
| provisional_recommendation | Per-row recommendation |
| rationale | Per-row rationale |

This differs from current row-only review TSVs by adding `member_role`,
`contrast_delta_note`, and explicit linkage to the contrast unit. Current
gate-based fields (gate_a through gate_d) would still be evaluated per
row; the contrast layer adds the between-row comparison.

This is a **proposed future format**, not yet canonical.

---

## 5. Legacy tranche uniform metric backfill plan

Current accepted tranches have uneven metric surfaces. Specifically:

| Tranche | WL metrics | Epi metrics | Symmetric? |
|---------|:---:|:---:|:---:|
| CA1/BU3 | yes | **no** | no |
| GSE237359 | yes | **no** | no |
| GSE221343 | yes | yes | yes |
| GSE289846 | yes | yes | yes |
| GSE308817 | yes | yes | yes |
| GSE193716 iAEC2 | yes | yes | yes |
| GSE221344 | yes | yes | yes |
| GSE221342 | yes | yes | yes |

Before contrast-aware summaries can be meaningful, the metric surface
should be as uniform as possible. Proposed phases:

**Phase 0 — Inventory.** Enumerate which accepted rows lack symmetric
epi-remap metrics. Currently: CA1/BU3 (2 rows) and GSE237359 (4 rows)
= 6/24 rows (25%).

**Phase 1 — Define target surface.** Agree on the minimum per-row
metric set: whole_lung_top_stage, whole_lung_top_state, epi_top_state,
epi_off_target, epi_ambiguity, epi_alignment. This is already the
de facto standard for post-GSE221343 tranches.

**Phase 2 — Backfill where source allows.** For CA1/BU3 and GSE237359,
check whether the multiroot projection outputs contain enough
information to extract epi-remap-equivalent metrics. If yes, backfill
with explicit annotation ("backfilled from multiroot outputs"). If not,
retain NA with annotation ("epi-remap metrics unavailable; multiroot
path does not produce symmetric epi summary").

**Phase 3 — Contrast-aware summaries.** Only after the metric surface
is reasonably uniform, introduce contrast-level comparison tables that
reference the per-row metrics.

This preserves current accepted artifacts. No silent recomputation.
Backfill improves comparability without rewriting history.

---

## 6. Worked examples

### GSE221344 as paired perturbation

| Field | Value |
|-------|-------|
| contrast_id | C-0001 (proposed) |
| contrast_type | paired_perturbation |
| tranche_ids | [GSE221344] |
| member_row_ids | GSM6858857_WT_YAP, GSM6858858_YAP5SA |
| control_row_ids | GSM6858857_WT_YAP |
| comparison_row_ids | GSM6858858_YAP5SA |
| matching_basis | same line (SPC2-ST-B2), same medium (CK+DCI), same timepoint (7d) |
| axis_primary | YAP transgene (WT vs constitutively active) |
| expected_direction | YAP5SA enriches CFTR+ lineage relative to WT-YAP |
| observed_direction_summary | 100x SOX2lowCFTR+ enrichment (5.6% vs 0.06%); partial shift, not identity conversion |
| supports_prediction_id | P-0001 (supportive, not confirmatory) |
| evidence_scope | within_tranche |

### GSE221342 as matched format-series / boundary-stress

| Field | Value |
|-------|-------|
| contrast_id | C-0002 (proposed) |
| contrast_type | directional_gradient |
| tranche_ids | [GSE221342] |
| member_row_ids | GSM6858850_iAT2_3D, GSM6858851_iAT1_3D, GSM6858852_iAT1_ALI_p0, GSM6858853_iAT1_ALI_p1 |
| control_row_ids | GSM6858850_iAT2_3D |
| comparison_row_ids | GSM6858851_iAT1_3D, GSM6858852_iAT1_ALI_p0, GSM6858853_iAT1_ALI_p1 |
| matching_basis | same line (BU3 NGAT), same lab |
| axis_primary | iAT1 differentiation (CKDCI -> LDCI) |
| axis_secondary | culture format (3D -> ALI) |
| expected_direction | iAT1 differentiation shifts toward SOX2lowCFTR+; ALI may enhance |
| observed_direction_summary | monotonic gradient: Budtip 24.5% -> SOX2lowCFTR+ 60.9% -> 56.8% -> 78.0% |
| supports_prediction_id | none (cross-line, not same-line P-0001) |
| evidence_scope | within_tranche |

### GSE193716 iAEC2 as matched culture-format

| Field | Value |
|-------|-------|
| contrast_id | C-0003 (proposed) |
| contrast_type | matched_format_series |
| tranche_ids | [GSE193716] |
| member_row_ids | GSM5819133_iAEC2_3D, GSM5819134_iAEC2_3D_insert, GSM5819135_iAEC2_MRC5_insert |
| control_row_ids | GSM5819133_iAEC2_3D |
| comparison_row_ids | GSM5819134_iAEC2_3D_insert, GSM5819135_iAEC2_MRC5_insert |
| matching_basis | same line (SPC2-ST-B2), same differentiation stage |
| axis_primary | culture format (3D vs insert vs +MRC5) |
| expected_direction | format affects alignment/ambiguity but retains Proliferating progenitors |
| observed_direction_summary | all 3 Proliferating progenitors; insert best aligned (0.814); +MRC5 minimal effect |
| supports_prediction_id | P-0001 (culture-format-only arm) |
| evidence_scope | within_tranche |

These examples do not change the current accepted/promoted status of
any tranche. They illustrate how existing evidence would map to the
proposed schema.

---

## 7. Recommendation / sequencing

**What to do now:** merge this design note. It fixes the schema proposal
and sequencing plan without changing any governance or implementation.

**What to do next (in order):**
1. Implement a tiny contrast registry skeleton (one TSV, proposed
   entries only)
2. Backfill legacy metric surface for CA1/BU3 and GSE237359 (Phase 0-2)
3. Only then introduce contrast-aware comparison-world summaries

**What not to do now:**
- Do not retrofit everything at once
- Do not change current governance first
- Do not rebuild the reference in this step
- Do not treat this design note as canonical policy

---

## 8. Explicit stop line

- data_contract.yaml: not changed
- decision_log.md: not changed
- research_scope.md: not changed
- Accepted tranche statuses: not changed
- Comparison world: not changed
- No new registry implementation in this step
- No backfill execution in this step
- No paired-review TSV template created in this step
