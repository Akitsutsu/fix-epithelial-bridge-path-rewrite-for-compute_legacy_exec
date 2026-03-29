# Next-step runbook for CA1 / BU3

Frozen assumptions carried forward:

- `reference = converted/reference_RNA.h5ad`
- `metadata = converted/reference_metadata_v1.csv`
- stage axis uses `sample_week`
- do **not** use `gestational_week`
- `whole-lung v1` is frozen
- `two-stage = whole-lung lineage gate -> epithelial-only remap`

## 1) Exact provenance audit from query obs

This does **not** modify the frozen reference or remap basis.

```bash
python provenance_audit_h5ad.py \
  --input CA1=converted/query_CA1_clean.h5ad BU3=converted/query_BU3_clean.h5ad \
  --outdir provenance_audit_v1
```

Key outputs:

- `provenance_audit_v1/CA1/CA1_provenance_summary.md`
- `provenance_audit_v1/CA1/CA1_provenance_exact_combinations.csv`
- `provenance_audit_v1/CA1/CA1_provenance_sample_id.csv`
- `provenance_audit_v1/CA1/CA1_provenance_donor_id.csv`
- `provenance_audit_v1/CA1/CA1_provenance_source_type.csv`
- `provenance_audit_v1/CA1/CA1_provenance_batch_id.csv`

and the same set for `BU3`, plus:

- `provenance_audit_v1/all_queries_provenance_overview.csv`
- `provenance_audit_v1/all_queries_target_field_presence.csv`

Interpretation target:

- confirm whether each query is single-source or mixed across
  `sample_id / donor_id / source_type / batch_id`
- see whether `CA1 mixed-ness` is biological-state mixed only, or whether
  metadata provenance is also mixed
- see whether `BU3 convergence` is accompanied by a tighter provenance footprint

## 2) Minimal readout to paste back into the project log

For each query, record:

- `n_cells_total`
- available target fields
- top exact provenance combination
- fraction explained by top combination
- number of exact provenance combinations
- whether any requested field is missing

## 3) If you roll out to a new query next

Keep the current frozen basis, then do in order:

1. exact provenance audit from query obs
2. whole-lung lineage gate
3. epithelial-only remap
4. compare new query against existing `CA1 / BU3` tables
5. only after that, decide whether the new query belongs in the same
   proximal-airway-like bucket or needs a separate branch
