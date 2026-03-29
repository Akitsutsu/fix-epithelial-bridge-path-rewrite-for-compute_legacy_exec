#!/usr/bin/env python3
"""
Week-1 whole-lung common adapter.

This adapter does not yet reimplement the legacy whole-lung mapping logic.
Instead, it standardizes the CLI and can replay existing per-query outputs into
 the common runner's fixed outdir layout.

Supported mode
--------------
copy_existing / symlink_existing
    Resolve source artifact paths from either explicit CLI arguments or a
    legacy-output manifest CSV keyed by query_id, then copy or symlink them into
    the standardized output filenames expected by benchmark_common_runner_v1.py.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import shutil
from pathlib import Path
from typing import Dict, Optional


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
        raise UserFacingError(f"Unsupported mode: {mode}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Week-1 whole-lung common adapter")
    parser.add_argument("--reference", required=True)
    parser.add_argument("--metadata", required=True)
    parser.add_argument("--query-id", required=True)
    parser.add_argument("--query-h5ad", required=True)
    parser.add_argument("--stage-axis", default="sample_week")
    parser.add_argument("--outdir", required=True)
    parser.add_argument(
        "--mode",
        choices=["copy_existing", "symlink_existing"],
        default="copy_existing",
        help="How to materialize standardized outputs from existing legacy files",
    )
    parser.add_argument(
        "--legacy-output-manifest",
        default=None,
        help="CSV keyed by query_id with whole_lung_summary and whole_lung_projection columns",
    )
    parser.add_argument("--source-summary", default=None)
    parser.add_argument("--source-projection", default=None)
    args = parser.parse_args()

    query_id = str(args.query_id).strip()
    outdir = Path(args.outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    query_h5ad = Path(args.query_h5ad).resolve()
    if not query_h5ad.exists():
        raise UserFacingError(f"query h5ad not found: {query_h5ad}")
    if str(args.stage_axis) != "sample_week":
        raise UserFacingError(
            f"stage_axis must remain sample_week for the frozen benchmark, got: {args.stage_axis!r}"
        )

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
        "adapter": "whole_lung_project_common_v1.py",
        "mode": args.mode,
        "query_id": query_id,
        "query_h5ad": str(query_h5ad),
        "reference": str(Path(args.reference).resolve()),
        "metadata": str(Path(args.metadata).resolve()),
        "stage_axis": args.stage_axis,
        "source_manifest": source_manifest,
        "source_summary": str(source_summary),
        "source_projection": str(source_projection),
        "target_summary": str(target_summary),
        "target_projection": str(target_projection),
        "note": "Week-1 compatibility replay from existing outputs; not a true recompute.",
    }
    with open(outdir / f"{query_id}_whole_lung_adapter_meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(
        f"[done] {query_id}: materialized whole-lung outputs to {outdir}\n"
        f"       summary={target_summary.name}\n"
        f"       projection={target_projection.name}\n"
        f"       mode={args.mode}"
    )


if __name__ == "__main__":
    main()
