# Reference Promotion Criteria v1

## Purpose

This document defines the criteria and decision framework for promoting a candidate
reference to a new versioned release.

It is a companion to `REFERENCE_UPDATE_SYSTEM_v1.md`, which describes the overall
lifecycle. This document focuses specifically on the **promotion decision** — the
gate between a candidate that has been built and evaluated and a new immutable release.

---

## Relationship to existing artifacts

The promotion decision depends on evidence produced by earlier stages of the
reference update pipeline:

| Stage | Script / artifact | What it provides |
|---|---|---|
| Candidate build | `build_reference_candidate_v1.R` | Candidate h5ad + h5Seurat |
| Metadata extraction | `extract_reference_metadata_candidate_v1.py` | Candidate metadata CSV |
| Structural drift | `run_reference_drift_report_v1.py --mode structural` | Shape, overlap, distribution drift |
| Benchmark drift | `run_reference_drift_report_v1.py --mode both` | Anchor-query key metrics diff |

A promotion decision **cannot** be made until the structural drift report exists.
A benchmark drift report is strongly recommended but may be deferred for exploratory
candidates.

---

## Evidence required before promotion can be considered

At minimum, the following must exist before a promotion decision is opened:

1. **Candidate build artifacts**
   - `reference_RNA.h5ad` in the candidate directory
   - `reference_metadata.csv` in the candidate directory
   - `build_manifest.yaml` recording build parameters
   - `build_versions.csv` recording software versions

2. **Structural drift report**
   - `REFERENCE_DRIFT_REPORT_<tag>.md`
   - `reference_drift_summary_<tag>.json`
   - `release_vs_candidate_structural_diff_<tag>.csv`

3. **Benchmark drift report** (strongly recommended)
   - `anchor_key_metrics_diff_<tag>.csv`
   - Benchmark runs for both release and candidate stored under the drift outdir

---

## Must-pass criteria

These are non-negotiable requirements. A candidate that fails any of these
**cannot** be promoted regardless of biological merit.

### 1. Rebuildability

The candidate can be rebuilt from its recorded build manifest and scripts.
The `build_manifest.yaml` must record the source RDS, tag, filter parameters,
codebook directory, and software versions.

### 2. Required metadata columns

The candidate metadata CSV must contain all 9 required columns:

- `cell_id`
- `sample_id`
- `sample_name`
- `stage_fine`
- `stage_num`
- `stage_coarse`
- `state_coarse`
- `state_fine`
- `group_internal`

This is verified automatically by the structural drift report
(`all_required_present` in the drift summary JSON).

### 3. Codebook decoding

All integer-coded categorical columns must decode without unmapped values.
This is verified during the `extract_reference_metadata_candidate_v1.py` step.

### 4. Source and software versions recorded

The `build_versions.csv` and `build_manifest.yaml` must exist in the candidate
directory and contain non-empty values for R, Seurat, SeuratDisk, and
SeuratObject versions.

### 5. Existing releases not overwritten

The promotion process must never modify artifacts belonging to a previous release.
Release v1 files under `converted/` and the registry entries for v1 must remain
unchanged.

### 6. X layer integrity

The candidate h5ad `.X` must be non-negative. This is checked by the structural
drift report (`x_non_negative` in the drift summary JSON).

---

## Explainable-drift criteria

These criteria **may change** between releases. Change is expected when the
reference is broadened, re-annotated, or filtered differently. However, every
change must be explained.

### 1. Gene coverage

| Check | Source |
|---|---|
| var_names identical to release | `var_names.identical` in drift summary |
| var_names overlap (if not identical) | `var_names.jaccard` in drift summary |
| Release-only genes | `var_names.release_only` |
| Candidate-only genes | `var_names.candidate_only` |

If the gene space changes, the explanation should state why and whether
downstream scripts depend on specific genes.

### 2. Stage and state distributions

| Check | Source |
|---|---|
| stage_fine L1 distance | `distributions.stage_fine.l1_distance` |
| stage_coarse L1 distance | `distributions.stage_coarse.l1_distance` |
| state_fine L1 distance | `distributions.state_fine.l1_distance` |
| state_coarse L1 distance | `distributions.state_coarse.l1_distance` |
| group_internal L1 distance | `distributions.group_internal.l1_distance` |
| Categories gained or lost | `*_only_categories` fields |

Large L1 distances are expected if the candidate includes different gestational
weeks or applies different filters. The key question is whether the shift is
consistent with the stated purpose of the candidate.

### 3. Anchor-query results (CA1 and BU3)

These are evaluated from `anchor_key_metrics_diff_<tag>.csv`:

| Metric | Field |
|---|---|
| top_stage match | `match_top_stage` |
| top_state match | `match_top_state` |
| off-target fraction change | `diff_lineage_off_target_fraction` |
| n_query_cells change | `diff_n_query_cells` |
| n_query_epi_eligible change | `diff_n_query_epi_eligible` |

**Interpretation guidance:**

- `top_stage` and `top_state` changing is not automatically disqualifying, but
  the new values must be biologically interpretable.
- `lineage_off_target_fraction` increasing substantially suggests the candidate
  reference may be less suitable for epithelial analysis.
- `n_query_cells` and `n_query_epi_eligible` should not change between release
  and candidate runs (the queries are the same). If they do, investigate whether
  the runner is behaving differently.

### 4. Epithelial remap stability

If benchmark mode was run, check whether the expected epithelial output files
exist for both BU3 and CA1 in both the release and candidate benchmark runs.
The `*_epi_artifacts_present` fields in the key metrics diff report this.

---

## Decision outcomes

### Promote

The candidate becomes the next release.

Conditions:
- All must-pass criteria are satisfied.
- Explainable-drift criteria have been reviewed and documented.
- Anchor-query changes (if any) are understood and acceptable.
- The promotion rationale is recorded in a decision YAML.

### Hold

The candidate is not rejected but requires further evaluation.

Conditions:
- Must-pass criteria are satisfied.
- Some drift results are ambiguous or incomplete.
- Additional evidence is needed (e.g., benchmark run not yet completed,
  biological interpretation pending).

### Reject

The candidate is not suitable for promotion.

Conditions:
- One or more must-pass criteria failed, OR
- Drift results show unexplained degradation, OR
- The candidate does not serve a clear purpose relative to the current release.

---

## What a release-freeze follow-up would need to do

This PR does **not** implement release freeze. When that automation is added,
a promotion-to-freeze step should:

1. Assign a new release version (e.g., `v2`).
2. Copy or symlink candidate artifacts into `references/releases/<release_name>/`.
3. Compute and record checksums for the h5ad and metadata CSV.
4. Write a release provenance document.
5. Write a release note summarizing what changed and why.
6. Add a new row to `references/registry/REFERENCE_REGISTRY.csv`.
7. Update `references/registry/current_release.yaml` to point to the new release.
8. Preserve the old release artifacts unchanged.

---

## What this document intentionally does not automate

- **No automated pass/fail thresholds.** L1 distances, fraction diffs, and
  category counts are reported but not auto-gated. The decision requires
  human judgment about biological acceptability.
- **No multi-atlas promotion.** This version assumes a single upstream source.
  Multi-atlas candidates would need additional merge provenance.
- **No query provenance versioning.** Anchor queries (CA1, BU3) are assumed
  stable. If query extraction changes, that should be tracked separately.
- **No CI integration.** Promotion decisions are currently manual review
  artifacts, not automated pipeline gates.

---

## Decision record format

Each promotion decision should be recorded as a YAML file in the promotion
directory. See `references/promotion/example_release_promotion_decision.yaml`
for the expected schema.

The decision YAML serves as the audit trail connecting a candidate, its drift
evidence, and the human judgment about whether to promote.
