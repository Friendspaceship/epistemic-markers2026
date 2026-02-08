# Phase 2C Judge Comparison Report

Generated: 2026-01-25 14:28:42 UTC
Judge A: gpt-4o-mini
Judge B: claude-3-5-haiku-20241022

## Coverage
- Judge A total rows: 817
- Judge A success rows: 817
- Judge B total rows: 817
- Judge B success rows: 817
- Overlap rows: 817
- Missing in A: 0
- Missing in B: 0

## Preference Agreement
- Exact match rate: 39.5%
- Grouped match rate: 95.7%
- Mean absolute diff: 0.6438188494492044
- Correlation: 0.3786252390672225
- Count: 817

## Behavior Tag Agreement
- Ref tag match rate: 91.3%
- Ref tag count: 816
- Model tag match rate: 72.5%
- Model tag count: 816

## AI/CS Agreement
| Metric | Mean A | Mean B | Mean Abs Diff | Correlation | Count |
| --- | --- | --- | --- | --- | --- |
| ref_ai | 0.4600454624934429 | 0.3142157719881098 | 0.20160867284490294 | 0.5622054467618874 | 817 |
| model_ai | 0.9007693652736493 | 0.9325056828116803 | 0.05411785277146355 | 0.4235331987417537 | 817 |
| cs | 0.44072390278020634 | 0.6182899108235705 | 0.23229585591886695 | 0.5746736156844295 | 817 |

## Dimension Agreement
| Dimension | Ref mean A | Ref mean B | Ref mean abs diff | Ref match rate | Model mean A | Model mean B | Model mean abs diff | Model match rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| reality | 1.4320685434516525 | 0.8017135862913096 | 0.7086903304773562 | 38.8% | 1.9534883720930232 | 1.9828641370869033 | 0.04895960832313342 | 95.3% |
| knowledge | 0.9216646266829865 | 0.5569155446756426 | 0.46511627906976744 | 58.0% | 1.96328029375765 | 1.9657282741738067 | 0.046511627906976744 | 95.5% |
| goal | 1.5679314565483475 | 1.441860465116279 | 0.3292533659730722 | 69.0% | 1.9902080783353733 | 1.99265605875153 | 0.012239902080783354 | 98.8% |
| visibility | 0.42717258261933905 | 0.2668298653610771 | 0.3733170134638923 | 68.5% | 1.8225214198286415 | 1.9204406364749083 | 0.16401468788249693 | 83.6% |
| agency | 0.966952264381885 | 0.6548347613219094 | 0.5716034271725826 | 49.8% | 1.832313341493268 | 1.8935128518971849 | 0.19583843329253367 | 81.3% |
| self_reflexivity | 0.10403916768665851 | 0.06854345165238677 | 0.0966952264381885 | 90.9% | 1.1223990208078336 | 1.3402692778457772 | 0.25703794369645044 | 74.3% |
| boundary | 1.0208078335373316 | 0.6083231334149327 | 0.5201958384332925 | 52.1% | 1.9265605875152998 | 1.959608323133415 | 0.08445532435740515 | 91.8% |

## Inputs
- Judge A file: <local-project-root>/CPTRed-2026/data/evaluated/gpt4o_mini_anchor5_817_full_20260106_001318.jsonl
- Judge B file: <local-project-root>/CPTRed-2026/data/evaluated/claude_haiku_anchor5_817_canonical_working_fixed20260114.jsonl