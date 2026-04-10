# Cross-tranche biology narrative memo v5

## Date
2026-04-10

## Version note
This memo **supersedes** v4 (`reports/comparison_world_biology_summary_v4/`).
v4 remains in the repository as a historical snapshot (24 rows, 8 tranches).
v5 adds 4 GSE246243 rows promoted as a same-line kinetic strengthening tranche.

## Reference basis
- Release v1: `converted/reference_RNA.h5ad` + `converted/reference_metadata_v1.csv`
- Stage axis: `sample_week`
- Execution: combined-root v2 canonical path (for all post-GSE237359 tranches);
  multiroot collector path (for CA1, BU3, GSE237359)

---

## 1. Comparison world composition

The current query-ready world contains **28 rows** across **9 tranche components**:

| Tranche | Role | Lab | Stem cell background | Platform | Rows |
|---------|------|-----|---------------------|----------|------|
| CA1 / BU3 | proximal anchor | NA | organoid | 10x (inferred) | 2 |
| GSE237359 | donor-resolved external validation | Rawlins / Cambridge | fetal lung-derived AT2 organoid | 10x Chromium | 4 |
| GSE221343 | nearest external validation | Kotton / BU | iPSC iAT2/iAT1 (SPC2-ST-B2) | 10x Chromium | 3 |
| GSE289846 | cross-lab external validation | Gotoh / CiRA Kyoto | iPSC alveolar epithelial (B2-3) | 10x Chromium | 3 |
| GSE308817 | passage-series external validation | Liu/Rong / Xiamen | hESC alveolar organoid (H9) | SeekOne | 3 |
| GSE193716 (iAEC2 subset) | nearest external validation | Kotton / BU | iPSC iAEC2 (SPC2-ST-B2) | 10x Chromium | 3 |
| GSE221344 | nearest external validation | Kotton / BU | iPSC iAT2 (SPC2-ST-B2, YAP perturbation) | 10x Chromium | 2 |
| GSE221342 | nearest external validation | Kotton / BU | iPSC iAT2/iAT1 (BU3 NGAT, boundary-stress) | 10x Chromium | 4 |
| **GSE246243** | **nearest external validation** | **Kotton / BU** | **iPSC iAT2/iAT1 (BU3 NGAT, kinetic)** | **10x Chromium** | **4** |

This spans **4 labs**, **4 stem cell backgrounds**, and **2 scRNA platforms**.

### What changed from v4 to v5
- +4 rows: GSE246243 same-line kinetic tranche
- +1 tranche component: GSE246243
- First kinetic time-series axis in the comparison world
- SOX2lowCFTR+ now in 4 tranches (GSE221343, GSE289846, GSE221342, +GSE246243 72hr)
- Proliferating progenitors now in 4 tranches (GSE289846, GSE193716, GSE221344, +GSE246243 t=0/24hr/48hr)

---

## 2. GSE246243: what it adds

### Same-line kinetic strengthening tranche
GSE246243 provides a 4-point kinetic time series on BU3 NGAT with
L+DCI switch:

| Sample | Timepoint | Epi top state | Off-target | Ambiguity |
|--------|-----------|--------------|-----------|-----------|
| iAT2 3D | t=0 (baseline) | Proliferating progenitors (44.5%) | 4.6% | 25.3% |
| iAT1 24hr | 24hr post L+DCI | Proliferating progenitors (71.7%) | 2.4% | 15.5% |
| iAT1 48hr | 48hr post L+DCI | Proliferating progenitors (45.5%) | 1.2% | 13.6% |
| iAT1 72hr | 72hr post L+DCI | **SOX2lowCFTR+ cells (53.6%)** | 0.6% | 13.8% |

The kinetic structure is:
- **t=0:** Proliferating progenitors baseline before L+DCI switch.
- **24hr:** Initial progenitor expansion phase.
- **48hr:** Transitional heterogeneity; SOX2lowCFTR+ emerging.
- **72hr:** SOX2lowCFTR+ cells becomes top state. Commitment direction
  is visible at the top-state level.

Off-target improves monotonically (4.6 → 0.6%). Ambiguity improves
from baseline and stabilizes (~14%).

### Relationship to GSE221342
Both tranches use BU3 NGAT with L+DCI differentiation. GSE221342
provides the endpoint gradient (3D vs ALI, reaching 78.0%
SOX2lowCFTR+ at ALI p1). GSE246243 provides the early kinetic
trajectory (0–72hr, reaching 53.6% SOX2lowCFTR+ at 72hr). Together
they form a complementary view: kinetic onset + endpoint resolution.

### This is NOT a P-0001 validation tranche
BU3 NGAT is a different iPSC line from SPC2-ST-B2. The kinetic
SOX2lowCFTR+ shift is cross-line supportive evidence, not same-line
P-0001 validation.

### This is NOT full alveolarization evidence
72hr is an early kinetic point. The SOX2lowCFTR+ fraction (53.6%)
is lower than GSE221342 endpoints. This strengthens the commitment
direction but does not close alveolarization.

---

## 3. Updated state-by-tranche summary

| State_fine | Tranche(s) | Cross-dataset? |
|-----------|-----------|----------------|
| Basal cells | CA1/BU3 | -- |
| Tip cells | GSE237359 | -- |
| Stromal-like cells 1 | GSE221343 (iAT2) | -- |
| SOX2lowCFTR+ cells | GSE221343 + GSE289846 + GSE221342 + **GSE246243 (72hr)** | **yes** (3 lines, 2 labs) |
| Proliferating progenitors | GSE289846 + GSE193716 + GSE221344 + **GSE246243 (t=0/24hr/48hr)** | **yes** |
| PNEC | GSE289846 (PAL) | -- |
| Budtip progenitors | GSE308817 + GSE221342 (iAT2_3D) | **yes** |

---

## 4. What is NOT yet in the comparison world

- GSE193716 primary AEC2 rows (4 held)
- No mesenchymal, endothelial, or immune compartment
- No disease-model organoids
- GSE308817 citation still missing
- P-0001 closure not formally assessed
- Full alveolarization not closed

---

## Source files used

All v4 sources plus:

| Source | Path |
|--------|------|
| GSE246243 query-ready review | `reports/tranches/gse246243_query_ready_review_v1/` |
| GSE246243 decisions TSV | `reports/tranches/gse246243_query_ready_review_v1/gse246243_query_ready_decisions_v1.tsv` |
