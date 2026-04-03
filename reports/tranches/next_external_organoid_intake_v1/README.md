# Next external organoid intake v1

## Objective
Start the next external organoid intake tranche on top of current release v1,
without changing the frozen reference.

## Starting point
- GSE237359 donor-resolved tranche is already fixed as a stable checkpoint.
- current release v1 remains:
  - converted/reference_RNA.h5ad
  - converted/reference_metadata_v1.csv
- current reproducible projection path is:
  per-query self/self runs + multiroot aggregation

## Intake requirements
A dataset is not treated as query-ready until:
1. dataset-level provenance is registered
2. sample sheet rows are created
3. local artifact structure is validated
4. donor/sample-resolved rows are defined where applicable
5. query_ready_flag criteria are satisfied

## Immediate tasks
1. choose the next external dataset tranche
2. register dataset-level provenance
3. build sample sheet v1
4. validate local artifact structure
5. promote validated rows to query-ready status
