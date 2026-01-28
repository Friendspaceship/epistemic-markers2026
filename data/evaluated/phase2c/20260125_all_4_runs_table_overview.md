# Phase 2C: All 4 Runs Table Overview

## Inputs
- gpt4o_mini_817: `data\evaluated\gpt4o_mini_anchor5_817_full_20260106_001318.jsonl`
- haiku_20260114_canonical: `data\evaluated\claude_haiku_anchor5_817_canonical_working_fixed20260114.jsonl`
- haiku_20260119_canonical: `data\evaluated\20260119_haiku_replication_run\20260119_haiku_anchor5_817_canonical.jsonl`
- haiku_20260125_completed_latest: `data\evaluated\20260123_Haiku_4_5\20260125_Haiku_4_5_completed_latest_merged.jsonl`

## Notes
- completed_latest_merged.jsonl is success-only; totals shown are canonical (817) with failed counts inferred from missing RowIndex values.

## Judge Models
- gpt4o_mini_817: gpt-4o-mini
- haiku_20260114_canonical: claude-3-5-haiku-20241022
- haiku_20260119_canonical: claude-3-5-haiku-20241022
- haiku_20260125_completed_latest: claude-haiku-4-5-20251001

## Coverage
| Run | Judge Model | Total | Successful | Failed | Success Rate |
| --- | --- | ---:| ---:| ---:| ---:|
| gpt4o_mini_817 | gpt-4o-mini | 817 | 817 | 0 | 1.0000 |
| haiku_20260114_canonical | claude-3-5-haiku-20241022 | 817 | 817 | 0 | 1.0000 |
| haiku_20260119_canonical | claude-3-5-haiku-20241022 | 817 | 808 | 9 | 0.9890 |
| haiku_20260125_completed_latest | claude-haiku-4-5-20251001 | 817 | 808 | 9 | 0.9890 |

## AI/CS Means (computed from Anchor-5 scores)
| Run | Judge Model | Ref AI Mean | Model AI Mean | CS Mean |
| --- | --- | ---:| ---:| ---:|
| gpt4o_mini_817 | gpt-4o-mini | 0.4600 | 0.9008 | +0.4407 |
| haiku_20260114_canonical | claude-3-5-haiku-20241022 | 0.3142 | 0.9325 | +0.6183 |
| haiku_20260119_canonical | claude-3-5-haiku-20241022 | 0.3097 | 0.9311 | +0.6215 |
| haiku_20260125_completed_latest | claude-haiku-4-5-20251001 | 0.6627 | 0.8598 | +0.1971 |

## Preference Distribution (Counts)
| Run | Judge Model | ref_strong | ref_slight | equal | model_slight | model_strong |
| --- | --- | ---:| ---:| ---:| ---:| ---:|
| gpt4o_mini_817 | gpt-4o-mini | 1 | 20 | 14 | 547 | 235 |
| haiku_20260114_canonical | claude-3-5-haiku-20241022 | 4 | 4 | 10 | 105 | 694 |
| haiku_20260119_canonical | claude-3-5-haiku-20241022 | 3 | 4 | 9 | 106 | 686 |
| haiku_20260125_completed_latest | claude-haiku-4-5-20251001 | 52 | 105 | 6 | 383 | 262 |

## Preference Distribution (Percent of Successful)
| Run | Judge Model | ref_strong | ref_slight | equal | model_slight | model_strong |
| --- | --- | ---:| ---:| ---:| ---:| ---:|
| gpt4o_mini_817 | gpt-4o-mini | 0.12% | 2.45% | 1.71% | 66.95% | 28.76% |
| haiku_20260114_canonical | claude-3-5-haiku-20241022 | 0.49% | 0.49% | 1.22% | 12.85% | 84.94% |
| haiku_20260119_canonical | claude-3-5-haiku-20241022 | 0.37% | 0.50% | 1.11% | 13.12% | 84.90% |
| haiku_20260125_completed_latest | claude-haiku-4-5-20251001 | 6.44% | 13.00% | 0.74% | 47.40% | 32.43% |

## Dimension Means (Ref / Model)
| Dimension | gpt4o_mini_817 ref | haiku_20260114_canonical ref | haiku_20260119_canonical ref | haiku_20260125_completed_latest ref |
| --- | ---: | ---: | ---: | ---: |
| reality | 1.4321 | 0.8017 | 0.8020 | 1.8750 |
| knowledge | 0.9217 | 0.5569 | 0.5557 | 1.4790 |
| goal | 1.5679 | 1.4419 | 1.4233 | 1.6040 |
| visibility | 0.4272 | 0.2668 | 0.2624 | 0.7401 |
| agency | 0.9670 | 0.6548 | 0.6423 | 1.8131 |
| self_reflexivity | 0.1040 | 0.0685 | 0.0644 | 0.4196 |
| boundary | 1.0208 | 0.6083 | 0.5854 | 1.3465 |

## Dimension Means (Model)
| Dimension | gpt4o_mini_817 model | haiku_20260114_canonical model | haiku_20260119_canonical model | haiku_20260125_completed_latest model |
| --- | ---: | ---: | ---: | ---: |
| reality | 1.9535 | 1.9829 | 1.9839 | 1.8800 |
| knowledge | 1.9633 | 1.9657 | 1.9715 | 1.7686 |
| goal | 1.9902 | 1.9927 | 1.9901 | 1.8589 |
| visibility | 1.8225 | 1.9204 | 1.9171 | 1.6163 |
| agency | 1.8323 | 1.8935 | 1.8849 | 1.9369 |
| self_reflexivity | 1.1224 | 1.3403 | 1.3329 | 1.3045 |
| boundary | 1.9266 | 1.9596 | 1.9554 | 1.6720 |