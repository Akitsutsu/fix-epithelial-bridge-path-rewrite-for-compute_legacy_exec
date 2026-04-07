# GSE193716 Gene-Space Audit v1

## Date
2026-04-07

## Purpose
Pre-conversion gene-space audit for GSE193716, the fifth external intake
candidate. Determines whether the per-GSM CellRanger H5 files are loadable,
what genome build was actually used, and whether the feature space is
compatible with the current reference (v1).

## Key finding: genome is GRCh38, not hg19

The GEO data processing notes state "mapped to hg19" but the actual genome
tag in all 7 H5 files is **GRCh38_tdtomato_10X**. This is a custom
CellRanger reference built on GRCh38 (hg38) with a TdTomato reporter gene
appended. The hg19 caveat documented in the registration manifest was based
on the GEO text and is now superseded by this direct inspection.

## Sample inventory

| GSM | Short | Category | Cells | Features |
|-----|-------|----------|------:|--------:|
| GSM5819131 | CG7 | primary AEC2 pre-culture (PL2) | 1,148 | 33,539 |
| GSM5819132 | CG8 | primary AEC2 pre-culture (PL1) | 879 | 33,539 |
| GSM5819129 | CG5 | primary AEC2 cultured (PL2) | 1,439 | 33,539 |
| GSM5819130 | CG6 | primary AEC2 cultured (PL1) | 2,097 | 33,539 |
| GSM5819133 | CG12 | iAEC2 3D (SPC2-ST-B2) | 2,982 | 33,539 |
| GSM5819134 | CG13 | iAEC2 3D/insert (SPC2-ST-B2) | 2,068 | 33,539 |
| GSM5819135 | CG14 | iAEC2 +MRC5/insert (SPC2-ST-B2) | 2,232 | 33,539 |

All 7 samples load successfully with `scanpy.read_10x_h5()`.
All have identical feature space (33,539 Gene Expression features).
X dtype is float32, integer-valued (raw counts).

## Reference overlap

| Metric | Value |
|--------|-------|
| Reference genes | 30,852 |
| Query Gene Expression features | 33,539 (unique symbols: 33,507) |
| Overlap with reference | 26,975 / 30,852 (**87.4%**) |
| Reference genes missing from query | 3,877 |
| Query-extra genes (not in ref) | 6,532 |

Overlap is **identical across all 7 samples** (same CellRanger reference).

### Comparison with GSE221343 (same lab, same pipeline)
- GSE221343: 56,855 features, 28,378/30,852 overlap (**92.0%**)
- GSE193716: 33,539 features, 26,975/30,852 overlap (**87.4%**)
- 1,403 genes are in GSE221343+ref but NOT in GSE193716

The 4.6% gap between GSE193716 and GSE221343 is due to different Gencode
annotation versions in their respective CellRanger references, not a
fundamental genome build difference.

## Missing reference genes: breakdown

| Category | Count | % of missing |
|----------|------:|---:|
| AC-prefix lncRNAs | 1,857 | 47.9% |
| AL-prefix lncRNAs | 818 | 21.1% |
| LINC genes | 235 | 6.1% |
| AP-prefix lncRNAs | 163 | 4.2% |
| Other (AF-prefix, AS1, DT, etc.) | 804 | 20.7% |

The missing genes are **overwhelmingly non-coding RNA annotation
differences** between Gencode releases. No protein-coding genes critical
for lung biology interpretation are missing.

## Key lung marker genes: all present

All 17 checked lung-relevant markers are present in both query and reference:
SFTPC, SFTPB, SFTPA1, SFTPA2, NKX2-1, SOX2, SOX9, TP63, KRT5, FOXJ1,
SCGB1A1, CFTR, HOPX, AGER, PDPN, EPCAM, CDH1.

## Duplicate gene symbols

32 gene symbols appear twice in the H5 feature list, each mapping to two
different Ensembl IDs. Examples: ABCF2, ALDOA, IGF2, MATR3, SOD2.
These require `var_names_make_unique()` during H5-to-H5AD conversion.

This is the same pattern seen in GSE221343 (which had 1,543 duplicates
from a larger feature set).

## TdTomato reporter

- Feature name: `TDTOMATO`
- Ensembl ID: `TDTOMATO` (custom, not a standard Ensembl ID)
- Present in all 7 samples
- NOT in the reference gene space
- Should be **retained during conversion** (useful for SPC2-ST-B2 lineage
  tracing QC in the iAEC2 samples) but will naturally be excluded from
  reference overlap calculations

## Conversion readiness assessment

| Gate | Status | Notes |
|------|--------|-------|
| H5 loadable | **pass** | All 7 load with `scanpy.read_10x_h5()` |
| Gene Expression only | **pass** | All 33,539 features are Gene Expression |
| Raw counts present | **pass** | X is integer-valued (float32 dtype) |
| Genome build | **pass** | GRCh38 (not hg19 as initially feared) |
| Reference overlap | **pass** | 87.4% — lower than GSE221343 (92.0%) but all key markers present; gap is lncRNA annotation |
| Duplicate symbols | **pass with action** | 32 duplicates; `var_names_make_unique()` needed |
| Reporter handling | **pass** | TDTOMATO present; retain in H5AD, exclude from overlap |

**Assessment: ready for H5-to-H5AD conversion.**

The 87.4% overlap is acceptable. The missing 3,877 genes are annotation-
version lncRNA differences, not biologically meaningful gaps. The same
conversion approach used for GSE221343 (CellRanger H5 → scanpy →
var_names_make_unique → save H5AD) should work.

## What this audit does NOT determine

- Whether primary adult AEC2s produce interpretable projections on the
  fetal lung reference (requires projection, not gene-space audit)
- Whether the 87.4% overlap produces different projection quality vs
  92.0% (GSE221343) or 100.0% (GSE289846/GSE308817)
- Whether culture-format differences (3D vs insert vs +MRC5) are
  resolvable on the reference
- Whether MRC5 fibroblast contamination persists after EPCAM+ sorting

## Files in this directory

| File | Description |
|------|-------------|
| `README.md` | This file |
| `gse193716_gene_space_audit_v1.tsv` | Per-sample audit metrics (7 rows) |

## Source files

| Source | Path |
|--------|------|
| Reference H5AD | `converted/reference_RNA.h5ad` |
| GSE193716 per-GSM H5 files (7) | `queries/raw/gse193716/*.h5` |
| Registration manifest | `metadata/external/gse193716_dataset_manifest_v1.yaml` |
| Registration sample sheet | `metadata/external/gse193716_organoid_query_sample_sheet_v1.tsv` |
| GSE221343 H5 (for comparison) | `queries/raw/gse221343/GSM6858854_CK+DCI.h5` |
