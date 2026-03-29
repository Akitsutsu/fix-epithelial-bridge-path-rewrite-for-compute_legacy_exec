library(Seurat)
library(SeuratDisk)

dir.create("converted", recursive = TRUE, showWarnings = FALSE)

# 参照データ
ref <- readRDS("GSE264407_full_fetal_lung_dataset_04142025.rds")
SaveH5Seurat(ref, filename = "converted/reference_full.h5Seurat", overwrite = TRUE)
Convert("converted/reference_full.h5Seurat",
        dest = "h5ad",
        overwrite = TRUE)

# query データ
qry <- readRDS("GSE266789_hPSC_fetal_lung_organoids.rds")
SaveH5Seurat(qry, filename = "converted/query_organoid_01.h5Seurat", overwrite = TRUE)
Convert("converted/query_organoid_01.h5Seurat",
        dest = "h5ad",
        overwrite = TRUE)
