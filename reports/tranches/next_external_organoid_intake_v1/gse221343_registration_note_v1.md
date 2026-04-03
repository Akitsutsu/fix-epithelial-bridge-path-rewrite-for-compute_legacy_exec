# GSE221343 registration note

## Why this dataset is next

- Small, clean iPSC-derived alveolar epithelial scRNA dataset (3 samples, ~3400 cells total).
- Covers iAT2-to-iAT1 differentiation axis relevant to the lung epithelial reference.
- Published in Cell Stem Cell (Burgess et al. 2024, PMID 38642558).
- Lower integration friction than larger multi-condition or disease-heavy series.
- Processed supplementary files are per-sample CellRanger HDF5 (.h5), which are straightforward to convert.

## What is included in this commit

- `metadata/external/gse221343_dataset_manifest_v1.yaml` -- dataset-level registration manifest.
- This registration note.

This is **dataset-level registration only**.

## What is NOT included yet

- No local download of raw or supplementary files.
- No sample sheet v1.
- No h5ad conversion or gene-space inspection.
- No provenance audit or projection run.
- `query_ready_flag` remains `false`.

## Planned next steps

1. Download per-sample `.h5` files from GEO supplementary.
2. Convert to `.h5ad` and inspect obs metadata, gene space, and raw count layer.
3. Build `gse221343_organoid_query_sample_sheet_v1.tsv` (following GSE237359 format).
4. Run provenance audit and evaluate reference compatibility tier.
5. If compatible, add to query manifest and run whole-lung + epithelial projection.
