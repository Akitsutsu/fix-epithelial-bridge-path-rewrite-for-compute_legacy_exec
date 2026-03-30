# Organoid query provenance v1

## Scope and purpose

This document records the current state of local organoid data available for
benchmarking against the fetal lung reference (release v1). It distinguishes
source-level organoid data from query-ready samples, documents what exists,
and states clearly what is missing.

CA1 and BU3 are currently used as **anchor queries** for regression checking
and parity validation. They are not a cohort. A cohort requires multiple
additional organoid lines, donors, or conditions to enable comparative analysis.

---

## Current local organoid sources

### GSE266789_hPSC_fetal_lung_organoids.rds

| Item | Value |
|---|---|
| GEO accession | GSE266789 |
| Local file | `GSE266789_hPSC_fetal_lung_organoids.rds` |
| File size | ~210 MB |
| Object type | Seurat v5 |
| Assays | RNA, integrated |
| Total cells | 2,450 |
| Total genes | 28,648 |
| Samples | 2 (`CA1_exp_org`, `BU3_exp_org`) |
| Publication | Wong et al. 2024, fetal lung epithelial atlas |

**Metadata columns in source RDS:**

| Column | Content |
|---|---|
| `orig.ident` | Sample identity: `CA1_exp_org` or `BU3_exp_org` |
| `nCount_RNA` | UMI count per cell |
| `nFeature_RNA` | Gene count per cell |
| `percent.mt` | Mitochondrial fraction |
| `integrated_snn_res.0.4` | Clustering resolution 0.4 |
| `seurat_clusters` | Default cluster assignment |
| `integrated_snn_res.0.5` | Clustering resolution 0.5 |
| `integrated_snn_res.0.6` | Clustering resolution 0.6 |
| `development_stage` | Constant: "hPSC fetal lung organoids" |

The source RDS does **not** contain: cell-type annotations, protocol version,
culture day/passage, donor identity, clone identity, or batch labels beyond
`orig.ident`.

---

## Query-ready samples

Two samples have been extracted from the source RDS and are currently used as
anchor queries in the benchmark system.

### CA1

| Item | Value |
|---|---|
| query_id | CA1 |
| Source file | `GSE266789_hPSC_fetal_lung_organoids.rds` |
| Extracted file | `converted/query_CA1_clean.h5ad` |
| orig.ident | `CA1_exp_org` |
| Cells | 1,719 |
| Genes | 28,648 |
| Gene overlap with v1 reference | 27,752 / 28,648 (96.9%) |
| Anchor status | Anchor query |

### BU3

| Item | Value |
|---|---|
| query_id | BU3 |
| Source file | `GSE266789_hPSC_fetal_lung_organoids.rds` |
| Extracted file | `converted/query_BU3_clean.h5ad` |
| orig.ident | `BU3_exp_org` |
| Cells | 731 |
| Genes | 28,648 |
| Gene overlap with v1 reference | 27,752 / 28,648 (96.9%) |
| Anchor status | Anchor query |

The `_clean` h5ad files contain additional metadata columns added during
extraction: `sample_id`, `donor_id`, `source_type`, `batch_id`,
`expected_stage_text`. These are recorded in `query_manifest_v1.csv`.

---

## Non-query-ready / out-of-scope files encountered

The following local files were checked during inventory and are **not**
organoid query data:

| File | Type | Reason excluded |
|---|---|---|
| `GSE264407_full_fetal_lung_dataset_04142025.rds` | Fetal tissue atlas | Reference source, not organoid |
| `full_fetal_lung_dataset.rds` | Fetal tissue atlas | Alias for GSE264407 |
| `C1filtered.h5ad` | Fetal tissue (9,096 cells) | Tissue batches, not organoid |
| `adata_combined.h5ad` | Fetal tissue (526 cells, GW10) | Reference subset, not organoid |
| `LungMAP_MouseLung_CellRef.v1.1.h5ad` | Mouse lung reference | Wrong species |
| `Mouse_budtip_subset.h5ad` | Mouse budtip subset | Wrong species |
| `gw10_budtip_cells.h5ad` | Fetal tissue subset | Tissue, not organoid |
| `gw10_stalk_cells.h5ad` | Fetal tissue subset | Tissue, not organoid |
| `gw10_SOX2_cells.h5ad` | Fetal tissue subset | Tissue, not organoid |
| `epi_window_*.h5ad` | Deconvolution intermediates | Analysis artifacts |
| `synthetic_grid_*.h5ad` | Spatial simulation | Synthetic data |
| `stage1_budtip_template*.h5ad` | Template objects | Analysis templates |
| `random_mapped_*.h5ad` | Mapping intermediates | Analysis artifacts |
| `fetal_lung_fixed*.h5ad` | Fetal tissue variants | Reference variants |
| `converted/query_organoid_01.h5ad` | Combined pre-split (2,450 cells) | Superseded by CA1 + BU3 splits |
| `converted/query_organoid_01_clean.h5ad` | Combined pre-split clean | Superseded by CA1 + BU3 splits |

---

## Readiness verdict

**Additional query-ready organoid samples beyond CA1 and BU3: 0**

The only local organoid source (`GSE266789`) contains exactly 2 samples,
both of which are already extracted and used as anchor queries.

**A first organoid cohort tranche is NOT feasible from currently available
local organoid data.**

---

## Exact gap to unlock a first cohort tranche

The required threshold for a first cohort tranche is >= 4 additional
query-ready organoid samples beyond the existing CA1 and BU3 anchors
(total >= 6 samples).

To reach this threshold, the project needs:

1. **Additional organoid scRNA-seq data** from at least 4 distinct organoid
   lines, donors, conditions, or time points. Potential sources:
   - Additional GEO deposits related to hPSC fetal lung organoids
   - Lab-internal organoid culture runs (different donors, passages, protocols)
   - Collaborator-shared datasets
   - Other published fetal lung organoid atlases

2. **Query extraction** for each new sample:
   - Split by sample identity (analogous to CA1/BU3 extraction from the combined RDS)
   - Produce `_clean.h5ad` files with 28,648 genes matching the reference var_names
   - Add provenance metadata (`sample_id`, `donor_id`, `source_type`, `batch_id`)

3. **Query provenance documentation** for each new sample, recording source,
   extraction method, expected identity, and estimated cell count.

---

## Recommended next steps

1. **Search for additional public organoid datasets** in GEO, CellxGene, or
   related repositories that contain hPSC fetal lung organoid scRNA-seq data.
2. **Confirm** whether lab-internal organoid runs exist that have not been
   deposited or converted.
3. **If new data is found**, extract queries using the established `_clean.h5ad`
   format and update the query manifest.
4. **Do not proceed to cohort implementation** until at least 4 additional
   query-ready samples are confirmed.
