"""
Convert GSE308817 per-GSM SeekSoulTools mtx triplets to H5AD.

Source: queries/raw/gse308817/GSM{id}_{alo}_{barcodes,features,matrix}.*
Output: queries/converted/gse308817/GSE308817_{alo}.h5ad

Each output H5AD contains:
  - X: raw integer counts (CSR sparse)
  - raw: frozen copy of X before any future subsetting
  - layers["counts"]: explicit raw-count layer
  - var: gene_ids, feature_types
  - obs: query_dataset_id, local_query_sample_id, source_sample_name,
         source_type, donor_id, species

Note: Library prep is SeekOne (SeekGene), not 10x Chromium. Processing
is SeekSoulTools v1.2.2, not CellRanger. Output format is standard
10x-like sparse matrix triplets, confirmed compatible with reference.
"""

import anndata as ad
import scipy.io as sio
import pandas as pd
import gzip
import os

RAW_DIR = "queries/raw/gse308817"
OUT_DIR = "queries/converted/gse308817"

SAMPLES = [
    {
        "gsm": "GSM9253578",
        "alo": "ALOp3",
        "sample_id": "GSE308817_ALOp3",
        "sample_name": "ALOp3",
        "source_type": "hESC-derived alveolar organoid (H9, passage 3)",
    },
    {
        "gsm": "GSM9253579",
        "alo": "ALOp7",
        "sample_id": "GSE308817_ALOp7",
        "sample_name": "ALOp7",
        "source_type": "hESC-derived alveolar organoid (H9, passage 7)",
    },
    {
        "gsm": "GSM9253580",
        "alo": "ALOp20",
        "sample_id": "GSE308817_ALOp20",
        "sample_name": "ALOp20",
        "source_type": "hESC-derived alveolar organoid (H9, passage 20)",
    },
]


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    for s in SAMPLES:
        prefix = f"{s['gsm']}_{s['alo']}"

        with gzip.open(os.path.join(RAW_DIR, f"{prefix}_barcodes.tsv.gz"), "rt") as f:
            barcodes = [line.strip() for line in f]

        with gzip.open(os.path.join(RAW_DIR, f"{prefix}_features.tsv.gz"), "rt") as f:
            features_lines = [line.strip().split("\t") for line in f]
        gene_ids = [l[0] for l in features_lines]
        gene_names = [l[1] for l in features_lines]
        feature_types = [l[2] if len(l) > 2 else "Gene Expression" for l in features_lines]

        mat = sio.mmread(os.path.join(RAW_DIR, f"{prefix}_matrix.mtx.gz")).T.tocsr()

        obs = pd.DataFrame(index=barcodes)
        var = pd.DataFrame({"gene_ids": gene_ids, "feature_types": feature_types}, index=gene_names)
        var.index.name = None

        adata = ad.AnnData(X=mat, obs=obs, var=var)
        adata.var_names_make_unique()

        adata.obs["query_dataset_id"] = "external_gse308817"
        adata.obs["local_query_sample_id"] = s["sample_id"]
        adata.obs["source_sample_name"] = s["sample_name"]
        adata.obs["source_type"] = s["source_type"]
        adata.obs["donor_id"] = "H9"
        adata.obs["species"] = "Homo sapiens"

        adata.raw = adata
        adata.layers["counts"] = adata.X.copy()

        out_path = os.path.join(OUT_DIR, f"{s['sample_id']}.h5ad")
        adata.write_h5ad(out_path)
        print(f"{s['sample_id']}: {adata.shape} -> {out_path}")


if __name__ == "__main__":
    main()
