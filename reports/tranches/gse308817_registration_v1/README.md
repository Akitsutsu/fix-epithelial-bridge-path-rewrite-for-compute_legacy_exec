# GSE308817 Registration v1

## Registration date
2026-04-06

## Status
Registration-only. No raw download, no H5AD conversion, no query-ready promotion.

## Dataset
- **GSE308817**: hESC-derived alveolar organoids at 3 passage timepoints
- **Lab**: Liu/Rong lab / Xiamen University
- **Cell line**: H9 hESC, wild type
- **Publication**: Citation missing (no PMID/DOI as of 2025-12-22)
- **Platform**: SeekOne (SeekGene), NOT 10x Chromium

## Registration rows (3 passage-level, 1 row = 1 GSM)

| Row ID | Passage | GSM | Filename prefix |
|--------|---------|-----|-----------------|
| GSE308817_ALOp3 | P3 (early) | GSM9253578 | ALOp3 |
| GSE308817_ALOp7 | P7 (middle) | GSM9253579 | ALOp7 |
| GSE308817_ALOp20 | P20 (late) | GSM9253580 | ALOp20 |

## Source-of-truth corrections from v2 screening
The v2 candidate screening (external_intake_candidate_screening_v2.tsv)
listed GSE308817 as "10x Chromium (GPL24676)". Re-verification found:
- **Platform correction**: SeekOne (SeekGene), not 10x Chromium. GPL24676
  is the sequencer (NovaSeq 6000), not the library prep.
- **System type correction**: hESC-derived (H9), not iPSC-derived or
  generic hPSC-derived. hPSC is technically correct as an umbrella term.
- **Processing**: SeekSoulTools v1.2.2, not CellRanger.

These corrections are documented in the manifest and sample sheet.

## Comparison to existing tranches

| Tranche | Lab | Cell line | Conditions | Platform | Role |
|---------|-----|-----------|------------|----------|------|
| CA1/BU3 | Kotton/BU | SPC2-ST-B2 (iPSC) | 2 anchors | 10x | anchor |
| GSE237359 | Rawlins/Cambridge | primary fetal | 4 donors | 10x | donor-resolved |
| GSE221343 | Kotton/BU | SPC2-ST-B2 (iPSC) | CK+DCI/YAP5SA/L+DCI | 10x | nearest external |
| GSE289846 | Gotoh/CiRA Kyoto | B2-3 (iPSC) | 3i/LATS/PAL | 10x | cross-lab |
| **GSE308817** | **Liu-Rong/Xiamen** | **H9 (hESC)** | **P3/P7/P20** | **SeekOne** | **passage-series** |

GSE308817 would be the first non-10x-Chromium tranche and uses a different
stem cell background (hESC H9 vs iPSC lines). Gene-space compatibility is
the primary validation concern.

## Files created
- `metadata/external/gse308817_dataset_manifest_v1.yaml`
- `metadata/external/gse308817_organoid_query_sample_sheet_v1.tsv`
- `reports/tranches/gse308817_registration_v1/README.md` (this file)
- `reports/tranches/gse308817_registration_v1/gse308817_registration_note_v1.md`

## Next steps
1. Download per-GSM mtx triplets → `queries/raw/gse308817/`
2. Convert mtx → H5AD
3. **Critical gate**: Verify gene-space compatibility (SeekOne vs 10x reference)
4. Gate A–D review
5. Explicit reviewer promotion decision
