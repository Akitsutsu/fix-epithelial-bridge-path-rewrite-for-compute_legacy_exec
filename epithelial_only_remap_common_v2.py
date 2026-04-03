#!/usr/bin/env python3
"""
Epithelial common adapter v2.

Modes
-----
copy_existing / symlink_existing
    Replay existing epithelial outputs into the common runner layout.
compute_legacy_exec
    Execute a legacy epithelial remap script after in-memory rewriting of the
    hard-coded reference/query/gate/output constants and output filename
    prefixes.

This keeps the frozen biology while standardizing the I/O contract.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shutil
import sys
import traceback
from pathlib import Path
from typing import Dict, Optional, Tuple


MANIFEST_REQUIRED_COLUMNS = [
    "query_id",
    "epi_summary",
    "epi_state_fine",
    "epi_stage_fine",
    "epi_lineage_off_target_state_coarse",
]
MANIFEST_OPTIONAL_COLUMNS = [
    "epi_stable_state_marker_summary",
    "epi_boundary_pairs_unordered",
    "epi_boundary_pair_direction_marker_summary",
]


class UserFacingError(RuntimeError):
    pass


def resolve_path(value: Optional[str], base_dir: Path) -> Optional[Path]:
    if value is None:
        return None
    s = str(value).strip()
    if s == "" or s.lower() == "nan":
        return None
    p = Path(s)
    if not p.is_absolute():
        p = (base_dir / p).resolve()
    else:
        p = p.resolve()
    return p


def load_manifest_row(manifest_path: Path, query_id: str) -> Dict[str, str]:
    try:
        with open(manifest_path, "r", encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
    except Exception as e:
        raise UserFacingError(f"Failed to read legacy output manifest {manifest_path}: {e}") from e

    if not rows:
        raise UserFacingError(f"Legacy output manifest is empty: {manifest_path}")

    missing_cols = [c for c in MANIFEST_REQUIRED_COLUMNS if c not in rows[0].keys()]
    if missing_cols:
        raise UserFacingError(
            f"Legacy output manifest is missing required columns: {', '.join(missing_cols)}"
        )

    matches = [r for r in rows if str(r.get("query_id", "")).strip() == query_id]
    if not matches:
        raise UserFacingError(f"query_id={query_id!r} not found in legacy output manifest {manifest_path}")
    if len(matches) > 1:
        raise UserFacingError(f"query_id={query_id!r} appears multiple times in {manifest_path}")
    return matches[0]


def materialize(src: Path, dst: Path, mode: str) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() or dst.is_symlink():
        dst.unlink()
    if mode == "copy_existing":
        shutil.copy2(src, dst)
    elif mode == "symlink_existing":
        os.symlink(src, dst)
    else:
        raise UserFacingError(f"Unsupported materialize mode: {mode}")


def _replace_assignment(source: str, name: str, py_expr: str) -> Tuple[str, int]:
    pattern = rf"(?m)^({re.escape(name)}\s*=\s*).*$"
    new_source, n = re.subn(pattern, rf"\1{py_expr}", source)
    return new_source, n


def _replace_path_literals(source: str, replacements: Dict[str, str]) -> Tuple[str, Dict[str, int]]:
    counts: Dict[str, int] = {}
    out = source
    for old, new in replacements.items():
        n = out.count(old)
        if n:
            out = out.replace(old, new)
        counts[old] = n
    return out, counts

def _replace_prefix_tokens(source: str, query_id: str) -> Tuple[str, Dict[str, int]]:
    counts = {"CA1_": source.count("CA1_"), "BU3_": source.count("BU3_")}
    out = source.replace("CA1_", f"{query_id}_").replace("BU3_", f"{query_id}_")
    return out, counts


def _legacy_rel(p: Path, project_root: Path) -> str:
    p = p.resolve()
    project_root = project_root.resolve()
    try:
        return p.relative_to(project_root).as_posix()
    except ValueError:
        return p.as_posix()

def _rewrite_epi_legacy_source(
    source: str,
    *,
    reference: Path,
    metadata: Path,
    query_h5ad: Path,
    whole_lung_projection: Path,
    outdir: Path,
    query_id: str,
    project_root: Path,
) -> Tuple[str, Dict[str, object]]:
    debug: Dict[str, object] = {}
    out = source

    # Step 1: Prefix token replacement FIRST, on the original source.
    # This changes output-filename prefixes (BU3_/CA1_ → query_id_) without
    # corrupting paths that will be inserted by later steps.
    out, prefix_counts = _replace_prefix_tokens(out, query_id)
    debug["prefix_token_counts"] = prefix_counts

    # Step 2: Replace constant assignments (definitive — replaces entire RHS).
    out, n_ref = _replace_assignment(
        out, "REFERENCE_H5AD", repr(_legacy_rel(reference, project_root)))
    out, n_meta = _replace_assignment(
        out, "REFERENCE_META", repr(_legacy_rel(metadata, project_root)))
    out, n_qry = _replace_assignment(
        out, "QUERY_H5AD", repr(_legacy_rel(query_h5ad, project_root)))
    out, n_gate = _replace_assignment(
        out, "WHOLELUNG_GATE_CSV", repr(_legacy_rel(whole_lung_projection, project_root)))
    out, n_outdir = _replace_assignment(
        out, "OUTDIR", repr(outdir.as_posix()))

    debug["assignment_replacements"] = {
        "REFERENCE_H5AD": n_ref,
        "REFERENCE_META": n_meta,
        "QUERY_H5AD": n_qry,
        "WHOLELUNG_GATE_CSV": n_gate,
        "OUTDIR": n_outdir,
    }

    # Step 3: Literal path replacements (safety net for non-assignment refs).
    # After prefix replacement, BU3_ tokens are now query_id_ tokens, so use
    # query_id-based patterns.
    ref_rel = _legacy_rel(reference, project_root)
    meta_rel = _legacy_rel(metadata, project_root)
    qry_rel = _legacy_rel(query_h5ad, project_root)
    gate_rel = _legacy_rel(whole_lung_projection, project_root)

    out, path_counts = _replace_path_literals(
        out,
        {
            "converted/reference_RNA.h5ad": ref_rel,
            "converted/reference_metadata_v1.csv": meta_rel,
            f"converted/query_{query_id}_clean.h5ad": qry_rel,
            f"prototype_out_v1/{query_id}_cell_projection_v1.csv": gate_rel,
            "prototype_out_epi_v1": outdir.as_posix(),
            f"prototype_out_epi_v1_{query_id}": outdir.as_posix(),
        },
    )
    debug["literal_path_replacements"] = path_counts

    # Step 4: Forced outdir override (belt-and-suspenders, matches whole-lung
    # adapter pattern).
    forced_outdir_line = f'outdir = Path(r"{outdir.as_posix()}")'
    out, n_forced_outdir = re.subn(
        r'(?m)^([ \t]*)outdir\s*=\s*.*$',
        rf'\1{forced_outdir_line}',
        out,
        count=1,
    )
    debug["forced_outdir_replacements"] = n_forced_outdir
    debug["forced_outdir"] = str(outdir)

    # Step 5: Force mkdir parents=True (safety net).
    out, n_mkdir = re.subn(
        r'(?m)^([ \t]*)outdir\.mkdir\([^\n]*\)\s*$',
        r'\1outdir.mkdir(parents=True, exist_ok=True)',
        out,
    )
    debug["outdir_mkdir_replacements"] = n_mkdir

    debug["contains_main"] = ("def main(" in out)
    debug["contains_state_fine_output"] = ("_epi_state_fine.csv" in out)
    debug["contains_stage_fine_output"] = ("_epi_stage_fine.csv" in out)
    return out, debug


def run_compute_legacy_exec(
    *,
    legacy_script: Path,
    reference: Path,
    metadata: Path,
    query_h5ad: Path,
    whole_lung_summary: Path,
    whole_lung_projection: Path,
    outdir: Path,
    query_id: str,
    project_root: Path,
) -> Dict[str, object]:
    if not legacy_script.exists():
        raise UserFacingError(f"legacy script not found: {legacy_script}")
    if not whole_lung_summary.exists() or not whole_lung_projection.exists():
        raise UserFacingError(
            f"whole-lung prerequisites missing: summary_exists={whole_lung_summary.exists()} projection_exists={whole_lung_projection.exists()}"
        )

    source = legacy_script.read_text(encoding="utf-8")
    rewritten, debug = _rewrite_epi_legacy_source(
        source,
        reference=reference,
        metadata=metadata,
        query_h5ad=query_h5ad,
        whole_lung_projection=whole_lung_projection,
        outdir=outdir,
        query_id=query_id,
        project_root=project_root,
    )

    # --- Debug dump: write rewritten source for inspection ---
    debug_script = outdir / f"{query_id}_epithelial_rewritten_debug.py"
    debug_script.write_text(rewritten, encoding="utf-8")
    debug["rewritten_debug_path"] = str(debug_script)

    # --- Pre-exec adapter meta ---
    adapter_meta_path = outdir / f"{query_id}_epithelial_adapter_meta.json"
    pre_meta: Dict[str, object] = {
        "status": "prepared",
        "adapter": "epithelial_only_remap_common_v2.py",
        "mode": "compute_legacy_exec",
        "query_id": query_id,
        "legacy_script": str(legacy_script),
        "project_root": str(project_root),
        "rewrite_debug": debug,
    }
    with open(adapter_meta_path, "w", encoding="utf-8") as f:
        json.dump(pre_meta, f, ensure_ascii=False, indent=2)

    expected_required = [
        outdir / f"{query_id}_epi_summary_v1.json",
        outdir / f"{query_id}_epi_state_fine.csv",
        outdir / f"{query_id}_epi_stage_fine.csv",
        outdir / f"{query_id}_lineage_off_target_state_coarse.csv",
    ]
    expected_optional = [
        outdir / f"{query_id}_stable_state_marker_summary.csv",
        outdir / f"{query_id}_epi_state_boundary_pairs_unordered.csv",
        outdir / f"{query_id}_boundary_pair_direction_marker_summary.csv",
    ]

    ns = {
        "__name__": "__main__",
        "__file__": str(legacy_script),
        "Path": Path,
    }
    old_argv = sys.argv[:]
    sys.argv = [str(legacy_script)]
    try:
        exec(compile(rewritten, str(legacy_script), "exec"), ns, ns)
    except Exception:
        tb_text = traceback.format_exc()
        tb_path = outdir / f"{query_id}_epithelial_traceback.txt"
        tb_path.write_text(tb_text, encoding="utf-8")
        pre_meta["status"] = "failed"
        pre_meta["traceback_path"] = str(tb_path)
        tail = tb_text.strip().splitlines()
        pre_meta["exception_tail"] = tail[-1] if tail else ""
        with open(adapter_meta_path, "w", encoding="utf-8") as f:
            json.dump(pre_meta, f, ensure_ascii=False, indent=2)
        raise
    finally:
        sys.argv = old_argv

    missing_required = [str(p) for p in expected_required if not p.exists()]
    if missing_required:
        raise UserFacingError(
            "legacy epithelial compute finished but expected required outputs are missing: "
            + ", ".join(missing_required)
        )

    return {
        "legacy_script": str(legacy_script),
        "project_root": str(project_root),
        "required_outputs": [str(p) for p in expected_required],
        "optional_outputs_present": [str(p) for p in expected_optional if p.exists()],
        "optional_outputs_missing": [str(p) for p in expected_optional if not p.exists()],
        "rewrite_debug": debug,
        "note": "Epithelial outputs computed by in-memory execution of rewritten legacy source.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Epithelial common adapter v2")
    parser.add_argument("--reference", required=True)
    parser.add_argument("--metadata", required=True)
    parser.add_argument("--query-id", required=True)
    parser.add_argument("--query-h5ad", required=True)
    parser.add_argument("--stage-axis", default="sample_week")
    parser.add_argument("--whole-lung-summary", required=True)
    parser.add_argument("--whole-lung-projection", required=True)
    parser.add_argument("--outdir", required=True)
    parser.add_argument(
        "--mode",
        choices=["copy_existing", "symlink_existing", "compute_legacy_exec"],
        default="copy_existing",
    )
    parser.add_argument("--legacy-output-manifest", default=None)
    parser.add_argument("--source-summary", default=None)
    parser.add_argument("--source-state-fine", default=None)
    parser.add_argument("--source-stage-fine", default=None)
    parser.add_argument("--source-lineage-off-target", default=None)
    parser.add_argument("--source-stable-marker", default=None)
    parser.add_argument("--source-boundary-pairs", default=None)
    parser.add_argument("--source-boundary-direction-marker", default=None)
    parser.add_argument("--legacy-script", default=None)
    parser.add_argument("--project-root", default=None,
                        help="Project root for repo-relative path resolution (default: cwd)")
    args = parser.parse_args()

    query_id = str(args.query_id).strip()
    if not query_id:
        raise UserFacingError("query_id must not be empty")
    outdir = Path(args.outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    reference = Path(args.reference).resolve()
    metadata = Path(args.metadata).resolve()
    query_h5ad = Path(args.query_h5ad).resolve()
    whole_lung_summary = Path(args.whole_lung_summary).resolve()
    whole_lung_projection = Path(args.whole_lung_projection).resolve()
    for p, label in [
        (reference, "reference"),
        (metadata, "metadata"),
        (query_h5ad, "query_h5ad"),
        (whole_lung_summary, "whole_lung_summary"),
        (whole_lung_projection, "whole_lung_projection"),
    ]:
        if not p.exists():
            raise UserFacingError(f"{label} not found: {p}")

    if str(args.stage_axis) != "sample_week":
        raise UserFacingError(
            f"stage_axis must remain sample_week for the frozen benchmark, got: {args.stage_axis!r}"
        )

    meta: Dict[str, object]
    if args.mode in {"copy_existing", "symlink_existing"}:
        source_map = {
            "summary": Path(args.source_summary).resolve() if args.source_summary else None,
            "state_fine": Path(args.source_state_fine).resolve() if args.source_state_fine else None,
            "stage_fine": Path(args.source_stage_fine).resolve() if args.source_stage_fine else None,
            "lineage_off_target": Path(args.source_lineage_off_target).resolve() if args.source_lineage_off_target else None,
            "stable_marker": Path(args.source_stable_marker).resolve() if args.source_stable_marker else None,
            "boundary_pairs": Path(args.source_boundary_pairs).resolve() if args.source_boundary_pairs else None,
            "boundary_direction_marker": Path(args.source_boundary_direction_marker).resolve() if args.source_boundary_direction_marker else None,
        }
        source_manifest = None

        if args.legacy_output_manifest:
            manifest_path = Path(args.legacy_output_manifest).resolve()
            row = load_manifest_row(manifest_path, query_id)
            source_manifest = str(manifest_path)
            base = manifest_path.parent
            fill = {
                "summary": ("epi_summary",),
                "state_fine": ("epi_state_fine",),
                "stage_fine": ("epi_stage_fine",),
                "lineage_off_target": ("epi_lineage_off_target_state_coarse",),
                "stable_marker": ("epi_stable_state_marker_summary",),
                "boundary_pairs": ("epi_boundary_pairs_unordered",),
                "boundary_direction_marker": ("epi_boundary_pair_direction_marker_summary",),
            }
            for key, cols in fill.items():
                if source_map[key] is None:
                    for col in cols:
                        source_map[key] = resolve_path(row.get(col), base)
                        if source_map[key] is not None:
                            break

        required_sources = [
            source_map["summary"],
            source_map["state_fine"],
            source_map["stage_fine"],
            source_map["lineage_off_target"],
        ]
        if any(p is None for p in required_sources):
            raise UserFacingError(
                "Need epithelial required sources. Provide explicit --source-* args or --legacy-output-manifest."
            )

        missing_required = [str(p) for p in required_sources if p is None or not p.exists()]
        if missing_required:
            raise UserFacingError(f"Missing epithelial required source files: {', '.join(missing_required)}")

        targets = {
            "summary": outdir / f"{query_id}_epi_summary_v1.json",
            "state_fine": outdir / f"{query_id}_epi_state_fine.csv",
            "stage_fine": outdir / f"{query_id}_epi_stage_fine.csv",
            "lineage_off_target": outdir / f"{query_id}_lineage_off_target_state_coarse.csv",
            "stable_marker": outdir / f"{query_id}_stable_state_marker_summary.csv",
            "boundary_pairs": outdir / f"{query_id}_epi_state_boundary_pairs_unordered.csv",
            "boundary_direction_marker": outdir / f"{query_id}_boundary_pair_direction_marker_summary.csv",
        }

        for key in ["summary", "state_fine", "stage_fine", "lineage_off_target"]:
            materialize(source_map[key], targets[key], args.mode)

        optional_materialized = {}
        for key in ["stable_marker", "boundary_pairs", "boundary_direction_marker"]:
            src = source_map[key]
            if src is not None and src.exists():
                materialize(src, targets[key], args.mode)
                optional_materialized[key] = str(targets[key])
            else:
                optional_materialized[key] = None

        meta = {
            "adapter": "epithelial_only_remap_common_v2.py",
            "mode": args.mode,
            "query_id": query_id,
            "query_h5ad": str(query_h5ad),
            "reference": str(reference),
            "metadata": str(metadata),
            "stage_axis": args.stage_axis,
            "whole_lung_summary": str(whole_lung_summary),
            "whole_lung_projection": str(whole_lung_projection),
            "source_manifest": source_manifest,
            "source_files": {k: (str(v) if v is not None else None) for k, v in source_map.items()},
            "target_files": {k: str(v) for k, v in targets.items()},
            "optional_materialized": optional_materialized,
            "note": "Compatibility replay from existing outputs; not a true recompute.",
        }
    else:
        if not args.legacy_script:
            raise UserFacingError("--legacy-script is required for --mode compute_legacy_exec")
        project_root = Path(args.project_root).resolve() if args.project_root else Path.cwd()
        compute_meta = run_compute_legacy_exec(
            legacy_script=Path(args.legacy_script).resolve(),
            reference=reference,
            metadata=metadata,
            query_h5ad=query_h5ad,
            whole_lung_summary=whole_lung_summary,
            whole_lung_projection=whole_lung_projection,
            outdir=outdir,
            query_id=query_id,
            project_root=project_root,
        )
        meta = {
            "adapter": "epithelial_only_remap_common_v2.py",
            "mode": args.mode,
            "query_id": query_id,
            "query_h5ad": str(query_h5ad),
            "reference": str(reference),
            "metadata": str(metadata),
            "stage_axis": args.stage_axis,
            "whole_lung_summary": str(whole_lung_summary),
            "whole_lung_projection": str(whole_lung_projection),
            **compute_meta,
        }

    with open(outdir / f"{query_id}_epithelial_adapter_meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(
        f"[done] {query_id}: epithelial stage completed\n"
        f"       mode={args.mode}\n"
        f"       outdir={outdir}"
    )


if __name__ == "__main__":
    main()
