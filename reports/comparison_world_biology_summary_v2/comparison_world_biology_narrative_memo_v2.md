# Cross-tranche biology narrative memo v2

## Date
2026-04-07

## Version note
This memo **supersedes** v1 (`reports/comparison_world_biology_summary_v1/`).
v1 remains in the repository as a historical snapshot (15 rows, 5 tranches).
v2 adds 3 GSE193716 iAEC2 rows promoted via D-0013.

## Reference basis
- Release v1: `converted/reference_RNA.h5ad` + `converted/reference_metadata_v1.csv`
- Stage axis: `sample_week`
- Execution: combined-root v2 canonical path (for GSE221343, GSE289846, GSE308817,
  GSE193716); multiroot collector path (for CA1, BU3, GSE237359)

---

## 1. Comparison world composition

The current query-ready world contains **18 rows** across **6 tranche components**:

| Tranche | Role | Lab | Stem cell background | Platform | Rows |
|---------|------|-----|---------------------|----------|------|
| CA1 / BU3 | proximal anchor | NA | organoid | 10x (inferred) | 2 |
| GSE237359 | donor-resolved external validation | Rawlins / Cambridge | fetal lung-derived AT2 organoid (HDBR donors) | 10x Chromium | 4 |
| GSE221343 | nearest external validation | Kotton / BU | iPSC iAT2/iAT1 (SPC2-ST-B2) | 10x Chromium | 3 |
| GSE289846 | cross-lab external validation | Gotoh / CiRA Kyoto | iPSC alveolar epithelial (B2-3) | 10x Chromium | 3 |
| GSE308817 | passage-series external validation | Liu/Rong / Xiamen | hESC alveolar organoid (H9) | SeekOne | 3 |
| GSE193716 (iAEC2 subset) | nearest external validation | Kotton / BU | iPSC iAEC2 (SPC2-ST-B2) | 10x Chromium | 3 |

This spans **4 labs** (BU, Cambridge, Kyoto, Xiamen), **3 stem cell backgrounds**
(iPSC SPC2-ST-B2, iPSC B2-3, hESC H9) plus primary fetal lung tissue, and
**2 scRNA platforms** (10x Chromium, SeekOne).

### What changed from v1 to v2
- +3 rows: GSE193716 iAEC2 subset (D-0013)
- +1 tranche component: GSE193716
- GSE193716 is a **subset promotion** — 4 primary AEC2 rows remain held
- Kotton / BU now has 2 tranches (GSE221343 + GSE193716 iAEC2)
- The same iPSC line (SPC2-ST-B2) is now represented in 2 independent datasets

---

## 2. GSE193716 iAEC2 subset: what it adds

### Culture-format comparison axis
GSE193716 is the only tranche that compares culture formats within a single
iPSC line and differentiation protocol:
- **3D Matrigel** (feeder-free) — baseline
- **3D/insert** (feeder-free) — best alignment, lowest ambiguity
- **+MRC5/insert** (co-culture) — minimal stromal effect on iAEC2

All 3 map to **Proliferating progenitors** at **late_GW17_19 / week_18**
with near-pure epithelial identity (97.9–99.1%).

### Cross-dataset replication of Proliferating progenitors
GSE193716 iAEC2 Proliferating progenitors replicates GSE289846 3i_Day7
(Kyoto, B2-3 line). These are different labs, iPSC lines, and protocols
converging on the same state_fine label — strengthening the cross-dataset
signal. Note however that GSE193716 is from the same lab as GSE221343
(Kotton / BU), so this is cross-dataset within the same lab rather than
fully cross-lab.

### Controlled same-line comparison with GSE221343
- GSE221343 CK+DCI (SPC2-ST-B2) → Stromal-like cells 1
- GSE193716 iAEC2 3D (SPC2-ST-B2) → Proliferating progenitors

Different state_fine for the same iPSC line in different culture formats
and differentiation timepoints. This demonstrates that culture format
affects the projection state, not just the cell line or donor.

### 87.4% gene overlap was adequate
GSE193716 has 26,975/30,852 (87.4%) reference overlap — lower than
GSE221343 (92.0%) or GSE289846/GSE308817 (100.0%). Despite this, the
iAEC2 3D/insert row achieves the highest single alignment score (0.814)
of any external tranche row in the comparison world. The overlap gap
(lncRNA annotation drift) does not degrade projection quality.

---

## 3. Anchor and tranche roles (updated)

Roles are unchanged from v1 for existing tranches:
- **CA1/BU3**: proximal anchor (mid_GW14_16 / week_15 / Basal cells)
- **GSE237359**: distal / donor-resolved benchmark (late_GW17_19 / Tip cells)
- **GSE221343**: condition-perturbation axis (iAT2 vs iAT1)
- **GSE289846**: cross-lab differentiation / transitional axis
- **GSE308817**: passage / maturation axis

New:
- **GSE193716 iAEC2**: same-line culture-format comparison axis

---

## 4. Updated state-by-tranche summary

| State_fine | Tranche(s) | Cross-dataset? |
|-----------|-----------|----------------|
| Basal cells | CA1/BU3 | — |
| Tip cells | GSE237359 | — |
| Stromal-like cells 1 | GSE221343 (iAT2) | — |
| SOX2lowCFTR+ cells | GSE221343 (iAT1) + GSE289846 (LATS) | **yes** (BU + Kyoto) |
| Proliferating progenitors | GSE289846 (3i_Day7) + GSE193716 (iAEC2) | **yes** (Kyoto + BU) |
| PNEC | GSE289846 (PAL) | — |
| Budtip progenitors | GSE308817 | — |

Two states now replicate across datasets:
1. **SOX2lowCFTR+** — cross-lab (BU + Kyoto)
2. **Proliferating progenitors** — cross-dataset (Kyoto + BU, same state from different labs/lines)

---

## 5. What the current world enables (updated from v1)

All v1 capabilities retained, plus:
7. **Culture-format comparison**: GSE193716 shows that insert format produces
   more resolved projections than 3D Matrigel for the same iPSC line
8. **Same-line cross-dataset comparison**: SPC2-ST-B2 in GSE221343 vs
   GSE193716 — different state_fine, demonstrating format sensitivity
9. **Proliferating progenitors cross-dataset replication**: GSE289846 +
   GSE193716 converge on the same state from independent datasets

---

## 6. What is NOT yet in the comparison world

### GSE193716 primary AEC2 rows (4 rows held)
- 2 pre-culture: hold_pending_biological_review (adult-vs-fetal Budtip caveat)
- 2 cultured: not_recommended_now (epi off-target 10–16%)
- These can be reconsidered after domain-expert input

### Other gaps (carried from v1)
- No mesenchymal, endothelial, or immune compartment representation
- No disease-model organoids
- GSE308817 citation still missing
- CA1/BU3 epi-remap metrics still unavailable in decision-TSV format

---

## Source files used

All v1 sources plus:

| Source | Path |
|--------|------|
| GSE193716 iAEC2 subset review | `reports/tranches/gse193716_iAEC2_subset_review_v1/` |
| GSE193716 projection review | `reports/tranches/gse193716_projection_review_v1/` |
| GSE193716 manifest | `metadata/external/gse193716_dataset_manifest_v1.yaml` |
| GSE193716 sample sheet | `metadata/external/gse193716_organoid_query_sample_sheet_v1.tsv` |
| Decision D-0013 | `decision_log.md` |
