"""Drop-in integration sketch for epithelial_only_remap_common_v2.py.

Usage pattern:
1. Copy epithelial_bridge_exec_debug_helper.py into the repo.
2. Import the helper symbols shown below.
3. Insert this block *after* the legacy source has been rewritten in memory and
   *before* calling exec().
4. Keep the outer CLI / runner semantics unchanged.

This is a sketch rather than a ready-to-run file because the original bridge
script is not present in the current workspace.
"""

from epithelial_bridge_exec_debug_helper import (  # noqa: F401
    ExecDebugContext,
    ExecDebugPaths,
    mark_exec_prepared,
    run_compiled_rewritten_source,
)

# Example variables assumed to already exist in epithelial_only_remap_common_v2.py:
# - query_id: str
# - outdir: str | Path
# - legacy_source_path: str | Path
# - rewritten_source: str
# - query_h5ad: str | Path
# - reference_h5ad: str | Path
# - reference_meta: str | Path
# - whole_lung_gate_csv: str | Path
# - replacements: dict[str, str]
# - exec_globals: dict[str, Any]

paths = ExecDebugPaths(stage_dir=outdir, query_id=query_id, stage_name="epithelial")
context = ExecDebugContext(
    query_id=query_id,
    stage_name="epithelial",
    original_source_path=str(legacy_source_path),
    query_h5ad=str(query_h5ad),
    reference_h5ad=str(reference_h5ad),
    reference_meta=str(reference_meta),
    whole_lung_gate_csv=str(whole_lung_gate_csv),
    outdir=str(outdir),
    replacements=dict(replacements),
    extra={
        # Optional but useful:
        # "bridge_mode": "compute_legacy_exec",
        # "runner_version": "benchmark_common_runner_v2",
    },
)
meta = mark_exec_prepared(
    paths=paths,
    context=context,
    rewritten_source=rewritten_source,
)

exec_globals.setdefault("__name__", "__main__")
exec_globals.setdefault("__file__", str(paths.rewritten_script_py))

run_compiled_rewritten_source(
    rewritten_source=rewritten_source,
    paths=paths,
    meta=meta,
    exec_globals=exec_globals,
)
