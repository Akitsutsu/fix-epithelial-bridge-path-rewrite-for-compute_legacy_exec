# Artifact Lifecycle Registry v4

## Date
2026-04-10

## Supersedes
`reports/artifact_lifecycle_registry_v3/` (8 tranches, summary pointer v4).
v3 is retained as a historical snapshot and is not deleted.

## Purpose
Single-file registry of all tranche-level artifacts in the repository,
organized by lifecycle stage.

Updated to reflect GSE246243 same-line kinetic tranche promotion and
comparison world v5.

## Registry

See `tranche_lifecycle_registry_v4.tsv` for the machine-readable registry.

### Summary

| Tranche | Status | Rows in world | Stage reached |
|---------|--------|--------------|---------------|
| CA1/BU3 | accepted_fixed | 2 | projection (multiroot) |
| GSE237359 | accepted_fixed | 4 | projection (multiroot) |
| GSE221343 | accepted_query_ready | 3 | Gate A-D review |
| GSE289846 | accepted_query_ready | 3 | Gate A-D review |
| GSE308817 | accepted_query_ready | 3 | Gate A-D review |
| GSE193716 | accepted_query_ready | 3 (iAEC2 subset) | Gate A-D review (subset) |
| GSE221344 | accepted_query_ready | 2 | Gate A-D review (paired) |
| GSE221342 | accepted_query_ready | 4 | Gate A-D review (boundary-stress) |
| **GSE246243** | **accepted_query_ready** | **4** | **Gate A-D review (kinetic)** |

### What changed from v3

| Change | v3 | v4 |
|--------|----|----|
| Tranches | 8 | 9 |
| GSE246243 | not listed | accepted_query_ready, 4 rows |
| Current summary pointer | v4 | v5 |

## What counts as canonical surface

| Category | Path(s) |
|----------|---------|
| Current comparison-world summary | `reports/comparison_world_biology_summary_v5/` |
| Current lifecycle registry | `reports/artifact_lifecycle_registry_v4/` |
| Prediction registry | `reports/prediction_registry_v2/` (unchanged) |

## Files in this directory

| File | Description |
|------|-------------|
| `README.md` | This file |
| `tranche_lifecycle_registry_v4.tsv` | Machine-readable lifecycle registry (9 rows, 15 columns) |
