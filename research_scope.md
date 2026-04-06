# research_scope.md

## Project name
fix-epithelial-bridge-path-rewrite-for-compute_legacy_exec

## Mission
Build and operate a reproducible human fetal lung reference projection system that:

1. fixes and preserves the canonical projection / remap execution path,
2. projects organoid or hPSC-derived query data into the native fetal lung reference,
3. returns stage / composition / alignment outputs that remain interpretable across time,
4. supports controlled reference evolution through release / candidate / drift / promotion mechanics,
5. expands external organoid intake without weakening provenance discipline.

## Current canonical state

### Frozen reference
- Current operational reference release: `v1`
- Canonical pair:
  - `converted/reference_RNA.h5ad`
  - `converted/reference_metadata_v1.csv`
- Formal stage axis: `sample_week`

### Canonical execution path
- Use the combined-root v2 path as canonical.
- Canonical runner / bridge files:
  - `benchmark_common_runner_v2.py`
  - `whole_lung_project_common_v2.py`
  - `epithelial_only_remap_common_v2.py`
  - `whole_lung_cmd_template_compute_legacy_v1.txt`
  - `epithelial_cmd_template_compute_legacy_v1.txt`

### Canonical anchor queries
- `CA1`
- `BU3`

Interpretation shorthand:
- `CA1` = mixed proximal airway-like epithelial population
- `BU3` = more converged proximal airway-like epithelial population

### Canonical external tranches
- Accepted and fixed:
  - `GSE237359` donor-resolved external validation tranche
- Accepted and query-ready:
  - `GSE221343` nearest external validation tranche (promoted 2026-04-06)
  - `GSE289846` cross-lab external validation tranche (promoted 2026-04-06)
  - `GSE308817` passage-series external validation tranche (promoted 2026-04-06)

### Canonical validation layer
- Spatial data are a validation / supportive-evidence layer.
- Spatial is not a replacement reference and should not be used to silently redefine the release reference.

## What is in scope now

### A. Stable operation of the current release
In scope:
- benchmark / regression / parity maintenance,
- keeping current release v1 reproducible,
- preserving benchmark comparability.

Out of scope unless explicitly proposed:
- ad hoc modification of release v1 artifacts,
- silent schema drift,
- replacing reference semantics without an explicit decision.

### B. External organoid intake
In scope:
- manifest creation,
- sample-sheet registration,
- raw / processed object inspection,
- H5 -> H5AD conversion,
- metadata harmonization,
- query-ready promotion only after local validation.

Out of scope:
- auto-promoting samples from titles or paper expectations alone,
- mixing donor-level and pooled-level samples without explicit declaration,
- accepting untracked provenance.

### C. Reference evolution
In scope:
- candidate build,
- candidate audit,
- drift reporting,
- explicit promotion decisions.

Out of scope:
- overwriting published releases,
- promoting a candidate without review artifacts.

## What the repo is optimizing for
1. Reproducibility over speed.
2. Reviewable decisions over implicit convenience.
3. Biological interpretability over raw automation throughput.
4. Explicit contracts over handoff-only memory.

## Primary research questions
1. Can organoid / hPSC-derived samples be placed into a stable fetal lung native reference in a way that remains biologically interpretable?
2. Do those interpretations remain stable across reference versions and external validation tranches?
3. Can provenance-preserving intake make external cohort growth cumulative instead of one-off?

## Near-term priorities
1. Make repo-level contracts explicit.
2. ~~Finish local validation / conversion for `GSE221343`.~~ Done (D-0010).
3. Continue external organoid intake under the same provenance rules.
4. Keep spatial as supportive evidence rather than the main growth axis.

## Notable non-goals for the near term
- Rebuilding the reference engineering stack from scratch.
- Expanding spatial analysis into the main bottleneck.
- Treating CA1 / BU3 alone as a real cohort.

## Change policy
Any change that alters one of the following must update both `data_contract.yaml` and `decision_log.md`:
- release identity,
- stage axis,
- canonical runner / bridge entrypoints,
- query-ready promotion rules,
- anchor-query interpretation,
- accepted external tranche status.
