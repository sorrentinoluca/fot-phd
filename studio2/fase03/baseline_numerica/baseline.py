#!/usr/bin/env python3
"""Build and evaluate the frozen 697-D nearest-prototype baseline."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable


DIMENSIONS = 697
TIE_TOLERANCE = 1e-12
EXPECTED_FAULT_MANIFEST_SHA256 = (
    "5111d0c61c2e93fe5071d7a85015673549af0bf9c1dc74e0d940719a8400e020"
)
EXPECTED_BASELINE_SHA256 = (
    "79883dd0aabbd034c15337b0be1ffca37e59ea7b32443a15d560b7feda2b2e6a"
)
EXPECTED_R2_GUARD_SHA256 = (
    "7df0cef2d7854c689b79eb911fa01d1ede1625e22f0d3636c0ea5d678c9f33f8"
)
F_NUMBER = re.compile(rb"(?<![A-Za-z0-9_])F(?:1|2|3|8|10|13|14|15)(?![A-Za-z0-9_])")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
        + "\n"
    ).encode("utf-8")


def csv_bytes(rows: Iterable[dict[str, Any]], fields: list[str]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def write_once(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != content:
            raise RuntimeError(f"refusing to overwrite different output: {path}")
        return
    path.write_bytes(content)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def load_signature(path: Path, expected_sha256: str) -> tuple[float, ...]:
    if sha256_file(path) != expected_sha256:
        raise RuntimeError(f"signature hash mismatch: {path}")
    rows = read_csv(path)
    if len(rows) != DIMENSIONS:
        raise RuntimeError(f"expected {DIMENSIONS} signature rows: {path}")
    vector: list[float] = []
    for index, row in enumerate(rows):
        if int(row["component"]) != index:
            raise RuntimeError(f"non-canonical signature component order: {path}")
        value = float(row["value"])
        if not math.isfinite(value) or not 0.0 <= value <= 1.0:
            raise RuntimeError(f"invalid signature component: {path}")
        vector.append(value)
    return tuple(vector)


def load_evidence(
    root: Path,
    *,
    expected_manifest_sha256: str | None,
) -> tuple[dict[str, tuple[float, ...]], str, list[dict[str, str]]]:
    manifest_path = root / "EVIDENCE_MANIFEST.csv"
    manifest_sha256 = sha256_file(manifest_path)
    if expected_manifest_sha256 and manifest_sha256 != expected_manifest_sha256:
        raise RuntimeError(
            f"evidence manifest mismatch: expected {expected_manifest_sha256}, "
            f"got {manifest_sha256}"
        )
    rows = read_csv(manifest_path)
    vectors: dict[str, tuple[float, ...]] = {}
    for row in rows:
        evidence_id = row["evidence_id"]
        if evidence_id in vectors:
            raise RuntimeError(f"duplicate evidence_id: {evidence_id}")
        if int(row["signature_dimension"]) != DIMENSIONS:
            raise RuntimeError(f"wrong signature dimension: {evidence_id}")
        if row.get("leakage_pass") != "true":
            raise RuntimeError(f"evidence leakage status is not true: {evidence_id}")
        if row.get("baseline_sha256") not in {EXPECTED_BASELINE_SHA256, "synthetic"}:
            raise RuntimeError(f"unexpected baseline provenance: {evidence_id}")
        if row.get("r2_guard_sha256") not in {EXPECTED_R2_GUARD_SHA256, "synthetic"}:
            raise RuntimeError(f"unexpected R2 guard provenance: {evidence_id}")
        signature_path = root / row["signature_path"]
        vectors[evidence_id] = load_signature(signature_path, row["signature_sha256"])
    return vectors, manifest_sha256, rows


def arithmetic_mean(vectors: list[tuple[float, ...]]) -> list[float]:
    if not vectors:
        raise ValueError("cannot build a prototype from zero signatures")
    if any(len(vector) != DIMENSIONS for vector in vectors):
        raise ValueError("prototype input dimension mismatch")
    count = len(vectors)
    return [math.fsum(vector[index] for vector in vectors) / count for index in range(DIMENSIONS)]


def classify(
    vector: tuple[float, ...] | list[float],
    prototypes: dict[str, list[float]],
    *,
    tie_tolerance: float = TIE_TOLERANCE,
) -> tuple[str | None, bool, dict[str, float]]:
    if len(vector) != DIMENSIONS or not prototypes:
        raise ValueError("invalid classification input")
    distances = {
        label: math.fsum(abs(left - right) for left, right in zip(vector, prototype))
        / DIMENSIONS
        for label, prototype in sorted(prototypes.items())
    }
    minimum = min(distances.values())
    tied = [label for label, distance in distances.items() if abs(distance - minimum) <= tie_tolerance]
    if len(tied) != 1:
        return None, True, distances
    return tied[0], False, distances


def _load_mapping(path: Path) -> tuple[dict[str, str], list[str]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    mapping = {str(key): str(value) for key, value in payload["label_by_identifier"].items()}
    labels = [str(value) for value in payload["label_space"]]
    if mapping.get("Normal") != "Normal" or set(mapping.values()) != set(labels):
        raise RuntimeError("pseudolabel mapping is inconsistent")
    return mapping, labels


def _load_assignment(path: Path, mapping: dict[str, str]) -> dict[str, str]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assignment = {
        str(agent): str(item["local_fault_label"])
        for agent, item in payload["assignment"].items()
    }
    if len(assignment) != 8 or set(assignment.values()) != set(mapping.values()) - {"Normal"}:
        raise RuntimeError("agent assignment is inconsistent")
    return assignment


def build_prototypes(
    *,
    fault_root: Path,
    fault_index_path: Path,
    normal_root: Path,
    normal_index_path: Path,
    mapping_path: Path,
    assignment_path: Path,
    output_dir: Path,
    strict_campaign: bool = True,
) -> dict[str, Any]:
    here = Path(__file__).resolve().parent
    expected = EXPECTED_FAULT_MANIFEST_SHA256 if strict_campaign else None
    fault_vectors, fault_manifest_hash, _ = load_evidence(
        fault_root, expected_manifest_sha256=expected
    )
    normal_vectors, normal_manifest_hash, _ = load_evidence(
        normal_root, expected_manifest_sha256=None
    )
    mapping, labels = _load_mapping(mapping_path)
    assignment = _load_assignment(assignment_path, mapping)

    fault_groups: dict[str, list[tuple[float, ...]]] = defaultdict(list)
    used_fault: set[str] = set()
    for row in read_csv(fault_index_path):
        evidence_id = row["evidence_id"]
        identifier = row.get("fault") or row.get("class_identifier")
        if identifier not in mapping or identifier == "Normal":
            raise RuntimeError(f"invalid fault index identifier: {identifier}")
        if evidence_id not in fault_vectors or evidence_id in used_fault:
            raise RuntimeError(f"invalid or duplicate fault evidence index: {evidence_id}")
        used_fault.add(evidence_id)
        fault_groups[mapping[identifier]].append(fault_vectors[evidence_id])

    normal_by_agent: dict[str, list[tuple[float, ...]]] = defaultdict(list)
    used_normal: set[str] = set()
    for row in read_csv(normal_index_path):
        evidence_id = row["evidence_id"]
        agent_id = row["agent_id"]
        identifier = row.get("class_identifier", "Normal")
        if identifier != "Normal" or agent_id not in assignment:
            raise RuntimeError(f"invalid Normal evaluator index row: {row}")
        if evidence_id not in normal_vectors or evidence_id in used_normal:
            raise RuntimeError(f"invalid or duplicate Normal evidence index: {evidence_id}")
        used_normal.add(evidence_id)
        normal_by_agent[agent_id].append(normal_vectors[evidence_id])

    fault_labels = labels[:-1]
    if set(fault_groups) != set(fault_labels) or set(normal_by_agent) != set(assignment):
        raise RuntimeError("development class or agent coverage mismatch")
    if used_fault != set(fault_vectors) or used_normal != set(normal_vectors):
        raise RuntimeError("some evidence units are absent from evaluator indices")
    if strict_campaign:
        if {len(fault_groups[label]) for label in fault_labels} != {40}:
            raise RuntimeError("each fault prototype requires exactly 40 signatures")
        if {len(normal_by_agent[agent]) for agent in assignment} != {40}:
            raise RuntimeError("each local Normal prototype requires exactly 40 signatures")

    all_normal = [vector for agent in sorted(normal_by_agent) for vector in normal_by_agent[agent]]
    global_doc: dict[str, Any] = {}
    for label in labels:
        vectors = all_normal if label == "Normal" else fault_groups[label]
        global_doc[label] = {"n_signatures": len(vectors), "vector": arithmetic_mean(vectors)}
    local_doc: dict[str, Any] = {}
    for agent, local_label in sorted(assignment.items()):
        local_doc[agent] = {
            "local_fault_label": local_label,
            "prototypes": {
                "Normal": {
                    "n_signatures": len(normal_by_agent[agent]),
                    "vector": arithmetic_mean(normal_by_agent[agent]),
                },
                local_label: {
                    "n_signatures": len(fault_groups[local_label]),
                    "vector": arithmetic_mean(fault_groups[local_label]),
                },
            },
            "absent_class_policy": "not_a_candidate_no_global_fallback",
        }

    prototype_doc = {
        "schema_version": 1,
        "method": "arithmetic_mean_697d_then_minimum_mean_l1",
        "dimensions": DIMENSIONS,
        "tie_tolerance_absolute": TIE_TOLERANCE,
        "distance_abstention_threshold": None,
        "label_space": labels,
        "global": global_doc,
        "local": local_doc,
    }
    prototype_bytes = json_bytes(prototype_doc)
    if F_NUMBER.search(prototype_bytes):
        raise RuntimeError("F-number leaked into PROTOTYPES.json")
    prototype_path = output_dir / "PROTOTYPES.json"
    write_once(prototype_path, prototype_bytes)
    manifest_doc = {
        "schema_version": 1,
        "status": "PROTOTYPES_BUILT_NOT_INDEPENDENTLY_VERIFIED",
        "fault_evidence_manifest_sha256": fault_manifest_hash,
        "normal_evidence_manifest_sha256": normal_manifest_hash,
        "pseudolabel_map_sha256": sha256_file(mapping_path),
        "agent_assignment_sha256": sha256_file(assignment_path),
        "baseline_code_sha256": sha256_file(Path(__file__)),
        "baseline_specification_sha256": sha256_file(here / "SPECIFICA_BASELINE_NUMERICA.md"),
        "prototypes_sha256": hashlib.sha256(prototype_bytes).hexdigest(),
        "dimensions": DIMENSIONS,
        "fault_signatures_per_class": sorted({len(value) for value in fault_groups.values()}),
        "normal_signatures_global": len(all_normal),
        "normal_signatures_per_agent": sorted({len(value) for value in normal_by_agent.values()}),
        "r2_dependency": "required; regenerate Normal evidence if R2 fails",
    }
    manifest_bytes = json_bytes(manifest_doc)
    if F_NUMBER.search(manifest_bytes):
        raise RuntimeError("F-number leaked into prototype manifest")
    write_once(output_dir / "PROTOTYPES_MANIFEST.json", manifest_bytes)
    return prototype_doc


def _prototype_vectors(items: dict[str, Any]) -> dict[str, list[float]]:
    return {label: value["vector"] for label, value in items.items()}


def _bool(value: Any) -> bool:
    return value is True or str(value).lower() == "true"


def metric(rows: list[dict[str, Any]]) -> dict[str, Any]:
    correct = sum(_bool(row["is_correct"]) for row in rows)
    abstentions = sum(_bool(row["abstain"]) for row in rows)
    non_abstained = len(rows) - abstentions
    return {
        "n": len(rows),
        "correct": correct,
        "abstentions": abstentions,
        "non_abstained": non_abstained,
        "accuracy": correct / len(rows) if rows else None,
        "abstention_rate": abstentions / len(rows) if rows else None,
        "accuracy_non_abstained": correct / non_abstained if non_abstained else None,
    }


def evaluate(
    *,
    prototypes_path: Path,
    test_evidence_root: Path,
    test_index_path: Path,
    output_dir: Path,
    expected_test_manifest_sha256: str | None = None,
) -> dict[str, Any]:
    prototype_doc = json.loads(prototypes_path.read_text(encoding="utf-8"))
    vectors, evidence_manifest_hash, _ = load_evidence(
        test_evidence_root, expected_manifest_sha256=expected_test_manifest_sha256
    )
    index_rows = read_csv(test_index_path)
    case_rows: list[dict[str, str]] = []
    keys: set[tuple[str, str]] = set()
    agents = set(prototype_doc["local"])
    for row in index_rows:
        key = (row["agent_id"], row["physical_case_id"])
        if key in keys or row["agent_id"] not in agents or row["evidence_id"] not in vectors:
            raise RuntimeError(f"invalid or duplicate test index row: {row}")
        keys.add(key)
        case_rows.append({key: row[key] for key in ("agent_id", "physical_case_id", "evidence_id")})

    unscored: list[dict[str, Any]] = []
    distance_rows: list[dict[str, Any]] = []
    for condition in ("numeric_global", "numeric_local"):
        for row in case_rows:
            if condition == "numeric_global":
                candidates = _prototype_vectors(prototype_doc["global"])
            else:
                candidates = _prototype_vectors(
                    prototype_doc["local"][row["agent_id"]]["prototypes"]
                )
            predicted, abstain, distances = classify(vectors[row["evidence_id"]], candidates)
            unscored.append({
                "condition": condition,
                **row,
                "predicted_label": predicted or "",
                "abstain": str(abstain).lower(),
                "valid": "true",
            })
            for label, distance in distances.items():
                distance_rows.append({
                    "condition": condition,
                    "agent_id": row["agent_id"],
                    "physical_case_id": row["physical_case_id"],
                    "candidate_label": label,
                    "mean_l1_distance": format(distance, ".17g"),
                })

    unscored_fields = [
        "condition", "agent_id", "physical_case_id", "evidence_id",
        "predicted_label", "abstain", "valid",
    ]
    unscored_bytes = csv_bytes(unscored, unscored_fields)
    if F_NUMBER.search(unscored_bytes):
        raise RuntimeError("F-number leaked into unscored predictions")
    write_once(output_dir / "predictions_unscored.csv", unscored_bytes)

    truth: dict[tuple[str, str], str] = {}
    for row in read_csv(test_index_path):
        label = row["true_pseudolabel"]
        if label not in prototype_doc["label_space"]:
            raise RuntimeError(f"truth is not a pseudolabel: {label}")
        truth[(row["agent_id"], row["physical_case_id"])] = label
    local_labels = {
        agent: value["local_fault_label"] for agent, value in prototype_doc["local"].items()
    }
    scored: list[dict[str, Any]] = []
    for row in unscored:
        actual = truth[(row["agent_id"], row["physical_case_id"])]
        population = (
            "normal" if actual == "Normal"
            else "local_seen" if actual == local_labels[row["agent_id"]]
            else "local_unseen"
        )
        scored.append({
            "condition": row["condition"],
            "agent_id": row["agent_id"],
            "physical_case_id": row["physical_case_id"],
            "true_pseudolabel": actual,
            "abstain": row["abstain"],
            "predicted_label": row["predicted_label"],
            "valid": row["valid"],
            "is_correct": str(bool(row["predicted_label"] and row["predicted_label"] == actual)).lower(),
            "population": population,
        })
    scored_fields = [
        "condition", "agent_id", "physical_case_id", "true_pseudolabel",
        "abstain", "predicted_label", "valid", "is_correct", "population",
    ]
    scored_bytes = csv_bytes(scored, scored_fields)
    distance_bytes = csv_bytes(distance_rows, [
        "condition", "agent_id", "physical_case_id", "candidate_label", "mean_l1_distance",
    ])
    if F_NUMBER.search(scored_bytes + distance_bytes):
        raise RuntimeError("F-number leaked into evaluator outputs")
    write_once(output_dir / "predictions.csv", scored_bytes)
    write_once(output_dir / "distances.csv", distance_bytes)

    summary: dict[str, Any] = {}
    clusters: list[dict[str, Any]] = []
    for condition in ("numeric_global", "numeric_local"):
        selected = [row for row in scored if row["condition"] == condition]
        summary[condition] = {"all": metric(selected)}
        for population in ("local_unseen", "local_seen", "normal"):
            summary[condition][population] = metric(
                [row for row in selected if row["population"] == population]
            )
        for case_id in sorted({row["physical_case_id"] for row in selected}):
            cluster_rows = [row for row in selected if row["physical_case_id"] == case_id]
            clusters.append({
                "condition": condition,
                "physical_case_id": case_id,
                "independence_claim": False,
                **metric(cluster_rows),
            })
    metrics_doc = {
        "schema_version": 1,
        "status": "TECHNICAL_OUTPUT_NOT_A_PERFORMANCE_ESTIMATE",
        "three_numbers": ["accuracy", "abstention_rate", "accuracy_non_abstained"],
        "statistical_unit": "physical_case_id",
        "independence_claim": False,
        "test_evidence_manifest_sha256": evidence_manifest_hash,
        "summary": summary,
        "clusters": clusters,
    }
    metrics_bytes = json_bytes(metrics_doc)
    if F_NUMBER.search(metrics_bytes):
        raise RuntimeError("F-number leaked into metrics")
    write_once(output_dir / "metrics.json", metrics_bytes)
    output_manifest = {
        "schema_version": 1,
        "status": "EVALUATOR_SIDE",
        "prototypes_sha256": sha256_file(prototypes_path),
        "test_index_sha256": sha256_file(test_index_path),
        "files": {
            name: sha256_file(output_dir / name)
            for name in ("predictions_unscored.csv", "predictions.csv", "distances.csv", "metrics.json")
        },
    }
    write_once(output_dir / "OUTPUT_MANIFEST.json", json_bytes(output_manifest))
    return metrics_doc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    build = subparsers.add_parser("build")
    build.add_argument("--fault-evidence", type=Path, required=True)
    build.add_argument("--fault-index", type=Path, required=True)
    build.add_argument("--normal-evidence", type=Path, required=True)
    build.add_argument("--normal-index", type=Path, required=True)
    build.add_argument("--pseudolabel-map", type=Path, required=True)
    build.add_argument("--agent-assignment", type=Path, required=True)
    build.add_argument("--output", type=Path, required=True)
    build.add_argument("--fixture", action="store_true")
    evaluate_parser = subparsers.add_parser("evaluate")
    evaluate_parser.add_argument("--prototypes", type=Path, required=True)
    evaluate_parser.add_argument("--test-evidence", type=Path, required=True)
    evaluate_parser.add_argument("--test-index", type=Path, required=True)
    evaluate_parser.add_argument("--output", type=Path, required=True)
    evaluate_parser.add_argument("--expected-test-manifest-sha256")
    args = parser.parse_args()
    if args.command == "build":
        build_prototypes(
            fault_root=args.fault_evidence,
            fault_index_path=args.fault_index,
            normal_root=args.normal_evidence,
            normal_index_path=args.normal_index,
            mapping_path=args.pseudolabel_map,
            assignment_path=args.agent_assignment,
            output_dir=args.output,
            strict_campaign=not args.fixture,
        )
    else:
        evaluate(
            prototypes_path=args.prototypes,
            test_evidence_root=args.test_evidence,
            test_index_path=args.test_index,
            output_dir=args.output,
            expected_test_manifest_sha256=args.expected_test_manifest_sha256,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
