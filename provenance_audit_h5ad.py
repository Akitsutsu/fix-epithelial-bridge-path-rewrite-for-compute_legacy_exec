
#!/usr/bin/env python3
"""
Provenance audit for query .h5ad files.

Purpose
-------
Summarize exact query provenance from obs metadata without touching the frozen
reference/remap basis. Default target fields are:
    sample_id, donor_id, source_type, batch_id

Outputs (per query)
-------------------
- <query_id>_obs_inventory.csv
- <query_id>_provenance_field_presence.csv
- <query_id>_provenance_exact_combinations.csv
- <query_id>_provenance_<field>.csv   (for each available target field)
- <query_id>_provenance_summary.json
- <query_id>_provenance_summary.md

Combined outputs
----------------
- all_queries_provenance_overview.csv
- all_queries_target_field_presence.csv

Notes
-----
1) Tries to use anndata if available.
2) Falls back to a lightweight h5py reader for AnnData .h5ad obs tables.
3) Supports both newer categorical encoding (per-column group with codes/categories)
   and older __categories style in obs.
"""

from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

import numpy as np
import pandas as pd


DEFAULT_FIELDS = ["sample_id", "donor_id", "source_type", "batch_id"]


def _decode_item(x: Any) -> Any:
    if isinstance(x, (bytes, np.bytes_)):
        return x.decode("utf-8", errors="replace")
    return x


def _decode_list(values: Iterable[Any]) -> List[Any]:
    return [_decode_item(v) for v in values]


def _normalize_1d(arr: Any) -> np.ndarray:
    out = np.asarray(arr)
    if out.ndim == 0:
        out = out.reshape(1)
    elif out.ndim > 1:
        if out.shape[1:] == (1,):
            out = out.reshape(out.shape[0])
        else:
            # Rare in obs. Keep first column as a best-effort fallback.
            out = out.reshape(out.shape[0], -1)[:, 0]
    return out


def _as_python_list(arr: Any) -> List[Any]:
    arr = _normalize_1d(arr)
    if arr.dtype.kind in {"S", "O", "U"}:
        return [_decode_item(v) for v in arr.tolist()]
    return arr.tolist()


def _safe_dtype_name(series: pd.Series) -> str:
    try:
        return str(series.dtype)
    except Exception:
        return "unknown"


def _series_to_preview(series: pd.Series, max_items: int = 5) -> str:
    non_null = series.dropna()
    if non_null.empty:
        return ""
    vals = pd.unique(non_null.astype(str))
    vals = vals[:max_items]
    return " | ".join(map(str, vals))


def _top_value(series: pd.Series) -> Tuple[Any, int]:
    ser = series.astype("object")
    ser = ser.where(~ser.isna(), "<NA>")
    vc = ser.astype(str).value_counts(dropna=False)
    if vc.empty:
        return "", 0
    return vc.index[0], int(vc.iloc[0])


def load_obs_with_anndata(path: str) -> pd.DataFrame:
    import anndata as ad  # type: ignore

    adata = ad.read_h5ad(path, backed="r")
    obs = adata.obs.copy()
    try:
        adata.file.close()
    except Exception:
        pass
    return obs


def _read_h5_dataset(ds: Any) -> pd.Series:
    arr = ds[()]
    vals = _as_python_list(arr)
    return pd.Series(vals)


def _read_categorical_group(group: Any) -> pd.Series:
    codes = np.asarray(group["codes"][()]).reshape(-1)
    categories = _as_python_list(group["categories"][()])
    out: List[Any] = []
    for code in codes:
        if code < 0 or code >= len(categories):
            out.append(pd.NA)
        else:
            out.append(categories[int(code)])
    return pd.Series(out, dtype="object")


def _read_nullable_group(group: Any) -> pd.Series:
    values = _normalize_1d(group["values"][()])
    mask = _normalize_1d(group["mask"][()]).astype(bool)
    vals = _as_python_list(values)
    out: List[Any] = []
    for v, m in zip(vals, mask):
        out.append(pd.NA if bool(m) else v)
    return pd.Series(out, dtype="object")


def _read_h5_node(node: Any) -> pd.Series:
    import h5py  # local import so the script can still parse help without h5py

    if isinstance(node, h5py.Dataset):
        return _read_h5_dataset(node)

    if isinstance(node, h5py.Group):
        encoding = _decode_item(node.attrs.get("encoding-type", "")) or ""
        if encoding == "categorical" or ("codes" in node and "categories" in node):
            return _read_categorical_group(node)
        if str(encoding).startswith("nullable") and "values" in node and "mask" in node:
            return _read_nullable_group(node)
        # Fallback for array-like groups that expose values/mask even without attrs.
        if "values" in node and "mask" in node:
            return _read_nullable_group(node)

    raise ValueError(f"Unsupported HDF5 node for obs column: {node}")


def load_obs_with_h5py(path: str) -> pd.DataFrame:
    import h5py

    with h5py.File(path, "r") as f:
        if "obs" not in f:
            raise KeyError(f"'obs' group not found in {path}")
        g = f["obs"]

        index_key = _decode_item(g.attrs.get("_index", "_index"))
        if index_key not in g and "_index" in g:
            index_key = "_index"

        raw_col_order = g.attrs.get("column-order", None)
        if raw_col_order is not None:
            columns = _decode_list(list(raw_col_order))
        else:
            columns = [
                _decode_item(k)
                for k in g.keys()
                if k not in {"_index", "__categories"}
            ]

        old_style_categories = g.get("__categories", None)

        data: Dict[str, pd.Series] = {}
        for col in columns:
            if col not in g:
                # Be tolerant of stale column-order attrs.
                continue

            node = g[col]
            if old_style_categories is not None and col in old_style_categories:
                codes = _normalize_1d(node[()]).astype(int)
                categories = _as_python_list(old_style_categories[col][()])
                vals: List[Any] = []
                for code in codes:
                    if code < 0 or code >= len(categories):
                        vals.append(pd.NA)
                    else:
                        vals.append(categories[int(code)])
                series = pd.Series(vals, dtype="object")
            else:
                series = _read_h5_node(node)

            data[col] = series.reset_index(drop=True).tolist()

        if index_key in g:
            idx = _read_h5_node(g[index_key])
            index = pd.Index(idx.astype(str).tolist(), name=str(index_key))
        else:
            # Fallback to RangeIndex if the h5ad is malformed.
            n = len(next(iter(data.values()))) if data else 0
            index = pd.RangeIndex(n, name="index")

        df = pd.DataFrame(data, index=index)
        return df


def load_obs(path: str) -> pd.DataFrame:
    try:
        return load_obs_with_anndata(path)
    except Exception:
        return load_obs_with_h5py(path)


def build_obs_inventory(df: pd.DataFrame, query_id: str, max_preview: int = 5) -> pd.DataFrame:
    rows: List[Dict[str, Any]] = []
    for col in df.columns:
        ser = df[col]
        non_null = ser.dropna()
        try:
            n_unique = int(non_null.nunique(dropna=True))
        except Exception:
            n_unique = int(pd.Series(non_null.astype(str)).nunique(dropna=True))

        top_val, top_count = _top_value(ser)
        rows.append(
            {
                "query_id": query_id,
                "field": col,
                "dtype": _safe_dtype_name(ser),
                "n_cells": int(len(ser)),
                "n_missing": int(ser.isna().sum()),
                "missing_fraction": float(ser.isna().mean()) if len(ser) else math.nan,
                "n_unique_non_null": n_unique,
                "example_values": _series_to_preview(ser, max_items=max_preview),
                "top_value": top_val,
                "top_count": int(top_count),
                "top_fraction": float(top_count / len(ser)) if len(ser) else math.nan,
            }
        )
    out = pd.DataFrame(rows).sort_values(
        by=["n_unique_non_null", "field"], ascending=[False, True]
    )
    return out


def build_target_field_presence(
    df: pd.DataFrame,
    query_id: str,
    fields: Sequence[str],
) -> Tuple[pd.DataFrame, List[str], List[str]]:
    rows: List[Dict[str, Any]] = []
    available: List[str] = []
    missing: List[str] = []
    for field in fields:
        present = field in df.columns
        if present:
            available.append(field)
            ser = df[field]
            top_val, top_count = _top_value(ser)
            try:
                n_unique = int(ser.dropna().nunique(dropna=True))
            except Exception:
                n_unique = int(pd.Series(ser.dropna().astype(str)).nunique(dropna=True))
            rows.append(
                {
                    "query_id": query_id,
                    "field": field,
                    "present": True,
                    "dtype": _safe_dtype_name(ser),
                    "n_cells": int(len(ser)),
                    "n_missing": int(ser.isna().sum()),
                    "missing_fraction": float(ser.isna().mean()) if len(ser) else math.nan,
                    "n_unique_non_null": n_unique,
                    "top_value": top_val,
                    "top_count": int(top_count),
                    "top_fraction": float(top_count / len(ser)) if len(ser) else math.nan,
                }
            )
        else:
            missing.append(field)
            rows.append(
                {
                    "query_id": query_id,
                    "field": field,
                    "present": False,
                    "dtype": "",
                    "n_cells": int(len(df)),
                    "n_missing": int(len(df)),
                    "missing_fraction": 1.0 if len(df) else math.nan,
                    "n_unique_non_null": 0,
                    "top_value": "",
                    "top_count": 0,
                    "top_fraction": 0.0,
                }
            )
    return pd.DataFrame(rows), available, missing


def build_exact_combinations(
    df: pd.DataFrame,
    query_id: str,
    available_fields: Sequence[str],
) -> pd.DataFrame:
    if not available_fields:
        return pd.DataFrame(
            {
                "query_id": [query_id],
                "n_cells": [int(len(df))],
                "fraction": [1.0 if len(df) else math.nan],
            }
        )

    combo = df.loc[:, list(available_fields)].copy()
    combo = combo.astype("object").where(~combo.isna(), "<NA>")
    out = (
        combo.groupby(list(available_fields), dropna=False)
        .size()
        .reset_index(name="n_cells")
        .sort_values("n_cells", ascending=False)
        .reset_index(drop=True)
    )
    out.insert(0, "query_id", query_id)
    out["fraction"] = out["n_cells"] / len(df) if len(df) else math.nan
    return out


def build_single_field_counts(
    df: pd.DataFrame,
    query_id: str,
    field: str,
) -> pd.DataFrame:
    ser = df[field].astype("object").where(~df[field].isna(), "<NA>")
    out = (
        ser.value_counts(dropna=False)
        .rename_axis(field)
        .reset_index(name="n_cells")
        .sort_values("n_cells", ascending=False)
        .reset_index(drop=True)
    )
    out.insert(0, "query_id", query_id)
    out["fraction"] = out["n_cells"] / len(df) if len(df) else math.nan
    return out


def _jsonable_value(x: Any) -> Any:
    if pd.isna(x):
        return None
    if isinstance(x, (np.integer, np.floating)):
        return x.item()
    return x


def build_summary_json(
    df: pd.DataFrame,
    query_id: str,
    requested_fields: Sequence[str],
    available_fields: Sequence[str],
    missing_fields: Sequence[str],
    exact_combinations: pd.DataFrame,
    field_presence: pd.DataFrame,
) -> Dict[str, Any]:
    field_summaries: Dict[str, Any] = {}
    for _, row in field_presence.iterrows():
        field = str(row["field"])
        field_summaries[field] = {
            "present": bool(row["present"]),
            "dtype": row["dtype"],
            "n_missing": int(row["n_missing"]),
            "missing_fraction": float(row["missing_fraction"])
            if pd.notna(row["missing_fraction"])
            else None,
            "n_unique_non_null": int(row["n_unique_non_null"]),
            "top_value": _jsonable_value(row["top_value"]),
            "top_count": int(row["top_count"]),
            "top_fraction": float(row["top_fraction"])
            if pd.notna(row["top_fraction"])
            else None,
        }

    top_combo_records: List[Dict[str, Any]] = []
    for _, row in exact_combinations.head(10).iterrows():
        record: Dict[str, Any] = {
            "n_cells": int(row["n_cells"]),
            "fraction": float(row["fraction"]) if pd.notna(row["fraction"]) else None,
        }
        for field in available_fields:
            if field in row:
                record[field] = _jsonable_value(row[field])
        top_combo_records.append(record)

    return {
        "query_id": query_id,
        "n_cells_total": int(len(df)),
        "requested_fields": list(requested_fields),
        "available_fields": list(available_fields),
        "missing_fields": list(missing_fields),
        "n_exact_combinations": int(len(exact_combinations)),
        "top_exact_combinations": top_combo_records,
        "field_summaries": field_summaries,
    }


def build_summary_markdown(
    summary: Mapping[str, Any],
    field_presence: pd.DataFrame,
    exact_combinations: pd.DataFrame,
) -> str:
    qid = summary["query_id"]
    lines: List[str] = []
    lines.append(f"# {qid} provenance audit")
    lines.append("")
    lines.append(f"- n_cells_total: {summary['n_cells_total']}")
    lines.append(f"- available_fields: {', '.join(summary['available_fields']) or '(none)'}")
    lines.append(f"- missing_fields: {', '.join(summary['missing_fields']) or '(none)'}")
    lines.append(f"- n_exact_combinations: {summary['n_exact_combinations']}")
    lines.append("")

    lines.append("## Target field presence")
    lines.append("")
    fp = field_presence.copy()
    fp["present"] = fp["present"].astype(str)
    cols = [
        "field",
        "present",
        "dtype",
        "n_missing",
        "missing_fraction",
        "n_unique_non_null",
        "top_value",
        "top_count",
        "top_fraction",
    ]
    lines.extend(_markdown_table(fp[cols].head(len(fp))))
    lines.append("")

    lines.append("## Top exact provenance combinations")
    lines.append("")
    if len(exact_combinations) == 0:
        lines.append("(none)")
    else:
        max_rows = min(20, len(exact_combinations))
        lines.extend(_markdown_table(exact_combinations.head(max_rows)))
    lines.append("")
    return "\n".join(lines)


def _markdown_table(df: pd.DataFrame) -> List[str]:
    if df.empty:
        return ["(empty)"]
    tmp = df.copy()
    for col in tmp.columns:
        tmp[col] = tmp[col].apply(lambda x: "" if pd.isna(x) else str(x))
    header = "| " + " | ".join(tmp.columns.astype(str)) + " |"
    sep = "| " + " | ".join(["---"] * len(tmp.columns)) + " |"
    rows = [
        "| " + " | ".join(row.astype(str).tolist()) + " |"
        for _, row in tmp.iterrows()
    ]
    return [header, sep] + rows


def parse_input_item(item: str) -> Tuple[str, str]:
    if "=" not in item:
        raise argparse.ArgumentTypeError(
            f"Invalid --input '{item}'. Use QUERY_ID=/path/to/query.h5ad"
        )
    query_id, path = item.split("=", 1)
    query_id = query_id.strip()
    path = path.strip()
    if not query_id:
        raise argparse.ArgumentTypeError(f"Empty query id in --input '{item}'")
    if not path:
        raise argparse.ArgumentTypeError(f"Empty path in --input '{item}'")
    return query_id, path


def run_one_query(
    query_id: str,
    path: str,
    outdir: Path,
    fields: Sequence[str],
    max_preview: int,
) -> Dict[str, Any]:
    df = load_obs(path)
    query_outdir = outdir / query_id
    query_outdir.mkdir(parents=True, exist_ok=True)

    inventory = build_obs_inventory(df, query_id=query_id, max_preview=max_preview)
    field_presence, available_fields, missing_fields = build_target_field_presence(
        df=df, query_id=query_id, fields=fields
    )
    exact = build_exact_combinations(df, query_id=query_id, available_fields=available_fields)

    inventory_path = query_outdir / f"{query_id}_obs_inventory.csv"
    field_presence_path = query_outdir / f"{query_id}_provenance_field_presence.csv"
    exact_path = query_outdir / f"{query_id}_provenance_exact_combinations.csv"

    inventory.to_csv(inventory_path, index=False)
    field_presence.to_csv(field_presence_path, index=False)
    exact.to_csv(exact_path, index=False)

    per_field_paths: Dict[str, str] = {}
    for field in available_fields:
        field_counts = build_single_field_counts(df, query_id=query_id, field=field)
        path_field = query_outdir / f"{query_id}_provenance_{field}.csv"
        field_counts.to_csv(path_field, index=False)
        per_field_paths[field] = str(path_field)

    summary = build_summary_json(
        df=df,
        query_id=query_id,
        requested_fields=fields,
        available_fields=available_fields,
        missing_fields=missing_fields,
        exact_combinations=exact,
        field_presence=field_presence,
    )
    summary["source_query_path"] = path
    summary["output_dir"] = str(query_outdir)
    summary["files"] = {
        "obs_inventory": str(inventory_path),
        "field_presence": str(field_presence_path),
        "exact_combinations": str(exact_path),
        "per_field_counts": per_field_paths,
    }

    summary_json_path = query_outdir / f"{query_id}_provenance_summary.json"
    with open(summary_json_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    summary_md_path = query_outdir / f"{query_id}_provenance_summary.md"
    with open(summary_md_path, "w", encoding="utf-8") as f:
        f.write(build_summary_markdown(summary, field_presence, exact))

    print(f"[done] {query_id}: n_cells={len(df)}, available_fields={available_fields}")
    top_row = exact.iloc[0].to_dict() if len(exact) else {}
    if top_row:
        top_n = int(top_row.get("n_cells", 0))
        top_frac = float(top_row.get("fraction", 0.0))
        combo_bits = []
        for field in available_fields:
            combo_bits.append(f"{field}={top_row.get(field)}")
        combo_str = ", ".join(combo_bits) if combo_bits else "(no target fields)"
        print(f"       top_combo: {combo_str} -> {top_n} cells ({top_frac:.3f})")

    return {
        "query_id": query_id,
        "n_cells_total": int(len(df)),
        "available_fields": ",".join(available_fields),
        "missing_fields": ",".join(missing_fields),
        "n_exact_combinations": int(len(exact)),
        "top_exact_combo_n_cells": int(exact.iloc[0]["n_cells"]) if len(exact) else 0,
        "top_exact_combo_fraction": float(exact.iloc[0]["fraction"]) if len(exact) else None,
        "summary_json_path": str(summary_json_path),
        "summary_md_path": str(summary_md_path),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit query provenance from h5ad obs metadata.")
    parser.add_argument(
        "--input",
        required=True,
        nargs="+",
        help="One or more QUERY_ID=/path/to/query.h5ad items.",
    )
    parser.add_argument(
        "--outdir",
        required=True,
        help="Output directory.",
    )
    parser.add_argument(
        "--fields",
        nargs="+",
        default=DEFAULT_FIELDS,
        help=f"Target obs fields to summarize. Default: {' '.join(DEFAULT_FIELDS)}",
    )
    parser.add_argument(
        "--max-preview",
        type=int,
        default=5,
        help="Max unique example values shown per obs field in inventory.",
    )
    args = parser.parse_args()

    inputs = [parse_input_item(item) for item in args.input]
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    overview_rows: List[Dict[str, Any]] = []
    presence_rows: List[pd.DataFrame] = []

    for query_id, path in inputs:
        row = run_one_query(
            query_id=query_id,
            path=path,
            outdir=outdir,
            fields=args.fields,
            max_preview=args.max_preview,
        )
        overview_rows.append(row)

        # Read back field presence from the generated CSV for a combined file.
        fp = pd.read_csv(outdir / query_id / f"{query_id}_provenance_field_presence.csv")
        presence_rows.append(fp)

    overview = pd.DataFrame(overview_rows).sort_values("query_id")
    overview.to_csv(outdir / "all_queries_provenance_overview.csv", index=False)

    if presence_rows:
        combined_presence = pd.concat(presence_rows, ignore_index=True)
        combined_presence.to_csv(outdir / "all_queries_target_field_presence.csv", index=False)

    print(f"[done] wrote combined outputs to {outdir}")


if __name__ == "__main__":
    main()
