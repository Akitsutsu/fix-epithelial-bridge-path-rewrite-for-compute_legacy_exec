# GSE289846 Registration v1

## Registration date
2026-04-06

## Status
Registration-only. No raw download, no H5AD conversion, no query-ready promotion.

## Dataset
- **GSE289846**: iPSC-derived alveolar epithelial organoids on micro-patterned plates
- **Lab**: Gotoh lab / CiRA, Kyoto University
- **Paper**: Tsutsui et al. 2026, Nat Commun. PMID 41680175.
- **iPSC line**: B2-3

## Registration rows (3 condition-level)

| Row ID | Condition | Treatment | Day | Source GSMs |
|--------|-----------|-----------|-----|------------|
| GSE289846_3i_Day7 | iAT2 baseline | DCIK+3i | Day7 | GSM8800137, GSM8800138 |
| GSE289846_3i_LATS_Day14 | AT1 induction | DCI+LATS-IN-1 | Day14 | GSM8800133, GSM8800134 |
| GSE289846_3i_PAL_Day14 | Transitional state | PAL medium | Day14 | GSM8800135, GSM8800136 |

## Why condition-level rows (not 6 per-replicate)
Public supplementary count matrices are condition-level (3 CellRanger mtx
triplets merging 2 replicates each). No per-GSM supplementary files exist.
Replicate-level separation would require barcode suffix parsing or SRA FASTQ
re-processing. Registration v1 aligns with the public count-space granularity.

## Source-of-truth verification
- GEO series page: verified organism (Homo sapiens), platform (GPL24676),
  supplementary files (9 files = 3 triplets), 6 GSMs with titles/characteristics
- Paper: PMID 41680175, Nat Commun 2026
- All 6 GSMs have per-GSM supplementary = NONE
- CellRanger 7.1.0, hg38 (refdata-gex-GRCh38-2020-A)

## Comparison to existing tranches

| Tranche | Lab | iPSC line | Conditions | Role |
|---------|-----|-----------|------------|------|
| CA1/BU3 | Kotton/BU | SPC2-ST-B2 | 2 anchor queries | anchor |
| GSE237359 | Rawlins/Cambridge | primary fetal | 4 donors | donor-resolved validation |
| GSE221343 | Kotton/BU | SPC2-ST-B2 | CK+DCI / YAP5SA / L+DCI | nearest external validation |
| **GSE289846** | **Gotoh/CiRA Kyoto** | **B2-3** | **3i / LATS / PAL** | **cross-lab validation** |

GSE289846 is the first independent-lab tranche. It adds cross-lab replication
with a different iPSC line and differentiation protocol, plus an AT1/AT2
transitional axis not present in existing tranches.

## Files created
- `metadata/external/gse289846_dataset_manifest_v1.yaml`
- `metadata/external/gse289846_organoid_query_sample_sheet_v1.tsv`
- `reports/tranches/gse289846_registration_v1/README.md` (this file)
- `reports/tranches/gse289846_registration_v1/gse289846_registration_note_v1.md`

## Next steps
1. Download 9 supplementary files → `queries/raw/gse289846/`
2. Convert mtx → H5AD
3. Gate A–D review
4. Explicit reviewer promotion decision
