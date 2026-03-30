#!/usr/bin/env python3
"""
Reference drift report v1.

Compares a candidate reference against the current release, producing
human-readable and machine-readable drift summaries.

Two modes:
  structural  — compare matrix shape, obs/var overlap, metadata distributions
  benchmark   — run the benchmark runner twice (release vs candidate) and diff
                anchor-query key metrics
  both        — run structural first, then benchmark

All output goes to --outdir. No existing release or candidate files are modified.

Usage (structural):
    python run_reference_drift_report_v1.py \\
      --candidate-dir references/candidates/2026-04-early-only \\
      --outdir references/drift/2026-04-early-only \\
      --tag 2026-04-early-only \\
      --mode structural

Usage (both):
    python run_reference_drift_report_v1.py \\
      --candidate-dir references/candidates/2026-04-early-only \\
      --outdir references/drift/2026-04-early-only \\
      --tag 2026-04-early-only \\
      --mode both \\
      --manifest query_manifest_v1.csv \\
      --whole-lung-cmd-template-file whole_lung_cmd_template_v1.txt \\
      --epi-cmd-template-file epithelial_cmd_template_v1.txt
"""

from __future__ import annotations

import argparse
import csv
import json
import shlex
import subprocess
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import anndata as ad
import numpy as np
import pandas as pd


# ── Registry resolution ──────────────────────────────────────────────────────

def resolve_release(
    release_version: str,
    registry_dir: Path,
) -> Dict[str, str]:
    """Resolve release paths from registry files."""
    current_yaml = registry_dir / "current_release.yaml"
    registry_csv = registry_dir / "REFERENCE_REGISTRY.csv"

    if release_version == "current":
        if not current_yaml.exists():
            raise SystemExit(f"ERROR: {current_yaml} not found")
        # Parse minimal flat YAML without pyyaml
        release_info: Dict[str, str] = {}
        for line in current_yaml.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                key, val = line.split(":", 1)
                release_info[key.strip()] = val.strip()
        return release_info

    # Look up specific version in CSV registry
    if not registry_csv.exists():
        raise SystemExit(f"ERROR: {registry_csv} not found")
    df = pd.read_csv(registry_csv)
    match = df[df["release_version"] == release_version]
    if match.empty:
        raise SystemExit(
            f"ERROR: release_version '{release_version}' not found in {registry_csv}"
        )
    row = match.iloc[0].to_dict()
    return {
        "release_version": str(row["release_version"]),
        "release_name": str(row["release_name"]),
        "expression_path": str(row["expression_path"]),
        "metadata_path": str(row["metadata_path"]),
    }


# ── Structural drift ─────────────────────────────────────────────────────────

REQUIRED_METADATA_COLUMNS = [
    "cell_id", "sample_id", "sample_name",
    "stage_fine", "stage_num", "stage_coarse",
    "state_coarse", "state_fine", "group_internal",
]

DISTRIBUTION_COLUMNS = [
    "stage_fine", "stage_coarse", "state_fine", "state_coarse", "group_internal",
]


def load_h5ad_summary(path: Path) -> Dict[str, Any]:
    """Load an h5ad and extract structural summary without loading X into memory."""
    adata = ad.read_h5ad(str(path), backed="r")
    obs = adata.obs
    summary: Dict[str, Any] = {
        "path": str(path),
        "n_cells": int(adata.shape[0]),
        "n_genes": int(adata.shape[1]),
        "obs_columns": sorted(obs.columns.tolist()),
        "obs_names_sample": [str(x) for x in adata.obs_names[:5]],
        "var_names_sample": [str(x) for x in adata.var_names[:5]],
        "obs_names_set": set(str(x) for x in adata.obs_names),
        "var_names_set": set(str(x) for x in adata.var_names),
        "var_names_list": [str(x) for x in adata.var_names],
        "has_raw": adata.raw is not None,
    }

    # Check X non-negativity and dtype on a sample
    try:
        sample_size = min(1000, adata.shape[0])
        x_sample = adata.X[:sample_size]
        if hasattr(x_sample, "toarray"):
            x_sample = x_sample.toarray()
        x_sample = np.asarray(x_sample, dtype=float)
        summary["x_dtype"] = str(adata.X.dtype) if hasattr(adata.X, "dtype") else "unknown"
        summary["x_sample_min"] = float(np.nanmin(x_sample))
        summary["x_sample_max"] = float(np.nanmax(x_sample))
        summary["x_non_negative"] = bool(np.nanmin(x_sample) >= 0)
        summary["x_has_nan"] = bool(np.isnan(x_sample).any())
    except Exception as e:
        summary["x_error"] = str(e)

    # Check .raw var_names if present
    if adata.raw is not None:
        try:
            summary["raw_n_genes"] = int(adata.raw.shape[1])
            summary["raw_var_names_sample"] = [str(x) for x in adata.raw.var_names[:5]]
            raw_var_set = set(str(x) for x in adata.raw.var_names)
            summary["raw_var_names_set"] = raw_var_set
        except Exception as e:
            summary["raw_error"] = str(e)

    adata.file.close()
    return summary


def load_metadata_summary(path: Path) -> Dict[str, Any]:
    """Load a metadata CSV and extract structural summary."""
    df = pd.read_csv(path)
    cols = df.columns.tolist()
    summary: Dict[str, Any] = {
        "path": str(path),
        "n_rows": len(df),
        "n_columns": len(cols),
        "columns": cols,
    }
    # Distribution summaries for key columns
    for col in DISTRIBUTION_COLUMNS:
        if col in df.columns:
            vc = df[col].value_counts()
            total = int(vc.sum())
            summary[f"dist_{col}"] = {
                str(k): {"n": int(v), "frac": round(v / total, 6)}
                for k, v in vc.items()
            }
    return summary


def compute_structural_drift(
    release_h5ad: Dict[str, Any],
    candidate_h5ad: Dict[str, Any],
    release_meta: Dict[str, Any],
    candidate_meta: Dict[str, Any],
) -> Dict[str, Any]:
    """Compare release vs candidate structural properties."""
    drift: Dict[str, Any] = {}

    # Shape
    drift["shape"] = {
        "release_cells": release_h5ad["n_cells"],
        "release_genes": release_h5ad["n_genes"],
        "candidate_cells": candidate_h5ad["n_cells"],
        "candidate_genes": candidate_h5ad["n_genes"],
        "cells_diff": candidate_h5ad["n_cells"] - release_h5ad["n_cells"],
        "genes_diff": candidate_h5ad["n_genes"] - release_h5ad["n_genes"],
        "shape_identical": (
            release_h5ad["n_cells"] == candidate_h5ad["n_cells"]
            and release_h5ad["n_genes"] == candidate_h5ad["n_genes"]
        ),
    }

    # obs_names overlap
    r_obs = release_h5ad["obs_names_set"]
    c_obs = candidate_h5ad["obs_names_set"]
    drift["obs_names"] = {
        "identical": r_obs == c_obs,
        "release_only": len(r_obs - c_obs),
        "candidate_only": len(c_obs - r_obs),
        "shared": len(r_obs & c_obs),
        "jaccard": round(len(r_obs & c_obs) / len(r_obs | c_obs), 6) if (r_obs | c_obs) else 1.0,
    }

    # var_names overlap
    r_var = release_h5ad["var_names_set"]
    c_var = candidate_h5ad["var_names_set"]
    drift["var_names"] = {
        "identical": r_var == c_var,
        "release_only": len(r_var - c_var),
        "candidate_only": len(c_var - r_var),
        "shared": len(r_var & c_var),
        "jaccard": round(len(r_var & c_var) / len(r_var | c_var), 6) if (r_var | c_var) else 1.0,
    }
    # Check if var_names are in the same order
    if r_var == c_var:
        drift["var_names"]["same_order"] = (
            release_h5ad["var_names_list"] == candidate_h5ad["var_names_list"]
        )

    # Required metadata columns
    r_cols = set(release_meta["columns"])
    c_cols = set(candidate_meta["columns"])
    missing_required = [c for c in REQUIRED_METADATA_COLUMNS if c not in c_cols]
    drift["metadata_columns"] = {
        "release_columns": sorted(r_cols),
        "candidate_columns": sorted(c_cols),
        "missing_required_in_candidate": missing_required,
        "all_required_present": len(missing_required) == 0,
    }

    # Distribution comparisons
    dist_diffs: Dict[str, Any] = {}
    for col in DISTRIBUTION_COLUMNS:
        r_dist = release_meta.get(f"dist_{col}", {})
        c_dist = candidate_meta.get(f"dist_{col}", {})
        all_keys = sorted(set(r_dist.keys()) | set(c_dist.keys()))
        col_diff = {
            "release_n_categories": len(r_dist),
            "candidate_n_categories": len(c_dist),
            "categories_identical": set(r_dist.keys()) == set(c_dist.keys()),
            "release_only_categories": sorted(set(r_dist.keys()) - set(c_dist.keys())),
            "candidate_only_categories": sorted(set(c_dist.keys()) - set(r_dist.keys())),
        }
        # Distribution shift (L1 distance of fraction vectors)
        l1 = 0.0
        for k in all_keys:
            r_frac = r_dist.get(k, {}).get("frac", 0.0) if r_dist.get(k) else 0.0
            c_frac = c_dist.get(k, {}).get("frac", 0.0) if c_dist.get(k) else 0.0
            l1 += abs(r_frac - c_frac)
        col_diff["l1_distance"] = round(l1, 6)
        dist_diffs[col] = col_diff
    drift["distributions"] = dist_diffs

    # X layer summary
    drift["x_layer"] = {
        "release_non_negative": release_h5ad.get("x_non_negative"),
        "candidate_non_negative": candidate_h5ad.get("x_non_negative"),
        "release_dtype": release_h5ad.get("x_dtype"),
        "candidate_dtype": candidate_h5ad.get("x_dtype"),
    }

    # .raw presence
    drift["raw"] = {
        "release_has_raw": release_h5ad["has_raw"],
        "candidate_has_raw": candidate_h5ad["has_raw"],
        "both_have_raw": release_h5ad["has_raw"] and candidate_h5ad["has_raw"],
    }
    if release_h5ad["has_raw"] and candidate_h5ad["has_raw"]:
        r_raw_var = release_h5ad.get("raw_var_names_set", set())
        c_raw_var = candidate_h5ad.get("raw_var_names_set", set())
        drift["raw"]["raw_var_identical"] = r_raw_var == c_raw_var
        drift["raw"]["release_raw_n_genes"] = release_h5ad.get("raw_n_genes")
        drift["raw"]["candidate_raw_n_genes"] = candidate_h5ad.get("raw_n_genes")

    # Drop-in compatibility assessment
    drift["drop_in_compatible"] = (
        len(missing_required) == 0
        and drift["var_names"]["identical"]
        and candidate_h5ad.get("x_non_negative", False)
    )

    return drift


def write_structural_csv(
    drift: Dict[str, Any],
    outdir: Path,
    tag: str,
) -> Path:
    """Write a flat CSV summarizing key structural differences."""
    rows: List[Dict[str, Any]] = []

    shape = drift["shape"]
    rows.append({"metric": "n_cells", "release": shape["release_cells"],
                 "candidate": shape["candidate_cells"], "diff": shape["cells_diff"]})
    rows.append({"metric": "n_genes", "release": shape["release_genes"],
                 "candidate": shape["candidate_genes"], "diff": shape["genes_diff"]})

    obs = drift["obs_names"]
    rows.append({"metric": "obs_names_shared", "release": shape["release_cells"],
                 "candidate": shape["candidate_cells"], "diff": obs["shared"]})
    rows.append({"metric": "obs_names_jaccard", "release": "", "candidate": "",
                 "diff": obs["jaccard"]})

    var = drift["var_names"]
    rows.append({"metric": "var_names_identical", "release": shape["release_genes"],
                 "candidate": shape["candidate_genes"], "diff": var["identical"]})

    for col, dd in drift["distributions"].items():
        rows.append({"metric": f"{col}_l1_distance", "release": dd["release_n_categories"],
                     "candidate": dd["candidate_n_categories"], "diff": dd["l1_distance"]})

    out_path = outdir / f"release_vs_candidate_structural_diff_{tag}.csv"
    pd.DataFrame(rows).to_csv(out_path, index=False)
    return out_path


def write_structural_report(
    drift: Dict[str, Any],
    release_info: Dict[str, str],
    candidate_dir: str,
    tag: str,
    outdir: Path,
) -> Path:
    """Write a human-readable markdown drift report."""
    lines: List[str] = []
    lines.append(f"# Reference Drift Report: {tag}")
    lines.append("")
    lines.append(f"**Date:** {date.today()}")
    lines.append(f"**Release:** {release_info.get('release_version', 'unknown')} "
                 f"({release_info.get('release_name', 'unknown')})")
    lines.append(f"**Candidate:** {candidate_dir}")
    lines.append(f"**Mode:** structural")
    lines.append("")

    # Shape
    s = drift["shape"]
    lines.append("## Matrix shape")
    lines.append("")
    lines.append("| | Release | Candidate | Diff |")
    lines.append("|---|---|---|---|")
    lines.append(f"| Cells | {s['release_cells']:,} | {s['candidate_cells']:,} | {s['cells_diff']:+,} |")
    lines.append(f"| Genes | {s['release_genes']:,} | {s['candidate_genes']:,} | {s['genes_diff']:+,} |")
    lines.append("")

    # obs_names
    o = drift["obs_names"]
    lines.append("## obs_names overlap")
    lines.append("")
    lines.append(f"- Identical: **{o['identical']}**")
    lines.append(f"- Shared: {o['shared']:,}")
    lines.append(f"- Release-only: {o['release_only']:,}")
    lines.append(f"- Candidate-only: {o['candidate_only']:,}")
    lines.append(f"- Jaccard: {o['jaccard']:.4f}")
    lines.append("")

    # var_names
    v = drift["var_names"]
    lines.append("## var_names overlap")
    lines.append("")
    lines.append(f"- Identical: **{v['identical']}**")
    lines.append(f"- Shared: {v['shared']:,}")
    lines.append(f"- Release-only: {v['release_only']:,}")
    lines.append(f"- Candidate-only: {v['candidate_only']:,}")
    lines.append(f"- Jaccard: {v['jaccard']:.4f}")
    if "same_order" in v:
        lines.append(f"- Same order: {v['same_order']}")
    lines.append("")

    # Metadata columns
    m = drift["metadata_columns"]
    lines.append("## Metadata columns")
    lines.append("")
    lines.append(f"- All required present in candidate: **{m['all_required_present']}**")
    if m["missing_required_in_candidate"]:
        lines.append(f"- Missing: {', '.join(m['missing_required_in_candidate'])}")
    lines.append("")

    # Distributions
    lines.append("## Distribution drift (L1 distance)")
    lines.append("")
    lines.append("| Column | Release categories | Candidate categories | L1 distance |")
    lines.append("|---|---|---|---|")
    for col, dd in drift["distributions"].items():
        lines.append(f"| {col} | {dd['release_n_categories']} | {dd['candidate_n_categories']} | {dd['l1_distance']:.4f} |")
    lines.append("")

    for col, dd in drift["distributions"].items():
        if dd["release_only_categories"] or dd["candidate_only_categories"]:
            lines.append(f"### {col} category changes")
            if dd["release_only_categories"]:
                lines.append(f"- Release-only: {', '.join(dd['release_only_categories'])}")
            if dd["candidate_only_categories"]:
                lines.append(f"- Candidate-only: {', '.join(dd['candidate_only_categories'])}")
            lines.append("")

    # X layer
    x = drift["x_layer"]
    lines.append("## X layer")
    lines.append("")
    lines.append(f"- Release non-negative: {x['release_non_negative']}")
    lines.append(f"- Candidate non-negative: {x['candidate_non_negative']}")
    lines.append(f"- Release dtype: {x['release_dtype']}")
    lines.append(f"- Candidate dtype: {x['candidate_dtype']}")
    lines.append("")

    # .raw
    r = drift["raw"]
    lines.append("## .raw layer")
    lines.append("")
    lines.append(f"- Release has .raw: {r['release_has_raw']}")
    lines.append(f"- Candidate has .raw: {r['candidate_has_raw']}")
    if r.get("raw_var_identical") is not None:
        lines.append(f"- .raw var_names identical: {r['raw_var_identical']}")
    lines.append("")

    # Drop-in assessment
    lines.append("## Drop-in compatibility")
    lines.append("")
    compat = drift["drop_in_compatible"]
    lines.append(f"**Drop-in replacement for downstream use: {'YES' if compat else 'NO'}**")
    lines.append("")
    if not compat:
        reasons = []
        if drift["metadata_columns"]["missing_required_in_candidate"]:
            reasons.append("missing required metadata columns")
        if not drift["var_names"]["identical"]:
            reasons.append("var_names differ (gene space mismatch)")
        if not drift.get("x_layer", {}).get("candidate_non_negative", True):
            reasons.append("candidate X contains negative values")
        if reasons:
            lines.append(f"Reasons: {'; '.join(reasons)}")
            lines.append("")

    out_path = outdir / f"REFERENCE_DRIFT_REPORT_{tag}.md"
    out_path.write_text("\n".join(lines) + "\n")
    return out_path


# ── Benchmark drift ──────────────────────────────────────────────────────────

NOISE_COLUMNS = {
    "whole_lung_summary_json",
    "epi_summary_json",
    "epi_stage_fine_csv",
    "epi_state_fine_csv",
}

BENCHMARK_COMPARE_COLUMNS = [
    "query_id",
    "n_query_cells",
    "n_query_epi_eligible",
    "lineage_off_target_fraction",
    "top_stage",
    "top_stage_fraction",
    "top_state",
    "top_state_fraction",
]


def run_benchmark(
    reference_h5ad: Path,
    metadata_csv: Path,
    manifest: Path,
    outdir: Path,
    whole_lung_template_file: Path,
    epi_template_file: Path,
    query_ids: List[str],
    fail_fast: bool,
    label: str,
) -> Tuple[int, Path]:
    """Run the benchmark runner and return (returncode, outdir)."""
    run_dir = outdir / f"benchmark_{label}"
    cmd_parts = [
        sys.executable,
        "benchmark_common_runner_v2.py",
        "--manifest", str(manifest),
        "--outdir", str(run_dir),
        "--reference", str(reference_h5ad),
        "--metadata", str(metadata_csv),
        "--whole-lung-cmd-template-file", str(whole_lung_template_file),
        "--epi-cmd-template-file", str(epi_template_file),
    ]
    if query_ids:
        cmd_parts += ["--query-id"] + query_ids
    if fail_fast:
        cmd_parts.append("--fail-fast")

    cmd_str = " ".join(shlex.quote(p) for p in cmd_parts)
    print(f"  [{label}] Running benchmark: {cmd_str}")

    proc = subprocess.run(
        cmd_parts,
        text=True,
        capture_output=True,
    )

    # Save logs
    log_dir = outdir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    (log_dir / f"benchmark_{label}.stdout.log").write_text(proc.stdout)
    (log_dir / f"benchmark_{label}.stderr.log").write_text(proc.stderr)

    if proc.returncode != 0:
        print(f"  [{label}] Benchmark FAILED (rc={proc.returncode})", file=sys.stderr)
        print(f"  stderr: {proc.stderr[:500]}", file=sys.stderr)
    else:
        print(f"  [{label}] Benchmark completed OK")

    return proc.returncode, run_dir


def compare_key_metrics(
    release_dir: Path,
    candidate_dir: Path,
    outdir: Path,
    tag: str,
) -> Tuple[Optional[pd.DataFrame], Dict[str, Any]]:
    """Compare all_queries_key_metrics.csv from release vs candidate runs."""
    r_path = release_dir / "compare" / "all_queries_key_metrics.csv"
    c_path = candidate_dir / "compare" / "all_queries_key_metrics.csv"

    summary: Dict[str, Any] = {
        "release_metrics_path": str(r_path),
        "candidate_metrics_path": str(c_path),
        "release_metrics_exists": r_path.exists(),
        "candidate_metrics_exists": c_path.exists(),
    }

    if not r_path.exists() or not c_path.exists():
        summary["status"] = "incomplete"
        return None, summary

    r_df = pd.read_csv(r_path)
    c_df = pd.read_csv(c_path)

    # Align on query_id
    r_df = r_df.set_index("query_id")
    c_df = c_df.set_index("query_id")

    common_ids = sorted(set(r_df.index) & set(c_df.index))
    if not common_ids:
        summary["status"] = "no_common_query_ids"
        return None, summary

    diff_rows: List[Dict[str, Any]] = []
    for qid in common_ids:
        row: Dict[str, Any] = {"query_id": qid}
        for col in BENCHMARK_COMPARE_COLUMNS:
            if col == "query_id":
                continue
            if col in NOISE_COLUMNS:
                continue
            r_val = r_df.at[qid, col] if col in r_df.columns else None
            c_val = c_df.at[qid, col] if col in c_df.columns else None
            row[f"release_{col}"] = r_val
            row[f"candidate_{col}"] = c_val

            # Compute diff for numeric columns
            try:
                r_num = float(r_val) if r_val is not None and not pd.isna(r_val) else None
                c_num = float(c_val) if c_val is not None and not pd.isna(c_val) else None
                if r_num is not None and c_num is not None:
                    row[f"diff_{col}"] = round(c_num - r_num, 8)
                else:
                    row[f"diff_{col}"] = None
            except (ValueError, TypeError):
                # String columns (top_stage, top_state)
                row[f"match_{col}"] = str(r_val) == str(c_val)

        # Check epithelial artifacts
        for label_prefix, run_dir in [("release", release_dir), ("candidate", candidate_dir)]:
            epi_dir = run_dir / "epithelial" / qid
            epi_artifacts = [
                f"{qid}_epi_summary_v1.json",
                f"{qid}_epi_state_fine.csv",
                f"{qid}_epi_stage_fine.csv",
                f"{qid}_lineage_off_target_state_coarse.csv",
            ]
            present = sum(1 for a in epi_artifacts if (epi_dir / a).exists())
            row[f"{label_prefix}_epi_artifacts_present"] = f"{present}/{len(epi_artifacts)}"

        diff_rows.append(row)

    diff_df = pd.DataFrame(diff_rows)
    out_path = outdir / f"anchor_key_metrics_diff_{tag}.csv"
    diff_df.to_csv(out_path, index=False)

    summary["status"] = "ok"
    summary["n_queries_compared"] = len(common_ids)
    summary["query_ids"] = common_ids

    # Per-query verdict
    query_verdicts: Dict[str, Dict[str, Any]] = {}
    for qid in common_ids:
        qrow = diff_df[diff_df["query_id"] == qid].iloc[0]
        verdict: Dict[str, Any] = {}
        for col in ["top_stage", "top_state"]:
            verdict[f"{col}_match"] = qrow.get(f"match_{col}", None)
        for col in ["lineage_off_target_fraction", "n_query_cells", "n_query_epi_eligible"]:
            verdict[f"{col}_diff"] = qrow.get(f"diff_{col}", None)
        query_verdicts[qid] = verdict
    summary["per_query"] = query_verdicts

    return diff_df, summary


def append_benchmark_to_report(
    report_path: Path,
    benchmark_summary: Dict[str, Any],
    tag: str,
) -> None:
    """Append benchmark drift section to an existing markdown report."""
    lines: List[str] = []
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Benchmark drift (anchor-query comparison)")
    lines.append("")
    lines.append(f"**Status:** {benchmark_summary.get('status', 'unknown')}")
    lines.append("")

    if benchmark_summary.get("status") != "ok":
        lines.append("Benchmark comparison could not be completed.")
        lines.append("")
        report_path.write_text(report_path.read_text() + "\n".join(lines) + "\n")
        return

    lines.append(f"**Queries compared:** {benchmark_summary.get('n_queries_compared', 0)}")
    lines.append(f"**Query IDs:** {', '.join(benchmark_summary.get('query_ids', []))}")
    lines.append("")

    per_query = benchmark_summary.get("per_query", {})
    if per_query:
        lines.append("### Per-query results")
        lines.append("")
        lines.append("| Query | top_stage match | top_state match | off_target_frac diff | n_cells diff | n_epi_eligible diff |")
        lines.append("|---|---|---|---|---|---|")
        for qid, v in per_query.items():
            lines.append(
                f"| {qid} "
                f"| {v.get('top_stage_match', 'N/A')} "
                f"| {v.get('top_state_match', 'N/A')} "
                f"| {v.get('lineage_off_target_fraction_diff', 'N/A')} "
                f"| {v.get('n_query_cells_diff', 'N/A')} "
                f"| {v.get('n_query_epi_eligible_diff', 'N/A')} |"
            )
        lines.append("")

    lines.append(f"Detailed diff: `anchor_key_metrics_diff_{tag}.csv`")
    lines.append("")

    report_path.write_text(report_path.read_text() + "\n".join(lines) + "\n")


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--candidate-dir", required=True,
                        help="Path to candidate build directory")
    parser.add_argument("--outdir", required=True,
                        help="Output directory for drift report")
    parser.add_argument("--tag", required=True,
                        help="Drift report tag")
    parser.add_argument("--release-version", default="current",
                        help="Release version to compare against (default: current)")
    parser.add_argument("--mode", choices=["structural", "benchmark", "both"],
                        default="structural",
                        help="Drift comparison mode (default: structural)")
    parser.add_argument("--manifest",
                        help="Query manifest CSV (required for benchmark/both)")
    parser.add_argument("--whole-lung-cmd-template-file",
                        help="Whole-lung command template file (required for benchmark/both)")
    parser.add_argument("--epi-cmd-template-file",
                        help="Epithelial command template file (required for benchmark/both)")
    parser.add_argument("--query-id", default="BU3,CA1",
                        help="Comma-separated query IDs (default: BU3,CA1)")
    parser.add_argument("--fail-fast", action="store_true",
                        help="Pass --fail-fast to benchmark runner")
    parser.add_argument("--registry-dir", default="references/registry",
                        help="Path to registry directory (default: references/registry)")
    args = parser.parse_args()

    candidate_dir = Path(args.candidate_dir).resolve()
    outdir = Path(args.outdir).resolve()
    registry_dir = Path(args.registry_dir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    query_ids = [q.strip() for q in args.query_id.split(",") if q.strip()]

    # Validate benchmark mode requirements
    if args.mode in ("benchmark", "both"):
        missing_args = []
        if not args.manifest:
            missing_args.append("--manifest")
        if not args.whole_lung_cmd_template_file:
            missing_args.append("--whole-lung-cmd-template-file")
        if not args.epi_cmd_template_file:
            missing_args.append("--epi-cmd-template-file")
        if missing_args:
            parser.error(
                f"Benchmark mode requires: {', '.join(missing_args)}"
            )

    # Resolve release
    print("Resolving release reference ...")
    release_info = resolve_release(args.release_version, registry_dir)
    release_h5ad_path = Path(release_info["expression_path"]).resolve()
    release_meta_path = Path(release_info["metadata_path"]).resolve()
    print(f"  Release: {release_info.get('release_version')} ({release_info.get('release_name', '')})")
    print(f"  h5ad:     {release_h5ad_path}")
    print(f"  metadata: {release_meta_path}")

    # Resolve candidate
    candidate_h5ad_path = candidate_dir / "reference_RNA.h5ad"
    candidate_meta_path = candidate_dir / "reference_metadata.csv"
    print(f"  Candidate dir: {candidate_dir}")

    # Validate files exist
    for label, path in [
        ("release h5ad", release_h5ad_path),
        ("release metadata", release_meta_path),
        ("candidate h5ad", candidate_h5ad_path),
        ("candidate metadata", candidate_meta_path),
    ]:
        if not path.exists():
            raise SystemExit(f"ERROR: {label} not found: {path}")

    # Master summary for JSON output
    master_summary: Dict[str, Any] = {
        "tag": args.tag,
        "mode": args.mode,
        "report_date": str(date.today()),
        "release_version": release_info.get("release_version"),
        "release_name": release_info.get("release_name"),
        "release_h5ad": str(release_h5ad_path),
        "release_metadata": str(release_meta_path),
        "candidate_dir": str(candidate_dir),
        "candidate_h5ad": str(candidate_h5ad_path),
        "candidate_metadata": str(candidate_meta_path),
        "query_ids": query_ids,
    }

    # ── Structural mode ───────────────────────────────────────────────────────

    if args.mode in ("structural", "both"):
        print("\n=== Structural drift analysis ===")

        print("  Loading release h5ad ...")
        release_h5ad = load_h5ad_summary(release_h5ad_path)
        print("  Loading candidate h5ad ...")
        candidate_h5ad = load_h5ad_summary(candidate_h5ad_path)
        print("  Loading release metadata ...")
        release_meta = load_metadata_summary(release_meta_path)
        print("  Loading candidate metadata ...")
        candidate_meta = load_metadata_summary(candidate_meta_path)

        print("  Computing structural drift ...")
        drift = compute_structural_drift(
            release_h5ad, candidate_h5ad, release_meta, candidate_meta
        )
        master_summary["structural"] = drift

        # Write outputs
        csv_path = write_structural_csv(drift, outdir, args.tag)
        print(f"  Written: {csv_path}")

        report_path = write_structural_report(
            drift, release_info, str(candidate_dir), args.tag, outdir
        )
        print(f"  Written: {report_path}")
    else:
        report_path = outdir / f"REFERENCE_DRIFT_REPORT_{args.tag}.md"
        if not report_path.exists():
            report_path.write_text(
                f"# Reference Drift Report: {args.tag}\n\n"
                f"**Date:** {date.today()}\n"
                f"**Mode:** benchmark-only\n\n"
            )

    # ── Benchmark mode ────────────────────────────────────────────────────────

    if args.mode in ("benchmark", "both"):
        print("\n=== Benchmark drift analysis ===")

        manifest_path = Path(args.manifest).resolve()
        wl_template = Path(args.whole_lung_cmd_template_file).resolve()
        epi_template = Path(args.epi_cmd_template_file).resolve()

        for label, path in [
            ("manifest", manifest_path),
            ("whole-lung template", wl_template),
            ("epi template", epi_template),
        ]:
            if not path.exists():
                raise SystemExit(f"ERROR: {label} not found: {path}")

        # Run release benchmark
        print("\n  --- Release benchmark ---")
        r_rc, r_dir = run_benchmark(
            reference_h5ad=release_h5ad_path,
            metadata_csv=release_meta_path,
            manifest=manifest_path,
            outdir=outdir,
            whole_lung_template_file=wl_template,
            epi_template_file=epi_template,
            query_ids=query_ids,
            fail_fast=args.fail_fast,
            label="release",
        )

        # Run candidate benchmark
        print("\n  --- Candidate benchmark ---")
        c_rc, c_dir = run_benchmark(
            reference_h5ad=candidate_h5ad_path,
            metadata_csv=candidate_meta_path,
            manifest=manifest_path,
            outdir=outdir,
            whole_lung_template_file=wl_template,
            epi_template_file=epi_template,
            query_ids=query_ids,
            fail_fast=args.fail_fast,
            label="candidate",
        )

        master_summary["benchmark"] = {
            "release_returncode": r_rc,
            "candidate_returncode": c_rc,
            "release_dir": str(r_dir),
            "candidate_dir": str(c_dir),
        }

        # Compare key metrics
        if r_rc == 0 and c_rc == 0:
            print("\n  --- Comparing key metrics ---")
            diff_df, bench_summary = compare_key_metrics(r_dir, c_dir, outdir, args.tag)
            master_summary["benchmark"].update(bench_summary)

            # Append to markdown report
            append_benchmark_to_report(report_path, bench_summary, args.tag)
            print(f"  Updated: {report_path}")
        else:
            master_summary["benchmark"]["comparison_status"] = "skipped_due_to_failure"
            print("  Skipping key metrics comparison due to benchmark failure.")

    # ── Write master summary JSON ─────────────────────────────────────────────

    # Remove non-serializable sets from structural drift before writing JSON
    def sanitize_for_json(obj: Any) -> Any:
        if isinstance(obj, set):
            return sorted(obj)
        if isinstance(obj, dict):
            return {k: sanitize_for_json(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [sanitize_for_json(v) for v in obj]
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, np.bool_):
            return bool(obj)
        return obj

    summary_path = outdir / f"reference_drift_summary_{args.tag}.json"
    with open(summary_path, "w") as f:
        json.dump(sanitize_for_json(master_summary), f, indent=2, default=str)
    print(f"\nWritten: {summary_path}")
    print("Done.")


if __name__ == "__main__":
    main()
