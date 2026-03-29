#!/usr/bin/env Rscript
# build_frozen_reference_v1.R
#
# Canonical rebuild of the frozen fetal lung reference from the upstream RDS.
# Produces RNA-only h5Seurat and h5ad into a TEMPORARY output directory.
# Does NOT overwrite the operational frozen pair under converted/.
#
# Prerequisites:
#   R >= 4.1, Seurat >= 5.0, SeuratDisk (remotes::install_github("mojaveazure/seurat-disk"))
#
# Usage:
#   Rscript build_frozen_reference_v1.R [output_dir]
#   Default output_dir: rebuild_audit_v1/

args <- commandArgs(trailingOnly = TRUE)
outdir <- if (length(args) >= 1) args[1] else "rebuild_audit_v1"
dir.create(outdir, recursive = TRUE, showWarnings = FALSE)

cat("=== build_frozen_reference_v1.R ===\n")
cat("Output directory:", outdir, "\n")

library(Seurat)
library(SeuratDisk)

cat("Seurat version:", as.character(packageVersion("Seurat")), "\n")
cat("SeuratDisk version:", as.character(packageVersion("SeuratDisk")), "\n")

# --- Step 1: Load the upstream RDS ---
rds_path <- "full_fetal_lung_dataset.rds"
if (!file.exists(rds_path)) {
  rds_path <- "GSE264407_full_fetal_lung_dataset_04142025.rds"
}
if (!file.exists(rds_path)) {
  stop("Source RDS not found. Expected full_fetal_lung_dataset.rds or GSE264407_*.rds")
}
cat("Loading RDS:", rds_path, "\n")
ref <- readRDS(rds_path)
cat("Loaded. Cells:", ncol(ref), " Assays:", paste(Assays(ref), collapse=", "), "\n")

# --- Step 2: Set RNA as default and export ---
DefaultAssay(ref) <- "RNA"
cat("DefaultAssay set to RNA\n")
cat("RNA features:", nrow(ref[["RNA"]]), "\n")

h5seurat_path <- file.path(outdir, "reference_RNA.h5Seurat")
h5ad_path     <- file.path(outdir, "reference_RNA.h5ad")

cat("Saving h5Seurat:", h5seurat_path, "\n")
SaveH5Seurat(ref, filename = h5seurat_path, overwrite = TRUE)

cat("Converting to h5ad:", h5ad_path, "\n")
Convert(h5seurat_path, dest = "h5ad", overwrite = TRUE)

cat("Done. Files written:\n")
cat("  ", h5seurat_path, "\n")
cat("  ", h5ad_path, "\n")

# --- Record versions ---
versions <- data.frame(
  package = c("R", "Seurat", "SeuratDisk", "SeuratObject"),
  version = c(
    paste(R.version$major, R.version$minor, sep = "."),
    as.character(packageVersion("Seurat")),
    as.character(packageVersion("SeuratDisk")),
    as.character(packageVersion("SeuratObject"))
  )
)
write.csv(versions, file.path(outdir, "build_versions.csv"), row.names = FALSE)
cat("Version info written to", file.path(outdir, "build_versions.csv"), "\n")
