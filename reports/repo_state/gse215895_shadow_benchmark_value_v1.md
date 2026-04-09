# GSE215895 shadow benchmark value note

## Date
2026-04-09

## Scope
Repo-state diagnostic note. Not a governance change, not a reference
change, not a comparison-world admission decision. This note assesses
whether GSE215895 has value as a shadow benchmark and recommends a
next step.

---

## Current status

GSE215895 (Sountoulidis et al., Nature 2023, PMID:36646791) is
registered and gene-space-audit-complete. It is a PCW5.5-14 human
embryonic lung dataset with 39 samples across 11 developmental
timepoints. It is framed as a shadow benchmark and candidate-v2
trigger lane — not part of the current comparison-world core.
Public main is unchanged by this note.

## Why this dataset matters

The coverage boundary audit (v1) identified two structural weak
points in the current comparison world:

1. **GW6-9 has zero external coverage.** No accepted tranche maps
   to this early embryonic window. GSE215895 covers PCW5-8.5
   (approximately GW6-10), directly filling this gap.

2. **Single-source reference risk.** Release v1 derives from one
   fetal lung dataset. GSE215895 is an independent embryonic lung
   source from a different lab (Samakovlis / Stockholm) and a
   different study, making it a natural stress test for single-source
   bias.

Additionally, GSE215895 provides biological replicates at most
developmental stages (2-7 replicates per PCW), which is richer
temporal coverage than any single accepted tranche offers.

## What is already resolved

The gene-space audit confirmed:

- 39/39 H5 files load successfully
- All samples share a single object-shape class (33,538 features)
- Reference overlap is 87.85% — uniform across all 39 samples
  and stable between 10Xv2 (5 samples) and 10Xv3 (34 samples)
- No duplicate gene symbols; no remapping needed
- No reporter/custom features (embryonic tissue, not a reporter line)
- PCW labels are preserved as source text; no sample_week coercion

The dataset is technically coherent as a shadow benchmark.

## What is still unresolved

- Conversion has not been performed (39 H5AD files not written)
- Projection has not been run
- How embryonic tissue maps onto the current fetal reference is unknown
- Whether this dataset should ever enter the comparison-world core
  has not been discussed
- Whether this dataset should participate in candidate-v2 construction
  has not been decided

## Value assessment

**Does this have value as a shadow benchmark? Yes.**

It covers the exact temporal gap (GW6-9) that the current world
cannot probe. It provides an independent fetal-source stress test
against v1 — the kind of evidence that would inform a future
multi-source reference decision (Trigger A from the coverage audit).
The technical audit shows low friction: standard GRCh38 CellRanger
H5 files with 87.85% reference overlap and no structural issues.

**Why not convert now?** No immediate biology question requires
these projections. The current comparison-world priorities
(GSE221342 promotion, comparison-world v4 refresh) do not depend
on GSE215895. Conversion of 39 samples is a non-trivial batch
operation whose output would sit unused until a specific early-
embryonic or candidate-v2 question motivates it. The audit-complete
state is sufficient to justify holding the dataset in reserve.

## Recommendation

Keep GSE215895 as a registered, audit-complete shadow benchmark.
Do not convert yet. Revisit only if:

1. An early-embryonic comparison question becomes urgent (e.g., a
   new query maps to GW6-9 and needs a tissue benchmark)
2. Candidate-v2 trigger evidence accumulates and an independent
   fetal source is needed for multi-source reference construction
3. A targeted benchmark against early-stage queries is required
   for a specific tranche review

This note is sufficient to justify holding the dataset in reserve.
Conversion is not the recommended immediate next step.

---

## Explicit stop line

- data_contract.yaml: not changed
- decision_log.md: not changed
- research_scope.md: not changed
- Accepted tranche statuses: not changed
- Comparison world: not changed
- Conversion: not done
- Projection: not done
- Promotion: not done
