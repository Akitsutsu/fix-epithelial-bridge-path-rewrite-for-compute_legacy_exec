#!/usr/bin/env python3
"""
Week-1 epithelial common adapter.

This adapter standardizes the CLI expected by benchmark_common_runner_v1.py and
can replay existing epithelial outputs into the fixed per-query layout.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import shutil
from pathlib import Path
from typing import Dict, Optional


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
        raise UserFacingError(f"Unsupported mode: {mode}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Week-1 epithelial common adapter")
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
        choices=["copy_existing", "symlink_existing"],
        default="copy_existing",
        help="How to materialize standardized outputs from existing legacy files",
    )
    parser.add_argument(
        "--legacy-output-manifest",
        default=None,
        help="CSV keyed by query_id with epithelial source artifact columns",
    )
    parser.add_argument("--source-summary", default=None)
    parser.add_argument("--source-state-fine", default=None)
    parser.add_argument("--source-stage-fine", default=None)
    parser.add_argument("--source-lineage-off-target", default=None)
    parser.add_argument("--source-stable-marker", default=None)
    parser.add_argument("--source-boundary-pairs", default=None)
    parser.add_argument("--source-boundary-direction-marker", default=None)
    args = parser.parse_args()

    query_id = str(args.query_id).strip()
    outdir = Path(args.outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    query_h5ad = Path(args.query_h5ad).resolve()
    if not query_h5ad.exists():
        raise UserFacingError(f"query h5ad not found: {query_h5ad}")
    whole_lung_summary = Path(args.whole_lung_summary).resolve()
    whole_lung_projection = Path(args.whole_lung_projection).resolve()
    if not whole_lung_summary.exists() or not whole_lung_projection.exists():
        raise UserFacingError(
            "Whole-lung standardized outputs are required before epithelial stage; "
            f"got summary_exists={whole_lung_summary.exists()} projection_exists={whole_lung_projection.exists()}"
        )
    if str(args.stage_axis) != "sample_week":
        raise UserFacingError(
            f"stage_axis must remain sample_week for the frozen benchmark, got: {args.stage_axis!r}"
        )

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
        "adapter": "epithelial_only_remap_common_v1.py",
        "mode": args.mode,
        "query_id": query_id,
        "query_h5ad": str(query_h5ad),
        "reference": str(Path(args.reference).resolve()),
        "metadata": str(Path(args.metadata).resolve()),
        "stage_axis": args.stage_axis,
        "whole_lung_summary": str(whole_lung_summary),
        "whole_lung_projection": str(whole_lung_projection),
        "source_manifest": source_manifest,
        "source_files": {k: (str(v) if v is not None else None) for k, v in source_map.items()},
        "target_files": {k: str(v) for k, v in targets.items()},
        "optional_materialized": optional_materialized,
        "note": "Week-1 compatibility replay from existing outputs; not a true recompute.",
    }
    with open(outdir / f"{query_id}_epithelial_adapter_meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(
        f"[done] {query_id}: materialized epithelial outputs to {outdir}\n"
        f"       required=4 files\n"
        f"       optional_materialized={sum(v is not None for v in optional_materialized.values())}\n"
        f"       mode={args.mode}"
    )


if __name__ == "__main__":
    main()
