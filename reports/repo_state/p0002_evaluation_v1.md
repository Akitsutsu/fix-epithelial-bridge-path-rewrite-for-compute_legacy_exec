# P-0002 evaluation v1

## Date
2026-04-10

## Scope
Repo-state evaluation note. Not a governance change, not a reference
change, not a prediction refresh, not a comparison-world refresh. No
existing artifact is replaced in this step. This note evaluates P-0002
on the current canonical basis only.

---

## 1. Why now

P-0002 is registered in prediction_registry_v2 with
`current_world_version=v4` and `validation_target_type=
retrospective_canonical_tranche`. Its validation target (GSE221342)
and all basis rows are now canonical. The open question is no longer
registration readiness — it is whether the current canonical evidence
supports, falsifies, or leaves P-0002 borderline.

## 2. Evaluation basis

| Family | Rows | Role |
|--------|------|------|
| **Retrospective canonical validation** | GSM6858850_iAT2_3D (control), GSM6858851_iAT1_3D, GSM6858852_iAT1_ALI_p0, GSM6858853_iAT1_ALI_p1 | GSE221342 directional gradient |
| **Supportive same-direction** | GSM6858856_L_DCI (GSE221343), GSE289846_3i_LATS_Day14 (GSE289846) | Canonical iAT1-directed lanes |
| **Null / falsification family** | GSM5819133_iAEC2_3D, GSM5819134_iAEC2_3D_insert, GSM5819135_iAEC2_MRC5_insert | GSE193716 format-only controls |
| **Supportive-only** | GSM6858858_YAP5SA (GSE221344) | Partial positive-arm; not counted toward success |

Evaluation is based on canonical v4 rows. The contrast pilot is used
as interpretive supplement only. GSE221344 remains supportive-only
and does not contribute to the success determination.

## 3. Fixed interpretation rules

- Wording: 1b ("shows a directional shift toward alveolar commitment")
- Thresholds: guardrails only, not hard pass/fail
- GSE221344: supportive-only, not confirmatory

These are fixed for this evaluation and are not reopened here.

## 4. Support criteria evaluation

### (a) Directional shift

| Row | epithelial_top_state_fine | vs baseline |
|-----|-------------------------|-------------|
| GSM6858850_iAT2_3D (baseline) | Budtip progenitors | — |
| GSM6858851_iAT1_3D | SOX2lowCFTR+ cells | shifted |
| GSM6858852_iAT1_ALI_p0 | SOX2lowCFTR+ cells | shifted |
| GSM6858853_iAT1_ALI_p1 | SOX2lowCFTR+ cells | shifted |

All 3 directed rows show a directional shift of epithelial_top_state_fine
from Budtip progenitors to SOX2lowCFTR+ cells. The shift is a clear
top-state identity change, not a sub-top-state enrichment.

**Condition (a): met.**

### (b) Quality guardrails

| Row | off-target | delta vs baseline | ambiguity | delta vs baseline |
|-----|-----------|-------------------|-----------|-------------------|
| iAT2_3D (baseline) | 4.8 | — | 15.6 | — |
| iAT1_3D | 3.9 | −0.9 (improved) | 22.2 | +6.6 |
| iAT1_ALI_p0 | 2.1 | −2.7 (improved) | 18.2 | +2.6 |
| iAT1_ALI_p1 | 0.9 | −3.9 (improved) | 14.2 | −1.4 (improved) |

Off-target improved along the entire gradient (4.8 → 0.9). No worsening
at any point.

Ambiguity had a modest transient increase at iAT1_3D (+6.6pp) but
improved through ALI, ending below baseline at iAT1_ALI_p1 (14.2%).
Maximum value (22.2%) is well within the indicative ≤60% guardrail.

The shift is not accompanied by quality degradation. Off-target and
ambiguity both improve at the gradient endpoint.

**Condition (b): met.**

### (c) Not contradicted by supportive lanes

| Supportive lane | epithelial_top_state_fine | Direction |
|----------------|-------------------------|-----------|
| GSM6858856_L_DCI (GSE221343) | SOX2lowCFTR+ cells | same ✓ |
| GSE289846_3i_LATS_Day14 (GSE289846) | SOX2lowCFTR+ cells | same ✓ |

Both supportive lanes confirm the same directional shift toward
SOX2lowCFTR+ cells under iAT1-directed conditions, on two other
iPSC lines (SPC2-ST-B2, B2-3). No contradiction.

**Condition (c): met.**

## 5. Falsification criteria evaluation

### (i) Format-only controls reproduce the shift?

| Format-only row | epithelial_top_state_fine |
|----------------|-------------------------|
| GSM5819133_iAEC2_3D | Proliferating progenitors |
| GSM5819134_iAEC2_3D_insert | Proliferating progenitors |
| GSM5819135_iAEC2_MRC5_insert | Proliferating progenitors |

All 3 format-only controls retain Proliferating progenitors. None
show the SOX2lowCFTR+ shift seen in the directed arm.

**Not triggered.**

### (ii) Directed rows fail to separate from baseline?

All 3 directed rows shifted from Budtip progenitors to SOX2lowCFTR+
cells. Clear separation.

**Not triggered.**

### (iii) Shift driven by quality degradation?

Off-target improved (4.8 → 0.9). Ambiguity stayed modest (max 22.2%,
endpoint 14.2%). The shift reflects genuine identity change, not
projection degradation.

**Not triggered.**

### (iv) Supportive lanes collapse?

GSE221343 L+DCI and GSE289846 LATS-IN-1 both continue to show
SOX2lowCFTR+ as top state. No evidence of unreproducibility.

**Not triggered.**

**No falsification condition is triggered.**

## 6. Borderline assessment

Not applicable. All three support conditions are met and no
falsification condition is triggered. The evidence does not sit in the
borderline zone.

## 7. Primary outcome

**A — support_on_current_canonical_basis**

P-0002 is supported at the alveolar epithelial commitment level on
the current canonical v4 basis. The GSE221342 directional gradient
shows a directional shift toward alveolar commitment (Budtip
progenitors → SOX2lowCFTR+ cells) with improving quality metrics,
consistent with the same direction seen on two other iPSC lines, and
not reproduced by format-only controls.

## 8. Limitations

This support statement is bounded by:

1. **Retrospective framing.** The validation target was canonical
   before formal evaluation. A prospective external replication
   would strengthen the claim.

2. **Single cross-line replication.** BU3 NGAT is one additional
   line beyond the original SPC2-ST-B2 and B2-3 basis. A second
   independent replication line would further strengthen.

3. **Commitment level only.** This evaluation supports alveolar
   epithelial commitment. It does not support claims about full
   alveolarization, morphogenesis, or AT1/AT2 segregation.

4. **Reference-dependent.** All evidence is on reference v1. The
   directional pattern could in principle be reference-specific,
   though cross-line consistency makes this less likely.

5. **GSE221344 not counted.** YAP5SA's partial positive-arm signal
   is directionally consistent but was not used in the success
   determination. It remains supportive-only.

None of these limitations constitute falsification. They define the
boundary of the current support claim.

## 9. Recommendation

The current canonical basis is sufficient for a cautious
commitment-level support statement. Specifically:

- P-0002 remains registered with status `registered`.
- The evaluation outcome can be recorded as
  `support_on_current_canonical_basis` in a future registry update
  if desired.
- Do not escalate the claim to full alveolarization.
- Do not change prediction_registry_v2 in this step.

If stronger closure is desired in the future, the smallest next
validation need is a prospective external replication on an
independent iPSC line not already in the canonical world. This is
not required for the current commitment-level support statement.

---

## 10. Explicit stop line

- reports/comparison_world_biology_summary_v4/: not changed
- reports/artifact_lifecycle_registry_v3/: not changed
- reports/prediction_registry_v2/: not changed
- reports/contrast_registry_v1/: not changed
- reports/contrast_paired_review_pilot_v1/: not changed
- data_contract.yaml: not changed
- decision_log.md: not changed
- research_scope.md: not changed
- No new TSV or XLSX
- No new implementation
- No canonical migration in this step
