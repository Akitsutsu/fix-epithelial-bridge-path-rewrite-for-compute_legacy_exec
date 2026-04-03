#!/usr/bin/env python3
"""
Week-1 common runner for frozen-reference lung benchmark queries.

What this script does
---------------------
1) Loads a manifest CSV of query_id / h5ad_path rows.
2) Runs provenance preflight via provenance_audit_h5ad.py.
3) Creates a fixed run directory structure.
4) Invokes whole-lung and epithelial stages through configurable shell-command
   templates so the runner itself is query-ID agnostic.
5) Verifies required output files and writes compare/status tables.

This is intentionally a thin orchestration layer. It does *not* reimplement the
existing mapping logic inside epithelial_only_remap_v1.py or the BU3 working
copy. Instead, it defines the Week-1 I/O contract and gives a single entry
point that both old scripts can be adapted to.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

import pandas as pd


MANIFEST_REQUIRED_COLUMNS = ["query_id", "h5ad_path"]
MANIFEST_OPTIONAL_DEFAULTS: Dict[str, Any] = {
    "note": "",
    "enabled": True,
    "group_label": "",
    "expected_sample_id": "",
    "expected_donor_id": "",
    "expected_source_type": "",
    "expected_batch_id": "",
}

DEFAULT_PROVENANCE_FIELDS = ["sample_id", "donor_id", "source_type", "batch_id"]

WHOLE_LUNG_REQUIRED_FILES = [
    "{query_id}_summary_v1.json",
    "{query_id}_cell_projection_v1.csv",
]

EPI_REQUIRED_FILES = [
    "{query_id}_epi_summary_v1.json",
    "{query_id}_epi_state_fine.csv",
    "{query_id}_epi_stage_fine.csv",
    "{query_id}_lineage_off_target_state_coarse.csv",
]

EPI_OPTIONAL_FILES = [
    "{query_id}_stable_state_marker_summary.csv",
    "{query_id}_epi_state_boundary_pairs_unordered.csv",
    "{query_id}_boundary_pair_direction_marker_summary.csv",
]


@dataclass
class StageResult:
    stage: str
    status: str
    command: str
    returncode: Optional[int]
    stdout_log: str
    stderr_log: str
    message: str


class UserFacingError(RuntimeError):
    pass


class SafeDict(dict):
    def __missing__(self, key: str) -> str:
        return "{" + key + "}"


def parse_bool(x: Any) -> bool:
    if isinstance(x, bool):
        return x
    if x is None:
        return False
    s = str(x).strip().lower()
    if s in {"1", "true", "t", "yes", "y", "on"}:
        return True
    if s in {"0", "false", "f", "no", "n", "off", ""}:
        return False
    raise UserFacingError(f"Could not parse boolean value: {x!r}")


def normalize_query_id(qid: str) -> str:
    qid = str(qid).strip()
    if not qid:
        raise UserFacingError("query_id must not be empty")
    if not re.fullmatch(r"[A-Za-z0-9._-]+", qid):
        raise UserFacingError(
            f"Invalid query_id {qid!r}. Allowed characters: A-Z a-z 0-9 . _ -"
        )
    return qid


def resolve_path(value: str, base_dir: Path) -> Path:
    p = Path(str(value).strip())
    if not p.is_absolute():
        p = (base_dir / p).resolve()
    else:
        p = p.resolve()
    return p


def read_manifest(manifest_path: Path) -> pd.DataFrame:
    try:
        df = pd.read_csv(manifest_path)
    except Exception as e:
        raise UserFacingError(f"Failed to read manifest {manifest_path}: {e}") from e

    missing_cols = [c for c in MANIFEST_REQUIRED_COLUMNS if c not in df.columns]
    if missing_cols:
        raise UserFacingError(
            f"Manifest is missing required columns: {', '.join(missing_cols)}"
        )

    for col, default in MANIFEST_OPTIONAL_DEFAULTS.items():
        if col not in df.columns:
            df[col] = default
        else:
            if isinstance(default, bool):
                df[col] = df[col].map(parse_bool)
            else:
                df[col] = df[col].fillna(default).astype(str)

    df["query_id"] = df["query_id"].map(normalize_query_id)
    if df["query_id"].duplicated().any():
        dups = df.loc[df["query_id"].duplicated(keep=False), "query_id"].tolist()
        raise UserFacingError(f"Manifest has duplicated query_id values: {dups}")

    manifest_dir = manifest_path.parent.resolve()
    resolved_paths: List[str] = []
    exists_flags: List[bool] = []
    for raw in df["h5ad_path"].tolist():
        resolved = resolve_path(str(raw), manifest_dir)
        resolved_paths.append(str(resolved))
        exists_flags.append(resolved.exists())
    df["h5ad_path"] = resolved_paths
    df["h5ad_exists"] = exists_flags

    missing_files = df.loc[~df["h5ad_exists"], ["query_id", "h5ad_path"]]
    if len(missing_files):
        details = "; ".join(
            f"{row.query_id}={row.h5ad_path}" for row in missing_files.itertuples(index=False)
        )
        raise UserFacingError(f"Some manifest h5ad_path values do not exist: {details}")

    # Keep only canonical columns first, then extras if present.
    ordered = MANIFEST_REQUIRED_COLUMNS + list(MANIFEST_OPTIONAL_DEFAULTS.keys()) + [
        c for c in df.columns if c not in (MANIFEST_REQUIRED_COLUMNS + list(MANIFEST_OPTIONAL_DEFAULTS.keys()))
    ]
    df = df.loc[:, ordered]
    return df


def ensure_dirs(root: Path) -> Dict[str, Path]:
    dirs = {
        "root": root,
        "config": root / "run_config",
        "preflight": root / "preflight",
        "provenance": root / "preflight" / "provenance",
        "whole_lung": root / "whole_lung",
        "epithelial": root / "epithelial",
        "compare": root / "compare",
        "logs": root / "logs",
    }
    for p in dirs.values():
        p.mkdir(parents=True, exist_ok=True)
    return dirs


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def quote_context(raw_context: Mapping[str, Any]) -> Dict[str, str]:
    return {k: shlex.quote(str(v)) for k, v in raw_context.items()}


def format_expected_files(root: Path, query_id: str, patterns: Sequence[str]) -> List[Path]:
    return [root / pattern.format(query_id=query_id) for pattern in patterns]


def read_text_template(value: Optional[str], maybe_file: Optional[str]) -> Optional[str]:
    if value:
        return value
    if maybe_file:
        return Path(maybe_file).read_text(encoding="utf-8").strip()
    return None


def run_subprocess_shell(
    command_template: str,
    raw_context: Mapping[str, Any],
    stage: str,
    query_id: str,
    log_dir: Path,
    dry_run: bool,
) -> StageResult:
    quoted = quote_context(raw_context)
    command = command_template.format_map(SafeDict(quoted))

    stdout_log = log_dir / f"{stage}.stdout.log"
    stderr_log = log_dir / f"{stage}.stderr.log"

    if dry_run:
        stdout_log.write_text("[dry-run]\n" + command + "\n", encoding="utf-8")
        stderr_log.write_text("", encoding="utf-8")
        return StageResult(
            stage=stage,
            status="dry_run",
            command=command,
            returncode=None,
            stdout_log=str(stdout_log),
            stderr_log=str(stderr_log),
            message="Command not executed because --dry-run was set.",
        )

    proc = subprocess.run(
        command,
        shell=True,
        executable="/bin/bash",
        text=True,
        capture_output=True,
    )
    stdout_log.write_text(proc.stdout, encoding="utf-8")
    stderr_log.write_text(proc.stderr, encoding="utf-8")
    status = "ok" if proc.returncode == 0 else "failed"
    message = "completed" if proc.returncode == 0 else f"returncode={proc.returncode}"
    return StageResult(
        stage=stage,
        status=status,
        command=command,
        returncode=proc.returncode,
        stdout_log=str(stdout_log),
        stderr_log=str(stderr_log),
        message=message,
    )


def verify_files(paths: Sequence[Path], optional: bool = False) -> Tuple[str, str]:
    missing = [str(p) for p in paths if not p.exists()]
    if not missing:
        return ("ok", "all expected files present")
    if optional:
        return ("warning", f"optional files missing: {', '.join(missing)}")
    return ("failed", f"missing required files: {', '.join(missing)}")


def run_provenance_preflight(
    manifest_df: pd.DataFrame,
    provenance_script: Path,
    provenance_outdir: Path,
    fields: Sequence[str],
    dry_run: bool,
    root_logs: Path,
) -> StageResult:
    input_args: List[str] = []
    for row in manifest_df.itertuples(index=False):
        if not bool(row.enabled):
            continue
        input_args.append(f"{row.query_id}={row.h5ad_path}")

    if not provenance_script.exists():
        raise UserFacingError(f"Provenance script not found: {provenance_script}")

    command_parts = [
        shlex.quote(sys.executable),
        shlex.quote(str(provenance_script)),
        "--input",
    ] + [shlex.quote(x) for x in input_args] + [
        "--outdir",
        shlex.quote(str(provenance_outdir)),
        "--fields",
    ] + [shlex.quote(x) for x in fields]

    command = " ".join(command_parts)
    log_dir = root_logs / "preflight"
    log_dir.mkdir(parents=True, exist_ok=True)
    stdout_log = log_dir / "provenance.stdout.log"
    stderr_log = log_dir / "provenance.stderr.log"

    if dry_run:
        stdout_log.write_text("[dry-run]\n" + command + "\n", encoding="utf-8")
        stderr_log.write_text("", encoding="utf-8")
        return StageResult(
            stage="preflight_provenance",
            status="dry_run",
            command=command,
            returncode=None,
            stdout_log=str(stdout_log),
            stderr_log=str(stderr_log),
            message="Command not executed because --dry-run was set.",
        )

    proc = subprocess.run(command, shell=True, executable="/bin/bash", text=True, capture_output=True)
    stdout_log.write_text(proc.stdout, encoding="utf-8")
    stderr_log.write_text(proc.stderr, encoding="utf-8")
    status = "ok" if proc.returncode == 0 else "failed"
    message = "completed" if proc.returncode == 0 else f"returncode={proc.returncode}"
    return StageResult(
        stage="preflight_provenance",
        status=status,
        command=command,
        returncode=proc.returncode,
        stdout_log=str(stdout_log),
        stderr_log=str(stderr_log),
        message=message,
    )


def load_top_provenance_combo(provenance_dir: Path, query_id: str) -> Dict[str, Any]:
    path = provenance_dir / query_id / f"{query_id}_provenance_exact_combinations.csv"
    if not path.exists():
        return {}
    try:
        df = pd.read_csv(path)
    except Exception:
        return {}
    if df.empty:
        return {}
    row = df.iloc[0].to_dict()
    return row


def build_provenance_expectation_check(manifest_df: pd.DataFrame, provenance_dir: Path) -> pd.DataFrame:
    rows: List[Dict[str, Any]] = []
    expected_map = {
        "expected_sample_id": "sample_id",
        "expected_donor_id": "donor_id",
        "expected_source_type": "source_type",
        "expected_batch_id": "batch_id",
    }
    for row in manifest_df.itertuples(index=False):
        top = load_top_provenance_combo(provenance_dir, row.query_id)
        out: Dict[str, Any] = {
            "query_id": row.query_id,
            "enabled": bool(row.enabled),
            "top_combo_fraction": top.get("fraction"),
            "top_combo_n_cells": top.get("n_cells"),
            "provenance_n_exact_combinations": None,
            "provenance_status": "not_run" if not top else "ok",
        }
        n_exact_path = provenance_dir / row.query_id / f"{row.query_id}_provenance_summary.json"
        if n_exact_path.exists():
            try:
                summary = json.loads(n_exact_path.read_text(encoding="utf-8"))
                out["provenance_n_exact_combinations"] = summary.get("n_exact_combinations")
            except Exception:
                pass
        field_results: List[str] = []
        for expected_col, observed_col in expected_map.items():
            expected_val = getattr(row, expected_col, "")
            observed_val = top.get(observed_col, "") if top else ""
            out[expected_col] = expected_val
            out[observed_col] = observed_val
            if str(expected_val).strip() == "":
                out[f"{observed_col}_match"] = "not_checked"
            else:
                matched = str(expected_val) == str(observed_val)
                out[f"{observed_col}_match"] = matched
                field_results.append("pass" if matched else "fail")

        if out["provenance_status"] == "not_run":
            pass
        elif not field_results:
            out["provenance_status"] = "observed_only"
        elif all(x == "pass" for x in field_results):
            out["provenance_status"] = "pass"
        else:
            out["provenance_status"] = "fail"
        rows.append(out)
    return pd.DataFrame(rows)


def load_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _first_present(mapping: Mapping[str, Any], candidates: Sequence[str]) -> Any:
    for c in candidates:
        if c in mapping:
            return mapping[c]
    return None


def _norm_key(x: Any) -> str:
    return re.sub(r"[^a-z0-9]+", "", str(x).strip().lower())


def _is_missing(x: Any) -> bool:
    if x is None:
        return True
    try:
        return bool(pd.isna(x))
    except Exception:
        return False


def _pick_present(*values: Any) -> Any:
    for v in values:
        if _is_missing(v):
            continue
        if isinstance(v, str) and v.strip() == "":
            continue
        return v
    return None


def _infer_label_col(df: pd.DataFrame) -> Optional[str]:
    norm_map = {c: _norm_key(c) for c in df.columns}

    exact_priority = {
        "state",
        "stage",
        "label",
        "name",
        "cellstate",
        "sampleweek",
        "statefine",
        "stagefine",
        "predictedstate",
        "predictedstage",
        "statecoarse",
        "stagecoarse",
        "statelabel",
        "stagelabel",
    }
    for col, nk in norm_map.items():
        if nk in exact_priority:
            return col

    contains_priority = [
        "sampleweek",
        "stage",
        "state",
        "label",
        "name",
        "week",
    ]
    for needle in contains_priority:
        for col, nk in norm_map.items():
            if needle in nk:
                return col

    obj_like = []
    for col in df.columns:
        ser = df[col]
        if pd.api.types.is_object_dtype(ser) or pd.api.types.is_string_dtype(ser) or pd.api.types.is_categorical_dtype(ser):
            obj_like.append(col)
    if len(obj_like) == 1:
        return obj_like[0]
    if obj_like:
        return obj_like[0]

    return None


def _infer_fraction_col(df: pd.DataFrame, exclude: Sequence[str] = ()) -> Optional[str]:
    norm_map = {c: _norm_key(c) for c in df.columns}
    exact_priority = {
        "fraction",
        "fractionwithinquery",
        "fractionwithincrossstate",
        "fractionwithinambiguous",
        "proportion",
        "frac",
        "share",
        "pct",
        "percentage",
    }
    for col, nk in norm_map.items():
        if col in exclude:
            continue
        if nk in exact_priority:
            return col

    contains_priority = ["fraction", "proportion", "share", "frac", "pct", "percentage"]
    for needle in contains_priority:
        for col, nk in norm_map.items():
            if col in exclude:
                continue
            if needle in nk:
                return col

    candidate_cols = []
    for col in df.columns:
        if col in exclude:
            continue
        ser = pd.to_numeric(df[col], errors="coerce")
        if ser.notna().sum() == 0:
            continue
        valid = ser.dropna()
        if valid.empty:
            continue
        if (valid >= 0).all() and (valid <= 1).all():
            candidate_cols.append((col, float(valid.max())))
    if candidate_cols:
        candidate_cols.sort(key=lambda x: x[1], reverse=True)
        return candidate_cols[0][0]

    return None


def _infer_count_col(df: pd.DataFrame, exclude: Sequence[str] = ()) -> Optional[str]:
    norm_map = {c: _norm_key(c) for c in df.columns}
    exact_priority = {"n", "ncells", "count", "cells", "ncell", "numcells"}
    for col, nk in norm_map.items():
        if col in exclude:
            continue
        if nk in exact_priority:
            return col

    contains_priority = ["count", "cells", "ncell", "n"]
    for needle in contains_priority:
        for col, nk in norm_map.items():
            if col in exclude:
                continue
            if needle in nk:
                return col

    numeric_cols = []
    for col in df.columns:
        if col in exclude:
            continue
        ser = pd.to_numeric(df[col], errors="coerce")
        if ser.notna().sum() == 0:
            continue
        valid = ser.dropna()
        if valid.empty:
            continue
        # prefer non-fraction numeric columns
        if (valid >= 0).all() and (valid.round() == valid).all():
            numeric_cols.append((col, float(valid.sum())))
    if numeric_cols:
        numeric_cols.sort(key=lambda x: x[1], reverse=True)
        return numeric_cols[0][0]

    return None


def _find_top_distribution_entry(summary: Any, kind: str) -> Tuple[Optional[str], Optional[float]]:
    if not isinstance(summary, dict):
        return None, None

    # direct scalar keys first
    label = _pick_present(
        summary.get(f"top_{kind}"),
        summary.get(f"{kind}_top"),
        summary.get(f"{kind}_label"),
        summary.get(f"top_{kind}_label"),
    )
    frac = _pick_present(
        summary.get(f"top_{kind}_fraction"),
        summary.get(f"{kind}_top_fraction"),
        summary.get(f"{kind}_fraction"),
    )

    if isinstance(label, dict):
        label = _pick_present(
            label.get(kind),
            label.get("label"),
            label.get("name"),
            label.get("state"),
            label.get("stage"),
        )
    if isinstance(frac, dict):
        frac = _pick_present(frac.get("fraction"), frac.get("frac"), frac.get("proportion"))

    if label is not None:
        try:
            frac_f = None if frac is None else float(frac)
        except Exception:
            frac_f = None
        return str(label), frac_f

    # common distribution containers
    candidate_containers = [
        summary.get(f"{kind}_distribution"),
        summary.get(f"{kind}s"),
        summary.get(f"{kind}_fine"),
        summary.get(f"{kind}_fine_distribution"),
        summary.get(f"top_{kind}s"),
        summary.get(f"{kind}_top_k"),
    ]
    for container in candidate_containers:
        if not isinstance(container, list) or len(container) == 0:
            continue
        try:
            df = pd.DataFrame(container)
        except Exception:
            continue
        lbl, frc = infer_top_label_and_fraction_from_dataframe(df)
        if lbl is not None:
            return lbl, frc

    # recursive search through nested dicts/lists
    for v in summary.values():
        if isinstance(v, dict):
            lbl, frc = _find_top_distribution_entry(v, kind)
            if lbl is not None:
                return lbl, frc
        elif isinstance(v, list):
            for item in v:
                if isinstance(item, dict):
                    lbl, frc = _find_top_distribution_entry(item, kind)
                    if lbl is not None:
                        return lbl, frc

    return None, None


def infer_top_label_and_fraction_from_dataframe(df: pd.DataFrame) -> Tuple[Optional[str], Optional[float]]:
    if df.empty:
        return None, None

    label_col = _infer_label_col(df)
    if label_col is None:
        return None, None

    frac_col = _infer_fraction_col(df, exclude=[label_col])
    count_col = _infer_count_col(df, exclude=[label_col, frac_col] if frac_col else [label_col])

    if frac_col is not None:
        tmp = df.assign(__frac__=pd.to_numeric(df[frac_col], errors="coerce")).sort_values("__frac__", ascending=False).iloc[0]
        frac_val = pd.to_numeric(tmp["__frac__"], errors="coerce")
        frac = None if pd.isna(frac_val) else float(frac_val)
        return str(tmp[label_col]), frac

    if count_col is not None:
        ser = pd.to_numeric(df[count_col], errors="coerce")
        if ser.notna().sum() > 0:
            tmp = df.assign(__count__=ser).sort_values("__count__", ascending=False).iloc[0]
            total = float(ser.dropna().sum()) if float(ser.dropna().sum()) != 0 else None
            count_val = pd.to_numeric(tmp["__count__"], errors="coerce")
            frac = (float(count_val) / total) if (total and not pd.isna(count_val)) else None
            return str(tmp[label_col]), frac

    return str(df.iloc[0][label_col]), None


def infer_top_label_and_fraction_from_csv(path: Path) -> Tuple[Optional[str], Optional[float]]:
    if not path.exists():
        return None, None
    try:
        df = pd.read_csv(path)
    except Exception:
        return None, None
    return infer_top_label_and_fraction_from_dataframe(df)


def infer_top_label_and_fraction_from_summary(summary: Mapping[str, Any], kind: str) -> Tuple[Optional[str], Optional[float]]:
    try:
        return _find_top_distribution_entry(summary, kind)
    except Exception:
        return None, None


def build_key_metrics_row(
    manifest_row: Mapping[str, Any],
    provenance_dir: Path,
    whole_lung_dir: Path,
    epi_dir: Path,
) -> Dict[str, Any]:
    query_id = str(manifest_row["query_id"])
    note = str(manifest_row.get("note", ""))

    whole_summary_path = whole_lung_dir / query_id / f"{query_id}_summary_v1.json"
    epi_summary_path = epi_dir / query_id / f"{query_id}_epi_summary_v1.json"
    stage_csv_path = epi_dir / query_id / f"{query_id}_epi_stage_fine.csv"
    state_csv_path = epi_dir / query_id / f"{query_id}_epi_state_fine.csv"

    whole = load_json(whole_summary_path)
    epi = load_json(epi_summary_path)
    provenance_top = load_top_provenance_combo(provenance_dir, query_id)

    top_stage_label_csv, top_stage_fraction_csv = infer_top_label_and_fraction_from_csv(stage_csv_path)
    top_state_label_csv, top_state_fraction_csv = infer_top_label_and_fraction_from_csv(state_csv_path)
    top_stage_label_json, top_stage_fraction_json = infer_top_label_and_fraction_from_summary(whole, "stage")
    if top_stage_label_json is None:
        top_stage_label_json, top_stage_fraction_json = infer_top_label_and_fraction_from_summary(epi, "stage")
    top_state_label_json, top_state_fraction_json = infer_top_label_and_fraction_from_summary(epi, "state")
    if top_state_label_json is None:
        top_state_label_json, top_state_fraction_json = infer_top_label_and_fraction_from_summary(whole, "state")

    row = {
        "query_id": query_id,
        "note": note,
        "sample_id": provenance_top.get("sample_id"),
        "donor_id": provenance_top.get("donor_id"),
        "source_type": provenance_top.get("source_type"),
        "batch_id": provenance_top.get("batch_id"),
        "n_query_cells": _pick_present(
            whole.get("n_query_cells"), epi.get("n_query_cells"), whole.get("n_cells_total")
        ),
        "n_query_epi_eligible": _pick_present(
            whole.get("n_query_epi_eligible"), epi.get("n_query_epi_eligible")
        ),
        "lineage_off_target_fraction": _pick_present(
            whole.get("off_target_fraction"),
            whole.get("lineage_off_target_fraction"),
            epi.get("lineage_off_target_fraction"),
        ),
        "top_stage": _pick_present(
            whole.get("top_stage"),
            epi.get("top_stage"),
            top_stage_label_json,
            top_stage_label_csv,
        ),
        "top_stage_fraction": _pick_present(
            whole.get("top_stage_fraction"),
            epi.get("top_stage_fraction"),
            top_stage_fraction_json,
            top_stage_fraction_csv,
        ),
        "top_state": _pick_present(
            epi.get("top_state"),
            whole.get("top_state"),
            top_state_label_json,
            top_state_label_csv,
        ),
        "top_state_fraction": _pick_present(
            epi.get("top_state_fraction"),
            whole.get("top_state_fraction"),
            top_state_fraction_json,
            top_state_fraction_csv,
        ),
        "whole_lung_summary_json": str(whole_summary_path) if whole_summary_path.exists() else "",
        "epi_summary_json": str(epi_summary_path) if epi_summary_path.exists() else "",
        "epi_stage_fine_csv": str(stage_csv_path) if stage_csv_path.exists() else "",
        "epi_state_fine_csv": str(state_csv_path) if state_csv_path.exists() else "",
    }
    return row


def concat_per_query_csvs(
    query_ids: Iterable[str],
    root: Path,
    suffix: str,
    add_query_id_if_missing: bool = True,
) -> pd.DataFrame:
    frames: List[pd.DataFrame] = []
    for qid in query_ids:
        path = root / qid / f"{qid}_{suffix}"
        if not path.exists():
            continue
        try:
            df = pd.read_csv(path)
        except Exception:
            continue
        if add_query_id_if_missing and "query_id" not in df.columns:
            df.insert(0, "query_id", qid)
        frames.append(df)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def build_context(row: Mapping[str, Any], dirs: Mapping[str, Path], args: argparse.Namespace) -> Dict[str, Any]:
    query_id = str(row["query_id"])
    query_log_dir = dirs["logs"] / query_id
    query_log_dir.mkdir(parents=True, exist_ok=True)
    whole_out = dirs["whole_lung"] / query_id
    whole_out.mkdir(parents=True, exist_ok=True)
    epi_out = dirs["epithelial"] / query_id
    epi_out.mkdir(parents=True, exist_ok=True)
    provenance_qdir = dirs["provenance"] / query_id
    return {
        "query_id": query_id,
        "h5ad_path": row["h5ad_path"],
        "note": row.get("note", ""),
        "reference": args.reference,
        "metadata": args.metadata,
        "stage_axis": args.stage_axis,
        "run_outdir": dirs["root"],
        "config_outdir": dirs["config"],
        "preflight_outdir": dirs["preflight"],
        "provenance_root": dirs["provenance"],
        "provenance_outdir": provenance_qdir,
        "provenance_summary_json": provenance_qdir / f"{query_id}_provenance_summary.json",
        "provenance_summary_md": provenance_qdir / f"{query_id}_provenance_summary.md",
        "whole_lung_root": dirs["whole_lung"],
        "whole_lung_outdir": whole_out,
        "whole_lung_summary_json": whole_out / f"{query_id}_summary_v1.json",
        "whole_lung_cell_projection_csv": whole_out / f"{query_id}_cell_projection_v1.csv",
        "epi_root": dirs["epithelial"],
        "epi_outdir": epi_out,
        "epi_summary_json": epi_out / f"{query_id}_epi_summary_v1.json",
        "epi_state_fine_csv": epi_out / f"{query_id}_epi_state_fine.csv",
        "epi_stage_fine_csv": epi_out / f"{query_id}_epi_stage_fine.csv",
        "epi_lineage_off_target_state_coarse_csv": epi_out / f"{query_id}_lineage_off_target_state_coarse.csv",
        "query_log_dir": query_log_dir,
        "query_log_outdir": query_log_dir,
    }


def write_run_status_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    pd.DataFrame(list(rows)).to_csv(path, index=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Common benchmark runner for frozen-reference lung queries.")
    parser.add_argument("--manifest", required=True, help="Path to query_manifest_v1.csv")
    parser.add_argument("--outdir", required=True, help="Run output directory")
    parser.add_argument("--reference", required=True, help="Frozen reference h5ad")
    parser.add_argument("--metadata", required=True, help="Frozen reference metadata csv")
    parser.add_argument("--stage-axis", default="sample_week", help="Stage axis. Fixed default: sample_week")
    parser.add_argument(
        "--provenance-script",
        default="provenance_audit_h5ad.py",
        help="Path to provenance audit script",
    )
    parser.add_argument(
        "--provenance-fields",
        nargs="+",
        default=DEFAULT_PROVENANCE_FIELDS,
        help="Obs fields to audit in preflight provenance step",
    )
    parser.add_argument(
        "--whole-lung-cmd-template",
        default=None,
        help="Shell command template for whole-lung stage",
    )
    parser.add_argument(
        "--whole-lung-cmd-template-file",
        default=None,
        help="Text file containing the whole-lung command template",
    )
    parser.add_argument(
        "--epi-cmd-template",
        default=None,
        help="Shell command template for epithelial stage",
    )
    parser.add_argument(
        "--epi-cmd-template-file",
        default=None,
        help="Text file containing the epithelial command template",
    )
    parser.add_argument(
        "--query-id",
        nargs="*",
        default=None,
        help="Optional subset of query_id values to run",
    )
    parser.add_argument(
        "--stop-after",
        choices=["preflight", "whole_lung", "epithelial", "compare"],
        default="compare",
        help="Stop after the selected stage",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print/record commands without running them")
    parser.add_argument("--fail-fast", action="store_true", help="Stop on first stage failure")
    args = parser.parse_args()

    if args.stage_axis != "sample_week":
        raise UserFacingError(
            f"This Week-1 runner fixes --stage-axis to sample_week, got: {args.stage_axis!r}"
        )

    manifest_path = Path(args.manifest).resolve()
    outdir = Path(args.outdir).resolve()
    reference = Path(args.reference).resolve()
    metadata = Path(args.metadata).resolve()
    provenance_script = Path(args.provenance_script).resolve()

    if not reference.exists():
        raise UserFacingError(f"Reference file not found: {reference}")
    if not metadata.exists():
        raise UserFacingError(f"Metadata file not found: {metadata}")

    manifest_df = read_manifest(manifest_path)
    if args.query_id:
        requested = {normalize_query_id(x) for x in args.query_id}
        missing = requested.difference(set(manifest_df["query_id"]))
        if missing:
            raise UserFacingError(f"Requested --query-id not present in manifest: {sorted(missing)}")
        manifest_df = manifest_df[manifest_df["query_id"].isin(requested)].copy()

    dirs = ensure_dirs(outdir)
    manifest_resolved_path = dirs["config"] / "manifest_resolved.csv"
    manifest_df.to_csv(manifest_resolved_path, index=False)
    shutil.copy2(manifest_path, dirs["config"] / manifest_path.name)

    whole_lung_template = read_text_template(
        args.whole_lung_cmd_template, args.whole_lung_cmd_template_file
    )
    epi_template = read_text_template(args.epi_cmd_template, args.epi_cmd_template_file)

    config_payload = {
        "manifest": str(manifest_path),
        "manifest_resolved": str(manifest_resolved_path),
        "outdir": str(outdir),
        "reference": str(reference),
        "metadata": str(metadata),
        "stage_axis": args.stage_axis,
        "provenance_script": str(provenance_script),
        "provenance_fields": list(args.provenance_fields),
        "whole_lung_cmd_template": whole_lung_template,
        "epi_cmd_template": epi_template,
        "stop_after": args.stop_after,
        "dry_run": bool(args.dry_run),
        "fail_fast": bool(args.fail_fast),
    }
    write_json(dirs["config"] / "run_config.json", config_payload)

    status_rows: List[Dict[str, Any]] = []

    # Stage 0: provenance preflight across all enabled queries.
    preflight_result = run_provenance_preflight(
        manifest_df=manifest_df,
        provenance_script=provenance_script,
        provenance_outdir=dirs["provenance"],
        fields=args.provenance_fields,
        dry_run=args.dry_run,
        root_logs=dirs["logs"],
    )
    write_json(dirs["config"] / "preflight_result.json", preflight_result.__dict__)

    if preflight_result.status == "failed":
        raise UserFacingError(
            f"Preflight provenance failed. See logs: {preflight_result.stderr_log}"
        )

    if preflight_result.status != "dry_run":
        prov_check = build_provenance_expectation_check(manifest_df, dirs["provenance"])
        prov_check.to_csv(dirs["compare"] / "all_queries_provenance_check.csv", index=False)

    if args.stop_after == "preflight":
        return

    # Per-query stages.
    for row in manifest_df.to_dict(orient="records"):
        query_id = row["query_id"]
        enabled = bool(row.get("enabled", True))
        context = build_context(row, dirs, argparse.Namespace(
            reference=reference,
            metadata=metadata,
            stage_axis=args.stage_axis,
        ))
        query_log_dir = Path(context["query_log_dir"])

        stage_record: Dict[str, Any] = {
            "query_id": query_id,
            "enabled": enabled,
            "note": row.get("note", ""),
            "whole_lung_status": "skipped",
            "whole_lung_message": "disabled" if not enabled else "not_run",
            "epi_status": "skipped",
            "epi_message": "disabled" if not enabled else "not_run",
        }

        if not enabled:
            status_rows.append(stage_record)
            continue

        # Whole-lung stage.
        if whole_lung_template:
            wl_run = run_subprocess_shell(
                command_template=whole_lung_template,
                raw_context=context,
                stage="whole_lung",
                query_id=query_id,
                log_dir=query_log_dir,
                dry_run=args.dry_run,
            )
            required = format_expected_files(Path(context["whole_lung_outdir"]), query_id, WHOLE_LUNG_REQUIRED_FILES)
            verify_status, verify_msg = verify_files(required, optional=False)

            stage_record.update(
                {
                    "whole_lung_command": wl_run.command,
                    "whole_lung_returncode": wl_run.returncode,
                    "whole_lung_stdout_log": wl_run.stdout_log,
                    "whole_lung_stderr_log": wl_run.stderr_log,
                }
            )
            if wl_run.status in {"ok", "dry_run"} and (wl_run.status == "dry_run" or verify_status == "ok"):
                stage_record["whole_lung_status"] = wl_run.status
                stage_record["whole_lung_message"] = wl_run.message if wl_run.status == "dry_run" else verify_msg
            else:
                stage_record["whole_lung_status"] = "failed"
                stage_record["whole_lung_message"] = verify_msg if wl_run.status == "ok" else wl_run.message
                status_rows.append(stage_record)
                if args.fail_fast:
                    write_run_status_csv(dirs["compare"] / "all_queries_run_status.csv", status_rows)
                    raise UserFacingError(
                        f"Whole-lung stage failed for {query_id}. See logs in {query_log_dir}"
                    )
                continue
        else:
            stage_record["whole_lung_status"] = "not_configured"
            stage_record["whole_lung_message"] = "No --whole-lung-cmd-template provided."

        if args.stop_after == "whole_lung":
            status_rows.append(stage_record)
            continue

        # Epithelial stage.
        if epi_template:
            epi_run = run_subprocess_shell(
                command_template=epi_template,
                raw_context=context,
                stage="epithelial",
                query_id=query_id,
                log_dir=query_log_dir,
                dry_run=args.dry_run,
            )
            required = format_expected_files(Path(context["epi_outdir"]), query_id, EPI_REQUIRED_FILES)
            optional_paths = format_expected_files(Path(context["epi_outdir"]), query_id, EPI_OPTIONAL_FILES)
            verify_status, verify_msg = verify_files(required, optional=False)
            optional_status, optional_msg = verify_files(optional_paths, optional=True)

            stage_record.update(
                {
                    "epi_command": epi_run.command,
                    "epi_returncode": epi_run.returncode,
                    "epi_stdout_log": epi_run.stdout_log,
                    "epi_stderr_log": epi_run.stderr_log,
                    "epi_optional_files_status": optional_status,
                    "epi_optional_files_message": optional_msg,
                }
            )
            if epi_run.status in {"ok", "dry_run"} and (epi_run.status == "dry_run" or verify_status == "ok"):
                stage_record["epi_status"] = epi_run.status
                stage_record["epi_message"] = epi_run.message if epi_run.status == "dry_run" else verify_msg
            else:
                stage_record["epi_status"] = "failed"
                stage_record["epi_message"] = verify_msg if epi_run.status == "ok" else epi_run.message
                status_rows.append(stage_record)
                if args.fail_fast:
                    write_run_status_csv(dirs["compare"] / "all_queries_run_status.csv", status_rows)
                    raise UserFacingError(
                        f"Epithelial stage failed for {query_id}. See logs in {query_log_dir}"
                    )
                continue
        else:
            stage_record["epi_status"] = "not_configured"
            stage_record["epi_message"] = "No --epi-cmd-template provided."

        status_rows.append(stage_record)

    write_run_status_csv(dirs["compare"] / "all_queries_run_status.csv", status_rows)

    # Cross-query compare tables.
    query_ids = manifest_df.loc[manifest_df["enabled"], "query_id"].tolist()
    key_metrics_rows = [
        build_key_metrics_row(row, dirs["provenance"], dirs["whole_lung"], dirs["epithelial"])
        for row in manifest_df.to_dict(orient="records")
        if bool(row.get("enabled", True))
    ]
    pd.DataFrame(key_metrics_rows).to_csv(
        dirs["compare"] / "all_queries_key_metrics.csv", index=False
    )

    state_compare = concat_per_query_csvs(query_ids, dirs["epithelial"], "epi_state_fine.csv")
    if not state_compare.empty:
        state_compare.to_csv(dirs["compare"] / "all_queries_epi_state_fine_compare.csv", index=False)

    stage_compare = concat_per_query_csvs(query_ids, dirs["epithelial"], "epi_stage_fine.csv")
    if not stage_compare.empty:
        stage_compare.to_csv(dirs["compare"] / "all_queries_epi_stage_fine_compare.csv", index=False)

    boundary_compare = concat_per_query_csvs(
        query_ids, dirs["epithelial"], "epi_state_boundary_pairs_unordered.csv"
    )
    if not boundary_compare.empty:
        boundary_compare.to_csv(
            dirs["compare"] / "all_queries_epi_boundary_pairs_compare.csv", index=False
        )


if __name__ == "__main__":
    try:
        main()
    except UserFacingError as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(2)
