# Anchor-5 Analysis Comparison Report (20260114 vs 20260119)

## Inputs (4 analysis files)
- `data/evaluated/20260114_anchor5_analysis_summary.md`
- `data/evaluated/20260114_anchor5_analysis_results.json`
- `data/evaluated/20260119_haiku_replication_run/20260119_anchor5_analysis_summary.md`
- `data/evaluated/20260119_haiku_replication_run/20260119_anchor5_analysis_results.json`

## Assumptions
- This report compares the two Haiku analysis outputs as-is without recomputation.
- Differences reflect run coverage (successful count) and any run-time variability in the 20260119 replication.

## Coverage
- 20260114 successful: 817 of 817
- 20260119 successful: 808 of 817
- Success delta: -9

## AI/CS Means (20260119 - 20260114)
- Ref AI mean delta: -0.007956
- Model AI mean delta: -0.011628
- CS mean delta: -0.003672

## Preference Distribution Delta (20260119 - 20260114)
- ref_preferred: -1
- model_preferred: -7
- equal: -1
- ref_strong: -1
- ref_slight: 0
- model_slight: 1
- model_strong: -8

## Dimension Mean Deltas (Ref) (20260119 - 20260114)
- agency: -0.012508
- boundary: -0.022927
- goal: -0.018593
- knowledge: -0.001222
- reality: 0.000267
- self_reflexivity: -0.004187
- visibility: -0.004454

## Dimension Mean Deltas (Model) (20260119 - 20260114)
- agency: -0.008612
- boundary: -0.004163
- goal: -0.002557
- knowledge: 0.005806
- reality: 0.001047
- self_reflexivity: -0.007348
- visibility: -0.003361

## Source Summaries (verbatim excerpts)

### 20260114 Summary (first 60 lines)
````text
# Anchor-5 Analysis Summary (Haiku)

## Inputs
- Evaluation file: `<local-project-root>/CPTRed-2026/data/evaluated/claude_haiku_anchor5_817_canonical_working_fixed20260114.jsonl`
- Canonical file: `<local-project-root>/CPTRed-2026/data/processed/20260105_817_qna_answers_with_rowindex.jsonl`
- Analysis timestamp (UTC): `2026-01-14T00:03:37.145303+00:00`

## Coverage
- Total evaluations: 817
- Successful: 817
- Canonical matched: 817
- Coverage: 100.0%

## Epistemic Awareness Metrics (AI/CS)
- Reference AI mean: 0.3142 (median 0.3571, stdev 0.2119)
- Model AI mean: 0.9325 (median 0.9286, stdev 0.0844)
- CS mean (model - ref): 0.6183 (median 0.6429, stdev 0.2412)
- CS interpretation: Model shows MORE awareness

## Preference Distribution
- Reference preferred: 8 (1.0%)
- Equal: 10
- Model preferred: 799 (97.8%)

## Behavior Tags
### Reference
- DIRECT: 699
- REFUSE: 61
- CLARIFY: 42
- PLURALIST: 8
- META-AWARE: 7

### Model
- CLARIFY: 474
- PLURALIST: 192
- DIRECT: 104
- META-AWARE: 45
- REFUSE: 2

## Dimension Means (Ref / Model / Diff)
| Dimension | Ref Mean | Model Mean | Mean Diff |
| --- | --- | --- | --- |
| reality | 0.8017 | 1.9829 | 1.1812 |
| knowledge | 0.5569 | 1.9657 | 1.4088 |
| goal | 1.4419 | 1.9927 | 0.5508 |
| visibility | 0.2668 | 1.9204 | 1.6536 |
| agency | 0.6548 | 1.8935 | 1.2387 |
| self_reflexivity | 0.0685 | 1.3403 | 1.2717 |
| boundary | 0.6083 | 1.9596 | 1.3513 |
````

### 20260119 Summary (first 60 lines)
````text
================================================================================
ANCHOR-5 JUDGE EVALUATIONS ANALYSIS REPORT (CPTRed-2025 Metrics)
Generated: 2026-01-19 23:19:52 UTC
================================================================================

 OVERVIEW
Total Evaluations: 817
Successful: 808
Canonical Records Evaluated: 817
Coverage: 100.0%

 EPISTEMIC AWARENESS METRICS (CPTRed-2025)
Reference AI (Awareness Index):
  Mean: 0.3063, Median: 0.2857, StDev: 0.2144
  Range: [0.0000, 0.9286]
Model AI (Awareness Index):
  Mean: 0.9209, Median: 0.9286, StDev: 0.1259
  Range: [0.0000, 1.0000]
Compression Signal (CS = model_ai - ref_ai):
  Mean: 0.6146, Median: 0.5714, StDev: 0.2477
  Interpretation: Model shows MORE awareness

 PREFERENCE SCORES
Reference Preferred: 7 (0.9%)
Equal: 9
Model Preferred: 792 (98.0%)

  BEHAVIOR TAGS - REFERENCE ANSWERS
  DIRECT: 687
  REFUSE: 65
  CLARIFY: 44
  PLURALIST: 7
  META-AWARE: 5

  BEHAVIOR TAGS - MODEL ANSWERS
  CLARIFY: 467
  PLURALIST: 190
  DIRECT: 103
  META-AWARE: 46
  REFUSE: 2

 EPISTEMIC DIMENSIONS (Mean Scores)
Dimension            Reference       Model           Diff      
------------------------------------------------------------
reality              0.80            1.98            1.18      
knowledge            0.56            1.97            1.42      
goal                 1.42            1.99            0.57      
visibility           0.26            1.92            1.65      
agency               0.64            1.88            1.24      
self_reflexivity     0.06            1.33            1.27      
boundary             0.59            1.96            1.37      

================================================================================
````
