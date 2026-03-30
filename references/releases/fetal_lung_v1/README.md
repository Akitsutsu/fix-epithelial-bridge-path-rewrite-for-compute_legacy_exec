# fetal_lung_v1

This directory represents release v1 of the versioned fetal lung reference.

## Important: pointer-based design

Release v1 does **not** duplicate the frozen pair into this directory.
The operational files remain at their original locations:

- `converted/reference_RNA.h5ad` (144,380 cells x 30,852 genes)
- `converted/reference_metadata_v1.csv` (144,380 rows x 9 columns)

This directory exists to anchor the release identity within the
`references/releases/` structure proposed in `REFERENCE_UPDATE_SYSTEM_v1.md`.

## Associated artifacts

All of these are at the repo root (not copied here):

| Artifact | Path |
|---|---|
| Provenance | `REFERENCE_PROVENANCE_v1.md` |
| Provenance audit | `REFERENCE_PROVENANCE_AUDIT_v1.md` |
| Audit summary (JSON) | `provenance_audit_v1_summary.json` |
| Build script (R) | `build_frozen_reference_v1.R` |
| Metadata script (Python) | `extract_reference_metadata_v1.py` |
| Codebook directory | `codebook/` |

## Registry

This release is registered in `references/registry/REFERENCE_REGISTRY.csv`
and declared as the current operational release in
`references/registry/current_release.yaml`.

## Upstream source

| Item | Value |
|---|---|
| GEO accession | GSE264407 |
| Source file | `GSE264407_full_fetal_lung_dataset_04142025.rds` |
| Publication | Wong et al. 2024, fetal lung epithelial atlas |

## Audit verdict

**MATCH** — rebuild is content-exact / operationally exact match to frozen pair.
See `REFERENCE_PROVENANCE_AUDIT_v1.md` for full details.
