# Week 2 compute parity playbook

## What I could verify here
I could only inspect the uploaded handoff and seed notes. The actual repo, stderr logs, and bridge scripts are not present in this workspace, so I could not read

- `benchmark_run_v1_compute_legacy/logs/CA1/epithelial.stderr.log`
- `benchmark_run_v1_compute_legacy/logs/BU3/epithelial.stderr.log`
- `epithelial_only_remap_common_v2.py`

That means I could not localize the live exception yet. I did, however, convert the stated next step into runnable helper artifacts so the next debug pass is immediate once the repo is available.

## What the handoff already establishes
- Week 1 replay is already stable under the common runner.
- Week 2 true compute bridge is localized to the epithelial compute path.
- Whole-lung compute bridge is already ok for CA1 and BU3.
- Epithelial compute fails for both CA1 and BU3 with `returncode=1`.
- `CA1_whole_lung_adapter_meta.json` exists, while `CA1_epithelial_adapter_meta.json` does not.
- The handoff explicitly recommends: read epithelial stderr, then add rewritten-source dump, full traceback capture, and pre-exec adapter meta, then rerun BU3 first.

## Files created in this workspace
### 1) `epithelial_bridge_exec_debug_helper.py`
Reusable helper that:
- writes the rewritten epithelial legacy source to a debug `.py`
- writes adapter meta JSON *before* execution
- compiles + execs the rewritten source
- writes a full traceback sidecar on failure
- updates adapter meta to `ok` or `failed`

### 2) `inspect_epi_bridge_failure.py`
Standalone triage script that scans an existing `benchmark_run_v1_compute_legacy/` tree and summarizes:
- presence/absence of epithelial stderr
- traceback / final exception line in stderr
- whole-lung vs epithelial adapter meta existence
- presence of `*_epi_summary_v1.json`, `*_epi_stage_fine*`, `*_epi_state_fine*`
- `all_queries_key_metrics.csv` epithelial-like columns

Example:
```bash
python inspect_epi_bridge_failure.py \
  --run-dir benchmark_run_v1_compute_legacy \
  --query-ids CA1 BU3 \
  --write-json benchmark_run_v1_compute_legacy/triage_summary.json
```

### 3) `epithelial_only_remap_common_v2_integration_snippet.py`
A drop-in integration sketch for `epithelial_only_remap_common_v2.py` showing exactly where to call the helper.

## Recommended execution sequence once repo is mounted
1. Run the inspection script first.
2. If stderr already contains a usable traceback, patch the real failure point directly.
3. If stderr is thin or empty, wire in the helper.
4. Rerun BU3 only.
5. Check for:
   - `BU3_epi_summary_v1.json`
   - `BU3_epi_stage_fine*`
   - `BU3_epi_state_fine*`
   - populated epithelial columns in `all_queries_key_metrics.csv`
6. Compare BU3 compute outputs against replay baseline.
7. Only then rerun CA1.

## Suggested acceptance gates
### Gate A: failure exposure
Pass if at least one of these becomes true after the next run:
- `epithelial.stderr.log` contains a concrete traceback
- `BU3_epithelial_traceback.txt` exists
- `BU3_epithelial_adapter_meta.json` exists with `status=failed`

### Gate B: BU3 compute parity
Pass if all are true:
- `BU3_epi_summary_v1.json` exists
- `BU3_epi_stage_fine*` exists
- `BU3_epi_state_fine*` exists
- BU3 epithelial metrics are populated in `all_queries_key_metrics.csv`

### Gate C: CA1 compute parity
Same as BU3, after BU3 is stable.

## Practical checks inside the rewritten debug script
When the rewritten debug `.py` is produced, search it for surviving hard-coded assumptions such as:
- `CA1_` or `BU3_` output basenames in places that should be query-agnostic
- legacy output dirs like `prototype_out_epi_v1` / `prototype_out_epi_v1_BU3`
- fixed `WHOLELUNG_GATE_CSV` paths or original gate filenames
- original query file literals instead of the manifest-provided query path

## Minimal note for the next compute pass
Keep the strategy narrow:
- do not redesign the pipeline yet
- expose the epithelial failure point first
- stabilize BU3 before widening to CA1 and then new queries
