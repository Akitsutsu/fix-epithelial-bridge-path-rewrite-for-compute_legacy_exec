# Local vs GitHub Reconciliation Report v1

Generated: 2026-04-03
Branch at time of inspection: `infra/fix_whole_lung_combined_root_outdir`

---

## A. Executive Summary

The repository has 13 local branches (11 merged into main, 2 active work branches).
There are ~65 untracked items in the repo root — a mix of scratch scripts, debugging notes,
generated benchmark run directories, data directories, and download artifacts accumulated
across the GSE237359 intake, infra bridge-fix, and early spatial work.

Key findings:
- **11 branches already merged into main** still exist locally and on remote. Safe to prune.
- **2 active branches** (`infra/fix_whole_lung_combined_root_outdir`, `tranche/next_external_organoid_intake_v1`) are pushed but not yet merged.
- **19 benchmark_run_* directories** (~20 MB total) are generated outputs; all but one are gitignored.
- **~80 GB of data** lives in `data/`, `rebuild_audit_v1/`, `objects/`, `queries/` — none tracked (by design).
- **3 root-level scripts** are exact duplicates of copies in `scripts/`.
- **2 "(1)" files** are browser-download duplicates identical to their originals.
- **1 empty Japanese-named text file** is a Windows artifact.
- **1 `.bak` file** is already covered by the `.bak` gitignore pattern.
- The `.gitignore` covers most generated outputs, but `benchmark_run_gse237359_manual_compare/` slips through.

---

## B. Branch Status

### Merged into main (safe to delete both local and remote)

| Branch | Last commit | Merged via |
|---|---|---|
| `audit/reference-rebuild-v1` | `3f6dc8b` | PR #5 |
| `docs/reference-provenance-v1` | `65bcb9d` | PR #3 |
| `docs/reference-update-system-v1` | `ccec90b` | PR #6 |
| `feat/organoid-inventory-phaseA-v1` | `8b85d18` | PR #11 |
| `feat/reference-candidate-build-v1` | `000fdcf` | PR #8 |
| `feat/reference-drift-report-v1` | `bc677df` | PR #9 |
| `feat/reference-promotion-scaffolding-v1` | `6104a29` | PR #10 |
| `feat/reference-registry-v1` | `97f78ca` | PR #7 |
| `fix/epi-bridge-paths` | `e78ae86` | PR #4 |
| `tranche/gse237359_external_validation_v1` | `0c2f744` | PR #12 |

Classification: **SAFE_TO_DELETE_BRANCH** (all 10, both local and remote)

### Active work branches (NOT merged)

| Branch | Ahead of main | Status |
|---|---|---|
| `infra/fix_whole_lung_combined_root_outdir` | 4 commits | Pushed. Contains epithelial bridge fix, off-target key fix, combined-root outdir fix. Ready for PR. |
| `tranche/next_external_organoid_intake_v1` | 3 commits | Pushed. Contains GSE221343 registration, sample sheet. Active intake work. |

Classification: **KEEP_TRACKED** (both)

---

## C. Tracked-vs-Untracked File Triage

### Root-level untracked scripts

| Path | Size | Classification | Rationale |
|---|---|---|---|
| `append_gse237359_donors_to_manifest_v2.py` | 3.5 KB | IGNORE_LOCAL_SCRATCH | One-shot manifest builder; work is done |
| `build_gse237359_projection_manifest.py` | 4.8 KB | SAFE_TO_DELETE_LOCAL | Identical copy exists at `scripts/` |
| `build_spatial_objects.py` | 15 KB | REVIEW_NEEDED | Spatial pipeline script; may be needed for spatial lane |
| `collect_projection_key_metrics_multiroot.py` | 4.6 KB | SAFE_TO_DELETE_LOCAL | Tracked at `scripts/collect_projection_key_metrics_multiroot.py` |
| `collect_projection_key_metrics_v2.py` | 6.1 KB | IGNORE_LOCAL_SCRATCH | Superseded by v4 and multiroot versions |
| `collect_projection_key_metrics_v4.py` | 10.8 KB | IGNORE_LOCAL_SCRATCH | Superseded by tracked multiroot version |
| `collect_projection_metrics.py` | 2.4 KB | SAFE_TO_DELETE_LOCAL | Identical copy at `scripts/` |
| `gse237359_expand_sample_sheet_from_report.py` | 6.0 KB | SAFE_TO_DELETE_LOCAL | Identical copy at `scripts/` |
| `gse237359_inspect_and_split_pooled_scrna.py` | 19.4 KB | IGNORE_LOCAL_SCRATCH | v1; superseded by v3 |
| `gse237359_inspect_and_split_pooled_scrna_v3.py` | 19.4 KB | IGNORE_LOCAL_SCRATCH | One-shot donor split script; work is done |
| `inspect_reference_h5seurat.R` | 752 B | IGNORE_LOCAL_SCRATCH | One-shot reference inspection |
| `inspect_reference_rds.R` | 752 B | IGNORE_LOCAL_SCRATCH | One-shot reference inspection |
| `make_visium_coarse_lineage_maps.py` | 14 KB | REVIEW_NEEDED | Spatial visualization; may be needed for spatial lane |
| `make_visium_control_maps.py` | 8.4 KB | REVIEW_NEEDED | Spatial visualization |
| `make_visium_state_maps_epi_gated.py` | 21 KB | REVIEW_NEEDED | Spatial visualization |
| `make_visium_state_maps_from_release_v1.py` | 17 KB | REVIEW_NEEDED | Spatial visualization |
| `make_xenium_6gene_overlays.py` | 6.0 KB | REVIEW_NEEDED | Spatial visualization |
| `patch_whole_lung_bridge_forced_outdir.py` | 3.8 KB | SAFE_TO_DELETE_LOCAL | Debugging patch; fix is now committed |
| `provenance_audit_h5ad_fixed.py` | 21 KB | REVIEW_NEEDED | May differ from tracked `provenance_audit_h5ad.py` |
| `scan_rewritten_script_for_hardcodes.py` | tracked | KEEP_TRACKED | Already tracked |
| `xenium_airway_crops.py` | 9.2 KB | REVIEW_NEEDED | Spatial pipeline |
| `xenium_local_crop_from_raw.py` | 7.4 KB | IGNORE_LOCAL_SCRATCH | Superseded by v2/v3 |
| `xenium_local_crop_from_raw_v2.py` | 9.8 KB | IGNORE_LOCAL_SCRATCH | Superseded by v3 |
| `xenium_local_crop_from_raw_v3.py` | 11.8 KB | REVIEW_NEEDED | Latest xenium crop version; spatial lane |
| `xenium_roi_quant.py` | 11.4 KB | REVIEW_NEEDED | Spatial quantification |
| `git_stage_gse237359_external_validation_v1.sh` | 3.0 KB | SAFE_TO_DELETE_LOCAL | One-shot git staging script; tranche already merged |

### Root-level untracked scripts in `scripts/` (untracked copies)

| Path | Classification | Rationale |
|---|---|---|
| `scripts/build_gse237359_projection_manifest.py` | IGNORE_LOCAL_SCRATCH | Untracked; identical to root copy |
| `scripts/collect_projection_metrics.py` | IGNORE_LOCAL_SCRATCH | Untracked; identical to root copy |
| `scripts/gse237359_expand_sample_sheet_from_report.py` | IGNORE_LOCAL_SCRATCH | Untracked; identical to root copy |

### Root-level untracked notes / memos / docs

| Path | Lines | Classification | Rationale |
|---|---|---|---|
| `ca1_diff_and_cleanup_playbook.md` | 92 | IGNORE_LOCAL_SCRATCH | Early playbook; work completed |
| `claude_code_prompt_gse237359_intake_v1.md` | 125 | IGNORE_LOCAL_SCRATCH | Prompt template; ephemeral |
| `gse237359_git_branch_runbook_v1.md` | 40 | IGNORE_LOCAL_SCRATCH | Branch management notes; superseded |
| `gse237359_github_integration_recommendation_v1.md` | 26 | IGNORE_LOCAL_SCRATCH | One-shot recommendation; acted on |
| `gse237359_projection_runbook_v1.md` | 62 | IGNORE_LOCAL_SCRATCH | Projection runbook; work done |
| `gse237359_tranche_README_draft_v1.md` | 31 | SAFE_TO_DELETE_LOCAL | Draft; canonical README tracked in `reports/tranches/` |
| `gse237359_tranche_result_memo_v1.md` | ~same | SAFE_TO_DELETE_LOCAL | Canonical copy tracked at `reports/tranches/gse237359.../` |
| `gse237359_tranche_result_memo_v1 (1).md` | ~same | SAFE_TO_DELETE_LOCAL | Browser download duplicate, identical to above |
| `gse237359_vs_CA1_BU3_canonical_compare_table_v1.tsv` | — | IGNORE_LOCAL_SCRATCH | Superset of tracked `key_metrics_multiroot.tsv` (different columns) |
| `gse237359_vs_CA1_BU3_canonical_compare_table_v1 (1).tsv` | — | SAFE_TO_DELETE_LOCAL | Browser download duplicate, identical to above |
| `gse237359_vs_CA1_BU3_comparison_figure_v1.png` | — | SAFE_TO_DELETE_LOCAL | Tracked at `reports/tranches/gse237359.../` (identical) |
| `gse237359_work_summary_and_github_boundary_v1.md` | 42 | IGNORE_LOCAL_SCRATCH | Work summary; ephemeral |
| `handoff_parity_reached_2026-03-29.md` | 106 | IGNORE_LOCAL_SCRATCH | Parity milestone note |
| `lungs_analysisCLAUDE.md.txt` | 35 | IGNORE_LOCAL_SCRATCH | Draft CLAUDE.md; not active |
| `new_chat_seed_post_parity.txt` | 41 | IGNORE_LOCAL_SCRATCH | Chat prompt seed; ephemeral |
| `pr_fix_epi_bridge_paths.md` | 55 | SAFE_TO_DELETE_LOCAL | PR description draft; PR already merged |
| `whole_lung_bridge_hotfix_note_2026-04-03.md` | 116 | IGNORE_LOCAL_SCRATCH | Hotfix notes for current infra work |
| `whole_lung_forced_outdir_patch_instructions_2026-04-03.md` | 109 | IGNORE_LOCAL_SCRATCH | Patch instructions for current infra work |

### Root-level untracked data / manifest files

| Path | Size | Classification | Rationale |
|---|---|---|---|
| `gse237359_organoid_query_sample_sheet_v1.tsv` | 11.7 KB | IGNORE_LOCAL_SCRATCH | Earlier version; v2 tracked at `queries/converted/gse237359/` |
| `query_manifest_gse237359_vs_CA1_BU3_minimal_v1.csv` | 453 B | IGNORE_LOCAL_SCRATCH | Subset manifest; superseded by full manifest |
| `query_manifest_v1_plus_gse237359.csv` | 1.1 KB | REVIEW_NEEDED | Active manifest used by benchmark runner; referenced by infra branch |
| `ref_sig_gw10_epi.csv` | 6.9 MB | REVIEW_NEEDED | Epithelial signature file; may be needed |
| `riken_to_symbol.csv` | 177 B | IGNORE_LOCAL_SCRATCH | Gene symbol mapping; one-shot |
| `mart_export.csv.txt` | 26 MB | SAFE_TO_DELETE_LOCAL | BioMart export; re-downloadable |
| `mart_export.new.txt` | 26 MB | SAFE_TO_DELETE_LOCAL | BioMart export duplicate |
| `epithelial_only_remap_common_v2.py.bak.20260329_084630` | 16.4 KB | SAFE_TO_DELETE_LOCAL | Backup; gitignored by `*.bak` pattern but file shows in status |
| `新規 テキスト ドキュメント.txt` | 0 B | SAFE_TO_DELETE_LOCAL | Empty Windows-created text file |

### Untracked files in `metadata/external/`

| Path | Classification | Rationale |
|---|---|---|
| `metadata/external/gse237359_organoid_query_sample_sheet_v1.tsv` | REVIEW_NEEDED | Earlier sample sheet v1; v2 tracked at `queries/converted/gse237359/`. Check if still needed. |

Note: `metadata/external/gse221343_*` files are tracked on `tranche/next_external_organoid_intake_v1` only; they appear untracked on this branch.

---

## D. Generated Run Directories Triage

### Gitignored benchmark runs (all SAFE_TO_DELETE_LOCAL)

| Directory | Size | Classification | Rationale |
|---|---|---|---|
| `benchmark_run_v1/` | 24 KB | SAFE_TO_DELETE_LOCAL | Early prototype run |
| `benchmark_run_v1_compute_legacy/` | 2.0 MB | SAFE_TO_DELETE_LOCAL | Early compute test |
| `benchmark_run_v1_replay/` | 644 KB | SAFE_TO_DELETE_LOCAL | Early replay test |
| `benchmark_run_v1_replay_v2/` | 644 KB | SAFE_TO_DELETE_LOCAL | Early replay test |
| `benchmark_run_gse237359_vs_CA1_BU3_compute/` | 8.2 MB | REVIEW_NEEDED | Active 6-query verified run; needed until results committed |
| `benchmark_run_gse237359_vs_CA1_CA1_compute/` | 1.3 MB | SAFE_TO_DELETE_LOCAL | Single-query standalone run; superseded by combined-root |
| `benchmark_run_gse237359_vs_CA1_BU3_dryrun_check/` | 20 KB | SAFE_TO_DELETE_LOCAL | Dry run test |
| `benchmark_run_gse237359_vs_G237359_*_compute/` (4 dirs) | ~6 MB | SAFE_TO_DELETE_LOCAL | Single-query standalone runs; superseded |
| `benchmark_run_gse237359_vs_*_symlink/` (7 dirs) | ~2.7 MB | SAFE_TO_DELETE_LOCAL | Symlink workaround dirs; approach abandoned |

### Not gitignored

| Directory | Size | Classification | Rationale |
|---|---|---|---|
| `benchmark_run_gse237359_manual_compare/` | 4 KB | REVIEW_NEEDED | Contains `gse237359_vs_CA1_BU3_key_metrics_multiroot.tsv` referenced as comparison baseline. Canonical copy is tracked at `reports/tranches/gse237359_external_validation_v1/`. Should be gitignored. |

### Large data directories (all gitignored by pattern or extension)

| Directory | Size | Classification | Rationale |
|---|---|---|---|
| `data/` | 69 GB | IGNORE_LOCAL_SCRATCH | Spatial data (Visium/Xenium); local only by design |
| `rebuild_audit_v1/` | 9.6 GB | IGNORE_LOCAL_SCRATCH | Reference rebuild audit artifacts; local only |
| `objects/` | 1.6 GB | IGNORE_LOCAL_SCRATCH | Spatial AnnData objects; local only |
| `queries/raw/` | ~700 MB | IGNORE_LOCAL_SCRATCH | Raw downloads (GSE237359 + GSE221343); local only |
| `qc_png/` | 138 MB | IGNORE_LOCAL_SCRATCH | QC figures; local only |
| `codebook/` (untracked CSVs) | 56 KB | IGNORE_LOCAL_SCRATCH | Cross-tab CSVs not in tracked codebook set |
| `config/` | 4 KB | IGNORE_LOCAL_SCRATCH | Visium config; local only |
| `roi_boxes/` | 0 | SAFE_TO_DELETE_LOCAL | Empty directory |

---

## E. Proposed .gitignore Additions

Current `.gitignore` covers most cases well. Suggested additions:

```gitignore
# Manual comparison baseline directories (non-canonical; canonical is in reports/)
benchmark_run_gse237359_manual_compare/

# Raw query downloads
queries/raw/

# Local data directories
data/
objects/
rebuild_audit_v1/
qc_png/
roi_boxes/
codebook/xtab_*
config/

# One-shot scratch manifests
query_manifest_*_minimal_*.csv

# BioMart exports
mart_export*

# Windows artifacts
新規*
```

No removals from current `.gitignore` are recommended.

---

## F. Safe Next Actions (exact commands)

### F.1 Delete merged branches (local)

```bash
for b in audit/reference-rebuild-v1 docs/reference-provenance-v1 docs/reference-update-system-v1 feat/organoid-inventory-phaseA-v1 feat/reference-candidate-build-v1 feat/reference-drift-report-v1 feat/reference-promotion-scaffolding-v1 feat/reference-registry-v1 fix/epi-bridge-paths tranche/gse237359_external_validation_v1; do
  git branch -d "$b"
done
```

### F.2 Delete merged branches (remote)

```bash
for b in audit/reference-rebuild-v1 docs/reference-provenance-v1 docs/reference-update-system-v1 feat/organoid-inventory-phaseA-v1 feat/reference-candidate-build-v1 feat/reference-drift-report-v1 feat/reference-promotion-scaffolding-v1 feat/reference-registry-v1 fix/epi-bridge-paths tranche/gse237359_external_validation_v1; do
  git push origin --delete "$b"
done
```

### F.3 Delete exact-duplicate files

```bash
rm "gse237359_tranche_result_memo_v1 (1).md"
rm "gse237359_vs_CA1_BU3_canonical_compare_table_v1 (1).tsv"
rm gse237359_vs_CA1_BU3_comparison_figure_v1.png
rm gse237359_tranche_result_memo_v1.md
rm gse237359_tranche_README_draft_v1.md
rm pr_fix_epi_bridge_paths.md
rm 新規\ テキスト\ ドキュメント.txt
```

### F.4 Delete root-level script duplicates (identical copies exist in scripts/)

```bash
rm build_gse237359_projection_manifest.py
rm collect_projection_metrics.py
rm gse237359_expand_sample_sheet_from_report.py
rm collect_projection_key_metrics_multiroot.py
```

### F.5 Delete obsolete debugging artifacts

```bash
rm patch_whole_lung_bridge_forced_outdir.py
rm git_stage_gse237359_external_validation_v1.sh
rm epithelial_only_remap_common_v2.py.bak.20260329_084630
```

### F.6 Delete re-downloadable BioMart files (~52 MB)

```bash
rm mart_export.csv.txt mart_export.new.txt
```

### F.7 Delete obsolete symlink workaround dirs

```bash
rm -rf benchmark_run_gse237359_vs_*_symlink/
```

### F.8 Delete obsolete standalone run dirs

```bash
rm -rf benchmark_run_v1/ benchmark_run_v1_compute_legacy/ benchmark_run_v1_replay/ benchmark_run_v1_replay_v2/
rm -rf benchmark_run_gse237359_vs_CA1_CA1_compute/
rm -rf benchmark_run_gse237359_vs_CA1_BU3_dryrun_check/
rm -rf benchmark_run_gse237359_vs_G237359_15934_G237359_15934_compute/
rm -rf benchmark_run_gse237359_vs_G237359_16011_G237359_16011_compute/
rm -rf benchmark_run_gse237359_vs_G237359_16392_G237359_16392_compute/
rm -rf benchmark_run_gse237359_vs_G237359_16402_G237359_16402_compute/
```

### F.9 Delete empty directory

```bash
rm -rf roi_boxes/
```

---

## G. DO_NOT_TOUCH

The following are canonical tracked files and directories that must not be modified or deleted:

### Frozen reference artifacts
- `converted/reference_metadata_v1.csv`
- (All `.h5ad` files are gitignored but `converted/reference_RNA.h5ad` is the canonical reference)

### Tracked science and infrastructure code
- `benchmark_common_runner_v2.py`
- `whole_lung_project_common_v2.py`
- `epithelial_only_remap_common_v2.py`
- `epithelial_only_remap_BU3_v1.py`
- `project_BU3_to_reference_RNA_v1.py`
- `provenance_audit_h5ad.py`
- `epithelial_only_remap_v1.py`
- `epithelial_only_remap_common_v1.py`
- `whole_lung_project_common_v1.py`
- `benchmark_common_runner_v1.py`
- All files in `references/`
- `legacy_output_manifest_v1.csv`
- `query_manifest_v1.csv`

### Tracked reports and tranche artifacts
- `reports/tranches/gse237359_external_validation_v1/` (entire directory)
- `reports/infra/whole_lung_combined_root_outdir.md`
- `reports/organoid_cohort_readiness_v1.md`

### Tracked query artifacts
- `queries/converted/gse237359/GSM8229877_inspection_report.json`
- `queries/converted/gse237359/gse237359_organoid_query_sample_sheet_v2.tsv`

### Tracked documentation
- All `*_v1.md` files at root that are in `git ls-files`
- `.gitignore`

### Active work branches (do not delete)
- `infra/fix_whole_lung_combined_root_outdir`
- `tranche/next_external_organoid_intake_v1`

### Local data needed for active work (do not delete yet)
- `queries/converted/gse237359/donor_split_h5ad/` (4 h5ad files used by benchmark runner)
- `queries/raw/gse221343/` (downloaded H5 files for GSE221343 intake)
- `benchmark_run_gse237359_vs_CA1_BU3_compute/` (current verified 6-query run output)
- `query_manifest_v1_plus_gse237359.csv` (active manifest for combined-root runs)
