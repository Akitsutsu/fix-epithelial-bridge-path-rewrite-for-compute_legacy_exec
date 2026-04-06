# GSE221343 Query-Ready Review v1

## Review date
2026-04-06

## Dataset
- GSE221343: iPSC-derived alveolar epithelial organoids (iAT2 / iAT1)
- Kotton lab / Boston University / Center for Regenerative Medicine
- 3 samples, single donor cell line SPC2-ST-B2, no multiplexing

## Reference
- Release v1: `converted/reference_RNA.h5ad` + `converted/reference_metadata_v1.csv`
- Stage axis: `sample_week`
- Execution: combined-root v2 canonical path

## Review scope
Explicit reviewer promotion decision for 3 rows previously at
`qc_status=local_validation_inspected_manual_review_required`,
`query_ready_flag=false`.

## Gate summary

### Gate A — Object contract
All 3 pass. H5AD loadable, raw present, counts layer present, X integer-valued,
92.0% reference gene overlap, obs/var columns intact, modality = Gene Expression.

### Gate B — Provenance / row identity
All 3 pass. Sample sheet row identity matches local objects. Source accession,
sample name, output paths, conversion script, cell counts all consistent.
Single donor cell line — no demultiplexing needed.

### Gate C — Projection smoke test
All 3 pass. Whole-lung and epithelial projections completed without errors
using canonical combined-root v2 path against current release v1.

| Sample | WL cells | WL Epithelial% | WL top stage | Epi eligible | Epi off-target% |
|--------|------:|---:|---|------:|---:|
| GSM6858854_CK_DCI | 1,365 | 95.3% | late_GW17_19 | 1,301 | 4.7% |
| GSM6858855_YAP5SA_CK_DCI | 2,628 | 97.9% | late_GW17_19 | 2,573 | 2.1% |
| GSM6858856_L_DCI | 4,748 | 99.2% | late_GW17_19 | 4,710 | 0.8% |

### Gate D — Within-tranche biology coherence
All 3 pass.

Key observations:
- All 3 project overwhelmingly to Epithelial at coarse level (95–99%)
- All 3 map to late_GW17_19 / week_18 stage — consistent temporal placement
- iAT2 samples (CK+DCI, YAP5SA) share top_state_fine (Stromal-like cells 1)
- iAT1 differentiation (L+DCI) shows distinct top_state_fine (SOX2lowCFTR+ cells)
- Condition difference between iAT2 baseline and iAT1 differentiation is clearly readable
- YAP5SA perturbation projects similarly to baseline — perturbation effect is subtle, not identity-breaking
- No extreme outlier; graded variation across conditions
- Within-tranche comparison is interpretable on current release v1

Note: "Stromal-like cells 1" as a state_fine label for epithelial organoids may seem
counterintuitive but reflects reference label mapping, not actual stromal identity.
The key is that (a) coarse state is overwhelmingly Epithelial, (b) condition differences
are visible within the epithelial remap, and (c) the tranche is internally coherent.

## Decisions

| Sample | Decision | Rationale |
|--------|----------|-----------|
| GSM6858854_CK_DCI | **promote** | iAT2 control baseline; strong epithelial identity; interpretable on v1 |
| GSM6858855_YAP5SA_CK_DCI | **promote** | iAT2 + YAP5SA; similar to baseline; perturbation readable as relative shift |
| GSM6858856_L_DCI | **promote** | iAT1 differentiation; distinct state; condition difference clearly visible |

**Dataset-level decision**: All 3 rows promoted → dataset-level `query_ready_flag=true`.

## What this review is NOT based on
- Paper expectations alone — projections were run and evaluated independently
- Similarity to CA1/BU3 — the question is whether these rows are interpretable on v1, not whether they look like the anchor queries
- Automated thresholds — this is an explicit reviewer decision

## Artifacts
- `gse221343_query_ready_decisions_v1.tsv` — machine-readable decision table
- `benchmark_review_gse221343_v1/` — temporary projection run outputs (not committed)
