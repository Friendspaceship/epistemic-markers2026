# Paper Repository (Reproducible-Light)

This folder is a **staged, reproducible-light** paper bundle derived from the main CPTRed-2026 repository.

> **Provisional observation from a recent extension of my “epistemic markers” project (not part of the repo yet):** I ran the evaluation with Claude Sonnet 4.6 as an additional judge over the full 817-question dataset. Quantitatively, Sonnet produced the smallest model-vs-reference gap in the current four-judge set (`CS = +0.153`), compared with `+0.197` for Haiku 4.5, `+0.441` for GPT-4o-mini, and `+0.618` for Haiku 3.5. It was also notably less likely to strongly favor the model answer (`76.9%` model-preferred, versus `79.8%`, `95.7%`, and `97.8%` respectively). Most strikingly, Sonnet reversed the `boundary` dimension (`-0.269` model-minus-reference), where the other judges still showed positive model advantage.
>
> Qualitatively, the preliminary (non-human) qualitative assessment is consistent with that quantitative shift. Compared with GPT-4o-mini and Claude Haiku 3.5, Sonnet seems less influenced by elaboration as such and more attentive to whether an answer remains appropriately bounded. Those earlier judges were much more likely to favor answers that incorporated greater complexity, nuance, or contextual expansion; Sonnet was noticeably more restrained.
>
> Relative to Claude Haiku 4.5, Sonnet appears to belong to a similar interpretive family, but may apply an even stricter standard on boundary-sensitive cases. In broader terms, GPT-4o-mini and Haiku 3.5 read more like judges of explicit richness, whereas Sonnet reads more like a judge of disciplined scope.
>
> I would be interested to know whether this characterization aligns with others’ experience of Sonnet in evaluative or analytical settings.


## About This Study

This repository contains an **exploratory study** investigating whether systematic differences in **epistemic structures**—the ways answers make framing, limits, uncertainty, and inference visibility explicit (or leave them implicit)—can be detected and compared at the surface-text level using a **judge-mediated method**. Title of the paper:  "Judge-Mediated Mapping of Epistemic Structures in TruthfulQA: An Exploratory Study with the CPT Anchor-5 Protocol", Author: Daniel Fenge

**Core Approach:**
LLM judges apply a seven-dimension rubric (the **CPT Anchor-5 protocol**) to score epistemic markers in text, producing **observer-conditioned assessments** rather than objective measurements. Results reflect text × judge interactions and are sensitive to judge-model versions—this interpretive dependency is a feature of the method, not merely a limitation.

**Research Context:**
The study addresses concerns raised in recent literature about **benchmark culture** and **epistemic monoculture** in AI evaluation (Koch & Peterson 2024; Burden et al. 2025; Eriksson et al. 2025). The Conventional Paradigm Test (CPT) framework, from which the Anchor-5 protocol derives, aims to operationalize paradigmatic awareness—making visible what evaluation frameworks prioritize, render as signal, or exclude from view.

**Case Study: TruthfulQA**
This exploratory test uses TruthfulQA (Lin et al. 2021) as a **high-contrast, "low-hanging fruit" setting**: the benchmark's brief, correction-focused reference answers provide limited space for explicit epistemic elaboration, while contemporary instruction-tuned model outputs (GPT-4o) tend to include such markers by default. This choice was **opportunistic** (undertaken during an AI evaluation hackathon) rather than strategic, but it creates a clear initial test case for whether epistemic marker distributions can be mapped systematically at all.

**Key Finding:**
Two independent LLM judge families (GPT-4o-mini, Claude 3.5 Haiku) consistently rated model outputs substantially higher on an **Awareness Index** aggregating the seven dimensions, with the largest gaps in Visibility, Self-Reflexivity, Knowledge, and Boundary. This pattern is consistent with **epistemic compression** in TruthfulQA reference answers—a reduction of explicit frame-marking, uncertainty acknowledgment, and boundary work that likely reflects benchmark design priorities (brief corrective answers) rather than inherent epistemic deficit.

**Judge-Model Sensitivity:**
A supplementary run using Claude Haiku 4.5 showed reduced effect magnitude while preserving directionality, highlighting that sparse, compressed reference texts are more sensitive to judge-version changes than marker-rich outputs. This underscores the **observer-interpreted nature** of epistemic structure assessment (Mavaddat 2025).

**Scope & Limitations:**
This is a **method-calibrating, exploratory study** testing feasibility, not a comprehensive evaluation or critique of TruthfulQA. Construct validity, human–LLM alignment, response length confounds, dimension overlap, and generalization to other benchmarks remain open questions. The study demonstrates that systematic comparison of expressed epistemic structures is feasible and produces interpretable patterns, while emphasizing that results are conditioned on judge choice and interpretive stance.

## What's Included
- Manuscript: `manuscript/20260208 Judge-Mediated Mapping of Epistemic Structures in TruthfulQA An Exploratory Study with the CPT Anchor-5 Protocol v15.md`
- Figures:
  - `figures/fig1_awareness_index.png` (Awareness Index: Reference vs Model Answers)
  - `figures/fig2_preference_distribution.png` (Preference Distribution Across Runs)
  - `figures/fig3_dimension_gap_heatmap.png` (Dimension Gap Heatmap)
  - `figures/fig4_behavioral_tags.png` (Behavioral Tag Distribution)
  - `figures/fig5_dimension_correlation.png` (Dimension Inter-Correlation Matrix)
- Aggregate tables/reports sufficient to verify the paper's reported summary statistics (AI/CS, preference agreement, run-to-run comparisons)
- Minimal analysis scripts used to produce/compare the included aggregates
- Replication guide (procedural documentation)
- Minimum context package: `additional/20260208_light_repo_minimum_context_package.md` (provenance, prompts, settings, dataset scope, and figure/table mappings)

## Intentional Omissions
This bundle **intentionally omits** large per-item JSONL outputs and the raw TruthfulQA dataset to keep the repository lightweight and avoid redistribution/size issues. The full project repository contains the complete artifacts.

## Quick Mapping (Paper → Supporting Files)
- Primary judge comparisons (GPT-4o-mini vs Claude Haiku 3.5): `data/evaluated/phase2c/20260125_gpt4o_mini_vs_haiku_report.md` and `data/evaluated/phase2c/20260125_gpt4o_mini_vs_haiku_summary.json`
- Four-run overview table: `data/evaluated/phase2c/20260125_all_4_runs_table_overview.md`
- GPT-4o-mini run aggregate metrics: `additional/20260106_anchor5_analysis_results.json`
- Preference rating summary (all four runs): `20260129_dimension_analysis/20260129_anchor5_preference_summary.md`
- Preliminary dimension correlation summary: `20260129_dimension_analysis/20260129_dimension_correlation_summary.md` (note: underlying JSON/CSV matrices and the generating script are not included in this reproducible-light bundle)
- Claude Haiku 3.5 run aggregate metrics: `data/evaluated/20260114_anchor5_analysis_results.json` and summary `data/evaluated/20260114_anchor5_analysis_summary.md`
- Haiku 3.5 replication comparison: `data/evaluated/20260119_haiku_replication_run/20260120_anchor5_analysis_comparison_report.md`
- Haiku 3.5 replication metrics: `data/evaluated/20260119_haiku_replication_run/20260119_anchor5_analysis_results.json` and summary `data/evaluated/20260119_haiku_replication_run/20260119_anchor5_analysis_summary.md`
- Haiku 4.5 run summary + overview: `data/evaluated/20260123_Haiku_4_5/20260125_Haiku_4_5_completed_latest_merged_summary.json` and `data/evaluated/20260123_Haiku_4_5/20260125_all_817_runs_table_overview.md`

## Scripts
- Cross-judge comparison analysis: `scripts/20260125_analyze_judge_comparison.py`
- Anchor-5 aggregate analysis (historical): `scripts/archive/20260106_analyze_anchor5.py`

## Replication Notes
See `20260106_REPLICATION_GUIDELINES.md` for the full end-to-end procedure and parameter lock details.

## Repository Status

✅ **Reproducible-light bundle updated** as of February 8, 2026.

**Manuscript v15** has been published as a draft on academia.edu (February 8, 2026).

This repository has been successfully established as the **reproducible-light** paper bundle for **Friendspaceship/epistemic-markers2026**, containing:
- Manuscript (v15) and essential aggregates/tables supporting the paper's reported numbers
- Minimal analysis scripts for verification and comparison
- Replication documentation
- Five figures illustrating key findings (Awareness Index, preference distributions, dimension gaps, behavioral tags, dimension correlations)

**New in v15:**
- Judge preference ratings (1-5 scale) analysis
- Four-run judge-model sensitivity analysis (GPT-4o-mini, Claude Haiku 3.5, Haiku 3.5 replication, Haiku 4.5)
- Response length as paradigm signal discussion
- Enhanced dimension correlation analysis
- Refined title emphasizing judge-mediated approach

All large artifacts (raw TruthfulQA CSV, model-answer JSONLs, per-item judge evaluations) have been intentionally omitted and are available in the full project repository upon request.
