#!/usr/bin/env python3
"""Independently recompute every prototype from signed evidence CSV files."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
from collections import defaultdict
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Any


DIMENSIONS = 697
ABSOLUTE_TOLERANCE = Decimal("2e-16")
F_NUMBER = re.compile(r"(?<![A-Za-z0-9_])F(?:1|2|3|8|10|13|14|15)(?![A-Za-z0-9_])")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def load_vectors(root: Path) -> tuple[dict[str, tuple[Decimal, ...]], str]:
    manifest_path = root / "EVIDENCE_MANIFEST.csv"
    rows = read_csv(manifest_path)
    vectors: dict[str, tuple[Decimal, ...]] = {}
    for row in rows:
        evidence_id = row["evidence_id"]
        path = root / row["signature_path"]
        if sha256_file(path) != row["signature_sha256"]:
            raise RuntimeError(f"{evidence_id}: signature SHA-256 mismatch")
        values = read_csv(path)
        if len(values) != DIMENSIONS:
            raise RuntimeError(f"{evidence_id}: signature dimension mismatch")
        vector = tuple(Decimal(item["value"]) for item in values)
        if any(int(item["component"]) != index for index, item in enumerate(values)):
            raise RuntimeError(f"{evidence_id}: component order mismatch")
        if any(not value.is_finite() or value < 0 or value > 1 for value in vector):
            raise RuntimeError(f"{evidence_id}: invalid signature value")
        if evidence_id in vectors:
            raise RuntimeError(f"duplicate evidence_id: {evidence_id}")
        vectors[evidence_id] = vector
    return vectors, sha256_file(manifest_path)


def mean(vectors: list[tuple[Decimal, ...]]) -> tuple[Decimal, ...]:
    if not vectors:
        raise RuntimeError("cannot recompute a mean from zero signatures")
    count = Decimal(len(vectors))
    return tuple(sum((vector[index] for vector in vectors), Decimal(0)) / count for index in range(DIMENSIONS))


def compare_vector(actual: list[float], expected: tuple[Decimal, ...]) -> Decimal:
    if len(actual) != DIMENSIONS:
        raise RuntimeError("prototype dimension mismatch")
    differences = [abs(Decimal(str(value)) - reference) for value, reference in zip(actual, expected)]
    maximum = max(differences)
    if maximum > ABSOLUTE_TOLERANCE:
        raise RuntimeError(f"prototype differs from independent Decimal mean: {maximum}")
    return maximum


def verify(
    *,
    prototypes_path: Path,
    prototype_manifest_path: Path,
    fault_root: Path,
    fault_index_path: Path,
    normal_root: Path,
    normal_index_path: Path,
    mapping_path: Path,
    assignment_path: Path,
) -> dict[str, Any]:
    getcontext().prec = 50
    prototypes = json.loads(prototypes_path.read_text(encoding="utf-8"))
    manifest = json.loads(prototype_manifest_path.read_text(encoding="utf-8"))
    mapping_payload = json.loads(mapping_path.read_text(encoding="utf-8"))
    assignment_payload = json.loads(assignment_path.read_text(encoding="utf-8"))
    mapping = mapping_payload["label_by_identifier"]
    assignment = {
        agent: item["local_fault_label"]
        for agent, item in assignment_payload["assignment"].items()
    }
    fault_vectors, fault_manifest_sha256 = load_vectors(fault_root)
    normal_vectors, normal_manifest_sha256 = load_vectors(normal_root)

    fault_groups: dict[str, list[tuple[Decimal, ...]]] = defaultdict(list)
    used_fault: set[str] = set()
    for row in read_csv(fault_index_path):
        evidence_id = row["evidence_id"]
        label = mapping[row["fault"]]
        if evidence_id in used_fault or evidence_id not in fault_vectors:
            raise RuntimeError(f"invalid fault evidence index: {evidence_id}")
        used_fault.add(evidence_id)
        fault_groups[label].append(fault_vectors[evidence_id])

    normal_groups: dict[str, list[tuple[Decimal, ...]]] = defaultdict(list)
    used_normal: set[str] = set()
    local_examples = 0
    for row in read_csv(normal_index_path):
        evidence_id = row["evidence_id"]
        agent = row["agent_id"]
        if evidence_id in used_normal or evidence_id not in normal_vectors:
            raise RuntimeError(f"invalid Normal evidence index: {evidence_id}")
        if row["class_identifier"] != "Normal" or agent not in assignment:
            raise RuntimeError(f"invalid Normal class or agent: {evidence_id}")
        expected_local = int(row["agent_run_index"]) == 1 and int(row["window_ordinal"]) == 1
        if (row["local_example_03_10"] == "true") != expected_local:
            raise RuntimeError(f"invalid local example flag: {evidence_id}")
        local_examples += expected_local
        used_normal.add(evidence_id)
        normal_groups[agent].append(normal_vectors[evidence_id])

    if used_fault != set(fault_vectors) or used_normal != set(normal_vectors):
        raise RuntimeError("an evaluator index does not cover every evidence unit exactly once")
    if {len(values) for values in fault_groups.values()} != {40}:
        raise RuntimeError("fault prototype inputs are not 40 signatures per class")
    if {len(values) for values in normal_groups.values()} != {40}:
        raise RuntimeError("Normal prototype inputs are not 40 signatures per agent")
    if local_examples != 8:
        raise RuntimeError("expected one pre-specified Normal example per agent")

    all_normal = [vector for agent in sorted(normal_groups) for vector in normal_groups[agent]]
    maximum = Decimal(0)
    compared = 0
    for label, record in prototypes["global"].items():
        inputs = all_normal if label == "Normal" else fault_groups[label]
        if record["n_signatures"] != len(inputs):
            raise RuntimeError(f"{label}: global input count mismatch")
        maximum = max(maximum, compare_vector(record["vector"], mean(inputs)))
        compared += 1
    for agent, record in prototypes["local"].items():
        local_label = assignment[agent]
        if record["local_fault_label"] != local_label:
            raise RuntimeError(f"{agent}: local label mismatch")
        for label, inputs in (
            ("Normal", normal_groups[agent]),
            (local_label, fault_groups[local_label]),
        ):
            item = record["prototypes"][label]
            if item["n_signatures"] != len(inputs):
                raise RuntimeError(f"{agent}/{label}: local input count mismatch")
            maximum = max(maximum, compare_vector(item["vector"], mean(inputs)))
            compared += 1

    prototype_bytes = prototypes_path.read_bytes()
    if F_NUMBER.search(prototype_bytes.decode("utf-8")):
        raise RuntimeError("F-number leaked into PROTOTYPES.json")
    expected_manifest = {
        "prototypes_sha256": sha256_file(prototypes_path),
        "fault_evidence_manifest_sha256": fault_manifest_sha256,
        "normal_evidence_manifest_sha256": normal_manifest_sha256,
        "pseudolabel_map_sha256": sha256_file(mapping_path),
        "agent_assignment_sha256": sha256_file(assignment_path),
    }
    mismatches = {
        key: (manifest.get(key), value)
        for key, value in expected_manifest.items()
        if manifest.get(key) != value
    }
    if mismatches:
        raise RuntimeError(f"prototype manifest hash mismatch: {mismatches}")
    if prototypes.get("dimensions") != DIMENSIONS or not math.isclose(
        float(prototypes.get("tie_tolerance_absolute")), 1e-12, rel_tol=0, abs_tol=0
    ):
        raise RuntimeError("prototype method constants differ from the specification")
    if prototypes.get("distance_abstention_threshold") is not None:
        raise RuntimeError("an unplanned distance threshold is present")

    return {
        "status": "PASS",
        "verification_method": "independent Decimal(precision=50) componentwise recomputation",
        "dimensions": DIMENSIONS,
        "global_prototypes_recomputed": 9,
        "local_prototypes_recomputed": 16,
        "prototype_vectors_compared": compared,
        "fault_signatures_per_class": 40,
        "normal_signatures_global": len(all_normal),
        "normal_signatures_per_agent": 40,
        "local_examples_03_10": local_examples,
        "maximum_absolute_component_difference": format(maximum, "f"),
        "absolute_tolerance": format(ABSOLUTE_TOLERANCE, "f"),
        "prototypes_sha256": sha256_file(prototypes_path),
        "prototype_manifest_sha256": sha256_file(prototype_manifest_path),
        "fault_evidence_manifest_sha256": fault_manifest_sha256,
        "normal_evidence_manifest_sha256": normal_manifest_sha256,
        "test_data_opened": False,
        "performance_evaluation_performed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prototypes", type=Path, required=True)
    parser.add_argument("--prototype-manifest", type=Path, required=True)
    parser.add_argument("--fault-evidence", type=Path, required=True)
    parser.add_argument("--fault-index", type=Path, required=True)
    parser.add_argument("--normal-evidence", type=Path, required=True)
    parser.add_argument("--normal-index", type=Path, required=True)
    parser.add_argument("--mapping", type=Path, required=True)
    parser.add_argument("--assignment", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = verify(
        prototypes_path=args.prototypes,
        prototype_manifest_path=args.prototype_manifest,
        fault_root=args.fault_evidence,
        fault_index_path=args.fault_index,
        normal_root=args.normal_evidence,
        normal_index_path=args.normal_index,
        mapping_path=args.mapping,
        assignment_path=args.assignment,
    )
    content = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if args.output.exists() and args.output.read_text(encoding="utf-8") != content:
        raise RuntimeError(f"refusing to overwrite different output: {args.output}")
    args.output.write_text(content, encoding="utf-8")
    print(content, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
