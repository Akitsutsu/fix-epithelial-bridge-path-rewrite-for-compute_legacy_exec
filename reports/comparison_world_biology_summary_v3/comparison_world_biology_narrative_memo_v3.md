# Cross-tranche biology narrative memo v3

## Date
2026-04-08

## Version note
This memo **supersedes** v2 (`reports/comparison_world_biology_summary_v2/`).
v2 remains in the repository as a historical snapshot (18 rows, 6 tranches).
v3 adds 2 GSE221344 rows promoted via D-0014 (paired same-line positive-arm
tranche).

## Reference basis
- Release v1: `converted/reference_RNA.h5ad` + `converted/reference_metadata_v1.csv`
- Stage axis: `sample_week`
- Execution: combined-root v2 canonical path (for GSE221343, GSE289846,
  GSE308817, GSE193716, GSE221344); multiroot collector path (for CA1, BU3,
  GSE237359)

---

## 1. Comparison world composition

The current query-ready world contains **20 rows** across **7 tranche components**:

| Tranche | Role | Lab | Stem cell background | Platform | Rows |
|---------|------|-----|---------------------|----------|------|
| CA1 / BU3 | proximal anchor | NA | organoid | 10x (inferred) | 2 |
| GSE237359 | donor-resolved external validation | Rawlins / Cambridge | fetal lung-derived AT2 organoid (HDBR donors) | 10x Chromium | 4 |
| GSE221343 | nearest external validation | Kotton / BU | iPSC iAT2/iAT1 (SPC2-ST-B2) | 10x Chromium | 3 |
| GSE289846 | cross-lab external validation | Gotoh / CiRA Kyoto | iPSC alveolar epithelial (B2-3) | 10x Chromium | 3 |
| GSE308817 | passage-series external validation | Liu/Rong / Xiamen | hESC alveolar organoid (H9) | SeekOne | 3 |
| GSE193716 (iAEC2 subset) | nearest external validation | Kotton / BU | iPSC iAEC2 (SPC2-ST-B2) | 10x Chromium | 3 |
| **GSE221344** | **nearest external validation** | **Kotton / BU** | **iPSC iAT2 (SPC2-ST-B2, YAP perturbation)** | **10x Chromium** | **2** |

This spans **4 labs** (BU, Cambridge, Kyoto, Xiamen), **3 stem cell backgrounds**
(iPSC SPC2-ST-B2, iPSC B2-3, hESC H9) plus primary fetal lung tissue, and
**2 scRNA platforms** (10x Chromium, SeekOne).

### What changed from v2 to v3
- +2 rows: GSE221344 paired perturbation tranche (D-0014)
- +1 tranche component: GSE221344
- GSE221344 is a **paired promotion** -- both WT-YAP (lentiviral control)
  and YAP5SA (constitutively active nuclear YAP) promoted together
- Kotton / BU now has 3 tranches (GSE221343, GSE193716 iAEC2, GSE221344)
- SPC2-ST-B2 is now represented in 3 independent datasets

---

## 2. GSE221344: what it adds

### Same-line paired perturbation axis
GSE221344 is the only tranche that provides a lentiviral-matched
perturbation comparison within a single iPSC line:
- **GSM6858857_WT_YAP** -- WT YAP lentiviral control (CK+DCI 7d)
- **GSM6858858_YAP5SA** -- YAP5SA constitutively active nuclear YAP (CK+DCI 7d)

Both map to **Proliferating progenitors** at **late_GW17_19 / week_18**
with near-pure epithelial identity (~98%).

### Directional CFTR+ lineage enrichment in YAP5SA
YAP5SA shows a clear enrichment of CFTR+ lineage cells relative to WT-YAP:
- SOX2lowCFTR+: **5.6%** vs **0.06%** (100x)
- NKX2-1+SOX9+CFTR+: **7.3%** vs **0.07%** (100x)
- Combined CFTR+ lineage: **~13%** vs **~0.1%**

This enrichment is perturbation-specific: same cell line, same medium,
same timepoint -- only the YAP transgene differs.

### Relationship to P-0001
The CFTR+ enrichment in YAP5SA is **directionally consistent** with P-0001,
which predicts that iAT1-directed perturbation drives SOX2lowCFTR+ identity
in SPC2-ST-B2 cells. However:

1. **SOX2lowCFTR+ is not the top state** in YAP5SA (only 5.6%). P-0001's
   success condition requires SOX2lowCFTR+ as the top epithelial state.
2. **GSE221344 lacks a culture-format-only control.** WT-YAP is a lentiviral
   control, not an untransduced control.
3. **P-0001 remains registered/supportive, not confirmed.**

GSE221344 provides **supportive positive-arm evidence** for P-0001 but
does not close the prediction.

### Required caveats
1. **WT-YAP is a lentiviral control, not an untransduced control.**
   Tip cells enrichment (29.9%) in WT-YAP distinguishes it from the
   untransduced CK+DCI control in GSE221343 (Stromal-like cells 1 at
   27.2%). Lentiviral transduction itself may alter cell state.
2. **YAP5SA shows a partial shift, not a top-state identity conversion.**
   Proliferating progenitors remains dominant (42.8%). This is a partial
   directional shift, not the complete SOX2lowCFTR+ conversion seen in
   GSE221343 L+DCI (34.8%).
3. **P-0001 remains registered/supportive, not confirmed.** No claim of
   single-tranche closure or prediction confirmation is made.

---

## 3. Anchor and tranche roles (updated)

Roles are unchanged from v2 for existing tranches:
- **CA1/BU3**: proximal anchor (mid_GW14_16 / week_15 / Basal cells)
- **GSE237359**: distal / donor-resolved benchmark (late_GW17_19 / Tip cells)
- **GSE221343**: condition-perturbation axis (iAT2 vs iAT1)
- **GSE289846**: cross-lab differentiation / transitional axis
- **GSE308817**: passage / maturation axis
- **GSE193716 iAEC2**: same-line culture-format comparison axis

New:
- **GSE221344**: same-line paired positive-arm perturbation axis

---

## 4. Updated state-by-tranche summary

| State_fine | Tranche(s) | Cross-dataset? |
|-----------|-----------|----------------|
| Basal cells | CA1/BU3 | -- |
| Tip cells | GSE237359 | -- |
| Stromal-like cells 1 | GSE221343 (iAT2) | -- |
| SOX2lowCFTR+ cells | GSE221343 (iAT1) + GSE289846 (LATS) | **yes** (BU + Kyoto) |
| Proliferating progenitors | GSE289846 (3i_Day7) + GSE193716 (iAEC2) + **GSE221344** | **yes** (Kyoto + BU) |
| PNEC | GSE289846 (PAL) | -- |
| Budtip progenitors | GSE308817 | -- |

Proliferating progenitors now appears in 3 tranches (GSE289846, GSE193716,
GSE221344). GSE221344's both rows map to Proliferating progenitors as top
state, adding a perturbation axis within the same state label.

---

## 5. What the current world enables (updated from v2)

All v2 capabilities retained, plus:
10. **Lentiviral perturbation comparison**: GSE221344 shows that
    constitutively active nuclear YAP (YAP5SA) partially enriches CFTR+
    lineage cells relative to the WT YAP lentiviral control, demonstrating
    perturbation-specific transcriptomic effects
11. **P-0001 supportive evidence**: the comparison world now includes
    direct evidence that an iAT1-directed perturbation enriches
    SOX2lowCFTR+ (even if partially), supporting the predicted direction

---

## 6. What is NOT yet in the comparison world

### Carried from v2
- GSE193716 primary AEC2 rows (4 rows held)
- No mesenchymal, endothelial, or immune compartment representation
- No disease-model organoids
- GSE308817 citation still missing
- CA1/BU3 epi-remap metrics still unavailable in decision-TSV format

### New gaps
- P-0001 cross-tranche closure assessment (combining GSE221344 perturbation
  arm with GSE193716 culture-format arm) has not been formally performed
- The discrepancy between GSE221343 YAP5SA (Stromal-like cells 1) and
  GSE221344 YAP5SA (Proliferating progenitors + CFTR+ enrichment) is noted
  but not resolved

---

## Source files used

All v2 sources plus:

| Source | Path |
|--------|------|
| GSE221344 query-ready review | `reports/tranches/gse221344_query_ready_review_v1/` |
| GSE221344 manifest | `metadata/external/gse221344_dataset_manifest_v1.yaml` |
| GSE221344 sample sheet | `metadata/external/gse221344_organoid_query_sample_sheet_v1.tsv` |
| Decision D-0014 | `decision_log.md` |
