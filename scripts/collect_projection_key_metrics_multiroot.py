
#!/usr/bin/env python3
import argparse, csv, json
from pathlib import Path
from typing import Dict, Any, Optional, List

def read_tsv(path: Path) -> List[Dict[str,str]]:
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f, delimiter='\t'))

def choose(d: Dict[str, Any], *keys: str):
    for k in keys:
        if k in d and d[k] not in ("", None):
            return d[k]
    return ""

def load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open(encoding='utf-8') as f:
        return json.load(f)

def find_whole_lung_summary(root: Path, q: str) -> Optional[Path]:
    candidates = [
        root / "whole_lung" / q / f"{q}_summary_v1.json",
        root / q / "whole_lung" / f"{q}_summary_v1.json",
    ]
    for p in candidates:
        if p.exists():
            return p
    hits = sorted(root.rglob(f"{q}_summary_v1.json"))
    return hits[0] if hits else None

def find_epi_summary(root: Path, q: str) -> Optional[Path]:
    candidates = [
        root / "epithelial" / q / f"{q}_epi_summary_v1.json",
        root / q / "epithelial" / f"{q}_epi_summary_v1.json",
    ]
    for p in candidates:
        if p.exists():
            return p
    hits = sorted(root.rglob(f"{q}_epi_summary_v1.json"))
    return hits[0] if hits else None

def row_from_summaries(q: str, root: Path, sample_meta: Dict[str, Dict[str,str]]) -> Dict[str, Any]:
    wl_path = find_whole_lung_summary(root, q)
    epi_path = find_epi_summary(root, q)
    wl = load_json(wl_path) if wl_path else {}
    epi = load_json(epi_path) if epi_path else {}

    row = {
        "query_id": q,
        "run_root": str(root),
        "whole_lung_summary": str(wl_path) if wl_path else "",
        "epi_summary": str(epi_path) if epi_path else "",
        "top_stage_fine": choose(wl, "top_stage_fine", "top_stage"),
        "top_stage_coarse": choose(wl, "top_stage_coarse"),
        "top_state_fine": choose(epi, "top_state_fine", "top_epi_state_fine", "top_state"),
        "top_state_coarse": choose(wl, "top_state_coarse", "lineage_top_state_coarse"),
        "off_target_fraction": choose(wl, "lineage_off_target_fraction", "off_target_fraction"),
        "n_query_cells": choose(wl, "n_query_cells", "query_cell_count"),
        "n_query_epi_eligible": choose(epi, "n_query_epi_eligible", "query_cell_count", "n_query_cells"),
        "n_common_genes": choose(wl, "n_common_genes"),
    }
    sm = sample_meta.get(q, {})
    row.update({
        "sample_sheet_donor_id": sm.get("donor_id",""),
        "sample_sheet_stage": sm.get("stage_label",""),
        "sample_sheet_passage": sm.get("passage",""),
        "sample_sheet_cells": sm.get("cell_count_post_qc",""),
        "sample_sheet_local_query_sample_id": sm.get("local_query_sample_id",""),
        "sample_sheet_h5ad_path": sm.get("output_h5ad_path",""),
    })
    return row

def build_sample_meta(path: Optional[Path]) -> Dict[str, Dict[str,str]]:
    if not path:
        return {}
    rows = read_tsv(path)
    out = {}
    for r in rows:
        qid = r.get("query_id","") or r.get("local_query_sample_id","")
        if qid:
            out[qid] = r
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--query-id", nargs="+", required=True)
    ap.add_argument("--run-root", nargs="+", required=True,
                    help="One or more per-query run roots, same order as --query-id, or a single root reused for all.")
    ap.add_argument("--sample-sheet")
    ap.add_argument("--output-tsv", required=True)
    args = ap.parse_args()

    if len(args.run_root) not in (1, len(args.query_id)):
        raise SystemExit("--run-root must be either one path or the same count as --query-id")
    sample_meta = build_sample_meta(Path(args.sample_sheet) if args.sample_sheet else None)
    roots = [Path(args.run_root[0])] * len(args.query_id) if len(args.run_root) == 1 else [Path(x) for x in args.run_root]

    rows = [row_from_summaries(q, r, sample_meta) for q, r in zip(args.query_id, roots)]
    out = Path(args.output_tsv)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    print(f"[write] {out} (rows={len(rows)})")
    for r in rows:
        print(r["query_id"], r["top_stage_fine"], r["top_state_fine"], r["off_target_fraction"], r["whole_lung_summary"], r["epi_summary"])

if __name__ == "__main__":
    main()
