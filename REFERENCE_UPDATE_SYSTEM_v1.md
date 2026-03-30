# Reference Update System v1

## Purpose

This document proposes a reference update system for the fetal lung reference used by the organoid benchmarking pipeline.

The goal is **not** to replace the current frozen reference design. The goal is to preserve the reproducibility benefits of the current frozen pair while adding a safe and explicit mechanism for future reference updates.

In other words, this proposal reframes the current frozen reference as **release v1** of a versioned reference system, rather than as the only reference that will ever exist.

---

## Background

The current operational reference is the frozen pair:

- `converted/reference_RNA.h5ad`
- `converted/reference_metadata_v1.csv`

This design has been useful because it provides a stable, read-only target for benchmark runs, exemplar validation, and parity checks.

The current repository state also now includes:

- a provenance document for the frozen pair,
- canonical rebuild scripts,
- and a rebuild-vs-frozen audit.

As a result, the present frozen reference is no longer just an undocumented working artifact. It is now a reproducible and auditable reference release.

At the same time, this reference remains a specific operational snapshot of a fetal lung atlas under one set of assumptions, filters, metadata mappings, and annotation choices. Over time, it is likely that we will want to:

- include additional gestational stages,
- include additional donors or samples,
- revise annotation mappings,
- harmonize multiple atlas sources,
- or improve metadata semantics.

For that reason, the long-term system should support **reference evolution** without compromising the reproducibility of existing benchmark results.

---

## What this proposal is trying to solve

This proposal addresses the following tension:

1. The current benchmark system needs a **stable, immutable reference**.
2. The long-term biological program benefits from a **reference that can improve over time**.

The design goal is therefore:

- to keep benchmark reproducibility,
- while making reference updates possible,
- explicit,
- reviewable,
- auditable,
- and versioned.

---

## Relationship to the current design

This proposal is an extension of the current design, not a rejection of it.

### What remains the same

The following principles from the current design should remain in force:

- The operational reference used for benchmark runs must be clearly defined.
- Existing frozen artifacts must not be overwritten casually.
- Provenance must be documented.
- Rebuildability and auditability are required.
- Benchmark anchor queries such as CA1 and BU3 should continue to be used for regression checking.

### What changes

The main change is conceptual:

**Current design:**
- one frozen pair is treated as the operational reference.

**Proposed design:**
- the current frozen pair becomes **versioned release v1**,
- future reference changes are first built as **candidate references**,
- and only promoted to a new release after audit and benchmark review.

So the proposal does **not** replace the current frozen reference.
It places it inside a broader release system.

---

## Key differences from the previous design

### 1. From a single frozen pair to multiple versioned releases

**Previous design**
- `reference_RNA.h5ad` + `reference_metadata_v1.csv` functioned as the single operational reference.

**Proposed design**
- maintain a series of immutable releases, for example:
  - `fetal_lung_v1`
  - `fetal_lung_v2`
  - `fetal_lung_v3`
- treat the current frozen pair as `fetal_lung_v1`
- build future updates as candidate references before promotion

This makes reference updates possible without invalidating older benchmark results.

### 2. From provenance-only documentation to provenance plus change management

**Previous design**
- the main question was: how was the current frozen reference created?

**Proposed design**
- document not only how a release was built,
- but also what changed relative to the previous release,
- why it changed,
- what benchmark impact it had,
- and why promotion was justified.

This moves the system from static provenance into controlled reference lifecycle management.

### 3. From a rebuild backstop to a candidate build pipeline

**Previous design**
- rebuild scripts existed primarily as a reproducibility backstop for the current frozen pair.

**Proposed design**
- generalize those scripts into a candidate build pipeline that can accept controlled changes such as:
  - gestational week range,
  - donor subset,
  - annotation mapping version,
  - source atlas version,
  - output tag.

This makes the system useful not only for rebuilding v1, but also for testing future v2/v3 candidates.

### 4. From code validation to reference drift evaluation

**Previous design**
- benchmark checks mainly verified code-path correctness, parity, and bridge stability.

**Proposed design**
- benchmark queries should also be used to measure the effect of reference updates.

Examples:
- Does CA1 keep the same top stage?
- Does BU3 keep the same top state?
- Does off-target fraction change materially?
- Does epithelial remapping become more or less stable?

This expands the benchmark role from software validation to reference-change evaluation.

### 5. From static freezing to controlled promotion

**Previous design**
- the frozen pair was effectively static, and updates would be exceptional and manual.

**Proposed design**
- updates are expected and allowed,
- but only through a controlled path:
  - candidate build,
  - internal audit,
  - benchmark drift review,
  - promotion decision,
  - release freeze.

This changes the philosophy from **“do not update the reference”** to **“do not update the reference without a release process.”**

---

## Design principles

### 1. Releases are immutable

Once a reference release is published, it should not be overwritten.
If a correction is needed, create a new release such as `v1.1` or `v2` rather than silently modifying `v1`.

### 2. Candidates are mutable

Candidate references may be rebuilt and revised during exploration.
They are not benchmark standards until formally promoted.

### 3. Promotion must be explicit

A candidate should not become the operational reference automatically.
Promotion should require explicit review artifacts.

### 4. Backward compatibility matters

Reference updates should be evaluated against stable anchor queries.
CA1 and BU3 are the obvious starting points.

### 5. Engineering and biology both matter

A reference update is not only a technical event.
It can change biological interpretation.
A good release process must therefore assess:

- reproducibility,
- schema integrity,
- and biological drift.

---

## Proposed architecture

### A. Release layer

This is the immutable layer used for:

- benchmark runs,
- regression checks,
- figure generation,
- manuscript support,
- and stable comparison across organoid queries.

Examples:

- `fetal_lung_v1`
- `fetal_lung_v2`

### B. Candidate layer

This is the mutable staging layer used to test possible reference updates.

Examples:

- `candidate_2026-04_add_GW18_19`
- `candidate_2026-05_annotation_refresh`
- `candidate_2026-06_multiatlas_merge`

A candidate can be rebuilt many times. A release cannot.

---

## Suggested repository structure

```text
references/
  registry/
    reference_registry.csv
    current_release.yaml
  releases/
    fetal_lung_v1/
      reference_RNA.h5ad
      reference_metadata_v1.csv
      REFERENCE_PROVENANCE_v1.md
      REFERENCE_PROVENANCE_AUDIT_v1.md
      build_versions.csv
      codebook/
  candidates/
    2026-04-fetal-lung-v2rc1/
      build_manifest.yaml
      reference_RNA.h5ad
      reference_metadata.csv
      build_versions.csv
      codebook/
      audit/
```

This structure makes the distinction between immutable release artifacts and mutable candidate artifacts explicit.

---

## Compatibility with the current pipeline

The current pipeline does not need to be rewritten immediately.

### Phase 1

Keep using:

- `converted/reference_RNA.h5ad`
- `converted/reference_metadata_v1.csv`

Operationally, treat these as aliases for release `fetal_lung_v1`.

### Phase 2

Update benchmark configuration so that a run can specify:

- `reference_release = v1`
- `reference_release = v2`

and resolve the appropriate release files internally.

This allows the system to evolve without interrupting current workflows.

---

## Reference update workflow

### Step 1. Propose a change

Define what is changing.
Examples:

- broader gestational week coverage,
- additional donors,
- revised annotation mapping,
- source atlas change,
- metadata schema refinement.

### Step 2. Build a candidate reference

Create a candidate reference in a staging area.
Record:

- source dataset name,
- source checksum,
- included weeks,
- included donors/samples,
- filter rules,
- annotation mapping version,
- output tag,
- software versions.

### Step 3. Build the metadata adapter

Generate the metadata table corresponding to the candidate expression matrix.
At minimum, verify the integrity of:

- `sample_week`
- `stage_fine`
- `stage_coarse`
- `state_coarse`
- `state_fine`
- `group_internal`

### Step 4. Run internal candidate audit

Audit the candidate on its own terms.
Examples:

- matrix shape,
- `obs_names` / `var_names`,
- required metadata columns,
- missing IDs,
- duplicate IDs,
- non-negativity and layer semantics,
- codebook coverage,
- stage/state distributions.

### Step 5. Run benchmark regression

Project anchor queries onto the candidate reference and compare results against the current release.

Initial anchor queries:

- CA1
- BU3

### Step 6. Review biological drift

Evaluate whether observed changes are acceptable and interpretable.
Examples:

- top stage changes,
- top state changes,
- off-target fraction changes,
- state composition changes,
- epithelial remap changes.

### Step 7. Make a promotion decision

Possible outcomes:

- reject,
- hold,
- promote to next release.

### Step 8. Freeze the new release

If promoted:

- assign a version,
- store checksums,
- write provenance,
- write audit,
- write release note,
- update the registry,
- preserve the old release.

---

## Promotion criteria

A candidate reference does **not** need to be identical to the previous release.
If the reference is broadened or re-annotated, some biological movement is expected.

The right question is not “did anything change?”
The right question is “are the changes reproducible, explainable, and useful?”

### Must-pass criteria

- Candidate can be rebuilt from recorded scripts.
- Required metadata columns are present.
- Codebook decoding succeeds.
- Source and software versions are recorded.
- Existing releases are not overwritten.

### Drift criteria that may change but must be explained

- gene coverage,
- stage/state distributions,
- CA1 / BU3 top stage and top state,
- off-target fraction,
- epithelial remap structure.

### Promotion logic

- unexplained degradation → reject,
- explainable neutral change → hold or discuss,
- explainable improvement → candidate for promotion.

---

## New artifacts needed for this system

### 1. Reference registry

Examples:

- `REFERENCE_REGISTRY.csv`
- `current_release.yaml`

Suggested fields:

- release version,
- source dataset,
- source checksum,
- included weeks,
- included donors/samples,
- filtering rules,
- annotation schema version,
- build script hash,
- audit verdict,
- promotion date.

### 2. Generalized candidate build script

A generalized descendant of the current rebuild script.
For example:

- `build_reference_candidate_v1.R`

### 3. Generalized metadata extraction script

A generalized descendant of the current metadata extraction script.
For example:

- `extract_reference_metadata_candidate_v1.py`

### 4. Drift report template

For example:

- `REFERENCE_DRIFT_REPORT_<tag>.md`

This report should summarize differences between the current release and the candidate, using anchor queries.

---

## Scientific value of this system

The scientific value is not just that the reference becomes easier to update.
The more important value is that biological interpretation becomes more robust.

Without a versioned update system, the strongest statement we can make is:

- “This organoid looks like this fetal reference snapshot.”

With a versioned update system, we can ask stronger questions:

- Is that interpretation stable when the reference is broadened?
- Does adding new donors change the conclusion?
- Does refined annotation improve the explanation?
- Is a given organoid position robust across reference versions?

That is a more meaningful scientific standard.

---

## Near-term implementation priorities

1. Register the current frozen pair as **release v1**.
2. Generalize the current rebuild scripts into candidate-capable scripts.
3. Add a drift report comparing candidate vs release.
4. Version query provenance as well, including organoid-to-CA1/BU3 extraction.

---

## Conclusion

The key idea is not to abandon the frozen reference.
The key idea is to reinterpret it as **one release in a versioned reference system**.

The current design was the correct design for establishing reproducibility and benchmark stability.
The next design problem is different: how to support future reference updates without losing those properties.

The proposed solution is a controlled lifecycle:

- build candidate,
- audit candidate,
- benchmark candidate,
- review drift,
- promote deliberately.

This approach preserves the value of the current frozen pair while making it possible to extend the fetal reference over time in a way that remains reproducible, reviewable, and biologically interpretable.
