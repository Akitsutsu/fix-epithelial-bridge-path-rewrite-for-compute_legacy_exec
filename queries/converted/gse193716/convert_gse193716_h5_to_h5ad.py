"""
Convert GSE193716 CellRanger filtered H5 files to H5AD.

Source: queries/raw/gse193716/GSM58191{29..35}_*.filtered_feature_bc_matrix.h5
Output: queries/converted/gse193716/GSM58191{29..35}_*.h5ad

Dataset: Alysandratos et al., JCI Insight 2023 (PMID 36454643)
Lab: Kotton / Boston University
CellRanger reference: GRCh38_tdtomato_10X (CellRanger v3)
Reference overlap: 26,975/30,852 (87.4%) — gap is lncRNA annotation drift

Each output H5AD contains:
  - X: raw integer counts (CSR sparse, float32 storage from scanpy)
  - raw: frozen copy of X before any future subsetting
  - layers["counts"]: explicit raw-count layer
  - var: gene_ids, feature_types, genome (from CellRanger)
  - obs: query_dataset_id, local_query_sample_id, source_sample_name,
         source_type, donor_id, species

Note: 32 duplicate gene symbols resolved via var_names_make_unique().
TdTomato reporter gene retained (useful for SPC2-ST-B2 lineage QC).
"""

import scanpy as sc
import os

RAW_DIR = "queries/raw/gse193716"
OUT_DIR = "queries/converted/gse193716"

SAMPLES = [
    {
        "h5": "GSM5819131_CG7.filtered_feature_bc_matrix.h5",
        "sample_id": "GSM5819131_primary_preculture_PL2",
        "sample_name": "CG7",
        "source_type": "primary adult AEC2 (freshly isolated)",
        "donor_id": "PL2",
    },
    {
        "h5": "GSM5819132_CG8.filtered_feature_bc_matrix.h5",
        "sample_id": "GSM5819132_primary_preculture_PL1",
        "sample_name": "CG8",
        "source_type": "primary adult AEC2 (freshly isolated)",
        "donor_id": "PL1",
    },
    {
        "h5": "GSM5819129_CG5.filtered_feature_bc_matrix.h5",
        "sample_id": "GSM5819129_primary_cultured_PL2",
        "sample_name": "CG5",
        "source_type": "primary adult AEC2 (cultured with MRC5 fibroblasts)",
        "donor_id": "PL2",
    },
    {
        "h5": "GSM5819130_CG6.filtered_feature_bc_matrix.h5",
        "sample_id": "GSM5819130_primary_cultured_PL1",
        "sample_name": "CG6",
        "source_type": "primary adult AEC2 (cultured with MRC5 fibroblasts)",
        "donor_id": "PL1",
    },
    {
        "h5": "GSM5819133_CG12.filtered_feature_bc_matrix.h5",
        "sample_id": "GSM5819133_iAEC2_3D",
        "sample_name": "CG12",
        "source_type": "iPSC-derived iAEC2 (SPC2-ST-B2, 3D feeder-free)",
        "donor_id": "SPC2-ST-B2",
    },
    {
        "h5": "GSM5819134_CG13.filtered_feature_bc_matrix.h5",
        "sample_id": "GSM5819134_iAEC2_3D_insert",
        "sample_name": "CG13",
        "source_type": "iPSC-derived iAEC2 (SPC2-ST-B2, 3D/insert)",
        "donor_id": "SPC2-ST-B2",
    },
    {
        "h5": "GSM5819135_CG14.filtered_feature_bc_matrix.h5",
        "sample_id": "GSM5819135_iAEC2_MRC5_insert",
        "sample_name": "CG14",
        "source_type": "iPSC-derived iAEC2 (SPC2-ST-B2, +MRC5/insert)",
        "donor_id": "SPC2-ST-B2",
    },
]


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    for s in SAMPLES:
        h5_path = os.path.join(RAW_DIR, s["h5"])
        out_path = os.path.join(OUT_DIR, f"{s['sample_id']}.h5ad")

        adata = sc.read_10x_h5(h5_path)
        adata.var_names_make_unique()

        adata.obs["query_dataset_id"] = "external_gse193716"
        adata.obs["local_query_sample_id"] = s["sample_id"]
        adata.obs["source_sample_name"] = s["sample_name"]
        adata.obs["source_type"] = s["source_type"]
        adata.obs["donor_id"] = s["donor_id"]
        adata.obs["species"] = "Homo sapiens"

        # Preserve raw counts in .raw and .layers["counts"]
        adata.raw = adata
        adata.layers["counts"] = adata.X.copy()

        adata.write_h5ad(out_path)
        print(f"{s['sample_id']}: {adata.shape} -> {out_path}")


if __name__ == "__main__":
    main()
