#!/usr/bin/env python3
"""
Extract reference_metadata_v1.csv from a reference h5ad file.

This script decodes integer-coded Seurat categoricals using the codebook CSVs
and produces the canonical metadata CSV used by all downstream benchmark scripts.

Outputs are written to a specified directory (default: rebuild_audit_v1/).
The operational frozen pair under converted/ is NOT overwritten.

Usage:
    python extract_reference_metadata_v1.py [--h5ad PATH] [--codebook-dir PATH] [--outdir PATH]
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import anndata as ad
import numpy as np
import pandas as pd


def load_codebook(path: Path) -> dict[int, str]:
    """Load a codebook CSV mapping h5ad integer codes to labels."""
    df = pd.read_csv(path)
    if "h5ad_code" in df.columns and "label" in df.columns:
        return dict(zip(df["h5ad_code"].astype(int), df["label"].astype(str)))
    if "value" in df.columns:
        # value-only codebook (e.g. sample_week): values are already strings
        return {i: str(v) for i, v in enumerate(df["value"])}
    raise ValueError(f"Unrecognized codebook format in {path}: columns={list(df.columns)}")


def derive_stage_num(stage_fine: pd.Series) -> pd.Series:
    return pd.to_numeric(
        stage_fine.astype(str).str.replace("week_", "", regex=False),
        errors="coerce",
    ).astype("Int64")


def derive_stage_coarse(stage_num: pd.Series) -> pd.Series:
    vals = stage_num.astype(float)
    return pd.Series(
        np.where(vals <= 13, "early_GW10_13",
                 np.where(vals <= 16, "mid_GW14_16", "late_GW17_19")),
        index=stage_num.index,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--h5ad", default="converted/reference_RNA.h5ad",
                        help="Path to reference h5ad (default: converted/reference_RNA.h5ad)")
    parser.add_argument("--codebook-dir", default="codebook",
                        help="Path to codebook directory (default: codebook/)")
    parser.add_argument("--outdir", default="rebuild_audit_v1",
                        help="Output directory (default: rebuild_audit_v1/)")
    args = parser.parse_args()

    h5ad_path = Path(args.h5ad)
    codebook_dir = Path(args.codebook_dir)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    if not h5ad_path.exists():
        print(f"ERROR: h5ad not found: {h5ad_path}", file=sys.stderr)
        raise SystemExit(1)

    # --- Load h5ad obs ---
    print(f"Loading {h5ad_path} ...")
    ref = ad.read_h5ad(str(h5ad_path), backed="r")
    obs = ref.obs.copy()
    obs.index = [str(x) for x in ref.obs_names]
    obs.index.name = "cell_id"
    print(f"  shape: {ref.shape}")
    print(f"  obs columns: {list(obs.columns)}")

    # --- Load codebooks (fail clearly if missing) ---
    required_codebooks = [
        "codebook_cell_type.csv",
        "codebook_all_cell_type.csv",
        "codebook_group.csv",
    ]
    missing = [name for name in required_codebooks if not (codebook_dir / name).exists()]
    if missing:
        print(f"ERROR: required codebook CSVs not found in {codebook_dir}/:", file=sys.stderr)
        for name in missing:
            print(f"  - {name}", file=sys.stderr)
        raise SystemExit(1)

    cb_cell_type = load_codebook(codebook_dir / "codebook_cell_type.csv")
    cb_all_cell_type = load_codebook(codebook_dir / "codebook_all_cell_type.csv")
    cb_group = load_codebook(codebook_dir / "codebook_group.csv")

    # --- Decode and build metadata ---
    meta = pd.DataFrame(index=obs.index)
    meta.index.name = "cell_id"

    meta["sample_id"] = obs["orig.ident"].astype(str)
    meta["sample_name"] = obs["sample_name"].astype(str)

    # sample_week is already a string in the frozen h5ad
    meta["stage_fine"] = obs["sample_week"].astype(str)
    meta["stage_num"] = derive_stage_num(meta["stage_fine"])
    meta["stage_coarse"] = derive_stage_coarse(meta["stage_num"])

    # Decode integer-coded categoricals
    meta["state_coarse"] = obs["cell_type"].astype(int).map(cb_cell_type)
    meta["state_fine"] = obs["all_cell_type"].astype(int).map(cb_all_cell_type)
    meta["group_internal"] = obs["group"].astype(int).map(cb_group)

    # --- Validate ---
    for col in ["state_coarse", "state_fine", "group_internal"]:
        n_missing = int(meta[col].isna().sum())
        if n_missing > 0:
            print(f"WARNING: {n_missing} unmapped values in {col}", file=sys.stderr)

    # --- Write output ---
    out_path = outdir / "reference_metadata_v1.csv"
    meta.to_csv(out_path, index=True, quoting=csv.QUOTE_ALL)
    print(f"Written: {out_path}  ({len(meta)} rows, {len(meta.columns)} columns)")

    # --- Write summary ---
    summary = {
        "h5ad_path": str(h5ad_path),
        "n_cells": int(ref.shape[0]),
        "n_genes": int(ref.shape[1]),
        "metadata_columns": list(meta.columns),
        "stage_fine_values": sorted(meta["stage_fine"].unique().tolist()),
        "state_coarse_values": sorted(meta["state_coarse"].dropna().unique().tolist()),
        "n_state_fine_values": int(meta["state_fine"].nunique()),
        "group_internal_values": sorted(meta["group_internal"].dropna().unique().tolist()),
    }
    summary_path = outdir / "extract_metadata_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Written: {summary_path}")

    ref.file.close()


if __name__ == "__main__":
    main()
