# Contrast paired-review pilot value assessment v1

## Date
2026-04-10

## Scope
Repo-state pilot-value assessment note. Not a governance change, not a
reference change, not a comparison-world refresh, not a lifecycle
refresh, not a prediction refresh, not an implementation PR. No
existing artifact is replaced in this step.

---

## 1. Why now

The contrast paired-review pilot (PR #58) is now merged. Prediction
registry v2 with P-0002 is also merged. The open question is no
longer "can we build a pilot?" but "did the pilot add enough
interpretive value beyond row-first summaries to justify future
contrast-layer work?"

## 2. Current stable baseline

| Surface | Version | Content |
|---------|---------|---------|
| Comparison world | v4 | 24 rows, 8 tranche components |
| Lifecycle registry | v3 | 8 tranches |
| Prediction registry | v2 | P-0001 + P-0002 |
| Contrast pilot | v1 | 9 member rows across C-0001/C-0002/C-0003 (non-canonical) |

No canonical surface currently depends on the contrast pilot. The
pilot exists as a non-canonical side artifact only.

## 3. What the pilot clarified

### C-0001: paired perturbation (GSE221344)

**Added value: marginal.**

The pilot structures the WT-YAP vs YAP5SA comparison with explicit
control/comparison roles and a control_interpretability_note about the
lentiviral-vs-untransduced distinction. However, this observation is
already well-captured in the v4 narrative memo and comparison-world
README. The sub-top-state CFTR+ enrichment (5.6% vs 0.06%) was
already narrated in the v3 memo and carried forward into v4. The
paired framing makes it slightly more structured but does not surface
a judgment that was previously invisible.

C-0001 remains best treated as supportive-only. The paired review
confirmed this without changing the interpretive picture.

### C-0002: directional gradient (GSE221342)

**Added value: meaningful.**

The pilot groups the 4-point gradient (iAT2 baseline → iAT1 3D →
iAT1 ALI p0 → iAT1 ALI p1) with explicit control/comparison roles
and contrast_delta_note fields showing the monotonic progression:

| Row | State | Off-target | Ambiguity |
|-----|-------|-----------|-----------|
| iAT2_3D (control) | Budtip progenitors | 4.8 | 15.6 |
| iAT1_3D | SOX2lowCFTR+ (60.9%) | 3.9 | 22.2 |
| iAT1_ALI_p0 | SOX2lowCFTR+ (56.8%) | 2.1 | 18.2 |
| iAT1_ALI_p1 | SOX2lowCFTR+ (78.0%) | 0.9 | 14.2 |

This monotonic pattern — identity shift and quality improvement
progressing together — is visible only when the rows are grouped as a
gradient. The row-first v4 summary lists these as 4 independent rows,
and while a human reader can infer the pattern, the contrast framing
makes the between-row comparison explicit and reviewable.

The stage discrepancy note for the iAT2 baseline (WL mid_GW14_16 vs
epi late_GW17_19) is also more naturally surfaced in a control-role
annotation than in a per-row ambiguity_note.

### C-0003: matched format series (GSE193716)

**Added value: narrow but real.**

The pilot groups the 3 format conditions as a null/control family and
explicitly connects them to P-0002 falsification logic: "format-only
variation does not shift identity toward SOX2lowCFTR+." The v4
row-first summary already shows all 3 rows as Proliferating
progenitors, but does not explicitly frame them as a falsification
null for any prediction. The contrast review makes this connection
structured and reviewable.

The added value is specifically for falsification reasoning, not for
the positive biology signal.

## 4. Overall pilot value judgment

**Meaningful but narrow value.**

The pilot demonstrates genuine added interpretive value for two of
three contrast types:
- `directional_gradient` (C-0002): the monotonic between-row pattern
  is materially clearer in grouped framing than in row-first reading.
- `matched_format_series` (C-0003): the falsification-null framing
  adds structured reasoning that row-first summaries lack.
- `paired_perturbation` (C-0001): marginal added value; the existing
  narrative already captures the key observation.

The value is narrow because it applies to specific contrast types
(gradients and matched-control families), not to all possible
contrast framings.

## 5. Primary outcome

**B — narrow_followup_worthwhile_for_specific_contrast_types**

The pilot justifies further work for `directional_gradient` and
`matched_format_series` contrast types. It does not justify a
broader contrast layer covering all possible contrast framings.
`paired_perturbation` does not currently add enough beyond
row-first narrative to warrant further investment.

## 6. Recommendation

If future contrast-layer work is desired, the smallest acceptable
next step is:

1. A tiny non-canonical follow-up that extends paired-review coverage
   only for contrast types where the pilot demonstrated clear added
   value: `directional_gradient` and `matched_format_series`.
2. This follow-up should remain non-canonical and should not modify
   comparison-world, lifecycle, or prediction surfaces.
3. It should target only contrasts where new canonical tranches
   provide grounded data (i.e., do not create hypothetical contrasts
   for tranches not yet in the comparison world).
4. `paired_perturbation` contrasts should remain narrated in
   comparison-world memos rather than structured in a separate layer,
   unless new paired data makes the case stronger.

**Do not expand the contrast layer in this step.**

## 7. Human-judgment-sensitive points

Three places where human review matters most:

1. **Whether C-0002 meaningfully exceeds row-first interpretation.**
   The monotonic gradient table above is the strongest evidence for
   the pilot's value. A human reviewer should judge whether this
   grouped view changed any interpretive conclusion compared to
   reading the 4 v4 rows independently. If yes, the gradient contrast
   type is genuinely worth retaining. If no, the pilot is only a
   formatting convenience.

2. **Whether C-0003 materially sharpens falsification logic.** The
   null-control framing connects directly to P-0002 falsification
   condition (i). A human reviewer should judge whether this
   structured connection is necessary for P-0002 evaluation or
   whether the existing row-first data is sufficient.

3. **Whether C-0001 should remain at marginal.** If the sub-top-state
   enrichment pattern (5.6% vs 0.06%) is considered more informative
   in paired framing than in narrative memo form, C-0001 could be
   upgraded to narrow value. The current assessment treats it as
   marginal because the narrative memo already captured the key facts.

---

## 8. Explicit stop line

- reports/comparison_world_biology_summary_v4/: not changed
- reports/artifact_lifecycle_registry_v3/: not changed
- reports/prediction_registry_v2/: not changed
- reports/contrast_registry_v1/: not changed
- reports/contrast_paired_review_pilot_v1/: not changed
- data_contract.yaml: not changed
- decision_log.md: not changed
- research_scope.md: not changed
- No new TSV or XLSX
- No new pilot implementation
- No canonical migration in this step
