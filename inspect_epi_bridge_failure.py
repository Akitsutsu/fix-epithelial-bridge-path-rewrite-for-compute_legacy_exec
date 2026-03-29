#!/usr/bin/env python3
"""Summarize the current epithelial compute-bridge failure surface.

Expected use:
    python inspect_epi_bridge_failure.py \
        --run-dir benchmark_run_v1_compute_legacy \
        --query-ids CA1 BU3 \
        --write-json triage_summary.json

The script does not assume exact file layout beyond the names already frozen in
handoff notes. It performs a mostly heuristic scan and reports what exists,
what is missing, and what the stderr logs appear to contain.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


TRACEBACK_RE = re.compile(r"Traceback \(most recent call last\):", re.MULTILINE)
EXCEPTION_LINE_RE = re.compile(r"^(?P<etype>[A-Za-z_][A-Za-z0-9_]*(?:Error|Exception|Warning)?): (?P<msg>.+)$")


@dataclass(slots=True)
class QueryFailureSummary:
    query_id: str
    epithelial_stderr_exists: bool = False
    epithelial_stderr_path: str | None = None
    stderr_last_nonempty_line: str | None = None
    stderr_exception_type: str | None = None
    stderr_exception_message: str | None = None
    stderr_has_traceback: bool = False
    whole_lung_adapter_meta_exists: bool = False
    epithelial_adapter_meta_exists: bool = False
    whole_lung_adapter_meta_path: str | None = None
    epithelial_adapter_meta_path: str | None = None
    epithelial_summary_exists: bool = False
    epithelial_summary_paths: list[str] = field(default_factory=list)
    epithelial_stage_fine_exists: bool = False
    epithelial_stage_fine_paths: list[str] = field(default_factory=list)
    epithelial_state_fine_exists: bool = False
    epithelial_state_fine_paths: list[str] = field(default_factory=list)
    suspicious_files: list[str] = field(default_factory=list)


@dataclass(slots=True)
class RunSummary:
    run_dir: str
    query_ids: list[str]
    key_metrics_csv_exists: bool = False
    key_metrics_csv_path: str | None = None
    key_metrics_columns: list[str] = field(default_factory=list)
    epithelial_metric_like_columns: list[str] = field(default_factory=list)
    queries: list[QueryFailureSummary] = field(default_factory=list)


def read_text_if_exists(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def extract_exception(stderr_text: str) -> tuple[str | None, str | None]:
    lines = [line.strip() for line in stderr_text.splitlines() if line.strip()]
    for line in reversed(lines):
        match = EXCEPTION_LINE_RE.match(line)
        if match:
            return match.group("etype"), match.group("msg")
    return None, None


def find_one(root: Path, pattern: str) -> Path | None:
    matches = sorted(root.glob(pattern))
    return matches[0] if matches else None


def find_many(root: Path, pattern: str) -> list[Path]:
    return sorted(root.glob(pattern))


def summarize_query(run_dir: Path, query_id: str) -> QueryFailureSummary:
    summary = QueryFailureSummary(query_id=query_id)

    stderr_path = run_dir / "logs" / query_id / "epithelial.stderr.log"
    if stderr_path.exists():
        summary.epithelial_stderr_exists = True
        summary.epithelial_stderr_path = str(stderr_path)
        text = read_text_if_exists(stderr_path)
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        summary.stderr_last_nonempty_line = lines[-1] if lines else None
        summary.stderr_has_traceback = bool(TRACEBACK_RE.search(text))
        etype, emsg = extract_exception(text)
        summary.stderr_exception_type = etype
        summary.stderr_exception_message = emsg

    whole_lung_meta = find_one(run_dir, f"**/{query_id}_whole_lung_adapter_meta.json")
    epithelial_meta = find_one(run_dir, f"**/{query_id}_epithelial_adapter_meta.json")
    if whole_lung_meta is not None:
        summary.whole_lung_adapter_meta_exists = True
        summary.whole_lung_adapter_meta_path = str(whole_lung_meta)
    if epithelial_meta is not None:
        summary.epithelial_adapter_meta_exists = True
        summary.epithelial_adapter_meta_path = str(epithelial_meta)

    epi_summary = find_many(run_dir, f"**/{query_id}_epi_summary_v1.json")
    stage_fine = find_many(run_dir, f"**/{query_id}_epi_stage_fine*")
    state_fine = find_many(run_dir, f"**/{query_id}_epi_state_fine*")

    summary.epithelial_summary_exists = bool(epi_summary)
    summary.epithelial_summary_paths = [str(p) for p in epi_summary]
    summary.epithelial_stage_fine_exists = bool(stage_fine)
    summary.epithelial_stage_fine_paths = [str(p) for p in stage_fine]
    summary.epithelial_state_fine_exists = bool(state_fine)
    summary.epithelial_state_fine_paths = [str(p) for p in state_fine]

    suspicious_patterns = [
        f"**/*{query_id}*rewritten*debug*.py",
        f"**/*{query_id}*traceback*.txt",
        f"**/*{query_id}*adapter_meta*.json",
    ]
    suspicious: list[str] = []
    for pattern in suspicious_patterns:
        suspicious.extend(str(p) for p in find_many(run_dir, pattern))
    summary.suspicious_files = sorted(set(suspicious))
    return summary


def summarize_key_metrics(run_dir: Path) -> tuple[bool, str | None, list[str], list[str]]:
    key_metrics = run_dir / "compare" / "all_queries_key_metrics.csv"
    if not key_metrics.exists():
        key_metrics = run_dir / "all_queries_key_metrics.csv"
    if not key_metrics.exists():
        return False, None, [], []

    with key_metrics.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        columns = reader.fieldnames or []
    epi_like = [c for c in columns if ("epi" in c.lower() or "epithelial" in c.lower())]
    return True, str(key_metrics), columns, epi_like


def build_summary(run_dir: Path, query_ids: list[str]) -> RunSummary:
    exists, path, columns, epi_cols = summarize_key_metrics(run_dir)
    return RunSummary(
        run_dir=str(run_dir),
        query_ids=query_ids,
        key_metrics_csv_exists=exists,
        key_metrics_csv_path=path,
        key_metrics_columns=columns,
        epithelial_metric_like_columns=epi_cols,
        queries=[summarize_query(run_dir, qid) for qid in query_ids],
    )


def render_text(summary: RunSummary) -> str:
    lines: list[str] = []
    lines.append(f"run_dir: {summary.run_dir}")
    if summary.key_metrics_csv_exists:
        lines.append(f"key_metrics_csv: {summary.key_metrics_csv_path}")
        if summary.epithelial_metric_like_columns:
            joined = ", ".join(summary.epithelial_metric_like_columns)
            lines.append(f"epithelial_metric_like_columns: {joined}")
        else:
            lines.append("epithelial_metric_like_columns: <none>")
    else:
        lines.append("key_metrics_csv: <missing>")

    for q in summary.queries:
        lines.append("")
        lines.append(f"[{q.query_id}]")
        lines.append(f"  stderr_exists: {q.epithelial_stderr_exists}")
        if q.epithelial_stderr_path:
            lines.append(f"  stderr_path: {q.epithelial_stderr_path}")
        lines.append(f"  stderr_has_traceback: {q.stderr_has_traceback}")
        if q.stderr_exception_type:
            lines.append(f"  stderr_exception: {q.stderr_exception_type}: {q.stderr_exception_message}")
        elif q.stderr_last_nonempty_line:
            lines.append(f"  stderr_last_line: {q.stderr_last_nonempty_line}")
        lines.append(f"  whole_lung_adapter_meta_exists: {q.whole_lung_adapter_meta_exists}")
        lines.append(f"  epithelial_adapter_meta_exists: {q.epithelial_adapter_meta_exists}")
        if q.whole_lung_adapter_meta_path:
            lines.append(f"  whole_lung_adapter_meta_path: {q.whole_lung_adapter_meta_path}")
        if q.epithelial_adapter_meta_path:
            lines.append(f"  epithelial_adapter_meta_path: {q.epithelial_adapter_meta_path}")
        lines.append(f"  epithelial_summary_exists: {q.epithelial_summary_exists}")
        lines.append(f"  epithelial_stage_fine_exists: {q.epithelial_stage_fine_exists}")
        lines.append(f"  epithelial_state_fine_exists: {q.epithelial_state_fine_exists}")
        if q.suspicious_files:
            lines.append("  related_debug_like_files:")
            for path in q.suspicious_files:
                lines.append(f"    - {path}")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True, help="Path to benchmark_run_v1_compute_legacy")
    parser.add_argument("--query-ids", nargs="+", default=["CA1", "BU3"])
    parser.add_argument("--write-json", help="Optional path to save structured JSON summary")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    run_dir = Path(args.run_dir)
    summary = build_summary(run_dir, list(args.query_ids))
    print(render_text(summary))

    if args.write_json:
        out = Path(args.write_json)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(asdict(summary), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
