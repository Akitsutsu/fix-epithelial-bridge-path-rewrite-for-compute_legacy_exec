# Contrast-aware summary reassessment v1

## Date
2026-04-10

## Scope
Repo-state reassessment note. Not a governance change, not a reference
change, not a comparison-world refresh, not a lifecycle refresh, not a
prediction refresh, not an implementation PR. No existing artifact is
replaced in this step.

---

## 1. Why now

PR #51 merged the canonical surface refresh that completed the legacy
6-row epithelial backfill lane. The 5 target columns
(`epithelial_top_stage_coarse`, `epithelial_top_stage_fine`,
`epithelial_top_state_fine`, `epithelial_lineage_off_target_fraction`,
`epithelial_ambiguous_fraction`) are now populated for all 20 rows in
comparison world v3.

The open question is no longer "which rows lack metrics" but "should
contrast-aware summary migration start now?" This note fixes the
answer.

This is a sequencing and boundary decision, not a criticism of the
current v3 surface or the contrast registry design.

## 2. Current stable state

| Surface | Version | Status |
|---------|---------|--------|
| Comparison world | v3 | 20 rows, 7 tranche components, all 25 columns populated |
| Lifecycle registry | v2 | 7 tranches, all current |
| Prediction registry | v1 | 1 prediction (P-0001), registered/supportive |
| Contrast registry | v1 skeleton | 3 proposed entries (C-0001, C-0002, C-0003), non-canonical |

Key facts:
- All 20 rows now have the 5-column epithelial surface populated.
- The 6 legacy rows (CA1, BU3, G237359_15934, G237359_16011,
  G237359_16392, G237359_16402) were backfilled from multiroot
  rerun outputs via `legacy_metric_backfill_pilot_v1.tsv`.
- Multiroot provenance for CA1/BU3/GSE237359 is retained.
- Combined-root migration for those rows remains deferred.
- `epi_alignment` remains deferred (not in current v3 schema).
- No accepted tranche statuses were changed.

## 3. What changed in substance

The forcing asymmetry that justified the legacy backfill lane — 6
rows with NA in all epithelial columns while 14 rows were fully
populated — is now resolved at the 5-column level. The current
row-first summary is symmetric enough to stand on its own as the
canonical comparison-world surface.

The contrast registry exists as a proposed, non-canonical side layer
with only 3 worked-example entries (C-0001 GSE221344, C-0002
GSE221342, C-0003 GSE193716 iAEC2). No contrast entry covers the
anchor or GSE237359 rows. No contrast entry has been accepted or
promoted. No comparison-world summary has ever referenced contrast
entries.

This is enough to remove urgency: the row-first summary is complete
and symmetric. It is not enough to force migration: the contrast
layer has not demonstrated value beyond the design note.

## 4. Remaining open questions

1. **Whether contrast-aware comparison-world summaries are worth
   adding now.** The 3 skeleton entries illustrate the schema but
   have not been reviewed, validated, or connected to any canonical
   decision.

2. **Whether paired/matched review TSV artifacts should exist before
   any summary migration.** Current review artifacts are row-level
   only. A contrast-aware summary that references unreviewed contrast
   entries would invert the normal review-before-summary order.

3. **Whether `epi_alignment` should remain deferred or become part of
   a future schema extension.** It was explicitly deferred during the
   backfill target-surface decision and was not adopted in the
   backfill or refresh. Adding it would be a schema extension, not a
   value recovery.

4. **Whether CA1/BU3/GSE237359 should migrate from multiroot to
   combined-root provenance.** The tranche README and compare table
   define multiroot as the stable lane. Migration would change the
   execution provenance for 6 rows and should be a separate decision.

5. **Whether P-0001 cross-tranche closure assessment should happen
   before any contrast-aware surface change.** P-0001 remains
   registered/supportive. GSE221344 provided directional but not
   confirmatory evidence. A closure assessment would consume the
   existing contrast entries without requiring a canonical migration.

## 5. Decision: do not start canonical contrast-aware migration now

**Recommendation: keep the current canonical surfaces stable.**

Specifically:
- Do not create comparison_world_biology_summary_v4 now.
- Do not create artifact_lifecycle_registry_v3 now.
- Do not widen the canonical surface with contrast-level columns.
- Do not adopt `epi_alignment` now.
- Do not migrate CA1/BU3/GSE237359 to combined-root now.
- Keep prediction registry v1 unchanged.

**Rationale:**
- No forcing asymmetry remains in the row-first summary.
- The contrast layer is still proposed and minimal (3 entries, none
  accepted).
- Open interpretive questions remain (paired review, P-0001 closure,
  combined-root migration).
- Canonical migration should follow demonstrated value, not precede
  it.

## 6. What could happen later

If future work is desired, the only acceptable next implementation
lane is a **tiny non-canonical contrast-aware pilot**. That pilot, if
ever undertaken, should:

- Live outside the canonical comparison-world surface (e.g., a
  separate reports directory, not inside `comparison_world_biology_summary_v3/`).
- Use only the existing contrast registry skeleton entries (C-0001,
  C-0002, C-0003).
- Not replace or modify row-first summaries.
- Serve as a decision aid for whether the contrast layer adds
  enough value to justify a future canonical migration.
- Not expand the contrast registry without a preceding review step.

This note does not design that pilot fully. It only bounds the
acceptable scope if one is ever attempted.

---

## 7. Explicit stop line

- reports/comparison_world_biology_summary_v3/: not changed
- reports/artifact_lifecycle_registry_v2/: not changed
- reports/prediction_registry_v1/: not changed
- reports/contrast_registry_v1/: not changed
- data_contract.yaml: not changed
- decision_log.md: not changed
- research_scope.md: not changed
- No new v4 / v3 version directories
- No new canonical summary schema
- No `epi_alignment` adoption in this step
- No combined-root migration in this step
- No paired-review TSV template in this step
- No new implementation in this step
