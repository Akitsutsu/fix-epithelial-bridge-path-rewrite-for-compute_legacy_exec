# AGENTS.md

## Read this first
Before changing code, metadata, or analysis state, read in this order:
1. `research_scope.md`
2. `data_contract.yaml`
3. `decision_log.md`
4. The closest path-specific instructions, if added later

## Purpose of this repository
This repo operates a reproducible human fetal lung reference projection system with explicit reference releases, benchmark anchors, and provenance-preserving external organoid intake.

## Canonical project facts
- Current operational reference release: `v1`
- Canonical reference pair:
  - `converted/reference_RNA.h5ad`
  - `converted/reference_metadata_v1.csv`
- Formal stage axis: `sample_week`
- Canonical anchor queries: `CA1`, `BU3`
- Canonical execution path: combined-root v2
- Spatial role: supportive evidence only

## Authoritative files for current operation
- `references/registry/current_release.yaml`
- `references/registry/REFERENCE_REGISTRY.csv`
- `query_manifest_v1.csv`
- `metadata/external/*_dataset_manifest_v*.yaml`
- `metadata/external/*_organoid_query_sample_sheet_v*.tsv`

## Canonical execution entrypoints
- `benchmark_common_runner_v2.py`
- `whole_lung_project_common_v2.py`
- `epithelial_only_remap_common_v2.py`
- `whole_lung_cmd_template_compute_legacy_v1.txt`
- `epithelial_cmd_template_compute_legacy_v1.txt`

## Working rules
- Do not overwrite release artifacts.
- Do not silently change the stage axis.
- Do not auto-promote candidate references.
- Do not set `query_ready_flag=true` from paper metadata alone.
- Do not treat CA1 / BU3 as a cohort.
- Do not treat spatial support as a replacement for reference semantics.
- Prefer minimal, reviewable edits over broad rewrites.

## When editing contracts or semantics
If a change affects any of the following, update both `data_contract.yaml` and `decision_log.md` in the same change:
- release identity or alias paths,
- stage axis,
- canonical runner / bridge entrypoints,
- enum values,
- query-ready promotion rules,
- external tranche status.

## Intake rules for external data
- Registration is allowed before conversion.
- Query readiness requires explicit local validation.
- Preserve provenance at every step: dataset -> sample -> donor split -> output object.
- Keep donor-resolved and pooled rows explicitly distinguishable.

## Review guidelines
- Flag silent contract drift as a high-priority issue.
- Flag any change that weakens provenance.
- Flag any change that edits release v1 artifacts in place.
- Flag any change that changes benchmark interpretation without a logged decision.
- Flag any sample promotion that lacks a validation trail.

## Preferred behavior for coding agents
- Start by summarizing the active contract before proposing structural edits.
- When the task is ambiguous, optimize for preserving current canonical behavior.
- When repeated confusion occurs, update this file or a path-specific instruction file so the lesson persists.

## Suggested future layering
- Keep this root file short.
- Add deeper `AGENTS.md` files only when a subtree has genuinely different rules.
- Put reusable workflows into skills or scripts, not into an oversized root instruction file.
