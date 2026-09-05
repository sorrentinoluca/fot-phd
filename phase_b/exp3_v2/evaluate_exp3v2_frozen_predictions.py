#!/usr/bin/env python3
"""Confirmatory-only offline evaluator for frozen EXP3_V2 aggregates.

The production CLI is intentionally unusable until its harness manifest is
frozen and reachable through the approved annotated tag.  Pure functions are
exposed so synthetic fixtures can exercise the complete statistical contract
without opening any EXP3_V2 prediction.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any, Iterable

import jsonschema
import numpy as np


HERE = Path(__file__).resolve().parent
SCHEMA_DIR = HERE / "evaluation_schemas"
HARNESS_TAG = "exp3-v2-evaluation-harness-frozen-002"
HARNESS_SCHEMA = "exp3v2_evaluation_harness_manifest_002.schema.json"
FROZEN_STATUS = "HARNESS_FROZEN_BEFORE_EVALUATION"
AGENTS = ("agent_1", "agent_2", "agent_3", "agent_4")
CONDITIONS = ("A", "B", "E")
LABELS = ("CLS-ZOGAA", "CLS-OJNSG", "CLS-R463B", "CLS-Z3ISU", "Normal")
EXPECTED_RUNTIME = {
    "python": "3.13.9",
    "numpy": "2.5.2",
    "jsonschema": "4.25.0",
}


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


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


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
    if not lines or any(not line.strip() for line in lines):
        raise RuntimeError(f"invalid blank or empty JSONL: {path}")
    return [json.loads(line) for line in lines]


def validate_schema(value: Any, name: str) -> None:
    schema = load_json(SCHEMA_DIR / name)
    jsonschema.Draft202012Validator(schema).validate(value)


def git_value(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()


def verify_clean_detached_tag(
    root: Path,
    *,
    tag: str,
    tag_object: str | None = None,
    peeled_commit: str | None = None,
) -> str:
    if not root.is_dir() or root.is_symlink():
        raise RuntimeError(f"checkout missing or symlinked: {root}")
    if (
        subprocess.run(
            ["git", "-C", str(root), "symbolic-ref", "-q", "HEAD"],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        ).returncode
        == 0
    ):
        raise RuntimeError(f"checkout is not detached: {root}")
    if git_value(root, "status", "--porcelain=v1", "--untracked-files=all"):
        raise RuntimeError(f"checkout is not clean: {root}")
    observed_object = git_value(root, "rev-parse", f"refs/tags/{tag}")
    observed_commit = git_value(root, "rev-parse", f"refs/tags/{tag}^{{}}")
    if git_value(root, "rev-parse", "HEAD") != observed_commit:
        raise RuntimeError(f"checkout HEAD does not equal annotated tag target: {tag}")
    if tag_object is not None and observed_object != tag_object:
        raise RuntimeError(f"annotated tag object mismatch: {tag}")
    if peeled_commit is not None and observed_commit != peeled_commit:
        raise RuntimeError(f"annotated tag target mismatch: {tag}")
    return observed_commit


def verify_runtime() -> None:
    observed_python = ".".join(str(item) for item in sys.version_info[:3])
    observed = {
        "python": observed_python,
        "numpy": importlib.metadata.version("numpy"),
        "jsonschema": importlib.metadata.version("jsonschema"),
    }
    if observed != EXPECTED_RUNTIME:
        raise RuntimeError(f"evaluation runtime mismatch: {observed}")


def verify_file(path: Path, binding: dict[str, Any]) -> None:
    if path.is_symlink() or not path.is_file():
        raise RuntimeError(f"missing or symlinked input: {path}")
    if path.stat().st_size != binding["size_bytes"]:
        raise RuntimeError(f"input size mismatch: {path}")
    if sha256_file(path) != binding["sha256"]:
        raise RuntimeError(f"input hash mismatch: {path}")


def validate_harness_boundary(manifest_path: Path) -> tuple[dict[str, Any], Path]:
    harness_root = manifest_path.resolve().parents[2]
    manifest = load_json(manifest_path)
    validate_schema(manifest, HARNESS_SCHEMA)
    if manifest["status"] != FROZEN_STATUS or manifest["tag_created"] is not True:
        raise RuntimeError("evaluation harness is not frozen")
    if manifest["prospective_tag"] != HARNESS_TAG:
        raise RuntimeError("evaluation harness tag identity mismatch")
    verify_clean_detached_tag(harness_root, tag=HARNESS_TAG)
    tracked = git_value(
        harness_root, "ls-tree", "-r", "--name-only", "HEAD"
    ).splitlines()
    for binding in manifest["harness_artifacts"]:
        if binding["path"] not in tracked:
            raise RuntimeError(f"harness artifact is not tracked: {binding['path']}")
        verify_file(harness_root / binding["path"], binding)
    config_path = harness_root / "phase_b/exp3_v2/EXP3_V2_EVALUATION_CONFIG_001.json"
    config = load_json(config_path)
    validate_schema(config, "exp3v2_evaluation_config.schema.json")
    if (
        config["status"] != "FROZEN_BEFORE_EVALUATION"
        or config["optional_analyses"] != []
    ):
        raise RuntimeError(
            "confirmatory evaluation configuration is not frozen and minimal"
        )
    return manifest, harness_root


def validate_upstream_checkouts(
    manifest: dict[str, Any], roots: dict[str, Path]
) -> None:
    bindings = {item["role"]: item for item in manifest["upstream_tags"]}
    if set(bindings) != set(roots):
        raise RuntimeError("upstream checkout role set mismatch")
    for role, root in roots.items():
        item = bindings[role]
        verify_clean_detached_tag(
            root,
            tag=item["tag"],
            tag_object=item["tag_object"],
            peeled_commit=item["peeled_commit"],
        )
        boundary_manifest = root / item["manifest_path"]
        if boundary_manifest.is_symlink() or not boundary_manifest.is_file():
            raise RuntimeError(f"upstream manifest missing or symlinked: {role}")
        if sha256_file(boundary_manifest) != item["manifest_sha256"]:
            raise RuntimeError(f"upstream manifest hash mismatch: {role}")


def canonical_case_ids() -> list[str]:
    return [
        *[f"EXP3V2-N-{index:03d}" for index in range(1, 7)],
        *[f"EXP3V2-F1-{index:03d}" for index in range(1, 7)],
        *[f"EXP3V2-F8-{index:03d}" for index in range(1, 7)],
        *[f"EXP3V2-F10-{index:03d}" for index in range(1, 7)],
        *[f"EXP3V2-F13-{index:03d}" for index in range(1, 7)],
    ]


def validate_case_sources(
    case_plan: dict[str, Any],
    data_rows: list[dict[str, str]],
    mapping: dict[str, Any],
) -> dict[str, str]:
    expected_ids = canonical_case_ids()
    cases = case_plan.get("cases")
    if (
        not isinstance(cases, list)
        or [item.get("physical_case_id") for item in cases] != expected_ids
    ):
        raise RuntimeError("case plan is not in exact canonical order")
    if [row.get("physical_case_id") for row in data_rows] != expected_ids:
        raise RuntimeError("data manifest is not in exact canonical order")
    if any(row.get("attempt") != "0" for row in data_rows):
        raise RuntimeError("evaluation requires exactly attempt 0 for all cases")
    real_to_opaque = mapping.get("real_to_opaque")
    if (
        real_to_opaque
        != {
            "F1": "CLS-ZOGAA",
            "F8": "CLS-OJNSG",
            "F10": "CLS-R463B",
            "F13": "CLS-Z3ISU",
        }
        or mapping.get("normal_label") != "Normal"
    ):
        raise RuntimeError("evaluator-side pseudolabel mapping mismatch")
    truth: dict[str, str] = {}
    counts: Counter[str] = Counter()
    for case, row in zip(cases, data_rows, strict=True):
        condition = case.get("condition")
        if row.get("fault/status") != condition:
            raise RuntimeError("case plan and data manifest condition mismatch")
        expected_seed = 320001 + len(truth)
        if case.get("primary_seed") != expected_seed or row.get("seed") != str(
            expected_seed
        ):
            raise RuntimeError("case plan and data manifest seed mismatch")
        counts[condition] += 1
        truth[case["physical_case_id"]] = (
            "Normal" if condition == "Normal" else real_to_opaque[condition]
        )
    if counts != Counter({"Normal": 6, "F1": 6, "F8": 6, "F10": 6, "F13": 6}):
        raise RuntimeError("case condition counts mismatch")
    return truth


def expected_aggregate_keys() -> list[tuple[str, str, str]]:
    return [
        (case_id, agent_id, condition)
        for case_id in canonical_case_ids()
        for agent_id in AGENTS
        for condition in CONDITIONS
    ]


def normalized_prediction(parsed: dict[str, Any]) -> str | None:
    if set(parsed) != {
        "predicted_label",
        "abstain",
        "used_insight_ids",
        "reasoning_summary",
    }:
        raise RuntimeError("aggregate prediction schema mismatch")
    if type(parsed["abstain"]) is not bool:
        raise RuntimeError("aggregate abstain is not boolean")
    prediction = parsed["predicted_label"]
    if parsed["abstain"]:
        if prediction is not None:
            raise RuntimeError("abstention requires null predicted label")
        return None
    if prediction not in LABELS:
        raise RuntimeError("aggregate prediction is outside frozen label space")
    return prediction


def validate_aggregates(
    records: list[dict[str, Any]],
) -> dict[tuple[str, str, str], dict[str, Any]]:
    if len(records) != 360:
        raise RuntimeError("exactly 360 aggregate records are required")
    observed_keys: list[tuple[str, str, str]] = []
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
            raise RuntimeError("aggregate record fields mismatch")
        key = (record["physical_case_id"], record["agent_id"], record["condition"])
        if key in lookup:
            raise RuntimeError("duplicate aggregate key")
        if (
            record["aggregation_rule"]
            != "frozen_valid_label_majority_2_of_3_else_abstain"
        ):
            raise RuntimeError("aggregate rule mismatch")
        outcomes = record["repetition_outcomes"]
        if not isinstance(outcomes, list) or [
            item.get("repetition") for item in outcomes
        ] != [1, 2, 3]:
            raise RuntimeError("aggregate requires ordered repetitions 1,2,3")
        votes: Counter[str] = Counter()
        for outcome in outcomes:
            if set(outcome) != {
                "repetition",
                "predicted_label",
                "abstain",
                "parse_failure",
            }:
                raise RuntimeError("repetition outcome fields mismatch")
            if (
                type(outcome["abstain"]) is not bool
                or type(outcome["parse_failure"]) is not bool
            ):
                raise RuntimeError("repetition outcome boolean mismatch")
            label = outcome["predicted_label"]
            if outcome["abstain"]:
                if label is not None:
                    raise RuntimeError("abstaining repetition requires null label")
            elif label not in LABELS:
                raise RuntimeError("repetition prediction outside frozen label space")
            else:
                votes[label] += 1
        winners = [label for label, count in votes.items() if count >= 2]
        expected = winners[0] if len(winners) == 1 else None
        observed = normalized_prediction(record["parsed_output"])
        if observed != expected:
            raise RuntimeError("aggregate does not reproduce frozen majority rule")
        observed_keys.append(key)
        lookup[key] = record
    if observed_keys != expected_aggregate_keys():
        raise RuntimeError("aggregate order or coverage mismatch")
    return lookup


def is_correct(record: dict[str, Any], truth: str) -> int:
    return int(normalized_prediction(record["parsed_output"]) == truth)


def population_rows(
    lookup: dict[tuple[str, str, str], dict[str, Any]],
    truth: dict[str, str],
    local_labels: dict[str, str],
) -> dict[str, list[dict[str, Any]]]:
    if set(truth) != set(canonical_case_ids()) or Counter(truth.values()) != Counter(
        {
            "Normal": 6,
            "CLS-ZOGAA": 6,
            "CLS-OJNSG": 6,
            "CLS-R463B": 6,
            "CLS-Z3ISU": 6,
        }
    ):
        raise RuntimeError("truth population is incomplete or incorrectly partitioned")
    if set(local_labels) != set(AGENTS):
        raise RuntimeError("local-label mapping must contain exactly four agents")
    fault_labels = set(LABELS) - {"Normal"}
    if set(local_labels.values()) != fault_labels:
        raise RuntimeError("local-label mapping must bijectively cover four faults")
    populations: dict[str, list[dict[str, Any]]] = {
        "unseen": [],
        "local_seen": [],
        "normal": [],
        "overall": [],
    }
    for case_id in canonical_case_ids():
        true_label = truth[case_id]
        for agent_id in AGENTS:
            row: dict[str, Any] = {
                "physical_case_id": case_id,
                "true_pseudolabel": true_label,
                "agent_id": agent_id,
            }
            for condition in CONDITIONS:
                prediction = normalized_prediction(
                    lookup[(case_id, agent_id, condition)]["parsed_output"]
                )
                row[f"{condition}_prediction"] = prediction
                row[f"{condition}_correct"] = int(prediction == true_label)
                row[f"{condition}_abstain"] = int(prediction is None)
            if true_label == "Normal":
                population = "normal"
            elif local_labels[agent_id] == true_label:
                population = "local_seen"
            else:
                population = "unseen"
            populations[population].append(row)
            populations["overall"].append(row)

    expected_sizes = {"unseen": 72, "local_seen": 24, "normal": 24, "overall": 120}
    if {name: len(rows) for name, rows in populations.items()} != expected_sizes:
        raise RuntimeError(
            "evaluation population denominators do not match 72/24/24/120"
        )
    keys = {
        name: {(row["physical_case_id"], row["agent_id"]) for row in rows}
        for name, rows in populations.items()
    }
    if any(len(keys[name]) != expected_sizes[name] for name in expected_sizes):
        raise RuntimeError("evaluation population contains duplicate agent-case rows")
    if (
        keys["unseen"] & keys["local_seen"]
        or keys["unseen"] & keys["normal"]
        or keys["local_seen"] & keys["normal"]
    ):
        raise RuntimeError("evaluation populations overlap")
    if keys["unseen"] | keys["local_seen"] | keys["normal"] != keys["overall"]:
        raise RuntimeError("evaluation populations are incomplete")

    rows = populations["unseen"]
    if len(rows) != 72:
        raise RuntimeError("primary population must contain 72 agent-case rows")
    counts = Counter(item["physical_case_id"] for item in rows)
    if set(counts.values()) != {3} or len(counts) != 24:
        raise RuntimeError("primary rows must retain three agents per fault case")
    strata: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        strata[row["true_pseudolabel"]].add(row["physical_case_id"])
    if len(strata) != 4 or {len(value) for value in strata.values()} != {6}:
        raise RuntimeError("primary rows require four strata of six physical cases")
    return populations


def primary_rows(
    lookup: dict[tuple[str, str, str], dict[str, Any]],
    truth: dict[str, str],
    local_labels: dict[str, str],
) -> list[dict[str, Any]]:
    return population_rows(lookup, truth, local_labels)["unseen"]


def summarize_conditions(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    denominator = len(rows)
    if denominator not in {24, 72, 120}:
        raise RuntimeError("unsupported evaluation population denominator")
    for condition in CONDITIONS:
        correct = sum(row[f"{condition}_correct"] for row in rows)
        abstentions = sum(row[f"{condition}_abstain"] for row in rows)
        incorrect = denominator - correct
        if (
            incorrect < 0
            or abstentions > incorrect
            or correct + incorrect != denominator
        ):
            raise RuntimeError("condition outcome counts do not cover denominator")
        result[condition] = {
            "n": denominator,
            "correct": correct,
            "incorrect": incorrect,
            "abstentions": abstentions,
            "accuracy": correct / denominator,
        }
    return result


def bootstrap_confirmatory(
    rows: list[dict[str, Any]], *, draws: int = 10000, seed: int = 320031
) -> dict[str, Any]:
    if draws != 10000 or seed != 320031:
        raise RuntimeError("bootstrap settings differ from the frozen EXP3_V2 contract")
    by_label: dict[str, list[str]] = defaultdict(list)
    by_case: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        case_id = row["physical_case_id"]
        by_case[case_id].append(row)
        if case_id not in by_label[row["true_pseudolabel"]]:
            by_label[row["true_pseudolabel"]].append(case_id)
    if len(by_label) != 4 or {len(value) for value in by_label.values()} != {6}:
        raise RuntimeError("bootstrap strata mismatch")
    rng = np.random.default_rng(seed)
    b_minus_a = np.empty(draws, dtype=float)
    b_minus_e = np.empty(draws, dtype=float)
    for index in range(draws):
        sample: list[dict[str, Any]] = []
        for label in sorted(by_label):
            cases = sorted(by_label[label])
            for case_id in rng.choice(cases, size=6, replace=True).tolist():
                sample.extend(by_case[case_id])
        if len(sample) != 72:
            raise RuntimeError("bootstrap draw lost clustered agent rows")
        b_minus_a[index] = np.mean(
            [row["B_correct"] - row["A_correct"] for row in sample]
        )
        b_minus_e[index] = np.mean(
            [row["B_correct"] - row["E_correct"] for row in sample]
        )

    def summary(values: np.ndarray, point: float) -> dict[str, Any]:
        return {
            "point_estimate": point,
            "confidence_level": 0.95,
            "ci_lower": float(np.quantile(values, 0.025)),
            "ci_upper": float(np.quantile(values, 0.975)),
            "distribution": [float(value) for value in values],
        }

    point_ba = float(np.mean([row["B_correct"] - row["A_correct"] for row in rows]))
    point_be = float(np.mean([row["B_correct"] - row["E_correct"] for row in rows]))
    result = {
        "method": "paired physical_case_id cluster bootstrap stratified by true pseudolabel",
        "draws": draws,
        "seed": seed,
        "quantiles": [0.025, 0.975],
        "quantile_method": "numpy.quantile default linear",
        "n_physical_clusters": 24,
        "n_agent_case_rows": 72,
        "clusters_per_pseudolabel": 6,
        "rows_per_physical_cluster": 3,
        "paired_conditions": True,
        "B_minus_A": summary(b_minus_a, point_ba),
        "B_minus_E": summary(b_minus_e, point_be),
    }
    validate_schema(result, "exp3v2_evaluation_bootstrap.schema.json")
    return result


def confirmatory_bundle(
    aggregates: list[dict[str, Any]],
    truth: dict[str, str],
    *,
    aggregate_sha256: str,
    local_labels: dict[str, str] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    local = local_labels or {
        "agent_1": "CLS-ZOGAA",
        "agent_2": "CLS-OJNSG",
        "agent_3": "CLS-R463B",
        "agent_4": "CLS-Z3ISU",
    }
    lookup = validate_aggregates(aggregates)
    populations = population_rows(lookup, truth, local)
    by_population = {
        name: summarize_conditions(rows) for name, rows in populations.items()
    }
    condition_metrics = {
        condition: {
            population: by_population[population][condition]
            for population in ("unseen", "local_seen", "normal", "overall")
        }
        for condition in CONDITIONS
    }
    bootstrap = bootstrap_confirmatory(populations["unseen"])
    delta_ba = (
        condition_metrics["B"]["unseen"]["accuracy"]
        - condition_metrics["A"]["unseen"]["accuracy"]
    )
    delta_be = (
        condition_metrics["B"]["unseen"]["accuracy"]
        - condition_metrics["E"]["unseen"]["accuracy"]
    )
    if delta_ba != bootstrap["B_minus_A"]["point_estimate"]:
        raise RuntimeError("B-A point estimate mismatch")
    if delta_be != bootstrap["B_minus_E"]["point_estimate"]:
        raise RuntimeError("B-E point estimate mismatch")
    results = {
        "schema_version": "1.0",
        "status": "CONFIRMATORY_EVALUATION_COMPLETE_PENDING_RESULTS_FREEZE",
        "analysis_population": "EXP3_V2_MINIMAL_CONFIRMATORY_PRIMARY_AND_DESCRIPTIVE_POPULATIONS",
        "prediction_source": "FROZEN_R3_AGGREGATES_ONLY",
        "aggregate_records_total": 360,
        "primary_agent_case_rows_per_condition": 72,
        "secondary_agent_case_rows_per_condition": {
            "local_seen": 24,
            "normal": 24,
            "overall": 120,
        },
        "physical_fault_clusters": 24,
        "condition_metrics": condition_metrics,
        "contrasts": {"B_minus_A": delta_ba, "B_minus_E": delta_be},
        "success_criteria": {
            "replication_supported": delta_ba > 0
            and bootstrap["B_minus_A"]["ci_lower"] > 0,
            "requires_observed_B_minus_A_gt_0": True,
            "requires_B_minus_A_ci_lower_gt_0": True,
            "semantic_specificity_supported": delta_be > 0,
            "semantic_specificity_ci_is_not_a_gate": True,
        },
        "abstention_treatment": "incorrect",
        "multiplicity_adjustment": "none_single_primary_contrast",
        "optional_analyses_included": [],
        "input_aggregate_sha256": aggregate_sha256,
        "bootstrap_artifact": "exp3v2_confirmatory_bootstrap.json",
    }
    validate_schema(results, "exp3v2_evaluation_results.schema.json")
    return results, bootstrap


def output_manifest(result_bytes: bytes, bootstrap_bytes: bytes) -> dict[str, Any]:
    artifacts = [
        {
            "path": "exp3v2_confirmatory_bootstrap.json",
            "size_bytes": len(bootstrap_bytes),
            "sha256": sha256_bytes(bootstrap_bytes),
        },
        {
            "path": "exp3v2_confirmatory_results.json",
            "size_bytes": len(result_bytes),
            "sha256": sha256_bytes(result_bytes),
        },
    ]
    inventory = "".join(
        f"{item['path']}\0{item['size_bytes']}\0{item['sha256']}\n"
        for item in artifacts
    ).encode("utf-8")
    value = {
        "schema_version": "1.0",
        "status": "COMPLETE_PENDING_RESULTS_FREEZE",
        "artifact_count": 2,
        "artifacts": artifacts,
        "inventory_sha256": sha256_bytes(inventory),
        "optional_analyses_included": [],
    }
    validate_schema(value, "exp3v2_evaluation_output_hash_manifest.schema.json")
    return value


def atomic_write_new(path: Path, content: bytes) -> None:
    if path.exists() or path.is_symlink():
        raise RuntimeError(f"refusing to overwrite evaluation output: {path}")
    temporary = path.with_name(path.name + ".tmp")
    if temporary.exists() or temporary.is_symlink():
        raise RuntimeError(f"temporary output already exists: {temporary}")
    with temporary.open("xb") as stream:
        stream.write(content)
        stream.flush()
        os.fsync(stream.fileno())
    temporary.replace(path)


def reserve_output_root(requested: Path, manifest: dict[str, Any]) -> Path:
    authorized_text = manifest.get("future_execution", {}).get("output_root")
    if (
        not isinstance(authorized_text, str)
        or not requested.is_absolute()
        or str(requested) != authorized_text
    ):
        raise RuntimeError("evaluation output path differs from frozen authorization")

    output_root = requested
    parent = output_root.parent
    if parent.is_symlink():
        raise RuntimeError("evaluation output parent is a symlink")
    if parent.exists():
        if not parent.is_dir():
            raise RuntimeError("evaluation output parent is not a directory")
    else:
        parent_parent = parent.parent
        if parent_parent.is_symlink() or not parent_parent.is_dir():
            raise RuntimeError("dedicated evaluation output parent cannot be created")
        try:
            parent.mkdir(mode=0o700, parents=False, exist_ok=False)
        except FileExistsError as error:
            raise RuntimeError(
                "evaluation output parent appeared concurrently"
            ) from error
        if parent.is_symlink() or not parent.is_dir():
            raise RuntimeError("created evaluation output parent is invalid")

    if output_root.exists() or output_root.is_symlink():
        raise RuntimeError("evaluation output root must not exist")
    try:
        output_root.mkdir(mode=0o700, parents=False, exist_ok=False)
    except FileExistsError as error:
        raise RuntimeError("evaluation output root already exists") from error
    if output_root.is_symlink() or not output_root.is_dir():
        raise RuntimeError("reserved evaluation output root is invalid")
    return output_root


def run(args: argparse.Namespace) -> dict[str, Any]:
    manifest_path = args.harness_manifest.resolve()
    manifest, _ = validate_harness_boundary(manifest_path)
    roots = {
        "source": args.source_root.resolve(),
        "data": args.data_root.resolve(),
        "verbalization_harness": args.verbalization_harness_root.resolve(),
        "verbalizations": args.verbalizations_root.resolve(),
        "inference_harness": args.inference_harness_root.resolve(),
        "execution_authorization": args.authorization_root.resolve(),
        "inference_outputs": args.inference_root.resolve(),
    }
    validate_upstream_checkouts(manifest, roots)
    verify_runtime()
    output_root = reserve_output_root(args.output_root, manifest)

    inputs = manifest["inputs"]
    source = roots["source"]
    data = roots["data"]
    inference = roots["inference_outputs"]
    case_plan_path = source / inputs["case_plan"]["path"]
    mapping_path = source / inputs["pseudolabel_mapping"]["path"]
    data_manifest_path = data / inputs["data_manifest"]["path"]
    aggregate_path = inference / inputs["aggregate_records"]["path"]
    for path, binding in (
        (case_plan_path, inputs["case_plan"]),
        (mapping_path, inputs["pseudolabel_mapping"]),
        (data_manifest_path, inputs["data_manifest"]),
        (aggregate_path, inputs["aggregate_records"]),
    ):
        verify_file(path, binding)

    with data_manifest_path.open(encoding="utf-8", newline="") as stream:
        data_rows = list(csv.DictReader(stream))
    truth = validate_case_sources(
        load_json(case_plan_path), data_rows, load_json(mapping_path)
    )
    aggregates = load_jsonl(aggregate_path)
    results, bootstrap = confirmatory_bundle(
        aggregates,
        truth,
        aggregate_sha256=inputs["aggregate_records"]["sha256"],
    )
    result_bytes = canonical_json_bytes(results)
    bootstrap_bytes = canonical_json_bytes(bootstrap)
    manifest_bytes = canonical_json_bytes(
        output_manifest(result_bytes, bootstrap_bytes)
    )
    try:
        atomic_write_new(
            output_root / "exp3v2_confirmatory_bootstrap.json", bootstrap_bytes
        )
        atomic_write_new(output_root / "exp3v2_confirmatory_results.json", result_bytes)
        atomic_write_new(
            output_root / "exp3v2_evaluation_output_hash_manifest.json", manifest_bytes
        )
    except Exception:
        raise RuntimeError(
            "evaluation output write failed; retain root for forensic review"
        )
    return {"status": "PASS", "output_files": 3, "aggregate_source_only": True}


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--harness-manifest", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--verbalization-harness-root", type=Path, required=True)
    parser.add_argument("--verbalizations-root", type=Path, required=True)
    parser.add_argument("--inference-harness-root", type=Path, required=True)
    parser.add_argument("--authorization-root", type=Path, required=True)
    parser.add_argument("--inference-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    result = run(parse_args(argv))
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
