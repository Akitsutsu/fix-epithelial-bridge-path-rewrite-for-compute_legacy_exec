# GSE246243 candidate value note v1

## Date
2026-04-10

## Scope
Repo-state candidate intake note. Not a governance change, not a
reference change, not a comparison-world refresh, not a lifecycle
refresh, not a prediction refresh, not a tranche promotion. No
existing artifact is replaced in this step.

---

## 1. Why GSE246243 matters

GSE246243 is a same-line kinetic time series of iAT1 differentiation
on the BU3 NGAT iPSC line. It provides temporal resolution of the
L+DCI commitment shift already observed as an endpoint in GSE221342
(now canonical in comparison world v4).

| Sample | GSM | Condition | Timepoint |
|--------|-----|-----------|-----------|
| iAT2 3D | GSM7865483 | CK+DCI (baseline) | 3d post-passage |
| iAT1 24hr | GSM7865484 | L+DCI switch | 24hr |
| iAT1 48hr | GSM7865485 | L+DCI switch | 48hr |
| iAT1 72hr | GSM7865486 | L+DCI switch | 72hr |

## 2. Same-line kinetic tranche

**Yes, this is truly same-line kinetic.**

- Cell line: BU3 NGAT (confirmed from GEO sample characteristics).
- Same line as: GSE221342 (canonical v4), BU3 anchor query.
- Same lab: Kotton / Boston University.
- Same publication: Burgess et al. 2024, Cell Stem Cell (PMID:38642558).
- Same differentiation medium: CK+DCI → L+DCI switch.
- Difference from GSE221342: GSE246243 provides early kinetic
  timepoints (24/48/72hr) rather than culture-format endpoints
  (3D vs ALI). The two tranches are complementary, not redundant.

## 3. Public availability

All download surfaces are confirmed public from GEO:

| Surface | Status | Detail |
|---------|--------|--------|
| SOFT family | confirmed_public | standard GEO format |
| MINiML family | confirmed_public | standard GEO format |
| Series Matrix | confirmed_public | standard GEO format |
| RAW tar | confirmed_public | GSE246243_RAW.tar, 61.3 Mb |
| SRA | confirmed_public | SRX22226278–SRX22226281 |
| GSM7865483 H5 | confirmed_public | 15.4 Mb, CellRanger filtered |
| GSM7865484 H5 | confirmed_public | 16.2 Mb, CellRanger filtered |
| GSM7865485 H5 | confirmed_public | 16.1 Mb, CellRanger filtered |
| GSM7865486 H5 | confirmed_public | 13.5 Mb, CellRanger filtered |

Per-sample CellRanger filtered H5 files are directly available on
each GSM page. Same format as GSE221342. Platform is GPL30173
(NextSeq 2000), sequencing on 10x Chromium. BioProject: PRJNA1032111.

No substantial conversion workflow is required — standard H5-to-H5AD
conversion path, identical to GSE221342.

## 4. What claim it could strengthen

GSE246243 could strengthen P-0002 (alveolar epithelial commitment
direction) by adding temporal resolution to the commitment shift:

- **Kinetic gradient**: if the 24/48/72hr timepoints show a
  progressive shift of epithelial_top_state_fine toward SOX2lowCFTR+
  cells, this would demonstrate that the commitment direction
  develops gradually over time on the same line already known to
  reach SOX2lowCFTR+ at endpoint (GSE221342 iAT1 3D/ALI).
- **Quality trajectory**: tracking off-target and ambiguity across
  timepoints could show whether projection quality improves,
  degrades, or is stable during early commitment.
- **Intermediate identity**: the 24hr and 48hr samples might capture
  intermediate states not visible at endpoint, providing finer
  resolution of the commitment trajectory.

This is valuable for commitment-level closure because it adds a
within-line temporal axis to the existing cross-line endpoint evidence.

## 5. What it cannot yet close by itself

- **Full alveolarization.** GSE246243 is 3D L+DCI kinetic — it does
  not include ALI, spatial, or morphogenesis evidence. The endpoint
  at 72hr is expected to be short of the GSE221342 ALI p1 (78.0%
  SOX2lowCFTR+) because 72hr is early relative to the full
  differentiation protocol.
- **Cross-line replication.** GSE246243 is the same line (BU3 NGAT)
  as GSE221342. It does not add a new cell line.
- **P-0001 closure.** BU3 NGAT ≠ SPC2-ST-B2. This remains
  cross-line supportive, not same-line P-0001 validation.
- **Reference independence.** Like all current evidence, this would
  be projected on reference v1 only.

## 6. Not yet canonical

GSE246243 is a candidate tranche only. It is not in the current
comparison world, lifecycle registry, or any review lane. No
query-ready review has been performed. No binary data has been
downloaded or committed.

## 7. Recommendation

The next step should be **local acquisition and conversion**, not
query-ready review. Specifically:

1. Download the 4 per-GSM CellRanger filtered H5 files (total ~61 Mb).
2. Run the standard H5-to-H5AD conversion (same path as GSE221342).
3. Confirm gene-space overlap with reference v1.
4. Only then proceed to projection and query-ready review.

This is low-friction because the processed H5 files are directly
available and the format is identical to GSE221342. No SRA-only
fallback or custom conversion is needed.

Do not promote GSE246243 into the canonical comparison world in this
step or the next acquisition step. Promotion requires a complete
query-ready review (gates A–D).

---

## 8. Explicit stop line

- reports/comparison_world_biology_summary_v4/: not changed
- reports/artifact_lifecycle_registry_v3/: not changed
- reports/prediction_registry_v2/: not changed
- reports/contrast_registry_v1/: not changed
- data_contract.yaml: not changed
- decision_log.md: not changed
- research_scope.md: not changed
- No binary data committed
- No conversion executed
- No projection executed
- No query-ready review performed
- No canonical migration in this step
