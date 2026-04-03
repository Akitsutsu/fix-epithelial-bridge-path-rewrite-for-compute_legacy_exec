# Local vs GitHub Reconciliation Report v3 (aggressive cleanup)

Generated: 2026-04-03
Branch at inspection: `infra/fix_whole_lung_combined_root_outdir`
Predecessor: v1 cleanup already removed 16 files, 17 dirs, 10 branches.

---

## A. Executive summary

After v1 cleanup the repo still has 39 untracked items and 72 tracked files.
Many tracked files are v1-era development notes, superseded adapters, replay
templates, and one-shot debugging scripts that are no longer needed for the
current v2 runner/adapter system or any canonical science artifact.

This report identifies:
- 26 untracked files/dirs safe to delete
- 0 branches to delete (v1 cleanup already pruned all 10 merged branches)
- 17 tracked files safe to delete via a dedicated commit
- .gitignore additions needed on main (v1 cleanup added them on infra branch only)
- 15 items classified REVIEW_NEEDED (spatial pipeline + active-work manifests)

---

## B. Branch triage

| Branch | Classification | Rationale |
|---|---|---|
| `main` | KEEP_TRACKED | Default branch |
| `infra/fix_whole_lung_combined_root_outdir` | KEEP_TRACKED | Active; 5 commits ahead of main; not merged |
| `tranche/next_external_organoid_intake_v1` | KEEP_TRACKED | Active; 3 commits ahead of main; not merged |

No merged branches remain (v1 cleanup deleted all 10).

---

## C. Untracked/local file triage

### SAFE_TO_DELETE_LOCAL_UNTRACKED

| Item | Kind | Rationale |
|---|---|---|
| `append_gse237359_donors_to_manifest_v2.py` | helper script | One-shot manifest builder; work complete |
| `ca1_diff_and_cleanup_playbook.md` | note | Early playbook; completed |
| `claude_code_prompt_gse237359_intake_v1.md` | note | Ephemeral prompt template |
| `collect_projection_key_metrics_v2.py` | helper script | Superseded by tracked multiroot version |
| `collect_projection_key_metrics_v4.py` | helper script | Superseded by tracked multiroot version |
| `gse237359_git_branch_runbook_v1.md` | note | Branch management; completed |
| `gse237359_github_integration_recommendation_v1.md` | note | Recommendation; acted on |
| `gse237359_inspect_and_split_pooled_scrna.py` | helper script | v1; superseded by v3 |
| `gse237359_inspect_and_split_pooled_scrna_v3.py` | helper script | One-shot donor split; complete |
| `gse237359_organoid_query_sample_sheet_v1.tsv` | data | v1; v2 tracked at queries/converted/gse237359/ |
| `gse237359_projection_runbook_v1.md` | note | Projection runbook; complete |
| `gse237359_vs_CA1_BU3_canonical_compare_table_v1.tsv` | data | Scratch compare; canonical tracked in reports/ |
| `gse237359_work_summary_and_github_boundary_v1.md` | note | Summary; superseded |
| `handoff_parity_reached_2026-03-29.md` | note | Milestone note; historical only |
| `inspect_reference_h5seurat.R` | helper script | One-shot reference inspection |
| `inspect_reference_rds.R` | helper script | One-shot reference inspection |
| `lungs_analysisCLAUDE.md.txt` | note | Draft CLAUDE.md; not active |
| `new_chat_seed_post_parity.txt` | note | Ephemeral prompt seed |
| `riken_to_symbol.csv` | data | Tiny gene mapping; one-shot |
| `whole_lung_bridge_hotfix_note_2026-04-03.md` | note | Hotfix notes for now-committed fix |
| `whole_lung_forced_outdir_patch_instructions_2026-04-03.md` | note | Patch instructions for now-committed fix |
| `xenium_local_crop_from_raw.py` | helper script | v1; superseded by v3 |
| `xenium_local_crop_from_raw_v2.py` | helper script | v2; superseded by v3 |
| `scripts/build_gse237359_projection_manifest.py` | helper script | Untracked copy; root copy already deleted |
| `scripts/collect_projection_metrics.py` | helper script | Untracked copy |
| `scripts/gse237359_expand_sample_sheet_from_report.py` | helper script | Untracked copy |

### REVIEW_NEEDED

| Item | Kind | Rationale |
|---|---|---|
| `build_spatial_objects.py` | script | Spatial pipeline; may be needed |
| `make_visium_coarse_lineage_maps.py` | script | Spatial visualization |
| `make_visium_control_maps.py` | script | Spatial visualization |
| `make_visium_state_maps_epi_gated.py` | script | Spatial visualization |
| `make_visium_state_maps_from_release_v1.py` | script | Spatial visualization |
| `make_xenium_6gene_overlays.py` | script | Spatial visualization |
| `xenium_airway_crops.py` | script | Spatial pipeline |
| `xenium_local_crop_from_raw_v3.py` | script | Latest xenium version |
| `xenium_roi_quant.py` | script | Spatial quantification |
| `provenance_audit_h5ad_fixed.py` | script | May differ from tracked provenance_audit_h5ad.py |
| `query_manifest_v1_plus_gse237359.csv` | data | Active manifest for infra branch benchmark runs |
| `ref_sig_gw10_epi.csv` | data | Epithelial signature (6.9 MB); may be needed |
| `metadata/external/gse237359_organoid_query_sample_sheet_v1.tsv` | data | Earlier v1; v2 tracked; check if still needed |
| `metadata/external/gse221343_dataset_manifest_v1.yaml` | data | Tracked on intake branch only; appears untracked here |
| `metadata/external/gse221343_organoid_query_sample_sheet_v1.tsv` | data | Tracked on intake branch only; appears untracked here |

---

## D. Generated run directory triage

| Directory | Size | Classification | Rationale |
|---|---|---|---|
| `benchmark_run_gse237359_vs_CA1_BU3_compute/` | 8.2 MB | REVIEW_NEEDED | Active verified 6-query run |
| `benchmark_run_gse237359_manual_compare/` | 4 KB | KEEP_LOCAL_ONLY | Comparison baseline; gitignored on infra branch |

All other benchmark_run dirs were deleted in v1 cleanup.

---

## E. Tracked-file deletion candidates (SAFE_TO_DELETE_TRACKED_VIA_COMMIT)

These satisfy all 9 strict criteria. None is referenced by any canonical
science/provenance/report file (only by each other or by tracked dev notes
also being deleted).

### Tier 1: Unreferenced development notes

| File | Rationale |
|---|---|
| `compute_legacy_exec_bridge_note_v1.md` | Bridge note; development history only |
| `next_step_runbook_CA1_BU3.md` | Runbook; all steps completed |
| `week1_manifest_runner_contract_v1.md` | v1 runner contract; superseded by v2 |
| `week1_replay_adapter_note.md` | Replay mode notes; approach abandoned |
| `week2_compute_parity_playbook.md` | Parity playbook; parity achieved |

### Tier 2: Unreferenced debugging/example scripts

| File | Rationale |
|---|---|
| `scan_rewritten_script_for_hardcodes.py` | One-shot debugging utility |
| `run_common_benchmark_example.sh` | Example script; runner v2 has own templates |
| `run_compute_legacy_example.sh` | Example script; superseded by v2 templates |
| `inspect_epi_bridge_failure.py` | Debugging helper; referenced only by week2 playbook (also deleted) |
| `epithelial_bridge_exec_debug_helper.py` | Debugging helper; referenced only by week2 playbook |
| `epithelial_only_remap_common_v2_integration_snippet.py` | Integration snippet; referenced only by week2 playbook |

### Tier 3: v1 runner/adapter/template code superseded by v2

| File | Rationale |
|---|---|
| `benchmark_common_runner_v1.py` | v1 runner; v2 is canonical; referenced only by week1 notes (also deleted) |
| `epithelial_only_remap_common_v1.py` | v1 adapter; v2 is canonical |
| `whole_lung_project_common_v1.py` | v1 adapter; v2 is canonical |
| `epithelial_cmd_template_replay_v1.txt` | Replay template; approach abandoned |
| `whole_lung_cmd_template_replay_v1.txt` | Replay template; approach abandoned |
| `legacy_output_manifest_v1.example.csv` | Example for replay mode; no longer needed |

### NOT deleting (REVIEW_NEEDED or referenced by canonical docs)

| File | Rationale |
|---|---|
| `epithelial_only_remap_v1.py` | Original CA1 biology script; structurally similar to BU3 but distinct; REVIEW_NEEDED |
| `epithelial_cmd_template_v1.txt` | Referenced by `references/drift/` (canonical) |
| `whole_lung_cmd_template_v1.txt` | Referenced by `references/drift/` (canonical) |
| `query_manifest_v1.example.csv` | Small; harmless; REVIEW_NEEDED |
| `check_exemplar_reproduction_v1.py` | Referenced by REFERENCE_PROVENANCE_v1.md (canonical) |
| `extract_reference_metadata_candidate_v1.py` | Referenced by REFERENCE_PROMOTION_CRITERIA_v1.md |
| `extract_reference_metadata_v1.py` | Referenced by provenance docs |
| `build_frozen_reference_v1.R` | Referenced by REFERENCE_PROVENANCE_AUDIT_v1.md |
| `build_reference_candidate_v1.R` | Referenced by REFERENCE_PROMOTION_CRITERIA_v1.md |
| `convert_to_h5ad.R` | Referenced by REFERENCE_PROVENANCE_v1.md |
| `run_reference_drift_report_v1.py` | Referenced by references/drift/ |

---

## F. Proposed .gitignore changes

Main's .gitignore is missing entries already added on the infra branch.
The cleanup branch should include these additions:

```gitignore
benchmark_run_gse237359_manual_compare/
queries/raw/
data/
objects/
rebuild_audit_v1/
qc_png/
roi_boxes/
codebook/xtab_*
config/
query_manifest_*_minimal_*.csv
mart_export*
```

No removals recommended.

---

## G. Exact commands (safe cleanup)

### G.1 Delete untracked files

```bash
rm append_gse237359_donors_to_manifest_v2.py ca1_diff_and_cleanup_playbook.md \
   claude_code_prompt_gse237359_intake_v1.md collect_projection_key_metrics_v2.py \
   collect_projection_key_metrics_v4.py gse237359_git_branch_runbook_v1.md \
   gse237359_github_integration_recommendation_v1.md \
   gse237359_inspect_and_split_pooled_scrna.py gse237359_inspect_and_split_pooled_scrna_v3.py \
   gse237359_organoid_query_sample_sheet_v1.tsv gse237359_projection_runbook_v1.md \
   gse237359_vs_CA1_BU3_canonical_compare_table_v1.tsv \
   gse237359_work_summary_and_github_boundary_v1.md handoff_parity_reached_2026-03-29.md \
   inspect_reference_h5seurat.R inspect_reference_rds.R lungs_analysisCLAUDE.md.txt \
   new_chat_seed_post_parity.txt riken_to_symbol.csv \
   whole_lung_bridge_hotfix_note_2026-04-03.md \
   whole_lung_forced_outdir_patch_instructions_2026-04-03.md \
   xenium_local_crop_from_raw.py xenium_local_crop_from_raw_v2.py \
   scripts/build_gse237359_projection_manifest.py scripts/collect_projection_metrics.py \
   scripts/gse237359_expand_sample_sheet_from_report.py
```

### G.2 Tracked cleanup branch (from main)

```bash
git checkout main && git pull --ff-only origin main
git checkout -b chore/repo_cleanup_v3
git rm benchmark_common_runner_v1.py epithelial_only_remap_common_v1.py \
      whole_lung_project_common_v1.py epithelial_cmd_template_replay_v1.txt \
      whole_lung_cmd_template_replay_v1.txt legacy_output_manifest_v1.example.csv \
      scan_rewritten_script_for_hardcodes.py run_common_benchmark_example.sh \
      run_compute_legacy_example.sh inspect_epi_bridge_failure.py \
      epithelial_bridge_exec_debug_helper.py \
      epithelial_only_remap_common_v2_integration_snippet.py \
      compute_legacy_exec_bridge_note_v1.md next_step_runbook_CA1_BU3.md \
      week1_manifest_runner_contract_v1.md week1_replay_adapter_note.md \
      week2_compute_parity_playbook.md
# + .gitignore update + cleanup summary
git commit -m "Prune obsolete tracked files after repository reconciliation v3"
```

---

## H. DO_NOT_TOUCH

- `converted/reference_metadata_v1.csv`
- `converted/reference_RNA.h5ad` (gitignored but canonical)
- `ORGANOID_QUERY_PROVENANCE_v1.md`
- `REFERENCE_PROVENANCE_v1.md`, `REFERENCE_PROVENANCE_AUDIT_v1.md`
- `REFERENCE_PROMOTION_CRITERIA_v1.md`, `REFERENCE_UPDATE_SYSTEM_v1.md`
- `metadata/organoid_data_inventory_v1.csv`
- `reports/` (all subdirectories)
- `queries/converted/gse237359/`
- `references/` (all subdirectories)
- `benchmark_common_runner_v2.py`, `whole_lung_project_common_v2.py`, `epithelial_only_remap_common_v2.py`
- `epithelial_only_remap_BU3_v1.py`, `project_BU3_to_reference_RNA_v1.py`
- `provenance_audit_h5ad.py`, `provenance_audit_v1_summary.json`
- `epithelial_cmd_template_compute_legacy_v1.txt`, `whole_lung_cmd_template_compute_legacy_v1.txt`
- `epithelial_cmd_template_v1.txt`, `whole_lung_cmd_template_v1.txt`
- `query_manifest_v1.csv`, `legacy_output_manifest_v1.csv`
- `codebook/codebook_*.csv` (tracked)
- `scripts/collect_projection_key_metrics_multiroot.py`
- All files referenced by canonical provenance/report docs
- Active branches: `infra/fix_whole_lung_combined_root_outdir`, `tranche/next_external_organoid_intake_v1`

---

## I. REVIEW_NEEDED

- 9 spatial pipeline scripts (untracked at root)
- `provenance_audit_h5ad_fixed.py`
- `query_manifest_v1_plus_gse237359.csv`
- `ref_sig_gw10_epi.csv`
- `metadata/external/gse237359_organoid_query_sample_sheet_v1.tsv`
- `metadata/external/gse221343_*` (tracked on intake branch only)
- `epithelial_only_remap_v1.py` (tracked; original CA1 biology script)
- `query_manifest_v1.example.csv` (tracked; small, harmless)
- `benchmark_run_gse237359_vs_CA1_BU3_compute/` (active run output)
