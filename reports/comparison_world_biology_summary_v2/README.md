# Comparison world biology summary v2

## Date
2026-04-07

## Supersedes
`reports/comparison_world_biology_summary_v1/` (15 rows, 5 tranches).
v1 is retained as a historical snapshot and is not deleted.

## Purpose
Cross-tranche biology summary of the current query-ready comparison world
after GSE193716 iAEC2 subset promotion (D-0013, PR #35).

This is a reports-only artifact. No code, metadata, reference, manifests, or
sample sheets were modified.

## Scope
- **18 rows** across **6 tranche components**
- 2 anchors (CA1, BU3)
- 4 GSE237359 donor-resolved rows
- 3 GSE221343 condition rows
- 3 GSE289846 condition rows
- 3 GSE308817 passage rows
- **3 GSE193716 iAEC2 rows** (new in v2)
- All rows are query_ready_flag=true
- Values mirrored from existing review artifacts — no re-projection performed

## What changed from v1

| Change | v1 | v2 |
|--------|----|----|
| Total rows | 15 | 18 |
| Tranche components | 5 | 6 |
| GSE193716 | not included | 3 iAEC2 rows (subset) |
| Cross-dataset Prolif. progenitors | GSE289846 only | GSE289846 + GSE193716 |

## Tranches included

| Tranche | Role | Rows | Decision |
|---------|------|------|----------|
| CA1 / BU3 | proximal_anchor | 2 | — |
| GSE237359 | donor_resolved_external_validation | 4 | D-0007 |
| GSE221343 | nearest_external_validation | 3 | D-0010 |
| GSE289846 | cross_lab_external_validation | 3 | D-0011 |
| GSE308817 | passage_series_external_validation | 3 | D-0012 |
| GSE193716 (iAEC2 subset) | nearest_external_validation | 3 | D-0013 |

## Files in this directory

| File | Description |
|------|-------------|
| `README.md` | This file |
| `comparison_world_biology_summary_v2.tsv` | Full 25-column 1-row-per-query summary table (18 rows) |
| `comparison_world_biology_summary_compact_v2.tsv` | Compact 12-column summary table (18 rows) |
| `comparison_world_biology_summary_v2.xlsx` | Excel workbook with both tables as sheets |
| `comparison_world_biology_narrative_memo_v2.md` | Narrative biology memo with v1→v2 delta |
| `comparison_world_state_by_tranche_v2.tsv` | State-by-tranche cross-reference matrix (7 states x 6 components) |

## Data sourcing
- CA1 / BU3 / GSE237359: mirrored from v1 (multiroot compare table)
- GSE221343 / GSE289846 / GSE308817: mirrored from v1 (decision TSVs)
- GSE193716 iAEC2: mirrored from `gse193716_iAEC2_subset_decisions_v1.tsv`
  and `gse193716_projection_review_v1.tsv`
- No values were re-computed

## Key biological takeaways (updated from v1)
1. CA1/BU3 = proximal anchor at mid_GW14_16 / Basal cells
2. GSE237359 = distal benchmark at late_GW17_19 / Tip cells
3. GSE221343 = condition-resolved biology (iAT2 vs iAT1)
4. GSE289846 = cross-lab differentiation / transitional axis
5. GSE308817 = passage / maturation trajectory
6. **GSE193716 iAEC2 = same-line culture-format comparison axis** (new)
7. SOX2lowCFTR+ replicates cross-lab (BU + Kyoto)
8. **Proliferating progenitors now replicates cross-dataset** (GSE289846 + GSE193716)
9. All 18 rows are overwhelmingly Epithelial at coarse level (84–100%)
10. The world spans 4 labs, 3 stem cell backgrounds, 2 platforms

## What is NOT in this summary
- GSE193716 primary AEC2 rows (4 held, not query-ready)
- Spatial evidence
- Combined-root compute for GSE237359
- Epi-remap decision-TSV-format metrics for anchors and GSE237359
