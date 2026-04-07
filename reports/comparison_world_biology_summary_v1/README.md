# Comparison world biology summary v1

## Date
2026-04-07

## Purpose
Cross-tranche biology summary of the current query-ready comparison world,
projected against release v1 (`converted/reference_RNA.h5ad` + `converted/reference_metadata_v1.csv`).

This is a reports-only artifact. No code, metadata, reference, manifests, or sample
sheets were modified.

## Scope
- 15 rows across 5 tranches (2 anchors + 4 GSE237359 donors + 3 GSE221343 + 3 GSE289846 + 3 GSE308817)
- All rows are query_ready_flag=true
- Values mirrored from existing review artifacts — no re-projection performed

## Tranches included

| Tranche | Role | Rows |
|---------|------|------|
| CA1 / BU3 | proximal_anchor | 2 |
| GSE237359 | donor_resolved_external_validation | 4 |
| GSE221343 | nearest_external_validation | 3 |
| GSE289846 | cross_lab_external_validation | 3 |
| GSE308817 | passage_series_external_validation | 3 |

## Files in this directory

| File | Description |
|------|-------------|
| `README.md` | This file |
| `comparison_world_biology_summary_v1.tsv` | Full 25-column 1-row-per-query summary table |
| `comparison_world_biology_summary_compact_v1.tsv` | Compact 12-column summary table |
| `comparison_world_biology_summary_v1.xlsx` | Excel workbook with both tables as sheets |
| `comparison_world_biology_narrative_memo_v1.md` | Narrative biology memo with interpretation and gap analysis |

## Data sourcing
- CA1 / BU3 / GSE237359: metrics from canonical multiroot compare table
  (`reports/tranches/gse237359_external_validation_v1/gse237359_vs_CA1_BU3_key_metrics_multiroot.tsv`)
- GSE221343 / GSE289846 / GSE308817: metrics from per-tranche query-ready decision TSVs
- Epi remap metrics for CA1/BU3/GSE237359 are NA (multiroot path did not produce decision TSVs)
- No values were inferred or re-computed; blanks are left as NA

## Key biological takeaways
1. CA1/BU3 define a **proximal anchor** at mid_GW14_16 / week_15 / Basal cells
2. GSE237359 defines a **distal benchmark** at late_GW17_19 / week_18 / Tip cells
3. GSE221343 demonstrates **condition-resolved biology** (iAT2 vs iAT1 differentiation)
4. GSE289846 confirms **cross-lab replication** of SOX2lowCFTR+ AT1-directed state
5. GSE308817 adds a **passage/maturation trajectory** (Budtip convergence then drift)
6. **SOX2lowCFTR+ cells** replicate across 2 labs (BU + Kyoto) as AT1-directed identity
7. All 15 rows are overwhelmingly **Epithelial** at coarse level (95–100%)
8. The world spans **4 labs, 3 stem cell backgrounds, 2 platforms**

## What is NOT in this summary
- Spatial evidence (Visium / Xenium) — excluded per scope
- Combined-root compute for GSE237359 — not yet canonical for that tranche
- Epi-remap decision-TSV-format metrics for anchors and GSE237359
- Any modification to data_contract.yaml, decision_log.md, or research_scope.md
