# GSE289846 Registration Note v1

## Registration date
2026-04-06

## Dataset identity
- **Series**: GSE289846
- **Title**: Human iPSC-based Modeling of Pulmonary Fibrosis Reveals p300/CBP
  Inhibition Suppresses Alveolar Transitional Cell State [scRNA-seq]
- **Lab**: Gotoh lab, Center for iPS Cell Research and Application (CiRA),
  Kyoto University, Japan
- **Paper**: Tsutsui Y et al., Nat Commun 2026; 17:1214. PMID 41680175.
- **Organism**: Homo sapiens (verified from GPL24676 platform metadata)
- **iPSC line**: B2-3
- **Assay**: scRNA-seq, 10x Chromium Single Cell 3' v3.1
- **Processing**: CellRanger 7.1.0, hg38 (refdata-gex-GRCh38-2020-A)

## GEO structure

### 6 GSM samples (2 replicates x 3 conditions)

| GSM | Title | Condition | Treatment | Day |
|-----|-------|-----------|-----------|-----|
| GSM8800137 | 3i_1_Day7 | DCIK+3i (iAT2 baseline) | DCIK+3i | Day7 |
| GSM8800138 | 3i_2_Day7 | DCIK+3i (iAT2 baseline) | DCIK+3i | Day7 |
| GSM8800133 | 3i_LATS_1_Day14 | AT1 induction | DCIK+3i → DCI+LATS-IN-1 | Day14 |
| GSM8800134 | 3i_LATS_2_Day14 | AT1 induction | DCIK+3i → DCI+LATS-IN-1 | Day14 |
| GSM8800135 | 3i_PAL_1_Day14 | Transitional state | DCIK+3i → PAL | Day14 |
| GSM8800136 | 3i_PAL_2_Day14 | Transitional state | DCIK+3i → PAL | Day14 |

### 9 series-level supplementary files (3 condition-level triplets)

| Condition | Files |
|-----------|-------|
| 3i_Day7 | barcodes.tsv.gz, features.tsv.gz, matrix.mtx.gz |
| 3i_LATS_Day14 | barcodes.tsv.gz, features.tsv.gz, matrix.mtx.gz |
| 3i_PAL_Day14 | barcodes.tsv.gz, features.tsv.gz, matrix.mtx.gz |

Per-GSM supplementary files: **NONE** (all 6 GSMs have supplementary = NONE).

### Registry unit decision
Public count matrices are condition-level (3 triplets merging 2 replicates each),
not per-GSM (6 triplets). Registration v1 uses **3 condition-level rows** as
canonical registry units. Replicate GSM provenance is preserved in
`source_sample_id` and `notes` columns.

## Why this dataset was selected
1. **Independent lab**: First non-BU, non-Rawlins lab in the comparison world
2. **Biology value**: AT2/AT1/transitional axis complements GSE221343
3. **Technical fit**: 10x Chromium, CellRanger mtx, Homo sapiens, hg38
4. **Published**: Nat Commun, PMID 41680175
5. **Low friction**: 3 condition-level triplets, clear naming, no mixed organs

## What remains before query-ready
1. Download 9 supplementary files to `queries/raw/gse289846/`
2. Convert mtx triplets to H5AD
3. Gate A: object contract verification (raw, counts layer, gene overlap)
4. Gate B: provenance / row identity check
5. Gate C: projection smoke test on current release v1
6. Gate D: within-tranche biology coherence review
7. Explicit reviewer promotion decision
