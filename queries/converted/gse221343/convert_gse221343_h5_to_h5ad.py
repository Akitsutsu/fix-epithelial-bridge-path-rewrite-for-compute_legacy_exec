"""
Convert GSE221343 CellRanger filtered H5 files to H5AD.

Source: queries/raw/gse221343/GSM68588{54,55,56}_*.h5
Output: queries/converted/gse221343/GSM68588{54,55,56}_*.h5ad

Each output H5AD contains:
  - X: raw integer counts (CSR sparse, float32 storage from scanpy)
  - raw: frozen copy of X before any future subsetting
  - layers["counts"]: explicit raw-count layer
  - var: gene_ids, feature_types, genome (from CellRanger)
  - obs: query_dataset_id, local_query_sample_id, source_sample_name,
         source_type, donor_id, species
"""

import scanpy as sc
import os

RAW_DIR = "queries/raw/gse221343"
OUT_DIR = "queries/converted/gse221343"

SAMPLES = [
    {
        "h5": "GSM6858854_CK+DCI.h5",
        "sample_id": "GSM6858854_CK_DCI",
        "sample_name": "CK+DCI",
        "source_type": "iPSC-derived iAT2 organoid (control CKDCI medium)",
    },
    {
        "h5": "GSM6858855_YAP5SA_in_CK+DCI.h5",
        "sample_id": "GSM6858855_YAP5SA_CK_DCI",
        "sample_name": "YAP5SA in CK+DCI",
        "source_type": "iPSC-derived iAT2 organoid (YAP5SA lentivirus + CKDCI)",
    },
    {
        "h5": "GSM6858856_L+DCI.h5",
        "sample_id": "GSM6858856_L_DCI",
        "sample_name": "L+DCI",
        "source_type": "iPSC-derived iAT1 organoid (LDCI differentiation medium)",
    },
]


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    for s in SAMPLES:
        h5_path = os.path.join(RAW_DIR, s["h5"])
        out_path = os.path.join(OUT_DIR, f"{s['sample_id']}.h5ad")

        adata = sc.read_10x_h5(h5_path)
        adata.var_names_make_unique()

        adata.obs["query_dataset_id"] = "external_gse221343"
        adata.obs["local_query_sample_id"] = s["sample_id"]
        adata.obs["source_sample_name"] = s["sample_name"]
        adata.obs["source_type"] = s["source_type"]
        adata.obs["donor_id"] = "SPC2-ST-B2"
        adata.obs["species"] = "Homo sapiens"

        # Preserve raw counts in .raw and .layers["counts"]
        adata.raw = adata
        adata.layers["counts"] = adata.X.copy()

        adata.write_h5ad(out_path)
        print(f"{s['sample_id']}: {adata.shape} -> {out_path}")


if __name__ == "__main__":
    main()
