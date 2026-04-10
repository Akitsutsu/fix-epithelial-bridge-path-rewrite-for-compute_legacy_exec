# Prediction Registry v2

## Date
2026-04-10

## Supersedes
`reports/prediction_registry_v1/` (1 prediction, world basis v2).
v1 is retained as a historical snapshot and is not deleted.

## Purpose
Register prospective and retrospective hypotheses derived from the
current comparison world. This registry is **not** a new canonical
biology source — it is a prediction index that records what the
current world predicts and how each prediction can be validated or
falsified.

## What changed from v1

| Change | v1 | v2 |
|--------|----|----|
| Predictions | 1 (P-0001) | 2 (P-0001 + P-0002) |
| Current world basis | v2 | v4 |
| P-0001 | registered, prospective | carried forward, world updated to v4 |
| P-0002 | -- | registered, retrospective canonical |

## Current comparison world used as basis
`reports/comparison_world_biology_summary_v4/` (24 rows, 8 components).

---

## P-0001: same-line perturbation direction (carried forward)

Carried forward from v1 with `current_world_version` updated to v4.
All hypothesis, success, and falsification logic are unchanged.
See v1 README for full rationale.

**Short summary:** within same-line SPC2-ST-B2, explicit iAT1-directed
perturbation drives epithelial_top_state_fine toward SOX2lowCFTR+
cells, while culture-format-only variation retains Proliferating
progenitors. Validation target: next same-line SPC2-ST-B2 tranche
with iAT1-directed condition split (prospective).

**Status:** registered.

---

## P-0002: alveolar epithelial commitment direction

### Why P-0002 now
The P-0002 design note (PR #53) fixed the endpoint at alveolar
epithelial commitment — not full alveolarization. The readiness
assessment v2 (PR #56) confirmed that the primary blocker (GSE221342
non-canonical) was resolved by its promotion into comparison world v4
(PR #55). All structural prerequisites for registration are met.

### Endpoint
**Alveolar epithelial commitment on the native fetal reference axis.**
This is explicitly not full alveolarization, alveologenesis, or
morphogenesis. Success and falsification are bounded to the 5 existing
epithelial columns. `epi_alignment` is not required.

### Basis
Signal tranches: GSE221343, GSE289846, GSE193716 (iAEC2 subset),
GSE221344 (supportive partial positive-arm).

Validation target: GSE221342 (retrospective canonical tranche — 4 rows
now in comparison world v4).

### Contrast registry
`reports/contrast_registry_v1/` is a proposed side layer and is not
required for P-0002 registration. P-0002 references canonical
comparison-world rows directly.

### Framing
P-0002 uses **retrospective canonical framing**: its validation target
(GSE221342) is already in the current comparison world. This differs
from P-0001's prospective external framing. Future replication on
additional iPSC lines can further refine or falsify P-0002.

### GSE221342 and P-0001
GSE221342 is **not** a same-line P-0001 validation tranche. BU3 NGAT
is a different iPSC line from SPC2-ST-B2. The cross-line SOX2lowCFTR+
replication is supportive evidence for the general direction but does
not close P-0001.

**Status:** registered.

---

## Explicit stop line
- **No new intake** registered by this artifact
- **No projection rerun** performed
- **No query-ready change** made
- **No governance file edited** (data_contract.yaml, decision_log.md,
  research_scope.md are unchanged)
- **No modification** to comparison_world_biology_summary_v4/ or
  artifact_lifecycle_registry_v3/
- **No contrast registry change**
- **No epi_alignment adoption**

## Files in this directory

| File | Description |
|------|-------------|
| `README.md` | This file |
| `prediction_registry_v2.tsv` | Machine-readable prediction registry (2 rows, 13 columns) |
