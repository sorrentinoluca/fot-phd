#!/usr/bin/env python3
"""Evaluate frozen Phase B aggregate predictions against evaluator-side truth."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from phase_b.evaluation.bootstrap import (
    draw_stratified_physical_clusters,
    expand_cluster_sample,
)


INFERENCE_COMMIT = "11c34358e28e875cd5c7249061ac2b89ffcd42f4"
INFERENCE_TAG = "phase-b-inference-frozen"
SCHEDULE_SHA256 = "d30cdf6a6c622c1653176b393114073b447fdde69729086f6399291d776c0c9b"
INFERENCE_DIR = ROOT / "phase_b/final_evaluation/inference"
AGGREGATE_PATH = INFERENCE_DIR / "aggregate_records.jsonl"
INFERENCE_HASH_MANIFEST_PATH = INFERENCE_DIR / "inference_output_hash_manifest.json"
HELDOUT_MANIFEST_PATH = ROOT / "phase_b/heldout/phase_b_heldout_manifest.csv"
MAPPING_PATH = ROOT / "phase_b/config/evaluator_side/pseudolabel_mapping.json"
CONFIG_PATH = ROOT / "phase_b/config/protocol_config.json"
PROTOCOL_HASH_MANIFEST_PATH = ROOT / "phase_b/PHASE_B_PROTOCOL_HASHES.json"
METRICS_CODE_PATH = ROOT / "phase_b/evaluation/metrics.py"
BOOTSTRAP_CODE_PATH = ROOT / "phase_b/evaluation/bootstrap.py"
DEFAULT_OUTPUT_DIR = ROOT / "phase_b/final_evaluation"
CONDITIONS = ("A", "B", "E")
AGENTS = ("agent_1", "agent_2", "agent_3", "agent_4")
ABSTAIN_TOKEN = "__ABSTAIN__"


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_value(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if any(not line.strip() for line in lines):
        raise RuntimeError(f"blank JSONL line: {path}")
    return [json.loads(line) for line in lines]


def write_if_identical_or_absent(path: Path, content: bytes) -> None:
    if path.exists():
        if path.read_bytes() != content:
            raise RuntimeError(f"deterministic output differs from existing file: {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(content)
    temporary.replace(path)


def csv_bytes(fieldnames: list[str], rows: list[dict[str, Any]]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def verify_frozen_inputs() -> dict[str, str]:
    if git_value("rev-parse", f"{INFERENCE_TAG}^{{}}") != INFERENCE_COMMIT:
        raise RuntimeError("inference freeze tag target mismatch")
    if subprocess.run(
        ["git", "merge-base", "--is-ancestor", INFERENCE_COMMIT, "HEAD"],
        cwd=ROOT,
        check=False,
    ).returncode != 0:
        raise RuntimeError("current HEAD does not derive from inference freeze")

    inference_manifest = load_json(INFERENCE_HASH_MANIFEST_PATH)
    if inference_manifest["status"] != "IMMUTABLE_BEFORE_OFFLINE_EVALUATION":
        raise RuntimeError("inference output manifest status mismatch")
    for relative_path, expected_hash in inference_manifest["artifacts"].items():
        if sha256_file(ROOT / relative_path) != expected_hash:
            raise RuntimeError(f"inference output hash mismatch: {relative_path}")
    if (
        inference_manifest["schedule_reference"]["sha256"] != SCHEDULE_SHA256
        or sha256_file(ROOT / inference_manifest["schedule_reference"]["path"])
        != SCHEDULE_SHA256
    ):
        raise RuntimeError("execution schedule hash mismatch")

    protocol_manifest = load_json(PROTOCOL_HASH_MANIFEST_PATH)["artifacts"]
    for relative_path, expected_hash in protocol_manifest.items():
        if sha256_file(ROOT / relative_path) != expected_hash:
            raise RuntimeError(f"protocol frozen hash mismatch: {relative_path}")

    return {
        "inference_freeze_tag": INFERENCE_TAG,
        "inference_freeze_commit": INFERENCE_COMMIT,
        "inference_output_manifest_sha256": sha256_file(
            INFERENCE_HASH_MANIFEST_PATH
        ),
        "aggregate_predictions_sha256": sha256_file(AGGREGATE_PATH),
        "protocol_hash_manifest_sha256": sha256_file(PROTOCOL_HASH_MANIFEST_PATH),
        "schedule_sha256": SCHEDULE_SHA256,
    }


def load_case_truth(config: dict[str, Any]) -> tuple[dict[str, str], dict[str, Any]]:
    mapping = load_json(MAPPING_PATH)
    label_space = set(config["label_space"])
    real_to_opaque = mapping["real_to_opaque"]
    if set(real_to_opaque.values()) != label_space - {mapping["normal_label"]}:
        raise RuntimeError("pseudolabel mapping does not cover frozen fault labels")

    with HELDOUT_MANIFEST_PATH.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) != 15:
        raise RuntimeError("held-out manifest must contain exactly 15 cases")
    case_ids = [row["case_id"] for row in rows]
    if len(set(case_ids)) != 15 or set(case_ids) != {
        f"PBH-{index:03d}" for index in range(1, 16)
    }:
        raise RuntimeError("held-out physical_case_id coverage mismatch")

    case_truth: dict[str, str] = {}
    real_class_counts: Counter[str] = Counter()
    for row in rows:
        real_class = row["class_offline"]
        real_class_counts[real_class] += 1
        if real_class == "Normal":
            pseudolabel = mapping["normal_label"]
        elif real_class in real_to_opaque:
            pseudolabel = real_to_opaque[real_class]
        else:
            raise RuntimeError(f"unmapped offline class for {row['case_id']}")
        if pseudolabel not in label_space or row["case_id"] in case_truth:
            raise RuntimeError("invalid or duplicate case truth assignment")
        case_truth[row["case_id"]] = pseudolabel
    if set(real_class_counts.values()) != {3} or len(real_class_counts) != 5:
        raise RuntimeError("held-out manifest must contain three runs for each class")

    return case_truth, {
        "physical_cases_mapped": len(case_truth),
        "unique_mapping": True,
        "fault_pseudoclass_count": 4,
        "runs_per_class": 3,
        "heldout_manifest_sha256": sha256_file(HELDOUT_MANIFEST_PATH),
        "pseudolabel_mapping_sha256": sha256_file(MAPPING_PATH),
    }


def validate_parsed_output(parsed: dict[str, Any], labels: set[str]) -> None:
    if set(parsed) != {
        "predicted_label",
        "abstain",
        "used_insight_ids",
        "reasoning_summary",
    }:
        raise RuntimeError("aggregate parsed output schema mismatch")
    abstain = parsed["abstain"]
    prediction = parsed["predicted_label"]
    if type(abstain) is not bool:
        raise RuntimeError("aggregate abstain must be boolean")
    if abstain and prediction is not None:
        raise RuntimeError("aggregate abstain requires null predicted_label")
    if not abstain and prediction not in labels:
        raise RuntimeError("aggregate prediction outside frozen label space")
    if parsed["used_insight_ids"] != []:
        raise RuntimeError("aggregate outcome must not carry repetition insight IDs")


def load_aggregate_predictions(
    config: dict[str, Any], case_truth: dict[str, str]
) -> tuple[list[dict[str, Any]], dict[tuple[str, str, str], dict[str, Any]]]:
    records = load_jsonl(AGGREGATE_PATH)
    if len(records) != 180:
        raise RuntimeError("aggregate record count must be 180")
    labels = set(config["label_space"])
    lookup: dict[tuple[str, str, str], dict[str, Any]] = {}
    for record in records:
        if set(record) != {
            "physical_case_id",
            "agent_id",
            "condition",
            "parsed_output",
            "repetition_outcomes",
            "aggregation_rule",
        }:
            raise RuntimeError("aggregate record schema mismatch")
        if record["physical_case_id"] not in case_truth:
            raise RuntimeError("aggregate record lacks evaluator-side truth")
        if record["agent_id"] not in AGENTS or record["condition"] not in CONDITIONS:
            raise RuntimeError("aggregate agent or condition mismatch")
        if record["aggregation_rule"] != "frozen_valid_label_majority_2_of_3_else_abstain":
            raise RuntimeError("aggregate rule provenance mismatch")
        if len(record["repetition_outcomes"]) != 3:
            raise RuntimeError("aggregate must preserve three repetition outcomes")
        validate_parsed_output(record["parsed_output"], labels)
        key = (record["agent_id"], record["physical_case_id"], record["condition"])
        if key in lookup:
            raise RuntimeError("duplicate aggregate key")
        lookup[key] = record

    expected = {
        (agent, case_id, condition)
        for agent in AGENTS
        for case_id in case_truth
        for condition in CONDITIONS
    }
    if set(lookup) != expected:
        raise RuntimeError("aggregate keys are incomplete or unexpected")
    return records, lookup


def is_correct(record: dict[str, Any], truth: str) -> bool:
    parsed = record["parsed_output"]
    return bool(not parsed["abstain"] and parsed["predicted_label"] == truth)


def scope_of(agent_id: str, truth: str, config: dict[str, Any]) -> str:
    if truth == "Normal":
        return "normal"
    if truth == config["agents"][agent_id]["local_fault_label"]:
        return "local_fault_seen"
    return "unseen"


def metric(rows: list[tuple[dict[str, Any], str]]) -> dict[str, Any]:
    n = len(rows)
    correct = sum(is_correct(record, truth) for record, truth in rows)
    abstentions = sum(record["parsed_output"]["abstain"] for record, _ in rows)
    return {
        "n": n,
        "correct": correct,
        "accuracy": correct / n if n else None,
        "abstentions": abstentions,
        "abstention_rate": abstentions / n if n else None,
    }


def condition_metrics(
    records: list[dict[str, Any]], case_truth: dict[str, str], config: dict[str, Any]
) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for condition in CONDITIONS:
        rows = [
            (record, case_truth[record["physical_case_id"]])
            for record in records
            if record["condition"] == condition
        ]
        result[condition] = {"overall": metric(rows)}
        for scope in ("unseen", "local_fault_seen", "normal"):
            selected = [
                (record, truth)
                for record, truth in rows
                if scope_of(record["agent_id"], truth, config) == scope
            ]
            result[condition][scope] = metric(selected)
    return result


def paired_unseen_rows(
    lookup: dict[tuple[str, str, str], dict[str, Any]],
    case_truth: dict[str, str],
    config: dict[str, Any],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for agent_id in AGENTS:
        for case_id in sorted(case_truth):
            truth = case_truth[case_id]
            if scope_of(agent_id, truth, config) != "unseen":
                continue
            correct = {
                condition: int(
                    is_correct(lookup[(agent_id, case_id, condition)], truth)
                )
                for condition in CONDITIONS
            }
            rows.append(
                {
                    "physical_case_id": case_id,
                    "true_pseudolabel": truth,
                    "agent_id": agent_id,
                    "A_correct": correct["A"],
                    "B_correct": correct["B"],
                    "E_correct": correct["E"],
                    "delta_unseen": correct["B"] - correct["A"],
                    "delta_specificity": correct["B"] - correct["E"],
                }
            )
    return rows


def transfer_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    helped = harmed = unchanged_correct = unchanged_incorrect = 0
    for row in rows:
        left, right = row["A_correct"], row["B_correct"]
        if not left and right:
            helped += 1
        elif left and not right:
            harmed += 1
        elif left and right:
            unchanged_correct += 1
        else:
            unchanged_incorrect += 1
    unchanged = unchanged_correct + unchanged_incorrect
    return {
        "n_pairs": len(rows),
        "helped": helped,
        "harmed": harmed,
        "unchanged": unchanged,
        "unchanged_correct": unchanged_correct,
        "unchanged_incorrect": unchanged_incorrect,
    }


def per_agent_primary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for agent_id in AGENTS:
        selected = [row for row in rows if row["agent_id"] == agent_id]
        if len(selected) != 9:
            raise RuntimeError("each agent must have nine unseen fault cases")
        accuracies = {
            condition: sum(row[f"{condition}_correct"] for row in selected)
            / len(selected)
            for condition in CONDITIONS
        }
        result[agent_id] = {
            "n": len(selected),
            "A_accuracy": accuracies["A"],
            "B_accuracy": accuracies["B"],
            "E_accuracy": accuracies["E"],
            "delta_unseen_B_minus_A": accuracies["B"] - accuracies["A"],
        }
    return result


def recall_and_confusion(
    records: list[dict[str, Any]], case_truth: dict[str, str], config: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    recall: dict[str, Any] = {}
    confusion: dict[str, Any] = {}
    labels = list(config["label_space"])
    prediction_columns = labels + [ABSTAIN_TOKEN]
    for condition in CONDITIONS:
        selected = [record for record in records if record["condition"] == condition]
        recall[condition] = {}
        matrix = {
            truth: {prediction: 0 for prediction in prediction_columns}
            for truth in labels
        }
        for record in selected:
            truth = case_truth[record["physical_case_id"]]
            parsed = record["parsed_output"]
            predicted = ABSTAIN_TOKEN if parsed["abstain"] else parsed["predicted_label"]
            matrix[truth][predicted] += 1
        for label in labels:
            label_rows = [
                (record, case_truth[record["physical_case_id"]])
                for record in selected
                if case_truth[record["physical_case_id"]] == label
            ]
            recall[condition][label] = metric(label_rows)
        confusion[condition] = matrix
    return recall, confusion


def bootstrap_primary(
    rows: list[dict[str, Any]], *, iterations: int, seed: int
) -> dict[str, Any]:
    if len(rows) != 36:
        raise RuntimeError("bootstrap primary rows must equal 36")
    clusters = sorted({row["physical_case_id"] for row in rows})
    strata: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        strata[row["true_pseudolabel"]].add(row["physical_case_id"])
    if len(clusters) != 12 or len(strata) != 4 or {
        len(cases) for cases in strata.values()
    } != {3}:
        raise RuntimeError("bootstrap requires four strata with three clusters each")
    cluster_sizes = Counter(row["physical_case_id"] for row in rows)
    if set(cluster_sizes.values()) != {3}:
        raise RuntimeError("each physical cluster must retain three unseen agent rows")

    rng = np.random.default_rng(seed)
    delta_unseen_draws = np.empty(iterations, dtype=float)
    delta_specificity_draws = np.empty(iterations, dtype=float)
    for index in range(iterations):
        sampled_clusters = draw_stratified_physical_clusters(rows, rng)
        expanded = expand_cluster_sample(rows, sampled_clusters)
        delta_unseen_draws[index] = np.mean(
            [row["delta_unseen"] for row in expanded]
        )
        delta_specificity_draws[index] = np.mean(
            [row["delta_specificity"] for row in expanded]
        )

    def summary(values: np.ndarray, field: str) -> dict[str, Any]:
        return {
            "definition": field,
            "point_estimate": float(np.mean([row[field] for row in rows])),
            "confidence_level": 0.95,
            "ci_lower": float(np.quantile(values, 0.025)),
            "ci_upper": float(np.quantile(values, 0.975)),
        }

    return {
        "method": "paired physical_case_id cluster bootstrap stratified by true pseudolabel",
        "draws": iterations,
        "seed": seed,
        "quantiles": [0.025, 0.975],
        "quantile_method": "numpy.quantile default linear",
        "n_physical_clusters": len(clusters),
        "n_agent_case_rows": len(rows),
        "clusters_per_pseudolabel": {
            label: len(cases) for label, cases in sorted(strata.items())
        },
        "rows_per_physical_cluster": 3,
        "independence_claim": False,
        "delta_unseen_B_minus_A": summary(delta_unseen_draws, "delta_unseen"),
        "delta_specificity_B_minus_E": summary(
            delta_specificity_draws, "delta_specificity"
        ),
    }


def integrity_checks(
    conditions: dict[str, Any],
    rows: list[dict[str, Any]],
    per_agent: dict[str, Any],
    transfers: dict[str, int],
    confusion: dict[str, Any],
    bootstrap: dict[str, Any],
) -> dict[str, Any]:
    checks = {
        "primary_denominator_36_each_condition": all(
            conditions[condition]["unseen"]["n"] == 36 for condition in CONDITIONS
        ),
        "physical_fault_clusters_12": bootstrap["n_physical_clusters"] == 12,
        "local_fault_seen_denominator_12_each_condition": all(
            conditions[condition]["local_fault_seen"]["n"] == 12
            for condition in CONDITIONS
        ),
        "normal_denominator_12_each_condition": all(
            conditions[condition]["normal"]["n"] == 12 for condition in CONDITIONS
        ),
        "overall_denominator_60_each_condition": all(
            conditions[condition]["overall"]["n"] == 60 for condition in CONDITIONS
        ),
        "transfer_total_36": transfers["helped"]
        + transfers["harmed"]
        + transfers["unchanged"]
        == 36,
        "confusion_total_60_each_condition": all(
            sum(sum(predictions.values()) for predictions in confusion[condition].values())
            == 60
            for condition in CONDITIONS
        ),
        "per_agent_unseen_total_9": all(
            per_agent[agent]["n"] == 9 for agent in AGENTS
        ),
        "bootstrap_strata_4_by_3": len(bootstrap["clusters_per_pseudolabel"])
        == 4
        and set(bootstrap["clusters_per_pseudolabel"].values()) == {3},
        "aggregate_source_only": len(rows) == 36,
    }
    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise RuntimeError(f"internal consistency check failed: {failed}")
    return {"status": "PASS", **checks}


def build_results() -> tuple[dict[str, Any], dict[str, bytes]]:
    frozen_inputs = verify_frozen_inputs()
    config = load_json(CONFIG_PATH)
    case_truth, truth_integrity = load_case_truth(config)
    records, lookup = load_aggregate_predictions(config, case_truth)
    conditions = condition_metrics(records, case_truth, config)
    rows = paired_unseen_rows(lookup, case_truth, config)
    if len(rows) != 36:
        raise RuntimeError("primary unseen subset must contain 36 rows")
    per_agent = per_agent_primary(rows)
    transfers = transfer_counts(rows)
    recall, confusion = recall_and_confusion(records, case_truth, config)

    delta_unseen = (
        conditions["B"]["unseen"]["accuracy"]
        - conditions["A"]["unseen"]["accuracy"]
    )
    delta_e = (
        conditions["E"]["unseen"]["accuracy"]
        - conditions["A"]["unseen"]["accuracy"]
    )
    delta_specificity = (
        conditions["B"]["unseen"]["accuracy"]
        - conditions["E"]["unseen"]["accuracy"]
    )
    positive_agents = sum(
        per_agent[agent]["delta_unseen_B_minus_A"] > 0 for agent in AGENTS
    )
    local_seen_delta = (
        conditions["B"]["local_fault_seen"]["accuracy"]
        - conditions["A"]["local_fault_seen"]["accuracy"]
    )
    criteria = {
        "C1_delta_unseen_gt_0": delta_unseen > 0,
        "C2_positive_delta_at_least_3_of_4_agents": positive_agents >= 3,
        "C3_helped_gt_harmed": transfers["helped"] > transfers["harmed"],
        "C4_delta_unseen_gt_delta_E": delta_unseen > delta_e,
        "H2_local_fault_seen_B_ge_A_epsilon_0": local_seen_delta >= 0,
    }
    bootstrap = bootstrap_primary(
        rows,
        iterations=int(config["metrics"]["bootstrap_iterations"]),
        seed=int(config["metrics"]["bootstrap_seed"]),
    )
    checks = integrity_checks(
        conditions, rows, per_agent, transfers, confusion, bootstrap
    )

    results = {
        "artifact_version": "1",
        "evaluation_status": "OFFLINE_EVALUATION_OF_FROZEN_AGGREGATE_PREDICTIONS",
        "primary_prediction_source": "phase_b/final_evaluation/inference/aggregate_records.jsonl",
        "aggregation_recomputed": False,
        "abstain_treatment": "incorrect",
        "ground_truth_join": truth_integrity,
        "condition_metrics": conditions,
        "primary": {
            "unit": "aggregate agent-case observation",
            "n_per_condition": 36,
            "physical_clusters": 12,
            "accuracy_A_unseen": conditions["A"]["unseen"]["accuracy"],
            "accuracy_B_unseen": conditions["B"]["unseen"]["accuracy"],
            "accuracy_E_unseen": conditions["E"]["unseen"]["accuracy"],
            "delta_unseen_B_minus_A": delta_unseen,
            "delta_E_E_minus_A": delta_e,
            "delta_specificity_B_minus_E": delta_specificity,
            "per_agent": per_agent,
            "positive_delta_agents": positive_agents,
            "transfer_B_vs_A": transfers,
        },
        "secondary": {
            "local_fault_seen_B_minus_A": local_seen_delta,
            "normal_B_minus_A": conditions["B"]["normal"]["accuracy"]
            - conditions["A"]["normal"]["accuracy"],
            "overall_B_minus_A": conditions["B"]["overall"]["accuracy"]
            - conditions["A"]["overall"]["accuracy"],
            "per_pseudolabel_recall": recall,
            "confusion_matrices": confusion,
        },
        "bootstrap": bootstrap,
        "frozen_criteria": {
            **criteria,
            "primary_support_criteria_satisfied": sum(
                criteria[name]
                for name in (
                    "C1_delta_unseen_gt_0",
                    "C2_positive_delta_at_least_3_of_4_agents",
                    "C3_helped_gt_harmed",
                    "C4_delta_unseen_gt_delta_E",
                )
            ),
            "primary_support_criteria_total": 4,
        },
        "integrity_checks": checks,
        "reproducibility": {
            **frozen_inputs,
            "evaluator_code_sha256": sha256_file(Path(__file__)),
            "metrics_code_sha256": sha256_file(METRICS_CODE_PATH),
            "bootstrap_code_sha256": sha256_file(BOOTSTRAP_CODE_PATH),
            "mapping_sha256": sha256_file(MAPPING_PATH),
            "heldout_manifest_sha256": sha256_file(HELDOUT_MANIFEST_PATH),
            "bootstrap_draws": int(config["metrics"]["bootstrap_iterations"]),
            "bootstrap_seed": int(config["metrics"]["bootstrap_seed"]),
        },
    }

    primary_rows = [
        {"condition": condition, **conditions[condition]["unseen"]}
        for condition in CONDITIONS
    ]
    agent_rows = [
        {"agent_id": agent, **per_agent[agent]} for agent in AGENTS
    ]
    secondary_rows = [
        {"scope": scope, "condition": condition, **conditions[condition][scope]}
        for scope in ("local_fault_seen", "normal", "overall")
        for condition in CONDITIONS
    ]
    transfer_rows = [{"comparison": "B_vs_A_primary_unseen", **transfers}]

    artifacts = {
        "evaluation_results.json": canonical_json_bytes(results),
        "primary_metrics.csv": csv_bytes(
            ["condition", "n", "correct", "accuracy", "abstentions", "abstention_rate"],
            primary_rows,
        ),
        "per_agent_metrics.csv": csv_bytes(
            [
                "agent_id",
                "n",
                "A_accuracy",
                "B_accuracy",
                "E_accuracy",
                "delta_unseen_B_minus_A",
            ],
            agent_rows,
        ),
        "secondary_metrics.csv": csv_bytes(
            ["scope", "condition", "n", "correct", "accuracy", "abstentions", "abstention_rate"],
            secondary_rows,
        ),
        "transfer_counts.csv": csv_bytes(
            [
                "comparison",
                "n_pairs",
                "helped",
                "harmed",
                "unchanged",
                "unchanged_correct",
                "unchanged_incorrect",
            ],
            transfer_rows,
        ),
        "confusion_matrices.json": canonical_json_bytes(
            {"confusion_matrices": confusion, "per_pseudolabel_recall": recall}
        ),
        "bootstrap_results.json": canonical_json_bytes(bootstrap),
    }
    artifacts["EVALUATION_REPORT.md"] = render_report(results).encode("utf-8")
    return results, artifacts


def pct(value: float) -> str:
    return f"{100.0 * value:.2f}%"


def criterion(value: bool) -> str:
    return "PASS" if value else "FAIL"


def render_report(results: dict[str, Any]) -> str:
    primary = results["primary"]
    conditions = results["condition_metrics"]
    bootstrap = results["bootstrap"]
    criteria = results["frozen_criteria"]
    lines = [
        "# Phase B final offline evaluation",
        "",
        "The primary analysis uses only the frozen R=3 aggregate outcomes. "
        "No aggregation was recomputed and abstentions count as incorrect.",
        "",
        "## Primary: locally unseen faults",
        "",
        "| Condition | Correct / n | Accuracy | Abstentions |",
        "|---|---:|---:|---:|",
    ]
    for condition in CONDITIONS:
        value = conditions[condition]["unseen"]
        lines.append(
            f"| {condition} | {value['correct']} / {value['n']} | "
            f"{pct(value['accuracy'])} | {value['abstentions']} |"
        )
    lines.extend(
        [
            "",
            f"- Delta_unseen (B−A): {primary['delta_unseen_B_minus_A']:.12g}",
            f"- Delta_E (E−A): {primary['delta_E_E_minus_A']:.12g}",
            f"- Delta_specificity (B−E): {primary['delta_specificity_B_minus_E']:.12g}",
            "",
            "### Per-agent primary",
            "",
            "| Agent | n | A | B | E | Delta B−A |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for agent in AGENTS:
        value = primary["per_agent"][agent]
        lines.append(
            f"| {agent} | {value['n']} | {pct(value['A_accuracy'])} | "
            f"{pct(value['B_accuracy'])} | {pct(value['E_accuracy'])} | "
            f"{value['delta_unseen_B_minus_A']:.12g} |"
        )
    transfer = primary["transfer_B_vs_A"]
    lines.extend(
        [
            "",
            "### Paired B versus A transfers",
            "",
            f"- Helped: {transfer['helped']}",
            f"- Harmed: {transfer['harmed']}",
            f"- Unchanged: {transfer['unchanged']} "
            f"(correct {transfer['unchanged_correct']}, incorrect {transfer['unchanged_incorrect']})",
            "",
            "### Frozen support criteria",
            "",
            f"- C1 Delta_unseen > 0: {criterion(criteria['C1_delta_unseen_gt_0'])}",
            f"- C2 positive delta in at least 3/4 agents: "
            f"{criterion(criteria['C2_positive_delta_at_least_3_of_4_agents'])}",
            f"- C3 helped > harmed: {criterion(criteria['C3_helped_gt_harmed'])}",
            f"- C4 Delta_unseen > Delta_E: "
            f"{criterion(criteria['C4_delta_unseen_gt_delta_E'])}",
            f"- Primary support criteria satisfied: "
            f"{criteria['primary_support_criteria_satisfied']}/4",
            "",
            "### Frozen cluster bootstrap",
            "",
            f"- Draws: {bootstrap['draws']}; seed: {bootstrap['seed']}",
            f"- Delta_unseen 95% CI: "
            f"[{bootstrap['delta_unseen_B_minus_A']['ci_lower']:.12g}, "
            f"{bootstrap['delta_unseen_B_minus_A']['ci_upper']:.12g}]",
            f"- Delta_specificity 95% CI: "
            f"[{bootstrap['delta_specificity_B_minus_E']['ci_lower']:.12g}, "
            f"{bootstrap['delta_specificity_B_minus_E']['ci_upper']:.12g}]",
            "",
            "## Secondary outcomes",
            "",
        ]
    )
    for scope, title in (
        ("local_fault_seen", "Local fault seen"),
        ("normal", "Normal"),
        ("overall", "Overall"),
    ):
        lines.extend(
            [
                f"### {title}",
                "",
                "| Condition | Correct / n | Accuracy | Abstention rate |",
                "|---|---:|---:|---:|",
            ]
        )
        for condition in CONDITIONS:
            value = conditions[condition][scope]
            lines.append(
                f"| {condition} | {value['correct']} / {value['n']} | "
                f"{pct(value['accuracy'])} | {pct(value['abstention_rate'])} |"
            )
        lines.append("")
    lines.extend(
        [
            f"H2 (B local-fault-seen accuracy ≥ A, epsilon=0): "
            f"**{criterion(criteria['H2_local_fault_seen_B_ge_A_epsilon_0'])}**",
            "",
            "Per-pseudolabel recall and complete confusion matrices are preserved in "
            "`confusion_matrices.json`.",
            "",
            "## Integrity and reproducibility",
            "",
            "- Ground-truth join: 15/15 physical cases, unique.",
            "- Primary denominator: 36 aggregate agent-case observations per condition.",
            "- Independent physical fault clusters: 12.",
            "- Local-fault-seen denominator: 12 per condition.",
            "- Normal denominator: 12 per condition.",
            "- Overall denominator: 60 per condition.",
            "- All internal consistency checks: PASS.",
            f"- Inference freeze: `{INFERENCE_TAG}` at `{INFERENCE_COMMIT}`.",
            "",
        ]
    )
    return "\n".join(lines)


def evaluate(output_dir: Path) -> dict[str, Any]:
    results, artifacts = build_results()
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, content in artifacts.items():
        write_if_identical_or_absent(output_dir / name, content)

    relative_artifacts: dict[str, str] = {}
    for name in sorted(artifacts):
        path = output_dir / name
        try:
            relative = str(path.relative_to(ROOT))
        except ValueError:
            relative = name
        relative_artifacts[relative] = sha256_file(path)
    hash_manifest = {
        "artifact_version": "1",
        "status": "OFFLINE_EVALUATION_COMPLETE_AWAITING_RESULTS_REVIEW",
        "inference_freeze_tag": INFERENCE_TAG,
        "inference_freeze_commit": INFERENCE_COMMIT,
        "primary_prediction_source": str(AGGREGATE_PATH.relative_to(ROOT)),
        "input_aggregate_predictions_sha256": sha256_file(AGGREGATE_PATH),
        "evaluator_code_sha256": sha256_file(Path(__file__)),
        "metrics_code_sha256": sha256_file(METRICS_CODE_PATH),
        "bootstrap_code_sha256": sha256_file(BOOTSTRAP_CODE_PATH),
        "mapping_sha256": sha256_file(MAPPING_PATH),
        "evaluation_artifacts": relative_artifacts,
    }
    write_if_identical_or_absent(
        output_dir / "evaluation_hash_manifest.json",
        canonical_json_bytes(hash_manifest),
    )
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    results = evaluate(args.output_dir.resolve())
    primary = results["primary"]
    print(
        json.dumps(
            {
                "status": "COMPLETE",
                "aggregate_source_only": True,
                "primary_n_per_condition": primary["n_per_condition"],
                "physical_clusters": primary["physical_clusters"],
                "integrity": results["integrity_checks"]["status"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
