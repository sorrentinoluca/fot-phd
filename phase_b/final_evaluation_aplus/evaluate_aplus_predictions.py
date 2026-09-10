#!/usr/bin/env python3
"""Evaluate A+ (local-only self-insight) aggregate predictions against evaluator-side truth.

Joins A+ results with the existing frozen A/B/E evaluation to produce a
four-condition comparison.  Does NOT modify any frozen A/B/E artifacts.

Outputs go to  phase_b/final_evaluation_aplus/  alongside the inference data.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import io
import json
from pathlib import Path
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


# ── frozen A/B/E evaluation (read-only reference) ──────────────────────
ABE_RESULTS_PATH = ROOT / "phase_b/final_evaluation/evaluation_results.json"
ABE_AGGREGATE_PATH = ROOT / "phase_b/final_evaluation/inference/aggregate_records.jsonl"

# ── A+ inference outputs ────────────────────────────────────────────────
APLUS_DIR = ROOT / "phase_b/final_evaluation_aplus"
APLUS_FREEZE_MANIFEST_PATH = APLUS_DIR / "APLUS_FREEZE_MANIFEST.json"
APLUS_INFERENCE_DIR = APLUS_DIR / "inference"
APLUS_AGGREGATE_PATH = APLUS_INFERENCE_DIR / "aggregate_records.jsonl"
APLUS_METADATA_PATH = APLUS_INFERENCE_DIR / "execution_metadata.json"
APLUS_HASH_MANIFEST_PATH = APLUS_INFERENCE_DIR / "inference_output_hash_manifest.json"

# ── shared protocol ─────────────────────────────────────────────────────
HELDOUT_MANIFEST_PATH = ROOT / "phase_b/heldout/phase_b_heldout_manifest.csv"
MAPPING_PATH = ROOT / "phase_b/config/evaluator_side/pseudolabel_mapping.json"
CONFIG_PATH = ROOT / "phase_b/config/protocol_config.json"
METRICS_CODE_PATH = ROOT / "phase_b/evaluation/metrics.py"
BOOTSTRAP_CODE_PATH = ROOT / "phase_b/evaluation/bootstrap.py"

DEFAULT_OUTPUT_DIR = APLUS_DIR
ALL_CONDITIONS = ("A", "A+", "B", "E")
AGENTS = ("agent_1", "agent_2", "agent_3", "agent_4")
ABSTAIN_TOKEN = "__ABSTAIN__"


# ── utility ─────────────────────────────────────────────────────────────

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


# ── input verification ──────────────────────────────────────────────────

def verify_frozen_inputs() -> dict[str, str]:
    """Verify A+ inference outputs and that the A/B/E results are untouched."""
    # 1. Verify A+ freeze manifest artifacts
    manifest = load_json(APLUS_FREEZE_MANIFEST_PATH)
    for rel_path, expected_hash in manifest["self_insight_libraries"].items():
        if sha256_file(ROOT / rel_path) != expected_hash:
            raise RuntimeError(f"self-insight library hash mismatch: {rel_path}")

    # 2. Verify A+ inference output hash manifest
    aplus_hash_manifest = load_json(APLUS_HASH_MANIFEST_PATH)
    if aplus_hash_manifest["status"] != "APLUS_INFERENCE_COMPLETE":
        raise RuntimeError("A+ inference output manifest status mismatch")
    for relative_path, expected_hash in aplus_hash_manifest["artifacts"].items():
        if sha256_file(ROOT / relative_path) != expected_hash:
            raise RuntimeError(f"A+ inference output hash mismatch: {relative_path}")

    # 3. Verify A/B/E evaluation results are untouched
    abe_results = load_json(ABE_RESULTS_PATH)
    if abe_results["evaluation_status"] != "OFFLINE_EVALUATION_OF_FROZEN_AGGREGATE_PREDICTIONS":
        raise RuntimeError("A/B/E evaluation status mismatch")
    abe_agg_sha = abe_results["reproducibility"]["aggregate_predictions_sha256"]
    if sha256_file(ABE_AGGREGATE_PATH) != abe_agg_sha:
        raise RuntimeError("A/B/E aggregate predictions have been modified")

    return {
        "abe_evaluation_results_sha256": sha256_file(ABE_RESULTS_PATH),
        "abe_aggregate_predictions_sha256": abe_agg_sha,
        "aplus_freeze_manifest_sha256": sha256_file(APLUS_FREEZE_MANIFEST_PATH),
        "aplus_aggregate_predictions_sha256": sha256_file(APLUS_AGGREGATE_PATH),
        "aplus_inference_hash_manifest_sha256": sha256_file(APLUS_HASH_MANIFEST_PATH),
    }


# ── ground truth ────────────────────────────────────────────────────────

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


# ── prediction loading ──────────────────────────────────────────────────

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


def load_abe_aggregates(
    config: dict[str, Any], case_truth: dict[str, str]
) -> dict[tuple[str, str, str], dict[str, Any]]:
    """Load A/B/E aggregate predictions from the frozen evaluation."""
    records = load_jsonl(ABE_AGGREGATE_PATH)
    if len(records) != 180:
        raise RuntimeError("A/B/E aggregate record count must be 180")
    labels = set(config["label_space"])
    lookup: dict[tuple[str, str, str], dict[str, Any]] = {}
    for record in records:
        if record["physical_case_id"] not in case_truth:
            raise RuntimeError("A/B/E aggregate record lacks evaluator-side truth")
        if record["agent_id"] not in AGENTS or record["condition"] not in ("A", "B", "E"):
            raise RuntimeError("A/B/E aggregate agent or condition mismatch")
        validate_parsed_output(record["parsed_output"], labels)
        key = (record["agent_id"], record["physical_case_id"], record["condition"])
        if key in lookup:
            raise RuntimeError("duplicate A/B/E aggregate key")
        lookup[key] = record
    expected = {
        (agent, case_id, condition)
        for agent in AGENTS
        for case_id in case_truth
        for condition in ("A", "B", "E")
    }
    if set(lookup) != expected:
        raise RuntimeError("A/B/E aggregate keys are incomplete or unexpected")
    return lookup


def load_aplus_aggregates(
    config: dict[str, Any], case_truth: dict[str, str]
) -> dict[tuple[str, str, str], dict[str, Any]]:
    """Load A+ aggregate predictions."""
    records = load_jsonl(APLUS_AGGREGATE_PATH)
    if len(records) != 60:
        raise RuntimeError("A+ aggregate record count must be 60")
    labels = set(config["label_space"])
    lookup: dict[tuple[str, str, str], dict[str, Any]] = {}
    for record in records:
        if record["physical_case_id"] not in case_truth:
            raise RuntimeError("A+ aggregate record lacks evaluator-side truth")
        if record["agent_id"] not in AGENTS:
            raise RuntimeError("A+ aggregate agent mismatch")
        if record["condition"] != "A+":
            raise RuntimeError(f"A+ aggregate has wrong condition: {record['condition']}")
        if record["aggregation_rule"] != "frozen_valid_label_majority_2_of_3_else_abstain":
            raise RuntimeError("A+ aggregate rule provenance mismatch")
        if len(record["repetition_outcomes"]) != 3:
            raise RuntimeError("A+ aggregate must preserve three repetition outcomes")
        validate_parsed_output(record["parsed_output"], labels)
        key = (record["agent_id"], record["physical_case_id"], "A+")
        if key in lookup:
            raise RuntimeError("duplicate A+ aggregate key")
        lookup[key] = record
    expected = {
        (agent, case_id, "A+")
        for agent in AGENTS
        for case_id in case_truth
    }
    if set(lookup) != expected:
        raise RuntimeError("A+ aggregate keys are incomplete or unexpected")
    return lookup


# ── metrics ─────────────────────────────────────────────────────────────

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


def condition_metrics_all(
    lookup: dict[tuple[str, str, str], dict[str, Any]],
    case_truth: dict[str, str],
    config: dict[str, Any],
) -> dict[str, Any]:
    """Compute per-condition metrics for A, A+, B, E."""
    result: dict[str, Any] = {}
    for condition in ALL_CONDITIONS:
        rows = [
            (lookup[(agent, case_id, condition)], case_truth[case_id])
            for agent in AGENTS
            for case_id in case_truth
            if (agent, case_id, condition) in lookup
        ]
        if len(rows) != 60:
            raise RuntimeError(f"condition {condition} must have 60 observations, got {len(rows)}")
        result[condition] = {"overall": metric(rows)}
        for scope in ("unseen", "local_fault_seen", "normal"):
            selected = [
                (record, truth)
                for record, truth in rows
                if scope_of(record["agent_id"], truth, config) == scope
            ]
            result[condition][scope] = metric(selected)
    return result


def paired_unseen_rows_all(
    lookup: dict[tuple[str, str, str], dict[str, Any]],
    case_truth: dict[str, str],
    config: dict[str, Any],
) -> list[dict[str, Any]]:
    """Build paired rows for all four conditions on unseen faults."""
    rows: list[dict[str, Any]] = []
    for agent_id in AGENTS:
        for case_id in sorted(case_truth):
            truth = case_truth[case_id]
            if scope_of(agent_id, truth, config) != "unseen":
                continue
            correct = {
                condition: int(is_correct(lookup[(agent_id, case_id, condition)], truth))
                for condition in ALL_CONDITIONS
            }
            rows.append(
                {
                    "physical_case_id": case_id,
                    "true_pseudolabel": truth,
                    "agent_id": agent_id,
                    "A_correct": correct["A"],
                    "Aplus_correct": correct["A+"],
                    "B_correct": correct["B"],
                    "E_correct": correct["E"],
                    # Primary deltas involving A+
                    "delta_Aplus_minus_A": correct["A+"] - correct["A"],
                    "delta_B_minus_Aplus": correct["B"] - correct["A+"],
                    "delta_E_minus_Aplus": correct["E"] - correct["A+"],
                    # Original deltas
                    "delta_B_minus_A": correct["B"] - correct["A"],
                    "delta_B_minus_E": correct["B"] - correct["E"],
                }
            )
    return rows


def transfer_counts_pair(
    rows: list[dict[str, Any]], left_key: str, right_key: str, label: str
) -> dict[str, int]:
    """Count helped/harmed/unchanged between two conditions on unseen rows."""
    helped = harmed = unchanged_correct = unchanged_incorrect = 0
    for row in rows:
        left, right = row[left_key], row[right_key]
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
        "comparison": label,
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
        accuracies = {}
        for condition, key in [("A", "A_correct"), ("A+", "Aplus_correct"),
                               ("B", "B_correct"), ("E", "E_correct")]:
            accuracies[condition] = sum(row[key] for row in selected) / len(selected)
        result[agent_id] = {
            "n": len(selected),
            "A_accuracy": accuracies["A"],
            "Aplus_accuracy": accuracies["A+"],
            "B_accuracy": accuracies["B"],
            "E_accuracy": accuracies["E"],
            "delta_Aplus_minus_A": accuracies["A+"] - accuracies["A"],
            "delta_B_minus_Aplus": accuracies["B"] - accuracies["A+"],
            "delta_B_minus_A": accuracies["B"] - accuracies["A"],
        }
    return result


def recall_and_confusion_aplus(
    lookup: dict[tuple[str, str, str], dict[str, Any]],
    case_truth: dict[str, str],
    config: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Recall and confusion matrix for condition A+ only."""
    labels = list(config["label_space"])
    prediction_columns = labels + [ABSTAIN_TOKEN]
    recall: dict[str, Any] = {}
    matrix = {
        truth: {prediction: 0 for prediction in prediction_columns}
        for truth in labels
    }
    records_aplus = [
        lookup[(agent, case_id, "A+")]
        for agent in AGENTS
        for case_id in sorted(case_truth)
    ]
    for record in records_aplus:
        truth = case_truth[record["physical_case_id"]]
        parsed = record["parsed_output"]
        predicted = ABSTAIN_TOKEN if parsed["abstain"] else parsed["predicted_label"]
        matrix[truth][predicted] += 1
    for label in labels:
        label_rows = [
            (record, case_truth[record["physical_case_id"]])
            for record in records_aplus
            if case_truth[record["physical_case_id"]] == label
        ]
        recall[label] = metric(label_rows)
    return recall, matrix


def inter_rep_agreement(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute inter-repetition agreement for A+ aggregate records."""
    total = 0
    unanimous = 0
    two_of_three = 0
    all_different = 0
    for record in records:
        outcomes = record["repetition_outcomes"]
        labels = []
        for outcome in outcomes:
            if isinstance(outcome, dict):
                if outcome.get("abstain", False):
                    labels.append("__ABSTAIN__")
                else:
                    labels.append(outcome.get("predicted_label", "__PARSE_FAIL__"))
            else:
                labels.append(str(outcome))
        total += 1
        counts = Counter(labels)
        most_common_count = counts.most_common(1)[0][1]
        if most_common_count == 3:
            unanimous += 1
        elif most_common_count == 2:
            two_of_three += 1
        else:
            all_different += 1
    return {
        "total_aggregates": total,
        "unanimous_3_of_3": unanimous,
        "majority_2_of_3": two_of_three,
        "all_different": all_different,
        "unanimity_rate": unanimous / total if total else None,
    }


def bootstrap_aplus(
    rows: list[dict[str, Any]],
    *,
    delta_field: str,
    definition: str,
    iterations: int,
    seed: int,
) -> dict[str, Any]:
    """Paired cluster bootstrap for a specific delta field."""
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
    draws = np.empty(iterations, dtype=float)
    for index in range(iterations):
        sampled_clusters = draw_stratified_physical_clusters(rows, rng)
        expanded = expand_cluster_sample(rows, sampled_clusters)
        draws[index] = np.mean([row[delta_field] for row in expanded])

    return {
        "definition": definition,
        "point_estimate": float(np.mean([row[delta_field] for row in rows])),
        "confidence_level": 0.95,
        "ci_lower": float(np.quantile(draws, 0.025)),
        "ci_upper": float(np.quantile(draws, 0.975)),
        "draws": iterations,
        "seed": seed,
        "n_physical_clusters": len(clusters),
        "n_agent_case_rows": len(rows),
        "clusters_per_pseudolabel": {
            label: len(cases) for label, cases in sorted(strata.items())
        },
        "rows_per_physical_cluster": 3,
        "independence_claim": False,
    }


# ── integrity ───────────────────────────────────────────────────────────

def integrity_checks(
    conditions: dict[str, Any],
    rows: list[dict[str, Any]],
    per_agent: dict[str, Any],
    transfers: dict[str, dict[str, int]],
    confusion_aplus: dict[str, Any],
    bootstrap_results: dict[str, Any],
) -> dict[str, Any]:
    checks = {
        "primary_denominator_36_each_condition": all(
            conditions[c]["unseen"]["n"] == 36 for c in ALL_CONDITIONS
        ),
        "physical_fault_clusters_12": all(
            b["n_physical_clusters"] == 12 for b in bootstrap_results.values()
        ),
        "local_fault_seen_denominator_12_each_condition": all(
            conditions[c]["local_fault_seen"]["n"] == 12 for c in ALL_CONDITIONS
        ),
        "normal_denominator_12_each_condition": all(
            conditions[c]["normal"]["n"] == 12 for c in ALL_CONDITIONS
        ),
        "overall_denominator_60_each_condition": all(
            conditions[c]["overall"]["n"] == 60 for c in ALL_CONDITIONS
        ),
        "transfer_total_36": all(
            t["helped"] + t["harmed"] + t["unchanged"] == 36
            for t in transfers.values()
        ),
        "confusion_aplus_total_60": sum(
            sum(predictions.values())
            for predictions in confusion_aplus.values()
        ) == 60,
        "per_agent_unseen_total_9": all(
            per_agent[agent]["n"] == 9 for agent in AGENTS
        ),
        "paired_rows_36": len(rows) == 36,
    }
    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise RuntimeError(f"internal consistency check failed: {failed}")
    return {"status": "PASS", **checks}


# ── main build ──────────────────────────────────────────────────────────

def build_results() -> tuple[dict[str, Any], dict[str, bytes]]:
    frozen_inputs = verify_frozen_inputs()
    config = load_json(CONFIG_PATH)
    case_truth, truth_integrity = load_case_truth(config)

    # Load both prediction sets
    abe_lookup = load_abe_aggregates(config, case_truth)
    aplus_lookup = load_aplus_aggregates(config, case_truth)

    # Merge into a single lookup
    lookup = {**abe_lookup, **aplus_lookup}

    # Compute metrics across all four conditions
    conditions = condition_metrics_all(lookup, case_truth, config)

    # Paired unseen rows with all four conditions
    rows = paired_unseen_rows_all(lookup, case_truth, config)
    if len(rows) != 36:
        raise RuntimeError("primary unseen subset must contain 36 rows")

    per_agent = per_agent_primary(rows)

    # Transfer counts for key comparisons
    transfers = {
        "Aplus_vs_A": transfer_counts_pair(rows, "A_correct", "Aplus_correct", "A+_vs_A_unseen"),
        "B_vs_Aplus": transfer_counts_pair(rows, "Aplus_correct", "B_correct", "B_vs_A+_unseen"),
        "E_vs_Aplus": transfer_counts_pair(rows, "Aplus_correct", "E_correct", "E_vs_A+_unseen"),
        "B_vs_A": transfer_counts_pair(rows, "A_correct", "B_correct", "B_vs_A_unseen"),
    }

    # A+ confusion matrix and recall
    recall_aplus, confusion_aplus = recall_and_confusion_aplus(lookup, case_truth, config)

    # Inter-repetition agreement for A+
    aplus_records = [
        aplus_lookup[(agent, case_id, "A+")]
        for agent in AGENTS
        for case_id in sorted(case_truth)
    ]
    agreement = inter_rep_agreement(aplus_records)

    # A+ execution metadata
    aplus_metadata = load_json(APLUS_METADATA_PATH)

    # Deltas
    acc = {c: conditions[c]["unseen"]["accuracy"] for c in ALL_CONDITIONS}
    delta_Aplus_A = acc["A+"] - acc["A"]
    delta_B_Aplus = acc["B"] - acc["A+"]
    delta_E_Aplus = acc["E"] - acc["A+"]
    delta_B_A = acc["B"] - acc["A"]
    delta_B_E = acc["B"] - acc["E"]

    # Bootstrap: three primary comparisons
    bootstrap_iters = int(config["metrics"]["bootstrap_iterations"])
    bootstrap_seed = int(config["metrics"]["bootstrap_seed"])

    bootstrap_Aplus_A = bootstrap_aplus(
        rows,
        delta_field="delta_Aplus_minus_A",
        definition="A+ minus A unseen accuracy delta",
        iterations=bootstrap_iters,
        seed=bootstrap_seed,
    )
    bootstrap_B_Aplus = bootstrap_aplus(
        rows,
        delta_field="delta_B_minus_Aplus",
        definition="B minus A+ unseen accuracy delta",
        iterations=bootstrap_iters,
        seed=bootstrap_seed,
    )
    bootstrap_E_Aplus = bootstrap_aplus(
        rows,
        delta_field="delta_E_minus_Aplus",
        definition="E minus A+ unseen accuracy delta",
        iterations=bootstrap_iters,
        seed=bootstrap_seed,
    )
    bootstrap_results = {
        "Aplus_minus_A": bootstrap_Aplus_A,
        "B_minus_Aplus": bootstrap_B_Aplus,
        "E_minus_Aplus": bootstrap_E_Aplus,
    }

    # Per-agent positive delta counts
    positive_Aplus_A = sum(
        per_agent[a]["delta_Aplus_minus_A"] > 0 for a in AGENTS
    )
    positive_B_Aplus = sum(
        per_agent[a]["delta_B_minus_Aplus"] > 0 for a in AGENTS
    )

    checks = integrity_checks(
        conditions, rows, per_agent, transfers, confusion_aplus, bootstrap_results
    )

    # Token summary
    token_summary = {
        "cumulative_input_tokens": aplus_metadata.get("cumulative_input_tokens"),
        "cumulative_output_tokens": aplus_metadata.get("cumulative_output_tokens"),
        "cumulative_total_tokens": aplus_metadata.get("cumulative_total_tokens"),
        "structural_retries_total": aplus_metadata.get("structural_retries_total"),
        "final_parse_failures": aplus_metadata.get("final_parse_failures"),
    }

    results = {
        "artifact_version": "1",
        "evaluation_status": "C01_FOUR_CONDITION_EVALUATION_COMPLETE",
        "description": "A+ (local-only self-insight) evaluation merged with frozen A/B/E results",
        "correction": "C01",
        "abstain_treatment": "incorrect",
        "ground_truth_join": truth_integrity,
        "condition_metrics": conditions,
        "primary_aplus": {
            "unit": "aggregate agent-case observation",
            "n_per_condition": 36,
            "physical_clusters": 12,
            "accuracy_A_unseen": acc["A"],
            "accuracy_Aplus_unseen": acc["A+"],
            "accuracy_B_unseen": acc["B"],
            "accuracy_E_unseen": acc["E"],
            "delta_Aplus_minus_A": delta_Aplus_A,
            "delta_B_minus_Aplus": delta_B_Aplus,
            "delta_E_minus_Aplus": delta_E_Aplus,
            "delta_B_minus_A": delta_B_A,
            "delta_B_minus_E": delta_B_E,
            "per_agent": per_agent,
            "positive_delta_Aplus_minus_A_agents": positive_Aplus_A,
            "positive_delta_B_minus_Aplus_agents": positive_B_Aplus,
            "transfer_Aplus_vs_A": transfers["Aplus_vs_A"],
            "transfer_B_vs_Aplus": transfers["B_vs_Aplus"],
            "transfer_E_vs_Aplus": transfers["E_vs_Aplus"],
            "transfer_B_vs_A": transfers["B_vs_A"],
        },
        "secondary": {
            "local_fault_seen_A": conditions["A"]["local_fault_seen"]["accuracy"],
            "local_fault_seen_Aplus": conditions["A+"]["local_fault_seen"]["accuracy"],
            "local_fault_seen_B": conditions["B"]["local_fault_seen"]["accuracy"],
            "local_fault_seen_E": conditions["E"]["local_fault_seen"]["accuracy"],
            "normal_A": conditions["A"]["normal"]["accuracy"],
            "normal_Aplus": conditions["A+"]["normal"]["accuracy"],
            "normal_B": conditions["B"]["normal"]["accuracy"],
            "normal_E": conditions["E"]["normal"]["accuracy"],
            "overall_A": conditions["A"]["overall"]["accuracy"],
            "overall_Aplus": conditions["A+"]["overall"]["accuracy"],
            "overall_B": conditions["B"]["overall"]["accuracy"],
            "overall_E": conditions["E"]["overall"]["accuracy"],
            "aplus_per_pseudolabel_recall": recall_aplus,
            "aplus_confusion_matrix": confusion_aplus,
        },
        "inter_repetition_agreement_aplus": agreement,
        "bootstrap": {
            "method": "paired physical_case_id cluster bootstrap stratified by true pseudolabel",
            "draws": bootstrap_iters,
            "seed": bootstrap_seed,
            "quantiles": [0.025, 0.975],
            "quantile_method": "numpy.quantile default linear",
            "Aplus_minus_A": bootstrap_Aplus_A,
            "B_minus_Aplus": bootstrap_B_Aplus,
            "E_minus_Aplus": bootstrap_E_Aplus,
        },
        "c01_criteria": {
            "A_unseen_is_zero": acc["A"] == 0.0,
            "Aplus_unseen_equals_A_if_no_remote_info": "expected" if delta_Aplus_A == 0.0 else "unexpected_nonzero",
            "B_gt_Aplus_unseen": acc["B"] > acc["A+"],
            "B_gt_E_unseen": acc["B"] > acc["E"],
            "Aplus_leq_B_confirms_peer_benefit": acc["A+"] <= acc["B"],
            "interpretation": (
                "A+ provides the self-insight control. If A+ ≈ A, self-insights alone "
                "do not help on unseen faults (as expected: the agent already knows its own class). "
                "If B >> A+ >> A, both self and peer insights help. "
                "If B >> A+ ≈ A, peer insights are the sole driver of transfer."
            ),
        },
        "token_summary_aplus": token_summary,
        "integrity_checks": checks,
        "reproducibility": {
            **frozen_inputs,
            "evaluator_code_sha256": sha256_file(Path(__file__)),
            "metrics_code_sha256": sha256_file(METRICS_CODE_PATH),
            "bootstrap_code_sha256": sha256_file(BOOTSTRAP_CODE_PATH),
            "mapping_sha256": sha256_file(MAPPING_PATH),
            "heldout_manifest_sha256": sha256_file(HELDOUT_MANIFEST_PATH),
            "bootstrap_draws": bootstrap_iters,
            "bootstrap_seed": bootstrap_seed,
        },
    }

    # ── output artifacts ──────────────────────────────────────────────
    # Primary CSV: four-condition unseen
    primary_rows = [
        {"condition": c, **conditions[c]["unseen"]}
        for c in ALL_CONDITIONS
    ]
    # Per-agent CSV
    agent_rows = [
        {"agent_id": a, **per_agent[a]} for a in AGENTS
    ]
    # Secondary CSV: all scopes × all conditions
    secondary_rows = [
        {"scope": scope, "condition": c, **conditions[c][scope]}
        for scope in ("local_fault_seen", "normal", "overall")
        for c in ALL_CONDITIONS
    ]
    # Transfer CSV
    transfer_rows = list(transfers.values())
    # Paired rows CSV
    paired_fieldnames = [
        "physical_case_id", "true_pseudolabel", "agent_id",
        "A_correct", "Aplus_correct", "B_correct", "E_correct",
        "delta_Aplus_minus_A", "delta_B_minus_Aplus", "delta_E_minus_Aplus",
        "delta_B_minus_A", "delta_B_minus_E",
    ]

    artifacts = {
        "aplus_evaluation_results.json": canonical_json_bytes(results),
        "aplus_primary_metrics.csv": csv_bytes(
            ["condition", "n", "correct", "accuracy", "abstentions", "abstention_rate"],
            primary_rows,
        ),
        "aplus_per_agent_metrics.csv": csv_bytes(
            [
                "agent_id", "n",
                "A_accuracy", "Aplus_accuracy", "B_accuracy", "E_accuracy",
                "delta_Aplus_minus_A", "delta_B_minus_Aplus", "delta_B_minus_A",
            ],
            agent_rows,
        ),
        "aplus_secondary_metrics.csv": csv_bytes(
            ["scope", "condition", "n", "correct", "accuracy", "abstentions", "abstention_rate"],
            secondary_rows,
        ),
        "aplus_transfer_counts.csv": csv_bytes(
            [
                "comparison", "n_pairs",
                "helped", "harmed", "unchanged",
                "unchanged_correct", "unchanged_incorrect",
            ],
            transfer_rows,
        ),
        "aplus_paired_rows.csv": csv_bytes(paired_fieldnames, rows),
        "aplus_confusion_matrix.json": canonical_json_bytes(
            {"aplus_confusion_matrix": confusion_aplus, "aplus_per_pseudolabel_recall": recall_aplus}
        ),
        "aplus_bootstrap_results.json": canonical_json_bytes(bootstrap_results),
    }
    artifacts["APLUS_EVALUATION_REPORT.md"] = render_report(results).encode("utf-8")
    return results, artifacts


# ── report ──────────────────────────────────────────────────────────────

def pct(value: float | None) -> str:
    if value is None:
        return "N/A"
    return f"{100.0 * value:.2f}%"


def criterion(value: bool) -> str:
    return "PASS" if value else "FAIL"


def render_report(results: dict[str, Any]) -> str:
    primary = results["primary_aplus"]
    conditions = results["condition_metrics"]
    bootstrap = results["bootstrap"]
    c01 = results["c01_criteria"]
    agreement = results["inter_repetition_agreement_aplus"]
    lines = [
        "# C01 — A+ (local-only self-insight) evaluation",
        "",
        "Four-condition comparison: A (no insights), A+ (self-insights only), "
        "B (peer insights), E (corrupted peer insights).",
        "",
        "Abstentions count as incorrect. Primary analysis uses only frozen R=3 "
        "aggregate outcomes.",
        "",
        "## Primary: locally unseen faults",
        "",
        "| Condition | Correct / n | Accuracy | Abstentions |",
        "|---|---:|---:|---:|",
    ]
    for c in ALL_CONDITIONS:
        v = conditions[c]["unseen"]
        lines.append(
            f"| {c} | {v['correct']} / {v['n']} | "
            f"{pct(v['accuracy'])} | {v['abstentions']} |"
        )
    lines.extend([
        "",
        "### Key deltas",
        "",
        f"- Delta A+−A (self-insight effect): {primary['delta_Aplus_minus_A']:.12g}",
        f"- Delta B−A+ (peer benefit over local): {primary['delta_B_minus_Aplus']:.12g}",
        f"- Delta E−A+ (corrupted vs local): {primary['delta_E_minus_Aplus']:.12g}",
        f"- Delta B−A (total FoT effect): {primary['delta_B_minus_A']:.12g}",
        f"- Delta B−E (specificity): {primary['delta_B_minus_E']:.12g}",
        "",
        "### Per-agent primary (unseen faults)",
        "",
        "| Agent | n | A | A+ | B | E | Δ(A+−A) | Δ(B−A+) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ])
    for agent in AGENTS:
        v = primary["per_agent"][agent]
        lines.append(
            f"| {agent} | {v['n']} | {pct(v['A_accuracy'])} | "
            f"{pct(v['Aplus_accuracy'])} | {pct(v['B_accuracy'])} | "
            f"{pct(v['E_accuracy'])} | {v['delta_Aplus_minus_A']:.12g} | "
            f"{v['delta_B_minus_Aplus']:.12g} |"
        )
    lines.extend([
        "",
        "### Paired transfers (unseen, n=36)",
        "",
        "| Comparison | Helped | Harmed | Unchanged (correct/incorrect) |",
        "|---|---:|---:|---|",
    ])
    for key in ("Aplus_vs_A", "B_vs_Aplus", "E_vs_Aplus", "B_vs_A"):
        t = primary[f"transfer_{key}"]
        lines.append(
            f"| {t['comparison']} | {t['helped']} | {t['harmed']} | "
            f"{t['unchanged']} ({t['unchanged_correct']}/{t['unchanged_incorrect']}) |"
        )
    lines.extend([
        "",
        "### Inter-repetition agreement (A+)",
        "",
        f"- Unanimous 3/3: {agreement['unanimous_3_of_3']} / {agreement['total_aggregates']}",
        f"- Majority 2/3: {agreement['majority_2_of_3']} / {agreement['total_aggregates']}",
        f"- All different: {agreement['all_different']} / {agreement['total_aggregates']}",
        f"- Unanimity rate: {pct(agreement['unanimity_rate'])}",
        "",
        "### Bootstrap confidence intervals",
        "",
        f"- Draws: {bootstrap['draws']}; seed: {bootstrap['seed']}",
        f"- Delta A+−A 95% CI: [{bootstrap['Aplus_minus_A']['ci_lower']:.12g}, "
        f"{bootstrap['Aplus_minus_A']['ci_upper']:.12g}]",
        f"- Delta B−A+ 95% CI: [{bootstrap['B_minus_Aplus']['ci_lower']:.12g}, "
        f"{bootstrap['B_minus_Aplus']['ci_upper']:.12g}]",
        f"- Delta E−A+ 95% CI: [{bootstrap['E_minus_Aplus']['ci_lower']:.12g}, "
        f"{bootstrap['E_minus_Aplus']['ci_upper']:.12g}]",
        "",
        "## C01 interpretation criteria",
        "",
        f"- A unseen = 0%: {c01['A_unseen_is_zero']}",
        f"- A+ unseen ≈ A (self-insights alone insufficient): {c01['Aplus_unseen_equals_A_if_no_remote_info']}",
        f"- B > A+ (peer insights help beyond self): {criterion(c01['B_gt_Aplus_unseen'])}",
        f"- B > E (correct peers beat corrupted): {criterion(c01['B_gt_E_unseen'])}",
        f"- A+ ≤ B (peer benefit confirmed): {criterion(c01['Aplus_leq_B_confirms_peer_benefit'])}",
        "",
        f"> {c01['interpretation']}",
        "",
        "## Secondary outcomes",
        "",
    ])
    for scope, title in [
        ("local_fault_seen", "Local fault seen"),
        ("normal", "Normal"),
        ("overall", "Overall"),
    ]:
        lines.extend([
            f"### {title}",
            "",
            "| Condition | Correct / n | Accuracy | Abstention rate |",
            "|---|---:|---:|---:|",
        ])
        for c in ALL_CONDITIONS:
            v = conditions[c][scope]
            lines.append(
                f"| {c} | {v['correct']} / {v['n']} | "
                f"{pct(v['accuracy'])} | {pct(v['abstention_rate'])} |"
            )
        lines.append("")

    lines.extend([
        "A+ confusion matrix and per-pseudolabel recall are preserved in "
        "`aplus_confusion_matrix.json`.",
        "",
        "## Token usage (A+ inference only)",
        "",
    ])
    ts = results["token_summary_aplus"]
    if ts.get("cumulative_total_tokens") is not None:
        lines.extend([
            f"- Input tokens: {ts['cumulative_input_tokens']:,}",
            f"- Output tokens: {ts['cumulative_output_tokens']:,}",
            f"- Total tokens: {ts['cumulative_total_tokens']:,}",
            f"- Structural retries: {ts['structural_retries_total']}",
            f"- Final parse failures: {ts['final_parse_failures']}",
        ])
    else:
        lines.append("- Token data not yet available (inference pending)")
    lines.extend([
        "",
        "## Integrity and reproducibility",
        "",
        "- Ground-truth join: 15/15 physical cases, unique.",
        "- Primary denominator: 36 aggregate agent-case observations per condition.",
        "- Independent physical fault clusters: 12.",
        "- Local-fault-seen denominator: 12 per condition.",
        "- Normal denominator: 12 per condition.",
        "- Overall denominator: 60 per condition.",
        f"- All internal consistency checks: {results['integrity_checks']['status']}.",
        "- A/B/E frozen results: verified untouched.",
        "- A+ frozen inputs: verified against APLUS_FREEZE_MANIFEST.json.",
        "",
    ])
    return "\n".join(lines)


# ── entry point ─────────────────────────────────────────────────────────

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
        "status": "C01_EVALUATION_COMPLETE",
        "condition": "A+",
        "correction": "C01",
        "primary_prediction_sources": {
            "abe": str(ABE_AGGREGATE_PATH.relative_to(ROOT)),
            "aplus": str(APLUS_AGGREGATE_PATH.relative_to(ROOT)),
        },
        "abe_evaluation_results_sha256": sha256_file(ABE_RESULTS_PATH),
        "aplus_aggregate_sha256": sha256_file(APLUS_AGGREGATE_PATH),
        "evaluator_code_sha256": sha256_file(Path(__file__)),
        "evaluation_artifacts": relative_artifacts,
    }
    write_if_identical_or_absent(
        output_dir / "aplus_evaluation_hash_manifest.json",
        canonical_json_bytes(hash_manifest),
    )
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    results = evaluate(args.output_dir.resolve())
    primary = results["primary_aplus"]
    print(
        json.dumps(
            {
                "status": "COMPLETE",
                "correction": "C01",
                "conditions": list(ALL_CONDITIONS),
                "primary_n_per_condition": primary["n_per_condition"],
                "physical_clusters": primary["physical_clusters"],
                "accuracy_A_unseen": primary["accuracy_A_unseen"],
                "accuracy_Aplus_unseen": primary["accuracy_Aplus_unseen"],
                "accuracy_B_unseen": primary["accuracy_B_unseen"],
                "accuracy_E_unseen": primary["accuracy_E_unseen"],
                "delta_Aplus_minus_A": primary["delta_Aplus_minus_A"],
                "delta_B_minus_Aplus": primary["delta_B_minus_Aplus"],
                "integrity": results["integrity_checks"]["status"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
