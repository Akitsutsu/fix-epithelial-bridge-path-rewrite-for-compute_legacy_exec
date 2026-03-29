# Week 1 replay adapters

These adapters let `benchmark_common_runner_v1.py` complete end-to-end for CA1/BU3
without first refactoring the legacy compute scripts into argparse-based CLIs.

Important:
- This validates the **manifest**, **preflight provenance**, **fixed output layout**,
  and **compare-table assembly**.
- It does **not** constitute a fresh remap/recompute.
- The source of truth remains the frozen legacy outputs under `prototype_out_v1/`,
  `prototype_out_epi_v1/`, and `prototype_out_epi_v1_BU3/`.

## Required files to place in `lungs_analysis/`
- `whole_lung_project_common_v1.py`
- `epithelial_only_remap_common_v1.py`
- `legacy_output_manifest_v1.csv` (copy from the example and rename)
- `whole_lung_cmd_template_replay_v1.txt`
- `epithelial_cmd_template_replay_v1.txt`

## First run
```bash
cp query_manifest_v1.example.csv query_manifest_v1.csv
cp legacy_output_manifest_v1.example.csv legacy_output_manifest_v1.csv

python benchmark_common_runner_v1.py \
  --manifest query_manifest_v1.csv \
  --outdir benchmark_run_v1_replay \
  --reference converted/reference_RNA.h5ad \
  --metadata converted/reference_metadata_v1.csv \
  --provenance-script provenance_audit_h5ad.py \
  --whole-lung-cmd-template-file whole_lung_cmd_template_replay_v1.txt \
  --epi-cmd-template-file epithelial_cmd_template_replay_v1.txt
```

## Expected effect
The runner will materialize standardized per-query outputs into:
- `benchmark_run_v1_replay/whole_lung/<query_id>/...`
- `benchmark_run_v1_replay/epithelial/<query_id>/...`

Then it will build compare outputs from those standardized locations.

## Next step after replay passes
Refactor true compute into:
- `whole_lung_project_common_v1.py` as a real projector
- `epithelial_only_remap_common_v1.py` as a real remapper

The CLI contract should stay unchanged.
