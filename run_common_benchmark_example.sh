#!/usr/bin/env bash
set -euo pipefail

python benchmark_common_runner_v1.py \
  --manifest query_manifest_v1.example.csv \
  --outdir benchmark_run_v1 \
  --reference converted/reference_RNA.h5ad \
  --metadata converted/reference_metadata_v1.csv \
  --stage-axis sample_week \
  --provenance-script provenance_audit_h5ad.py \
  --whole-lung-cmd-template 'python whole_lung_project_common_v1.py --reference {reference} --metadata {metadata} --query-id {query_id} --query-h5ad {h5ad_path} --stage-axis {stage_axis} --outdir {whole_lung_outdir}' \
  --epi-cmd-template 'python epithelial_only_remap_common_v1.py --reference {reference} --metadata {metadata} --query-id {query_id} --query-h5ad {h5ad_path} --stage-axis {stage_axis} --whole-lung-summary {whole_lung_summary_json} --whole-lung-projection {whole_lung_cell_projection_csv} --outdir {epi_outdir}'
