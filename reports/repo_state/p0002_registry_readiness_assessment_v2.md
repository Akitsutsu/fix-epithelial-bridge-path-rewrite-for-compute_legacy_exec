# P-0002 registry readiness assessment v2

## Date
2026-04-10

## Scope
Repo-state reassessment note. Not a governance change, not a reference
change, not a prediction registration step, not a comparison-world
refresh. No existing artifact is replaced in this step. This note
reassesses P-0002 registry readiness after the primary blocker
identified in assessment v1 was resolved by PR #55.

---

## 1. Why now

Assessment v1 (PR #54) found a single primary blocker:

> **B — not_ready_primary_future_contrast_not_canonical**
>
> P-0002's primary validation candidate (GSE221342) was not in the
> current canonical comparison world.

PR #55 promoted GSE221342 into comparison world v4 (24 rows, 8
tranche components) and lifecycle registry v3. The old blocker must
now be re-tested to determine whether P-0002 is structurally
registrable.

## 2. Current stable baseline

| Surface | Version | Content |
|---------|---------|---------|
| Comparison world | v4 | 24 rows, 8 tranche components, all 25 columns populated |
| Lifecycle registry | v3 | 8 tranches, GSE221342 included |
| Prediction registry | v1 | P-0001 only, anchored to comparison world v2 |
| Contrast registry | v1 skeleton | 3 proposed entries (C-0001, C-0002, C-0003), non-canonical |

P-0002 currently exists only as a repo-state design note
(`p0002_alveolar_commitment_design_v1.md`). No registry row exists.

## 3. What changed since readiness v1

| Blocker from v1 | Status now |
|-----------------|-----------|
| GSE221342 not in canonical comparison world | **Resolved.** 4 GSE221342 rows in comparison world v4, lifecycle v3. |
| Prediction registry anchored to v2 | **Unchanged.** Still v1 with P-0001 only. Minor issue. |
| Success/falsification criteria slightly design-level | **Unchanged.** Criteria exist but could be tightened. Minor issue. |
| Contrast registry too skeletal | **Unchanged.** Still 3 proposed entries. Secondary issue. |

The primary blocker is resolved. The remaining issues are minor or
secondary and do not individually block registration.

## 4. Readiness questions

### Q1. Is P-0002 now expressible using current canonical rows only?

**Yes.** The design note's signal set — GSE221343 L+DCI (SOX2lowCFTR+),
GSE289846 LATS-IN-1 (SOX2lowCFTR+), GSE193716 iAEC2 (Proliferating
progenitors), GSE221344 YAP5SA (partial positive-arm) — is all
canonical in v4. The primary candidate (GSE221342 directional gradient)
is now also canonical. P-0002's entire basis and validation target
are expressible from current canonical rows.

### Q2. Does canonical inclusion of GSE221342 resolve the primary validation-basis problem?

**Yes.** GSE221342 is now in comparison world v4 with accepted_query_ready
status. Its 4-point directional gradient (iAT2 → iAT1 3D → ALI p0 →
ALI p1) is the strongest candidate for testing alveolar epithelial
commitment. The structural inconsistency flagged in v1 — registering a
prediction whose test case was locally available but not canonical — is
eliminated.

### Q3. Does P-0002 still need a clearly prospective validation target that is not already canonical?

**No.** P-0001 was prospective because its validation target was a
future external tranche. P-0002 is different: its evidence base
(GSE221342) is already canonical. This is not a structural problem —
P-0002 functions as a retrospective prediction that formalizes an
existing signal into a testable statement. The design note's
success/falsification criteria can be evaluated against current
canonical data directly, or against future replication tranches.

### Q4. Is prediction_registry_v1 being anchored to v2 a blocker?

**No longer a blocker.** P-0001 references `current_world_version=v2`,
but comparison world has been through v3 and v4 since then.
A registration PR would create `prediction_registry_v2` with P-0001
carried forward (world version updated to v4) and P-0002 added. This
is a mechanical version bump, not a conceptual blocker.

### Q5. Are success/falsification criteria concrete enough?

**Yes, sufficient for registration.** The design note's criteria use
the 5 existing epithelial columns with explicit delta thresholds
(off-target increase ≤ 10pp, ambiguity ≤ 60%). These are more
nuanced than P-0001's absolute top-state assertions, but appropriate
for a commitment endpoint. They can be tightened further in the
registry row itself if desired.

### Q6. Is contrast_registry_v1 sufficient support?

**Not required for registration.** The contrast registry is a proposed
side layer. P-0002 does not depend on it — P-0002's success/falsification
criteria reference canonical comparison-world rows directly. Contrast
registry support is a future enhancement, not a prerequisite.

## 5. Primary outcome

**A — ready_for_tiny_registration_pr**

All structural prerequisites are now met:
- P-0002's basis rows are canonical (v4).
- P-0002's primary validation candidate (GSE221342) is canonical (v4).
- Success/falsification criteria are concrete and bounded to the
  5-column epithelial surface.
- The prediction_registry version gap is mechanically resolvable.
- No conceptual blocker remains.

## 6. Recommendation

P-0002 is ready for formal registration. The next step is a **tiny
dedicated registration PR** that:

1. Creates `reports/prediction_registry_v2/`.
2. Carries forward P-0001 with `current_world_version` updated to v4.
3. Adds a P-0002 row with:
   - endpoint: alveolar epithelial commitment
   - basis: current canonical rows (GSE221343, GSE289846, GSE193716,
     GSE221344 as signal; GSE221342 as validation target)
   - success/falsification: from the design note, bounded to 5
     epithelial columns
4. Updates the prediction registry README.
5. Does not edit comparison world, lifecycle, contrast registry, or
   governance files.

**Do not register P-0002 in this step.** This step only confirms
readiness. The registration itself is a separate PR.

---

## 7. Explicit stop line

- reports/comparison_world_biology_summary_v4/: not changed
- reports/artifact_lifecycle_registry_v3/: not changed
- reports/prediction_registry_v1/: not changed
- reports/contrast_registry_v1/: not changed
- data_contract.yaml: not changed
- decision_log.md: not changed
- research_scope.md: not changed
- No new TSV or XLSX
- No new registry implementation
- No new canonical migration in this step
- No prediction registered in this step
