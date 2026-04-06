# GSE308817 Query-Ready Review v1

## Review date
2026-04-06

## Dataset
- GSE308817: hESC-derived alveolar organoids at 3 passage timepoints
- Liu/Rong lab / Xiamen University
- 3 GSM-level rows, H9 hESC wild type, SeekOne library prep
- Citation missing on GEO (no PMID/DOI as of 2025-12-22)

## Reference
- Release v1: `converted/reference_RNA.h5ad` + `converted/reference_metadata_v1.csv`
- Stage axis: `sample_week`
- Execution: combined-root v2 canonical path

## Gate summary

### Gate A — Object contract
All 3 pass. H5AD loadable, raw present, counts layer present, X integer-valued,
100.0% reference gene overlap (30,843/30,852), obs/var columns intact,
modality = Gene Expression only. SeekOne gene-space confirmed compatible.

### Gate B — Provenance / row identity
All 3 pass. Sample sheet row identity matches local objects. Source GSM IDs,
output paths, conversion script all consistent. Citation missing is recorded
in provenance notes and does not block promotion.

### Gate C — Projection smoke test
All 3 pass. Whole-lung and epithelial projections completed without errors
despite larger cell counts (10–18k per sample vs 1–5k in prior tranches).

| Row | WL cells | WL Epithelial% | WL top stage | Epi eligible | Epi off-target% |
|-----|------:|---:|---|------:|---:|
| GSE308817_ALOp3 | 18,218 | 97.9% | early_GW10_13 | 17,831 | 2.1% |
| GSE308817_ALOp7 | 10,569 | 99.9% | early_GW10_13 | 10,559 | 0.1% |
| GSE308817_ALOp20 | 17,029 | 99.9% | early_GW10_13 | 17,015 | 0.1% |

### Gate D — Within-tranche biology coherence
All 3 pass. Passage trajectory is interpretable on v1.

Key observations:
- All 3 map primarily to Budtip progenitors in epithelial state_fine
- **P3 → P7**: Organoids converge — Budtip fraction rises (44→48%),
  ambiguity drops (50→30%), alignment improves. P7 is the most resolved sample.
- **P7 → P20**: Extended passage causes drift — Budtip drops to 24%,
  week_19 emerges as top stage_fine (39%), ambiguity rises (47%).
  This is readable as passage-dependent maturation.
- No extreme outlier — graded passage progression across all metrics
- Stage diversification from early_GW10_13/week_11 dominance (P3) toward
  mixed early+late representation (P20) is biologically coherent

Notes on cross-tranche comparison:
- Lower alignment scores (0.48–0.55) than GSE289846 (0.62–0.76) or
  GSE221343 (0.62–0.67). This reflects cross-lab, cross-platform
  (SeekOne vs 10x), and cross-stem-cell-background (hESC H9 vs iPSC)
  variation, not a pipeline failure.
- Higher ambiguity (30–50%) than GSE289846 (18–35%) — expected for
  Budtip progenitors which occupy a less committed reference niche.
- These are interpretable differences, not promotion blockers.

## Decisions

| Row | Decision | Rationale |
|-----|----------|-----------|
| GSE308817_ALOp3 | **promote** | Early passage baseline; strong Budtip identity; interpretable on v1 |
| GSE308817_ALOp7 | **promote** | Optimal expansion state; best alignment/lowest ambiguity in tranche |
| GSE308817_ALOp20 | **promote** | Late passage drift readable as maturation; stage diversification interpretable |

**Dataset-level decision**: All 3 rows promoted → dataset-level `query_ready_flag=true`.

## What this review is NOT based on
- Paper expectations — citation is missing; projections evaluated independently
- Similarity to CA1/BU3 — Budtip progenitor identity differs from anchor states
- Similarity to GSE221343/GSE289846 — cross-lab difference is expected
- Platform match — SeekOne compatibility confirmed by 100% gene overlap
- Automated thresholds — explicit reviewer decision

## Artifacts
- `gse308817_query_ready_decisions_v1.tsv` — machine-readable decision table
- `benchmark_review_gse308817_v1/` — temporary projection run outputs (not committed)
