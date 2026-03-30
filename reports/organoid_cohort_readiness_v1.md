# Organoid cohort readiness assessment v1

## Decision summary

| Item | Value |
|---|---|
| Assessment date | 2026-03-30 |
| Required threshold | >= 4 additional query-ready samples beyond CA1/BU3 |
| Actual additional samples | 0 |
| **Verdict** | **STOP / NOT READY** |
| Next priority | Acquire additional real organoid data |

---

## Inventory result

### Data sources examined

| Source | Type | Organoid samples found |
|---|---|---|
| `GSE266789_hPSC_fetal_lung_organoids.rds` | hPSC fetal lung organoids | 2 (CA1, BU3) |
| `GSE264407_full_fetal_lung_dataset_04142025.rds` | Fetal tissue atlas | 0 (not organoid) |
| 15+ additional local h5ad files | Tissue/mouse/spatial/synthetic | 0 (not organoid) |

### Query-ready samples

| query_id | Source | Cells | Anchor status | Gene overlap with v1 |
|---|---|---|---|---|
| CA1 | GSE266789 | 1,719 | Anchor | 96.9% |
| BU3 | GSE266789 | 731 | Anchor | 96.9% |

### Additional query-ready samples beyond anchors

**0**

The entire `GSE266789` source contains only these 2 samples. No other
organoid data exists locally.

---

## Why Phase B is blocked

Phase B (cohort runner implementation) requires a manifest of organoid queries
large enough to enable comparative analysis. The minimum viable cohort is
6 total samples (2 anchors + 4 new).

Current state:
- Anchors exist: CA1 and BU3 (already benchmarked and validated)
- New organoid queries: **none**
- The benchmark runner, query manifest format, and reference system are all
  ready to accept new queries
- The blocking constraint is **data availability**, not infrastructure

---

## What data is missing

To reach the minimum cohort threshold, at least 4 additional organoid samples
are needed. Desirable properties for cohort diversity:

- **Different organoid lines** (beyond CA1 and BU3)
- **Different donors or clones** (genetic diversity)
- **Different culture time points** (developmental trajectory)
- **Different protocol variants** (robustness assessment)
- **Sufficient cell count** (>= 200 cells per sample for stable projections)

Potential data sources to investigate:

1. Additional GEO deposits containing hPSC fetal lung organoid scRNA-seq
2. Lab-internal organoid culture runs not yet deposited
3. Collaborator-shared datasets
4. Other published fetal lung organoid studies (check CellxGene, HCA)

---

## What extraction/provenance work would be needed once new organoid data is available

For each new organoid sample:

1. **Identify sample identity** from source metadata (e.g., `orig.ident` or equivalent)
2. **Extract per-sample h5ad** using the established pattern:
   - Subset by sample identity
   - Ensure full gene set (not HVG subset)
   - Match reference var_names where possible (28,648 or 30,852 genes)
3. **Add provenance metadata** to obs:
   - `sample_id`, `donor_id`, `source_type`, `batch_id`, `expected_stage_text`
4. **Write `_clean.h5ad`** to `converted/` or a new query directory
5. **Add row to query manifest** with appropriate `query_id`, `h5ad_path`, and metadata
6. **Update `ORGANOID_QUERY_PROVENANCE_v1.md`** with new sample details
7. **Update `metadata/organoid_data_inventory_v1.csv`** with new inventory rows

No new extraction scripts are needed — the existing conversion and splitting
pattern used for CA1/BU3 is sufficient. A reusable extraction script would be
beneficial if the number of new samples exceeds ~5.

---

## Recommended next action order

1. **Search for additional public organoid data.** This is the highest-priority
   action. The entire pipeline is blocked on data availability.
2. **If new data is found:**
   a. Download and inspect the source object
   b. Extract per-sample queries in `_clean.h5ad` format
   c. Update inventory and provenance documents
   d. Re-assess cohort readiness
3. **If >= 4 new query-ready samples are confirmed:**
   a. Build `metadata/organoid_query_manifest_v1.csv`
   b. Implement `run_organoid_cohort_v1.py`
   c. Run first cohort tranche on release v1
4. **If < 4 new samples are found:**
   a. Document what was found
   b. Assess whether a smaller pilot (e.g., 2 new + 2 anchors) is informative
   c. Decide whether to wait for more data or proceed with a reduced scope
