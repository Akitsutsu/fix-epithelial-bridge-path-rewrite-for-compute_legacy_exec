# Cross-tranche biology narrative memo v1

## Date
2026-04-07

## Reference basis
- Release v1: `converted/reference_RNA.h5ad` + `converted/reference_metadata_v1.csv`
- Stage axis: `sample_week`
- Execution: combined-root v2 canonical path (for GSE221343, GSE289846, GSE308817);
  multiroot collector path (for CA1, BU3, GSE237359)

---

## 1. Comparison world composition

The current query-ready world contains **15 rows** across **5 tranches**:

| Tranche | Role | Lab | Stem cell background | Platform | Rows |
|---------|------|-----|---------------------|----------|------|
| CA1 / BU3 | proximal anchor | NA | organoid | 10x (inferred) | 2 |
| GSE237359 | donor-resolved external validation | Rawlins / Cambridge | fetal lung-derived AT2 organoid (HDBR donors) | 10x Chromium | 4 |
| GSE221343 | nearest external validation | Kotton / BU | iPSC iAT2/iAT1 (SPC2-ST-B2) | 10x Chromium | 3 |
| GSE289846 | cross-lab external validation | Gotoh / CiRA Kyoto | iPSC alveolar epithelial (B2-3) | 10x Chromium | 3 |
| GSE308817 | passage-series external validation | Liu/Rong / Xiamen | hESC alveolar organoid (H9) | SeekOne | 3 |

This spans **4 labs** (BU, Cambridge, Kyoto, Xiamen), **3 stem cell backgrounds** (iPSC SPC2-ST-B2, iPSC B2-3, hESC H9) plus primary fetal lung tissue, and **2 scRNA platforms** (10x Chromium, SeekOne).

---

## 2. Anchor vs external tranche roles

### Proximal anchors: CA1 and BU3
- Both map to **mid_GW14_16 / week_15**, with **Basal cells** as top state_fine.
- CA1 is described as a mixed proximal airway-like population; BU3 as a more converged one.
- These define the proximal reference pole of the comparison world.
- They are anchors for regression, not a cohort (D-0005).

### Distal / donor-resolved benchmark: GSE237359
- All 4 donor-resolved rows map to **late_GW17_19 / week_18**, with **Tip cells** as top state_fine.
- This is the distal / late-fetal pole — biologically distinct from the Basal cell identity of CA1/BU3.
- GSE237359 does not behave like additional proximal anchors; it provides an independent distal benchmark.
- Donor 16011 is retained but treated as supportive (261 cells only).

### Condition-perturbation axis: GSE221343
- Same lab as anchor queries (Kotton / BU), same iPSC line (SPC2-ST-B2).
- 3 conditions: iAT2 control (CK+DCI), YAP5SA perturbation, iAT1 differentiation (L+DCI).
- All map to **late_GW17_19 / week_18**, distinct from anchor stage (week_15).
- Condition difference is readable: iAT2 samples share Stromal-like cells 1 state; iAT1 shows SOX2lowCFTR+ cells.

### Differentiation / transitional axis: GSE289846
- Independent lab (CiRA Kyoto), independent iPSC line (B2-3), micro-patterned culture.
- 3 conditions: progenitor baseline (3i Day7), AT1 induction (LATS Day14), transitional (PAL Day14).
- Each condition maps to a distinct state_fine: Proliferating progenitors → SOX2lowCFTR+ → PNEC.
- PAL transitional shows a **stage shift** from late_GW17_19 to **early_GW10_13 / week_13** — the only condition in the world that shifts stage coarse.
- Near-pure epithelial (99.3–99.9%), lowest off-target in any tranche.

### Passage / maturation axis: GSE308817
- Fourth independent lab (Xiamen), hESC H9, SeekOne platform (non-10x).
- 3 passages: P3 (early), P7 (middle), P20 (late).
- All map to **early_GW10_13** at coarse, with **Budtip progenitors** as top state_fine.
- Passage trajectory is readable: P3→P7 convergence (Budtip rises, ambiguity drops), P7→P20 drift (Budtip drops, week_19 emerges, ambiguity rises).
- Lower alignment scores (0.48–0.55) and higher ambiguity (30–50%) than other tranches, consistent with Budtip progenitors occupying a less committed reference niche plus cross-platform/cross-background variation.

---

## 3. Three primary biology axes

### Axis 1: Condition perturbation (GSE221343 + partial GSE289846)
- **What it tests**: whether distinct culture conditions (control vs perturbation vs differentiation medium) produce distinct projection states on the fetal lung reference.
- **What the reference resolves**: iAT2 vs iAT1 differentiation is clearly visible as a state_fine difference (Stromal-like cells 1 vs SOX2lowCFTR+), even when stage remains constant (late_GW17_19).
- **Cross-lab replication**: GSE289846's LATS-IN-1 condition also maps to SOX2lowCFTR+ cells, replicating the AT1-directed state from an independent lab, line, and protocol. This is the strongest cross-lab biological signal in the current world.

### Axis 2: Differentiation / transitional (GSE289846)
- **What it tests**: whether the reference can resolve transitional cell states vs committed differentiation endpoints.
- **What the reference resolves**: each GSE289846 condition maps to a distinct state_fine, and the PAL transitional condition shifts to an earlier developmental stage (early_GW10_13 vs late_GW17_19), consistent with a less committed identity.
- **Unique contribution**: PAL → PNEC is the only row mapping to neuroendocrine-like state in the current world.

### Axis 3: Passage / maturation (GSE308817)
- **What it tests**: whether serial passaging of organoids produces detectable shifts in the reference projection.
- **What the reference resolves**: P3→P7 convergence toward Budtip progenitor identity, P7→P20 drift with stage diversification (week_19 emerging). The passage-dependent trajectory is readable even across platforms.
- **Unique contribution**: first non-10x tranche, first hESC background, first passage-series biology axis.

---

## 4. GSE237359 as the distal / donor-resolved benchmark

GSE237359 occupies a distinct structural role in the comparison world:

- It is the only **primary fetal lung-derived** tranche (not iPSC/hESC).
- It is the only **multi-donor** tranche (4 donors from HDBR tissue bank).
- All donors consistently project to **week_18 / Tip cells**, providing a coherent distal benchmark independent of stem cell derivation.
- This positions GSE237359 as the distal counterpart to the proximal CA1/BU3 anchors: together they bracket the early-to-late, Basal-to-Tip range of the reference.

---

## 5. CA1 / BU3 as proximal anchors

CA1 and BU3 both project to **mid_GW14_16 / week_15 / Basal cells**, occupying the proximal airway-like niche of the reference. Key considerations:

- They are the only rows in the current world with Basal cell identity.
- They serve as regression anchors, not as a biological cohort (D-0005).
- All external tranches project to either late_GW17_19 or early_GW10_13, not mid_GW14_16 — so CA1/BU3 remain the sole occupants of the mid-gestational proximal niche.
- Epithelial remap metrics (stage_fine, state_fine, ambiguity) are not available for CA1/BU3 in the canonical compare table; these were computed under the multiroot collector path, which does not produce the same epi-remap decision TSV format.

---

## 6. Shared states and tranche-specific states

### Cross-tranche replicated states
- **SOX2lowCFTR+ cells**: observed in GSE221343 (L+DCI iAT1 differentiation) and GSE289846 (LATS-IN-1 AT1 induction). Two labs, two iPSC lines, two protocols → convergent AT1-directed state. This is the strongest cross-lab replication of a specific cell state in the current world.
- **Epithelial coarse assignment**: all 15 rows map primarily to Epithelial at WL coarse (95–100%), confirming that the organoid/fetal lung-derived systems in this world are overwhelmingly epithelial when projected onto the fetal lung reference.

### Tranche-specific states
- **Basal cells**: only CA1 and BU3 (proximal anchors).
- **Tip cells**: only GSE237359 (distal fetal lung-derived benchmark).
- **Stromal-like cells 1**: only GSE221343 iAT2 samples (CK+DCI and YAP5SA). This is a reference label mapping, not actual stromal identity.
- **Proliferating progenitors**: only GSE289846 3i_Day7 baseline.
- **PNEC**: only GSE289846 3i_PAL_Day14 transitional.
- **Budtip progenitors**: only GSE308817 passage series.

---

## 7. Cross-lab / cross-platform interpretability

### Readable across labs, lines, and platforms
- **Epithelial identity** is consistently detected (95–100%) across 4 labs, 3 stem cell backgrounds, and 2 platforms.
- **SOX2lowCFTR+ cells** as an AT1-directed state replicates across BU (GSE221343 L+DCI) and Kyoto (GSE289846 LATS Day14).
- **Stage axis resolution**: the reference separates early_GW10_13, mid_GW14_16, and late_GW17_19 stages for organoids from independent sources, and the assignments are biologically coherent (Budtip progenitors → early, Basal → mid, Tip/iAT2/iAT1 → late).

### Still ambiguous
- **Stromal-like cells 1** as a state_fine label for epithelial organoids is a reference-label artifact, not a biological identity. It maps to GSE221343 iAT2 samples but its biological meaning is unclear — the coarse assignment is correctly Epithelial.
- **Budtip progenitor ambiguity** in GSE308817 is high (30–50%), partly because Budtip occupies a less committed reference niche and partly because of cross-platform (SeekOne) and cross-background (hESC H9) variation. Whether this ambiguity is biological or technical is not yet resolved.
- **CA1/BU3 epithelial remap metrics** are not available in the current canonical compare table. Epi-level interpretation for the anchors relies on older multiroot collector outputs that did not produce decision-TSV-format metrics.
- **GSE237359 epithelial remap metrics** are similarly not available from the canonical compare table.
- **Fine-stage assignment for GSE308817 P7 and P20** is not clearly stated in existing review artifacts (P3 is week_11; P20 shows week_19 emerging but the top fine stage is not reported as a single value).

---

## 8. What the current world enables

1. **Proximal-to-distal bracketing**: CA1/BU3 (week_15 / Basal) and GSE237359 (week_18 / Tip) define a proximal-distal axis in the reference that external organoid tranches can be placed relative to.
2. **Condition-resolved biology**: GSE221343 and GSE289846 demonstrate that distinct culture conditions produce distinct and interpretable projection states, even within the same cell line.
3. **Cross-lab replication**: SOX2lowCFTR+ identity is confirmed across 2 independent labs and protocols, establishing that the reference can detect AT1-directed differentiation regardless of source.
4. **Passage trajectory**: GSE308817 shows that serial passaging produces a readable and graded trajectory (convergence then drift), demonstrating that the reference captures organoid maturation dynamics.
5. **Cross-platform validity**: SeekOne (GSE308817) and 10x Chromium (all others) both produce interpretable projections, confirming that the reference is not 10x-specific.
6. **Stage-axis resolution**: organoids from different sources map to biologically coherent developmental stages, with stage shifts that correspond to expected biology (e.g., transitional PAL → earlier stage, passage-dependent maturation → stage diversification).

---

## 9. Next biology gaps

1. **Primary tissue benchmark**: GSE237359 is primary fetal lung-derived, but its epi-remap metrics are not yet available in the same format as the newer tranches. A formal epi-remap comparison of the distal benchmark against the proximal anchors would strengthen the bracketing claim.
2. **Organotypic complexity**: all current external tranches are epithelial-dominated (>95%). The comparison world has no mesenchymal, endothelial, or immune-compartment representation. Organotypic or co-culture models would test whether the reference resolves non-epithelial organoid fates.
3. **Disease perturbation**: the current world is entirely healthy/wild-type (with the exception of YAP5SA, which is a subtle perturbation). Disease-model organoids (e.g., ILD, LUAD, CF) would test whether the reference can separate disease-associated states.
4. **Temporal resolution within passage**: GSE308817 samples P3/P7/P20, but intermediate passages and more granular timepoints are not available. Whether the P7 convergence optimum generalizes across labs is unknown.
5. **Anchor expansion**: CA1/BU3 remain the only proximal anchors. Additional proximal organoid samples from independent labs would confirm whether the Basal cell mapping is reproducible.
6. **Citation gap**: GSE308817 has no linked publication — once a citation is available, the passage biology interpretation can be cross-referenced against the authors' own analysis.

---

## Source files used

| Source | Path |
|--------|------|
| Research scope | `research_scope.md` |
| Data contract | `data_contract.yaml` |
| Decision log | `decision_log.md` |
| Current release | `references/registry/current_release.yaml` |
| Query manifest v1 | `query_manifest_v1.csv` |
| GSE237359 sample sheet v2 | `queries/converted/gse237359/gse237359_organoid_query_sample_sheet_v2.tsv` |
| GSE237359 canonical compare table | `reports/tranches/gse237359_external_validation_v1/gse237359_vs_CA1_BU3_key_metrics_multiroot.tsv` |
| GSE237359 tranche memo | `reports/tranches/gse237359_external_validation_v1/gse237359_tranche_result_memo_v1.md` |
| GSE237359 validation README | `reports/tranches/gse237359_external_validation_v1/README.md` |
| GSE221343 sample sheet v1 | `metadata/external/gse221343_organoid_query_sample_sheet_v1.tsv` |
| GSE221343 review README | `reports/tranches/gse221343_query_ready_review_v1/README.md` |
| GSE221343 decisions TSV | `reports/tranches/gse221343_query_ready_review_v1/gse221343_query_ready_decisions_v1.tsv` |
| GSE289846 sample sheet v1 | `metadata/external/gse289846_organoid_query_sample_sheet_v1.tsv` |
| GSE289846 review README | `reports/tranches/gse289846_query_ready_review_v1/README.md` |
| GSE289846 decisions TSV | `reports/tranches/gse289846_query_ready_review_v1/gse289846_query_ready_decisions_v1.tsv` |
| GSE308817 sample sheet v1 | `metadata/external/gse308817_organoid_query_sample_sheet_v1.tsv` |
| GSE308817 review README | `reports/tranches/gse308817_query_ready_review_v1/README.md` |
| GSE308817 decisions TSV | `reports/tranches/gse308817_query_ready_review_v1/gse308817_query_ready_decisions_v1.tsv` |

## Column sourcing notes

- **CA1, BU3, GSE237359**: whole-lung metrics sourced from canonical multiroot compare table. Epithelial remap metrics (epi_top_stage, epi_top_state_fine, epi_ambiguous) are NA because the multiroot collector path did not produce epi-remap decision TSVs in the current format.
- **GSE221343, GSE289846, GSE308817**: metrics sourced from per-tranche query-ready decision TSVs produced during Gate A–D review. Percentages in parentheses were stripped from labels for clean summary columns.
- **whole_lung_off_target_fraction** and **epithelial_lineage_off_target_fraction**: for the newer tranches (GSE221343/289846/308817), both represent the WL-level non-epithelial fraction (derived from WL coarse type assignment). These are the same value because the decision TSVs define epi_off_target as the WL non-epithelial fraction.
- **epithelial_eligible_fraction**: for CA1/BU3/GSE237359, computed as n_query_epi_eligible / n_query_cells from the compare table. For newer tranches, computed as (100 - epi_off_target_pct).
- All fractions expressed as percentages (0–100 scale) rounded to 1 decimal place.
