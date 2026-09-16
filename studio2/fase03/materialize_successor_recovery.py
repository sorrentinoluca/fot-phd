#!/usr/bin/env python3
"""Materialize the reviewed 122B successor recovery without network activity.

The target must not exist.  The predecessor is read and hashed but never opened
for writing.  No execution authorization is copied or created.
"""
from __future__ import annotations

import argparse
from contextlib import closing
from copy import deepcopy
import fcntl
import json
import os
from pathlib import Path
import shutil
import sqlite3
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from studio2.fase03.harness.common import canonical_json, sha256_file
from studio2.fase03.harness.ledger import PilotLedger
from studio2.fase03.harness.successor import build_successor_lineage_package
from studio2.fase03.technical_qualification_122b import technical_contract


PREDECESSOR_ROOT = Path("/Users/luker/fot-tep-runtime/studio2-fase03-d9-pilot-001")
PREDECESSOR_LEDGER = PREDECESSOR_ROOT / "ledger.sqlite3"
PREDECESSOR_SHA256 = "4802d7918dc063d198b799c367a9300c4ba11685cc37487c862e8a2f47bcc1eb"
PREDECESSOR_PILOT_ID = "studio2-fase03-d9-pilot-001"
TARGET_ROOT = Path("/Users/luker/fot-tep-runtime/studio2-fase03-d9-pilot-03")
SUCCESSOR_PILOT_ID = "studio2-fase03-d9-pilot-03"
EXPECTED_FINGERPRINT = "vllm-0.27.1-934a3247"
AUTHOR_DECISION_TEXT_SHA256 = "e9f4b92537c630a2fb3b476324c8811525fe4ee41a81451e0fd666f3b70b8190"
ACK = "MATERIALIZE_PHASE03_122B_SUCCESSOR_OFFLINE"

HARNESS = ROOT / "studio2/fase03/harness"
SOURCE_CONFIG = PREDECESSOR_ROOT / "execution/pilot_d9_execution_candidate_03_13.private.json"
SOURCE_PROVIDER_122B = PREDECESSOR_ROOT / "execution/producer_122b_03_13.private.json"
SOURCE_PROVIDER_27B = PREDECESSOR_ROOT / "execution/producer_27b_03_13.private.json"
SOURCE_SERVICE_27B = PREDECESSOR_ROOT / "execution/service_27b_03_13.private.json"


LEDGER_SIDECAR_SUFFIXES = ("-wal", "-shm", "-journal")


class PublishedDirectoryFsyncError(RuntimeError):
    """The target was published by rename, but the parent directory fsync failed.

    The published target is never removed or rewritten; ``published`` is always True.
    """

    def __init__(self, target: Path, result: dict, cause: OSError):
        super().__init__(
            f"successor target published at {target} but parent directory fsync failed: {cause}")
        self.target = str(target)
        self.result = result
        self.published = True


def _checkpoint_and_close_ledger(ledger_path: Path) -> None:
    """Fold the WAL into the main file, close deterministically, leave no sidecars."""
    with closing(sqlite3.connect(ledger_path)) as connection:
        busy, _, _ = connection.execute("PRAGMA wal_checkpoint(TRUNCATE)").fetchone()
        if busy:
            raise RuntimeError("successor ledger WAL checkpoint did not complete")
    for suffix in LEDGER_SIDECAR_SUFFIXES:
        sidecar = Path(str(ledger_path) + suffix)
        if not sidecar.exists():
            continue
        if suffix != "-shm" and sidecar.stat().st_size != 0:
            raise RuntimeError(f"successor ledger sidecar is not empty after checkpoint: {sidecar}")
        # Persistent-WAL SQLite builds keep empty sidecars after the last close.
        sidecar.unlink()
    _assert_no_ledger_sidecars(ledger_path)


def _assert_no_ledger_sidecars(ledger_path: Path) -> None:
    remaining = sorted(
        p.name for p in Path(ledger_path).parent.glob(Path(ledger_path).name + "-*"))
    if remaining:
        raise RuntimeError(f"successor ledger sidecars remain: {remaining}")


def _mkdir(path: Path) -> None:
    path.mkdir(mode=0o700, parents=True, exist_ok=False)
    os.chmod(path, 0o700)


def _write_bytes(path: Path, data: bytes) -> None:
    if path.exists():
        raise RuntimeError(f"refusing to overwrite {path}")
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(descriptor, "wb", closefd=False) as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
    finally:
        os.close(descriptor)
    os.chmod(path, 0o600)


def _write_json(path: Path, value: dict) -> None:
    _write_bytes(path, (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode())


def _load(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise RuntimeError(f"expected JSON object: {path}")
    return value


def _copy_tree_private(source: Path, target: Path) -> None:
    _mkdir(target)
    for child in sorted(source.iterdir()):
        destination = target / child.name
        if child.is_dir():
            _copy_tree_private(child, destination)
        elif child.is_file():
            _write_bytes(destination, child.read_bytes())
        else:
            raise RuntimeError(f"unsupported tokenizer entry: {child}")


def _ref(path: Path) -> dict[str, str]:
    return {"path": str(path.resolve()), "sha256": sha256_file(path)}


def _published_path(path: Path, staging_root: Path) -> Path:
    return TARGET_ROOT.resolve() / path.resolve().relative_to(staging_root.resolve())


def _published_ref(path: Path, staging_root: Path) -> dict[str, str]:
    return {"path": str(_published_path(path, staging_root)), "sha256": sha256_file(path)}


def _response_identity_binding() -> dict:
    """Bind identity_sha256 to the proposal object explicitly named by its review."""
    from studio2.fase03.harness import d9

    proposal = HARNESS / "PROPOSTA_RECUPERO_STOP_122B_QWEN_D9_03_13.json"
    supplement = HARNESS / "QUALIFICATION_SUPPLEMENT_122B_QWEN_D9_03_13.json"
    binding = {
        "artifact_version": "RESPONSE_IDENTITY_BINDING_1",
        "identity_sha256_semantics": d9.IDENTITY_SHA256_SEMANTICS,
        "source_proposal": _ref(proposal),
        "source_object_key": "qualification_supplement_candidate",
        "identity_sha256": d9.APPROVED_122B_IDENTITY_SHA256,
        "qualification_supplement_file": _ref(supplement),
        "qualification_supplement_canonical_sha256":
            d9.QUALIFICATION_SUPPLEMENT_CANONICAL_SHA256,
    }
    d9._validate_response_identity_binding(binding, {
        "identity_sha256": binding["identity_sha256"],
        "expected_response": {
            "returned_model": "qwen3.5-122b",
            "system_fingerprint": EXPECTED_FINGERPRINT,
        },
    })
    return binding


def _config_for_staging_validation(config: dict, staging_root: Path) -> dict:
    """Resolve only unpublished file references to staged bytes for validation."""
    staged = deepcopy(config)

    def remap(path: str) -> str:
        resolved = Path(path).resolve()
        try:
            relative = resolved.relative_to(TARGET_ROOT.resolve())
        except ValueError:
            return path
        return str((staging_root.resolve() / relative).resolve())

    staged["tokenizer_snapshot"] = remap(staged["tokenizer_snapshot"])
    staged["d9"]["r4_snapshot"] = remap(staged["d9"]["r4_snapshot"])
    for service in staged["d9"]["services"].values():
        service["documentation"]["path"] = remap(service["documentation"]["path"])
    for key in ("successor_lineage", "successor_lineage_approval"):
        staged["d9"][key]["path"] = remap(staged["d9"][key]["path"])
    return staged


def _materialize_tree(staging_root: Path) -> dict:
    staging_root = Path(staging_root).resolve()
    if not staging_root.is_dir() or any(staging_root.iterdir()):
        raise RuntimeError("materialization staging directory must exist and be empty")
    if sha256_file(PREDECESSOR_LEDGER) != PREDECESSOR_SHA256:
        raise RuntimeError("predecessor ledger SHA-256 changed before materialization")

    os.chmod(staging_root, 0o700)
    execution = staging_root / "execution"
    lineage = staging_root / "lineage"
    qualification = staging_root / "qualification"
    _mkdir(execution)
    _mkdir(lineage)
    _mkdir(qualification)
    _copy_tree_private(PREDECESSOR_ROOT / "tokenizers", staging_root / "tokenizers")

    supplement_source = HARNESS / "QUALIFICATION_SUPPLEMENT_122B_QWEN_D9_03_13.json"
    supplement = qualification / "QUALIFICATION_SUPPLEMENT_122B_QWEN_D9_03_13.private.json"
    _write_bytes(supplement, supplement_source.read_bytes())
    identity_binding = _response_identity_binding()
    identity_sha256 = identity_binding["identity_sha256"]

    evidence = {
        "stop_review_v2": _ref(HARNESS / "reviews/VERIFICA_STOP_PRIMA_CHIAMATA_PRODUCER_QWEN_D9_03_13_V2.md"),
        "proposal_md": _ref(HARNESS / "PROPOSTA_RECUPERO_STOP_122B_QWEN_D9_03_13.md"),
        "proposal_json": _ref(HARNESS / "PROPOSTA_RECUPERO_STOP_122B_QWEN_D9_03_13.json"),
        "proposal_review": _ref(HARNESS / "reviews/VERIFICA_PROPOSTA_RECUPERO_STOP_122B_QWEN_D9_03_13.md"),
        "author_decision": _ref(HARNESS / "ACQUISIZIONE_DECISIONE_AUTORE_RECUPERO_SUCCESSOR_122B_QWEN_D9_03_13.json"),
    }
    ledger_path = staging_root / "ledger.sqlite3"
    published_ledger_path = _published_path(ledger_path, staging_root)
    ledger_ref = {"path": str(published_ledger_path), "pilot_id": SUCCESSOR_PILOT_ID}
    package_value = build_successor_lineage_package(
        predecessor_path=PREDECESSOR_LEDGER,
        predecessor_pilot_id=PREDECESSOR_PILOT_ID,
        successor_ledger=ledger_ref,
        evidence=evidence,
        author_decision_text_sha256=AUTHOR_DECISION_TEXT_SHA256,
    )
    package = lineage / "SUCCESSOR_LINEAGE_S5_122B_QWEN_D9_03_13.private.json"
    _write_json(package, package_value)
    approval = lineage / "SUCCESSOR_LINEAGE_S5_122B_QWEN_D9_03_13.approval.private.json"
    _write_json(approval, {
        "artifact_version": "1",
        "author": "REDACTED_STUDY_AUTHOR",
        "decision": "SUCCESSOR_LINEAGE_IMPORT_AUTHORIZED",
        "package_sha256": sha256_file(package),
        "successor_ledger": ledger_ref,
        "author_decision": evidence["author_decision"],
    })

    published_package = _published_path(package, staging_root)
    published_approval = _published_path(approval, staging_root)
    successor = PilotLedger(
        ledger_path, pilot_id=SUCCESSOR_PILOT_ID,
        identity_path=published_ledger_path)
    successor.reconcile_successor_lineage(
        package_path=package, approval_path=approval,
        durable_package_path=published_package,
        durable_approval_path=published_approval)
    with successor._transaction() as connection:
        rows = successor._validated_predecessor_lineage(
            connection, package_path=published_package,
            approval_path=published_approval,
            source_package_path=package, source_approval_path=approval)
        native_requests = len(successor._rows(connection))
        historical_rows = len(successor._historical_rows(connection))
    if (len(rows), native_requests, historical_rows, 160 + 1 + len(rows),
            200 - (160 + 1 + len(rows))) != (5, 0, 0, 166, 34):
        raise RuntimeError("successor ledger snapshot differs from the approved S=5 budget")
    del successor
    _checkpoint_and_close_ledger(ledger_path)
    os.chmod(ledger_path, 0o600)

    old_config = _load(SOURCE_CONFIG)
    old_provider_122b = _load(SOURCE_PROVIDER_122B)
    provider_122b = deepcopy(old_provider_122b)
    provider_122b["identity_sha256"] = identity_sha256
    provider_122b["expected_response"] = {
        "returned_model": "qwen3.5-122b",
        "system_fingerprint": EXPECTED_FINGERPRINT,
    }
    provider_122b["extra_body"] = {"chat_template_kwargs": {"enable_thinking": False}}
    provider_122b_path = execution / "producer_122b_successor_03_13.private.json"
    _write_json(provider_122b_path, provider_122b)

    provider_27b_path = execution / "producer_27b_successor_03_13.private.json"
    _write_bytes(provider_27b_path, SOURCE_PROVIDER_27B.read_bytes())
    service_27b_path = execution / "service_27b_successor_03_13.private.json"
    _write_bytes(service_27b_path, SOURCE_SERVICE_27B.read_bytes())

    service_122b = {
        "artifact_version": "2",
        "status": "documented",
        "nominal_model": "122B",
        "source": (
            "identity_sha256 authenticates the canonical JSON object "
            "qualification_supplement_candidate in the pinned recovery proposal; "
            "the standalone qualification supplement has separately named file and canonical digests"),
        "validity_date": "2026-09-16",
        "weights_repository": "Qwen/Qwen3.5-122B-A10B-FP8",
        "weights_revision": "NOT_INFERRED",
        "quantization": "NOT_INFERRED",
        "serving": "NOT_INFERRED_FROM_OPAQUE_FINGERPRINT",
        "parser": "NOT_INFERRED",
        "thinking": "enable_thinking=false is an exact producer-only rendering control; consumer probe and gate retain the prespecified thinking-token-budget candidates",
        "limit_semantics": "131072 observed context limit; 4608 documented local consumer ceiling; producer max_tokens remains 2560",
        "sampling": "temperature omitted by the 122B producer; consumer candidates unchanged",
        "error_policy": "technical qualification has one charged attempt, no retry, and fail-closed suspension",
        "availability": "configuration materialized offline; service not contacted; technical qualification not executed",
        "identity_binding": deepcopy(identity_binding),
        "qualification": {
            **_published_ref(supplement, staging_root),
            "canonical_sha256": identity_binding["qualification_supplement_canonical_sha256"],
            "result": "OPAQUE_OBSERVED_IDENTITY_PENDING_ONE_CALL_TECHNICAL_QUALIFICATION",
        },
        "service": {
            "model": old_config["d9"]["services"]["122B"]["model"],
            "base_url": old_config["d9"]["services"]["122B"]["base_url"],
            "identity_sha256": identity_sha256,
            "tokenizer": deepcopy(old_config["d9"]["services"]["122B"]["tokenizer"]),
            "expected_response": deepcopy(provider_122b["expected_response"]),
            "max_model_len": old_config["d9"]["services"]["122B"]["max_model_len"],
            "max_output_tokens": old_config["d9"]["services"]["122B"]["max_output_tokens"],
        },
    }
    service_122b_path = execution / "service_122b_successor_03_13.private.json"
    _write_json(service_122b_path, service_122b)

    config = deepcopy(old_config)
    config["artifact_version"] = "D9-SUCCESSOR-CANDIDATE-03.13-PRIVATE-1"
    config["status"] = "READY_FOR_INDEPENDENT_REVIEW"
    config["study_model_decision"] = "SUCCESSOR_CONFIGURATION_APPROVED_AWAITING_EXECUTION_AUTHORIZATION"
    config["pilot_go"] = False
    config["scope"] = "SUCCESSOR_PRIVATE_CONFIGURATION_WITHOUT_EXECUTION_AUTHORIZATION"
    config["qualification"] = "ONE_CALL_TECHNICAL_QUALIFICATION_NOT_EXECUTED"
    config["execution_authorization_intentionally_absent"] = True
    config.pop("execution_authorization", None)
    config["pilot_ledger"] = ledger_ref
    config["tokenizer_snapshot"] = str(
        (TARGET_ROOT / "tokenizers" / provider_122b["tokenizer"]["revision"]).resolve())
    config["expected_response"] = deepcopy(provider_122b["expected_response"])
    config["candidate"]["expected_response"] = deepcopy(provider_122b["expected_response"])
    config["d9"]["r4_snapshot"] = str((TARGET_ROOT / "tokenizers/27B" / config["d9"]["r4_tokenizer"]["revision"]).resolve())
    config["d9"]["services"]["122B"] = deepcopy(service_122b["service"])
    config["d9"]["services"]["122B"]["documentation"] = _published_ref(
        service_122b_path, staging_root)
    config["d9"]["services"]["27B"]["documentation"] = _published_ref(
        service_27b_path, staging_root)
    config["d9"]["producer_configs"] = {
        "122B": sha256_file(provider_122b_path),
        "27B": sha256_file(provider_27b_path),
    }
    config["approved_producer_config_sha256"] = list(config["d9"]["producer_configs"].values())
    config["d9"].pop("history_reconciliation", None)
    config["d9"].pop("history_approval", None)
    config["d9"]["successor_lineage"] = _published_ref(package, staging_root)
    config["d9"]["successor_lineage_approval"] = _published_ref(approval, staging_root)
    config["d9"]["technical_qualification_122b"] = technical_contract()
    config["call_budget"].update({
        "predecessor_lineage_provider_requests_charged_once": 5,
        "predecessor_lineage_nominal_models": {"27B": 4, "122B": 1},
        "technical_qualification_122b_planned_calls": 1,
        "planned_max_without_alternate": 153,
        "planned_max_with_alternate": 161,
        "future_planned_max_with_shared_reserve": 161,
        "cumulative_base_total_with_predecessor_lineage_range": [144, 150],
        "cumulative_total_with_predecessor_lineage_and_technical_range": [145, 151],
        "cumulative_planned_max_with_predecessor_lineage_and_shared_reserve": 166,
        "hard_stop_provider_requests": 200,
        "hard_stop_margin_at_cumulative_planned_max": 34,
        "remediation_consumed": 0,
        "remediation_authorized": False,
    })
    config["call_budget"].pop("historical_provider_requests_charged_once", None)
    config["call_budget"].pop("historical_nominal_model", None)
    config["call_budget"].pop("cumulative_planned_max_with_historical_and_shared_reserve", None)
    config["call_budget"].pop("cumulative_base_total_with_historical_range", None)
    config["implementation_status"]["technical_qualification_122b"] = "IMPLEMENTED_NOT_EXECUTED"
    config_path = execution / "pilot_d9_successor_candidate_03_13.private.json"
    _write_json(config_path, config)

    from studio2.fase03.harness.d9 import validate_config
    validate_config(_config_for_staging_validation(_load(config_path), staging_root))
    if "execution_authorization" in config or any("authorization" in p.name for p in execution.iterdir()):
        raise RuntimeError("successor materialization must not contain execution authorization")
    if sha256_file(PREDECESSOR_LEDGER) != PREDECESSOR_SHA256:
        raise RuntimeError("predecessor ledger changed during materialization")

    summary_path = staging_root / "MATERIALIZATION_SUMMARY.private.json"
    _write_json(summary_path, {
        "artifact_version": "1",
        "status": "READY_FOR_INDEPENDENT_REVIEW",
        "pilot_id": SUCCESSOR_PILOT_ID,
        "predecessor": {"pilot_id": PREDECESSOR_PILOT_ID, "sha256": PREDECESSOR_SHA256},
        "ledger": _published_ref(ledger_path, staging_root),
        "configuration": _published_ref(config_path, staging_root),
        "lineage_package": _published_ref(package, staging_root),
        "lineage_approval": _published_ref(approval, staging_root),
        "qualification_supplement": _published_ref(supplement, staging_root),
        "producer_122b": _published_ref(provider_122b_path, staging_root),
        "service_122b": _published_ref(service_122b_path, staging_root),
        "budget": {"S": 5, "technical": 1, "planned_maximum": 166,
                   "hard_stop": 200, "non_spendable_margin": 34},
        "network": {"provider_calls": 0, "tokens": 0, "tunnels": 0},
        "execution_authorization": "ABSENT",
    })
    for directory in [staging_root, *[p for p in staging_root.rglob("*") if p.is_dir()]]:
        os.chmod(directory, 0o700)
    for file_path in [p for p in staging_root.rglob("*") if p.is_file()]:
        os.chmod(file_path, 0o600)
    _assert_no_ledger_sidecars(ledger_path)
    return {
        "status": "READY_FOR_INDEPENDENT_REVIEW",
        "root": str(TARGET_ROOT),
        "ledger_sha256": sha256_file(ledger_path),
        "configuration_sha256": sha256_file(config_path),
        "predecessor_sha256": sha256_file(PREDECESSOR_LEDGER),
    }


def _publish_staged(builder):
    """Build privately beside the destination, then publish once without replacement."""
    target = TARGET_ROOT.resolve()
    parent = target.parent
    if target.exists():
        raise RuntimeError(f"successor target already exists: {target}")
    parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(
        prefix=f".{target.name}.staging-", dir=str(parent))).resolve()
    result = None
    published = False
    try:
        result = builder(staging)
        lock_path = parent / f".{target.name}.publish.lock"
        lock_descriptor = os.open(lock_path, os.O_RDWR | os.O_CREAT, 0o600)
        try:
            fcntl.flock(lock_descriptor, fcntl.LOCK_EX)
            if target.exists():
                raise RuntimeError(f"successor target already exists: {target}")
            os.rename(staging, target)
            published = True
            # From here on the target is published: never remove or rewrite it.
            try:
                directory_descriptor = os.open(parent, os.O_RDONLY | os.O_DIRECTORY)
                try:
                    os.fsync(directory_descriptor)
                finally:
                    os.close(directory_descriptor)
            except OSError as exc:
                raise PublishedDirectoryFsyncError(target, result, exc) from exc
        finally:
            os.close(lock_descriptor)
        return result
    except BaseException:
        prefix = f".{target.name}.staging-"
        if (not published and staging.exists() and staging.parent == parent
                and staging.name.startswith(prefix)):
            shutil.rmtree(staging)
        raise


def materialize() -> dict:
    result = _publish_staged(_materialize_tree)
    print(canonical_json(result))
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--acknowledge")
    args = parser.parse_args(argv)
    if not args.execute or args.acknowledge != ACK:
        raise SystemExit(f"materialization requires --execute --acknowledge {ACK}")
    materialize()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
