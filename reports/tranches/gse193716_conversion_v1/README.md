# GSE193716 Conversion v1

## Date
2026-04-07

## Purpose
H5-to-H5AD conversion for all 7 GSE193716 per-GSM CellRanger filtered H5
files, following the gene-space audit that confirmed GRCh38 build and 87.4%
reference overlap.

## Inputs

| Input | Path |
|-------|------|
| Raw H5 files (7) | `queries/raw/gse193716/GSM58191{29..35}_*.filtered_feature_bc_matrix.h5` |
| Registration manifest | `metadata/external/gse193716_dataset_manifest_v1.yaml` |
| Registration sample sheet | `metadata/external/gse193716_organoid_query_sample_sheet_v1.tsv` |
| Gene-space audit | `reports/tranches/gse193716_registration_audit_v1/` |
| Reference H5AD | `converted/reference_RNA.h5ad` (30,852 genes) |

## Conversion method

1. `scanpy.read_10x_h5()` — load CellRanger filtered H5
2. `adata.var_names_make_unique()` — resolve 32 duplicate gene symbols
3. Add obs metadata: query_dataset_id, local_query_sample_id,
   source_sample_name, source_type, donor_id, species
4. `adata.raw = adata` — freeze raw copy
5. `adata.layers["counts"] = adata.X.copy()` — explicit raw-count layer
6. `adata.write_h5ad()` — save to queries/converted/gse193716/

Script: `queries/converted/gse193716/convert_gse193716_h5_to_h5ad.py`

This follows the same pattern as GSE221343 conversion
(`queries/converted/gse221343/convert_gse221343_h5_to_h5ad.py`).

## Per-sample output inventory

| Sample | GSM | Category | Cells | Features | Output |
|--------|-----|----------|------:|--------:|--------|
| GSM5819131_primary_preculture_PL2 | GSM5819131 | primary pre-culture (PL2) | 1,148 | 33,539 | `queries/converted/gse193716/GSM5819131_primary_preculture_PL2.h5ad` |
| GSM5819132_primary_preculture_PL1 | GSM5819132 | primary pre-culture (PL1) | 879 | 33,539 | `queries/converted/gse193716/GSM5819132_primary_preculture_PL1.h5ad` |
| GSM5819129_primary_cultured_PL2 | GSM5819129 | primary cultured (PL2) | 1,439 | 33,539 | `queries/converted/gse193716/GSM5819129_primary_cultured_PL2.h5ad` |
| GSM5819130_primary_cultured_PL1 | GSM5819130 | primary cultured (PL1) | 2,097 | 33,539 | `queries/converted/gse193716/GSM5819130_primary_cultured_PL1.h5ad` |
| GSM5819133_iAEC2_3D | GSM5819133 | iAEC2 3D (SPC2-ST-B2) | 2,982 | 33,539 | `queries/converted/gse193716/GSM5819133_iAEC2_3D.h5ad` |
| GSM5819134_iAEC2_3D_insert | GSM5819134 | iAEC2 3D/insert (SPC2-ST-B2) | 2,068 | 33,539 | `queries/converted/gse193716/GSM5819134_iAEC2_3D_insert.h5ad` |
| GSM5819135_iAEC2_MRC5_insert | GSM5819135 | iAEC2 +MRC5/insert (SPC2-ST-B2) | 2,232 | 33,539 | `queries/converted/gse193716/GSM5819135_iAEC2_MRC5_insert.h5ad` |

**Total**: 12,845 cells across 7 samples.
Cell count range: 879 (PL1 pre-culture) to 2,982 (iAEC2 3D).

## Metadata hygiene performed

The following stale registration-era assertions were corrected:

| Field | Before (registration) | After (audit-resolved) |
|-------|----------------------|----------------------|
| Genome build | "hg19" | GRCh38_tdtomato_10X |
| Gene-space status | "must be verified during conversion" | 87.4% overlap confirmed; lncRNA annotation drift |
| feature_space_notes | "hg19 + TdTomato reporter; gene-space compatibility with hg38 reference must be verified during conversion" | "GRCh38_tdtomato_10X; 33539 Gene Expression features; 26975/30852 (87.4%) reference overlap; ..." |
| registration_notes | full pre-download text | prefixed with [Superseded by conversion_notes below.] |
| qc_status | registered_not_validated | local_validation_inspected_manual_review_required |

## What is resolved

- **Build**: GRCh38 (not hg19)
- **Overlap**: 87.4% (26,975/30,852) — acceptable; gap is lncRNA annotation
- **Remapping**: not needed
- **Duplicate symbols**: 32 handled via var_names_make_unique
- **TdTomato**: retained in H5AD
- **Raw counts**: preserved in X, .raw, and layers["counts"]
- **Conversion**: 7/7 complete, all reload successfully

## What is NOT resolved

- **Adult-primary-vs-fetal-reference interpretability**: unknown until
  projection is run. Primary adult AEC2s may project to unexpected
  reference niches. This is a biology question, not a conversion issue.
- **Projection quality at 87.4% overlap vs 92%+ (other tranches)**:
  unknown until projection is run.
- **MRC5 fibroblast contamination**: cultured samples were FACS EPCAM+
  sorted, but residual non-epithelial cells cannot be ruled out until
  projection reveals coarse type composition.
- **query_ready_flag**: remains false for all 7 rows. Promotion requires
  projection smoke test + explicit reviewer decision.

## Explicit stop line

- Projection: **not done** — next step
- Review: **not done** — requires projection first
- query-ready decision: **not done** — requires review
- data_contract.yaml: **not edited** — no new enum needed at this stage
- decision_log.md: **not edited** — no promotion decision made
- comparison_world_biology_summary: **not edited** — GSE193716 is not yet
  part of the query-ready world

## Files in this directory

| File | Description |
|------|-------------|
| `README.md` | This file |
| `gse193716_conversion_summary_v1.tsv` | Per-sample conversion metrics (7 rows, 13 columns) |
