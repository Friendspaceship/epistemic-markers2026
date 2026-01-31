# Paper Repository (Reproducible-Light)

This folder is a **staged, reproducible-light** paper bundle derived from the main CPTRed-2026 repository.

## What's Included
- Manuscript: `manuscript/20260128 Measuring Textual Markers of Epistemic Stance v4.md`
- Aggregate tables/reports sufficient to verify the paper's reported summary statistics (AI/CS, preference agreement, run-to-run comparisons)
- Minimal analysis scripts used to produce/compare the included aggregates
- Replication guide (procedural documentation)

## Intentional Omissions
This bundle **intentionally omits** large per-item JSONL outputs and the raw TruthfulQA dataset to keep the repository lightweight and avoid redistribution/size issues. The full project repository contains the complete artifacts.

## Quick Mapping (Paper → Supporting Files)
- Primary judge comparisons (GPT-4o-mini vs Claude Haiku 3.5): `data/evaluated/phase2c/20260125_gpt4o_mini_vs_haiku_report.md` and `data/evaluated/phase2c/20260125_gpt4o_mini_vs_haiku_summary.json`
- Four-run overview table: `data/evaluated/phase2c/20260125_all_4_runs_table_overview.md`
- GPT-4o-mini run aggregate metrics: `additional/20260106_anchor5_analysis_results.json`
- Preference rating summary (all four runs): `additional/20260129_anchor5_preference_summary.md`
- Preliminary dimension correlation summary: `additional/20260129_dimension_correlation_summary.md` (note: underlying JSON/CSV matrices and the generating script are not included in this reproducible-light bundle)
- Claude Haiku 3.5 run aggregate metrics: `data/evaluated/20260114_anchor5_analysis_results.json` and summary `data/evaluated/20260114_anchor5_analysis_summary.md`
- Haiku 3.5 replication comparison: `data/evaluated/20260119_haiku_replication_run/20260120_anchor5_analysis_comparison_report.md`
- Haiku 3.5 replication metrics: `data/evaluated/20260119_haiku_replication_run/20260119_anchor5_analysis_results.json` and summary `data/evaluated/20260119_haiku_replication_run/20260119_anchor5_analysis_summary.md`
- Haiku 4.5 run summary + overview: `data/evaluated/20260123_Haiku_4_5/20260125_Haiku_4_5_completed_latest_merged_summary.json` and `data/evaluated/20260123_Haiku_4_5/20260125_all_817_runs_table_overview.md`

## Scripts
- Cross-judge comparison analysis: `scripts/20260125_analyze_judge_comparison.py`
- Anchor-5 aggregate analysis (historical): `scripts/archive/20260106_analyze_anchor5.py`

## Replication Notes
See `REPLICATION_GUIDELINES.md` for the full end-to-end procedure and parameter lock details.

## Repository Status

✅ **Reproducible-light bundle migration complete** as of January 28, 2026.

This repository has been successfully established as the **reproducible-light** paper bundle for **Friendspaceship/epistemic-markers2026**, containing:
- Manuscript and essential aggregates/tables supporting the paper's reported numbers
- Minimal analysis scripts for verification and comparison
- Replication documentation

All large artifacts (raw TruthfulQA CSV, model-answer JSONLs, per-item judge evaluations) have been intentionally omitted and are available in the full project repository upon request.
