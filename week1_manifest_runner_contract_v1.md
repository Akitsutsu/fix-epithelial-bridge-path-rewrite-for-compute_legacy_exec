# Week 1 manifest spec and common runner I/O contract (v1)

## Scope

This contract is for the **frozen basis**:

- `reference = converted/reference_RNA.h5ad`
- `metadata = converted/reference_metadata_v1.csv`
- `stage axis = sample_week`
- `gestational_week` is not used
- whole-lung v1 is frozen
- two-stage design is fixed: `whole-lung lineage gate -> epithelial-only remap`

The goal of Week 1 is **not** to redesign mapping logic. The goal is to make
CA1/BU3-style runs reproducible for any new query through a single entry point.

---

## 1. Manifest spec

### Required columns

| column | type | rule |
| --- | --- | --- |
| `query_id` | string | unique, stable slug; allowed chars: `A-Z a-z 0-9 . _ -` |
| `h5ad_path` | string | path to query `.h5ad`; relative paths are resolved relative to the manifest file |

### Optional columns

| column | type | default | use |
| --- | --- | --- | --- |
| `note` | string | `""` | free-text note shown in compare tables |
| `enabled` | bool | `true` | include/exclude a row without deleting it |
| `group_label` | string | `""` | optional cohort/batch grouping label |
| `expected_sample_id` | string | `""` | checked against provenance preflight if provided |
| `expected_donor_id` | string | `""` | checked against provenance preflight if provided |
| `expected_source_type` | string | `""` | checked against provenance preflight if provided |
| `expected_batch_id` | string | `""` | checked against provenance preflight if provided |

### Example

```csv
query_id,h5ad_path,note,enabled,group_label,expected_sample_id,expected_donor_id,expected_source_type,expected_batch_id
CA1,converted/query_CA1_clean.h5ad,CA1 organoid query,true,organoid_batch1,query_CA1_organoid_01,CA1,organoid,GSE266789_CA1_exp_org
BU3,converted/query_BU3_clean.h5ad,BU3 organoid query,true,organoid_batch1,query_BU3_organoid_01,BU3,organoid,GSE266789_BU3_exp_org
```

### Manifest rules

1. `query_id` is the **primary key** for the run.
2. `query_id` must not encode assumptions about donor provenance beyond what the
   provenance preflight confirms.
3. `enabled=false` is the standard way to park a query temporarily.
4. Query-specific code paths are **not** stored in the manifest.

---

## 2. Common runner responsibilities

The common runner is responsible for:

1. reading and validating the manifest;
2. resolving relative file paths;
3. creating a fixed output directory tree;
4. running provenance audit first;
5. running whole-lung and epithelial stages for each enabled query;
6. checking whether required files exist;
7. writing cross-query compare tables and run-status logs.

The runner is **query-ID agnostic**. It should only know `query_id` as a label,
not as a switch for code branches.

---

## 3. Fixed output directory structure

A run root should look like this:

```text
<run_outdir>/
  run_config/
    query_manifest_v1.csv                # copied original
    manifest_resolved.csv                # paths resolved, defaults filled
    run_config.json
    preflight_result.json

  preflight/
    provenance/
      all_queries_provenance_overview.csv
      all_queries_target_field_presence.csv
      <query_id>/
        <query_id>_obs_inventory.csv
        <query_id>_provenance_field_presence.csv
        <query_id>_provenance_exact_combinations.csv
        <query_id>_provenance_summary.json
        <query_id>_provenance_summary.md
        <query_id>_provenance_sample_id.csv
        <query_id>_provenance_donor_id.csv
        <query_id>_provenance_source_type.csv
        <query_id>_provenance_batch_id.csv

  whole_lung/
    <query_id>/
      <query_id>_summary_v1.json
      <query_id>_cell_projection_v1.csv

  epithelial/
    <query_id>/
      <query_id>_epi_summary_v1.json
      <query_id>_epi_state_fine.csv
      <query_id>_epi_stage_fine.csv
      <query_id>_lineage_off_target_state_coarse.csv
      <query_id>_stable_state_marker_summary.csv                     # optional but expected in normal runs
      <query_id>_epi_state_boundary_pairs_unordered.csv              # optional but expected in normal runs
      <query_id>_boundary_pair_direction_marker_summary.csv          # optional; may be absent in some runs

  compare/
    all_queries_run_status.csv
    all_queries_provenance_check.csv
    all_queries_key_metrics.csv
    all_queries_epi_state_fine_compare.csv
    all_queries_epi_stage_fine_compare.csv
    all_queries_epi_boundary_pairs_compare.csv

  logs/
    preflight/
      provenance.stdout.log
      provenance.stderr.log
    <query_id>/
      whole_lung.stdout.log
      whole_lung.stderr.log
      epithelial.stdout.log
      epithelial.stderr.log
```

This replaces the earlier ad hoc split across
`prototype_out_v1/`, `prototype_out_epi_v1/`, `prototype_out_epi_v1_BU3/`, and
`prototype_out_epi_compare/`.

---

## 4. Stage order (fixed)

### Stage 0: provenance preflight

Must run before any mapping stage.

**Input**
- query `.h5ad`
- target obs fields: `sample_id`, `donor_id`, `source_type`, `batch_id`

**Output**
- exact provenance combo table
- field presence table
- summary json/md
- cross-query provenance check table

**Decision rule**
- provenance is considered **closed** for a query when the exact-combination top
  row and fraction are reported.
- if expected provenance fields were given in the manifest, they are compared to
  the observed top combination and marked `pass/fail/not_checked`.

### Stage 1: whole-lung lineage gate

Runs on all enabled queries.

**Contract input**
- frozen reference h5ad
- frozen metadata csv
- query `.h5ad`
- `query_id`
- `stage_axis=sample_week`
- output directory

**Required output files**
- `<query_id>_summary_v1.json`
- `<query_id>_cell_projection_v1.csv`

**Required summary JSON fields**
- `query_id`
- `n_query_cells`
- `n_query_epi_eligible`
- `lineage_off_target_fraction`

**Recommended summary JSON fields**
- `top_stage`
- `top_stage_fraction`
- `top_state`
- `top_state_fraction`

**Required cell-projection CSV fields**
- `cell_id` or an equivalent obs-name column
- a lineage/state prediction column from the whole-lung pass
- an epithelial eligibility column usable by Stage 2

The exact internal modeling can remain unchanged from whole-lung v1. The key
Week-1 requirement is that Stage 2 can identify the epithelial-eligible cells in
one standardized file.

### Stage 2: epithelial-only remap

Runs after Stage 1, using the epithelial gate from whole-lung.

**Contract input**
- frozen reference h5ad
- frozen metadata csv
- query `.h5ad`
- `query_id`
- `stage_axis=sample_week`
- whole-lung summary JSON
- whole-lung cell-projection CSV
- output directory

**Required output files**
- `<query_id>_epi_summary_v1.json`
- `<query_id>_epi_state_fine.csv`
- `<query_id>_epi_stage_fine.csv`
- `<query_id>_lineage_off_target_state_coarse.csv`

**Strongly recommended output files**
- `<query_id>_stable_state_marker_summary.csv`
- `<query_id>_epi_state_boundary_pairs_unordered.csv`

**Optional output file**
- `<query_id>_boundary_pair_direction_marker_summary.csv`

**Required epithelial summary JSON fields**
- `query_id`
- `n_query_cells`
- `n_query_epi_eligible`
- `lineage_off_target_fraction`
- `top_stage`
- `top_stage_fraction`
- `top_state`
- `top_state_fraction`

This is the stage that should absorb the logic now split across
`epithelial_only_remap_v1.py` and the BU3 working copy. The Week-1 refactor goal
is: **same code path, different manifest rows**.

---

## 5. CLI contract for the common runner

The common runner can stay thin by delegating the actual mapping steps to stage
scripts through command templates.

### Suggested whole-lung command template

```bash
python whole_lung_project_common_v1.py \
  --reference {reference} \
  --metadata {metadata} \
  --query-id {query_id} \
  --query-h5ad {h5ad_path} \
  --stage-axis {stage_axis} \
  --outdir {whole_lung_outdir}
```

### Suggested epithelial command template

```bash
python epithelial_only_remap_common_v1.py \
  --reference {reference} \
  --metadata {metadata} \
  --query-id {query_id} \
  --query-h5ad {h5ad_path} \
  --stage-axis {stage_axis} \
  --whole-lung-summary {whole_lung_summary_json} \
  --whole-lung-projection {whole_lung_cell_projection_csv} \
  --outdir {epi_outdir}
```

### Placeholders the runner provides

| placeholder | meaning |
| --- | --- |
| `{query_id}` | query ID from manifest |
| `{h5ad_path}` | resolved path to query h5ad |
| `{note}` | free-text note from manifest |
| `{reference}` | frozen reference h5ad |
| `{metadata}` | frozen reference metadata csv |
| `{stage_axis}` | fixed stage axis, default `sample_week` |
| `{run_outdir}` | root output directory for the whole run |
| `{provenance_outdir}` | per-query provenance output directory |
| `{provenance_summary_json}` | per-query provenance summary JSON |
| `{whole_lung_outdir}` | per-query whole-lung output directory |
| `{whole_lung_summary_json}` | expected Stage 1 summary JSON path |
| `{whole_lung_cell_projection_csv}` | expected Stage 1 cell projection CSV path |
| `{epi_outdir}` | per-query epithelial output directory |
| `{epi_summary_json}` | expected Stage 2 summary JSON path |
| `{epi_state_fine_csv}` | expected Stage 2 state CSV path |
| `{epi_stage_fine_csv}` | expected Stage 2 stage CSV path |
| `{query_log_outdir}` | per-query log directory |

The runner shell-quotes these values before interpolation.

---

## 6. Cross-query compare contract

At the end of a run, the compare folder should contain at least:

### `all_queries_run_status.csv`
Tracks whether each stage ran and whether required files were found.

Minimum fields:
- `query_id`
- `enabled`
- `whole_lung_status`
- `whole_lung_message`
- `epi_status`
- `epi_message`

### `all_queries_provenance_check.csv`
Cross-query provenance summary.

Minimum fields:
- `query_id`
- `top_combo_fraction`
- `sample_id`
- `donor_id`
- `source_type`
- `batch_id`
- `expected_sample_id`
- `expected_donor_id`
- `expected_source_type`
- `expected_batch_id`
- `provenance_status`

### `all_queries_key_metrics.csv`
Cross-query benchmark table.

Target fields:
- `query_id`
- `note`
- `sample_id`
- `donor_id`
- `source_type`
- `batch_id`
- `n_query_cells`
- `n_query_epi_eligible`
- `lineage_off_target_fraction`
- `top_stage`
- `top_stage_fraction`
- `top_state`
- `top_state_fraction`

This table is the bridge between per-query outputs and the eventual Amy lab
benchmark memo.

---

## 7. Week-1 acceptance criteria

Week 1 is complete when all of the following are true:

1. CA1 and BU3 are both listed in one manifest.
2. provenance preflight runs from the manifest and confirms the known exact
   provenance:
   - CA1 = `query_CA1_organoid_01 / CA1 / organoid / GSE266789_CA1_exp_org`
   - BU3 = `query_BU3_organoid_01 / BU3 / organoid / GSE266789_BU3_exp_org`
3. the same runner entry point launches both queries.
4. the runner does **not** branch on query ID.
5. required outputs land in the fixed directory tree.
6. CA1/BU3 top conclusions are reproduced within this common layout.

---

## 8. What this contract intentionally does not do yet

Not in Week 1:
- reference rescue or metadata decode
- donor vs batch separation
- perturbation or causal program inference
- histology/spatial anchoring
- simulator/digital shadow logic

Week 1 is strictly about turning CA1/BU3 into reusable benchmark exemplars.
