#!/usr/bin/env python3
"""Fail-closed final FedAvg 03.14 preflight and single execution."""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import platform
import subprocess
import sys
from collections import Counter
from pathlib import Path
from types import ModuleType
from typing import Any, Iterable, Mapping

import numpy as np

try:
    from .fedavg import (
        CLIENTS,
        DIMENSION,
        LABELS,
        Config,
        Dataset,
        TrainedModel,
        concatenate,
        evaluate_all_modes,
        load_evidence_bundle,
        predict,
        sha256_file,
        train_all_modes,
        write_metrics,
        write_weight_hashes,
    )
except ImportError:
    from fedavg import (
        CLIENTS,
        DIMENSION,
        LABELS,
        Config,
        Dataset,
        TrainedModel,
        concatenate,
        evaluate_all_modes,
        load_evidence_bundle,
        predict,
        sha256_file,
        train_all_modes,
        write_metrics,
        write_weight_hashes,
    )


EXPECTED_PACKAGE_HEAD = "546edd7a1544beae06b3544a9de2eb659dcedbee"
EXPECTED_PACKAGE_TREE = "07cab1de0e282a841ce70a4b777545eae2746d71"
EXPECTED_0311_COMMIT = "fd41fcf05aa6374d01b45b26b0881e2ffcc98062"
EXPECTED_0311_TREE = "9010a6b3aab4029f20ff5355455c452bbefde1b5"
EXPECTED_REVIEW_SHA256 = "09994cf7536166d4d4717eecd585ebe61c664fb5f388d58425cbc181e611f16f"
EXPECTED_REVIEW_BYTES = 2339
EXPECTED_EXTRACTOR_SHA256 = "46b451c2d6d8b1627993828ac9bac39532562f2fa1b27955b8a20f098ba24e97"
EXPECTED_LEAKAGE_SHA256 = "c77ae5b11186c5b0df87b2f1df8800cb45fb25317e248fe8484d3e8283073887"
EXPECTED_BASELINE_SHA256 = "79883dd0aabbd034c15337b0be1ffca37e59ea7b32443a15d560b7feda2b2e6a"
EXPECTED_R2_SHA256 = "7df0cef2d7854c689b79eb911fa01d1ede1625e22f0d3636c0ea5d678c9f33f8"
EXPECTED_FAULT_MANIFEST_SHA256 = "5111d0c61c2e93fe5071d7a85015673549af0bf9c1dc74e0d940719a8400e020"
EXPECTED_FAULT_INDEX_SHA256 = "b966cdd3d579efaf595fd48c4b9baa70747ba584522926520840a1e914dbf69c"
EXPECTED_NORMAL_MANIFEST_SHA256 = "cc8d96c2c60169afc99cb811cea194aa553afcc7cc51cad4a0092d44de38fdc1"
EXPECTED_NORMAL_INDEX_SHA256 = "27a534502146589bdcb914fee3b5a55dfb7b209b094a55b1ad5495ac889431ae"
EXPECTED_TEST_ARCHIVE_SHA256 = "ac1e7c0c4575ab746ee24a8bb5ce7f09289919773bc4d8c61ba86f7a93218a55"
EXPECTED_TEST_ARCHIVE_BYTES = 141_191_097
EXPECTED_AUDIT_SHA256 = "420a61eb65a47961092ee042f7fa08797a25b350f875cad76c0954f7f3eeb6e3"
EXPECTED_GENERATION_MANIFEST_SHA256 = "e7c75d23107e95abcdbcf7531f845d3d90b8620974d7c3917071b37f70a34780"
EXPECTED_EVENTS_SHA256 = "af4f659ee82d25cc71caac1d3ca2c04c58efa9448d23ac1fe59b46276bb1b55e"
EXPECTED_PLAN_SHA256 = "ef0b28529b6a48932d6fb7483c1fef44e331db089f284cc3d7a06a6e20879572"
EXPECTED_RUNTIME_LOG_SHA256 = "73ce498d56d192b57da6bf957985adf0606b985f522e8feacfc45f1eed96587c"
PRIMARY_FAULTS = ("F1", "F2", "F3", "F8", "F10", "F13", "F14", "F15")
OOD_FAULTS = ("F4", "F5")
WINDOWS_PER_RUN = 8
PIPELINE_FILES = {
    "code/tep_features.py": "cbade7a295dfae6550df7ecbe35fa2be1f844b63c4c528ec194f95a20961040c",
    "code/tep_verbalize_v2.py": "3a9129b6353cac6f8c9e02281282f137dd07885b1f882ca633ee9d6bf52393be",
    "code/verbalizer_config_v2.json": "552a0b8a9cf9e416de77daa7aca2d8dee152a2700bbfaab4ae5e039081712519",
    "code/evaluate_verbalizer_v2.py": "972e06fa29bee5a58d57ca757bd158c5cddaa2f4ed12eb5c739169c7fef79a92",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fields: Iterable[str], rows: Iterable[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(("git", "-C", str(repo), *args), text=True).strip()


def require_hash(path: Path, expected: str, *, size: int | None = None) -> dict[str, Any]:
    actual = sha256_file(path)
    if actual != expected:
        raise RuntimeError(f"hash mismatch for {path}: expected {expected}, got {actual}")
    actual_size = path.stat().st_size
    if size is not None and actual_size != size:
        raise RuntimeError(f"size mismatch for {path}: expected {size}, got {actual_size}")
    return {"path": str(path), "bytes": actual_size, "sha256": actual}


def require_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"expected JSON object: {path}")
    return value


def classify_run(run_id: str) -> tuple[str, str]:
    if run_id.startswith("test-primary-Normal-"):
        return "primary", "Normal"
    if run_id.startswith("test-primary-"):
        label = run_id.split("-")[2]
        if label not in PRIMARY_FAULTS:
            raise RuntimeError(f"unexpected primary fault: {run_id}")
        return "primary", label
    if run_id.startswith("test-ood-"):
        label = run_id.split("-")[2]
        if label not in OOD_FAULTS:
            raise RuntimeError(f"unexpected OOD fault: {run_id}")
        return "ood", label
    if run_id.startswith("test-spare-"):
        return "spare", run_id.split("-")[2]
    raise RuntimeError(f"unexpected run id: {run_id}")


def load_verified_extractor(path: Path) -> ModuleType:
    path = path.resolve()
    leakage = path.with_name("leakage.py")
    require_hash(path, EXPECTED_EXTRACTOR_SHA256)
    require_hash(leakage, EXPECTED_LEAKAGE_SHA256)
    sys.path.insert(0, str(path.parent))
    try:
        spec = importlib.util.spec_from_file_location("fase03_6_final_extractor", path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"cannot load extractor: {path}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path.pop(0)


def verify_freeze(repo: Path) -> list[dict[str, Any]]:
    freeze = require_json(repo / "studio2/fase03/fedavg/FEDAVG_FREEZE.json")
    checked = []
    for item in freeze["files"]:
        checked.append(require_hash(repo / item["path"], item["sha256"]))
    if len(checked) != 8:
        raise RuntimeError("FEDAVG_FREEZE.json must contain exactly eight frozen files")
    return checked


def verify_0311_identity(repo_0311: Path) -> dict[str, Any]:
    current = git(repo_0311, "rev-parse", "HEAD")
    if subprocess.run(
        ("git", "-C", str(repo_0311), "merge-base", "--is-ancestor", EXPECTED_0311_COMMIT, current),
        check=False,
    ).returncode != 0:
        raise RuntimeError("verified 03.11 commit is not an ancestor of the current checkout")
    expected_tree = git(repo_0311, "show", "-s", "--format=%T", EXPECTED_0311_COMMIT)
    if expected_tree != EXPECTED_0311_TREE:
        raise RuntimeError("03.11 verified commit tree mismatch")
    delta = git(repo_0311, "diff", "--name-only", f"{EXPECTED_0311_COMMIT}..{current}").splitlines()
    allowed = {
        "studio2/fase03/fault_runs/ACQUISIZIONE_OK_ESECUZIONE_03_11.md",
        "studio2/fase03/fault_runs/VERIFICA_ESECUZIONE_03_11_v2.md",
    }
    if set(filter(None, delta)) - allowed:
        raise RuntimeError(f"substantive 03.11 delta after verified commit: {delta}")
    return {"verified_commit": EXPECTED_0311_COMMIT, "verified_tree": expected_tree,
            "checkout_head": current, "post_review_delta": delta}


def verify_test_batch(args: argparse.Namespace) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    require_hash(args.review, EXPECTED_REVIEW_SHA256, size=EXPECTED_REVIEW_BYTES)
    require_hash(args.audit, EXPECTED_AUDIT_SHA256)
    require_hash(args.generation_manifest, EXPECTED_GENERATION_MANIFEST_SHA256)
    require_hash(args.events, EXPECTED_EVENTS_SHA256)
    require_hash(args.plan, EXPECTED_PLAN_SHA256)
    require_hash(args.runtime_log, EXPECTED_RUNTIME_LOG_SHA256)
    require_hash(args.test_archive, EXPECTED_TEST_ARCHIVE_SHA256, size=EXPECTED_TEST_ARCHIVE_BYTES)
    audit = require_json(args.audit)
    counts = audit.get("counts", {})
    expected_counts = {
        "total_generated": 89,
        "primary_fault": 64,
        "primary_normal": 8,
        "ood": 6,
        "technical_spares": 11,
        "complete": 89,
        "physical_trip": 0,
        "technical_failure": 0,
        "not_run": 0,
        "spares_activated_as_replacements": 0,
        "complete_windows": 712,
    }
    if audit.get("status") != "PASS" or counts != expected_counts:
        raise RuntimeError("03.11 audit status or counts differ from the sealed values")
    if audit.get("generic_campaign_audit", {}).get("hashes_verified") is not True:
        raise RuntimeError("03.11 generic audit did not verify hashes")

    rows = read_csv(args.generation_manifest)
    if len(rows) != 89 or len({row["run_id"] for row in rows}) != 89:
        raise RuntimeError("03.11 generation manifest is not 89 unique runs")
    final_rows: list[dict[str, Any]] = []
    observed: Counter[str] = Counter()
    labels: Counter[str] = Counter()
    for row in sorted(rows, key=lambda item: item["run_id"]):
        scope, label = classify_run(row["run_id"])
        observed[scope] += 1
        labels[f"{scope}:{label}"] += 1
        if row.get("status") != "complete" or int(row.get("useful_windows_complete", -1)) != 8:
            raise RuntimeError(f"incomplete sealed run: {row['run_id']}")
        source = args.test_root / Path(row["output_path"]).name
        if sha256_file(source) != row["sha256"]:
            raise RuntimeError(f"source hash mismatch: {row['run_id']}")
        per_run_path = source.with_suffix(".manifest.json")
        per_run = require_json(per_run_path)
        if per_run.get("run_id") != row["run_id"] or per_run.get("sha256") != row["sha256"]:
            raise RuntimeError(f"per-run manifest mismatch: {row['run_id']}")
        if per_run.get("status") != "complete" or per_run.get("useful_windows_complete") != 8:
            raise RuntimeError(f"per-run completion mismatch: {row['run_id']}")
        if scope != "spare":
            final_rows.append({
                "run_id": row["run_id"],
                "evaluation_scope": scope,
                "true_label": label,
                "batch": row["batch"],
                "stream_id": row["stream_id"],
                "source_path": str(source),
                "source_bytes": source.stat().st_size,
                "source_sha256": row["sha256"],
                "source_manifest_path": str(per_run_path),
                "source_manifest_sha256": sha256_file(per_run_path),
                "windows": 8,
            })
    if observed != Counter({"primary": 72, "spare": 11, "ood": 6}):
        raise RuntimeError(f"unexpected 03.11 role counts: {observed}")
    expected_labels = Counter({f"primary:{label}": 8 for label in LABELS})
    expected_labels.update({"ood:F4": 3, "ood:F5": 3})
    if Counter({key: value for key, value in labels.items() if not key.startswith("spare:")}) != expected_labels:
        raise RuntimeError(f"unexpected final label counts: {labels}")
    return final_rows, {"all_89_source_hashes_verified": True, "role_counts": dict(observed),
                        "final_label_counts": dict(sorted(expected_labels.items()))}


def bundle_run_and_source_ids(root: Path) -> tuple[set[str], set[str]]:
    rows = read_csv(root / "EVALUATOR_INDEX.csv")
    return {row["run_id"] for row in rows}, {row["source_sha256"] for row in rows}


def preflight(args: argparse.Namespace) -> dict[str, Any]:
    repo = args.repo.resolve()
    output = args.output.resolve()
    if output.exists():
        raise FileExistsError(f"preflight output already exists: {output}")
    if git(repo, "rev-parse", "HEAD") != EXPECTED_PACKAGE_HEAD:
        raise RuntimeError("FedAvg package HEAD differs from the expected reviewed acquisition")
    if git(repo, "rev-parse", "HEAD^{tree}") != EXPECTED_PACKAGE_TREE:
        raise RuntimeError("FedAvg package tree differs from the expected reviewed acquisition")
    if git(repo, "branch", "--show-current") != "codex/studio2-fedavg":
        raise RuntimeError("wrong FedAvg branch")
    identity_0311 = verify_0311_identity(args.repo_0311.resolve())
    frozen_files = verify_freeze(repo)
    protocol = require_json(args.protocol)
    if not (
        protocol.get("recorded_before_final_signature_extraction") is True
        and protocol.get("ood_evaluation", {}).get("accuracy_defined") is False
        and protocol.get("ood_evaluation", {}).get("included_in_primary_metrics") is False
    ):
        raise RuntimeError("final OOD protocol is not fail-closed")
    pipeline = [require_hash(repo / path, digest) for path, digest in PIPELINE_FILES.items()]
    extractor = load_verified_extractor(args.extractor)
    require_hash(args.baseline, EXPECTED_BASELINE_SHA256)
    extractor.validate_r2_guard(args.r2_guard)
    require_hash(args.r2_guard, EXPECTED_R2_SHA256)
    final_rows, batch_checks = verify_test_batch(args)

    fault = load_evidence_bundle(
        args.fault_dev,
        expected_manifest_sha256=EXPECTED_FAULT_MANIFEST_SHA256,
        expected_index_sha256=EXPECTED_FAULT_INDEX_SHA256,
    )
    normal = load_evidence_bundle(
        args.normal_dev,
        expected_manifest_sha256=EXPECTED_NORMAL_MANIFEST_SHA256,
        expected_index_sha256=EXPECTED_NORMAL_INDEX_SHA256,
    )
    development = concatenate((fault, normal))
    if development.x.shape != (640, DIMENSION) or len(set(development.clusters.tolist())) != 80:
        raise RuntimeError("development inputs differ from the verified 640x697 / 80-run bundle")
    if set(development.clients.tolist()) != set(CLIENTS) or set(development.batches.tolist()) != set("12345"):
        raise RuntimeError("development client or batch coverage mismatch")
    fault_runs, fault_sources = bundle_run_and_source_ids(args.fault_dev)
    normal_runs, normal_sources = bundle_run_and_source_ids(args.normal_dev)
    final_run_ids = {row["run_id"] for row in final_rows}
    final_sources = {row["source_sha256"] for row in final_rows}
    if fault_runs & normal_runs or final_run_ids & (fault_runs | normal_runs):
        raise RuntimeError("development/final run-id overlap")
    if final_sources & (fault_sources | normal_sources):
        raise RuntimeError("development/final source-byte overlap")

    output.mkdir(parents=True)
    manifest_path = output / "FINAL_SET_MANIFEST.csv"
    fields = list(final_rows[0])
    write_csv(manifest_path, fields, final_rows)
    manifest_hash = sha256_file(manifest_path)
    summary = {
        "schema_version": 1,
        "status": "PASS",
        "scope": "preflight_before_final_signature_extraction_training_or_metric_readout",
        "package": {"commit": EXPECTED_PACKAGE_HEAD, "tree": EXPECTED_PACKAGE_TREE,
                    "frozen_files": frozen_files},
        "input_03_11": {**identity_0311, **batch_checks,
                         "review_sha256": EXPECTED_REVIEW_SHA256,
                         "generation_manifest_sha256": EXPECTED_GENERATION_MANIFEST_SHA256,
                         "audit_sha256": EXPECTED_AUDIT_SHA256,
                         "archive_sha256": EXPECTED_TEST_ARCHIVE_SHA256},
        "pipeline": {
            "phase03_6_extractor_sha256": EXPECTED_EXTRACTOR_SHA256,
            "phase03_6_leakage_sha256": EXPECTED_LEAKAGE_SHA256,
            "frozen_sources": pipeline,
            "baseline_sha256": EXPECTED_BASELINE_SHA256,
            "r2_guard_sha256": EXPECTED_R2_SHA256,
            "windows": {"start_h": 25.0, "end_h": 65.0, "window_h": 5.0,
                        "per_run": WINDOWS_PER_RUN},
        },
        "development": {
            "fault_samples": len(fault.x), "normal_samples": len(normal.x),
            "combined_samples": len(development.x), "dimensions": DIMENSION,
            "clusters": len(set(development.clusters.tolist())), "clients": len(CLIENTS),
            "batches": 5, "training_scope": "development_03_6_and_03_9_only",
            "normalization_scope": "development_only",
        },
        "final_set": {
            "primary_runs": 72, "primary_windows": 576, "ood_runs": 6,
            "ood_windows": 48, "spares_included": 0,
            "manifest_path": str(manifest_path.relative_to(repo)),
            "manifest_sha256": manifest_hash,
        },
        "separation": {"development_final_run_overlap": 0,
                       "development_final_source_hash_overlap": 0,
                       "final_run_ids_unique": True,
                       "evaluator_join_one_to_one_required": True},
        "ood": {"protocol_sha256": sha256_file(args.protocol),
                "separate_forced_attribution_only": True,
                "accuracy_defined": False, "structural_abstention_rate": 0.0,
                "direct_llm_comparison": False},
        "execution_started": False,
    }
    write_json(output / "INPUT_PREFLIGHT.json", summary)
    return summary


SIGNATURE_FIELDS = (
    "evidence_id", "run_id", "evaluation_scope", "true_label", "window_ordinal",
    "window_start_h", "window_end_h", "source_sha256", "source_manifest_sha256",
    "signature_path", "signature_bytes", "signature_sha256", "signature_dimension",
)


def extract_final_signatures(args: argparse.Namespace, extractor: ModuleType) -> list[dict[str, Any]]:
    root = args.output.resolve()
    signatures = root / "signatures"
    if signatures.exists():
        raise FileExistsError(f"signature output already exists: {signatures}")
    signatures.mkdir()
    api = extractor.load_frozen_api(args.repo.resolve())
    require_hash(args.baseline, EXPECTED_BASELINE_SHA256)
    extractor.validate_r2_guard(args.r2_guard)
    require_hash(args.r2_guard, EXPECTED_R2_SHA256)
    config = api.load_config(args.repo.resolve() / "code/verbalizer_config_v2.json")
    baseline = api.load_development_baseline(args.baseline, config)
    rows = read_csv(root / "FINAL_SET_MANIFEST.csv")
    evidence: list[dict[str, Any]] = []
    for counter, row in enumerate(rows, start=1):
        source = Path(row["source_path"])
        if sha256_file(source) != row["source_sha256"]:
            raise RuntimeError(f"source changed after preflight: {row['run_id']}")
        case = api.load_case(source)
        features = api.analyze_case_windows(case, baseline, start_h=25.0, end_h=65.0, window_h=5.0)
        starts = sorted(float(value) for value in features.window_start_h.unique())
        if starts != [25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 55.0, 60.0]:
            raise RuntimeError(f"unexpected final windows: {row['run_id']}")
        for ordinal, start_h in enumerate(starts, start=1):
            evidence_id = f"FINAL-EVD-{(counter - 1) * WINDOWS_PER_RUN + ordinal:04d}"
            unit = features[features.window_start_h == start_h].copy()
            unit = unit.sort_values(
                "variable", key=lambda series: series.map({name: i for i, name in enumerate(api.xmeas)})
            )
            result = api.verbalize_feature_table(unit, config)
            signature = api.signature_vector(result["structured"])
            if signature.shape != (DIMENSION,) or not np.isfinite(signature).all():
                raise RuntimeError(f"invalid final signature: {evidence_id}")
            signature_path = signatures / f"{evidence_id}.signature.csv"
            write_csv(signature_path, ("component", "value"), (
                {"component": index, "value": format(float(value), ".17g")}
                for index, value in enumerate(signature)
            ))
            evidence.append({
                "evidence_id": evidence_id, "run_id": row["run_id"],
                "evaluation_scope": row["evaluation_scope"], "true_label": row["true_label"],
                "window_ordinal": ordinal, "window_start_h": format(start_h, ".1f"),
                "window_end_h": format(start_h + 5.0, ".1f"),
                "source_sha256": row["source_sha256"],
                "source_manifest_sha256": row["source_manifest_sha256"],
                "signature_path": str(signature_path.relative_to(root)),
                "signature_bytes": signature_path.stat().st_size,
                "signature_sha256": sha256_file(signature_path), "signature_dimension": DIMENSION,
            })
    if len(evidence) != 624 or len({row["evidence_id"] for row in evidence}) != 624:
        raise RuntimeError("final evidence does not contain 624 unique signatures")
    write_csv(root / "FINAL_EVIDENCE_MANIFEST.csv", SIGNATURE_FIELDS, evidence)
    return evidence


def dataset_from_evidence(root: Path, rows: list[dict[str, Any]], scope: str) -> Dataset:
    selected = [row for row in rows if row["evaluation_scope"] == scope]
    xs: list[np.ndarray] = []
    ys: list[int] = []
    clusters: list[str] = []
    batches: list[str] = []
    owners: list[str] = []
    for row in selected:
        signature_rows = read_csv(root / row["signature_path"])
        if [int(item["component"]) for item in signature_rows] != list(range(DIMENSION)):
            raise RuntimeError(f"signature component mismatch: {row['evidence_id']}")
        values = np.asarray([float(item["value"]) for item in signature_rows], dtype=np.float64)
        if values.shape != (DIMENSION,) or not np.isfinite(values).all():
            raise RuntimeError(f"invalid persisted signature: {row['evidence_id']}")
        xs.append(values)
        label = row["true_label"]
        ys.append(LABELS.index(label) if label in LABELS else 0)
        clusters.append(row["run_id"])
        batches.append("final")
        owners.append(label if label in CLIENTS else CLIENTS[0])
    return Dataset(np.stack(xs), np.asarray(ys), np.asarray(owners),
                   np.asarray(clusters), np.asarray(batches))


def aggregate_primary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for mode in ("local", "fedavg", "centralized"):
        selected = [row for row in rows if row["mode"] == mode]
        correct = sum(int(row["correct"]) for row in selected)
        attempts = sum(int(row["n_attempts"]) for row in selected)
        result[mode] = {"correct": correct, "attempts": attempts,
                        "accuracy": correct / attempts, "abstentions": 0,
                        "abstention_rate": 0.0, "non_abstained": attempts,
                        "accuracy_non_abstained": correct / attempts}
    return result


OOD_FIELDS = (
    "mode", "receiver", "ood_fault", "predicted_label", "count", "total_for_fault_and_model",
    "proportion", "abstentions", "abstention_rate",
)


def ood_distribution(models: Mapping[str, object], dataset: Dataset) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    model_items: list[tuple[str, str, TrainedModel]] = []
    local = models["local"]
    if not isinstance(local, dict):
        raise TypeError("local models are not a mapping")
    for client in CLIENTS:
        model_items.append(("local", client, local[client]))
    model_items.extend((mode, "shared", models[mode]) for mode in ("fedavg", "centralized"))
    for mode, receiver, model in model_items:
        predictions = predict(model, dataset.x)
        for fault in OOD_FAULTS:
            mask = np.asarray([cluster.startswith(f"test-ood-{fault}-") for cluster in dataset.clusters])
            labels = [LABELS[int(value)] for value in predictions[mask]]
            counts = Counter(labels)
            total = len(labels)
            if total != 24:
                raise RuntimeError(f"expected 24 OOD predictions for {mode}/{receiver}/{fault}")
            for label in LABELS:
                output.append({"mode": mode, "receiver": receiver, "ood_fault": fault,
                               "predicted_label": label, "count": counts[label],
                               "total_for_fault_and_model": total,
                               "proportion": counts[label] / total,
                               "abstentions": 0, "abstention_rate": 0.0})
    return output


def execute(args: argparse.Namespace) -> dict[str, Any]:
    root = args.output.resolve()
    preflight_path = root / "INPUT_PREFLIGHT.json"
    preflight_record = require_json(preflight_path)
    if preflight_record.get("status") != "PASS" or preflight_record.get("execution_started") is not False:
        raise RuntimeError("final execution requires an unused PASS preflight")
    state_path = root / "EXECUTION_STATE.json"
    if state_path.exists():
        raise RuntimeError("final execution has already been started; rerun is forbidden")
    if sha256_file(root / "FINAL_SET_MANIFEST.csv") != preflight_record["final_set"]["manifest_sha256"]:
        raise RuntimeError("final set manifest changed after preflight")
    if sha256_file(args.protocol) != preflight_record["ood"]["protocol_sha256"]:
        raise RuntimeError("OOD protocol changed after preflight")
    verify_freeze(args.repo.resolve())
    for path, digest in PIPELINE_FILES.items():
        require_hash(args.repo.resolve() / path, digest)
    extractor = load_verified_extractor(args.extractor)
    evidence = extract_final_signatures(args, extractor)
    primary = dataset_from_evidence(root, evidence, "primary")
    ood = dataset_from_evidence(root, evidence, "ood")
    if primary.x.shape != (576, DIMENSION) or len(set(primary.clusters.tolist())) != 72:
        raise RuntimeError("primary final dataset is not 576 windows / 72 runs")
    if ood.x.shape != (48, DIMENSION) or len(set(ood.clusters.tolist())) != 6:
        raise RuntimeError("OOD final dataset is not 48 windows / 6 runs")
    fault = load_evidence_bundle(args.fault_dev, expected_manifest_sha256=EXPECTED_FAULT_MANIFEST_SHA256,
                                 expected_index_sha256=EXPECTED_FAULT_INDEX_SHA256)
    normal = load_evidence_bundle(args.normal_dev, expected_manifest_sha256=EXPECTED_NORMAL_MANIFEST_SHA256,
                                  expected_index_sha256=EXPECTED_NORMAL_INDEX_SHA256)
    development = concatenate((fault, normal))
    write_json(state_path, {"schema_version": 1, "status": "training_started",
                            "training_attempt": 1, "rerun_allowed": False,
                            "development_samples": len(development.x),
                            "final_primary_samples": len(primary.x), "ood_samples": len(ood.x)})
    models = train_all_modes(development, Config())
    primary_rows = evaluate_all_modes(models, primary)
    write_metrics(root / "primary_cluster_metrics.csv", primary_rows)
    write_weight_hashes(root / "weight_hashes.json", models)
    ood_rows = ood_distribution(models, ood)
    write_csv(root / "ood_forced_attributions.csv", OOD_FIELDS, ood_rows)
    primary_summary = {
        "schema_version": 1, "scope": "72 sealed in-catalog primary runs only",
        "runs": 72, "windows": 576, "ood_included": False,
        "metrics": aggregate_primary(primary_rows),
        "cluster_metrics_sha256": sha256_file(root / "primary_cluster_metrics.csv"),
    }
    write_json(root / "PRIMARY_SUMMARY.json", primary_summary)
    ood_summary = {
        "schema_version": 1, "scope": "six sealed OOD runs, separate forced attribution only",
        "runs": 6, "windows": 48, "accuracy_defined": False,
        "structural_abstention_rate": 0.0, "direct_llm_comparison": False,
        "included_in_primary_metrics": False,
        "distribution_sha256": sha256_file(root / "ood_forced_attributions.csv"),
    }
    write_json(root / "OOD_SUMMARY.json", ood_summary)
    result = {
        "schema_version": 1, "status": "PASS", "training_attempts": 1,
        "evaluation_attempts": 1, "tuning": False, "python": platform.python_version(),
        "numpy": np.__version__, "config": Config().__dict__,
        "development_samples": len(development.x), "primary_samples": len(primary.x),
        "ood_samples": len(ood.x), "final_signatures": len(evidence),
        "artifacts": {
            name: sha256_file(root / name) for name in (
                "FINAL_SET_MANIFEST.csv", "FINAL_EVIDENCE_MANIFEST.csv",
                "primary_cluster_metrics.csv", "weight_hashes.json",
                "ood_forced_attributions.csv", "PRIMARY_SUMMARY.json", "OOD_SUMMARY.json",
            )
        },
    }
    write_json(root / "FINAL_SUMMARY.json", result)
    write_json(state_path, {"schema_version": 1, "status": "completed",
                            "training_attempt": 1, "evaluation_attempt": 1,
                            "rerun_allowed": False,
                            "final_summary_sha256": sha256_file(root / "FINAL_SUMMARY.json")})
    return result


def add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--extractor", type=Path, required=True)
    parser.add_argument("--fault-dev", type=Path, required=True)
    parser.add_argument("--normal-dev", type=Path, required=True)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--r2-guard", type=Path, required=True)
    parser.add_argument("--protocol", type=Path, required=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    before = sub.add_parser("preflight")
    add_common(before)
    before.add_argument("--repo-0311", type=Path, required=True)
    before.add_argument("--review", type=Path, required=True)
    before.add_argument("--test-root", type=Path, required=True)
    before.add_argument("--test-archive", type=Path, required=True)
    before.add_argument("--audit", type=Path, required=True)
    before.add_argument("--generation-manifest", type=Path, required=True)
    before.add_argument("--events", type=Path, required=True)
    before.add_argument("--plan", type=Path, required=True)
    before.add_argument("--runtime-log", type=Path, required=True)
    run = sub.add_parser("execute")
    add_common(run)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = preflight(args) if args.command == "preflight" else execute(args)
    print(json.dumps(result, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
