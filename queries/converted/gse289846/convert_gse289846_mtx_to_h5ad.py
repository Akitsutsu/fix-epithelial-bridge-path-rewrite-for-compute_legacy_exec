"""
Convert GSE289846 condition-level CellRanger mtx triplets to H5AD.

Source: queries/raw/gse289846/GSE289846_{condition}_{barcodes,features,matrix}.*
Output: queries/converted/gse289846/GSE289846_{condition}.h5ad

Each output H5AD contains:
  - X: raw integer counts (CSR sparse)
  - raw: frozen copy of X before any future subsetting
  - layers["counts"]: explicit raw-count layer
  - var: gene_ids, feature_types
  - obs: query_dataset_id, local_query_sample_id, source_sample_name,
         source_type, donor_id, species

Note: Each condition-level matrix merges 2 biological replicates.
Replicate provenance is tracked in the sample sheet, not in the H5AD.
"""

import anndata as ad
import scipy.io as sio
import pandas as pd
import numpy as np
import gzip
import os

RAW_DIR = "queries/raw/gse289846"
OUT_DIR = "queries/converted/gse289846"

CONDITIONS = [
    {
        "prefix": "GSE289846_3i_Day7",
        "sample_id": "GSE289846_3i_Day7",
        "sample_name": "3i_Day7",
        "source_type": "iPSC-derived alveolar epithelial organoid (DCIK+3i Day7)",
    },
    {
        "prefix": "GSE289846_3i_LATS_Day14",
        "sample_id": "GSE289846_3i_LATS_Day14",
        "sample_name": "3i_LATS_Day14",
        "source_type": "iPSC-derived alveolar epithelial organoid (DCI+LATS-IN-1 Day14)",
    },
    {
        "prefix": "GSE289846_3i_PAL_Day14",
        "sample_id": "GSE289846_3i_PAL_Day14",
        "sample_name": "3i_PAL_Day14",
        "source_type": "iPSC-derived alveolar epithelial organoid (PAL transitional Day14)",
    },
]


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    for c in CONDITIONS:
        prefix = c["prefix"]
        barcodes_path = os.path.join(RAW_DIR, f"{prefix}_barcodes.tsv.gz")
        features_path = os.path.join(RAW_DIR, f"{prefix}_features.tsv.gz")
        matrix_path = os.path.join(RAW_DIR, f"{prefix}_matrix.mtx.gz")

        with gzip.open(barcodes_path, "rt") as f:
            barcodes = [line.strip() for line in f]

        with gzip.open(features_path, "rt") as f:
            features_lines = [line.strip().split("\t") for line in f]
        gene_ids = [l[0] for l in features_lines]
        gene_names = [l[1] for l in features_lines]
        feature_types = [l[2] if len(l) > 2 else "Gene Expression" for l in features_lines]

        mat = sio.mmread(matrix_path).T.tocsr()

        obs = pd.DataFrame(index=barcodes)
        var = pd.DataFrame({"gene_ids": gene_ids, "feature_types": feature_types}, index=gene_names)
        var.index.name = None

        adata = ad.AnnData(X=mat, obs=obs, var=var)
        adata.var_names_make_unique()

        adata.obs["query_dataset_id"] = "external_gse289846"
        adata.obs["local_query_sample_id"] = c["sample_id"]
        adata.obs["source_sample_name"] = c["sample_name"]
        adata.obs["source_type"] = c["source_type"]
        adata.obs["donor_id"] = "B2-3"
        adata.obs["species"] = "Homo sapiens"

        adata.raw = adata
        adata.layers["counts"] = adata.X.copy()

        out_path = os.path.join(OUT_DIR, f"{c['sample_id']}.h5ad")
        adata.write_h5ad(out_path)
        print(f"{c['sample_id']}: {adata.shape} -> {out_path}")


if __name__ == "__main__":
    main()
