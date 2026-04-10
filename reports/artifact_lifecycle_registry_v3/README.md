# Artifact Lifecycle Registry v3

## Date
2026-04-10

## Supersedes
`reports/artifact_lifecycle_registry_v2/` (7 tranches, summary pointer v3).
v2 is retained as a historical snapshot and is not deleted.

## Purpose
Single-file registry of all tranche-level artifacts in the repository,
organized by lifecycle stage. Answers: "which artifact is the current
source of truth, and how far has each tranche progressed?"

Updated to reflect GSE221342 boundary-stress tranche promotion and
comparison world v4.

## What counts as canonical surface

The following files and directories constitute the canonical surface of
the project. Changes to these should be deliberate and logged.

| Category | Path(s) |
|----------|---------|
| Research scope | `research_scope.md` |
| Data contract | `data_contract.yaml` |
| Decision log | `decision_log.md` |
| Agent instructions | `AGENTS.md`, `CLAUDE.md` |
| Current release | `references/registry/current_release.yaml` |
| Reference registry | `references/registry/REFERENCE_REGISTRY.csv` |
| Query manifest | `query_manifest_v1.csv` |
| Dataset manifests | `metadata/external/*_dataset_manifest_v*.yaml` |
| Sample sheets | `metadata/external/*_organoid_query_sample_sheet_v*.tsv` |
| Accepted tranche review artifacts | `reports/tranches/*/` (with decision TSVs) |
| Current comparison-world summary | `reports/comparison_world_biology_summary_v4/` |
| Current lifecycle registry | `reports/artifact_lifecycle_registry_v3/` |
| Prediction registry | `reports/prediction_registry_v1/` (unchanged) |

## What should be treated as non-canonical

| Category | Examples |
|----------|---------|
| Superseded summaries | `reports/comparison_world_biology_summary_v1/`, `v2/`, `v3/` (historical snapshots) |
| Superseded registries | `reports/artifact_lifecycle_registry_v1/`, `v2/` (historical snapshots) |
| Local projection workdirs | `benchmark_review_*_v1/` (not committed; local only) |
| Raw downloads | `queries/raw/` (not committed) |
| Scratch / candidate search | `reports/tranches/next_external_intake_*` |
| Auth / token artifacts | never committed |

## Registry

See `tranche_lifecycle_registry_v3.tsv` for the machine-readable registry.

### Summary

| Tranche | Status | Rows in world | Decision | Stage reached |
|---------|--------|--------------|----------|---------------|
| CA1/BU3 | accepted_fixed | 2 | -- | projection (multiroot) |
| GSE237359 | accepted_fixed | 4 | D-0007 | projection (multiroot) |
| GSE221343 | accepted_query_ready | 3 | D-0010 | Gate A-D review |
| GSE289846 | accepted_query_ready | 3 | D-0011 | Gate A-D review |
| GSE308817 | accepted_query_ready | 3 | D-0012 | Gate A-D review |
| GSE193716 | accepted_query_ready | 3 (iAEC2 subset) | D-0013 | Gate A-D review (subset) |
| GSE221344 | accepted_query_ready | 2 | D-0014 | Gate A-D review (paired) |
| **GSE221342** | **accepted_query_ready** | **4** | **accepted_query_ready** | **Gate A-D review (boundary-stress)** |

### What changed from v2

| Change | v2 | v3 |
|--------|----|----|
| Tranches | 7 | 8 |
| GSE221342 | not listed | accepted_query_ready, 4 rows |
| Current summary pointer | v3 | v4 |
| Superseded summaries | v1 + v2 | v1 + v2 + v3 |

### Lifecycle stages

1. **Registration** -- manifest + sample sheet created
2. **Audit** -- gene-space / build / overlap verified
3. **Conversion** -- H5/MTX -> H5AD with provenance
4. **Projection** -- whole-lung + epithelial on release v1
5. **Review** -- Gate A-D evaluation
6. **Decision** -- explicit reviewer promotion or hold
7. **Accepted** -- enters comparison world

## Files in this directory

| File | Description |
|------|-------------|
| `README.md` | This file |
| `tranche_lifecycle_registry_v3.tsv` | Machine-readable lifecycle registry (8 rows, 15 columns) |
