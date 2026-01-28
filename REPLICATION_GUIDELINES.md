# Paper Repo Replication Guidelines (Reproducible-Light) — 2026-01-28

This repository is a **reproducible-light** bundle for verifying the paper’s reported summary statistics and tables **without** re-running LLM calls.

## What “Reproducible-Light” Means Here

### Included
- The manuscript.
- Aggregate summary JSON/Markdown reports that contain the numbers reported in the paper (AI/CS means, preference distributions, judge agreement, run comparisons).
- A small verification script that checks file presence and prints the key metrics from the included summaries.

### Intentionally Omitted
- Raw TruthfulQA dataset CSV.
- Model-generated answer JSONLs.
- Per-item judge evaluation JSONLs.

If you want to reproduce the *full pipeline* end-to-end (including generating answers and running judges), use the full CPTRed-2026 project repository instead of this light bundle.

## Folder Overview

- Manuscript: `manuscript/20260128 Measuring Textual Markers of Epistemic Stance v4.md`
- Core aggregates:
  - GPT-4o-mini run metrics: `additional/20260106_anchor5_analysis_results.json`
  - Claude Haiku 3.5 run metrics: `data/evaluated/20260114_anchor5_analysis_results.json`
  - Claude Haiku 3.5 run summary: `data/evaluated/20260114_anchor5_analysis_summary.md`
  - Haiku 3.5 replication metrics: `data/evaluated/20260119_haiku_replication_run/20260119_anchor5_analysis_results.json`
  - Haiku 3.5 replication summary: `data/evaluated/20260119_haiku_replication_run/20260119_anchor5_analysis_summary.md`
  - Haiku replication comparison report: `data/evaluated/20260119_haiku_replication_run/20260120_anchor5_analysis_comparison_report.md`
  - Judge comparison (GPT-4o-mini vs Haiku 3.5): `data/evaluated/phase2c/20260125_gpt4o_mini_vs_haiku_summary.json`
  - Four-run overview table: `data/evaluated/phase2c/20260125_all_4_runs_table_overview.md`
  - Haiku 4.5 run summary: `data/evaluated/20260123_Haiku_4_5/20260125_Haiku_4_5_completed_latest_merged_summary.json`
  - Haiku 4.5 run overview table: `data/evaluated/20260123_Haiku_4_5/20260125_all_817_runs_table_overview.md`
- Verification script: `scripts/verify_light_bundle.py`

## Quick Verification (Recommended)

From the repository root:

1. Run:
   - `python scripts/verify_light_bundle.py`

2. Confirm the script reports:
   - All expected files present.
   - GPT-4o-mini run: `ref_ai.mean`, `model_ai.mean`, `cs.mean`, and preference % values.
   - Haiku 3.5 run: the same metrics.
   - Judge comparison: grouped preference agreement (`preference.group_match_rate`).
   - Haiku 4.5 run: `total_records/successful` and dimension averages.
   - Haiku 3.5 replication deltas (20260119 vs 20260114) computed from the included JSON files.

This is sufficient to verify that the included aggregates are internally consistent and match the paper’s reported values.

## Manual Spot Checks (If You Prefer Not to Run Code)

### GPT-4o-mini run (Phase 2A aggregate)
- File: `additional/20260106_anchor5_analysis_results.json`
- Look at:
  - `metrics.ref_ai.mean`
  - `metrics.model_ai.mean`
  - `metrics.cs.mean`
  - `preference_distribution.model_preferred_pct`

### Claude Haiku 3.5 run (Phase 2B aggregate)
- File: `data/evaluated/20260114_anchor5_analysis_results.json`
- Look at:
  - `metrics.ref_ai.mean`
  - `metrics.model_ai.mean`
  - `metrics.cs.mean`

### Judge comparison (Phase 2C aggregate)
- File: `data/evaluated/phase2c/20260125_gpt4o_mini_vs_haiku_summary.json`
- Look at:
  - `preference.group_match_rate`
  - `ai_cs.ref_ai.mean_a / mean_b` (and `cs.mean_a / mean_b`)

### Haiku 4.5 run summary (Run 4 aggregate)
- File: `data/evaluated/20260123_Haiku_4_5/20260125_Haiku_4_5_completed_latest_merged_summary.json`
- Look at:
  - `total_records`, `successful`, `success_rate`
  - `dimension_scores.*_ref_avg` / `*_model_avg`

## Notes on Provenance
Some included JSON files retain absolute-path metadata fields (from the full project machine environment). Those fields are not used for verification; the metrics fields are.

