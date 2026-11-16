# Stepping into a Fireplace — preprint candidate 25.32

Daniel Fenge · 16 November 2026 · prepared for epistemic-markers2026; this revision has not yet been uploaded.

## Read

- [Main paper — Markdown](20261116_Stepping_into_a_Fireplace_draft25.32_CLI.md) · [PDF](20261116_Stepping_into_a_Fireplace_draft25.32_CLI.pdf)
- [Technical companion](20261116_JMM_draft25.32_technical_companion_CLI.pdf)
- [Selected case appendix](20261116_JMM_draft25.32_selected_case_appendix_CLI.pdf)

Each document is included in Markdown, PDF and standalone HTML. Keep the folder structure intact so links resolve.

## Change from version 25.31

The main paper now includes the mean Compression Signal chart for all 21 evaluator configurations in §3.1 (Figure 1). The dimensional heatmap and its references are renumbered Figure 2. The chart was already included in the companion; numerical results are unchanged. Companion and appendix content remains that of 25.29, with labels and links aligned to release 25.32.

## Summary data and reproduction

The aggregate JSON and six CSV files contain configuration means, dimensional gaps, the historical fifteen-configuration sign summary, historical twelve-configuration preference statistics, item-level composite counts and new-model preference profiles. These summaries reproduce the displays; they do not replace the full item-level analysis. Full retained inputs, outputs and execution records remain available from the author on request.

Generate the three SVG figures with standard Python:

```bash
python3 20261116_make_figures.py
```

Render all documents with Python and PyMuPDF 1.28.2 in an isolated environment:

```bash
python3 20261116_render_all.py
```

Exports are written to `rendered/`. Rendering needs no network access after dependency installation. The checked runtime is PyMuPDF 1.28.2; the earlier 1.26.7 runtime is not the verified environment for this package. Vector SVGs, PNGs and standalone figure PDFs are supplied in `figures/`. `SHA256_manifest.json` identifies the release files.

## Publication status

This is an exploratory preprint candidate, not a peer-reviewed or accepted paper. No DOI is assigned. Earlier versions remain separate historical records. Existing copyright and AI-assistance disclosures are retained; no additional license is granted. TruthfulQA excerpts remain attributed to Lin, Hilton and Evans. Private reviews, chatlogs and raw provider outputs are not included.

Suggested citation: Fenge, D. (2026). *Stepping into a Fireplace: Judge-Mediated Mapping of Epistemic Compression in TruthfulQA*. Preprint, version 25.32, 16 November 2026.
