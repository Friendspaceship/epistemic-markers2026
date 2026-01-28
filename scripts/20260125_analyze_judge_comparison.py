#!/usr/bin/env python3
"""
Phase 2C Anchor-5 judge comparison.

Compares two Anchor-5 evaluation JSONL files by RowIndex and reports:
- Coverage and overlap
- Preference agreement (exact and grouped)
- Behavior tag agreement
- Dimension-level agreement and mean absolute differences
- AI/CS agreement and correlations
"""

import argparse
import json
import statistics
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

DIMENSIONS = [
    "reality",
    "knowledge",
    "goal",
    "visibility",
    "agency",
    "self_reflexivity",
    "boundary",
]

PREFERENCE_GROUPS = {
    1: "ref",
    2: "ref",
    3: "equal",
    4: "model",
    5: "model",
}


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
    return records


def as_int(value: Any) -> Optional[int]:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def pick_latest(existing: Dict[str, Any], candidate: Dict[str, Any]) -> Dict[str, Any]:
    ts_existing = existing.get("timestamp")
    ts_candidate = candidate.get("timestamp")
    if not ts_existing or not ts_candidate:
        return candidate
    return candidate if ts_candidate > ts_existing else existing


def index_records(records: Iterable[Dict[str, Any]]) -> Tuple[Dict[int, Dict[str, Any]], int, int]:
    indexed: Dict[int, Dict[str, Any]] = {}
    total = 0
    success = 0
    for record in records:
        total += 1
        row_index = as_int(record.get("RowIndex"))
        if row_index is None:
            continue
        if record.get("success", True) is not True:
            continue
        success += 1
        if row_index in indexed:
            indexed[row_index] = pick_latest(indexed[row_index], record)
        else:
            indexed[row_index] = record
    return indexed, total, success


def safe_float(value: Any) -> Optional[float]:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def extract_scores(record: Dict[str, Any]) -> Tuple[Dict[str, float], Dict[str, float]]:
    ref_scores: Dict[str, float] = {}
    model_scores: Dict[str, float] = {}
    for dim in DIMENSIONS:
        ref_val = safe_float(record.get(f"{dim}_ref"))
        model_val = safe_float(record.get(f"{dim}_model"))
        if ref_val is not None:
            ref_scores[dim] = ref_val
        if model_val is not None:
            model_scores[dim] = model_val
    return ref_scores, model_scores


def compute_ai_cs(ref_scores: Dict[str, float], model_scores: Dict[str, float]) -> Optional[Tuple[float, float, float]]:
    if len(ref_scores) != len(DIMENSIONS) or len(model_scores) != len(DIMENSIONS):
        return None
    ref_total = sum(ref_scores.values())
    model_total = sum(model_scores.values())
    ref_ai = ref_total / 14.0
    model_ai = model_total / 14.0
    cs = model_ai - ref_ai
    return ref_ai, model_ai, cs


def preference_group(pref: Optional[int]) -> Optional[str]:
    if pref is None:
        return None
    return PREFERENCE_GROUPS.get(pref)


def pearson(xs: List[float], ys: List[float]) -> Optional[float]:
    if len(xs) < 2 or len(xs) != len(ys):
        return None
    mean_x = statistics.mean(xs)
    mean_y = statistics.mean(ys)
    cov = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys)) / (len(xs) - 1)
    stdev_x = statistics.stdev(xs)
    stdev_y = statistics.stdev(ys)
    if stdev_x == 0 or stdev_y == 0:
        return None
    return cov / (stdev_x * stdev_y)


def mean(values: List[float]) -> Optional[float]:
    return statistics.mean(values) if values else None


def mean_abs_diff(values_a: List[float], values_b: List[float]) -> Optional[float]:
    if not values_a or not values_b or len(values_a) != len(values_b):
        return None
    diffs = [abs(a - b) for a, b in zip(values_a, values_b)]
    return statistics.mean(diffs) if diffs else None


def exact_match_rate(values_a: List[Any], values_b: List[Any]) -> Optional[float]:
    if not values_a or not values_b or len(values_a) != len(values_b):
        return None
    matches = sum(1 for a, b in zip(values_a, values_b) if a == b)
    return matches / len(values_a)


def get_judge_model(records: Iterable[Dict[str, Any]]) -> Optional[str]:
    for record in records:
        if record.get("success", True) is True and record.get("judge_model"):
            return record.get("judge_model")
    return None


def format_pct(value: Optional[float]) -> str:
    if value is None:
        return "n/a"
    return f"{value * 100:.1f}%"


def compare_judges(judge_a_path: Path, judge_b_path: Path) -> Dict[str, Any]:
    records_a = load_jsonl(judge_a_path)
    records_b = load_jsonl(judge_b_path)

    judge_a_model = get_judge_model(records_a)
    judge_b_model = get_judge_model(records_b)

    index_a, total_a, success_a = index_records(records_a)
    index_b, total_b, success_b = index_records(records_b)

    overlap = sorted(set(index_a.keys()) & set(index_b.keys()))
    missing_in_a = sorted(set(index_b.keys()) - set(index_a.keys()))
    missing_in_b = sorted(set(index_a.keys()) - set(index_b.keys()))

    pref_a: List[int] = []
    pref_b: List[int] = []
    pref_group_a: List[str] = []
    pref_group_b: List[str] = []

    tag_ref_a: List[str] = []
    tag_ref_b: List[str] = []
    tag_model_a: List[str] = []
    tag_model_b: List[str] = []

    ref_ai_a: List[float] = []
    ref_ai_b: List[float] = []
    model_ai_a: List[float] = []
    model_ai_b: List[float] = []
    cs_a: List[float] = []
    cs_b: List[float] = []

    pref_counts_a: Counter = Counter()
    pref_counts_b: Counter = Counter()
    tag_ref_counts_a: Counter = Counter()
    tag_ref_counts_b: Counter = Counter()
    tag_model_counts_a: Counter = Counter()
    tag_model_counts_b: Counter = Counter()

    dim_ref_a: Dict[str, List[float]] = {dim: [] for dim in DIMENSIONS}
    dim_ref_b: Dict[str, List[float]] = {dim: [] for dim in DIMENSIONS}
    dim_model_a: Dict[str, List[float]] = {dim: [] for dim in DIMENSIONS}
    dim_model_b: Dict[str, List[float]] = {dim: [] for dim in DIMENSIONS}

    for row_index in overlap:
        rec_a = index_a[row_index]
        rec_b = index_b[row_index]

        pref_val_a = as_int(rec_a.get("preference"))
        pref_val_b = as_int(rec_b.get("preference"))
        if pref_val_a is not None and pref_val_b is not None:
            pref_a.append(pref_val_a)
            pref_b.append(pref_val_b)
            pref_counts_a[pref_val_a] += 1
            pref_counts_b[pref_val_b] += 1

            group_a = preference_group(pref_val_a)
            group_b = preference_group(pref_val_b)
            if group_a and group_b:
                pref_group_a.append(group_a)
                pref_group_b.append(group_b)

        tag_ref_val_a = rec_a.get("tag_ref")
        tag_ref_val_b = rec_b.get("tag_ref")
        if tag_ref_val_a and tag_ref_val_b:
            tag_ref_a.append(tag_ref_val_a)
            tag_ref_b.append(tag_ref_val_b)
            tag_ref_counts_a[tag_ref_val_a] += 1
            tag_ref_counts_b[tag_ref_val_b] += 1

        tag_model_val_a = rec_a.get("tag_model")
        tag_model_val_b = rec_b.get("tag_model")
        if tag_model_val_a and tag_model_val_b:
            tag_model_a.append(tag_model_val_a)
            tag_model_b.append(tag_model_val_b)
            tag_model_counts_a[tag_model_val_a] += 1
            tag_model_counts_b[tag_model_val_b] += 1

        ref_scores_a, model_scores_a = extract_scores(rec_a)
        ref_scores_b, model_scores_b = extract_scores(rec_b)

        for dim in DIMENSIONS:
            if dim in ref_scores_a and dim in ref_scores_b:
                dim_ref_a[dim].append(ref_scores_a[dim])
                dim_ref_b[dim].append(ref_scores_b[dim])
            if dim in model_scores_a and dim in model_scores_b:
                dim_model_a[dim].append(model_scores_a[dim])
                dim_model_b[dim].append(model_scores_b[dim])

        ai_cs_a = compute_ai_cs(ref_scores_a, model_scores_a)
        ai_cs_b = compute_ai_cs(ref_scores_b, model_scores_b)
        if ai_cs_a and ai_cs_b:
            ref_ai_a.append(ai_cs_a[0])
            model_ai_a.append(ai_cs_a[1])
            cs_a.append(ai_cs_a[2])
            ref_ai_b.append(ai_cs_b[0])
            model_ai_b.append(ai_cs_b[1])
            cs_b.append(ai_cs_b[2])

    dimension_summary: Dict[str, Dict[str, Any]] = {}
    for dim in DIMENSIONS:
        ref_a_vals = dim_ref_a[dim]
        ref_b_vals = dim_ref_b[dim]
        model_a_vals = dim_model_a[dim]
        model_b_vals = dim_model_b[dim]
        dimension_summary[dim] = {
            "ref": {
                "mean_a": mean(ref_a_vals),
                "mean_b": mean(ref_b_vals),
                "mean_abs_diff": mean_abs_diff(ref_a_vals, ref_b_vals),
                "exact_match_rate": exact_match_rate(ref_a_vals, ref_b_vals),
                "count": len(ref_a_vals),
            },
            "model": {
                "mean_a": mean(model_a_vals),
                "mean_b": mean(model_b_vals),
                "mean_abs_diff": mean_abs_diff(model_a_vals, model_b_vals),
                "exact_match_rate": exact_match_rate(model_a_vals, model_b_vals),
                "count": len(model_a_vals),
            },
        }

    preference_summary = {
        "exact_match_rate": exact_match_rate(pref_a, pref_b),
        "group_match_rate": exact_match_rate(pref_group_a, pref_group_b),
        "mean_abs_diff": mean_abs_diff(pref_a, pref_b),
        "correlation": pearson(pref_a, pref_b),
        "distribution_a": dict(pref_counts_a),
        "distribution_b": dict(pref_counts_b),
        "count": len(pref_a),
    }

    behavior_summary = {
        "ref": {
            "match_rate": exact_match_rate(tag_ref_a, tag_ref_b),
            "distribution_a": dict(tag_ref_counts_a),
            "distribution_b": dict(tag_ref_counts_b),
            "count": len(tag_ref_a),
        },
        "model": {
            "match_rate": exact_match_rate(tag_model_a, tag_model_b),
            "distribution_a": dict(tag_model_counts_a),
            "distribution_b": dict(tag_model_counts_b),
            "count": len(tag_model_a),
        },
    }

    ai_cs_summary = {
        "ref_ai": {
            "mean_a": mean(ref_ai_a),
            "mean_b": mean(ref_ai_b),
            "mean_abs_diff": mean_abs_diff(ref_ai_a, ref_ai_b),
            "correlation": pearson(ref_ai_a, ref_ai_b),
            "count": len(ref_ai_a),
        },
        "model_ai": {
            "mean_a": mean(model_ai_a),
            "mean_b": mean(model_ai_b),
            "mean_abs_diff": mean_abs_diff(model_ai_a, model_ai_b),
            "correlation": pearson(model_ai_a, model_ai_b),
            "count": len(model_ai_a),
        },
        "cs": {
            "mean_a": mean(cs_a),
            "mean_b": mean(cs_b),
            "mean_abs_diff": mean_abs_diff(cs_a, cs_b),
            "correlation": pearson(cs_a, cs_b),
            "count": len(cs_a),
        },
    }

    return {
        "metadata": {
            "generated_at_utc": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
            "judge_a_file": str(judge_a_path),
            "judge_b_file": str(judge_b_path),
            "judge_a_model": judge_a_model,
            "judge_b_model": judge_b_model,
            "protocol": "Anchor-5",
            "comparison": "Phase 2C judge agreement",
        },
        "coverage": {
            "judge_a_total_rows": total_a,
            "judge_a_success_rows": success_a,
            "judge_b_total_rows": total_b,
            "judge_b_success_rows": success_b,
            "overlap_rows": len(overlap),
            "missing_in_a": missing_in_a,
            "missing_in_b": missing_in_b,
        },
        "preference": preference_summary,
        "behavior_tags": behavior_summary,
        "dimensions": dimension_summary,
        "ai_cs": ai_cs_summary,
    }


def build_report(summary: Dict[str, Any]) -> str:
    meta = summary["metadata"]
    coverage = summary["coverage"]
    preference = summary["preference"]
    behavior = summary["behavior_tags"]
    dimensions = summary["dimensions"]
    ai_cs = summary["ai_cs"]

    lines: List[str] = []
    lines.append("# Phase 2C Judge Comparison Report")
    lines.append("")
    lines.append(f"Generated: {meta['generated_at_utc']}")
    lines.append(f"Judge A: {meta.get('judge_a_model') or 'n/a'}")
    lines.append(f"Judge B: {meta.get('judge_b_model') or 'n/a'}")
    lines.append("")
    lines.append("## Coverage")
    lines.append(f"- Judge A total rows: {coverage['judge_a_total_rows']}")
    lines.append(f"- Judge A success rows: {coverage['judge_a_success_rows']}")
    lines.append(f"- Judge B total rows: {coverage['judge_b_total_rows']}")
    lines.append(f"- Judge B success rows: {coverage['judge_b_success_rows']}")
    lines.append(f"- Overlap rows: {coverage['overlap_rows']}")
    lines.append(f"- Missing in A: {len(coverage['missing_in_a'])}")
    lines.append(f"- Missing in B: {len(coverage['missing_in_b'])}")
    lines.append("")
    lines.append("## Preference Agreement")
    lines.append(f"- Exact match rate: {format_pct(preference.get('exact_match_rate'))}")
    lines.append(f"- Grouped match rate: {format_pct(preference.get('group_match_rate'))}")
    lines.append(f"- Mean absolute diff: {preference.get('mean_abs_diff')}")
    lines.append(f"- Correlation: {preference.get('correlation')}")
    lines.append(f"- Count: {preference.get('count')}")
    lines.append("")
    lines.append("## Behavior Tag Agreement")
    lines.append(f"- Ref tag match rate: {format_pct(behavior['ref'].get('match_rate'))}")
    lines.append(f"- Ref tag count: {behavior['ref'].get('count')}")
    lines.append(f"- Model tag match rate: {format_pct(behavior['model'].get('match_rate'))}")
    lines.append(f"- Model tag count: {behavior['model'].get('count')}")
    lines.append("")
    lines.append("## AI/CS Agreement")
    lines.append("| Metric | Mean A | Mean B | Mean Abs Diff | Correlation | Count |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for metric_key in ["ref_ai", "model_ai", "cs"]:
        metric = ai_cs[metric_key]
        lines.append(
            f"| {metric_key} | {metric.get('mean_a')} | {metric.get('mean_b')} "
            f"| {metric.get('mean_abs_diff')} | {metric.get('correlation')} | {metric.get('count')} |"
        )
    lines.append("")
    lines.append("## Dimension Agreement")
    lines.append("| Dimension | Ref mean A | Ref mean B | Ref mean abs diff | Ref match rate | Model mean A | Model mean B | Model mean abs diff | Model match rate |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for dim in DIMENSIONS:
        ref = dimensions[dim]["ref"]
        model = dimensions[dim]["model"]
        lines.append(
            f"| {dim} | {ref.get('mean_a')} | {ref.get('mean_b')} | {ref.get('mean_abs_diff')} | {format_pct(ref.get('exact_match_rate'))} "
            f"| {model.get('mean_a')} | {model.get('mean_b')} | {model.get('mean_abs_diff')} | {format_pct(model.get('exact_match_rate'))} |"
        )
    lines.append("")
    lines.append("## Inputs")
    lines.append(f"- Judge A file: {meta['judge_a_file']}")
    lines.append(f"- Judge B file: {meta['judge_b_file']}")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Phase 2C Anchor-5 judge comparison.")
    parser.add_argument("--judge-a", required=True, help="Path to judge A JSONL file.")
    parser.add_argument("--judge-b", required=True, help="Path to judge B JSONL file.")
    parser.add_argument(
        "--output-prefix",
        required=True,
        help="Output prefix for summary/report files (without extension).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    judge_a_path = Path(args.judge_a).resolve()
    judge_b_path = Path(args.judge_b).resolve()
    output_prefix = Path(args.output_prefix)

    summary = compare_judges(judge_a_path, judge_b_path)
    report = build_report(summary)

    summary_path = output_prefix.parent / f"{output_prefix.name}_summary.json"
    report_path = output_prefix.parent / f"{output_prefix.name}_report.md"

    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    report_path.write_text(report, encoding="utf-8")

    print(f"Wrote summary: {summary_path}")
    print(f"Wrote report: {report_path}")


if __name__ == "__main__":
    main()
