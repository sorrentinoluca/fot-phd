"""Offline evaluator for the completed C06 local-seen screening."""

from __future__ import annotations

from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path
import subprocess

from .constants import C06_ROOT, INFERENCE_PAYLOAD_COMMIT, ROOT, VARIANT
from .prompt_variant import canonical_json
from .run_screening import preflight


OUTPUT_ROOT = C06_ROOT / "inference"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    preflight()
    records = [
        load_json(OUTPUT_ROOT / "records" / f"{index:04d}.json")
        for index in range(72)
    ]
    config = load_json(C06_ROOT / "evaluator_side/screening_targets.json")
    expected = config["expected_local_labels"]
    original_errors = {
        (item["agent_id"], item["physical_case_id"])
        for item in config["original_errors"]
    }
    groups = defaultdict(list)
    for record in records:
        groups[(record["agent_id"], record["physical_case_id"])].append(record)
    if len(groups) != 24:
        raise RuntimeError("screening must contain exactly 24 agent-case groups")

    baseline_raw = subprocess.run(
        ["git", "show", f"{INFERENCE_PAYLOAD_COMMIT}:inference_outputs/aggregate_records.jsonl"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    ).stdout
    baseline = {}
    for line in baseline_raw.splitlines():
        item = json.loads(line)
        key = (item["agent_id"], item["physical_case_id"])
        if item["condition"] == "B" and key in groups:
            baseline[key] = item["parsed_output"]["predicted_label"]
    if len(baseline) != 24:
        raise RuntimeError("could not join all 24 frozen B baselines")

    rows = []
    aggregates = []
    for key in sorted(groups):
        agent_id, case_id = key
        repetitions = sorted(groups[key], key=lambda item: item["repetition"])
        if [item["repetition"] for item in repetitions] != [1, 2, 3]:
            raise RuntimeError(f"invalid repetitions for {agent_id}/{case_id}")
        votes = Counter(
            item["parsed_final_output"]["predicted_label"]
            for item in repetitions
            if not item["parsed_final_output"]["abstain"]
        )
        winners = [label for label, count in votes.items() if count >= 2]
        label = winners[0] if len(winners) == 1 else None
        abstain = label is None
        correct = label == expected[agent_id]
        used = sorted(
            {
                insight
                for item in repetitions
                for insight in item["parsed_final_output"]["used_insight_ids"]
            }
        )
        rep_labels = [
            item["parsed_final_output"]["predicted_label"] or "ABSTAIN"
            for item in repetitions
        ]
        row = {
            "agent_id": agent_id,
            "physical_case_id": case_id,
            "expected_label": expected[agent_id],
            "frozen_B_label": baseline[key],
            "variant_label": label or "ABSTAIN",
            "repetitions": "/".join(rep_labels),
            "correct": correct,
            "abstain": abstain,
            "three_of_three_agreement": len(set(rep_labels)) == 1,
            "parse_failures": sum(item["parse_failure"] for item in repetitions),
            "used_insight_ids": ",".join(used),
            "original_error": key in original_errors,
        }
        rows.append(row)
        aggregates.append(
            {
                "agent_id": agent_id,
                "physical_case_id": case_id,
                "condition": VARIANT,
                "parsed_output": {
                    "predicted_label": label,
                    "abstain": abstain,
                    "used_insight_ids": used,
                    "reasoning_summary": "aggregate_majority_2_of_3" if label else "aggregate_no_label_majority",
                },
                "repetition_outcomes": [
                    {
                        "repetition": item["repetition"],
                        "predicted_label": item["parsed_final_output"]["predicted_label"],
                        "abstain": item["parsed_final_output"]["abstain"],
                        "parse_failure": item["parse_failure"],
                        "used_insight_ids": item["parsed_final_output"]["used_insight_ids"],
                    }
                    for item in repetitions
                ],
            }
        )

    recovered = sum(row["correct"] for row in rows if row["original_error"])
    new_errors = sum(not row["correct"] for row in rows if not row["original_error"])
    correct = sum(row["correct"] for row in rows)
    abstentions = sum(row["abstain"] for row in rows)
    parse_failures = sum(row["parse_failures"] for row in rows)
    agreement = sum(row["three_of_three_agreement"] for row in rows)
    gate = recovered >= 4 and new_errors == 0 and correct >= 23 and parse_failures == 0
    results = {
        "variant": VARIANT,
        "analysis_kind": "post-hoc diagnostic; not an independent replication",
        "aggregate_accuracy": correct / 24,
        "correct": correct,
        "n": 24,
        "original_errors_recovered": recovered,
        "original_errors_n": 5,
        "new_errors_in_previously_correct": new_errors,
        "previously_correct_n": 19,
        "aggregate_abstentions": abstentions,
        "parse_failures": parse_failures,
        "three_of_three_agreement": agreement,
        "forbidden_information_detected": False,
        "new_error_cases": [
            {"agent_id": row["agent_id"], "physical_case_id": row["physical_case_id"]}
            for row in rows
            if not row["original_error"] and not row["correct"]
        ],
        "gate": "PASS" if gate else "FAIL",
        "recommended_c06_status": (
            "Mitigata — correzione preliminare promettente"
            if gate
            else "Mitigata — causa identificata"
        ),
    }
    (OUTPUT_ROOT / "aggregate_records.jsonl").write_text(
        "".join(canonical_json(item) + "\n" for item in aggregates), encoding="utf-8"
    )
    (OUTPUT_ROOT / "screening_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    with (OUTPUT_ROOT / "screening_table.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    report_lines = [
        "# C06 B_LOCAL_FIRST_V1 screening",
        "",
        "> Post-hoc diagnostic analysis; this is not an independent replication.",
        "",
        f"Gate: **{results['gate']}**",
        "",
        f"- Accuracy: {correct}/24 ({100 * correct / 24:.1f}%)",
        f"- Original errors recovered: {recovered}/5",
        f"- New errors: {new_errors}/19",
        f"- Aggregate abstentions: {abstentions}",
        f"- Parse failures: {parse_failures}",
        f"- Three-of-three agreement: {agreement}/24",
        "",
        "| Agent | Case | Expected | Frozen B | Variant | Repetitions | Correct | Insights |",
        "|---|---|---|---|---|---|---:|---|",
    ]
    for row in rows:
        report_lines.append(
            f"| {row['agent_id']} | {row['physical_case_id']} | {row['expected_label']} | "
            f"{row['frozen_B_label']} | {row['variant_label']} | {row['repetitions']} | "
            f"{'yes' if row['correct'] else 'no'} | {row['used_insight_ids'] or '—'} |"
        )
    report_lines.extend(
        [
            "",
            "## Five original frozen-B errors",
            "",
            "| Agent | Case | Frozen B | Variant reps | Variant aggregate | Declared insight IDs | Recovered |",
            "|---|---|---|---|---|---|---:|",
        ]
    )
    for row in rows:
        if row["original_error"]:
            report_lines.append(
                f"| {row['agent_id']} | {row['physical_case_id']} | {row['frozen_B_label']} | "
                f"{row['repetitions']} | {row['variant_label']} | "
                f"{row['used_insight_ids'] or '—'} | {'yes' if row['correct'] else 'no'} |"
            )
    report_lines.extend(["", "## New errors among the 19 frozen-B correct cases", ""])
    new_error_rows = [
        row for row in rows if not row["original_error"] and not row["correct"]
    ]
    if new_error_rows:
        for row in new_error_rows:
            report_lines.append(
                f"- {row['agent_id']} / {row['physical_case_id']}: "
                f"{row['variant_label']} (expected {row['expected_label']})"
            )
    else:
        report_lines.append("None.")
    (OUTPUT_ROOT / "SCREENING_REPORT.md").write_text(
        "\n".join(report_lines) + "\n", encoding="utf-8"
    )
    output_files = [
        "repetition_records.jsonl",
        "aggregate_records.jsonl",
        "execution_metadata.json",
        "screening_results.json",
        "screening_table.csv",
        "SCREENING_REPORT.md",
    ]
    hashes = {
        name: hashlib.sha256((OUTPUT_ROOT / name).read_bytes()).hexdigest()
        for name in output_files
    }
    (OUTPUT_ROOT / "output_hashes.json").write_text(
        json.dumps(hashes, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
