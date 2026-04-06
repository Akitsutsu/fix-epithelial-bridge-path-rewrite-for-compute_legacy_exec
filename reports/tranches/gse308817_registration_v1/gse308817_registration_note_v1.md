# GSE308817 Registration Note v1

## Registration date
2026-04-06

## Dataset identity
- **Series**: GSE308817
- **Title**: Human Pluripotent Stem Cell-Derived Alveolar Organoids for
  Gene-editing and Lung Adenocarcinomas Modeling
- **Lab**: Liu/Rong lab, Xiamen University, China
- **Publication**: Citation missing — no PMID or DOI linked as of 2025-12-22
- **Organism**: Homo sapiens (verified from GPL24676 platform metadata)
- **Cell line**: H9 hESC, wild type
- **Library prep**: SeekOne Single Cell Whole Transcriptome Kit (SeekGene K00801)
- **Processing**: SeekSoulTools v1.2.2, hg38
- **Sequencer**: Illumina NovaSeq 6000 (GPL24676)

## Platform note
This dataset uses **SeekOne** (SeekGene) droplet-based library preparation,
**NOT 10x Chromium**. The output format is standard 10x-like sparse matrix
triplets (barcodes/features/matrix), but gene naming, barcode format, and
feature space may differ from CellRanger output. Compatibility with the
10x-based reference pipeline must be explicitly verified during conversion.

## GEO structure

### 3 GSM samples (1 per passage)

| GSM | Title | Passage | Filename prefix |
|-----|-------|---------|-----------------|
| GSM9253578 | Human lung organoid, period 3 | P3 (early) | ALOp3 |
| GSM9253579 | Human lung organoid, period 7 | P7 (middle) | ALOp7 |
| GSM9253580 | Human lung organoid, period 20 | P20 (late) | ALOp20 |

Note: GEO sample titles say "period" but overall design and filenames confirm
these are passage numbers. "Period" is likely a translation artifact.

### 9 per-sample supplementary files (3 per-GSM triplets)

| Sample | Files |
|--------|-------|
| ALOp3 | GSM9253578_ALOp3_{barcodes,features,matrix}.tsv.gz / .mtx.gz |
| ALOp7 | GSM9253579_ALOp7_{barcodes,features,matrix}.tsv.gz / .mtx.gz |
| ALOp20 | GSM9253580_ALOp20_{barcodes,features,matrix}.tsv.gz / .mtx.gz |

All 9 files are bundled in GSE308817_RAW.tar (366 MB).

## Citation status
No PMID or DOI linked. BioProject PRJNA1332757 is linked. The GEO title
suggests a paper on hPSC-derived alveolar organoids for gene-editing and
LUAD modeling, but the paper has not been deposited or linked. Registration
proceeds without publication citation — provenance relies on GEO metadata
alone. This is noted as a lower-confidence provenance chain compared to
GSE221343 (PMID 38642558) and GSE289846 (PMID 41680175).

## Why this dataset was selected
1. **Third independent lab**: Xiamen University (vs BU, Cambridge, Kyoto)
2. **Passage/maturation axis**: P3/P7/P20 adds temporal stability assessment
3. **hESC H9 line**: New stem cell background (vs iPSC SPC2-ST-B2 and B2-3)
4. **Low friction**: Per-sample triplets, clear naming, hg38

## Risk factors
1. **SeekOne ≠ 10x**: Gene-space compatibility not yet verified
2. **Citation missing**: Lower provenance confidence
3. **H9 hESC**: Different from iPSC lines in existing world — may project differently

## What remains before query-ready
1. Download GSE308817_RAW.tar or per-GSM files to `queries/raw/gse308817/`
2. Convert mtx triplets to H5AD
3. **Verify gene-space compatibility** — this is the critical gate given SeekOne platform
4. Gate A: object contract verification
5. Gate B: provenance / row identity check
6. Gate C: projection smoke test on current release v1
7. Gate D: within-tranche biology coherence review
8. Explicit reviewer promotion decision
