# Cross-tranche biology narrative memo v4

## Date
2026-04-10

## Version note
This memo **supersedes** v3 (`reports/comparison_world_biology_summary_v3/`).
v3 remains in the repository as a historical snapshot (20 rows, 7 tranches).
v4 adds 4 GSE221342 rows promoted as a boundary-stress tranche.

## Reference basis
- Release v1: `converted/reference_RNA.h5ad` + `converted/reference_metadata_v1.csv`
- Stage axis: `sample_week`
- Execution: combined-root v2 canonical path (for GSE221343, GSE289846,
  GSE308817, GSE193716, GSE221344, GSE221342); multiroot collector path
  (for CA1, BU3, GSE237359)

---

## 1. Comparison world composition

The current query-ready world contains **24 rows** across **8 tranche components**:

| Tranche | Role | Lab | Stem cell background | Platform | Rows |
|---------|------|-----|---------------------|----------|------|
| CA1 / BU3 | proximal anchor | NA | organoid | 10x (inferred) | 2 |
| GSE237359 | donor-resolved external validation | Rawlins / Cambridge | fetal lung-derived AT2 organoid (HDBR donors) | 10x Chromium | 4 |
| GSE221343 | nearest external validation | Kotton / BU | iPSC iAT2/iAT1 (SPC2-ST-B2) | 10x Chromium | 3 |
| GSE289846 | cross-lab external validation | Gotoh / CiRA Kyoto | iPSC alveolar epithelial (B2-3) | 10x Chromium | 3 |
| GSE308817 | passage-series external validation | Liu/Rong / Xiamen | hESC alveolar organoid (H9) | SeekOne | 3 |
| GSE193716 (iAEC2 subset) | nearest external validation | Kotton / BU | iPSC iAEC2 (SPC2-ST-B2) | 10x Chromium | 3 |
| GSE221344 | nearest external validation | Kotton / BU | iPSC iAT2 (SPC2-ST-B2, YAP perturbation) | 10x Chromium | 2 |
| **GSE221342** | **nearest external validation** | **Kotton / BU** | **iPSC iAT2/iAT1 (BU3 NGAT, boundary-stress)** | **10x Chromium** | **4** |

This spans **4 labs** (BU, Cambridge, Kyoto, Xiamen), **4 stem cell backgrounds**
(iPSC SPC2-ST-B2, iPSC B2-3, iPSC BU3 NGAT, hESC H9) plus primary fetal lung
tissue, and **2 scRNA platforms** (10x Chromium, SeekOne).

### What changed from v3 to v4
- +4 rows: GSE221342 boundary-stress tranche
- +1 tranche component: GSE221342
- +1 stem cell background: BU3 NGAT
- First external mid_GW14_16 row (iAT2_3D)
- First ALI culture format (iAT1 ALI p0/p1)
- SOX2lowCFTR+ now replicates across 3 lines (SPC2-ST-B2, B2-3, BU3 NGAT)
- Budtip progenitors now in 2 tranches (GSE308817 + GSE221342 iAT2)

---

## 2. GSE221342: what it adds

### Boundary-stress / directional gradient tranche
GSE221342 provides a 4-point directional gradient within a single donor
cell line (BU3 NGAT):
- **GSM6858850_iAT2_3D** — iAT2 baseline (CK+DCI, 3D). Maps to
  **mid_GW14_16 / week_15** at whole-lung level, **Budtip progenitors**
  at epithelial level. First external row at mid_GW14_16.
- **GSM6858851_iAT1_3D** — iAT1 differentiation (L+DCI, 3D). Shifts to
  **late_GW17_19 / SOX2lowCFTR+ cells** (60.9%).
- **GSM6858852_iAT1_ALI_p0** — iAT1 ALI p0. SOX2lowCFTR+ retained
  (56.8%). First ALI condition in the comparison world.
- **GSM6858853_iAT1_ALI_p1** — iAT1 ALI p1 (3D pre-diff + ALI).
  Strongest SOX2lowCFTR+ in any tranche (**78.0%**), best alignment,
  lowest ambiguity (14.2%).

The gradient is monotonic: Budtip progenitors → SOX2lowCFTR+ cells with
improving alignment and decreasing off-target along the iAT1/ALI axis.

### Cross-line SOX2lowCFTR+ replication
BU3 NGAT L+DCI → SOX2lowCFTR+ (60.9–78.0%) replicates the same
directional shift seen on two other iPSC lines:
- SPC2-ST-B2 L+DCI (GSE221343): 34.8%
- B2-3 LATS-IN-1 (GSE289846): 31.8%

SOX2lowCFTR+ now appears across **3 cell lines** and **2 labs** (BU + Kyoto).

### This is NOT a P-0001 validation tranche
BU3 NGAT is a different iPSC line from SPC2-ST-B2 (the P-0001 basis).
The SOX2lowCFTR+ replication is cross-line supportive evidence, not
same-line P-0001 validation.

### ALI readability on v1
Both ALI conditions retain SOX2lowCFTR+ identity on the fetal reference.
ALI p1 with 3D pre-differentiation produces the most resolved iAT1 in
the comparison world. This confirms ALI is readable on the current
reference without requiring a new reference build.

---

## 3. Anchor and tranche roles (updated)

Roles unchanged from v3 for existing tranches. New:
- **GSE221342**: boundary-stress / directional gradient tranche. Tests
  mid-stage coverage gap (iAT2 baseline at mid_GW14_16) and the
  3D → ALI differentiation axis.

---

## 4. Updated state-by-tranche summary

| State_fine | Tranche(s) | Cross-dataset? |
|-----------|-----------|----------------|
| Basal cells | CA1/BU3 | -- |
| Tip cells | GSE237359 | -- |
| Stromal-like cells 1 | GSE221343 (iAT2) | -- |
| SOX2lowCFTR+ cells | GSE221343 (iAT1) + GSE289846 (LATS) + **GSE221342 (iAT1 3D/ALI)** | **yes** (BU SPC2-ST-B2 + Kyoto B2-3 + **BU BU3-NGAT**) |
| Proliferating progenitors | GSE289846 (3i_Day7) + GSE193716 (iAEC2) + GSE221344 | **yes** (Kyoto + BU) |
| PNEC | GSE289846 (PAL) | -- |
| Budtip progenitors | GSE308817 + **GSE221342 (iAT2_3D)** | **yes** (Xiamen + **BU**) |

---

## 5. What the current world enables (updated from v3)

All v3 capabilities retained, plus:
12. **Cross-line iAT1 replication**: SOX2lowCFTR+ now replicates across
    3 iPSC lines (SPC2-ST-B2, B2-3, BU3 NGAT), strengthening the
    directional signal
13. **Directional gradient within a single line**: GSE221342 provides a
    4-point 3D→ALI gradient on one cell line, enabling within-tranche
    dose-response-like analysis
14. **Mid-stage coverage**: iAT2_3D provides the first external
    mid_GW14_16 row, breaking the anchor-only coverage at this stage
15. **ALI culture format**: new axis for culture-format comparison

---

## 6. What is NOT yet in the comparison world

### Carried from v3
- GSE193716 primary AEC2 rows (4 rows held)
- No mesenchymal, endothelial, or immune compartment representation
- No disease-model organoids
- GSE308817 citation still missing

### New gaps
- P-0002 formal registration not yet performed (P-0002 design note exists;
  registry readiness assessment identified GSE221342 promotion as the
  prerequisite — now resolved)
- P-0001 cross-tranche closure assessment still not formally performed

---

## Source files used

All v3 sources plus:

| Source | Path |
|--------|------|
| GSE221342 query-ready review | `reports/tranches/gse221342_query_ready_review_v1/` |
| GSE221342 decisions TSV | `reports/tranches/gse221342_query_ready_review_v1/gse221342_query_ready_decisions_v1.tsv` |
| Legacy epithelial backfill pilot | `reports/repo_state/legacy_metric_backfill_pilot_v1.tsv` |

The 6-row legacy epithelial surface (CA1, BU3, 4 GSE237359 donors) is
symmetric at the 5-column level while preserving multiroot provenance.
Combined-root migration for these rows remains deferred.
