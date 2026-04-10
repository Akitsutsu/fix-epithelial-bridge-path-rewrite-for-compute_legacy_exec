# GSE246243 Query-Ready Review v1

## Review date
2026-04-10

## Dataset
- GSE246243: Time Series of differentiation from human iAT2s to iAT1s in L+DCI medium
- Kotton lab / Boston University / Center for Regenerative Medicine
- 4 samples, single donor cell line BU3 NGAT, no multiplexing
- Same iPSC line as BU3 anchor query and GSE221342
- Same-line kinetic strengthening tranche for P-0002

## Reference
- Release v1: `converted/reference_RNA.h5ad` + `converted/reference_metadata_v1.csv`
- Stage axis: `sample_week`
- Execution: combined-root v2 canonical path

## Promotion scope
**All 4 rows promoted together as a same-line kinetic tranche.**

| Row | Decision |
|-----|----------|
| GSM7865483_iAT2_3D | **promote** |
| GSM7865484_iAT1_24hr | **promote** |
| GSM7865485_iAT1_48hr | **promote** |
| GSM7865486_iAT1_72hr | **promote** |

**Dataset-level decision**: All 4 rows promoted -> `query_ready_flag=true`,
status `accepted_query_ready`, role `nearest_external_validation`.

---

## Gate summary

### Gate A -- Object contract
All 4 pass. CellRanger filtered H5 from GEO, converted to H5AD via
standard scanpy path. 58,397 features per sample, 28,378/30,852
(91.98%) reference gene overlap — identical to GSE221342/GSE221343.

### Gate B -- Provenance / row identity
All 4 pass. Single donor cell line BU3 NGAT. No demultiplexing needed.
Same line as BU3 anchor and GSE221342.

### Gate C -- Projection smoke test
All 4 pass.

| Sample | Cells | WL Epi% | WL top stage | Epi eligible | Epi OT% | Epi ambig% |
|--------|------:|---:|---|------:|---:|---:|
| iAT2 3D | 2,767 | 95.4% | late_GW17_19 (77.8%) | 2,639 | 4.6% | 25.3% |
| iAT1 24hr | 2,410 | 97.6% | late_GW17_19 (91.1%) | 2,351 | 2.4% | 15.5% |
| iAT1 48hr | 2,449 | 98.8% | late_GW17_19 (96.2%) | 2,420 | 1.2% | 13.6% |
| iAT1 72hr | 2,510 | 99.4% | late_GW17_19 (84.2%) | 2,496 | 0.6% | 13.8% |

### Gate D -- Within-tranche biology coherence
All 4 pass. Clear kinetic progression:

| Sample | Epi top state | Epi OT% | Epi ambig% |
|--------|--------------|------:|------:|
| iAT2 3D (t=0) | **Proliferating progenitors** (44.5%) | 4.6 | 25.3 |
| iAT1 24hr | **Proliferating progenitors** (71.7%) | 2.4 | 15.5 |
| iAT1 48hr | **Proliferating progenitors** (45.5%) | 1.2 | 13.6 |
| iAT1 72hr | **SOX2lowCFTR+ cells** (53.6%) | 0.6 | 13.8 |

The series shows a directional shift toward alveolar commitment:
baseline Proliferating progenitors → progenitor expansion at 24hr →
transitional state at 48hr → SOX2lowCFTR+ emergence at 72hr. Off-target
improves monotonically (4.6 → 0.6). Ambiguity improves from baseline
and stabilizes (~14%).

---

## Key findings

### 1. Is GSE246243 query-ready?

**Yes.** All 4 gates pass. Cell counts are healthy (2,410–2,767).
Gene-space overlap is excellent (91.98%). Quality metrics are within
accepted ranges for all rows.

### 2. Does the series behave as a same-line kinetic strengthening tranche?

**Yes.** The 4-point kinetic series on BU3 NGAT shows temporal
progression from Proliferating progenitors (baseline) to SOX2lowCFTR+
cells (72hr). This adds temporal resolution to the L+DCI commitment
shift already observed at endpoint in GSE221342 (same line).

The kinetic structure is:
- **t=0 (iAT2 3D):** Proliferating progenitors dominant (44.5%).
  Progenitor baseline before L+DCI switch.
- **24hr:** Proliferating progenitors strengthens to 71.7%. Initial
  progenitor expansion phase, not yet committed.
- **48hr:** Proliferating progenitors drops back (45.5%). Transitional
  heterogeneity. SOX2lowCFTR+ begins emerging at sub-top-state level.
- **72hr:** SOX2lowCFTR+ cells becomes top state (53.6%).
  Commitment direction is now visible at the top-state level.

### 3. Does it strengthen P-0002 at the commitment level?

**Yes.** P-0002 predicts that directed distal/alveolar conditions
show a directional shift toward SOX2lowCFTR+ cells. GSE246243
demonstrates this shift develops progressively over 72 hours of
L+DCI exposure on the same BU3 NGAT line already known to reach
SOX2lowCFTR+ at endpoint (GSE221342). The temporal resolution
confirms that commitment is a gradual process, not an artifact of
endpoint selection.

### 4. What it cannot close by itself

- **Full alveolarization.** 72hr is an early kinetic point. The
  SOX2lowCFTR+ fraction (53.6%) is lower than GSE221342 endpoints
  (iAT1 3D: 60.9%, ALI p1: 78.0%).
- **Cross-line replication.** Same line as GSE221342 (BU3 NGAT).
  Does not add a new cell line.
- **P-0001 closure.** BU3 NGAT ≠ SPC2-ST-B2. Cross-line supportive
  only.
- **Baseline difference.** GSE246243 baseline is Proliferating
  progenitors (44.5%), not Budtip progenitors (GSE221342 baseline
  24.5%). This may reflect timing differences (3d post-passage vs
  unspecified) or passage conditions. The commitment direction is
  preserved despite the different starting state.

### This is NOT a P-0001 validation tranche
BU3 NGAT is a different iPSC line from SPC2-ST-B2. The kinetic
SOX2lowCFTR+ shift is cross-line supportive evidence for the general
direction, not same-line P-0001 validation.

---

## Decisions

| Sample | Decision | Rationale |
|--------|----------|-----------|
| GSM7865483_iAT2_3D | **promote** | kinetic t=0 baseline; Proliferating progenitors; defines series starting point |
| GSM7865484_iAT1_24hr | **promote** | early kinetic; initial progenitor expansion; quality improving |
| GSM7865485_iAT1_48hr | **promote** | mid kinetic; transitional state; quality continues improving |
| GSM7865486_iAT1_72hr | **promote** | kinetic endpoint; SOX2lowCFTR+ top state (53.6%); confirms directional shift |

## Artifacts
- `gse246243_query_ready_decisions_v1.tsv` -- machine-readable decision table (4 rows)
