# Prediction Registry v1

## Date
2026-04-07

## Purpose
Register a single prospective hypothesis (P-0001) derived from the current
comparison world (v2, 18 rows). This registry is **not** a new canonical
biology source — it is a prospective test index that records what the
current world predicts and how that prediction could be validated or
falsified by future data.

## Why only one prediction
The goal is to close one loop cleanly before opening more. P-0001
captures the strongest directional signal visible in the current world:
the same iPSC line (SPC2-ST-B2) shows different epithelial states
depending on whether the perturbation is lineage-directing (iAT1) or
culture-format-only. Registering one prediction keeps the registry
focused and reviewable.

## Current comparison world used as basis
`reports/comparison_world_biology_summary_v2/` (18 rows, 6 components).

---

## P-0001: same-line perturbation direction

### Short rationale
Three independent observations converge:

1. **GSE221343 L+DCI** (Kotton / BU, SPC2-ST-B2): explicit iAT1-directed
   differentiation via L+DCI medium → epithelial_top_state_fine =
   **SOX2lowCFTR+ cells**

2. **GSE193716 iAEC2 subset** (Kotton / BU, SPC2-ST-B2): culture-format
   variation only (3D / insert / +MRC5, no lineage-directing medium) →
   epithelial_top_state_fine = **Proliferating progenitors** (all 3 rows)

3. **GSE289846** (Gotoh / Kyoto, B2-3): cross-lab support. 3i_Day7
   baseline = Proliferating progenitors; LATS-IN-1 AT1 induction =
   SOX2lowCFTR+ cells. Same direction, different lab and iPSC line.

The hypothesis: within same-line SPC2-ST-B2, the perturbation type
(lineage-directing vs culture-format-only) determines whether the
projection lands in SOX2lowCFTR+ or Proliferating progenitors.

### Success condition
A future same-line SPC2-ST-B2 tranche containing both:
- (a) an explicit iAT1-directed condition → epithelial_top_state_fine =
  SOX2lowCFTR+ cells
- (b) a culture-format-only condition → epithelial_top_state_fine =
  Proliferating progenitors, with epi off-target < 5%

Both (a) and (b) must hold in the same tranche for the prediction
to be confirmed.

### Falsification condition
Any of:
- (i) A culture-format-only SPC2-ST-B2 row maps to SOX2lowCFTR+ cells
  instead of Proliferating progenitors
- (ii) An explicit iAT1-directed SPC2-ST-B2 row retains Proliferating
  progenitors and does not shift toward SOX2lowCFTR+
- (iii) Direction is inconsistent across replicates within the same
  condition

### Validation target
Descriptive: **next same-line Kotton/BU SPC2-ST-B2 tranche with explicit
iAT1-directed condition split**. No specific GEO accession is named —
the target is a class of future datasets, not a pre-identified series.

### Why GSE193716 held primary rows are excluded
The 4 held primary AEC2 rows (GSM5819131, GSM5819132, GSM5819129,
GSM5819130) are adult primary tissue, not iPSC-derived. The
adult-primary-vs-fetal reference caveat remains unresolved, and the
Budtip/Tip mapping of these rows reflects a different biological
question (adult tissue identity on fetal reference) rather than the
same-line perturbation-direction question that P-0001 addresses.

---

## Explicit stop line
- **No new intake** registered by this artifact
- **No projection rerun** performed
- **No query-ready change** made
- **No governance file edited** (data_contract.yaml, decision_log.md,
  research_scope.md are unchanged)
- **No modification** to comparison_world_biology_summary_v2/ or
  artifact_lifecycle_registry_v1/

## Files in this directory

| File | Description |
|------|-------------|
| `README.md` | This file |
| `prediction_registry_v1.tsv` | Machine-readable prediction registry (1 row, 13 columns) |
