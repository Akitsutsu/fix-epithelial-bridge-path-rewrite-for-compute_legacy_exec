#!/usr/bin/env python3
"""Flag suspicious hard-coded remnants in a rewritten legacy debug script.

Typical use:
    python scan_rewritten_script_for_hardcodes.py \
        benchmark_run_v1_compute_legacy/epithelial/BU3/BU3_epithelial_rewritten_debug.py
"""
from __future__ import annotations

import argparse
from pathlib import Path

DEFAULT_PATTERNS = [
    "prototype_out_epi_v1",
    "prototype_out_epi_v1_BU3",
    "prototype_out_v1",
    "converted/query_CA1_clean.h5ad",
    "converted/query_BU3_clean.h5ad",
    "query_CA1_organoid_01",
    "query_BU3_organoid_01",
    "CA1_",
    "BU3_",
    "WHOLELUNG_GATE_CSV",
    "REFERENCE_H5AD",
    "REFERENCE_META",
    "QUERY_H5AD",
    "OUTDIR",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("script_path", help="Path to rewritten debug .py script")
    parser.add_argument("--pattern", action="append", default=[], help="Additional token to scan for")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    script_path = Path(args.script_path)
    text = script_path.read_text(encoding="utf-8", errors="replace")
    patterns = DEFAULT_PATTERNS + list(args.pattern)

    print(f"script: {script_path}")
    hits = 0
    for token in patterns:
        lines = []
        for idx, line in enumerate(text.splitlines(), start=1):
            if token in line:
                lines.append((idx, line.strip()))
        if not lines:
            continue
        hits += len(lines)
        print(f"\n[token] {token}")
        for idx, line in lines[:20]:
            print(f"  L{idx}: {line}")
        if len(lines) > 20:
            print(f"  ... {len(lines) - 20} more")

    if hits == 0:
        print("No suspicious tokens found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
