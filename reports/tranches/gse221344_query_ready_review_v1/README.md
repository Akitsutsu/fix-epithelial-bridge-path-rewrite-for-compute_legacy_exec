# GSE221344 Query-Ready Review v1

## Review date
2026-04-08

## Dataset
- GSE221344: iPSC-derived iAT2 organoids with YAP lentiviral perturbation
- Kotton lab / Boston University / Center for Regenerative Medicine
- 2 samples, single donor cell line SPC2-ST-B2, no multiplexing
- Lentiviral constructs: pHAGE2-EF1aL-WTYAP-UBC-tagBFP-WPRE (control)
  and pHAGE2-EF1aL-YAP5SA-UBC-tagBFP-WPRE (perturbation)

## Reference
- Release v1: `converted/reference_RNA.h5ad` + `converted/reference_metadata_v1.csv`
- Stage axis: `sample_week`
- Execution: combined-root v2 canonical path

## Review scope
Explicit reviewer promotion decision for 2 rows previously at
`qc_status=local_validation_inspected_manual_review_required`,
`query_ready_flag=false`.

## Promotion scope
**Both rows promoted together as a paired perturbation tranche.**
No row excluded. The pair is the evidence unit.

| Row | Decision |
|-----|----------|
| GSM6858857_WT_YAP | **promote** |
| GSM6858858_YAP5SA | **promote** |

**Dataset-level decision**: Both rows promoted -> dataset-level
`query_ready_flag=true`, status `accepted_query_ready`,
role `nearest_external_validation`.

---

## Gate summary

### Gate A -- Object contract
Both pass. H5AD loadable, raw present, counts layer present, X
integer-valued, 91.98% reference gene overlap, obs/var columns intact,
modality = Gene Expression.

### Gate B -- Provenance / row identity
Both pass. Sample sheet row identity matches local objects. Source
accession, sample name, output paths, conversion script, cell counts all
consistent. Single donor cell line -- no demultiplexing needed.

### Gate C -- Projection smoke test
Both pass. Whole-lung and epithelial projections completed without errors
using canonical combined-root v2 path against current release v1.

| Sample | WL cells | WL Epi% | WL top stage | Epi eligible | Epi OT% | Epi ambig% |
|--------|------:|---:|---|------:|---:|---:|
| GSM6858857_WT_YAP | 5,532 | 98.2% | late_GW17_19 (78.9%) | 5,432 | 1.8% | 11.2% |
| GSM6858858_YAP5SA | 4,201 | 98.3% | late_GW17_19 (80.7%) | 4,130 | 1.7% | 24.2% |

### Gate D -- Within-tranche biology coherence
Both pass.

Key observations:
- Both map to late_GW17_19 / week_18 -- consistent with all other
  SPC2-ST-B2 tranches (GSE221343, GSE193716 iAEC2)
- Both are Proliferating progenitors dominant at epithelial level
- YAP5SA shows clear CFTR+ lineage enrichment relative to WT-YAP:
  - SOX2lowCFTR+: 5.6% vs 0.06% (100x)
  - NKX2-1+SOX9+CFTR+: 7.3% vs 0.07% (100x)
  - Combined CFTR+ lineage: ~13% vs ~0.1%
- The perturbation effect is perturbation-specific: same cell line, same
  medium, same timepoint -- only the YAP transgene differs
- WT-YAP shows Tip cells enrichment (29.9%) as a notable secondary
  feature, distinct from untransduced GSE221343 CK+DCI (Stromal-like
  cells 1 at 27.2%)
- The within-tranche comparison (control vs perturbation) is internally
  coherent and biologically interpretable on v1

---

## Evidence summary

Both rows are **Proliferating progenitors dominant** in the epithelial
remap:
- WT-YAP: 35.9%
- YAP5SA: 42.8%

YAP5SA shows a **partial shift toward CFTR+ lineage identity**:
- SOX2lowCFTR+ enrichment: 5.6% (vs 0.06% in WT-YAP)
- NKX2-1+SOX9+CFTR+: 7.3% (vs 0.07% in WT-YAP)
- This shift is **directionally consistent with P-0001** (which predicts
  iAT1-directed perturbation -> SOX2lowCFTR+)
- However, SOX2lowCFTR+ is **not the top state** in YAP5SA (only 5.6%).
  The P-0001 success condition requires SOX2lowCFTR+ as top state. This
  is a partial shift, not a complete identity conversion.

## Why paired promotion

The YAP5SA CFTR+ enrichment is only interpretable relative to its
matched lentiviral control (WT-YAP). Without WT-YAP:
- The 5.6% SOX2lowCFTR+ in YAP5SA could not be evaluated as a 100x
  enrichment
- YAP5SA alone would look like another Proliferating progenitors row
  with a minor SOX2lowCFTR+ component
- The perturbation-specificity of the signal would be undemonstrable

Conversely, WT-YAP alone has limited analytical value -- it is a
lentiviral control that provides the baseline for the YAP5SA comparison.

**The pair is the unit of evidence. Neither row carries its full
interpretive value without the other.**

## Why this is supportive same-line positive-arm evidence

GSE221344 provides directional support for the P-0001 hypothesis:
- Same iPSC line (SPC2-ST-B2) as the existing P-0001 basis tranches
- Explicit YAP-mediated perturbation (nuclear YAP drives AT1 program
  per Burgess 2024) enriches CFTR+ lineage cells ~100x
- The direction of the shift (toward SOX2lowCFTR+ / NKX2-1+SOX9+CFTR+)
  is consistent with what P-0001 predicts for iAT1-directed perturbations

This tranche complements but does not duplicate the existing evidence:
- GSE221343 L+DCI provides strong iAT1 conversion (SOX2lowCFTR+ dominant)
- GSE193716 iAEC2 provides culture-format-only baseline (Proliferating
  progenitors)
- **GSE221344 fills the middle**: explicit perturbation with partial
  but directional CFTR+ enrichment, with a matched lentiviral control

---

## Required caveats

### 1. WT-YAP is a lentiviral control, not an untransduced control
WT-YAP (GSM6858857) is transduced with a WT YAP lentivirus. The Tip
cells enrichment (29.9%) distinguishes it from the untransduced CK+DCI
control in GSE221343 (Stromal-like cells 1 at 27.2%). Comparisons
between WT-YAP and untransduced conditions must acknowledge that
lentiviral transduction itself may alter cell state.

### 2. YAP5SA shows a partial shift, not a top-state identity conversion
YAP5SA's top epithelial state is Proliferating progenitors (42.8%), not
SOX2lowCFTR+ (5.6%). This is a partial directional shift, not the
complete identity conversion seen in GSE221343 L+DCI (SOX2lowCFTR+ at
34.8%). The P-0001 success condition (SOX2lowCFTR+ as top state) is
not met by this tranche.

### 3. P-0001 remains registered/supportive, not confirmed
GSE221344 is recorded as supportive positive-arm evidence for P-0001.
The prediction status is NOT changed to confirmed or falsified.
Single-tranche closure of P-0001 is not claimed. A full cross-tranche
assessment combining GSE221344 (perturbation arm) with GSE193716
(culture-format arm) would be needed for any status change.

---

## Decisions

| Sample | Decision | Rationale |
|--------|----------|-----------|
| GSM6858857_WT_YAP | **promote** | Paired lentiviral control; technically clean epi projection (OT 1.8%, ambiguity 11.2%, align 0.744); provides the matched baseline that makes YAP5SA CFTR+ enrichment interpretable |
| GSM6858858_YAP5SA | **promote** | Paired perturbation arm; 100x CFTR+ lineage enrichment relative to WT-YAP; directionally supportive of P-0001; technically clean epi projection (OT 1.7%, align 0.715) |

**Dataset-level decision**: Both rows promoted -> `query_ready_flag=true`.

## What this review is NOT based on
- Paper expectations alone -- projections were run and evaluated
  independently
- P-0001 confirmation -- the prediction remains registered/supportive
- YAP5SA-only analysis -- the pair is the evidence unit
- Whole-lung off-target alone -- epi off-target (1.7-1.8%) is the
  relevant metric; whole-lung off-target (16.6-28.7%) reflects
  CellRanger-vs-paper cell populations, not a fundamental identity
  problem

## Explicit statements

- **No claim that P-0001 is confirmed.** P-0001 remains
  registered/supportive.
- **No single-tranche closure claim.** GSE221344 provides one side
  of the evidence (perturbation arm); the culture-format-only arm
  is in GSE193716.
- **Comparison-world refresh is deferred** to a separate reports-only
  PR after this promotion merges.

## Artifacts
- `gse221344_query_ready_decisions_v1.tsv` -- machine-readable decision
  table (2 rows)
- `benchmark_review_gse221344_v1/` -- projection run outputs (local,
  not committed)
