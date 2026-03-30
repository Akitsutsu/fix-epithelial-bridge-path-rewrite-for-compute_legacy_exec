# Reference drift reports

This directory holds drift-report outputs comparing candidate references
against the current release.

## How it works

The drift report compares a candidate (built by `build_reference_candidate_v1.R`
and `extract_reference_metadata_candidate_v1.py`) against the current release
registered in `references/registry/current_release.yaml`.

Two comparison levels:

1. **Structural** — matrix shape, obs/var overlap, metadata distributions,
   X layer properties, drop-in compatibility assessment
2. **Benchmark** — runs the existing benchmark runner twice (release vs candidate)
   and diffs the anchor-query key metrics (BU3, CA1)

## Usage

```bash
# Structural only
python run_reference_drift_report_v1.py \
  --candidate-dir references/candidates/2026-04-early-only \
  --outdir references/drift/2026-04-early-only \
  --tag 2026-04-early-only \
  --mode structural

# Both structural and benchmark
python run_reference_drift_report_v1.py \
  --candidate-dir references/candidates/2026-04-early-only \
  --outdir references/drift/2026-04-early-only \
  --tag 2026-04-early-only \
  --mode both \
  --manifest query_manifest_v1.csv \
  --whole-lung-cmd-template-file whole_lung_cmd_template_v1.txt \
  --epi-cmd-template-file epithelial_cmd_template_v1.txt
```

## Output structure

```text
references/drift/<tag>/
  REFERENCE_DRIFT_REPORT_<tag>.md               # human-readable report
  reference_drift_summary_<tag>.json             # machine-readable summary
  release_vs_candidate_structural_diff_<tag>.csv # structural comparison table
  anchor_key_metrics_diff_<tag>.csv              # benchmark diff (if run)
  benchmark_release/                             # release benchmark run (if run)
  benchmark_candidate/                           # candidate benchmark run (if run)
  logs/                                          # benchmark logs
```

## Design notes

- The release reference is resolved from the registry, not hard-coded paths
- Benchmark mode invokes `benchmark_common_runner_v2.py` unmodified
- No release-promotion logic is included — drift reports are informational only
- wholelung_gate_file path strings are treated as metadata noise, not biological drift

See `REFERENCE_UPDATE_SYSTEM_v1.md` for the full lifecycle design.
