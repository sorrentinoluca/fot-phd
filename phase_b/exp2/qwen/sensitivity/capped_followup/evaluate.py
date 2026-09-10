#!/usr/bin/env python3
"""Evaluate and report the five-case post-hoc EXP2 Qwen capped follow-up."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import statistics
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[5]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import phase_b.final_evaluation.evaluate_frozen_predictions as frozen_evaluator  # noqa: E402
from phase_b.exp2.qwen.common import canonical_json, load_json, sha256_file  # noqa: E402
from phase_b.exp2.qwen.sensitivity.capped_followup.run import (  # noqa: E402
    CONFIG_PATH,
    FOLLOWUP_DIR,
    RECORDS_PATH,
    RESULTS_PATH,
    SOURCE_RECORDS_PATH,
    atomic_write,
    load_existing_records,
    verify_frozen_integrity,
    verify_server,
    verify_source_caps,
)

REPORT_PATH = FOLLOWUP_DIR / "REPORT.md"
SOURCE_BUDGETS = (1024, 1536, 2048, 3072)


def prediction(parsed: dict[str, Any]) -> str | None:
    return None if parsed.get("abstain") else parsed.get("predicted_label")


def _stats(values: list[float | int]) -> dict[str, float | int | None]:
    if not values:
        return {"min": None, "mean": None, "median": None, "max": None}
    return {
        "min": min(values),
        "mean": statistics.fmean(values),
        "median": statistics.median(values),
        "max": max(values),
    }


def load_source_trajectories(
    config: dict[str, Any], case_truth: dict[str, str]
) -> list[dict[str, Any]]:
    target_order = [tuple(value) for value in config["target_pairs"]]
    source_rows = [
        json.loads(line)
        for line in SOURCE_RECORDS_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    lookup: dict[tuple[int, str, str], dict[str, Any]] = {}
    for row in source_rows:
        key_pair = (row.get("agent_id"), row.get("physical_case_id"))
        budget = row.get("thinking_token_budget")
        if key_pair not in set(target_order) or budget not in SOURCE_BUDGETS:
            continue
        key = (budget, *key_pair)
        if key in lookup:
            raise RuntimeError(f"duplicate source trajectory row: {key}")
        lookup[key] = row
    expected_count = len(target_order) * len(SOURCE_BUDGETS)
    if len(lookup) != expected_count:
        raise RuntimeError(f"source trajectories are incomplete: {len(lookup)}/{expected_count}")

    followup = load_existing_records(RECORDS_PATH, config)
    if len(followup) != 5:
        raise RuntimeError(f"follow-up records are incomplete: {len(followup)}/5")
    trajectories: list[dict[str, Any]] = []
    for agent_id, case_id in target_order:
        truth = case_truth[case_id]
        item: dict[str, Any] = {
            "agent_id": agent_id,
            "physical_case_id": case_id,
            "truth": truth,
            "budgets": {},
        }
        for budget in SOURCE_BUDGETS:
            row = lookup[(budget, agent_id, case_id)]
            value = prediction(row["parsed_final_output"])
            item["budgets"][str(budget)] = {
                "prediction": value,
                "correct": value == truth,
                "reasoning_tokens": row["reasoning_tokens"],
                "cap_reached": row["cap_reached"],
                "finish_reason": row["finish_reason"],
            }
        current = followup[(agent_id, case_id, "B", 4096, 1)]
        value = prediction(current["parsed_final_output"])
        item["budgets"]["4096"] = {
            "prediction": value,
            "correct": value == truth,
            "reasoning_tokens": current["reasoning_tokens"],
            "cap_reached": current["cap_reached"],
            "finish_reason": current["finish_reason"],
        }
        prior = item["budgets"]["3072"]
        latest = item["budgets"]["4096"]
        item["error_at_3072_corrected"] = not prior["correct"] and latest["correct"]
        item["error_at_3072_persistent"] = not prior["correct"] and not latest["correct"]
        item["regression_from_3072"] = prior["correct"] and not latest["correct"]
        item["terminated_below_4096_cap"] = not latest["cap_reached"]
        if latest["cap_reached"] and latest["correct"]:
            interpretation = (
                "correct while still capped; additional evidence that reaching the cap does not imply error"
            )
        elif latest["cap_reached"]:
            interpretation = "still capped at 4096; mechanism remains inconclusive"
        elif not prior["correct"] and latest["correct"]:
            interpretation = "3072 error corrected below the new cap; compatible with reasoning truncation"
        elif not prior["correct"] and not latest["correct"]:
            interpretation = (
                "3072 error persists below the new cap; interference or negative transfer is more plausible, without causal attribution"
            )
        elif prior["correct"] and not latest["correct"]:
            interpretation = "regression; greater reasoning budget is not monotonically beneficial"
        else:
            interpretation = "correct and terminated below the new cap"
        item["interpretation"] = interpretation
        trajectories.append(item)
    return trajectories


def build_results(
    server: dict[str, Any], context_check: dict[str, Any] | None = None
) -> dict[str, Any]:
    config = load_json(CONFIG_PATH)
    frozen_hashes = verify_frozen_integrity(config)
    verify_source_caps(config)
    protocol = load_json(frozen_evaluator.CONFIG_PATH)
    case_truth, truth_provenance = frozen_evaluator.load_case_truth(protocol)
    trajectories = load_source_trajectories(config, case_truth)
    records = list(load_existing_records(RECORDS_PATH, config).values())
    if len(records) != 5:
        raise RuntimeError("follow-up evaluation requires exactly five records")
    if Counter((row["condition"], row["repetition"], row["thinking_token_budget"]) for row in records) != Counter({("B", 1, 4096): 5}):
        raise RuntimeError("follow-up record scope differs from B / R=1 / budget 4096")
    below = [item for item in trajectories if item["terminated_below_4096_cap"]]
    corrected = [item for item in trajectories if item["error_at_3072_corrected"]]
    persistent = [item for item in trajectories if item["error_at_3072_persistent"]]
    capped_incorrect = [
        item
        for item in trajectories
        if item["budgets"]["4096"]["cap_reached"] and not item["budgets"]["4096"]["correct"]
    ]
    capped_correct = [
        item
        for item in trajectories
        if item["budgets"]["4096"]["cap_reached"] and item["budgets"]["4096"]["correct"]
    ]
    regressions = [item for item in trajectories if item["regression_from_3072"]]
    result = {
        "artifact_version": "1",
        "experiment": "EXP2_QWEN_REASONING_CAP_CAPPED_FOLLOWUP",
        "design": "diagnostic_post_hoc_subset_selected_for_cap_at_3072_not_global_accuracy_estimate",
        "selection": {
            "basis": config["selection_basis"],
            "target_pairs": config["target_pairs"],
            "selected_count": 5,
            "source_budget": 3072,
            "source_cap_verification": "PASS",
        },
        "condition": "B",
        "repetitions": 1,
        "thinking_token_budget": 4096,
        "max_tokens": 4608,
        "temperature": config["temperature"],
        "seed": config["seed"],
        "stateless": True,
        "server": server,
        "context_check": context_check or {},
        "truth_provenance": truth_provenance,
        "integrity": {
            "status": "PASS",
            "frozen_artifact_count": len(frozen_hashes),
            "source_sensitivity_records_sha256": sha256_file(SOURCE_RECORDS_PATH),
        },
        "trajectories": trajectories,
        "diagnostic_counts": {
            "selected_cases": 5,
            "terminated_below_4096_cap": len(below),
            "still_capped_at_4096": 5 - len(below),
            "errors_at_3072_corrected": len(corrected),
            "errors_at_3072_persistent": len(persistent),
            "incorrect_and_still_capped_at_4096_inconclusive": len(capped_incorrect),
            "correct_and_still_capped_at_4096": len(capped_correct),
            "regressions_from_3072": len(regressions),
            "parse_failures": sum(bool(row["parse_failure"]) for row in records),
        },
        "case_lists": {
            "terminated_below_4096_cap": [[item["agent_id"], item["physical_case_id"]] for item in below],
            "errors_at_3072_corrected": [[item["agent_id"], item["physical_case_id"]] for item in corrected],
            "errors_at_3072_persistent": [[item["agent_id"], item["physical_case_id"]] for item in persistent],
            "incorrect_and_still_capped_at_4096_inconclusive": [[item["agent_id"], item["physical_case_id"]] for item in capped_incorrect],
            "correct_and_still_capped_at_4096": [[item["agent_id"], item["physical_case_id"]] for item in capped_correct],
            "regressions_from_3072": [[item["agent_id"], item["physical_case_id"]] for item in regressions],
        },
        "reasoning_tokens_4096": _stats([row["reasoning_tokens"] for row in records]),
        "completion_tokens_4096": _stats([row["completion_tokens"] for row in records]),
        "latency_seconds_4096": _stats([row["latency_seconds"] for row in records]),
        "finish_reasons_4096": dict(Counter(row["finish_reason"] for row in records)),
        "server_fingerprints": sorted({row["server_fingerprint_sha256"] for row in records}),
        "records_file_sha256": sha256_file(RECORDS_PATH),
    }
    projection = "".join(
        canonical_json(row) + "\n"
        for row in sorted(records, key=lambda value: value["followup_sequence_index"])
    )
    result["records_projection_sha256"] = hashlib.sha256(projection.encode("utf-8")).hexdigest()
    return result


def _display_prediction(value: str | None) -> str:
    return "ABSTAIN" if value is None else value


def render_report(results: dict[str, Any]) -> str:
    counts = results["diagnostic_counts"]
    lines = [
        "# EXP2 Qwen capped-at-3072 diagnostic follow-up",
        "",
        "This is a post-hoc diagnostic analysis of five condition-B, repetition-1 agent-case observations selected because they were the complete set with `cap_reached=true` at reasoning budget 3072. It is not a new estimate of overall accuracy at budget 4096.",
        "",
        "## Protocol and integrity",
        "",
        f"- Source cap-set verification: `{results['selection']['source_cap_verification']}` (exactly {results['selection']['selected_count']} declared pairs).",
        f"- Frozen-artifact integrity: `{results['integrity']['status']}` ({results['integrity']['frozen_artifact_count']} files checked).",
        f"- Inference: condition B, R=1, temperature={results['temperature']}, seed={results['seed']}, stateless single-message requests, reasoning budget={results['thinking_token_budget']}, max_tokens={results['max_tokens']}.",
        f"- Server: `{results['server']['model_root']}` revision `{results['server']['model_revision']}`, vLLM `{results['server']['vllm_version']}`, reasoning parser `qwen3`, max_model_len={results['server']['max_model_len']}, physical GPU {results['server']['cuda_visible_devices']}.",
        f"- Context fit: `{results['context_check'].get('status', 'UNKNOWN')}`; maximum request prompt={results['context_check'].get('maximum_prompt_tokens_request', 'n/a')} tokens and maximum prompt+max_tokens={results['context_check'].get('maximum_required_context', 'n/a')}.",
        "",
        "## Per-case trajectories",
        "",
        "Each cell is `prediction (reasoning tokens; cap status)`. Correct predictions are marked ✓ and errors ✗.",
        "",
        "| Agent | Case | Truth | 1024 | 1536 | 2048 | 3072 | 4096 | Diagnostic reading |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for item in results["trajectories"]:
        cells: list[str] = []
        for budget in (*SOURCE_BUDGETS, 4096):
            value = item["budgets"][str(budget)]
            cells.append(
                f"{_display_prediction(value['prediction'])} ({value['reasoning_tokens']}; "
                f"{'cap' if value['cap_reached'] else 'below'}; {'✓' if value['correct'] else '✗'})"
            )
        lines.append(
            f"| {item['agent_id']} | {item['physical_case_id']} | {item['truth']} | "
            + " | ".join(cells)
            + f" | {item['interpretation']} |"
        )
    lines.extend(
        [
            "",
            "## Diagnostic summary",
            "",
            f"- Terminated below the 4096 reasoning cap: {counts['terminated_below_4096_cap']}/5; still capped: {counts['still_capped_at_4096']}/5.",
            f"- Errors present at 3072 and corrected at 4096: {counts['errors_at_3072_corrected']}.",
            f"- Errors present at 3072 and still incorrect at 4096: {counts['errors_at_3072_persistent']}.",
            f"- Incorrect and still capped at 4096, hence mechanistically inconclusive: {counts['incorrect_and_still_capped_at_4096_inconclusive']}.",
            f"- Correct while still capped at 4096: {counts['correct_and_still_capped_at_4096']}; such a case is further evidence that reaching a cap does not automatically imply error.",
            f"- Regressions relative to 3072: {counts['regressions_from_3072']}; any regression shows that greater reasoning budget is not monotonically beneficial.",
            "",
            "An error corrected and terminated below the new limit is compatible with reasoning truncation. An error that persists but terminates below the limit makes interference or negative transfer more plausible, without establishing causality. An error still at the new limit remains inconclusive.",
            "",
            "## Methodological limits",
            "",
            "The subset was selected after observing cap status at 3072, so selection is outcome-dependent and cannot support an overall 4096-budget accuracy claim. R=1 with deterministic settings checks this fixed execution path but does not estimate stochastic variability. The comparison is diagnostic and observational: changes across budgets cannot by themselves identify a causal mechanism.",
            "",
        ]
    )
    return "\n".join(lines)


def evaluate_and_write(
    server: dict[str, Any] | None = None,
    context_check: dict[str, Any] | None = None,
) -> dict[str, Any]:
    config = load_json(CONFIG_PATH)
    server = server or verify_server(config["base_url"], config)
    results = build_results(server, context_check)
    atomic_write(RESULTS_PATH, (canonical_json(results) + "\n").encode("utf-8"))
    atomic_write(REPORT_PATH, render_report(results).encode("utf-8"))
    return results


def main() -> int:
    results = evaluate_and_write()
    print(
        canonical_json(
            {
                "status": "COMPLETE",
                "selected_cases": results["diagnostic_counts"]["selected_cases"],
                "terminated_below_cap": results["diagnostic_counts"]["terminated_below_4096_cap"],
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
