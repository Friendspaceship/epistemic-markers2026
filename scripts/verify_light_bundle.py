#!/usr/bin/env python3
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def require_any(rel_paths: list[str]) -> str:
    for rel_path in rel_paths:
        path = ROOT / rel_path
        if path.exists():
            return rel_path
    raise FileNotFoundError(" or ".join(rel_paths))


def load_json(rel_path: str) -> dict:
    path = ROOT / rel_path
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def require_exists(rel_path: str) -> None:
    path = ROOT / rel_path
    if not path.exists():
        raise FileNotFoundError(rel_path)


def fmt(x) -> str:
    if isinstance(x, float):
        return f"{x:.6f}"
    return str(x)


def main() -> None:
    required_files = [
        require_any(
            [
                "manuscript/20260208 Judge-Mediated Mapping of Epistemic Structures in TruthfulQA An Exploratory Study with the CPT Anchor-5 Protocol v15.md",
                "manuscript/20260128 Measuring Textual Markers of Epistemic Stance v4.md",
            ]
        ),
        require_any(
            [
                "20260106_REPLICATION_GUIDELINES.md",
                "REPLICATION_GUIDELINES.md",
            ]
        ),
        "additional/20260106_anchor5_analysis_results.json",
        "data/evaluated/20260114_anchor5_analysis_summary.md",
        "data/evaluated/20260114_anchor5_analysis_results.json",
        "data/evaluated/20260119_haiku_replication_run/20260119_anchor5_analysis_summary.md",
        "data/evaluated/20260119_haiku_replication_run/20260119_anchor5_analysis_results.json",
        "data/evaluated/20260119_haiku_replication_run/20260120_anchor5_analysis_comparison_report.md",
        "data/evaluated/phase2c/20260125_gpt4o_mini_vs_haiku_report.md",
        "data/evaluated/phase2c/20260125_all_4_runs_table_overview.md",
        "data/evaluated/phase2c/20260125_gpt4o_mini_vs_haiku_summary.json",
        "data/evaluated/20260123_Haiku_4_5/20260125_Haiku_4_5_completed_latest_merged_summary.json",
        "data/evaluated/20260123_Haiku_4_5/20260125_all_817_runs_table_overview.md",
    ]

    for rel in required_files:
        require_exists(rel)

    gpt = load_json("additional/20260106_anchor5_analysis_results.json")
    haiku = load_json("data/evaluated/20260114_anchor5_analysis_results.json")
    haiku_rep = load_json(
        "data/evaluated/20260119_haiku_replication_run/20260119_anchor5_analysis_results.json"
    )
    judge_cmp = load_json("data/evaluated/phase2c/20260125_gpt4o_mini_vs_haiku_summary.json")
    haiku45 = load_json(
        "data/evaluated/20260123_Haiku_4_5/20260125_Haiku_4_5_completed_latest_merged_summary.json"
    )

    print("OK: all expected files present")

    print("\n== GPT-4o-mini run (Phase 2A aggregate) ==")
    print("ref_ai.mean:", fmt(gpt["metrics"]["ref_ai"]["mean"]))
    print("model_ai.mean:", fmt(gpt["metrics"]["model_ai"]["mean"]))
    print("cs.mean:", fmt(gpt["metrics"]["cs"]["mean"]))
    print("model_preferred_pct:", fmt(gpt["preference_distribution"]["model_preferred_pct"]))

    print("\n== Claude Haiku 3.5 run (Phase 2B aggregate) ==")
    print("ref_ai.mean:", fmt(haiku["metrics"]["ref_ai"]["mean"]))
    print("model_ai.mean:", fmt(haiku["metrics"]["model_ai"]["mean"]))
    print("cs.mean:", fmt(haiku["metrics"]["cs"]["mean"]))
    print("model_preferred_pct:", fmt(haiku["preference_distribution"]["model_preferred_pct"]))

    print("\n== Haiku 3.5 replication (20260119 aggregate) ==")
    print("successful:", haiku_rep["metadata"]["successful"])
    print("ref_ai.mean:", fmt(haiku_rep["metrics"]["ref_ai"]["mean"]))
    print("model_ai.mean:", fmt(haiku_rep["metrics"]["model_ai"]["mean"]))
    print("cs.mean:", fmt(haiku_rep["metrics"]["cs"]["mean"]))

    print("\n== Haiku replication deltas (20260119 - 20260114) ==")
    print(
        "ref_ai.mean delta:",
        fmt(haiku_rep["metrics"]["ref_ai"]["mean"] - haiku["metrics"]["ref_ai"]["mean"]),
    )
    print(
        "model_ai.mean delta:",
        fmt(haiku_rep["metrics"]["model_ai"]["mean"] - haiku["metrics"]["model_ai"]["mean"]),
    )
    print("cs.mean delta:", fmt(haiku_rep["metrics"]["cs"]["mean"] - haiku["metrics"]["cs"]["mean"]))

    print("\n== Judge comparison (GPT-4o-mini vs Haiku 3.5 aggregate) ==")
    print("group_match_rate:", fmt(judge_cmp["preference"]["group_match_rate"]))
    print("exact_match_rate:", fmt(judge_cmp["preference"]["exact_match_rate"]))
    print("cs.mean_a (GPT-4o-mini):", fmt(judge_cmp["ai_cs"]["cs"]["mean_a"]))
    print("cs.mean_b (Haiku 3.5):", fmt(judge_cmp["ai_cs"]["cs"]["mean_b"]))

    print("\n== Haiku 4.5 run (aggregate summary) ==")
    print("judge_model:", haiku45.get("judge_model"))
    print("total_records:", haiku45.get("total_records"))
    print("successful:", haiku45.get("successful"))
    print("success_rate:", fmt(haiku45.get("success_rate")))
    dims = haiku45.get("dimension_scores", {})
    # Print a stable subset
    for key in [
        "visibility_ref_avg",
        "visibility_model_avg",
        "self_reflexivity_ref_avg",
        "self_reflexivity_model_avg",
    ]:
        if key in dims:
            print(f"{key}:", fmt(dims[key]))


if __name__ == "__main__":
    main()
