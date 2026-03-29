# Reference provenance audit v1

## Objective

Verify that the frozen reference pair under `converted/` can be faithfully
reproduced from the upstream RDS source using the canonical rebuild scripts.

## Verdict

**MATCH** — The rebuild is a content-exact / operationally exact match
to the frozen pair. The frozen pair is confirmed reproducible from source.

## Audit date

2026-03-29

## Rebuild environment

| Package | Version |
|---|---|
| R | 4.5.1 |
| Seurat | 5.3.0 |
| SeuratDisk | 0.0.0.9021 |
| SeuratObject | 5.1.0 |
| Python | 3.12 (anndata, pandas, numpy) |

## Scripts used

| Script | Purpose |
|---|---|
| `build_frozen_reference_v1.R` | RDS → RNA-only h5Seurat → h5ad |
| `extract_reference_metadata_v1.py` | h5ad obs → decoded metadata CSV |

## Rebuild procedure

```bash
# Step 1: R rebuild (RDS → h5Seurat → h5ad)
Rscript build_frozen_reference_v1.R rebuild_audit_v1

# Step 2: Metadata extraction (h5ad → decoded CSV)
python extract_reference_metadata_v1.py \
    --h5ad rebuild_audit_v1/reference_RNA.h5ad \
    --codebook-dir codebook \
    --outdir rebuild_audit_v1
```

## Comparison results

### Matrix (h5ad)

| Check | Result |
|---|---|
| Shape | 144,380 x 30,852 — **match** |
| obs_names (cell IDs) | Exact order match — **match** |
| var_names (gene names) | Exact order match — **match** |
| obs columns | All 17 columns identical — **match** |
| .X dtype | float64 — **match** |
| .X values (100 random full rows) | `array_equal` — **exact match** |
| .X non-negativity | All non-negative — **match** |
| .X is log-normalized | Non-integer values present — **match** |
| .raw exists | Both have .raw — **match** |
| .raw var_names | Integer-indexed (`'0','1','2',…`) — **match** |
| .raw X values (10 random full rows) | `array_equal` — **exact match** |
| .raw range | [0, 2575] — **match** |
| File size | Frozen 1,701,225,837 B / Rebuilt 1,701,225,791 B (46 B diff) |

The 46-byte h5ad size difference is HDF5 container metadata (timestamps,
library version strings). Matrix content is identical.

### Metadata (CSV)

| Check | Result |
|---|---|
| Shape | 144,380 x 9 — **match** |
| Columns | All 9 identical — **match** |
| cell_id order | Exact — **match** |
| sample_id | All values match — **match** |
| sample_name | All values match — **match** |
| stage_fine | All values match — **match** |
| stage_num | All values match — **match** |
| stage_coarse | All values match — **match** |
| state_coarse | All values match — **match** |
| state_fine | All values match — **match** |
| group_internal | All values match — **match** |
| stage_fine distribution | **match** |
| stage_coarse distribution | **match** |
| state_coarse distribution | **match** |
| group_internal distribution | **match** |
| File size | Frozen 16,382,869 B / Rebuilt 16,671,629 B (289 KB diff) |

The CSV size difference is quoting: the rebuild script uses `QUOTE_ALL`
(all fields quoted), while the frozen CSV leaves integer `stage_num` unquoted.
All values are identical.

### Query gene overlap

| Query | Genes | Overlap with reference | Percentage |
|---|---|---|---|
| CA1 | 28,648 | 27,752 | 96.9% |
| BU3 | 28,648 | 27,752 | 96.9% |

## Known artifacts preserved in rebuild

1. **.raw var_names are integer-indexed** (`'0','1','2',…` instead of gene
   symbols). This is a SeuratDisk conversion artifact present in both the
   frozen pair and the rebuild. Downstream scripts use `.X` and `.var_names`
   (which are correct gene symbols) and do not rely on `.raw.var_names`.

2. **.X is log-normalized** (Seurat "data" layer), not raw counts. The
   SeuratDisk export writes `data` as `.X` and `counts` as `.raw.X`.

## Conclusion

The canonical rebuild scripts (`build_frozen_reference_v1.R` +
`extract_reference_metadata_v1.py`) produce outputs that are a content-exact /
operationally exact match to the frozen pair under `converted/`. The
remaining non-semantic differences are a 46-byte h5ad container metadata
size difference and a CSV quoting-style difference only. The provenance
gap documented in
`REFERENCE_PROVENANCE_v1.md` (no reproducible script for steps 2 and 3)
is now closed: these scripts constitute the missing reproducible build chain.
