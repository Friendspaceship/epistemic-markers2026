# Stepping into a Fireplace — preprint candidate25.31

Daniel Fenge ·16 November2026 · prepared locally for epistemic-markers2026; not yet uploaded.

## Read

- [Main paper](20261116_Stepping_into_a_Fireplace_draft25.31_CLI.pdf)
- [Technical companion](20261116_JMM_draft25.31_technical_companion_CLI.pdf)
- [Selected case appendix](20261116_JMM_draft25.31_selected_case_appendix_CLI.pdf)

Markdown and standalone HTML editions accompany each PDF. Keep this directory together so document and data links resolve. Version25.31 incorporates21evaluator configurations, including Sol6.1and Astra, revised interpretation and limitations, and the revised conclusion. Companion and appendix content derives from25.29, with release labels and links aligned to25.31; no new empirical analysis is implied by relabeling.

## Data and reproduction

The aggregate JSON and sixCSV summaries contain configuration means, dimensional gaps, historical15sign counts, historical12matched preferences, item-level composite comparisons and new-model preference profiles. These are display summaries, not the full frozen corpus or raw evaluator outputs. Full retained source materials remain available from the author on request. Private reviews, operational logs and internal validation records are not part of this release.

Regenerate the three SVG figures with Python's standard library:

```bash
python3 20261116_make_figures.py
```

Regenerate HTML/PDF with Python and PyMuPDF1.28.2 in an isolated environment:

```bash
python3 20261116_render_all.py
```

The older1.26.7renderer is not the verified environment for this package. The render script preserves Markdown sources, embeds figures, and writes exports to rendered/. No network call is required after the dependency is installed. SVG, PNG and standalone figurePDF files are in figures/. SHA256_manifest.json identifies the release files.

## Publication status

This is a preprint candidate, not a peer-reviewed or accepted paper. No DOI is assigned. The February2026version15paper remains a separate earlier version. Existing copyright and AI-assistance disclosures are retained; no additional license is granted by this package. TruthfulQA excerpts remain attributed to Lin, Hilton and Evans.

Suggested citation: Fenge, D. (2026). *Stepping into a Fireplace: Judge-Mediated Mapping of Epistemic Compression in TruthfulQA*. Preprint, version25.31,16 November2026.
