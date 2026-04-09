# Legacy metric backfill execution readiness v1

## Date
2026-04-10

## Scope
Repo-state execution-readiness note. Not a governance change, not a
reference change, not a recompute execution step, not a comparison-world
refresh. No existing artifact is replaced in this step. This note
inspects what is grounded for a safe legacy multiroot rerun vs what
still depends on unresolved prerequisites.

---

## 1. Why now

The recompute decision note (PR #48) fixed the recovery lane to legacy
multiroot provenance. The next question is no longer policy — it is
whether the execution surface is grounded enough to run safely. This
note separates committed artifacts from local-only prerequisites for
the 6-row lane.

## 2. Committed execution surface

| Artifact | Present | Role in rerun |
|----------|:-------:|---------------|
| epithelial_cmd_template_compute_legacy_v1.txt | yes | epithelial rerun command template |
| whole_lung_cmd_template_compute_legacy_v1.txt | yes | whole-lung rerun command template |
| epithelial_only_remap_common_v2.py | yes | epithelial adapter (compute_legacy_exec) |
| epithelial_only_remap_BU3_v1.py | yes | legacy epithelial script |
| whole_lung_project_common_v2.py | yes | whole-lung adapter |
| project_BU3_to_reference_RNA_v1.py | yes | legacy whole-lung script |
| scripts/collect_projection_key_metrics_multiroot.py | yes | multiroot collector |
| gse237359_vs_CA1_BU3_key_metrics_multiroot.tsv | yes | canonical compare table (source of affected row IDs) |
| gse237359_organoid_query_sample_sheet_v2.tsv | yes | donor-resolved sample sheet |
| references/releases/fetal_lung_v1/README.md | yes | release v1 pointer |

All code and template files are committed and present in the worktree.

## 3. Local prerequisite check

| Prerequisite | Status | Path |
|-------------|--------|------|
| Reference H5AD | **present_local** | converted/reference_RNA.h5ad (1.6 Gb) |
| Reference metadata | **present_local** | converted/reference_metadata_v1.csv (16 Mb) |
| CA1 query H5AD | **present_local** | converted/query_CA1_clean.h5ad |
| BU3 query H5AD | **present_local** | converted/query_BU3_clean.h5ad |
| G237359_15934 donor H5AD | **present_local** | queries/converted/gse237359/donor_split_h5ad/GSM8229877_AT2_15934_scRNA.h5ad |
| G237359_16011 donor H5AD | **present_local** | queries/converted/gse237359/donor_split_h5ad/GSM8229877_AT2_16011_scRNA.h5ad |
| G237359_16392 donor H5AD | **present_local** | queries/converted/gse237359/donor_split_h5ad/GSM8229877_AT2_16392_scRNA.h5ad |
| G237359_16402 donor H5AD | **present_local** | queries/converted/gse237359/donor_split_h5ad/GSM8229877_AT2_16402_scRNA.h5ad |
| CA1 WL summary JSON | **present_local** | prototype_out_v1/CA1_summary_v1.json |
| CA1 WL projection CSV | **present_local** | prototype_out_v1/CA1_cell_projection_v1.csv |
| BU3 WL summary JSON | **present_local** | prototype_out_v1/BU3_summary_v1.json |
| BU3 WL projection CSV | **present_local** | prototype_out_v1/BU3_cell_projection_v1.csv |
| G237359_15934 WL summary | **missing_local** | not in prototype_out_v1/ or any known path |
| G237359_15934 WL projection | **missing_local** | not in prototype_out_v1/ or any known path |
| G237359_16011 WL summary | **missing_local** | (same) |
| G237359_16011 WL projection | **missing_local** | (same) |
| G237359_16392 WL summary | **missing_local** | (same) |
| G237359_16392 WL projection | **missing_local** | (same) |
| G237359_16402 WL summary | **missing_local** | (same) |
| G237359_16402 WL projection | **missing_local** | (same) |
| All 6 multiroot run-root dirs | **missing_local** | benchmark_run_gse237359_vs_*_compute/ (0/6 found) |

**Summary**: all 6 query H5AD inputs are present. CA1/BU3 whole-lung
outputs are present (from legacy prototype_out_v1/). GSE237359 donor
whole-lung outputs are entirely missing — both run-root directories
and any standalone summary/projection files.

## 4. Manifest / path-mapping assessment

- `query_manifest_v1.csv` covers CA1 and BU3 only. GSE237359 donor
  rows are **not** in this manifest.
- `legacy_output_manifest_v1.csv` covers CA1 and BU3 only. GSE237359
  donor WL outputs are **not** in this manifest.
- The compare table records `run_root` and `whole_lung_summary` for all
  6 rows, but the run-root directories no longer exist locally. The
  compare table does not record `whole_lung_projection` (cell-level
  CSV) paths at all.
- Therefore, the compare table alone is **not sufficient** to
  parameterize an epithelial-only rerun for the GSE237359 donor rows.

## 5. Decision: not_ready_missing_whole_lung_gate_inputs

**Primary outcome: C — not ready, missing whole-lung gate inputs.**

The epithelial rerun requires whole-lung summary JSON + cell-level
projection CSV as gate inputs. For the 4 GSE237359 donor rows, neither
exists locally and the run-root directories are gone. The manifests do
not cover these rows.

**CA1/BU3 are partially ready**: their query H5AD and whole-lung outputs
are present locally, so an epithelial-only rerun for just those 2 rows
could proceed. However, running a partial 2-row pilot while 4 donor
rows remain blocked would fragment the 6-row lane.

## 6. Blocker breakdown

| Row group | Query H5AD | WL summary | WL projection | Epi rerun ready? |
|-----------|:---:|:---:|:---:|:---:|
| CA1, BU3 | yes | yes | yes | **yes** |
| G237359_15934, _16011, _16392, _16402 | yes | **no** | **no** | **no** |

The blocker for the 4 donor rows is that **whole-lung self/self rerun
must precede epithelial rerun**. A whole-lung run for each donor row
would produce the summary JSON and cell-projection CSV needed as
epithelial-stage gate inputs.

## 7. Recommendation / sequencing

To unblock the full 6-row lane:

1. **Merge this note** — fixes the readiness assessment
2. **Run whole-lung self/self for the 4 GSE237359 donor rows** using
   the legacy whole-lung template + adapter, with donor-split H5AD
   inputs (which are present locally). This produces the missing
   summary JSON + cell-projection CSV files.
3. **Then run epithelial for all 6 rows** — CA1/BU3 using existing
   prototype_out_v1 WL outputs; donor rows using the newly produced
   WL outputs from step 2.
4. **Extract the 5 target epithelial columns** from the new epi_summary
   JSONs.
5. **Only then refresh** comparison-world and lifecycle surfaces.

Alternatively, if a partial 2-row pilot for CA1/BU3 only is acceptable
as a first step, that could proceed immediately — but it would leave
the 4 donor rows still unresolved.

No recompute in this step. No comparison-world refresh in this step.
No lifecycle refresh in this step.

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
