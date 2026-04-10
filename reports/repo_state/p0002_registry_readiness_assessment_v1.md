# P-0002 registry readiness assessment v1

## Date
2026-04-10

## Scope
Repo-state assessment note. Not a governance change, not a reference
change, not a prediction registration step, not a comparison-world
refresh. No existing artifact is replaced in this step. This note
assesses whether the merged P-0002 alveolar commitment design note is
mature enough for a formal prediction registry entry.

---

## 1. Why now

The P-0002 alveolar commitment design note (PR #53) fixed the initial
endpoint, candidate contrast family, and success/falsification criteria
at the design level. That note explicitly deferred formal registration
and said the earliest next step is a small follow-up note deciding
whether P-0002 is mature enough. This is that follow-up — a bounded
readiness check, not scope expansion.

## 2. Current stable baseline

| Surface | Version | Content |
|---------|---------|---------|
| Comparison world | v3 | 20 rows, 7 tranche components, all 25 columns populated |
| Lifecycle registry | v2 | 7 tranches |
| Prediction registry | v1 | P-0001 only, anchored to comparison world v2 |
| Contrast registry | v1 skeleton | 3 proposed entries (C-0001, C-0002, C-0003), non-canonical |

P-0002 currently exists only as a repo-state design note. No registry
row, no TSV entry, no canonical surface reference.

## 3. What P-0002 already has

The design note provides:
- **Endpoint:** alveolar epithelial commitment (not full alveolarization).
- **Success condition:** bounded to the 5 existing epithelial columns,
  with explicit thresholds for off-target and ambiguity deltas.
- **Falsification condition:** bounded to the same 5 columns, with
  concrete criteria for null-control equivalence, no-movement, and
  degradation-driven artifacts.
- **Candidate contrast family:** narrowly defined (GSE221342 primary,
  GSE193716 boundary, GSE221343/GSE289846/GSE221344 supportive).
- **Deferrals:** epi_alignment, combined-root, full alveolarization,
  spatial/morphogenesis — all explicitly out of scope.

These are genuine strengths. The design note is well-bounded and the
success/falsification criteria are concrete at the column level. The
question is whether the structural prerequisites for a registry entry
are also in place.

## 4. Readiness questions

### Q1. Is P-0002 expressible using current canonical rows only?

**Partially.** The current canonical signal — GSE221343 L+DCI
(SOX2lowCFTR+), GSE289846 LATS-IN-1 (SOX2lowCFTR+), GSE193716 iAEC2
(Proliferating progenitors), GSE221344 YAP5SA (partial positive-arm) —
is sufficient to motivate the prediction direction. However, the
strongest validation candidate (GSE221342 directional gradient) is not
in comparison world v3.

### Q2. Is the absence of GSE221342 from comparison world v3 a blocker?

**Yes, this is the primary blocker.** P-0001 was registered cleanly
because its validation target was a genuinely prospective future
tranche ("next same-line SPC2-ST-B2 tranche"). P-0002's primary
candidate (GSE221342) already exists locally, has been processed
through whole-lung and epithelial projection, and appears in the
contrast registry skeleton as C-0002 with worked-example values.

Registering P-0002 while its primary evidence base sits in a
non-canonical state would create a structural inconsistency: the
"prospective" validation target is already partially evaluated but
not formally promoted. This is different from P-0001's clean
prospective design and would weaken the registry's epistemic
integrity.

### Q3. Is prediction_registry_v1 anchored to v2 a blocker?

**Minor, not primary.** P-0001 references `current_world_version=v2`.
Current world is v3. Adding a P-0002 row referencing v3 would create
a mixed registry. This is resolvable (either update the registry to
v2 format with a v3 note, or create prediction_registry_v2), but it
is secondary to Q2.

### Q4. Are success/falsification criteria concrete enough?

**Nearly.** The design note uses relative language ("moves toward",
"does not increase by more than X points"), which is appropriate for
a commitment endpoint. P-0001 uses absolute language
("epithelial_top_state_fine = SOX2lowCFTR+"). P-0002's criteria are
slightly more design-level but could be tightened for a registry row
without fundamental rework.

### Q5. Does contrast_registry_v1 provide enough support?

**Not yet.** All 3 entries are `proposed` status. C-0002 (the entry
most relevant to P-0002) references GSE221342, which is not in the
comparison world. The contrast layer is still a proposed side layer,
not an operational support structure for predictions. This is a
secondary gap, not the primary blocker.

## 5. Primary outcome

**B — not_ready_primary_future_contrast_not_canonical**

P-0002 is well-designed at the endpoint and criteria level, but its
primary validation candidate (GSE221342) is not in the current
canonical comparison world. Registering a prediction whose strongest
test case is already locally available but not formally promoted would
create a structural inconsistency that P-0001 avoided by targeting a
genuinely external future tranche.

## 6. Recommendation

**Do not register P-0002 now.**

- Do not edit `reports/prediction_registry_v1/`.
- Do not create `prediction_registry_v2`.
- Do not add a P-0002 row anywhere.

**Smallest acceptable next prerequisite:** bring GSE221342 into the
canonical comparison world through its own intake/review/promotion
cycle. GSE221342 already has local projection outputs and contrast
skeleton coverage (C-0002). The minimum path is:

1. Complete GSE221342 query-ready review (gate A–D evaluation).
2. If accepted, promote GSE221342 into comparison world (v4 or
   in-place v3 extension, depending on policy at that time).
3. Only after GSE221342 is canonical, revisit P-0002 registration.

This keeps the registry clean: P-0002 would reference canonical
basis rows for its signal and a canonical validation target for its
test, just as P-0001 does.

**Alternative path (if GSE221342 promotion is deferred indefinitely):**
reformulate P-0002 to target a genuinely external future tranche
(analogous to P-0001's "next same-line" framing), removing the
dependency on GSE221342 being canonical. This is a weaker but
structurally clean option.

---

## 7. Explicit stop line

- reports/comparison_world_biology_summary_v3/: not changed
- reports/artifact_lifecycle_registry_v2/: not changed
- reports/prediction_registry_v1/: not changed
- reports/contrast_registry_v1/: not changed
- data_contract.yaml: not changed
- decision_log.md: not changed
- research_scope.md: not changed
- No new TSV or XLSX
- No new registry implementation
- No new canonical migration in this step
- No prediction registered in this step
