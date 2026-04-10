# Comparison world biology summary v4

## Date
2026-04-10

## Supersedes
`reports/comparison_world_biology_summary_v3/` (20 rows, 7 tranches).
v3 is retained as a historical snapshot and is not deleted.

## Purpose
Cross-tranche biology summary of the current query-ready comparison world
after GSE221342 boundary-stress tranche promotion.

This is a reports-only artifact. No code, metadata, reference, manifests, or
sample sheets were modified.

## Scope
- **24 rows** across **8 tranche components**
- 2 anchors (CA1, BU3)
- 4 GSE237359 donor-resolved rows
- 3 GSE221343 condition rows
- 3 GSE289846 condition rows
- 3 GSE308817 passage rows
- 3 GSE193716 iAEC2 rows
- 2 GSE221344 paired perturbation rows
- **4 GSE221342 boundary-stress differentiation rows** (new in v4)
- All rows are query_ready_flag=true
- Values mirrored from existing review artifacts -- no re-projection performed

## What changed from v3

| Change | v3 | v4 |
|--------|----|----|
| Total rows | 20 | 24 |
| Tranche components | 7 | 8 |
| GSE221342 | not included | 4 rows (iAT2 3D + iAT1 3D + iAT1 ALI p0 + ALI p1) |
| SOX2lowCFTR+ tranches | 2 (GSE221343, GSE289846) | 3 (+GSE221342) |
| Budtip progenitors tranches | 1 (GSE308817) | 2 (+GSE221342 iAT2 baseline) |
| mid_GW14_16 sources | anchors only (CA1/BU3) | anchors + GSE221342 iAT2_3D (first external) |
| ALI culture format | not represented | GSE221342 iAT1 ALI p0 + p1 |

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
| **GSE221342** | **nearest_external_validation** | **4** | **accepted_query_ready** |

## Data sourcing
- All v3 rows: mirrored unchanged from v3
- GSE221342: mirrored from `gse221342_query_ready_decisions_v1.tsv`
  and `reports/tranches/gse221342_query_ready_review_v1/README.md`
- CA1, BU3, GSE237359 (6 rows): epithelial columns from
  `reports/repo_state/legacy_metric_backfill_pilot_v1.tsv`
- No values were re-computed

## Key biological takeaways (updated from v3)
1. CA1/BU3 = proximal anchor at mid_GW14_16 / Basal cells
2. GSE237359 = distal benchmark at late_GW17_19 / Tip cells
3. GSE221343 = condition-resolved biology (iAT2 vs iAT1)
4. GSE289846 = cross-lab differentiation / transitional axis
5. GSE308817 = passage / maturation trajectory
6. GSE193716 iAEC2 = same-line culture-format comparison axis
7. GSE221344 = same-line paired positive-arm perturbation axis
8. **GSE221342 = boundary-stress / directional gradient tranche** (new)
9. SOX2lowCFTR+ replicates cross-lab (BU SPC2-ST-B2 + Kyoto B2-3 + **BU BU3-NGAT**)
10. Proliferating progenitors in 3 tranches (GSE289846, GSE193716, GSE221344)
11. **First external mid_GW14_16 row** (GSE221342 iAT2_3D) breaks anchor-only coverage
12. **ALI culture format now readable** on v1 reference (GSE221342 ALI p0/p1)
13. **Budtip progenitors now in 2 tranches** (GSE308817 + GSE221342 iAT2 baseline)
14. P-0001 remains registered/supportive, not confirmed
15. **GSE221342 is NOT a same-line P-0001 validation tranche** (BU3 NGAT ≠ SPC2-ST-B2)
16. All 24 rows are overwhelmingly Epithelial at coarse level (84-100%)
17. The world spans 4 labs, 4 stem cell backgrounds, 2 platforms

## What is NOT in this summary
- GSE193716 primary AEC2 rows (4 held, not query-ready)
- Spatial evidence
- Combined-root compute for GSE237359
- P-0001 cross-tranche closure assessment
- P-0002 formal registration

## Files in this directory

| File | Description |
|------|-------------|
| `README.md` | This file |
| `comparison_world_biology_summary_v4.tsv` | Full 25-column 1-row-per-query summary table (24 rows) |
| `comparison_world_biology_summary_compact_v4.tsv` | Compact 12-column summary table (24 rows) |
| `comparison_world_biology_summary_v4.xlsx` | Excel workbook with both tables as sheets |
| `comparison_world_biology_narrative_memo_v4.md` | Narrative biology memo with v3->v4 delta |
| `comparison_world_state_by_tranche_v4.tsv` | State-by-tranche cross-reference matrix (7 states x 8 components) |
