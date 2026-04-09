# decision_log.md

Append-only project decision log.

## Format
- Status: proposed | accepted | superseded | retired
- Scope: reference | execution | query | spatial | intake | repo-governance
- A change becomes canonical only when recorded here and reflected in `data_contract.yaml` when applicable.

---

## D-0001 — Frozen reference is a pair, not a single file
- Status: accepted
- Scope: reference
- Date: 2026-04-03
- Decision:
  - Treat the operational frozen reference as the pair:
    - `converted/reference_RNA.h5ad`
    - `converted/reference_metadata_v1.csv`
- Why:
  - Expression matrix and decoded metadata are jointly required for stable interpretation.
- Consequences:
  - Any release handling, drift, or provenance logic must preserve both artifacts.

## D-0002 — Formal stage axis is `sample_week`
- Status: accepted
- Scope: reference
- Date: 2026-04-03
- Decision:
  - Use `sample_week` as the formal stage axis for current release v1 interpretation.
- Why:
  - It is the operational axis already fixed in the reference workflow.
- Consequences:
  - Competing stage labels may exist, but `sample_week` is authoritative for current release semantics.

## D-0003 — Release layer is immutable; candidate layer is mutable
- Status: accepted
- Scope: reference
- Date: 2026-04-03
- Decision:
  - Published releases are immutable.
  - Candidate references are the staging area for change.
  - Promotion must be explicit.
- Why:
  - This preserves benchmark stability while allowing controlled evolution.
- Consequences:
  - No silent overwrite of `v1`.

## D-0004 — Combined-root v2 path is canonical
- Status: accepted
- Scope: execution
- Date: 2026-04-03
- Decision:
  - The canonical execution path is the combined-root v2 runner / bridge path.
- Why:
  - Combined-root parity and comparison-table consistency were restored there.
- Consequences:
  - Future benchmark maintenance should target v2 files first.

## D-0005 — CA1 and BU3 are anchor queries, not a cohort
- Status: accepted
- Scope: query
- Date: 2026-04-03
- Decision:
  - `CA1` and `BU3` remain anchor queries for regression and interpretation.
  - They are not sufficient to claim a cohort.
- Why:
  - Local organoid availability does not yet provide a broader cohort.
- Consequences:
  - Cohort language requires additional query-ready samples.

## D-0006 — Spatial is supportive evidence, not the main reference layer
- Status: accepted
- Scope: spatial
- Date: 2026-04-03
- Decision:
  - Treat Visium / Xenium outputs as orthogonal validation and supportive evidence.
- Why:
  - Spatial supports plausibility but is not the main source of reference semantics.
- Consequences:
  - Do not silently fold spatial interpretations into the frozen reference definition.

## D-0007 — GSE237359 is an accepted donor-resolved external validation tranche
- Status: accepted
- Scope: intake
- Date: 2026-04-03
- Decision:
  - `GSE237359` is accepted as a donor-resolved external validation tranche.
- Why:
  - Donor split was feasible and sample sheet v2 / inspection artifacts were fixed.
- Consequences:
  - This tranche is part of the comparison world for future biology narratives.

## D-0008 — GSE221343 is registered but not query-ready
- Status: superseded (by D-0010)
- Scope: intake
- Date: 2026-04-03
- Decision:
  - `GSE221343` is a next external intake candidate with registration and sample sheet v1 only.
  - All rows remain `query_ready_flag=false` until local validation is complete.
- Why:
  - Registration and paper metadata do not substitute for local object validation.
- Consequences:
  - H5 -> H5AD conversion and review remain the next practical gate.

## D-0009 — Governance files become first-class repo entrypoints
- Status: accepted
- Scope: repo-governance
- Date: 2026-04-05
- Decision:
  - Add these first-class files at repo root:
    - `research_scope.md`
    - `data_contract.yaml`
    - `decision_log.md`
    - `AGENTS.md`
    - `CLAUDE.md`
- Why:
  - Operational knowledge is currently distributed across handoffs, design docs, manifests, and prompts.
- Consequences:
  - Agents and humans will have a smaller and more stable entry surface.
  - Existing provenance docs remain valid but become referenced artifacts rather than the first place people look.

## D-0010 — GSE221343 promoted to query-ready after explicit reviewer review
- Status: accepted
- Scope: intake
- Date: 2026-04-06
- Decision:
  - All 3 GSE221343 rows promoted to `query_ready_flag=true`:
    - `GSM6858854_CK_DCI`
    - `GSM6858855_YAP5SA_CK_DCI`
    - `GSM6858856_L_DCI`
  - Dataset-level `query_ready_flag=true`, status changed to `accepted_query_ready`.
  - Tranche status in `data_contract.yaml` updated from `registered_not_validated` to `accepted_query_ready`.
- Why:
  - Gate A (object contract), Gate B (provenance), Gate C (projection smoke test on v1), and Gate D (within-tranche biology coherence) all passed.
  - Whole-lung and epithelial projections completed on canonical combined-root v2 path.
  - All 3 samples project to Epithelial (95–99%) at late_GW17_19/week_18 stage.
  - iAT1 differentiation (L+DCI) shows distinct state (SOX2lowCFTR+) vs iAT2 samples — condition difference interpretable.
  - This is an explicit reviewer decision, not an auto-promotion from paper metadata.
- Consequences:
  - GSE221343 rows enter the comparison world for biology narratives.
  - Review artifacts at `reports/tranches/gse221343_query_ready_review_v1/`.
  - Next external intake candidates can follow the same Gate A–D review path.

## D-0011 — GSE289846 promoted to query-ready after explicit reviewer review
- Status: accepted
- Scope: intake
- Date: 2026-04-06
- Decision:
  - All 3 GSE289846 condition-level rows promoted to `query_ready_flag=true`:
    - `GSE289846_3i_Day7`
    - `GSE289846_3i_LATS_Day14`
    - `GSE289846_3i_PAL_Day14`
  - Dataset-level `query_ready_flag=true`, status changed to `accepted_query_ready`.
  - Tranche status in `data_contract.yaml` updated from `registered_not_validated` to `accepted_query_ready`.
- Why:
  - Gate A–D all passed. 100.0% reference gene overlap. Near-pure epithelial (99.3–99.9%).
  - Each condition maps to a distinct state_fine on v1: Proliferating progenitors → SOX2lowCFTR+ → PNEC.
  - PAL transitional shows coherent stage shift (late → early).
  - First independent-lab tranche (Gotoh/CiRA Kyoto vs Kotton/BU), confirming cross-lab projection interpretability.
  - Explicit reviewer decision, not auto-promoted from paper metadata.
- Consequences:
  - GSE289846 enters the comparison world as the first cross-lab validation tranche.
  - Review artifacts at `reports/tranches/gse289846_query_ready_review_v1/`.
  - Comparison world now spans 3 labs (BU, Cambridge, Kyoto) and 2 iPSC lines (SPC2-ST-B2, B2-3).

## D-0012 — GSE308817 promoted to query-ready after explicit reviewer review
- Status: accepted
- Scope: intake
- Date: 2026-04-06
- Decision:
  - All 3 GSE308817 passage-level rows promoted to `query_ready_flag=true`:
    - `GSE308817_ALOp3`
    - `GSE308817_ALOp7`
    - `GSE308817_ALOp20`
  - Dataset-level `query_ready_flag=true`, status changed to `accepted_query_ready`.
  - Tranche status in `data_contract.yaml` added as `accepted_query_ready`.
- Why:
  - Gate A–D all passed. 100.0% reference gene overlap. Epithelial 97.9–99.9%.
  - Passage trajectory readable: P3→P7 Budtip convergence, P7→P20 stage diversification/drift.
  - SeekOne platform confirmed compatible with 10x-based reference.
  - Citation missing on GEO — noted but not a promotion blocker.
  - Fourth independent lab (Xiamen), hESC H9 background, first non-10x tranche.
  - Explicit reviewer decision, not auto-promoted.
- Consequences:
  - GSE308817 enters the comparison world with a passage/maturation axis.
  - Comparison world now spans 4 labs (BU, Cambridge, Kyoto, Xiamen), 3 stem cell lines (SPC2-ST-B2, B2-3, H9), and 2 platforms (10x, SeekOne).
  - Review artifacts at `reports/tranches/gse308817_query_ready_review_v1/`.

## D-0013 — GSE193716 iAEC2 subset promoted to query-ready after explicit reviewer review
- Status: accepted
- Scope: intake
- Date: 2026-04-07
- Decision:
  - 3 iAEC2 rows from GSE193716 promoted to `query_ready_flag=true`:
    - `GSM5819133_iAEC2_3D`
    - `GSM5819134_iAEC2_3D_insert`
    - `GSM5819135_iAEC2_MRC5_insert`
  - 4 primary AEC2 rows remain `query_ready_flag=false`:
    - `GSM5819131_primary_preculture_PL2` (hold_pending_biological_review)
    - `GSM5819132_primary_preculture_PL1` (hold_pending_biological_review)
    - `GSM5819129_primary_cultured_PL2` (not_recommended_now)
    - `GSM5819130_primary_cultured_PL1` (not_recommended_now)
  - Dataset-level `status` set to `accepted_query_ready` (iAEC2 subset only; 4 primary rows remain query_ready_flag=false).
  - Dataset-level `query_ready_flag` remains `false` (because primary rows are not promoted).
- Why:
  - Gate A–D all passed for the 3 iAEC2 rows. 87.4% reference gene overlap (lncRNA annotation gap only).
  - All 3 iAEC2 rows map to Proliferating progenitors at late_GW17_19/week_18.
  - Proliferating progenitors replicates GSE289846 3i_Day7 cross-dataset (Kyoto, B2-3 line).
  - Same iPSC line (SPC2-ST-B2) as GSE221343 — controlled same-lab comparison.
  - Culture-format comparison (3D vs insert vs +MRC5) is internally coherent and unique.
  - +MRC5 effect on iAEC2 is minimal (epi off-target 2.1%).
  - 3D/insert row has highest alignment score (0.814) of any external tranche row.
  - Primary rows excluded due to unresolved adult-primary-vs-fetal Budtip mapping caveat and elevated off-target (9.9–15.6%) in cultured samples.
  - Explicit reviewer decision, not auto-promoted.
- Consequences:
  - 3 iAEC2 rows enter the comparison world with a culture-format comparison axis.
  - This is the fifth accepted external tranche (first subset promotion).
  - Same lab as GSE221343 — comparison world now has 2 tranches from Kotton/BU.
  - Primary rows can be reconsidered after domain-expert input on adult-primary-vs-fetal biology.
  - Review artifacts at `reports/tranches/gse193716_iAEC2_subset_review_v1/`.

## D-0014 — GSE221344 promoted to query-ready as paired same-line positive-arm tranche
- Status: accepted
- Scope: intake
- Date: 2026-04-08
- Decision:
  - Both GSE221344 rows promoted to `query_ready_flag=true` as a paired tranche:
    - `GSM6858857_WT_YAP` (WT YAP lentiviral control)
    - `GSM6858858_YAP5SA` (YAP5SA constitutively active nuclear YAP)
  - Dataset-level `query_ready_flag=true`, status changed to `accepted_query_ready`.
  - Tranche role: `nearest_external_validation`.
  - Tranche meaning: same-line positive-arm supportive evidence for P-0001.
  - P-0001 prediction status remains `registered`/supportive, NOT confirmed.
- Why:
  - Gate A–D all passed. 91.98% reference gene overlap (identical to GSE221343).
  - Both samples project to Epithelial (~98%) at late_GW17_19/week_18.
  - Both are Proliferating progenitors dominant in the epithelial remap.
  - YAP5SA shows 100x enrichment of CFTR+ lineage cells relative to WT-YAP:
    SOX2lowCFTR+ 5.6% vs 0.06%, NKX2-1+SOX9+CFTR+ 7.3% vs 0.07%.
  - Direction is consistent with P-0001 (iAT1-directed perturbation enriches
    SOX2lowCFTR+), but SOX2lowCFTR+ is not the top state in YAP5SA (5.6%,
    partial shift, not identity conversion). P-0001 success condition is not met.
  - The pair is the evidence unit: the 100x enrichment is only interpretable
    relative to the matched WT-YAP lentiviral control.
  - Same iPSC line (SPC2-ST-B2), same lab (Kotton/BU), same paper (Burgess 2024)
    as GSE221343. Adjacent GSE/GSM IDs.
  - Explicit reviewer decision, not auto-promoted from paper expectations.
- Caveats:
  - WT-YAP is a lentiviral control, not an untransduced control. Tip cells
    enrichment (29.9%) distinguishes it from untransduced GSE221343 CK+DCI.
  - YAP5SA shows a partial shift, not a top-state SOX2lowCFTR+ conversion.
  - Whole-lung off-target (16.6-28.7%) is elevated because conversion uses
    full CellRanger filtered barcodes, not paper post-Seurat-QC subset.
    Epithelial-remap off-target is clean (1.7-1.8%).
- Consequences:
  - GSE221344 enters the comparison world as a paired perturbation tranche.
  - This is the sixth accepted external tranche.
  - P-0001 gains supportive evidence but is NOT confirmed or falsified.
  - Comparison-world refresh deferred to separate reports-only PR.
  - Review artifacts at `reports/tranches/gse221344_query_ready_review_v1/`.

## D-0015 — GSE221342 promoted to query-ready as boundary-stress tranche
- Status: accepted
- Scope: intake
- Date: 2026-04-09
- Decision:
  - All 4 GSE221342 rows promoted to `query_ready_flag=true`:
    - `GSM6858850_iAT2_3D` (iAT2 baseline, 3D CKDCI)
    - `GSM6858851_iAT1_3D` (iAT1 differentiation, 3D LDCI)
    - `GSM6858852_iAT1_ALI_p0` (iAT1, ALI transwell direct passage)
    - `GSM6858853_iAT1_ALI_p1` (iAT1, ALI transwell after 9d 3D LDCI)
  - Dataset-level `query_ready_flag=true`, status changed to `accepted_query_ready`.
  - Tranche role: `nearest_external_validation`.
  - Tranche meaning: same-line-to-anchor boundary-stress tranche.
  - NOT a P-0001 validation tranche (BU3 NGAT, not SPC2-ST-B2).
- Why:
  - Gate A–D all passed. 91.98% reference gene overlap (identical to GSE221343/GSE221344).
  - iAT2 3D maps to **mid_GW14_16 / week_15** — first external row at this stage, directly
    probing the anchor-only mid-stage gap identified in coverage boundary audit v1.
  - iAT1 conditions (3D, ALI p0, ALI p1) show SOX2lowCFTR+ dominant (60.9–78.0%),
    replicating the L+DCI -> SOX2lowCFTR+ shift cross-line (BU3 NGAT vs SPC2-ST-B2 vs B2-3).
  - ALI p1 has the strongest SOX2lowCFTR+ (78.0%) and best alignment (0.773) of any
    tranche in the comparison world.
  - ALI culture format is new to the comparison world and is readable on v1.
  - BU3 NGAT is the same iPSC line as the BU3 anchor query — first external tranche
    from the same line as an anchor.
  - Clear monotonic gradient: iAT2 Budtip -> iAT1 SOX2lowCFTR+ -> ALI p0 -> ALI p1.
  - Explicit reviewer decision, not auto-promoted.
- Consequences:
  - GSE221342 enters the comparison world as a boundary-stress tranche.
  - This is the seventh accepted external tranche.
  - First external mid_GW14_16 row enters the world (iAT2 3D).
  - First ALI culture format enters the world.
  - SOX2lowCFTR+ now replicates across 3 iPSC lines (SPC2-ST-B2, B2-3, BU3 NGAT).
  - P-0001 is NOT affected (different cell line).
  - Comparison-world refresh deferred to separate reports-only PR.
  - Review artifacts at `reports/tranches/gse221342_query_ready_review_v1/`.
