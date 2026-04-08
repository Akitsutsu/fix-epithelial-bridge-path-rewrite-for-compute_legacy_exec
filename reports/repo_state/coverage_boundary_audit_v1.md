# Coverage and Boundary Audit v1

## Date
2026-04-08

## Scope
This is a **repo-state diagnostic memo**. It does not change governance,
reference, metadata, or accepted tranche statuses. It summarizes coverage
strengths, boundary weak points, and proposed triggers for future action
based on the current comparison world (v3, 20 rows, 7 components).

## Basis artifacts
- `reports/comparison_world_biology_summary_v3/` (20 rows)
- `reports/artifact_lifecycle_registry_v2/` (7 tranches)
- `reports/prediction_registry_v1/` (P-0001 registered/supportive)
- Accepted tranche review artifacts for GSE237359, GSE221343, GSE289846,
  GSE308817, GSE193716 (iAEC2 subset), GSE221344

---

## 1. Current operational state

| Property | Value |
|----------|-------|
| Reference release | v1 (frozen) |
| Stage axis | sample_week |
| Comparison world | v3 (20 rows, 7 components) |
| Lifecycle registry | v2 (7 tranches) |
| Prediction registry | P-0001 registered/supportive, not confirmed |
| Labs represented | 4 (BU, Cambridge, Kyoto, Xiamen) |
| Stem cell backgrounds | 3 (iPSC SPC2-ST-B2, iPSC B2-3, hESC H9) + fetal tissue |
| Platforms | 2 (10x Chromium, SeekOne) |

---

## 2. Stage coverage audit

### Row distribution by coarse stage

| Stage coarse | Rows | Tranches | Notes |
|-------------|-----:|---------|-------|
| late_GW17_19 | 16 | 5 (GSE237359, GSE221343, GSE289846 partial, GSE193716, GSE221344) | Dominant stage; all iPSC SPC2-ST-B2 tranches land here |
| mid_GW14_16 | 2 | 1 (CA1/BU3 anchor) | Anchor-only; no external validation at this stage |
| early_GW10_13 | 4 | 2 (GSE289846 PAL, GSE308817) | Passage series + transitional only |

**Total**: 20 rows with assigned coarse stage (2 anchor + 18 external).

### What is well covered

**late_GW17_19 / week_18** is thoroughly covered:
- 16/20 rows (80%) map here
- 5 independent tranches contribute
- Multiple biology axes tested: condition, perturbation, culture format,
  donor variation
- Cross-lab replication achieved for SOX2lowCFTR+ (BU + Kyoto)
- Cross-dataset replication for Proliferating progenitors (3 tranches)
- State diversity within this stage: Tip cells, Stromal-like cells 1,
  SOX2lowCFTR+, Proliferating progenitors

### What is thinly covered

**mid_GW14_16**: only 2 rows (CA1/BU3 anchor). No external tranche maps
to this stage. If the anchor queries have a systematic bias, there is no
independent check.

**early_GW10_13**: 4 rows from 2 tranches. GSE308817 (3 passage rows)
provides the bulk but all are Budtip progenitors with high ambiguity
(30-50%). GSE289846 PAL (1 row) is the only non-Budtip early-stage row
(PNEC). No cross-lab replication at this stage — GSE308817 is Xiamen,
GSE289846 is Kyoto.

**GW6-9 (early embryonic)**: zero coverage. The reference contains these
stages but no external query has mapped there.

### Stage coverage bias summary

The world is **late-heavy**. 80% of rows map to late_GW17_19 / week_18.
This is partially driven by the iPSC differentiation protocols used in
most tranches (which produce late-fetal-like cells) and partially by the
reference structure (which may preferentially attract organoid queries to
late-fetal nodes). The mid-fetal window has no external support, and the
early-fetal window has limited and high-ambiguity coverage.

---

## 3. Whole-lung vs epithelial boundary audit

### Symmetric metrics available

| Category | Rows | WL + Epi metrics? | Epi OT range | Ambiguity range |
|----------|-----:|:-:|---:|---:|
| GSE221343 | 3 | yes | 0.8-4.7% | 29.9-37.3% |
| GSE289846 | 3 | yes | 0.1-0.7% | 17.8-34.9% |
| GSE308817 | 3 | yes | 0.1-2.1% | 30.3-49.9% |
| GSE193716 iAEC2 | 3 | yes | 0.9-2.1% | 9.9-31.0% |
| GSE221344 | 2 | yes | 1.7-1.8% | 11.2-24.2% |

These 14 rows have full WL + epithelial metrics. Epithelial off-target
is uniformly low (0.1-4.7%) across all accepted rows with symmetric
metrics. The epithelial lineage gate effectively isolates clean epithelial
signal even when whole-lung off-target is elevated.

### WL off-target high but epi clean

| Row | WL OT | Epi OT | Gap explanation |
|-----|------:|------:|-----------------|
| GSM5819133_iAEC2_3D | 38.1% | 0.9% | feeder-free 3D format; extra barcodes are non-epithelial |
| GSM6858858_YAP5SA | 28.7% | 1.7% | CellRanger filtered vs paper QC; extra barcodes are low-quality |
| GSM6858857_WT_YAP | 16.6% | 1.8% | same as YAP5SA |
| GSM5819135_iAEC2_MRC5_insert | 15.6% | 2.1% | +MRC5 co-culture; sorted but residual non-epi |

In all cases, the epithelial remap recovers clean results (OT < 2.5%).
The WL-epi gap is **localized** to specific technical/biological classes:
- **Full CellRanger barcode sets** (GSE221344): extra low-quality barcodes
  inflate WL off-target but are excluded by the epithelial lineage gate
- **Co-culture / feeder** (GSE193716 3D, +MRC5): non-epithelial cells
  survive EPCAM sorting at low levels
- **All other rows**: WL off-target < 12%, epi OT < 5%

**Conclusion**: boundary failure is **localized, not global**. The
epithelial lineage gate is effective across all accepted tranches.

### Missing symmetric epi metrics

| Category | Rows | Issue |
|----------|-----:|-------|
| CA1/BU3 (anchor) | 2 | epi-remap metrics unavailable in decision-TSV format; multiroot path does not produce symmetric epi summary |
| GSE237359 (donor-resolved) | 4 | same as CA1/BU3; multiroot collector path |

**6/20 rows (30%) lack symmetric epi-remap metrics.** These are the
oldest accepted artifacts (pre-combined-root-v2). This is a known gap
documented since v1. It does not block current interpretation but means
the anchors and distal benchmark cannot be directly compared on epi
off-target / ambiguity / epi state_fine with the newer tranches.

---

## 4. Adult primary handling

### Current status
4 GSE193716 primary AEC2 rows are **not in the current comparison world**:
- GSM5819131_primary_preculture_PL2 (hold_pending_biological_review)
- GSM5819132_primary_preculture_PL1 (hold_pending_biological_review)
- GSM5819129_primary_cultured_PL2 (not_recommended_now)
- GSM5819130_primary_cultured_PL1 (not_recommended_now)

### Why they are held
1. **Adult-primary-vs-fetal-reference caveat**: freshly isolated adult
   AEC2s project to fetal Budtip progenitors. Whether this reflects
   (a) a genuine retained progenitor signature, (b) limited adult
   representation in the fetal reference, or (c) a closest-neighbor
   default cannot be determined by projection alone.
2. **Cultured-primary off-target**: 9.9-15.6% epi off-target for cultured
   samples, 2-3x higher than any accepted row. MRC5 co-culture likely
   contributes non-epithelial signal.
3. **Donor effect**: PL2 cultured -> Tip cells, PL1 cultured -> Budtip
   progenitors. N=1 per condition per donor is insufficient to separate
   donor effect from culture stochasticity.

### Recommendation
**Treat as shadow benchmark, not current comparison-world core.**

The primary rows provide valuable diagnostic information (adult tissue
on fetal reference) but their biological interpretability is unresolved.
They should be:
- Referenced in audit and diagnostic contexts
- Used informally to probe reference coverage limits
- NOT promoted to query-ready until the adult-vs-fetal question has
  domain-expert input

### What evidence is still needed
1. **Domain-expert assessment** of the Budtip mapping for adult AEC2s —
   is this biologically meaningful or a reference artifact?
2. **Independent adult primary dataset** — if a second adult AEC2 dataset
   maps similarly, the Budtip mapping gains credibility
3. **Dedicated adult reference** or **multi-source reference** that
   includes adult AT2 representation — this would test whether the
   mapping changes with richer adult coverage
4. **Cultured-primary off-target explanation** — fibroblast marker
   analysis on the off-target fraction would disambiguate MRC5
   contamination from culture-induced transcriptomic change

---

## 5. Reference single-source risk

### Current state
Release v1 is a frozen reference derived from a single fetal lung
scRNA-seq dataset. It is the sole operational reference and has been
stable since project inception. All 20 comparison-world rows project
against this single source.

### Risk characterization
- All stage / state / off-target / ambiguity metrics are relative to v1
- If v1 has systematic bias (e.g., under-representing certain cell
  states, over-representing certain developmental windows), all downstream
  interpretations inherit that bias
- The late-heavy stage coverage of the comparison world may partially
  reflect v1's structure rather than intrinsic organoid biology
- The mid_GW14_16 gap (anchor-only) is particularly vulnerable: there
  is no external check on whether the anchor placement is v1-specific

### Why not replace v1 now
- v1 is frozen and stable — it has supported reproducible benchmarks
  across 7 accepted tranches
- No candidate v2 reference exists
- Replacing v1 without a candidate would break benchmark comparability
- The current comparison world's internal consistency (cross-lab
  replication, within-tranche coherence) suggests v1 is adequate for
  current purposes

### Proposed triggers for starting candidate v2

These are **proposals**, not established policy. They would need to be
logged in `decision_log.md` if adopted.

**Trigger A — Second independent fetal source becomes candidate-ready.**
A second fetal lung scRNA-seq dataset (different lab, different donors,
same or comparable developmental window) passes audit and demonstrates
sufficient quality for reference construction. This is the minimal
prerequisite for a multi-source reference.

**Trigger B — Repeated clean-tranche WL/epi disagreement.**
Two or more accepted tranches show systematic WL/epi metric disagreement
that cannot be explained by technical factors (cell population, sorting,
co-culture). This would suggest the reference structure is creating
boundary artifacts that the epithelial gate cannot resolve.

**Trigger C — Shadow benchmarks repeatedly collapse into the same niche.**
Held rows (e.g., adult primary AEC2s) and future diverse queries
repeatedly map to the same fetal niche (e.g., Budtip progenitors)
regardless of their actual biological identity. This would suggest v1
lacks the resolution to distinguish genuinely different cell types.

**Trigger D — Candidate reference materially changes core interpretations.**
A candidate v2 reference, once built, produces different top-state
assignments for existing query-ready rows compared to v1. If these
changes are biologically more plausible (validated by independent
evidence), this would motivate promotion of v2.

---

## 6. Recommendation

### What to do now
1. **Keep v1 fixed.** The reference is stable and supports reproducible
   benchmarks. There is no trigger evidence for starting candidate v2.
2. **Use targeted tranche intake to probe weak spots.** Priority gaps:
   - mid_GW14_16 external support (currently anchor-only)
   - early-fetal diversity beyond Budtip/PNEC
   - cross-lab replication for states currently represented by single
     tranches (Basal cells, Tip cells, Stromal-like cells 1, Budtip
     progenitors)
3. **Keep adult primary as shadow benchmark.** Use the held GSE193716
   primary rows diagnostically but do not promote them to query-ready
   until the adult-vs-fetal question is resolved.
4. **Start multi-source candidate v2 only after trigger evidence
   accumulates.** None of the four proposed triggers (A-D) are currently
   met. Monitor incoming tranches for trigger signals.

### What not to do now
- Do not silently rebuild v1
- Do not promote the held primary AEC2 rows without domain-expert input
- Do not claim P-0001 is confirmed based on current evidence
- Do not treat the late-heavy stage coverage as sufficient for early/mid
  fetal biology claims
- Do not change governance files based on this diagnostic memo

---

## 7. Explicit stop line

- **data_contract.yaml**: NOT changed
- **decision_log.md**: NOT changed
- **research_scope.md**: NOT changed
- **Accepted tranche statuses**: NOT changed
- **Prediction registry**: NOT changed (P-0001 remains registered/supportive)
- **Comparison world v3**: NOT changed
- **Lifecycle registry v2**: NOT changed

This memo is a diagnostic snapshot. It identifies where the world is
thin, where boundaries are clean vs messy, and what would trigger the
next phase of reference evolution. It does not execute any of those
actions.
