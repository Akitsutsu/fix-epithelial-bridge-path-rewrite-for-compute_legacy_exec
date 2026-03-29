import json
from pathlib import Path

import anndata as ad
import numpy as np
import pandas as pd
from scipy import sparse
from scipy.sparse import diags

rng = np.random.default_rng(0)
outdir = Path("prototype_out_v1")
outdir.mkdir(exist_ok=True)

def to_csr(x):
    if sparse.issparse(x):
        return x.tocsr().astype(np.float32)
    return sparse.csr_matrix(np.asarray(x, dtype=np.float32))

def row_normalize_csr(x):
    norms = np.sqrt(np.asarray(x.multiply(x).sum(axis=1)).ravel()).astype(np.float32)
    norms[norms == 0] = 1.0
    return diags(1.0 / norms).dot(x).tocsr(), norms

def mode_or_first(s):
    s = s.dropna().astype(str)
    if len(s) == 0:
        return None
    m = s.mode()
    return m.iloc[0] if len(m) else s.iloc[0]

def write_fraction_csv(df, col, path, out_name):
    vc = (
        df[col].value_counts(normalize=True, dropna=False)
        .rename("fraction")
        .reset_index()
        .rename(columns={"index": out_name, col: out_name})
    )
    vc.to_csv(path, index=False)

ref = ad.read_h5ad("converted/reference_RNA.h5ad", backed="r")
qry = ad.read_h5ad("converted/query_BU3_clean.h5ad")

meta = pd.read_csv("converted/reference_metadata_v1.csv", dtype=str)
meta["cell_id"] = meta["cell_id"].astype(str)
meta = meta.set_index("cell_id")

ref_cells = pd.Index([str(x) for x in ref.obs_names], name="cell_id")
meta = meta.reindex(ref_cells)

missing_meta = int(meta["stage_fine"].isna().sum())
print("missing metadata rows after reindex:", missing_meta)
if missing_meta > 0:
    raise ValueError(f"Metadata join failed for {missing_meta} reference cells")

meta["stage_num"] = pd.to_numeric(meta["stage_num"], errors="coerce")

ref_genes = pd.Index([str(x) for x in ref.var_names])
qry_genes = pd.Index([str(x) for x in qry.var_names])
common = ref_genes.intersection(qry_genes)
ref_pos = ref_genes.get_indexer(common)
qry_pos = qry_genes.get_indexer(common)
print("n_common_genes:", len(common))

valid_mask = (
    meta["stage_fine"].notna()
    & meta["stage_coarse"].notna()
    & meta["state_fine"].notna()
    & meta["state_coarse"].notna()
)
valid_idx = np.flatnonzero(valid_mask.to_numpy())
meta_valid = meta.iloc[valid_idx].reset_index(drop=True)

region = pd.Series(["whole_lung"] * len(meta_valid), dtype="object")
node_key = (
    meta_valid["stage_fine"].astype(str) + "||"
    + meta_valid["state_fine"].astype(str) + "||"
    + region.astype(str)
)
node_cat = pd.Categorical(node_key)
node_codes = node_cat.codes.astype(np.int32)
node_levels = pd.Index(node_cat.categories)

print("n_reference_cells_valid:", len(valid_idx))
print("n_nodes:", len(node_levels))

node_meta = pd.DataFrame({
    "node_key": node_levels,
    "stage_fine": [x.split("||", 2)[0] for x in node_levels],
    "state_fine": [x.split("||", 2)[1] for x in node_levels],
    "region": [x.split("||", 2)[2] for x in node_levels],
})

tmp = pd.DataFrame({
    "node_key": node_key.values,
    "stage_coarse": meta_valid["stage_coarse"].values,
    "state_coarse": meta_valid["state_coarse"].values,
    "group_internal": meta_valid["group_internal"].values,
    "stage_num": meta_valid["stage_num"].values,
})

for col in ["stage_coarse", "state_coarse", "group_internal"]:
    mapper = tmp.groupby("node_key")[col].agg(mode_or_first)
    node_meta[col] = node_meta["node_key"].map(mapper)

stage_num_map = tmp.groupby("node_key")["stage_num"].median()
node_meta["stage_num"] = node_meta["node_key"].map(stage_num_map)

n_nodes = len(node_levels)
n_genes = len(common)
sum_mat = np.zeros((n_nodes, n_genes), dtype=np.float32)
count_vec = np.zeros(n_nodes, dtype=np.int32)

chunk = 2000
for start in range(0, len(valid_idx), chunk):
    end = min(start + chunk, len(valid_idx))
    rows = valid_idx[start:end]
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

qX = to_csr(qry[:, qry_pos].X)
q_data = qX.data if qX.nnz else np.array([0], dtype=np.float32)
integer_like_frac = float(np.mean(np.isclose(q_data, np.round(q_data))))
max_nonzero = float(q_data.max()) if q_data.size else 0.0

query_preproc = "as_is"
if integer_like_frac > 0.95 and max_nonzero > 20:
    lib = np.asarray(qX.sum(axis=1)).ravel().astype(np.float32)
    scale = (1e4 / np.maximum(lib, 1.0)).astype(np.float32)
    qX = diags(scale).dot(qX).tocsr()
    qX.data = np.log1p(qX.data)
    query_preproc = "normalize_total_1e4_then_log1p"

qXn, _ = row_normalize_csr(qX)
scores = np.asarray(qXn.dot(centroids_norm.T), dtype=np.float32)

top1_idx = scores.argmax(axis=1)
top1_score = scores[np.arange(scores.shape[0]), top1_idx]

scores_tmp = scores.copy()
scores_tmp[np.arange(scores.shape[0]), top1_idx] = -np.inf
top2_idx = scores_tmp.argmax(axis=1)
top2_score = scores[np.arange(scores.shape[0]), top2_idx]
margin = top1_score - top2_score

pred1 = node_meta.iloc[top1_idx].reset_index(drop=True)
pred2 = node_meta.iloc[top2_idx].reset_index(drop=True)

sample_n = min(5000, len(valid_idx))
sample_rows = np.sort(rng.choice(valid_idx, size=sample_n, replace=False))
rX = to_csr(ref[sample_rows, :].X)[:, ref_pos]
rXn, _ = row_normalize_csr(rX)
r_scores = np.asarray(rXn.dot(centroids_norm.T), dtype=np.float32)

r_top1_idx = r_scores.argmax(axis=1)
r_top1 = r_scores[np.arange(sample_n), r_top1_idx]
r_tmp = r_scores.copy()
r_tmp[np.arange(sample_n), r_top1_idx] = -np.inf
r_top2 = r_tmp.max(axis=1)
r_margin = r_top1 - r_top2

score_thr = float(np.percentile(r_top1, 5))
margin_thr = float(np.percentile(r_margin, 5))

cell_df = pd.DataFrame({
    "cell_id": [str(x) for x in qry.obs_names],
    "pred_stage_fine": pred1["stage_fine"].values,
    "pred_stage_coarse": pred1["stage_coarse"].values,
    "pred_stage_num": pred1["stage_num"].values,
    "pred_state_fine": pred1["state_fine"].values,
    "pred_state_coarse": pred1["state_coarse"].values,
    "pred_region": pred1["region"].values,
    "pred_group_internal": pred1["group_internal"].values,
    "top1_node_key": pred1["node_key"].values,
    "top1_score": top1_score,
    "top2_node_key": pred2["node_key"].values,
    "top2_score": top2_score,
    "margin": margin,
})
cell_df["off_target_candidate"] = (
    (cell_df["top1_score"] < score_thr) |
    (cell_df["margin"] < margin_thr)
)

summary = {
    "reference_file": "converted/reference_RNA.h5ad",
    "reference_metadata_file": "converted/reference_metadata_v1.csv",
    "query_file": "converted/query_BU3_clean.h5ad",
    "n_ref_cells": int(ref.n_obs),
    "n_query_cells": int(qry.n_obs),
    "n_common_genes": int(len(common)),
    "n_nodes": int(n_nodes),
    "query_preprocessing": query_preproc,
    "alignment_mean_top1": float(cell_df["top1_score"].mean()),
    "alignment_median_top1": float(cell_df["top1_score"].median()),
    "alignment_mean_margin": float(cell_df["margin"].mean()),
    "reference_top1_score_p5": score_thr,
    "reference_margin_p5": margin_thr,
    "off_target_fraction": float(cell_df["off_target_candidate"].mean()),
}

for col, key in [
    ("pred_stage_fine", "top_stage_fine"),
    ("pred_stage_coarse", "top_stage_coarse"),
    ("pred_state_coarse", "top_state_coarse"),
    ("pred_state_fine", "top_state_fine"),
]:
    vc = cell_df[col].value_counts(normalize=True)
    if len(vc) > 0:
        summary[key] = vc.index[0]
        summary[key + "_fraction"] = float(vc.iloc[0])

cell_df.to_csv(outdir / "BU3_cell_projection_v1.csv", index=False)
node_meta.assign(n_cells=count_vec).to_csv(outdir / "reference_nodes_v1.csv", index=False)

write_fraction_csv(cell_df, "pred_stage_fine", outdir / "BU3_stage_fine.csv", "stage_fine")
write_fraction_csv(cell_df, "pred_stage_coarse", outdir / "BU3_stage_coarse.csv", "stage_coarse")
write_fraction_csv(cell_df, "pred_state_coarse", outdir / "BU3_state_coarse.csv", "state_coarse")
write_fraction_csv(cell_df, "pred_state_fine", outdir / "BU3_state_fine.csv", "state_fine")

off_df = cell_df.loc[cell_df["off_target_candidate"]].copy()
write_fraction_csv(off_df, "pred_state_coarse", outdir / "BU3_off_target_state_coarse.csv", "state_coarse")
write_fraction_csv(off_df, "pred_state_fine", outdir / "BU3_off_target_state_fine.csv", "state_fine")

with open(outdir / "BU3_summary_v1.json", "w") as f:
    json.dump(summary, f, indent=2)

print(json.dumps(summary, indent=2))
