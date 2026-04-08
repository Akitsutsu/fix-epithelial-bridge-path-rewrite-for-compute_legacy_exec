# Comparison world biology summary v3

## Date
2026-04-08

## Supersedes
`reports/comparison_world_biology_summary_v2/` (18 rows, 6 tranches).
v2 is retained as a historical snapshot and is not deleted.

## Purpose
Cross-tranche biology summary of the current query-ready comparison world
after GSE221344 paired promotion (D-0014).

This is a reports-only artifact. No code, metadata, reference, manifests, or
sample sheets were modified.

## Scope
- **20 rows** across **7 tranche components**
- 2 anchors (CA1, BU3)
- 4 GSE237359 donor-resolved rows
- 3 GSE221343 condition rows
- 3 GSE289846 condition rows
- 3 GSE308817 passage rows
- 3 GSE193716 iAEC2 rows
- **2 GSE221344 paired perturbation rows** (new in v3)
- All rows are query_ready_flag=true
- Values mirrored from existing review artifacts -- no re-projection performed

## What changed from v2

| Change | v2 | v3 |
|--------|----|----|
| Total rows | 18 | 20 |
| Tranche components | 6 | 7 |
| GSE221344 | not included | 2 rows (WT-YAP + YAP5SA paired) |
| Proliferating progenitors tranches | 2 (GSE289846, GSE193716) | 3 (+GSE221344) |
| P-0001 evidence | basis only | basis + supportive positive arm |

## Tranches included

| Tranche | Role | Rows | Decision |
|---------|------|------|----------|
| CA1 / BU3 | proximal_anchor | 2 | -- |
| GSE237359 | donor_resolved_external_validation | 4 | D-0007 |
| GSE221343 | nearest_external_validation | 3 | D-0010 |
| GSE289846 | cross_lab_external_validation | 3 | D-0011 |
| GSE308817 | passage_series_external_validation | 3 | D-0012 |
| GSE193716 (iAEC2 subset) | nearest_external_validation | 3 | D-0013 |
| GSE221344 | nearest_external_validation | 2 | D-0014 |

## Files in this directory

| File | Description |
|------|-------------|
| `README.md` | This file |
| `comparison_world_biology_summary_v3.tsv` | Full 25-column 1-row-per-query summary table (20 rows) |
| `comparison_world_biology_summary_compact_v3.tsv` | Compact 12-column summary table (20 rows) |
| `comparison_world_biology_summary_v3.xlsx` | Excel workbook with both tables as sheets |
| `comparison_world_biology_narrative_memo_v3.md` | Narrative biology memo with v2->v3 delta |
| `comparison_world_state_by_tranche_v3.tsv` | State-by-tranche cross-reference matrix (7 states x 7 components) |

## Data sourcing
- All v2 rows: mirrored unchanged from v2
- GSE221344: mirrored from `gse221344_query_ready_decisions_v1.tsv`
  and `gse221344_projection_review_v1.tsv`
- No values were re-computed

## Key biological takeaways (updated from v2)
1. CA1/BU3 = proximal anchor at mid_GW14_16 / Basal cells
2. GSE237359 = distal benchmark at late_GW17_19 / Tip cells
3. GSE221343 = condition-resolved biology (iAT2 vs iAT1)
4. GSE289846 = cross-lab differentiation / transitional axis
5. GSE308817 = passage / maturation trajectory
6. GSE193716 iAEC2 = same-line culture-format comparison axis
7. **GSE221344 = same-line paired positive-arm perturbation axis** (new)
8. SOX2lowCFTR+ replicates cross-lab (BU + Kyoto)
9. Proliferating progenitors now in 3 tranches (GSE289846, GSE193716, GSE221344)
10. **YAP5SA shows directional CFTR+ enrichment, supportive of P-0001**
11. **P-0001 remains registered/supportive, not confirmed**
12. All 20 rows are overwhelmingly Epithelial at coarse level (84-100%)
13. The world spans 4 labs, 3 stem cell backgrounds, 2 platforms

## What is NOT in this summary
- GSE193716 primary AEC2 rows (4 held, not query-ready)
- Spatial evidence
- Combined-root compute for GSE237359
- Epi-remap decision-TSV-format metrics for anchors and GSE237359
- P-0001 cross-tranche closure assessment
