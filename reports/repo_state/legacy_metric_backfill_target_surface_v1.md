# Legacy metric backfill target surface v1

## Date
2026-04-09

## Scope
Repo-state decision note. Not a governance change, not a reference
change, not a backfill execution step, not a comparison-world refresh.
No existing artifact is replaced in this step. This note fixes the
Phase 1 target surface for the legacy metric backfill pilot.

---

## 1. Why now

The backfill inventory (PR #46) identified 6 affected rows and flagged
a Phase 1 ambiguity: whether to target the 5 existing v3 columns only,
or to also add `epi_alignment` as a new column. Before executing any
backfill pilot, this choice must be made explicitly.

## 2. Decision: option A

**Phase 1 minimal target backfill surface is limited to the 5 epithelial
fields already present in `comparison_world_biology_summary_v3.tsv`.**

The target columns are:

1. `epithelial_top_stage_coarse`
2. `epithelial_top_stage_fine`
3. `epithelial_top_state_fine`
4. `epithelial_lineage_off_target_fraction`
5. `epithelial_ambiguous_fraction`

These are the same columns that post-GSE221343 tranches already populate.
The backfill pilot will recover values for these 5 columns only, for the
6 affected rows only.

## 3. Explicit deferral

`epi_alignment` is deferred. No new summary column is introduced in
this step. No compact summary schema expansion. No README / lifecycle /
prediction surface refresh.

Reasons for deferral:
- `epi_alignment` does not exist in the current v3 schema
- Adding it would be a schema extension, not a value recovery
- The backfill pilot should be limited to recovering values for
  already-defined fields, not mixing recovery with schema changes

## 4. Affected rows

The backfill pilot is limited to these 6 rows:

| row_id | component |
|--------|-----------|
| CA1 | anchor |
| BU3 | anchor |
| G237359_15934 | GSE237359 |
| G237359_16011 | GSE237359 |
| G237359_16392 | GSE237359 |
| G237359_16402 | GSE237359 |

The 4 GSE221342 rows (GSM6858850-53) are **not** part of this backfill
pilot. They already have full symmetric metrics and will enter the
comparison world through a separate refresh (v4), not through backfill.

## 5. Rationale

- Preserves current v3 schema without modification
- Avoids mixing metric recovery with schema extension
- Keeps the pilot limited to value recovery for already-defined fields
- Lowers risk before any comparison-world v4 refresh
- If `epi_alignment` is later needed, it can be added as a separate
  schema-extension step after the pilot succeeds

## 6. Next execution step

1. Merge this decision note
2. Check whether the 6 local multiroot `epi_summary` JSON files still
   exist at the run-root paths listed in the committed compare table
3. If they exist: run a tiny extraction pilot — read each JSON, extract
   the 5 target fields, produce a backfill-ready TSV for the 6 rows
4. If they do not exist: stop and report the exact missing paths and
   whether recomputation of the multiroot epithelial stage is needed
5. Only after a successful pilot, refresh comparison-world and
   lifecycle surfaces

No execution in this step. No refresh in this step.

---

## 7. Explicit stop line

- data_contract.yaml: not changed
- decision_log.md: not changed
- research_scope.md: not changed
- Accepted tranche statuses: not changed
- reports/comparison_world_biology_summary_v3/: not changed
- reports/artifact_lifecycle_registry_v2/: not changed
- reports/prediction_registry_v1/: not changed
- No backfill execution in this step
- No new TSV/XLSX in this step
