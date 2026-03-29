#!/usr/bin/env python3
"""Check whether CA1/BU3 replay outputs reproduce frozen benchmark key metrics."""

from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Dict, Any

import pandas as pd

EXPECTED = {
    "CA1": {
        "n_query_cells": 1719,
        "n_query_epi_eligible": 1522,
        "lineage_off_target_fraction": 0.1146,
        "top_stage": "week_15",
        "top_state": "Basal cells",
    },
    "BU3": {
        "n_query_cells": 731,
        "n_query_epi_eligible": 718,
        "lineage_off_target_fraction": 0.0178,
        "top_stage": "week_15",
        "top_state": "Basal cells",
    },
}


def almost_equal(a: Any, b: Any, tol: float) -> bool:
    try:
        return math.isclose(float(a), float(b), rel_tol=0.0, abs_tol=tol)
    except Exception:
        return False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--key-metrics", required=True, help="Path to all_queries_key_metrics.csv")
    parser.add_argument("--tol", type=float, default=1e-4, help="Absolute tolerance for numeric checks")
    args = parser.parse_args()

    path = Path(args.key_metrics).resolve()
    df = pd.read_csv(path)

    failures = []
    for qid, exp in EXPECTED.items():
        sub = df[df["query_id"].astype(str) == qid]
        if sub.empty:
            failures.append(f"missing query_id={qid}")
            continue
        row = sub.iloc[0].to_dict()
        for key, val in exp.items():
            obs = row.get(key)
            if isinstance(val, (int, float)):
                if not almost_equal(obs, val, args.tol):
                    failures.append(f"{qid}:{key} expected={val} observed={obs}")
            else:
                if str(obs) != str(val):
                    failures.append(f"{qid}:{key} expected={val!r} observed={obs!r}")

    if failures:
        print("[fail] exemplar reproduction check failed")
        for msg in failures:
            print(" -", msg)
        raise SystemExit(1)

    print("[pass] exemplar reproduction check passed")
    print(path)


if __name__ == "__main__":
    main()
