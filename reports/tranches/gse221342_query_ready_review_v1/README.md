# GSE221342 Query-Ready Review v1

## Review date
2026-04-09

## Dataset
- GSE221342: iPSC-derived iAT2/iAT1 organoids in 3D and ALI culture
- Kotton lab / Boston University / Center for Regenerative Medicine
- 4 samples, single donor cell line BU3 NGAT, no multiplexing
- Same iPSC line as BU3 anchor query
- Boundary-stress tranche: tests mid-stage coverage gap and ALI culture format

## Reference
- Release v1: `converted/reference_RNA.h5ad` + `converted/reference_metadata_v1.csv`
- Stage axis: `sample_week`
- Execution: combined-root v2 canonical path

## Promotion scope
**All 4 rows promoted together as a boundary-stress tranche.**

| Row | Decision |
|-----|----------|
| GSM6858850_iAT2_3D | **promote** |
| GSM6858851_iAT1_3D | **promote** |
| GSM6858852_iAT1_ALI_p0 | **promote** |
| GSM6858853_iAT1_ALI_p1 | **promote** |

**Dataset-level decision**: All 4 rows promoted -> `query_ready_flag=true`,
status `accepted_query_ready`, role `nearest_external_validation`.

---

## Gate summary

### Gate A -- Object contract
All 4 pass. H5AD loadable, raw present, counts layer present, X
integer-valued, 91.98% reference gene overlap, obs/var columns intact.

### Gate B -- Provenance / row identity
All 4 pass. Single donor cell line BU3 NGAT. No demultiplexing needed.

### Gate C -- Projection smoke test
All 4 pass.

| Sample | WL cells | WL Epi% | WL top stage | Epi eligible | Epi OT% | Epi ambig% |
|--------|------:|---:|---|------:|---:|---:|
| iAT2 3D | 2,262 | 95.2% | **mid_GW14_16** (45.3%) | 2,154 | 4.8% | 15.6% |
| iAT1 3D | 1,973 | 96.1% | late_GW17_19 (86.0%) | 1,896 | 3.9% | 22.2% |
| iAT1 ALI p0 | 950 | 97.9% | late_GW17_19 (80.0%) | 930 | 2.1% | 18.2% |
| iAT1 ALI p1 | 1,269 | 99.1% | late_GW17_19 (95.0%) | 1,257 | 0.9% | 14.2% |

### Gate D -- Within-tranche biology coherence
All 4 pass. Clear monotonic gradient: iAT2 3D (Budtip progenitors) ->
iAT1 3D (SOX2lowCFTR+ 60.9%) -> ALI p0 (56.8%) -> ALI p1 (78.0%).
Alignment and off-target both improve along the gradient.

---

## Key findings

### First external mid_GW14_16 row
iAT2 3D maps to **mid_GW14_16 / week_15** at whole-lung level -- the
first external row at this stage. Previously, mid_GW14_16 was anchor-only
(CA1/BU3). This directly addresses the mid-stage coverage gap identified
in the coverage boundary audit.

### Cross-line SOX2lowCFTR+ replication
BU3 NGAT L+DCI -> SOX2lowCFTR+ (60.9-78.0%) replicates the same shift
seen on two other iPSC lines:
- SPC2-ST-B2 L+DCI (GSE221343): 34.8%
- B2-3 LATS-IN-1 (GSE289846): 31.8%

### ALI culture format is readable on v1
Both ALI conditions retain SOX2lowCFTR+ identity. ALI p1 (with 3D
pre-differentiation) produces the most resolved iAT1 in any tranche
(78.0%, alignment 0.773).

### This is NOT a P-0001 validation tranche
BU3 NGAT is a different iPSC line from SPC2-ST-B2 (the P-0001 basis).
The SOX2lowCFTR+ replication is cross-line evidence, not same-line
P-0001 validation.

---

## Decisions

| Sample | Decision | Rationale |
|--------|----------|-----------|
| GSM6858850_iAT2_3D | **promote** | First external mid_GW14_16 row; same-line-to-anchor baseline; defines the 3D->ALI axis starting point |
| GSM6858851_iAT1_3D | **promote** | SOX2lowCFTR+ dominant (60.9%); cross-line replication of iAT1 shift |
| GSM6858852_iAT1_ALI_p0 | **promote** | First ALI condition; SOX2lowCFTR+ retained (56.8%); new culture format axis |
| GSM6858853_iAT1_ALI_p1 | **promote** | Strongest SOX2lowCFTR+ in any tranche (78.0%); best alignment (0.773) |

## Artifacts
- `gse221342_query_ready_decisions_v1.tsv` -- machine-readable decision table (4 rows)
