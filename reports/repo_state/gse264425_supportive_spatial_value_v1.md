# GSE264425 supportive spatial value note

## Date
2026-04-09

## Scope
Repo-state diagnostic note. Not a governance change, not a reference
change, not a comparison-world admission decision. This note assesses
whether GSE264425 has value as a supportive spatial lane and recommends
a next step.

---

## Current status

GSE264425 (Quach et al., Nature 2024, PMID:39003323) is registered
and spatial-object-audit-complete. Two FFPE fetal lung Xenium samples
(GW15 and GW18) with a 339-gene targeted panel (289 human lung base +
50 custom CFVU2E). Framed as a supportive spatial lane — not part of
the current comparison-world core. Public main is unchanged by this
note.

## Why this dataset matters

The current comparison world is built entirely from scRNA-seq data.
No spatial evidence is part of the accepted tranche set. GSE264425
provides what the comparison world cannot: spatial localization context
for the epithelial states defined by scRNA projection.

The two samples cover GW15 (overlapping mid_GW14_16, the anchor-only
stage) and GW18 (overlapping late_GW17_19, the dominant comparison-world
stage). The 339-gene panel includes markers relevant to the key
epithelial states — CFTR, SOX2, NKX2-1, SFTPC, HOPX, AGER, SCGB1A1
among others. This is sufficient for marker-panel-level corroboration:
checking whether CFTR-rich or progenitor-like cells occupy plausible
spatial positions in the fetal lung.

This is particularly useful for:
- Corroborating whether the SOX2lowCFTR+ state (the most replicated
  condition-dependent state in the comparison world) has a coherent
  spatial niche in distal fetal lung tissue
- Providing spatial context for mid-fetal epithelial states at GW15,
  relevant to the newly accepted GSE221342 iAT2 mid-stage row
- Supporting future interpretive questions without requiring core
  comparison-world admission

## What is already resolved

The spatial object audit confirmed:
- Per-GSM object types are consistent (one inventory class)
- Recommended later-use object: `cell_feature_matrix.zarr.zip` (53-67 Mb)
- The 339-gene panel is appropriately framed as supportive corroboration,
  not direct canonical projection input
- The dataset is technically coherent as a supportive spatial lane

## What is still unresolved

- No raw object has been downloaded into repo workflows
- No conversion or projection has been done
- Whether this dataset should ever enter the comparison-world core has
  not been discussed
- Whether the 339-gene panel covers the specific discriminating genes
  for SOX2lowCFTR+ vs Proliferating progenitors has not been verified
  (requires downloading the 4 Kb features.tsv.gz)

## Value assessment

**Does this have value as a supportive spatial lane? Yes.**

It adds a dimension (spatial localization) that the scRNA comparison
world fundamentally cannot provide. The object audit shows low-friction
later-use: a compact zarr cell-feature matrix is already identified as
the recommended starting point. The two developmental timepoints (GW15,
GW18) align with the comparison world's two primary stage windows.

**Why not convert or project now?** No immediate biology question
requires spatial analysis. The 339-gene panel is too limited for
standard whole-transcriptome projection. The dataset's value is as
reserve corroboration — ready to answer spatial localization questions
when they arise, not as an immediate analytical priority.

## Recommendation

Keep GSE264425 as a registration-only supportive spatial lane. The
object inventory is understood. Do not download, convert, or project
yet. If revisited, start only from `cell_feature_matrix.zarr.zip` as
identified in the spatial object audit.

This dataset is useful as supportive spatial corroboration for mid/late
fetal epithelial localization, but it is not part of the current
comparison-world core and should not be treated as a query-ready tranche.

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
