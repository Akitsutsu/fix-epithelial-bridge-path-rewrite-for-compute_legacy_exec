# Legacy metric backfill recompute decision v1

## Date
2026-04-09

## Scope
Repo-state decision note. Not a governance change, not a reference
change, not a recompute execution step, not a comparison-world refresh.
No existing artifact is replaced in this step. This note records the
failed extraction pilot result and fixes the recovery lane for the
legacy epithelial backfill.

---

## 1. Why now

The target-surface note (PR #47) fixed the 5-column backfill target.
The extraction pilot then checked whether the 6 local multiroot
`epi_summary` JSONs existed at the exact paths listed in the committed
compare table. Result: 0/6 found. The open question is no longer
availability — it is which recompute lane to use for recovery.

This is a design-sequencing choice, not a criticism of the existing
surfaced world.

## 2. Observed blocker

All 6 local `epi_summary` JSONs are absent from the filesystem:

| row_id | missing path | status |
|--------|-------------|--------|
| CA1 | benchmark_run_gse237359_vs_CA1_CA1_compute/epithelial/CA1/CA1_epi_summary_v1.json | missing |
| BU3 | benchmark_run_gse237359_vs_BU3_BU3_compute/epithelial/BU3/BU3_epi_summary_v1.json | missing |
| G237359_15934 | benchmark_run_gse237359_vs_G237359_15934_G237359_15934_compute/epithelial/G237359_15934/G237359_15934_epi_summary_v1.json | missing |
| G237359_16011 | benchmark_run_gse237359_vs_G237359_16011_G237359_16011_compute/epithelial/G237359_16011/G237359_16011_epi_summary_v1.json | missing |
| G237359_16392 | benchmark_run_gse237359_vs_G237359_16392_G237359_16392_compute/epithelial/G237359_16392/G237359_16392_epi_summary_v1.json | missing |
| G237359_16402 | benchmark_run_gse237359_vs_G237359_16402_G237359_16402_compute/epithelial/G237359_16402/G237359_16402_epi_summary_v1.json | missing |

No staging TSV was created. No commit, push, or PR was made in the
failed pilot step.

## 3. Decision: preserve multiroot provenance

Legacy epithelial backfill recovery for these 6 rows will preserve
multiroot provenance. The recovery lane, if executed later, is an
explicit rerun of the legacy multiroot epithelial stage for exactly
these 6 rows against frozen reference v1.

This step does not execute that rerun. This step does not switch
these rows to combined-root.

## 4. Rationale

- The committed compare table and tranche README define multiroot as
  the stable / reproducible lane for this legacy tranche
- The GSE237359 tranche README explicitly says combined-root compute
  is intentionally excluded
- Current comparison-world v3 also excludes combined-root compute for
  GSE237359
- Preserving multiroot provenance minimizes scope and avoids mixing
  metric recovery with execution-lane migration
- Whether multiroot rerun will be straightforward depends on input
  availability (H5AD files, reference, legacy scripts) — this note
  does not overclaim feasibility

## 5. Explicit deferral

Combined-root migration for CA1/BU3/GSE237359 is deferred. It is a
separate future design/policy decision. It is not decided in this note.
This note does not make combined-root canonical for legacy rows.

## 6. Affected rows

Affected rows remain exactly:

- CA1
- BU3
- G237359_15934
- G237359_16011
- G237359_16392
- G237359_16402

No row expansion. GSE221342 rows remain excluded from this backfill
lane (they already have symmetric metrics).

## 7. Next execution step

1. Merge this decision note
2. Inspect committed manifests, command templates, and input paths
   needed for a safe legacy multiroot epithelial rerun for these 6 rows
3. Only if that execution surface is sufficiently grounded, run a tiny
   recompute pilot for the same 6-row lane
4. Extract the 5 existing epithelial columns from the new outputs
5. Only after successful recompute + extraction, refresh comparison-world
   and lifecycle surfaces

No execution in this step. No refresh in this step.

---

## 8. Explicit stop line

- data_contract.yaml: not changed
- decision_log.md: not changed
- research_scope.md: not changed
- Accepted tranche statuses: not changed
- reports/comparison_world_biology_summary_v3/: not changed
- reports/artifact_lifecycle_registry_v2/: not changed
- reports/prediction_registry_v1/: not changed
- No new TSV/XLSX in this step
- No recompute execution in this step
- No combined-root migration in this step
