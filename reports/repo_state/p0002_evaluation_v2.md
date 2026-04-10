# P-0002 evaluation v2

## Date
2026-04-10

## Scope
Repo-state evaluation note. Not a governance change, not a reference
change, not a prediction refresh, not a comparison-world refresh. No
existing artifact is replaced in this step. This note re-evaluates
P-0002 on the current canonical v5 basis, which now includes the
GSE246243 same-line kinetic tranche.

## Supersedes
`reports/repo_state/p0002_evaluation_v1.md` (evaluated on v4 basis).
v1 is retained as a historical snapshot.

---

## 1. Why now

P-0002 evaluation v1 concluded `support_on_current_canonical_basis`
using comparison world v4. v5 now includes GSE246243 — a 4-point
same-line kinetic time series on BU3 NGAT showing temporal
progression toward SOX2lowCFTR+ cells. The open question is whether
this kinetic evidence strengthens, leaves unchanged, or materially
changes the v4 support claim.

## 2. Evaluation basis

| Family | Rows | Role |
|--------|------|------|
| **Retrospective canonical validation** | GSM6858850–53 (GSE221342) | Endpoint directional gradient |
| **Same-line kinetic strengthening** | GSM7865483–86 (GSE246243) | Temporal progression (new in v5) |
| **Supportive same-direction** | GSM6858856_L_DCI, GSE289846_3i_LATS_Day14 | Cross-line iAT1-directed lanes |
| **Null / falsification family** | GSM5819133–35 (GSE193716) | Format-only controls |
| **Supportive-only** | GSM6858858_YAP5SA (GSE221344) | Partial positive-arm; not counted |

GSE221344 remains supportive-only. GSE246243 is not a same-line
P-0001 validation tranche (BU3 NGAT ≠ SPC2-ST-B2). GSE246243 is
not full alveolarization evidence (72hr is early kinetic).

## 3. Fixed interpretation rules

- Wording: 1b ("shows a directional shift toward alveolar commitment")
- Thresholds: guardrails only, not hard pass/fail
- GSE221344: supportive-only, not confirmatory

These are unchanged from evaluation v1.

## 4. What v5 adds over v4

Evaluation v1 had the GSE221342 endpoint gradient (Budtip → SOX2lowCFTR+
60.9–78.0%) as the primary evidence. v5 adds temporal resolution from
GSE246243 on the same BU3 NGAT line:

| GSE246243 row | Epi top state | Off-target | Ambiguity |
|---------------|--------------|-----------|-----------|
| iAT2_3D (t=0) | Proliferating progenitors (44.5%) | 4.6 | 25.3 |
| iAT1_24hr | Proliferating progenitors (71.7%) | 2.4 | 15.5 |
| iAT1_48hr | Proliferating progenitors (45.5%) | 1.2 | 13.6 |
| iAT1_72hr | **SOX2lowCFTR+ cells (53.6%)** | 0.6 | 13.8 |

This adds three qualitatively new pieces:

1. **Temporal ordering.** The commitment shift develops progressively
   over 72 hours, not as an artifact of endpoint-only sampling.
2. **Intermediate states.** The 24hr progenitor expansion phase and
   48hr transitional state were not visible in the endpoint-only
   GSE221342 gradient.
3. **Quality improvement trajectory.** Off-target improves
   monotonically across the kinetic series (4.6 → 0.6), confirming
   the shift is not degradation-driven.

## 5. Support criteria re-evaluation

### (a) Directional shift — strengthened

v4 evidence: GSE221342 endpoint gradient shows Budtip → SOX2lowCFTR+.

v5 adds: GSE246243 kinetic series shows the same line (BU3 NGAT)
progressing from Proliferating progenitors → SOX2lowCFTR+ over 72
hours of L+DCI exposure. The 72hr timepoint (53.6% SOX2lowCFTR+) is
consistent with the GSE221342 3D L+DCI endpoint (60.9%). The kinetic
trajectory confirms the directional shift is temporally progressive.

**Condition (a): met, strengthened by kinetic confirmation.**

### (b) Quality guardrails — strengthened

v4 evidence: GSE221342 off-target improved along gradient (4.8 → 0.9).

v5 adds: GSE246243 off-target also improves monotonically (4.6 → 0.6).
Ambiguity improves from baseline (25.3 → 13.8). The kinetic trajectory
confirms the quality improvement is not a feature of endpoint selection
but develops progressively.

**Condition (b): met, strengthened by kinetic trajectory.**

### (c) Not contradicted — unchanged

Supportive lanes (GSE221343 L+DCI, GSE289846 LATS-IN-1) still confirm
SOX2lowCFTR+ direction. No new contradiction.

**Condition (c): met, unchanged from v1.**

### Falsification — still not triggered

No falsification condition is triggered:
- (i) Format-only controls (GSE193716) still retain Proliferating
  progenitors.
- (ii) GSE221342 directed rows still separate clearly from baseline.
- (iii) GSE246243 kinetic series shows clear directional ordering,
  not noise or degradation.
- (iv) Supportive lanes remain consistent.

## 6. Primary outcome

**A — support_strengthened_on_current_canonical_basis**

The v5 basis strengthens the v4 support claim in two concrete ways:

1. **Temporal confirmation.** The commitment shift is now shown to
   develop progressively (0 → 24 → 48 → 72hr), not just at endpoint.
   This rules out the possibility that the GSE221342 endpoint signal
   is an artifact of sampling the final state only.

2. **Quality trajectory confirmation.** The monotonic off-target
   improvement across the kinetic series independently confirms that
   the shift reflects genuine identity change, not projection
   degradation.

The claim remains bounded at alveolar epithelial commitment. It does
not extend to full alveolarization.

## 7. Comparison: v1 vs v2 evaluation

| Aspect | v1 (on v4) | v2 (on v5) |
|--------|-----------|-----------|
| Primary outcome | support | support_strengthened |
| Endpoint gradient | yes (GSE221342) | yes (unchanged) |
| Kinetic confirmation | absent | **yes** (GSE246243) |
| Quality trajectory | endpoint only | **temporal + endpoint** |
| Cross-line replication | 3 lines | 3 lines (unchanged) |
| Format-only null | holds | holds (unchanged) |
| Falsification triggered | no | no |

The v5 evaluation is qualitatively stronger than v4 because kinetic
temporal evidence is a different type of support than endpoint
evidence. Having both is stronger than either alone.

## 8. Limitations (updated)

1. **Retrospective framing.** Both GSE221342 and GSE246243 were
   canonical before evaluation. A prospective external replication
   would still strengthen the claim further.
2. **Same line, same lab.** GSE246243 adds kinetic resolution but not
   a new cell line or lab. Cross-line/cross-lab confirmation remains
   at the endpoint level (3 lines, 2 labs).
3. **Commitment level only.** GSE246243's 72hr SOX2lowCFTR+ (53.6%)
   is weaker than GSE221342's ALI p1 (78.0%). Full alveolarization
   is not claimed.
4. **Reference v1 dependent.** All evidence on same reference.
5. **GSE221344 not counted.** Supportive-only, as before.

## 9. Recommendation

The current v5 canonical basis supports a strengthened but still
commitment-level statement. Specifically:

- P-0002 remains registered with status `registered`.
- A future tiny registry update could record
  `support_strengthened_on_current_canonical_basis` if desired.
  This is optional, not required.
- Do not escalate to full alveolarization.
- Do not change prediction_registry_v2 in this step.

If prospective external replication on a new iPSC line becomes
available in the future, it would be the strongest possible next
step for P-0002 closure — but it is not required for the current
commitment-level support statement.

---

## 10. Explicit stop line

- reports/comparison_world_biology_summary_v5/: not changed
- reports/artifact_lifecycle_registry_v4/: not changed
- reports/prediction_registry_v2/: not changed
- reports/contrast_registry_v1/: not changed
- data_contract.yaml: not changed
- decision_log.md: not changed
- research_scope.md: not changed
- No new TSV or XLSX
- No new implementation
- No canonical migration in this step
