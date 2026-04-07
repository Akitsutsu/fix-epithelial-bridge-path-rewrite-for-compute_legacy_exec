# GSE193716 iAEC2 Subset Query-Ready Review v1

## Review date
2026-04-07

## Dataset
- GSE193716: primary adult AEC2s and iPSC-derived iAEC2s
- Kotton lab / Boston University / Center for Regenerative Medicine
- **This review covers the 3 iAEC2 rows only (subset promotion)**
- 4 primary AEC2 rows remain query_ready_flag=false

## Subset scope
| Row | Short | Culture format | Co-culture |
|-----|-------|---------------|------------|
| GSM5819133_iAEC2_3D | CG12 | 3D Matrigel alveolosphere | none (feeder-free) |
| GSM5819134_iAEC2_3D_insert | CG13 | 3D cell culture insert | none (feeder-free) |
| GSM5819135_iAEC2_MRC5_insert | CG14 | 3D cell culture insert | MRC5 fibroblasts |

All from SPC2-ST-B2 iPSC line (same as GSE221343), Day 114 differentiation,
CK+DCI medium, 10x Chromium, CellRanger v3.

## Reference
- Release v1: `converted/reference_RNA.h5ad` + `converted/reference_metadata_v1.csv`
- Stage axis: `sample_week`
- Execution: combined-root v2 canonical path
- Gene overlap: 26,975/30,852 (87.4%) — gap is lncRNA annotation drift

## Gate summary

### Gate A — Object contract
All 3 pass. H5AD loadable, raw present, counts layer present, X integer-valued,
87.4% reference gene overlap (26,975/30,852), obs/var columns intact,
modality = Gene Expression only. 32 duplicate gene symbols resolved via
var_names_make_unique.

### Gate B — Provenance / row identity
All 3 pass. Sample sheet row identity matches local objects. Source GSM IDs,
output paths, conversion script all consistent. Same iPSC line (SPC2-ST-B2)
and differentiation protocol as GSE221343.

### Gate C — Projection smoke test
All 3 pass. Whole-lung and epithelial projections completed without errors.

| Row | WL cells | WL Epithelial% | WL top stage | Epi eligible | Epi off-target% |
|-----|------:|---:|---|------:|---:|
| GSM5819133_iAEC2_3D | 2,982 | 99.1% | late_GW17_19 | 2,955 | 0.9% |
| GSM5819134_iAEC2_3D_insert | 2,068 | 98.5% | late_GW17_19 | 2,038 | 1.5% |
| GSM5819135_iAEC2_MRC5_insert | 2,232 | 97.9% | late_GW17_19 | 2,185 | 2.1% |

### Gate D — Within-tranche biology coherence
All 3 pass.

Key observations:
- All 3 project to **Proliferating progenitors** as top epithelial state_fine
- All 3 map to **late_GW17_19 / week_18** — same stage as GSE221343 and
  most of GSE289846
- **Culture format produces graded resolution**:
  - 3D/insert (CG13): best alignment (0.814), lowest ambiguity (9.9%),
    Prolif. progenitors at 50.9%
  - +MRC5/insert (CG14): near-equivalent alignment (0.819), moderate
    ambiguity (15.7%), highest Prolif. progenitors fraction (65.9%)
  - 3D Matrigel (CG12): lower alignment (0.690), higher ambiguity (31.0%),
    Prolif. progenitors at 31.1%
- +MRC5 co-culture effect on iAEC2 is minimal (epi off-target 2.1% vs
  0.9–1.5% feeder-free) — contrast with primary cultured samples where
  MRC5 effect is substantial (10–16% off-target)
- **Proliferating progenitors replicates cross-dataset**: matches
  GSE289846 3i_Day7 (Kyoto, B2-3 line) — independent lab, line, protocol

Comparison with same-line GSE221343 (SPC2-ST-B2):
- GSE221343 CK+DCI iAT2 → Stromal-like cells 1 (25.9%)
- GSE193716 iAEC2 3D → Proliferating progenitors (30.9%)
- Different state_fine for the same iPSC line in different culture format.
  This is interpretable: GSE221343 uses 3D Matrigel alveolosphere after
  longer expansion; GSE193716 is Day 114 directed differentiation in
  varied formats.

## Decisions

| Row | Decision | Rationale |
|-----|----------|-----------|
| GSM5819133_iAEC2_3D | **promote** | feeder-free 3D Matrigel baseline; near-pure epithelial; cross-dataset Prolif. progenitor replication; culture-format baseline for insert and +MRC5 comparison |
| GSM5819134_iAEC2_3D_insert | **promote** | strongest row in tranche; best alignment of any external tranche row; lowest ambiguity; most resolved culture format |
| GSM5819135_iAEC2_MRC5_insert | **promote** | highest Prolif. progenitors fraction; MRC5 effect minimal; adds unique co-culture comparison value |

**Subset-level decision**: 3 iAEC2 rows promoted → dataset-level
`query_ready_flag` remains **false** (because 4 primary rows are not
promoted). Dataset-level `status` set to `accepted_iAEC2_subset_query_ready`.

## What this review is NOT based on
- Similarity to CA1/BU3 — interpretability on v1 is the criterion
- Paper expectations alone — projections evaluated independently
- Automated thresholds — explicit reviewer decision
- All-7 promotion — primary rows excluded by design (adult-primary caveat)

## Rows NOT promoted (primary AEC2, 4 rows)
| Row | Status | Reason |
|-----|--------|--------|
| GSM5819131_primary_preculture_PL2 | hold_pending_biological_review | adult-primary-vs-fetal Budtip interpretation unresolved |
| GSM5819132_primary_preculture_PL1 | hold_pending_biological_review | adult-primary-vs-fetal Budtip interpretation unresolved |
| GSM5819129_primary_cultured_PL2 | not_recommended_now | epi off-target 15.6%; MRC5 culture confound |
| GSM5819130_primary_cultured_PL1 | not_recommended_now | epi off-target 9.9%; MRC5 culture confound |

These remain `query_ready_flag=false` and can be reconsidered after
domain-expert input on the adult-primary-vs-fetal mapping question.

## Artifacts
- `gse193716_iAEC2_subset_decisions_v1.tsv` — machine-readable decision table
- `benchmark_review_gse193716_v1/` — local projection run outputs (not committed)
