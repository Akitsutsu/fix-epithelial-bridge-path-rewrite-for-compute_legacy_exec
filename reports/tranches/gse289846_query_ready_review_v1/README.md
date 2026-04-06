# GSE289846 Query-Ready Review v1

## Review date
2026-04-06

## Dataset
- GSE289846: iPSC-derived alveolar epithelial organoids on micro-patterned plates
- Gotoh lab / CiRA, Kyoto University
- 3 condition-level rows (each merging 2 biological replicates), iPSC line B2-3

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
100.0% reference gene overlap (30,843/30,852), obs/var columns intact,
modality = Gene Expression only.

### Gate B — Provenance / row identity
All 3 pass. Sample sheet row identity matches local objects. Source accession,
source sample IDs, output paths, conversion script all consistent.
Condition-level registry units with replicate GSM provenance in notes.

### Gate C — Projection smoke test
All 3 pass. Whole-lung and epithelial projections completed without errors.

| Row | WL cells | WL Epithelial% | WL top stage | Epi eligible | Epi off-target% |
|-----|------:|---:|---|------:|---:|
| GSE289846_3i_Day7 | 3,576 | 99.3% | late_GW17_19 | 3,551 | 0.7% |
| GSE289846_3i_LATS_Day14 | 3,742 | 99.9% | late_GW17_19 | 3,738 | 0.1% |
| GSE289846_3i_PAL_Day14 | 4,147 | 99.9% | early_GW10_13 | 4,142 | 0.1% |

### Gate D — Within-tranche biology coherence
All 3 pass.

Key observations:
- All 3 project near-purely to Epithelial (99.3–99.9%) with off-target < 1%
- Each condition maps to a distinct epithelial state_fine:
  - **3i_Day7** → Proliferating progenitors (30.8%) — progenitor baseline
  - **3i_LATS_Day14** → SOX2lowCFTR+ cells (31.8%) — AT1-directed state
  - **3i_PAL_Day14** → PNEC (42.8%) — transitional/neuroendocrine state
- PAL transitional maps to an earlier stage (early_GW10_13/week_13) compared to
  baseline/LATS (late_GW17_19/week_18) — consistent with a less committed transitional identity
- Ambiguity decreases from baseline (35%) to transitional (18%) — PAL condition
  is the most resolved within the epithelial remap
- No outlier — 3 conditions form a coherent within-tranche comparison

Comparison to GSE221343 tranche:
- GSE289846 has higher epithelial purity (99%+ vs 95–99%)
- GSE289846 has lower off-target (0.1–0.7% vs 0.8–4.7%)
- GSE289846 shows a stage shift between conditions (PAL → earlier stage),
  while GSE221343 conditions all mapped to the same stage
- Different iPSC line (B2-3 vs SPC2-ST-B2) and protocol confirm cross-lab
  replication of the reference's ability to resolve condition differences

## Decisions

| Row | Decision | Rationale |
|-----|----------|-----------|
| GSE289846_3i_Day7 | **promote** | iAT2 baseline; near-pure epithelial; progenitor state interpretable on v1 |
| GSE289846_3i_LATS_Day14 | **promote** | AT1 induction; distinct SOX2lowCFTR+ state; near-zero off-target |
| GSE289846_3i_PAL_Day14 | **promote** | Transitional; distinct PNEC state + stage shift; most resolved condition |

**Dataset-level decision**: All 3 rows promoted → dataset-level `query_ready_flag=true`.

## What this review is NOT based on
- Paper expectations alone — projections were run and evaluated independently
- Similarity to CA1/BU3 — interpretability on v1 is the criterion
- Similarity to GSE221343 — cross-lab difference is expected and valuable
- Automated thresholds — explicit reviewer decision

## Artifacts
- `gse289846_query_ready_decisions_v1.tsv` — machine-readable decision table
- `benchmark_review_gse289846_v1/` — temporary projection run outputs (not committed)
