# Artifact Lifecycle Registry v2

## Date
2026-04-08

## Supersedes
`reports/artifact_lifecycle_registry_v1/` (6 tranches, summary pointer v2).
v1 is retained as a historical snapshot and is not deleted.

## Purpose
Single-file registry of all tranche-level artifacts in the repository,
organized by lifecycle stage. Answers: "which artifact is the current
source of truth, and how far has each tranche progressed?"

Updated to reflect GSE221344 paired promotion (D-0014) and comparison
world v3.

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
| Current comparison-world summary | `reports/comparison_world_biology_summary_v3/` |
| Current lifecycle registry | `reports/artifact_lifecycle_registry_v2/` |
| Prediction registry | `reports/prediction_registry_v1/` (unchanged) |

## What should be treated as non-canonical

| Category | Examples |
|----------|---------|
| Superseded summaries | `reports/comparison_world_biology_summary_v1/`, `reports/comparison_world_biology_summary_v2/` (historical snapshots) |
| Superseded registries | `reports/artifact_lifecycle_registry_v1/` (historical snapshot) |
| Local projection workdirs | `benchmark_review_*_v1/` (not committed; local only) |
| Raw downloads | `queries/raw/` (not committed) |
| Scratch / candidate search | `reports/tranches/next_external_intake_*` |
| Auth / token artifacts | never committed |

## Registry

See `tranche_lifecycle_registry_v2.tsv` for the machine-readable registry.

### Summary

| Tranche | Status | Rows in world | Decision | Stage reached |
|---------|--------|--------------|----------|---------------|
| CA1/BU3 | accepted_fixed | 2 | -- | projection (multiroot) |
| GSE237359 | accepted_fixed | 4 | D-0007 | projection (multiroot) |
| GSE221343 | accepted_query_ready | 3 | D-0010 | Gate A-D review |
| GSE289846 | accepted_query_ready | 3 | D-0011 | Gate A-D review |
| GSE308817 | accepted_query_ready | 3 | D-0012 | Gate A-D review |
| GSE193716 | accepted_query_ready | 3 (iAEC2 subset) | D-0013 | Gate A-D review (subset) |
| **GSE221344** | **accepted_query_ready** | **2** | **D-0014** | **Gate A-D review (paired)** |

### What changed from v1

| Change | v1 | v2 |
|--------|----|----|
| Tranches | 6 | 7 |
| GSE221344 | not listed | accepted_query_ready, 2 rows, D-0014 |
| Current summary pointer | v2 | v3 |
| Superseded summaries | v1 only | v1 + v2 |

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
| `tranche_lifecycle_registry_v2.tsv` | Machine-readable lifecycle registry (7 rows, 15 columns) |
