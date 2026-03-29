#!/usr/bin/env bash
set -euo pipefail

python benchmark_common_runner_v2.py \
  --manifest query_manifest_v1.csv \
  --outdir benchmark_run_v1_compute_legacy \
  --reference converted/reference_RNA.h5ad \
  --metadata converted/reference_metadata_v1.csv \
  --provenance-script provenance_audit_h5ad.py \
  --whole-lung-cmd-template-file whole_lung_cmd_template_compute_legacy_v1.txt \
  --epi-cmd-template-file epithelial_cmd_template_compute_legacy_v1.txt

python check_exemplar_reproduction_v1.py \
  --key-metrics benchmark_run_v1_compute_legacy/compare/all_queries_key_metrics.csv
