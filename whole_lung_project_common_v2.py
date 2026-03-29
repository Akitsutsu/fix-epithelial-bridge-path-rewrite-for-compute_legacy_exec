#!/usr/bin/env python3
"""
Whole-lung common adapter v2.

Modes
-----
copy_existing / symlink_existing
    Replay existing legacy artifacts into the common runner layout.
compute_legacy_exec
    Execute a legacy whole-lung script after patching hard-coded paths/output
    prefixes in-memory so it behaves like a query-agnostic CLI stage.

This is a compatibility bridge for Week 1/2. It does not rewrite the biology;
it reuses the existing legacy compute logic with a standardized I/O contract.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Dict, Optional, Tuple


MANIFEST_REQUIRED_COLUMNS = ["query_id", "whole_lung_summary", "whole_lung_projection"]


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


def _rewrite_whole_lung_legacy_source(
    source: str,
    *,
    reference: Path,
    metadata: Path,
    query_h5ad: Path,
    outdir: Path,
    query_id: str,
) -> Tuple[str, Dict[str, object]]:
    debug: Dict[str, object] = {}
    out = source

    # Replace the outdir assignment if present.
    out, n_outdir = re.subn(
        r'(?m)^outdir\s*=\s*Path\((?:"[^"]*"|\'[^\']*\')\)\s*$',
        f"outdir = Path({outdir.as_posix()!r})",
        out,
    )
    debug["outdir_assignment_replacements"] = n_outdir

    # Replace known literal paths anywhere they appear.
    out, path_counts = _replace_path_literals(
        out,
        {
            "converted/reference_RNA.h5ad": reference.as_posix(),
            "converted/reference_metadata_v1.csv": metadata.as_posix(),
            "converted/query_CA1_clean.h5ad": query_h5ad.as_posix(),
            "converted/query_BU3_clean.h5ad": query_h5ad.as_posix(),
            "prototype_out_v1": outdir.as_posix(),
        },
    )
    debug["literal_path_replacements"] = path_counts

    out, prefix_counts = _replace_prefix_tokens(out, query_id)
    debug["prefix_token_counts"] = prefix_counts

    # Basic sanity signals.
    debug["contains_read_h5ad"] = ("read_h5ad" in out)
    debug["contains_summary_output"] = ("_summary_v1.json" in out)
    debug["contains_projection_output"] = ("_cell_projection_v1.csv" in out)
    return out, debug


def run_compute_legacy_exec(
    *,
    legacy_script: Path,
    reference: Path,
    metadata: Path,
    query_h5ad: Path,
    outdir: Path,
    query_id: str,
) -> Dict[str, object]:
    if not legacy_script.exists():
        raise UserFacingError(f"legacy script not found: {legacy_script}")

    source = legacy_script.read_text(encoding="utf-8")
    rewritten, debug = _rewrite_whole_lung_legacy_source(
        source,
        reference=reference,
        metadata=metadata,
        query_h5ad=query_h5ad,
        outdir=outdir,
        query_id=query_id,
    )

    summary_path = outdir / f"{query_id}_summary_v1.json"
    projection_path = outdir / f"{query_id}_cell_projection_v1.csv"

    ns = {
        "__name__": "__main__",
        "__file__": str(legacy_script),
        "Path": Path,
    }
    old_argv = sys.argv[:]
    sys.argv = [str(legacy_script)]
    try:
        exec(compile(rewritten, str(legacy_script), "exec"), ns, ns)
    finally:
        sys.argv = old_argv

    missing = [str(p) for p in [summary_path, projection_path] if not p.exists()]
    if missing:
        raise UserFacingError(
            "legacy whole-lung compute finished but expected outputs are missing: "
            + ", ".join(missing)
        )

    return {
        "legacy_script": str(legacy_script),
        "summary": str(summary_path),
        "projection": str(projection_path),
        "rewrite_debug": debug,
        "note": "Whole-lung outputs computed by in-memory execution of rewritten legacy source.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Whole-lung common adapter v2")
    parser.add_argument("--reference", required=True)
    parser.add_argument("--metadata", required=True)
    parser.add_argument("--query-id", required=True)
    parser.add_argument("--query-h5ad", required=True)
    parser.add_argument("--stage-axis", default="sample_week")
    parser.add_argument("--outdir", required=True)
    parser.add_argument(
        "--mode",
        choices=["copy_existing", "symlink_existing", "compute_legacy_exec"],
        default="copy_existing",
    )
    parser.add_argument("--legacy-output-manifest", default=None)
    parser.add_argument("--source-summary", default=None)
    parser.add_argument("--source-projection", default=None)
    parser.add_argument("--legacy-script", default=None)
    args = parser.parse_args()

    query_id = str(args.query_id).strip()
    if not query_id:
        raise UserFacingError("query_id must not be empty")
    outdir = Path(args.outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    reference = Path(args.reference).resolve()
    metadata = Path(args.metadata).resolve()
    query_h5ad = Path(args.query_h5ad).resolve()
    for p, label in [(reference, "reference"), (metadata, "metadata"), (query_h5ad, "query_h5ad")]:
        if not p.exists():
            raise UserFacingError(f"{label} not found: {p}")

    if str(args.stage_axis) != "sample_week":
        raise UserFacingError(
            f"stage_axis must remain sample_week for the frozen benchmark, got: {args.stage_axis!r}"
        )

    meta: Dict[str, object]
    if args.mode in {"copy_existing", "symlink_existing"}:
        source_summary = Path(args.source_summary).resolve() if args.source_summary else None
        source_projection = Path(args.source_projection).resolve() if args.source_projection else None
        source_manifest = None

        if args.legacy_output_manifest:
            manifest_path = Path(args.legacy_output_manifest).resolve()
            row = load_manifest_row(manifest_path, query_id)
            source_manifest = str(manifest_path)
            manifest_base = manifest_path.parent
            if source_summary is None:
                source_summary = resolve_path(row.get("whole_lung_summary"), manifest_base)
            if source_projection is None:
                source_projection = resolve_path(row.get("whole_lung_projection"), manifest_base)

        if source_summary is None or source_projection is None:
            raise UserFacingError(
                "Need both whole-lung sources. Provide --source-summary/--source-projection or --legacy-output-manifest."
            )

        missing = [str(p) for p in [source_summary, source_projection] if p is None or not p.exists()]
        if missing:
            raise UserFacingError(f"Missing whole-lung source files: {', '.join(missing)}")

        target_summary = outdir / f"{query_id}_summary_v1.json"
        target_projection = outdir / f"{query_id}_cell_projection_v1.csv"
        materialize(source_summary, target_summary, args.mode)
        materialize(source_projection, target_projection, args.mode)

        meta = {
            "adapter": "whole_lung_project_common_v2.py",
            "mode": args.mode,
            "query_id": query_id,
            "query_h5ad": str(query_h5ad),
            "reference": str(reference),
            "metadata": str(metadata),
            "stage_axis": args.stage_axis,
            "source_manifest": source_manifest,
            "source_summary": str(source_summary),
            "source_projection": str(source_projection),
            "target_summary": str(target_summary),
            "target_projection": str(target_projection),
            "note": "Compatibility replay from existing outputs; not a true recompute.",
        }
    else:
        if not args.legacy_script:
            raise UserFacingError("--legacy-script is required for --mode compute_legacy_exec")
        compute_meta = run_compute_legacy_exec(
            legacy_script=Path(args.legacy_script).resolve(),
            reference=reference,
            metadata=metadata,
            query_h5ad=query_h5ad,
            outdir=outdir,
            query_id=query_id,
        )
        meta = {
            "adapter": "whole_lung_project_common_v2.py",
            "mode": args.mode,
            "query_id": query_id,
            "query_h5ad": str(query_h5ad),
            "reference": str(reference),
            "metadata": str(metadata),
            "stage_axis": args.stage_axis,
            **compute_meta,
        }

    with open(outdir / f"{query_id}_whole_lung_adapter_meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(
        f"[done] {query_id}: whole-lung stage completed\n"
        f"       mode={args.mode}\n"
        f"       outdir={outdir}"
    )


if __name__ == "__main__":
    main()
