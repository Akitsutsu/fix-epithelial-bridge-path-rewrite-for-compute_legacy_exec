#!/usr/bin/env Rscript
# build_reference_candidate_v1.R
#
# Build a candidate fetal lung reference from an upstream RDS source.
# Generalization of build_frozen_reference_v1.R for candidate reference testing.
#
# All output goes to --outdir. The frozen pair under converted/ is NEVER touched.
#
# Required:
#   --source-rds PATH    Upstream RDS file
#   --outdir PATH        Output directory for candidate artifacts
#   --tag STRING         Candidate tag (e.g. "2026-04-early-only")
#
# Optional:
#   --codebook-dir PATH  Codebook directory (default: codebook). Recorded in
#                         manifest for the metadata extraction step.
#   --sample-week-include WEEKS
#       Comma-separated sample_week values to keep (e.g. week_10,week_11).
#       If omitted, all weeks are included.
#
# Outputs (written to --outdir):
#   reference_RNA.h5Seurat
#   reference_RNA.h5ad
#   build_versions.csv
#   build_manifest.yaml
#
# Example:
#   Rscript build_reference_candidate_v1.R \
#     --source-rds full_fetal_lung_dataset.rds \
#     --outdir references/candidates/2026-04-early-only \
#     --tag 2026-04-early-only \
#     --sample-week-include week_10,week_11,week_12,week_13
#
# TODO filters not yet implemented (need deeper metadata evidence):
#   --donor-include      Filter by donor / orig.ident
#   --cell-type-include  Filter by cell_type (requires codebook access in R)
#   --gene-include       Restrict to a gene list

# ── Argument parsing ──────────────────────────────────────────────────────────

parse_args <- function() {
  raw <- commandArgs(trailingOnly = TRUE)
  p <- list(source_rds = NULL, outdir = NULL, tag = NULL,
            codebook_dir = "codebook", sample_week_include = NULL)
  i <- 1L
  while (i <= length(raw)) {
    a <- raw[i]
    if (a == "--source-rds") {
      p$source_rds <- raw[i + 1L]; i <- i + 2L
    } else if (a == "--outdir") {
      p$outdir <- raw[i + 1L]; i <- i + 2L
    } else if (a == "--tag") {
      p$tag <- raw[i + 1L]; i <- i + 2L
    } else if (a == "--codebook-dir") {
      p$codebook_dir <- raw[i + 1L]; i <- i + 2L
    } else if (a == "--sample-week-include") {
      p$sample_week_include <- strsplit(raw[i + 1L], ",")[[1]]; i <- i + 2L
    } else {
      stop(paste("Unknown argument:", a))
    }
  }
  if (is.null(p$source_rds)) stop("--source-rds is required")
  if (is.null(p$outdir))     stop("--outdir is required")
  if (is.null(p$tag))        stop("--tag is required")
  p
}

args <- parse_args()
dir.create(args$outdir, recursive = TRUE, showWarnings = FALSE)

cat("=== build_reference_candidate_v1.R ===\n")
cat("Tag:         ", args$tag, "\n")
cat("Source RDS:  ", args$source_rds, "\n")
cat("Output dir:  ", args$outdir, "\n")
cat("Codebook dir:", args$codebook_dir, "\n")
if (!is.null(args$sample_week_include))
  cat("Week filter: ", paste(args$sample_week_include, collapse = ", "), "\n")

# ── Load libraries ────────────────────────────────────────────────────────────

library(Seurat)
library(SeuratDisk)

cat("Seurat version:      ", as.character(packageVersion("Seurat")), "\n")
cat("SeuratDisk version:  ", as.character(packageVersion("SeuratDisk")), "\n")
cat("SeuratObject version:", as.character(packageVersion("SeuratObject")), "\n")

# ── Load RDS ──────────────────────────────────────────────────────────────────

if (!file.exists(args$source_rds))
  stop(paste("Source RDS not found:", args$source_rds))

cat("Loading RDS ...\n")
ref <- readRDS(args$source_rds)
cat("Loaded. Cells:", ncol(ref), " Assays:", paste(Assays(ref), collapse = ", "), "\n")

DefaultAssay(ref) <- "RNA"
cells_before <- ncol(ref)

# ── Optional sample_week filter ───────────────────────────────────────────────

if (!is.null(args$sample_week_include)) {
  if (!"sample_week" %in% colnames(ref@meta.data))
    stop("sample_week column not found in Seurat metadata. Cannot apply --sample-week-include.")

  actual_weeks <- sort(unique(as.character(ref$sample_week)))
  cat("Available sample_week values:", paste(actual_weeks, collapse = ", "), "\n")

  invalid <- setdiff(args$sample_week_include, actual_weeks)
  if (length(invalid) > 0)
    warning(paste("Requested weeks not found in data:", paste(invalid, collapse = ", ")))

  keep <- as.character(ref$sample_week) %in% args$sample_week_include
  if (sum(keep) == 0) stop("Filter resulted in 0 cells. Aborting.")

  ref <- subset(ref, cells = colnames(ref)[keep])
  cat("Filtered:", cells_before, "->", ncol(ref), "cells\n")
}

cells_after <- ncol(ref)
genes <- nrow(ref[["RNA"]])

# ── Export h5Seurat and h5ad ──────────────────────────────────────────────────

h5seurat_path <- file.path(args$outdir, "reference_RNA.h5Seurat")
h5ad_path     <- file.path(args$outdir, "reference_RNA.h5ad")

cat("Saving h5Seurat:", h5seurat_path, "\n")
SaveH5Seurat(ref, filename = h5seurat_path, overwrite = TRUE)

cat("Converting to h5ad:", h5ad_path, "\n")
Convert(h5seurat_path, dest = "h5ad", overwrite = TRUE)

# ── build_versions.csv ────────────────────────────────────────────────────────

versions <- data.frame(
  package = c("R", "Seurat", "SeuratDisk", "SeuratObject"),
  version = c(
    paste(R.version$major, R.version$minor, sep = "."),
    as.character(packageVersion("Seurat")),
    as.character(packageVersion("SeuratDisk")),
    as.character(packageVersion("SeuratObject"))
  )
)
write.csv(versions, file.path(args$outdir, "build_versions.csv"), row.names = FALSE)

# ── build_manifest.yaml ──────────────────────────────────────────────────────

manifest_lines <- c(
  "# Candidate reference build manifest",
  paste0("tag: ", args$tag),
  paste0("source_rds: ", basename(args$source_rds)),
  paste0("build_date: ", Sys.Date()),
  paste0("build_script: build_reference_candidate_v1.R"),
  paste0("codebook_dir: ", args$codebook_dir),
  paste0("sample_week_include: ",
         if (!is.null(args$sample_week_include))
           paste(args$sample_week_include, collapse = ",")
         else "all"),
  paste0("cells_before_filter: ", cells_before),
  paste0("cells_after_filter: ", cells_after),
  paste0("genes: ", genes),
  paste0("h5seurat_output: reference_RNA.h5Seurat"),
  paste0("h5ad_output: reference_RNA.h5ad")
)
writeLines(manifest_lines, file.path(args$outdir, "build_manifest.yaml"))

# ── Summary ───────────────────────────────────────────────────────────────────

cat("\nDone. Candidate artifacts written to:", args$outdir, "\n")
cat("  ", h5ad_path, "\n")
cat("  ", h5seurat_path, "\n")
cat("  ", file.path(args$outdir, "build_versions.csv"), "\n")
cat("  ", file.path(args$outdir, "build_manifest.yaml"), "\n")
