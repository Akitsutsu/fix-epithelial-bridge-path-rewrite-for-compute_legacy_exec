from pathlib import Path
import json
import numpy as np
import pandas as pd
import anndata as ad
from scipy import sparse
from scipy.sparse import diags

# =========================
# User-editable paths
# =========================
REFERENCE_H5AD = "converted/reference_RNA.h5ad"
REFERENCE_META = "converted/reference_metadata_v1.csv"
QUERY_H5AD = "converted/query_BU3_clean.h5ad"
WHOLELUNG_GATE_CSV = "prototype_out_v1/BU3_cell_projection_v1.csv"
OUTDIR = "prototype_out_epi_v1_BU3"

# Exact 19 epithelial states from the Wong et al. 2024 epithelial atlas / decoded RDS
EPI_STATES = [
    "Budtip progenitors",
    "Stromal-like cells 1",
    "Mature ciliated cells",
    "Tip cells",
    "Proliferating progenitors",
    "SOX2lowCFTR+ cells",
    "SOX2highCFTR+ cells",
    "PTEN+STAT3+ cells",
    "SCGB3A2+SFTPB+CFTR+ cells",
    "Ciliated precursor cells",
    "NKX2-1+SOX9+CFTR+ cells",
    "PNEC",
    "SCGB3A2+FOXJ1+ cells",
    "Stromal-like cells 2",
    "SMG basal cells",
    "Club cells",
    "NRGN+ cells",
    "SMG secretory cells",
    "Basal cells",
]

REGION_LABEL = "whole_lung"
RNG = np.random.default_rng(0)


def to_csr(x):
    if sparse.issparse(x):
        return x.tocsr().astype(np.float32)
    return sparse.csr_matrix(np.asarray(x, dtype=np.float32))


def row_normalize_csr(x):
    norms = np.sqrt(np.asarray(x.multiply(x).sum(axis=1)).ravel()).astype(np.float32)
    norms[norms == 0] = 1.0
    return diags(1.0 / norms).dot(x).tocsr(), norms


def value_counts_fraction(df, col, order=None, out_name=None):
    out_name = out_name or col
    if df.empty:
        return pd.DataFrame(columns=[out_name, "fraction"])
    vc = df[col].value_counts(normalize=True, dropna=False)
    vc = vc.reset_index()
    vc.columns = [out_name, "fraction"]
    if order is not None:
        vc["__order"] = vc[out_name].map({k: i for i, k in enumerate(order)}).fillna(10**9)
        vc = vc.sort_values(["__order", "fraction"], ascending=[True, False]).drop(columns="__order")
    return vc


def mode_or_first(s):
    s = s.dropna().astype(str)
    if len(s) == 0:
        return None
    m = s.mode()
    return m.iloc[0] if len(m) else s.iloc[0]


def derive_stage_num(stage_fine):
    # stage_fine is like week_10
    return pd.to_numeric(pd.Series(stage_fine).astype(str).str.replace("week_", "", regex=False), errors="coerce")


def make_stage_coarse(stage_num_series):
    vals = pd.to_numeric(stage_num_series, errors="coerce")
    out = np.where(
        vals <= 13,
        "early_GW10_13",
        np.where(vals <= 16, "mid_GW14_16", "late_GW17_19"),
    )
    return pd.Series(out, index=getattr(stage_num_series, "index", None))


def main():
    outdir = Path(OUTDIR)
    outdir.mkdir(parents=True, exist_ok=True)

    # -------------------------
    # Load files
    # -------------------------
    ref = ad.read_h5ad(REFERENCE_H5AD, backed="r")
    qry = ad.read_h5ad(QUERY_H5AD)

    meta = pd.read_csv(REFERENCE_META, dtype=str)
    meta["cell_id"] = meta["cell_id"].astype(str)
    meta = meta.set_index("cell_id")

    ref_cells = pd.Index([str(x) for x in ref.obs_names], name="cell_id")
    meta = meta.reindex(ref_cells)
    missing_meta = int(meta["stage_fine"].isna().sum())
    if missing_meta > 0:
        raise ValueError(f"Metadata join failed for {missing_meta} reference cells")

    gate = pd.read_csv(WHOLELUNG_GATE_CSV)
    if "cell_id" not in gate.columns:
        raise ValueError("WHOLELUNG_GATE_CSV must contain a cell_id column")
    gate["cell_id"] = gate["cell_id"].astype(str)
    gate = gate.set_index("cell_id")
    qry_cells = pd.Index([str(x) for x in qry.obs_names], name="cell_id")
    gate = gate.reindex(qry_cells)
    missing_gate = int(gate["pred_state_coarse"].isna().sum())
    if missing_gate > 0:
        raise ValueError(f"Whole-lung gate join failed for {missing_gate} query cells")

    # -------------------------
    # Subset epithelial reference
    # -------------------------
    epi_ref_mask = (
        meta["state_coarse"].astype(str).eq("Epithelial")
        & meta["state_fine"].astype(str).isin(EPI_STATES)
        & meta["stage_fine"].notna()
    )
    epi_ref_idx = np.flatnonzero(epi_ref_mask.to_numpy())
    meta_epi = meta.iloc[epi_ref_idx].copy()

    if meta_epi.empty:
        raise ValueError("No epithelial reference cells found after subsetting")

    # Keep stage_coarse consistent even if the CSV already has it
    meta_epi["stage_num"] = derive_stage_num(meta_epi["stage_fine"])
    meta_epi["stage_coarse"] = make_stage_coarse(meta_epi["stage_num"])

    # -------------------------
    # Common genes
    # -------------------------
    ref_genes = pd.Index([str(x) for x in ref.var_names])
    qry_genes = pd.Index([str(x) for x in qry.var_names])
    common = ref_genes.intersection(qry_genes)
    ref_pos = ref_genes.get_indexer(common)
    qry_pos = qry_genes.get_indexer(common)

    # -------------------------
    # Build epithelial nodes
    # node = stage_fine x state_fine x region
    # -------------------------
    region = pd.Series([REGION_LABEL] * len(meta_epi), index=meta_epi.index)
    node_key = (
        meta_epi["stage_fine"].astype(str)
        + "||"
        + meta_epi["state_fine"].astype(str)
        + "||"
        + region.astype(str)
    )
    node_cat = pd.Categorical(node_key)
    node_codes = node_cat.codes.astype(np.int32)
    node_levels = pd.Index(node_cat.categories)

    node_meta = pd.DataFrame(
        {
            "node_key": node_levels,
            "stage_fine": [x.split("||", 2)[0] for x in node_levels],
            "state_fine": [x.split("||", 2)[1] for x in node_levels],
            "region": [x.split("||", 2)[2] for x in node_levels],
        }
    )
    tmp = pd.DataFrame(
        {
            "node_key": node_key.values,
            "stage_num": meta_epi["stage_num"].values,
            "stage_coarse": meta_epi["stage_coarse"].values,
            "state_coarse": meta_epi["state_coarse"].values,
        }
    )
    node_meta["stage_num"] = node_meta["node_key"].map(tmp.groupby("node_key")["stage_num"].median())
    node_meta["stage_coarse"] = node_meta["node_key"].map(tmp.groupby("node_key")["stage_coarse"].agg(mode_or_first))
    node_meta["state_coarse"] = node_meta["node_key"].map(tmp.groupby("node_key")["state_coarse"].agg(mode_or_first))

    # -------------------------
    # Compute epithelial centroids
    # -------------------------
    n_nodes = len(node_levels)
    n_genes = len(common)
    sum_mat = np.zeros((n_nodes, n_genes), dtype=np.float32)
    count_vec = np.zeros(n_nodes, dtype=np.int32)

    chunk = 2000
    for start in range(0, len(epi_ref_idx), chunk):
        end = min(start + chunk, len(epi_ref_idx))
        rows = epi_ref_idx[start:end]
        block = ref[rows, :].X
        block = to_csr(block)[:, ref_pos]
        codes = node_codes[start:end]
        for g in np.unique(codes):
            rr = np.flatnonzero(codes == g)
            count_vec[g] += len(rr)
            sum_mat[g] += np.asarray(block[rr].sum(axis=0)).ravel().astype(np.float32)

    centroids = sum_mat / np.maximum(count_vec[:, None], 1)
    centroids = centroids.astype(np.float32)
    centroid_norms = np.linalg.norm(centroids, axis=1).astype(np.float32)
    centroid_norms[centroid_norms == 0] = 1.0
    centroids_norm = centroids / centroid_norms[:, None]

    # -------------------------
    # Select query cells for epithelial remap
    # -------------------------
    gate = gate.copy()
    gate["lineage_gate_state_coarse"] = gate["pred_state_coarse"].astype(str)
    gate["wholelung_off_target_candidate"] = gate.get("off_target_candidate", False)
    gate["wholelung_top1_score"] = pd.to_numeric(gate.get("top1_score", np.nan), errors="coerce")
    gate["wholelung_margin"] = pd.to_numeric(gate.get("margin", np.nan), errors="coerce")

    eligible_mask = gate["lineage_gate_state_coarse"].eq("Epithelial").to_numpy()
    eligible_idx = np.flatnonzero(eligible_mask)

    qX = to_csr(qry[:, qry_pos].X)
    q_data = qX.data if qX.nnz else np.array([0], dtype=np.float32)
    integer_like_frac = float(np.mean(np.isclose(q_data, np.round(q_data)))) if q_data.size else 1.0
    max_nonzero = float(q_data.max()) if q_data.size else 0.0
    query_preproc = "as_is"
    if integer_like_frac > 0.95 and max_nonzero > 20:
        lib = np.asarray(qX.sum(axis=1)).ravel().astype(np.float32)
        scale = (1e4 / np.maximum(lib, 1.0)).astype(np.float32)
        qX = diags(scale).dot(qX).tocsr()
        qX.data = np.log1p(qX.data)
        query_preproc = "normalize_total_1e4_then_log1p"

    # -------------------------
    # Epithelial self-projection thresholds
    # -------------------------
    sample_n = min(5000, len(epi_ref_idx))
    sample_rows = np.sort(RNG.choice(epi_ref_idx, size=sample_n, replace=False))
    rX = to_csr(ref[sample_rows, :].X)[:, ref_pos]
    rXn, _ = row_normalize_csr(rX)
    r_scores = np.asarray(rXn.dot(centroids_norm.T), dtype=np.float32)
    r_top1_idx = r_scores.argmax(axis=1)
    r_top1 = r_scores[np.arange(sample_n), r_top1_idx]
    r_tmp = r_scores.copy()
    r_tmp[np.arange(sample_n), r_top1_idx] = -np.inf
    r_top2 = r_tmp.max(axis=1)
    r_margin = r_top1 - r_top2
    epi_score_thr = float(np.percentile(r_top1, 5))
    epi_margin_thr = float(np.percentile(r_margin, 5))

    # -------------------------
    # Remap eligible epithelial query cells
    # -------------------------
    epi_pred = pd.DataFrame(index=qry_cells)

    epi_pred["epi_input_eligible"] = pd.Series(eligible_mask, index=qry_cells, dtype="bool")
    epi_pred["lineage_off_target"] = pd.Series(~eligible_mask, index=qry_cells, dtype="bool")

    obj_cols = [
        "epi_top1_node_key",
        "epi_top2_node_key",
        "epi_stage_fine",
        "epi_stage_coarse",
        "epi_state_fine",
        "epi_state_coarse",
        "epi_region",
    ]
    for c in obj_cols:
        epi_pred[c] = pd.Series(pd.NA, index=epi_pred.index, dtype="object")

    float_cols = [
        "epi_top1_score",
        "epi_top2_score",
        "epi_margin",
        "epi_stage_num",
    ]
    for c in float_cols:
        epi_pred[c] = pd.Series(np.nan, index=epi_pred.index, dtype="float64")

    epi_pred["epi_ambiguous"] = pd.Series(False, index=epi_pred.index, dtype="bool")

    if len(eligible_idx) > 0:
        qX_epi = qX[eligible_idx]
        qXn, _ = row_normalize_csr(qX_epi)
        scores = np.asarray(qXn.dot(centroids_norm.T), dtype=np.float32)
        top1_idx = scores.argmax(axis=1)
        top1_score = scores[np.arange(scores.shape[0]), top1_idx]
        s2 = scores.copy()
        s2[np.arange(scores.shape[0]), top1_idx] = -np.inf
        top2_idx = s2.argmax(axis=1)
        top2_score = scores[np.arange(scores.shape[0]), top2_idx]
        margin = top1_score - top2_score

        pred1 = node_meta.iloc[top1_idx].reset_index(drop=True)
        pred2 = node_meta.iloc[top2_idx].reset_index(drop=True)

        epi_ambiguous = (top1_score < epi_score_thr) | (margin < epi_margin_thr)

        eligible_cells = qry_cells[eligible_idx]
    
        epi_pred.loc[eligible_cells, "epi_top1_node_key"] = pred1["node_key"].values
        epi_pred.loc[eligible_cells, "epi_top2_node_key"] = pred2["node_key"].values
        epi_pred.loc[eligible_cells, "epi_top1_score"] = top1_score
        epi_pred.loc[eligible_cells, "epi_top2_score"] = top2_score
        epi_pred.loc[eligible_cells, "epi_margin"] = margin
        epi_pred.loc[eligible_cells, "epi_stage_fine"] = pred1["stage_fine"].values
        epi_pred.loc[eligible_cells, "epi_stage_coarse"] = pred1["stage_coarse"].values
        epi_pred.loc[eligible_cells, "epi_stage_num"] = pred1["stage_num"].values
        epi_pred.loc[eligible_cells, "epi_state_fine"] = pred1["state_fine"].values
        epi_pred.loc[eligible_cells, "epi_state_coarse"] = pred1["state_coarse"].values
        epi_pred.loc[eligible_cells, "epi_region"] = pred1["region"].values
        epi_pred.loc[eligible_cells, "epi_ambiguous"] = epi_ambiguous

    # -------------------------
    # Merge with whole-lung gate
    # -------------------------
    merged = pd.DataFrame(index=qry_cells)
    merged.index.name = "cell_id"
    merged = merged.join(gate[[
        "lineage_gate_state_coarse",
        "wholelung_off_target_candidate",
        "wholelung_top1_score",
        "wholelung_margin",
    ]], how="left")
    merged = merged.join(epi_pred, how="left")
    merged = merged.reset_index()

    # -------------------------
    # Write outputs
    # -------------------------
    merged.to_csv(outdir / "BU3_lineage_gate_plus_epi_remap.csv", index=False)
    node_meta.assign(n_cells=count_vec).to_csv(outdir / "reference_nodes_epi_v1.csv", index=False)

    epi_cells = merged[merged["epi_input_eligible"] == True].copy()
    epi_cells.to_csv(outdir / "BU3_epi_cell_projection.csv", index=False)

    stage_order = [f"week_{x}" for x in [10, 11, 12, 13, 14, 15, 16, 18, 19]]
    stage_coarse_order = ["early_GW10_13", "mid_GW14_16", "late_GW17_19"]
    coarse_order = ["Epithelial", "Stromal", "Endothelial", "Immune", "Schwann"]

    value_counts_fraction(epi_cells, "epi_stage_fine", order=stage_order, out_name="stage_fine").to_csv(
        outdir / "BU3_epi_stage_fine.csv", index=False
    )
    value_counts_fraction(epi_cells, "epi_stage_coarse", order=stage_coarse_order, out_name="stage_coarse").to_csv(
        outdir / "BU3_epi_stage_coarse.csv", index=False
    )
    value_counts_fraction(epi_cells, "epi_state_fine", out_name="state_fine").to_csv(
        outdir / "BU3_epi_state_fine.csv", index=False
    )
    value_counts_fraction(epi_cells, "epi_state_coarse", order=coarse_order, out_name="state_coarse").to_csv(
        outdir / "BU3_epi_state_coarse.csv", index=False
    )

    ambiguous = epi_cells[epi_cells["epi_ambiguous"] == True].copy()
    value_counts_fraction(ambiguous, "epi_state_fine", out_name="state_fine").to_csv(
        outdir / "BU3_epi_ambiguous_state_fine.csv", index=False
    )
    value_counts_fraction(ambiguous, "epi_stage_fine", order=stage_order, out_name="stage_fine").to_csv(
        outdir / "BU3_epi_ambiguous_stage_fine.csv", index=False
    )

    lineage_off = merged[merged["lineage_off_target"] == True].copy()
    value_counts_fraction(lineage_off, "lineage_gate_state_coarse", order=coarse_order, out_name="state_coarse").to_csv(
        outdir / "BU3_lineage_off_target_state_coarse.csv", index=False
    )

    summary = {
        "reference_file": REFERENCE_H5AD,
        "reference_metadata_file": REFERENCE_META,
        "wholelung_gate_file": WHOLELUNG_GATE_CSV,
        "query_file": QUERY_H5AD,
        "n_ref_epi_cells": int(len(epi_ref_idx)),
        "n_query_cells": int(qry.n_obs),
        "n_query_epi_eligible": int(eligible_mask.sum()),
        "n_common_genes": int(len(common)),
        "n_epi_nodes": int(len(node_meta)),
        "query_preprocessing": query_preproc,
        "epi_reference_top1_score_p5": epi_score_thr,
        "epi_reference_margin_p5": epi_margin_thr,
        "lineage_off_target_fraction": float((merged["lineage_off_target"] == True).mean()),
        "epi_ambiguous_fraction_within_epi_eligible": float((epi_cells["epi_ambiguous"] == True).mean()) if len(epi_cells) else None,
        "epi_ambiguous_fraction_of_all_cells": float(((merged["epi_input_eligible"] == True) & (merged["epi_ambiguous"] == True)).mean()),
    }

    if len(epi_cells):
        for col, key in [
            ("epi_stage_fine", "top_epi_stage_fine"),
            ("epi_stage_coarse", "top_epi_stage_coarse"),
            ("epi_state_fine", "top_epi_state_fine"),
        ]:
            vc = epi_cells[col].value_counts(normalize=True)
            if len(vc):
                summary[key] = vc.index[0]
                summary[key + "_fraction"] = float(vc.iloc[0])
        summary["epi_alignment_mean_top1"] = float(pd.to_numeric(epi_cells["epi_top1_score"]).mean())
        summary["epi_alignment_median_top1"] = float(pd.to_numeric(epi_cells["epi_top1_score"]).median())
        summary["epi_alignment_mean_margin"] = float(pd.to_numeric(epi_cells["epi_margin"]).mean())

    with open(outdir / "BU3_epi_summary_v1.json", "w") as f:
        json.dump(summary, f, indent=2)

    ref.file.close()


if __name__ == "__main__":
    main()
