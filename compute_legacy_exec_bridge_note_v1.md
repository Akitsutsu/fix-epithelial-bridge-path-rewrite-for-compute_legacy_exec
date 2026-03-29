# compute_legacy_exec bridge (Week 2 starter)

This bridge keeps the benchmark contract fixed while reusing the current legacy compute scripts.

## Strategy
- Keep `benchmark_common_runner_v2.py` unchanged.
- Swap command templates to call `whole_lung_project_common_v2.py` and `epithelial_only_remap_common_v2.py` in `--mode compute_legacy_exec`.
- For now, use the BU3 legacy scripts as the generic compute engine:
  - `project_BU3_to_reference_RNA_v1.py`
  - `epithelial_only_remap_BU3_v1.py`
- The adapters rewrite hard-coded paths and output prefixes in memory, then execute the legacy source.

## First validation target
Run CA1/BU3 through the compute bridge and compare against the replay baseline using:

```bash
python check_exemplar_reproduction_v1.py \
  --key-metrics benchmark_run_v1_compute_legacy/compare/all_queries_key_metrics.csv
```

## Interpretation of outcomes
- If CA1/BU3 both pass, the legacy BU3 scripts are acting as query-agnostic compute kernels.
- If BU3 passes but CA1 fails, the adapter worked but the legacy compute logic still contains hidden query-specific assumptions.
- If both fail early, inspect the adapter meta JSON and stdout/stderr logs for missing rewrite targets.
