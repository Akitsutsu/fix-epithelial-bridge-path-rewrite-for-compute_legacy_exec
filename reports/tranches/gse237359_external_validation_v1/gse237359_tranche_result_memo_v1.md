# GSE237359 vs CA1/BU3 tranche result memo (v1)

## Canonical table
Use `benchmark_run_gse237359_manual_compare/gse237359_vs_CA1_BU3_key_metrics_multiroot.tsv` as the tranche-level canonical compare table.
A reconstructed copy is bundled here as `gse237359_vs_CA1_BU3_canonical_compare_table_v1.tsv`.

## What was fixed in this tranche
- Registered GSE237359 as the first external intake.
- Opened `GSM8229877_240314KT_AT2_organoid_filtered.h5ad.gz` locally and verified:
  - `.raw` is present
  - donor column = `donor`
  - souporcell status column = `Souporcell4_status`
- Split the pooled scRNA sample into four donor-specific H5ADs.
- Confirmed that the common combined-root compute route is still unstable for whole-lung legacy compute due to output-path mismatch.
- Established a working compute route using **per-query self/self run roots** followed by a **multiroot collector**.

## Donor-resolved intake summary
- `G237359_15934`: 2170 cells, `17 pcw`, `P16`
- `G237359_16011`: 261 cells, `21 pcw`, `P11`
- `G237359_16392`: 3349 cells, `17 pcw`, `P15`
- `G237359_16402`: 2046 cells, `20 pcw`, `P15`

## Main projection result
- Benchmark anchors:
  - `CA1` -> `week_15`, `Basal cells`
  - `BU3` -> `week_15`, `Basal cells`
- External GSE237359 donors:
  - all four donors -> `week_18`, `Tip cells`

## Interpretation
This intake does **not** behave like additional CA1/BU3-type proximal anchors.
Instead, GSE237359 behaves as a coherent **distal / late-fetal / Tip-like external validation tranche**.
This is strongest for donors `15934`, `16392`, and `16402`.
Donor `16011` is retained, but should be treated as supportive because of its lower cell count.

## Operational conclusion
- Keep the scientific conclusion.
- Keep the donor split sample sheet and donor H5AD outputs.
- Keep the multiroot compare table as canonical for this tranche.
- Do **not** treat the symlink workaround or forced-outdir patch attempt as canonical.
- Combined-root compute remains a separate engineering issue.

## Suggested GitHub boundary
### Good to commit now
- donor-resolved sample sheet / manifest updates
- multiroot collector script
- canonical compare table
- short result memo
- comparison figure
- a short note describing the unresolved combined-root whole-lung output-path mismatch

### Better not to merge as canonical yet
- symlink workaround shell steps
- broken forced-outdir patch attempts
- any claim that combined-root compute is fixed

## One-sentence freeze
**CA1/BU3 remain proximal week_15 Basal anchors, whereas donor-resolved GSE237359 consistently maps to week_18 Tip cells and should be treated as distal external validation rather than additional proximal cohort support.**
