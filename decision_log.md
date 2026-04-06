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
- Status: accepted
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
