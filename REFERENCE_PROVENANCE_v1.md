# Reference provenance v1

## Frozen pair

These two files are the frozen reference inputs for all benchmark runs.
They must not be regenerated or overwritten without a versioned migration.

| File | Path | Rows | Columns |
|---|---|---|---|
| Expression matrix | `converted/reference_RNA.h5ad` | 144,380 cells | 30,852 genes |
| Cell metadata | `converted/reference_metadata_v1.csv` | 144,380 rows | 9 columns |

### Metadata columns

| Column | Example | Source |
|---|---|---|
| `cell_id` | `AAACCCAAGCGCCCAT-1_1` | h5ad obs index |
| `sample_id` | `GW10.1` | h5ad `orig.ident` |
| `sample_name` | `GW_10_1` | h5ad `sample_name` |
| `stage_fine` | `week_10` | h5ad `sample_week` |
| `stage_num` | `10` | derived: `int(stage_fine.replace("week_", ""))` |
| `stage_coarse` | `early_GW10_13` | derived: `<=13 early, <=16 mid, else late` |
| `state_coarse` | `Immune` | h5ad `cell_type` decoded via codebook |
| `state_fine` | `Macrophage` | h5ad `all_cell_type` decoded via codebook |
| `group_internal` | `week_10` | h5ad `group` decoded via codebook |

## Upstream source

| Item | Value |
|---|---|
| GEO accession | GSE264407 |
| File | `GSE264407_full_fetal_lung_dataset_04142025.rds` |
| Local alias | `full_fetal_lung_dataset.rds` |
| Object type | Seurat v5, multiple assays |
| Publication | Wong et al. 2024, fetal lung epithelial atlas |

## Query source

| Item | Value |
|---|---|
| GEO accession | GSE266789 |
| File | `GSE266789_hPSC_fetal_lung_organoids.rds` |
| Object type | Seurat v5 |
| Queries extracted | CA1 (`query_CA1_clean.h5ad`), BU3 (`query_BU3_clean.h5ad`) |

## Build chain

The frozen pair was created through three sequential steps.
No single end-to-end script existed at the time of creation.
The steps below are reconstructed from file timestamps, sizes, and the
surviving `convert_to_h5ad.R` script.

### Step 1: RDS → full h5Seurat → full h5ad

Script: `convert_to_h5ad.R` (exists, 18 lines)

```
readRDS("GSE264407_full_fetal_lung_dataset_04142025.rds")
  → SaveH5Seurat("converted/reference_full.h5Seurat")
  → Convert("converted/reference_full.h5Seurat", dest = "h5ad")
  → converted/reference_full.h5ad  (6.8 GB, 144380 × 30852, all assays)
```

Date: 2026-03-23

### Step 2: full h5Seurat → RNA-only h5Seurat → RNA-only h5ad

Script: **not preserved** (interactive R session)

Reconstructed procedure:
```r
library(Seurat); library(SeuratDisk)
ref <- LoadH5Seurat("converted/reference_full.h5Seurat")
DefaultAssay(ref) <- "RNA"
ref[["RNA"]] <- as(ref[["RNA"]], "Assay")   # or similar V5→V3 coercion
SaveH5Seurat(ref, "converted/reference_RNA.h5Seurat", overwrite = TRUE)
Convert("converted/reference_RNA.h5Seurat", dest = "h5ad", overwrite = TRUE)
```

Evidence:
- `reference_RNA.h5Seurat` = 8.0 GB (same as `reference_full.h5Seurat`)
- `reference_RNA.h5ad` = 1.7 GB (vs 6.8 GB for full) — h5ad export extracted RNA assay only
- Timestamp: 2026-03-27 (4 days after step 1)

Date: 2026-03-27

### Step 3: h5ad obs → reference_metadata_v1.csv

Script: **not preserved** (interactive Python session)

Reconstructed procedure:
```python
import anndata as ad, pandas as pd
ref = ad.read_h5ad("converted/reference_RNA.h5ad")
# codebook/ CSVs were used to decode integer-coded categoricals:
#   cell_type      → state_coarse  (5 levels: Epithelial, Stromal, …)
#   all_cell_type  → state_fine    (58 levels: Basal cells, Club cells, …)
#   sample_week    → stage_fine    (9 levels: week_10 … week_19)
#   group          → group_internal
# stage_num and stage_coarse were derived from stage_fine.
meta = pd.DataFrame(...)  # selected + decoded columns
meta.to_csv("converted/reference_metadata_v1.csv", index=False)
```

Date: 2026-03-28

## Codebook directory

`codebook/` contains the integer-to-label mappings extracted from the Seurat
factor levels. These were used in step 3 to decode h5ad obs columns.

| File | Maps | Levels |
|---|---|---|
| `codebook_cell_type.csv` | h5ad `cell_type` → `state_coarse` | 5 |
| `codebook_all_cell_type.csv` | h5ad `all_cell_type` → `state_fine` | 58 |
| `codebook_sample_week.csv` | h5ad `sample_week` values | 9 |
| `codebook_gestational_week.csv` | h5ad `gestational_week` → display labels | 9 |
| `codebook_group.csv` | h5ad `group` → `group_internal` | 7 |
| `codebook_orig.ident.csv` | h5ad `orig.ident` → `sample_id` | 20 |
| `codebook_sample_name.csv` | h5ad `sample_name` values | 20 |

## Integrity notes

- The frozen pair has been validated by the benchmark runner for CA1 and BU3.
- `check_exemplar_reproduction_v1.py` passes on the combined BU3+CA1 run.
- The h5ad obs columns `cell_type` and `all_cell_type` are integer-coded
  categoricals. The codebook CSVs are the authoritative decode tables.
- `reference_metadata_v1.csv` is the decoded, human-readable form used by all
  downstream scripts. It is the metadata of record; the raw h5ad obs integers
  should not be used directly.

## Provenance gaps

1. **No reproducible script for step 2** (full → RNA-only conversion).
   The exact R commands and Seurat version used are not recorded.
2. **No reproducible script for step 3** (metadata extraction + decode).
   The exact column selection and codebook application logic is not recorded.
3. **Seurat/SeuratDisk version** used for conversion is not recorded.
4. **Query splitting** (organoid → CA1 + BU3) script is not documented here.

These gaps do not affect the frozen pair — the files exist and are validated.
They would matter only if the reference needed to be rebuilt from the RDS source.
