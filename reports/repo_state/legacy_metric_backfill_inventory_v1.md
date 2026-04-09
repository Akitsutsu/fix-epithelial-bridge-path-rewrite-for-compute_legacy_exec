# Legacy metric backfill inventory v1

## Date
2026-04-09

## Scope
Repo-state inventory note. Not a governance change, not a reference
change, not a backfill execution step, not a comparison-world refresh.
No existing artifact is replaced in this step. This note inventories
the exact rows, missing fields, and candidate source availability before
any backfill work begins.

---

## 1. Why now

The contrast registry skeleton (PR #45) is merged. The design note's
sequencing calls for legacy metric backfill before contrast-aware
summaries. Before executing any backfill, the denominator, affected
rows, candidate sources, and surface-definition ambiguities should be
fixed in a single inventory document.

## 2. Surface boundary / denominator reconciliation

Two row pools exist and must be distinguished:

| Pool | Rows | Components | Description |
|------|-----:|----------:|-------------|
| Current surfaced world (v3) | 20 | 7 | Published in `comparison_world_biology_summary_v3/` |
| Broader accepted/promoted pool | 24 | 8 | Includes GSE221342 (4 rows, D-0015) not yet surfaced in v3 |

The 6 asymmetric rows (lacking epi decision-TSV-format metrics) are the
same in both pools: CA1, BU3, and the 4 GSE237359 donor-resolved rows.
The 4 additional GSE221342 rows have full symmetric metrics and do not
require backfill — they only need a comparison-world refresh (v4) to be
surfaced, which is a separate step.

**6/20 rows in the current surfaced world lack epi metrics.**
**6/24 rows in the broader accepted pool lack epi metrics.**
The affected rows are the same either way.

## 3. Exact affected-row inventory

| row_id | component | WL fields | Epi eligible | Epi stage/state/OT/ambig | Candidate source | Key caveat |
|--------|-----------|:---------:|:------------:|:------------------------:|-----------------|------------|
| CA1 | anchor | yes | 88.5% | **all NA** | multiroot epi_summary JSON path in compare table | run-root path; not a committed repo artifact |
| BU3 | anchor | yes | 98.2% | **all NA** | multiroot epi_summary JSON path in compare table | run-root path; not a committed repo artifact |
| G237359_15934 | GSE237359 | yes | 100.0% | **all NA** | multiroot epi_summary JSON path in compare table | run-root path; not a committed repo artifact |
| G237359_16011 | GSE237359 | yes | 100.0% | **all NA** | multiroot epi_summary JSON path in compare table | run-root path; low cell count (261) |
| G237359_16392 | GSE237359 | yes | 100.0% | **all NA** | multiroot epi_summary JSON path in compare table | run-root path; not a committed repo artifact |
| G237359_16402 | GSE237359 | yes | 100.0% | **all NA** | multiroot epi_summary JSON path in compare table | run-root path; not a committed repo artifact |

All 6 rows have whole-lung metrics (stage, state, off-target) and
epithelial eligibility fractions in the current published summary.
All 6 lack: `epithelial_top_stage_coarse`, `epithelial_top_stage_fine`,
`epithelial_top_state_fine`, `epithelial_lineage_off_target_fraction`,
`epithelial_ambiguous_fraction`.

## 4. Source artifact assessment

The committed multiroot compare table
(`gse237359_vs_CA1_BU3_key_metrics_multiroot.tsv`) lists an
`epi_summary` column with JSON file paths for all 6 rows. These paths
point to run-root directories (e.g.,
`benchmark_run_gse237359_vs_CA1_CA1_compute/epithelial/CA1/CA1_epi_summary_v1.json`).

**These run-root paths are not committed repo artifacts.** They are
local-only projection outputs from the original multiroot validation
run. If those local run directories still exist on the machine where
the original run was executed, the epi_summary JSONs could be read
to extract the missing metrics. If they do not exist, the metrics
would need to be recomputed — which means re-running the multiroot
epithelial stage for these 6 rows.

The committed compare table itself is a stable repo artifact. The
epi_summary JSON file contents are not.

Combined-root compute for CA1/BU3/GSE237359 remains non-canonical.
The multiroot collector path was used for these tranches.

## 5. Metric-surface definition gap

| Column | Current v3 surface | Design note Phase 1 target |
|--------|:------------------:|:--------------------------:|
| whole_lung_top_stage | yes | yes |
| whole_lung_top_state | yes | yes |
| epithelial_top_state | **NA for 6 rows** | yes |
| epithelial_off_target | **NA for 6 rows** | yes |
| epithelial_ambiguity | **NA for 6 rows** | yes |
| epithelial_alignment | **not in v3 schema** | **yes (proposed)** |

The first 5 columns are already defined in the v3 summary schema.
The 6th (`epi_alignment`) is proposed in the design note but does not
exist in any current summary version. Whether to add `epi_alignment`
as part of backfill or defer it to a later schema extension is a
Phase 1 decision point that is **not resolved in this inventory note**.

## 6. Recommendation / sequencing

1. **Merge this inventory note.** It fixes the denominator, affected
   rows, and source-availability assessment without changing anything.
2. **Decide the minimal target backfill surface.** Two options:
   - (a) Fill only the 5 existing v3 columns for the 6 rows
   - (b) Fill the 5 existing columns plus add `epi_alignment`
   - Option (a) is lower-friction; option (b) aligns with the
     design note target but introduces a schema change
3. **Execute a tiny backfill pilot** limited to those 6 rows, using
   whichever source is available (local run-root JSONs if they exist,
   or re-run if not).
4. **Only after successful backfill**, refresh lifecycle and
   comparison-world surfaces.

Do not backfill in this step. Do not refresh comparison world in
this step. Do not refresh lifecycle registry in this step. Do not
change prediction registry in this step.

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
