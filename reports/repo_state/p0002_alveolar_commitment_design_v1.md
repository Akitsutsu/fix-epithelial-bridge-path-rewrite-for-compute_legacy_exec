# P-0002 alveolar commitment design note v1

## Date
2026-04-10

## Scope
Repo-state design note. Not a governance change, not a reference
change, not a prediction registration step, not a comparison-world
refresh. No existing artifact is replaced in this step. This note
fixes the initial endpoint and candidate contrast family for a future
P-0002, without adding any entry to the prediction registry.

---

## 1. Why now

The reassessment note (PR #52) confirmed that the legacy 6-row
epithelial backfill is complete, current canonical surfaces are
stable, and contrast-aware canonical migration is not starting now.

This creates space for a bounded design memo that explores what the
next testable prediction might look like — without colliding with
the current stop line. P-0002 can be designed here because:

- Current comparison world v3 has all 20 rows with symmetric
  5-column epithelial metrics.
- The contrast registry skeleton (C-0001 through C-0003) provides
  worked examples of how within-tranche evidence is structured.
- P-0001 demonstrated the registration pattern.

No registry change is made in this step.

## 2. Endpoint decision

**P-0002 initial endpoint: alveolar epithelial commitment on the
native fetal reference axis.**

This is explicitly not full alveolarization or alveologenesis.

Rationale:
- The current canonical 5-column epithelial surface measures stage
  placement, state identity, lineage off-target, and ambiguity —
  all at the projected epithelial level.
- These columns can distinguish whether a directed condition shifts
  cells toward a distal/alveolar epithelial identity (e.g.,
  SOX2lowCFTR+ or Tip cells) relative to a matched control.
- Full alveolarization would require spatial / niche / morphogenesis
  evidence (e.g., alveolar sac structure, AT1/AT2 segregation, ECM
  remodeling) that is beyond the current canonical surface.
- Fixing the endpoint at commitment keeps the prediction expressible
  in existing columns and testable with existing infrastructure.

## 3. Current canonical signal set relevant to P-0002

The following rows in comparison world v3 provide the signal
landscape for a future alveolar commitment prediction:

**iAT1-directed conditions → SOX2lowCFTR+ side:**
- GSM6858856_L_DCI (GSE221343): explicit L+DCI iAT1 induction.
  `epithelial_top_state_fine` = SOX2lowCFTR+ cells. Off-target 0.8%,
  ambiguity 37.3%.
- GSE289846_3i_LATS_Day14 (GSE289846): LATS-IN-1 AT1 induction.
  `epithelial_top_state_fine` = SOX2lowCFTR+ cells. Off-target 0.1%,
  ambiguity 27.7%. Cross-lab (Kyoto) replication of direction.

**Culture-format-only controls → Proliferating progenitors side:**
- GSM5819133_iAEC2_3D, GSM5819134_iAEC2_3D_insert,
  GSM5819135_iAEC2_MRC5_insert (GSE193716): all three retain
  `epithelial_top_state_fine` = Proliferating progenitors with low
  off-target (0.9–2.1%).

**Supportive partial positive-arm:**
- GSM6858858_YAP5SA (GSE221344): YAP5SA shows directional CFTR+
  enrichment relative to WT-YAP control, but top state remains
  Proliferating progenitors. This is supportive of the direction but
  does not achieve identity conversion. Off-target 1.7%, ambiguity
  24.2%.

These signals are enough to draft P-0002 at the design level. They
do not yet force formal registration.

## 4. Candidate contrast family

P-0002 is bounded to a narrow set of candidate contrasts:

**Primary future candidate:**
- GSE221342 directional gradient (C-0002 in contrast skeleton).
  4 rows: iAT2_3D → iAT1_3D → iAT1_ALI_p0 → iAT1_ALI_p1.
  This is the strongest candidate for an alveolar commitment
  gradient within a single tranche.
- GSE221342 is **not** in current comparison world v3. It is a
  future candidate contrast family for P-0002, not a current
  canonical basis.

**Boundary / negative-control family:**
- GSE193716 iAEC2 culture-format series (C-0003 in contrast
  skeleton). 3 rows: 3D / insert / +MRC5. All Proliferating
  progenitors. These define the null expectation: format-only
  variation does not drive alveolar commitment.

**Supportive same-direction family (current canonical):**
- GSE221343 L+DCI (SOX2lowCFTR+ as top state).
- GSE289846 LATS-IN-1 (SOX2lowCFTR+ as top state, cross-lab).
- GSE221344 YAP5SA (partial positive-arm, supportive only).

## 5. Success condition (design-level)

Expressed using only the current 5-column epithelial surface:

A future directed alveolar commitment condition, when projected onto
the fetal reference alongside a matched control from the same line,
shows:

1. **State shift:** `epithelial_top_state_fine` moves toward a
   distal/alveolar-associated identity (e.g., SOX2lowCFTR+ cells,
   Tip cells, or NKX2-1+SOX9+CFTR+ cells) in the directed arm,
   while the matched control retains a progenitor or non-alveolar
   identity.

2. **Stage consistency:** `epithelial_top_stage_coarse` remains
   within the expected gestational window (late_GW17_19 for most
   alveolar-directed protocols). Stage should not regress to
   early_GW10_13 unless biologically motivated.

3. **Quality maintenance:** `epithelial_lineage_off_target_fraction`
   does not increase by more than 10 percentage points relative to
   matched control. `epithelial_ambiguous_fraction` does not increase
   by more than 20 percentage points.

4. **Directional support:** the observed direction is not contradicted
   by at least one row from the supportive same-direction family
   (GSE221343 L+DCI or GSE289846 LATS-IN-1).

This does not require `epi_alignment`. It does not require spatial or
morphogenesis evidence.

## 6. Falsification condition (design-level)

Any of the following would falsify the alveolar commitment prediction
at the 5-column level:

1. **Null control moves the same way:** a culture-format-only control
   family (e.g., GSE193716 iAEC2 rows) shows the same state shift as
   the proposed directed arm, indicating the shift is not
   perturbation-specific.

2. **Directed arm does not move:** the proposed directed condition
   retains the same `epithelial_top_state_fine` as the matched
   control with no directional shift.

3. **Driven by degradation:** apparent state shift is accompanied by
   `epithelial_lineage_off_target_fraction` increasing by more than
   15 percentage points or `epithelial_ambiguous_fraction` exceeding
   60%, suggesting the shift reflects poor projection rather than
   genuine commitment.

4. **Direction collapses:** supportive lanes (GSE221343 L+DCI,
   GSE289846 LATS-IN-1) are later found to be unreproducible or
   driven by technical artifact when re-evaluated.

## 7. Explicit deferrals

The following are explicitly deferred and not decided in this note:

- **Formal prediction registry entry.** P-0002 is not registered.
  `reports/prediction_registry_v1/` is not edited.
- **`epi_alignment` adoption.** Not used in success/falsification
  criteria. Remains deferred per the backfill target-surface decision.
- **Full alveolarization language.** The endpoint is commitment, not
  morphogenesis. Spatial / niche / AT1-AT2 segregation closure is
  out of scope for P-0002 at this level.
- **Combined-root migration.** CA1/BU3/GSE237359 remain multiroot.
  P-0002 does not depend on or trigger combined-root migration.
- **GSE221342 promotion.** GSE221342 is referenced as a future
  candidate, not a current canonical basis. Its 4 rows are not in
  comparison world v3 and would need their own intake / review /
  promotion cycle.

## 8. Recommendation / sequencing

1. **Merge this design note.** It fixes the initial endpoint,
   candidate contrast family, and success/falsification criteria at
   the design level without changing any registry or canonical surface.

2. **Do not edit the prediction registry now.** P-0002 is a design
   memo. It becomes a registry candidate only after a follow-up note
   decides it is mature enough for formal registration.

3. **If desired later:** write a small follow-up note that assesses
   whether P-0002 is expressible enough — given current canonical
   data and the existing contrast skeleton — to justify a
   `prediction_registry_v2` entry. That follow-up would be the
   earliest point at which a P-0002 row could be added.

4. **Do not create `prediction_registry_v2` now.** Do not widen the
   canonical comparison-world surface now. Do not add GSE221342 to
   the comparison world in this step.

---

## 9. Explicit stop line

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
