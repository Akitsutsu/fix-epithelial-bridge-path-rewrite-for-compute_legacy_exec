# Reference candidates

This directory holds candidate reference builds that are under evaluation
and have not yet been promoted to a release.

## How it works

1. Build a candidate h5ad using `build_reference_candidate_v1.R`
2. Extract metadata using `extract_reference_metadata_candidate_v1.py`
3. Each candidate gets its own subdirectory named by its tag

## Example

```bash
# Step 1: Build candidate (early gestational weeks only)
Rscript build_reference_candidate_v1.R \
  --source-rds full_fetal_lung_dataset.rds \
  --outdir references/candidates/2026-04-early-only \
  --tag 2026-04-early-only \
  --sample-week-include week_10,week_11,week_12,week_13

# Step 2: Extract metadata
python extract_reference_metadata_candidate_v1.py \
  --h5ad references/candidates/2026-04-early-only/reference_RNA.h5ad \
  --codebook-dir codebook \
  --outdir references/candidates/2026-04-early-only \
  --tag 2026-04-early-only
```

## Candidate directory structure

```text
references/candidates/<tag>/
  reference_RNA.h5Seurat
  reference_RNA.h5ad
  reference_metadata.csv
  build_versions.csv
  build_manifest.yaml
  extract_metadata_summary.json
```

## Relationship to releases

Candidates are mutable and may be rebuilt during evaluation.
Only promoted candidates become immutable releases under `references/releases/`.

See `REFERENCE_UPDATE_SYSTEM_v1.md` for the full lifecycle design.
