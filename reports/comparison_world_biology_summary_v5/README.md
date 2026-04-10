# Comparison world biology summary v5

## Date
2026-04-10

## Supersedes
`reports/comparison_world_biology_summary_v4/` (24 rows, 8 tranches).
v4 is retained as a historical snapshot and is not deleted.

## Purpose
Cross-tranche biology summary of the current query-ready comparison world
after GSE246243 same-line kinetic tranche promotion.

This is a reports-only artifact. No code, metadata, reference, manifests, or
sample sheets were modified.

## Scope
- **28 rows** across **9 tranche components**
- 2 anchors (CA1, BU3)
- 4 GSE237359 donor-resolved rows
- 3 GSE221343 condition rows
- 3 GSE289846 condition rows
- 3 GSE308817 passage rows
- 3 GSE193716 iAEC2 rows
- 2 GSE221344 paired perturbation rows
- 4 GSE221342 boundary-stress differentiation rows
- **4 GSE246243 same-line kinetic rows** (new in v5)
- All rows are query_ready_flag=true
- Values mirrored from existing review artifacts -- no re-projection performed

## What changed from v4

| Change | v4 | v5 |
|--------|----|----|
| Total rows | 24 | 28 |
| Tranche components | 8 | 9 |
| GSE246243 | not included | 4 rows (iAT2 t=0, iAT1 24hr, iAT1 48hr, iAT1 72hr) |
| SOX2lowCFTR+ tranches | 3 (GSE221343, GSE289846, GSE221342) | 4 (+GSE246243 72hr) |
| Proliferating progenitors tranches | 3 (GSE289846, GSE193716, GSE221344) | 4 (+GSE246243 t=0/24hr/48hr) |
| Kinetic axis | not represented | GSE246243 4-point L+DCI time series |

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
| GSE221342 | nearest_external_validation | 4 | accepted_query_ready |
| **GSE246243** | **nearest_external_validation** | **4** | **accepted_query_ready** |

## Data sourcing
- All v4 rows: mirrored unchanged from v4
- GSE246243: mirrored from `gse246243_query_ready_decisions_v1.tsv`
  and `reports/tranches/gse246243_query_ready_review_v1/README.md`
- No values were re-computed

## Key biological takeaways (updated from v4)
1. CA1/BU3 = proximal anchor at mid_GW14_16 / Basal cells
2. GSE237359 = distal benchmark at late_GW17_19 / Tip cells
3. GSE221343 = condition-resolved biology (iAT2 vs iAT1)
4. GSE289846 = cross-lab differentiation / transitional axis
5. GSE308817 = passage / maturation trajectory
6. GSE193716 iAEC2 = same-line culture-format comparison axis
7. GSE221344 = same-line paired positive-arm perturbation axis
8. GSE221342 = boundary-stress / directional gradient tranche
9. **GSE246243 = same-line kinetic strengthening tranche** (new)
10. **First kinetic tranche** in the current comparison world
11. **Same BU3 NGAT line** as BU3 anchor and GSE221342
12. **Kinetic progression**: Proliferating progenitors → SOX2lowCFTR+ at 72hr
13. Strengthens commitment-level directional support for P-0002
14. SOX2lowCFTR+ now replicates across 3 lines, 2 labs, with kinetic confirmation
15. P-0001 remains registered/supportive, not confirmed
16. **GSE246243 is NOT a same-line P-0001 validation tranche** (BU3 NGAT ≠ SPC2-ST-B2)
17. **GSE246243 is NOT full alveolarization evidence** (72hr is early kinetic)
18. All 28 rows are overwhelmingly Epithelial at coarse level (84-100%)
19. The world spans 4 labs, 4 stem cell backgrounds, 2 platforms

## What is NOT in this summary
- GSE193716 primary AEC2 rows (4 held, not query-ready)
- Spatial evidence
- Combined-root compute for GSE237359
- P-0001 cross-tranche closure assessment
- Full alveolarization closure

## Files in this directory

| File | Description |
|------|-------------|
| `README.md` | This file |
| `comparison_world_biology_summary_v5.tsv` | Full 25-column 1-row-per-query summary table (28 rows) |
| `comparison_world_biology_summary_compact_v5.tsv` | Compact 12-column summary table (28 rows) |
| `comparison_world_biology_summary_v5.xlsx` | Excel workbook with both tables as sheets |
| `comparison_world_biology_narrative_memo_v5.md` | Narrative biology memo with v4->v5 delta |
| `comparison_world_state_by_tranche_v5.tsv` | State-by-tranche cross-reference matrix (7 states x 9 components) |
