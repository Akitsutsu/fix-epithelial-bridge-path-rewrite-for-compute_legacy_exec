# Reference promotion scaffolding

This directory holds promotion decision records and templates for the
versioned fetal reference update system.

## What this is for

Promotion is the gate between a candidate reference that has been built and
evaluated and a new immutable release. This scaffolding provides:

- a formal criteria document (`REFERENCE_PROMOTION_CRITERIA_v1.md`)
- a decision record template (`example_release_promotion_decision.yaml`)
- a place to store actual decision records for future promotion reviews

This scaffolding does **not** automate the release-freeze step. It defines
the decision framework only.

## Intended lifecycle

```text
candidate build
  └─> drift report (structural + benchmark)
        └─> promotion decision (this layer)
              └─> release freeze (future — not yet implemented)
```

## What artifacts are expected before a decision

From the **candidate build** step:

- `<candidate-dir>/reference_RNA.h5ad`
- `<candidate-dir>/reference_metadata.csv`
- `<candidate-dir>/build_manifest.yaml`
- `<candidate-dir>/build_versions.csv`

From the **drift report** step:

- `REFERENCE_DRIFT_REPORT_<tag>.md`
- `reference_drift_summary_<tag>.json`
- `release_vs_candidate_structural_diff_<tag>.csv`
- `anchor_key_metrics_diff_<tag>.csv` (if benchmark mode was run)

## What a promotion review should include

A promotion decision record (`*_promotion_decision.yaml`) should contain:

- candidate identification (tag, directory, base release)
- links to all drift-report artifacts
- decision outcome (promote / hold / reject)
- rationale
- required follow-ups (if hold)
- approver and date

See `example_release_promotion_decision.yaml` for the full schema.

## How this differs from actual promotion/freeze

This scaffolding defines **what to decide** and **how to record the decision**.
It does **not**:

- copy candidate artifacts into a release directory
- compute checksums for release files
- update the reference registry CSV
- update `current_release.yaml`
- write release provenance or release notes

Those steps belong to a future release-freeze automation layer.

## Related documents

- `REFERENCE_UPDATE_SYSTEM_v1.md` — overall lifecycle design
- `REFERENCE_PROMOTION_CRITERIA_v1.md` — formal criteria for promotion decisions
- `references/drift/README.md` — drift report layer documentation
- `references/candidates/README.md` — candidate build layer documentation
- `references/registry/` — release registry
