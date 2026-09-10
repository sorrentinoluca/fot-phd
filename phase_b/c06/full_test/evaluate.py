"""Stratified evaluator for the C06 B_LOCAL_FIRST_V1 full test."""

from __future__ import annotations

from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path
import subprocess

from phase_b.c06.prompt_variant import canonical_json

from .constants import (
    FULL_TEST_ROOT,
    GATES,
    INFERENCE_PAYLOAD_COMMIT,
    PLANNED_AGENT_CASES,
    PLANNED_CALLS,
    ROOT,
    VARIANT,
    expected_label,
    stratum,
)
from .run_full_test import preflight


OUTPUT_ROOT = FULL_TEST_ROOT / "inference"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    preflight()

    records = [
        load_json(OUTPUT_ROOT / "records" / f"{index:04d}.json")
        for index in range(PLANNED_CALLS)
    ]

    # ── Load frozen-B baselines for comparison ──
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
        if item["condition"] == "B":
            baseline[(item["agent_id"], item["physical_case_id"])] = item["parsed_output"]["predicted_label"]

    # ── Group by (agent, case) and aggregate 2-of-3 ──
    groups = defaultdict(list)
    for record in records:
        groups[(record["agent_id"], record["physical_case_id"])].append(record)

    if len(groups) != PLANNED_AGENT_CASES:
        raise RuntimeError(
            f"full test must contain exactly {PLANNED_AGENT_CASES} agent-case groups, "
            f"found {len(groups)}"
        )

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

        expected = expected_label(case_id)
        correct = label == expected
        strat = stratum(agent_id, case_id)
        frozen_b = baseline.get(key)

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
            "stratum": strat,
            "expected_label": expected,
            "frozen_B_label": frozen_b,
            "variant_label": label or "ABSTAIN",
            "repetitions": "/".join(rep_labels),
            "correct": correct,
            "abstain": abstain,
            "three_of_three_agreement": len(set(rep_labels)) == 1,
            "parse_failures": sum(item["parse_failure"] for item in repetitions),
            "used_insight_ids": ",".join(used),
            "frozen_B_correct": frozen_b == expected,
            "change": (
                "IMPROVED" if correct and not (frozen_b == expected) else
                "REGRESSED" if not correct and (frozen_b == expected) else
                "SAME_CORRECT" if correct else
                "SAME_WRONG"
            ),
        }
        rows.append(row)
        aggregates.append(
            {
                "agent_id": agent_id,
                "physical_case_id": case_id,
                "condition": VARIANT,
                "stratum": strat,
                "parsed_output": {
                    "predicted_label": label,
                    "abstain": abstain,
                    "used_insight_ids": used,
                    "reasoning_summary": (
                        "aggregate_majority_2_of_3" if label
                        else "aggregate_no_label_majority"
                    ),
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

    # ── Stratified metrics ──
    strata_rows = defaultdict(list)
    for row in rows:
        strata_rows[row["stratum"]].append(row)

    strata_results = {}
    for strat_name in ("local-seen", "local-unseen", "normal"):
        srows = strata_rows[strat_name]
        n = len(srows)
        correct = sum(r["correct"] for r in srows)
        frozen_b_correct = sum(r["frozen_B_correct"] for r in srows)
        improved = sum(1 for r in srows if r["change"] == "IMPROVED")
        regressed = sum(1 for r in srows if r["change"] == "REGRESSED")
        parse_failures = sum(r["parse_failures"] for r in srows)
        abstentions = sum(r["abstain"] for r in srows)
        agreement = sum(r["three_of_three_agreement"] for r in srows)
        strata_results[strat_name] = {
            "n": n,
            "correct": correct,
            "accuracy": correct / n if n > 0 else 0.0,
            "frozen_B_correct": frozen_b_correct,
            "frozen_B_accuracy": frozen_b_correct / n if n > 0 else 0.0,
            "improved": improved,
            "regressed": regressed,
            "net_change": improved - regressed,
            "parse_failures": parse_failures,
            "abstentions": abstentions,
            "three_of_three_agreement": agreement,
        }

    # ── Gate evaluation ──
    ls = strata_results["local-seen"]
    lu = strata_results["local-unseen"]
    nm = strata_results["normal"]
    total_parse_failures = sum(r["parse_failures"] for r in rows)

    gate_details = {
        "local_seen": {
            "value": ls["correct"],
            "threshold": GATES["local_seen_min"],
            "n": GATES["local_seen_n"],
            "pass": ls["correct"] >= GATES["local_seen_min"],
        },
        "local_unseen": {
            "value": lu["correct"],
            "threshold": GATES["local_unseen_min"],
            "n": GATES["local_unseen_n"],
            "pass": lu["correct"] >= GATES["local_unseen_min"],
        },
        "normal": {
            "value": nm["correct"],
            "threshold": GATES["normal_min"],
            "n": GATES["normal_n"],
            "pass": nm["correct"] >= GATES["normal_min"],
        },
        "parse_failures": {
            "value": total_parse_failures,
            "threshold": GATES["parse_failures_max"],
            "pass": total_parse_failures <= GATES["parse_failures_max"],
        },
    }
    gate_pass = all(g["pass"] for g in gate_details.values())

    overall_correct = sum(r["correct"] for r in rows)
    overall_n = len(rows)

    results = {
        "variant": VARIANT,
        "scope": "full_test",
        "analysis_kind": "post-hoc diagnostic; not an independent replication",
        "overall_accuracy": overall_correct / overall_n,
        "overall_correct": overall_correct,
        "overall_n": overall_n,
        "strata": strata_results,
        "gate_details": gate_details,
        "gate": "PASS" if gate_pass else "FAIL",
        "total_parse_failures": total_parse_failures,
        "total_abstentions": sum(r["abstain"] for r in rows),
        "total_three_of_three_agreement": sum(r["three_of_three_agreement"] for r in rows),
        "regressions": [
            {
                "agent_id": r["agent_id"],
                "physical_case_id": r["physical_case_id"],
                "stratum": r["stratum"],
                "frozen_B_label": r["frozen_B_label"],
                "variant_label": r["variant_label"],
                "expected_label": r["expected_label"],
            }
            for r in rows
            if r["change"] == "REGRESSED"
        ],
        "improvements": [
            {
                "agent_id": r["agent_id"],
                "physical_case_id": r["physical_case_id"],
                "stratum": r["stratum"],
                "frozen_B_label": r["frozen_B_label"],
                "variant_label": r["variant_label"],
                "expected_label": r["expected_label"],
            }
            for r in rows
            if r["change"] == "IMPROVED"
        ],
        "recommended_c06_status": (
            "Risolta — trasferimento negativo mitigato dal decision-policy block"
            if gate_pass
            else "Mitigata — full test non superato"
        ),
    }

    # ── Write outputs ──
    (OUTPUT_ROOT / "aggregate_records.jsonl").write_text(
        "".join(canonical_json(item) + "\n" for item in aggregates), encoding="utf-8"
    )
    (OUTPUT_ROOT / "full_test_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    with (OUTPUT_ROOT / "full_test_table.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    # ── Markdown report ──
    report_lines = [
        "# C06 B_LOCAL_FIRST_V1 — full test results",
        "",
        "> Post-hoc diagnostic analysis; this is not an independent replication.",
        "",
        f"Gate: **{results['gate']}**",
        "",
        "## Overall",
        "",
        f"- Accuracy: {overall_correct}/{overall_n} ({100 * overall_correct / overall_n:.1f}%)",
        f"- Abstentions: {results['total_abstentions']}",
        f"- Parse failures: {results['total_parse_failures']}",
        f"- Three-of-three agreement: {results['total_three_of_three_agreement']}/{overall_n}",
        "",
        "## Stratified results",
        "",
        "| Stratum | N | Correct | Accuracy | Frozen B | Delta | Gate | Pass |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for strat_name in ("local-seen", "local-unseen", "normal"):
        s = strata_results[strat_name]
        g = gate_details[strat_name.replace("-", "_")]
        delta = s["correct"] - s["frozen_B_correct"]
        sign = "+" if delta > 0 else ""
        report_lines.append(
            f"| {strat_name} | {s['n']} | {s['correct']} | {100*s['accuracy']:.1f}% | "
            f"{s['frozen_B_correct']}/{s['n']} | {sign}{delta} | "
            f"≥{g['threshold']} | {'PASS' if g['pass'] else 'FAIL'} |"
        )

    report_lines.extend([
        "",
        "## Regressions (correct in frozen B, wrong in variant)",
        "",
    ])
    regressions = [r for r in rows if r["change"] == "REGRESSED"]
    if regressions:
        report_lines.append(
            "| Agent | Case | Stratum | Expected | Frozen B | Variant | Reps |"
        )
        report_lines.append("|---|---|---|---|---|---|---|")
        for r in regressions:
            report_lines.append(
                f"| {r['agent_id']} | {r['physical_case_id']} | {r['stratum']} | "
                f"{r['expected_label']} | {r['frozen_B_label']} | "
                f"{r['variant_label']} | {r['repetitions']} |"
            )
    else:
        report_lines.append("None.")

    report_lines.extend([
        "",
        "## Improvements (wrong in frozen B, correct in variant)",
        "",
    ])
    improvements = [r for r in rows if r["change"] == "IMPROVED"]
    if improvements:
        report_lines.append(
            "| Agent | Case | Stratum | Expected | Frozen B | Variant | Reps |"
        )
        report_lines.append("|---|---|---|---|---|---|---|")
        for r in improvements:
            report_lines.append(
                f"| {r['agent_id']} | {r['physical_case_id']} | {r['stratum']} | "
                f"{r['expected_label']} | {r['frozen_B_label']} | "
                f"{r['variant_label']} | {r['repetitions']} |"
            )
    else:
        report_lines.append("None.")

    report_lines.extend([
        "",
        "## Full results by stratum",
        "",
    ])
    for strat_name in ("local-seen", "local-unseen", "normal"):
        srows = [r for r in rows if r["stratum"] == strat_name]
        report_lines.extend([
            f"### {strat_name} ({len(srows)} cases)",
            "",
            "| Agent | Case | Expected | Frozen B | Variant | Reps | Correct | Change | Insights |",
            "|---|---|---|---|---|---|---:|---|---|",
        ])
        for r in srows:
            report_lines.append(
                f"| {r['agent_id']} | {r['physical_case_id']} | {r['expected_label']} | "
                f"{r['frozen_B_label']} | {r['variant_label']} | {r['repetitions']} | "
                f"{'yes' if r['correct'] else 'no'} | {r['change']} | "
                f"{r['used_insight_ids'] or '—'} |"
            )
        report_lines.append("")

    (OUTPUT_ROOT / "FULL_TEST_REPORT.md").write_text(
        "\n".join(report_lines) + "\n", encoding="utf-8"
    )

    # ── Output hashes ──
    output_files = [
        "repetition_records.jsonl",
        "aggregate_records.jsonl",
        "execution_metadata.json",
        "full_test_results.json",
        "full_test_table.csv",
        "FULL_TEST_REPORT.md",
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
