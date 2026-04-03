# Cleanup Actions Log v1

Executed: 2026-04-03
Based on: `reports/repo_state/local_github_reconciliation_report_v1.md`

---

## Actions performed

### 1. Deleted 10 merged local branches

All verified `git branch --merged main` before deletion. Used `git branch -d` (safe delete).

```
audit/reference-rebuild-v1        (was 3f6dc8b)
docs/reference-provenance-v1      (was 65bcb9d)
docs/reference-update-system-v1   (was ccec90b)
feat/organoid-inventory-phaseA-v1 (was 8b85d18)
feat/reference-candidate-build-v1 (was 000fdcf)
feat/reference-drift-report-v1    (was bc677df)
feat/reference-promotion-scaffolding-v1 (was 6104a29)
feat/reference-registry-v1        (was 97f78ca)
fix/epi-bridge-paths              (was e78ae86)
tranche/gse237359_external_validation_v1 (was 0c2f744)
```

Rollback: `git branch <name> <sha>` to recreate any branch.

### 2. Deleted 10 merged remote branches

Same 10 branches deleted from `origin` via `git push origin --delete`.

Rollback: `git push origin <sha>:refs/heads/<name>` to recreate any remote branch.

### 3. Deleted 7 exact-duplicate / obsolete untracked files

```
gse237359_tranche_result_memo_v1 (1).md       — browser dup; original also deleted (tracked in reports/)
gse237359_vs_CA1_BU3_canonical_compare_table_v1 (1).tsv — browser dup
gse237359_vs_CA1_BU3_comparison_figure_v1.png — canonical tracked in reports/tranches/gse237359_external_validation_v1/
gse237359_tranche_result_memo_v1.md           — canonical tracked in reports/tranches/gse237359_external_validation_v1/
gse237359_tranche_README_draft_v1.md          — canonical README tracked in reports/tranches/
pr_fix_epi_bridge_paths.md                    — PR #4 already merged
新規 テキスト ドキュメント.txt                   — 0-byte Windows artifact
```

Rollback: tracked canonical copies exist in git; no data lost.

### 4. Deleted 4 root-level script duplicates

```
build_gse237359_projection_manifest.py        — identical at scripts/build_gse237359_projection_manifest.py
collect_projection_metrics.py                 — identical at scripts/collect_projection_metrics.py
gse237359_expand_sample_sheet_from_report.py  — identical at scripts/gse237359_expand_sample_sheet_from_report.py
collect_projection_key_metrics_multiroot.py   — tracked at scripts/collect_projection_key_metrics_multiroot.py
```

Rollback: copies still exist in `scripts/` directory.

### 5. Deleted 3 obsolete debugging artifacts

```
patch_whole_lung_bridge_forced_outdir.py      — fix committed to whole_lung_project_common_v2.py
git_stage_gse237359_external_validation_v1.sh — tranche merged via PR #12
epithelial_only_remap_common_v2.py.bak.20260329_084630 — .bak of file now committed
```

Rollback: these were one-shot; the fixes they implemented are in tracked code.

### 6. Deleted 2 BioMart exports (~52 MB)

```
mart_export.csv.txt  (26 MB)
mart_export.new.txt  (26 MB)
```

Rollback: re-download from Ensembl BioMart.

### 7. Deleted 7 symlink workaround benchmark directories

```
benchmark_run_gse237359_vs_BU3_BU3_compute_symlink/
benchmark_run_gse237359_vs_CA1_BU3_compute_symlink/
benchmark_run_gse237359_vs_CA1_CA1_compute_symlink/
benchmark_run_gse237359_vs_G237359_15934_G237359_15934_compute_symlink/
benchmark_run_gse237359_vs_G237359_16011_G237359_16011_compute_symlink/
benchmark_run_gse237359_vs_G237359_16392_G237359_16392_compute_symlink/
benchmark_run_gse237359_vs_G237359_16402_G237359_16402_compute_symlink/
```

Rollback: re-run benchmarks if needed; approach was abandoned.

### 8. Deleted 10 obsolete standalone/prototype run directories

```
benchmark_run_v1/
benchmark_run_v1_compute_legacy/
benchmark_run_v1_replay/
benchmark_run_v1_replay_v2/
benchmark_run_gse237359_vs_CA1_CA1_compute/
benchmark_run_gse237359_vs_CA1_BU3_dryrun_check/
benchmark_run_gse237359_vs_G237359_15934_G237359_15934_compute/
benchmark_run_gse237359_vs_G237359_16011_G237359_16011_compute/
benchmark_run_gse237359_vs_G237359_16392_G237359_16392_compute/
benchmark_run_gse237359_vs_G237359_16402_G237359_16402_compute/
```

Rollback: re-run `benchmark_common_runner_v2.py` with appropriate flags.

### 9. Deleted 1 empty directory

```
roi_boxes/
```

Rollback: `mkdir roi_boxes/`

### 10. Updated .gitignore

Added patterns for: `benchmark_run_gse237359_manual_compare/`, `queries/raw/`,
`data/`, `objects/`, `rebuild_audit_v1/`, `qc_png/`, `roi_boxes/`, `codebook/xtab_*`,
`config/`, `query_manifest_*_minimal_*.csv`, `mart_export*`, `新規*`.

Rollback: `git checkout -- .gitignore`

---

## Items NOT touched

- All REVIEW_NEEDED items (see report section C and D)
- All DO_NOT_TOUCH items (see report section G)
- Active branches: `infra/fix_whole_lung_combined_root_outdir`, `tranche/next_external_organoid_intake_v1`
- Active run: `benchmark_run_gse237359_vs_CA1_BU3_compute/`
- Active manifest: `query_manifest_v1_plus_gse237359.csv`
- All tracked files
