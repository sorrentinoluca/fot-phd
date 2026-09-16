#!/usr/bin/env python3
"""Materialize the reviewed 122B successor recovery without network activity.

The target must not exist.  The predecessor is read and hashed but never opened
for writing.  No execution authorization is copied or created.
"""
from __future__ import annotations

from copy import deepcopy
import json
import os
from pathlib import Path
import shutil
import sqlite3
import sys

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
TARGET_ROOT = Path("/Users/luker/fot-tep-runtime/studio2-fase03-d9-pilot-002")
SUCCESSOR_PILOT_ID = "studio2-fase03-d9-pilot-002"
EXPECTED_FINGERPRINT = "vllm-0.27.1-934a3247"
AUTHOR_DECISION_TEXT_SHA256 = "e9f4b92537c630a2fb3b476324c8811525fe4ee41a81451e0fd666f3b70b8190"

HARNESS = ROOT / "studio2/fase03/harness"
SOURCE_CONFIG = PREDECESSOR_ROOT / "execution/pilot_d9_execution_candidate_03_13.private.json"
SOURCE_PROVIDER_122B = PREDECESSOR_ROOT / "execution/producer_122b_03_13.private.json"
SOURCE_PROVIDER_27B = PREDECESSOR_ROOT / "execution/producer_27b_03_13.private.json"
SOURCE_SERVICE_27B = PREDECESSOR_ROOT / "execution/service_27b_03_13.private.json"


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


def main() -> int:
    if TARGET_ROOT.exists():
        raise RuntimeError(f"successor target already exists: {TARGET_ROOT}")
    if sha256_file(PREDECESSOR_LEDGER) != PREDECESSOR_SHA256:
        raise RuntimeError("predecessor ledger SHA-256 changed before materialization")

    _mkdir(TARGET_ROOT)
    execution = TARGET_ROOT / "execution"
    lineage = TARGET_ROOT / "lineage"
    qualification = TARGET_ROOT / "qualification"
    _mkdir(execution)
    _mkdir(lineage)
    _mkdir(qualification)
    _copy_tree_private(PREDECESSOR_ROOT / "tokenizers", TARGET_ROOT / "tokenizers")

    supplement_source = HARNESS / "QUALIFICATION_SUPPLEMENT_122B_QWEN_D9_03_13.json"
    supplement = qualification / "QUALIFICATION_SUPPLEMENT_122B_QWEN_D9_03_13.private.json"
    _write_bytes(supplement, supplement_source.read_bytes())
    identity_sha256 = sha256_file(supplement)

    evidence = {
        "stop_review_v2": _ref(HARNESS / "reviews/VERIFICA_STOP_PRIMA_CHIAMATA_PRODUCER_QWEN_D9_03_13_V2.md"),
        "proposal_md": _ref(HARNESS / "PROPOSTA_RECUPERO_STOP_122B_QWEN_D9_03_13.md"),
        "proposal_json": _ref(HARNESS / "PROPOSTA_RECUPERO_STOP_122B_QWEN_D9_03_13.json"),
        "proposal_review": _ref(HARNESS / "reviews/VERIFICA_PROPOSTA_RECUPERO_STOP_122B_QWEN_D9_03_13.md"),
        "author_decision": _ref(HARNESS / "ACQUISIZIONE_DECISIONE_AUTORE_RECUPERO_SUCCESSOR_122B_QWEN_D9_03_13.json"),
    }
    ledger_path = TARGET_ROOT / "ledger.sqlite3"
    ledger_ref = {"path": str(ledger_path.resolve()), "pilot_id": SUCCESSOR_PILOT_ID}
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

    successor = PilotLedger(ledger_path, pilot_id=SUCCESSOR_PILOT_ID)
    successor.reconcile_successor_lineage(package_path=package, approval_path=approval)
    snapshot = successor.snapshot()
    if (snapshot["requests_cumulative"], snapshot["native_requests"],
            snapshot["predecessor_lineage_requests"], snapshot["planned_maximum_with_alternate"],
            snapshot["hard_stop_margin_at_planned_maximum"]) != (5, 0, 5, 166, 34):
        raise RuntimeError("successor ledger snapshot differs from the approved S=5 budget")
    with sqlite3.connect(ledger_path) as connection:
        connection.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    for candidate in TARGET_ROOT.glob("ledger.sqlite3*"):
        if candidate.is_file():
            os.chmod(candidate, 0o600)

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
        "source": f"opaque observed response-identity supplement {supplement}; SHA-256 {identity_sha256}",
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
        "qualification": {
            "path": str(supplement.resolve()),
            "sha256": identity_sha256,
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
    config["tokenizer_snapshot"] = str((TARGET_ROOT / "tokenizers" / provider_122b["tokenizer"]["revision"]).resolve())
    config["expected_response"] = deepcopy(provider_122b["expected_response"])
    config["candidate"]["expected_response"] = deepcopy(provider_122b["expected_response"])
    config["d9"]["r4_snapshot"] = str((TARGET_ROOT / "tokenizers/27B" / config["d9"]["r4_tokenizer"]["revision"]).resolve())
    config["d9"]["services"]["122B"] = deepcopy(service_122b["service"])
    config["d9"]["services"]["122B"]["documentation"] = _ref(service_122b_path)
    config["d9"]["services"]["27B"]["documentation"] = _ref(service_27b_path)
    config["d9"]["producer_configs"] = {
        "122B": sha256_file(provider_122b_path),
        "27B": sha256_file(provider_27b_path),
    }
    config["approved_producer_config_sha256"] = list(config["d9"]["producer_configs"].values())
    config["d9"].pop("history_reconciliation", None)
    config["d9"].pop("history_approval", None)
    config["d9"]["successor_lineage"] = _ref(package)
    config["d9"]["successor_lineage_approval"] = _ref(approval)
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
    validate_config(_load(config_path))
    if "execution_authorization" in config or any("authorization" in p.name for p in execution.iterdir()):
        raise RuntimeError("successor materialization must not contain execution authorization")
    if sha256_file(PREDECESSOR_LEDGER) != PREDECESSOR_SHA256:
        raise RuntimeError("predecessor ledger changed during materialization")

    summary_path = TARGET_ROOT / "MATERIALIZATION_SUMMARY.private.json"
    _write_json(summary_path, {
        "artifact_version": "1",
        "status": "READY_FOR_INDEPENDENT_REVIEW",
        "pilot_id": SUCCESSOR_PILOT_ID,
        "predecessor": {"pilot_id": PREDECESSOR_PILOT_ID, "sha256": PREDECESSOR_SHA256},
        "ledger": _ref(ledger_path),
        "configuration": _ref(config_path),
        "lineage_package": _ref(package),
        "lineage_approval": _ref(approval),
        "qualification_supplement": _ref(supplement),
        "producer_122b": _ref(provider_122b_path),
        "service_122b": _ref(service_122b_path),
        "budget": {"S": 5, "technical": 1, "planned_maximum": 166,
                   "hard_stop": 200, "non_spendable_margin": 34},
        "network": {"provider_calls": 0, "tokens": 0, "tunnels": 0},
        "execution_authorization": "ABSENT",
    })
    for directory in [TARGET_ROOT, *[p for p in TARGET_ROOT.rglob("*") if p.is_dir()]]:
        os.chmod(directory, 0o700)
    for file_path in [p for p in TARGET_ROOT.rglob("*") if p.is_file()]:
        os.chmod(file_path, 0o600)
    print(canonical_json({
        "status": "READY_FOR_INDEPENDENT_REVIEW",
        "root": str(TARGET_ROOT),
        "ledger_sha256": sha256_file(ledger_path),
        "configuration_sha256": sha256_file(config_path),
        "predecessor_sha256": sha256_file(PREDECESSOR_LEDGER),
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
