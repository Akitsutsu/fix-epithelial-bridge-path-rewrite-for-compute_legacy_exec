# GSE193716 Projection Review v1

## Review date
2026-04-07

## Dataset
- GSE193716: primary adult AEC2s (freshly isolated + cultured) and iPSC-derived iAEC2s
- Kotton lab / Boston University / Center for Regenerative Medicine
- 7 GSM-level rows: 2 primary pre-culture, 2 primary cultured, 3 iAEC2 conditions
- iPSC line: SPC2-ST-B2 (same as GSE221343)
- CellRanger reference: GRCh38_tdtomato_10X
- Reference overlap: 26,975/30,852 (87.4%)

## Reference
- Release v1: `converted/reference_RNA.h5ad` + `converted/reference_metadata_v1.csv`
- Stage axis: `sample_week`
- Execution: combined-root v2 canonical path

## Review scope
First-pass projection review for 7 rows at
`qc_status=local_validation_inspected_manual_review_required`,
`query_ready_flag=false`. This review covers whole-lung and epithelial
projection. **No query-ready promotion decision is made in this review.**

## Inputs
- 7 local H5AD files (`queries/converted/gse193716/*.h5ad`)
- Registration manifest and sample sheet
- Gene-space audit (`reports/tranches/gse193716_registration_audit_v1/`)
- Conversion report (`reports/tranches/gse193716_conversion_v1/`)

## Gate C — Projection smoke test

All 7 pass. Whole-lung and epithelial projections completed without errors
using canonical combined-root v2 path against current release v1.

| Sample | WL cells | WL Epithelial% | WL top stage | WL top state_fine | Epi eligible | Epi off-target% | Epi ambiguity% |
|--------|------:|---:|---|---|------:|---:|---:|
| GSM5819131 pre-culture PL2 | 1,148 | 94.3% | late_GW17_19 | Budtip progenitors (52.2%) | 1,083 | 5.7% | 32.8% |
| GSM5819132 pre-culture PL1 | 879 | 95.6% | late_GW17_19 | Budtip progenitors (63.1%) | 840 | 4.4% | 22.4% |
| GSM5819129 cultured PL2 | 1,439 | 84.4% | late_GW17_19 | Tip cells (32.9%) | 1,215 | 15.6% | 21.3% |
| GSM5819130 cultured PL1 | 2,097 | 90.1% | late_GW17_19 | Budtip progenitors (33.0%) | 1,890 | 9.9% | 19.6% |
| GSM5819133 iAEC2 3D | 2,982 | 99.1% | late_GW17_19 | Prolif. progenitors (30.9%) | 2,955 | 0.9% | 31.0% |
| GSM5819134 iAEC2 3D/insert | 2,068 | 98.5% | late_GW17_19 | Prolif. progenitors (50.2%) | 2,038 | 1.5% | 9.9% |
| GSM5819135 iAEC2 +MRC5/insert | 2,232 | 97.9% | late_GW17_19 | Prolif. progenitors (32.1%) | 2,185 | 2.1% | 15.7% |

## Gate D — Within-tranche biology coherence

### Primary pre-culture AEC2s (adult, freshly isolated)
- Both donors map to **late_GW17_19 / week_18 / Budtip progenitors**
- PL1 is better aligned (0.739 vs 0.695) with lower ambiguity (22.4% vs 32.8%)
- Epithelial purity is high (94–96%) with low epi off-target (4.4–5.7%)
- **Key finding**: freshly isolated adult AEC2s project to a distal
  progenitor niche on the fetal reference, NOT to a mature/terminal
  state. This is biologically coherent — adult AT2 cells retain
  progenitor-like features that map to the Budtip compartment of the
  fetal reference.

### Primary cultured AEC2s (adult, cultured with MRC5)
- Both donors map to **late_GW17_19 / week_18** but diverge in state:
  - PL2 cultured → **Tip cells** (32.9%) — culture shifts toward more
    distal identity
  - PL1 cultured → **Budtip progenitors** (33.0%) — retains progenitor
    identity
- Epithelial purity is lower (84–90%) than pre-culture (94–96%) —
  consistent with MRC5 co-culture introducing non-epithelial signal
  despite EPCAM+ sorting
- Epi off-target is elevated (9.9–15.6%) vs pre-culture (4.4–5.7%)
- Culture effect is readable: PL2 shows a partial shift from Budtip
  toward Tip; PL1 retains Budtip but with reduced fraction

### iAEC2s (iPSC-derived, SPC2-ST-B2)
- All 3 conditions map to **late_GW17_19 / week_18 / Proliferating progenitors**
- Near-pure epithelial (97.9–99.1%) with very low epi off-target (0.9–2.1%)
- 3D/insert (CG13) is the best-aligned sample in the entire tranche
  (align=0.814, ambiguity=9.9%) — insert format produces the most
  resolved projection
- +MRC5/insert (CG14) shows slightly higher off-target (2.1%) but
  remains strongly epithelial — MRC5 co-culture effect is minimal after
  EPCAM+ sorting
- 3D Matrigel (CG12) has highest ambiguity (31.0%) — feeder-free 3D
  format produces a less resolved projection

### Cross-group comparison

| Group | Epi% | WL state_fine | Epi off-target | Ambiguity | Align |
|-------|-----:|---------------|---------------:|----------:|------:|
| Pre-culture primary | 94–96% | Budtip progenitors | 4.4–5.7% | 22–33% | 0.70–0.74 |
| Cultured primary | 84–90% | Tip cells / Budtip | 9.9–15.6% | 19–21% | 0.75–0.77 |
| iAEC2 | 98–99% | Proliferating progenitors | 0.9–2.1% | 10–31% | 0.69–0.82 |

**Key observations**:
1. **iAEC2s are the purest epithelial** (98–99%) — as expected for
   iPSC-derived lineage
2. **Cultured primary has the most off-target** (10–16%) — MRC5
   co-culture leaves a non-epithelial signature
3. **All groups map to late_GW17_19** — adult primary AEC2s land in the
   same stage window as existing iPSC tranches (GSE221343, GSE289846)
4. **State diversity**: primary → Budtip/Tip, iAEC2 → Proliferating
   progenitors — three distinct state_fine labels within one dataset

### Comparison with existing tranches

| Tranche | WL state_fine | Epi off-target | Stage |
|---------|---------------|---------------:|-------|
| GSE221343 (BU, iAT2/iAT1) | Stromal-like cells 1 / SOX2lowCFTR+ | 0.8–4.7% | late_GW17_19 |
| GSE289846 (Kyoto, iPSC epi) | Prolif. progenitors / SOX2lowCFTR+ / PNEC | 0.1–0.7% | late/early |
| GSE308817 (Xiamen, hESC ALO) | Budtip progenitors | 0.1–2.1% | early_GW10_13 |
| GSE193716 iAEC2 | Proliferating progenitors | 0.9–2.1% | late_GW17_19 |
| GSE193716 primary pre-culture | Budtip progenitors | 4.4–5.7% | late_GW17_19 |
| GSE193716 primary cultured | Tip cells / Budtip | 9.9–15.6% | late_GW17_19 |

- GSE193716 iAEC2 **Proliferating progenitors** matches GSE289846 3i_Day7
  baseline — cross-dataset replication of progenitor state for iPSC-derived
  alveolar epithelium
- GSE193716 primary pre-culture **Budtip progenitors** matches GSE308817
  (hESC passage series) but at a different stage (late vs early) — Budtip
  identity can emerge from both primary adult tissue and hESC organoids
- GSE193716 primary cultured **Tip cells** partially overlaps GSE237359
  donor-resolved Tip cells — culture may push primary AEC2s toward a more
  distal Tip-like identity

## 87.4% overlap adequacy

26,975/30,852 (87.4%) reference genes overlap, vs 92.0% for GSE221343
(same lab) and 100.0% for GSE289846/GSE308817.

- Alignment scores (0.69–0.82) are **within the range** of existing
  tranches (GSE221343: 0.62–0.67, GSE289846: 0.62–0.76, GSE308817:
  0.48–0.55). GSE193716 iAEC2 3D/insert actually has the highest single
  alignment score (0.814) of any external tranche row.
- The 87.4% overlap does **not** appear to degrade projection quality.
  The missing genes are lncRNAs that do not contribute meaningfully to
  the projection algorithm's nearest-neighbor calculations.
- **Conclusion**: 87.4% overlap is sufficient for interpretable projection.

## What seems biologically interpretable

1. **Adult primary AEC2s project to a distal progenitor niche** (Budtip /
   Tip) on the fetal reference — they do NOT fall off-target or map to an
   uninterpretable region.
2. **Culture effect is readable**: pre-culture → Budtip; cultured with
   MRC5 → partial shift toward Tip, plus elevated non-epithelial fraction.
3. **iAEC2 culture format matters**: 3D/insert produces the most resolved
   projection (lowest ambiguity, highest alignment); 3D Matrigel the least.
4. **Proliferating progenitors as iAEC2 identity** replicates across
   GSE193716 (BU) and GSE289846 (Kyoto) — cross-dataset signal.
5. **Stage consistency**: all 7 rows map to late_GW17_19 / week_18,
   matching GSE221343 and most of GSE289846.

## What remains unresolved

1. **Adult-primary-vs-fetal interpretability**: the projections are
   interpretable but the biological meaning of "adult AEC2 maps to fetal
   Budtip" requires domain judgment. Is this (a) a genuine progenitor
   signature retained in adult tissue, or (b) a reference-niche artifact?
   This cannot be resolved by projection alone.
2. **MRC5 contamination in cultured samples**: elevated off-target (10–16%)
   may reflect residual fibroblast cells despite EPCAM+ sorting, or it may
   reflect culture-induced transcriptomic changes. Coarse-type breakdown
   of the off-target fraction would disambiguate.
3. **Donor effect in cultured primary**: PL2 shifts to Tip, PL1 stays
   Budtip — is this donor-specific biology or stochastic? N=2 is
   insufficient to resolve.
4. **iAEC2 3D Matrigel ambiguity (31%)**: highest among iAEC2 conditions.
   Whether this is a feeder-free limitation or a Matrigel effect is unclear.

## Explicit stop line

- **query-ready promotion**: NOT done — all rows remain `query_ready_flag=false`
- **decision_log.md**: NOT edited
- **data_contract.yaml**: NOT edited
- **research_scope.md**: NOT edited
- **comparison_world_biology_summary**: NOT edited — GSE193716 is not
  part of the query-ready world yet

The purpose of this review is to document what the projections show and
flag open questions. Promotion requires a separate explicit reviewer
decision after evaluating the adult-primary-vs-fetal biological caveat.

## Files in this directory

| File | Description |
|------|-------------|
| `README.md` | This file |
| `gse193716_projection_review_v1.tsv` | Per-sample projection metrics and reviewer notes (7 rows, 21 columns) |

## Source files

| Source | Path |
|--------|------|
| Reference H5AD | `converted/reference_RNA.h5ad` |
| Reference metadata | `converted/reference_metadata_v1.csv` |
| GSE193716 H5AD files (7) | `queries/converted/gse193716/*.h5ad` |
| Projection run outputs | `benchmark_review_gse193716_v1/` (local, not committed) |
| Registration manifest | `metadata/external/gse193716_dataset_manifest_v1.yaml` |
| Registration sample sheet | `metadata/external/gse193716_organoid_query_sample_sheet_v1.tsv` |
| Gene-space audit | `reports/tranches/gse193716_registration_audit_v1/` |
| Conversion report | `reports/tranches/gse193716_conversion_v1/` |
