# whole-lung combined-root outdir mismatch

## Problem
The current combined-root compute path is not canonical yet.

Observed behavior:
- self/self BU3 run writes:
  benchmark_run_gse237359_vs_BU3_BU3_compute/whole_lung/BU3/BU3_summary_v1.json
  benchmark_run_gse237359_vs_BU3_BU3_compute/whole_lung/BU3/BU3_cell_projection_v1.csv
- combined-root run expects:
  benchmark_run_gse237359_vs_CA1_BU3_compute/whole_lung/BU3/BU3_summary_v1.json
  benchmark_run_gse237359_vs_CA1_BU3_compute/whole_lung/BU3/BU3_cell_projection_v1.csv
- runner stops with "expected outputs are missing"

## Why this branch exists
To repair the whole-lung legacy compute bridge so combined-root runs become the canonical execution path again.

## Minimal reproduction target
- query: BU3
- stage: whole_lung
- reference: converted/reference_RNA.h5ad
- metadata: converted/reference_metadata_v1.csv

## Acceptance criteria
1. BU3 combined-root run writes summary + cell_projection into the combined-root whole_lung/BU3 directory.
2. CA1 + BU3 combined-root run reaches epithelial stage.
3. 6-query combined-root run reproduces the current self/self + multiroot comparison table.
