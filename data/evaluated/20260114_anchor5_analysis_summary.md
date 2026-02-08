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
