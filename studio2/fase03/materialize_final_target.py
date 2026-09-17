#!/usr/bin/env python3
"""Materialize the fresh target of the final batch. Offline; Luca runs it after the tag.

Without ``--execute`` this is a dry run: it validates every prerequisite, prints exactly
what would be created and writes nothing. It never contacts a model and never touches
``pilot-001``, ``pilot-002`` or ``pilot-03``.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from studio2.fase03.harness.common import HarnessError, canonical_json, load_json, sha256_file, sha256_text  # noqa: E402
from studio2.fase03.harness.ledger import FINAL_BATCH_PROFILE, PilotLedger  # noqa: E402
from studio2.fase03.harness import final_inventory as inventory_module  # noqa: E402
from studio2.fase03.harness.runtime import durable_write  # noqa: E402

ACK = "MATERIALIZE_PHASE03_FINAL_BATCH_TARGET"
TARGET_ID = "studio2-fase03-batch-finale-01"
DEFAULT_ROOT = Path("/Users/luker/fot-tep-runtime") / TARGET_ID
SUMMARY_PATH = ROOT / "studio2/fase03/batch_finale/INVENTARIO_SCHEDULE_7_4.json"
CANARY_PATH = ROOT / "studio2/fase03/batch_finale/CANARY_ATTESI_7_4.json"
PROTOCOL_TAG = "studio2-fase03-protocollo-finale-frozen-001"


def check_approval(path: Path) -> dict:
    """The author's written release of the tagged protocol (§7.1, step 1)."""
    approval = load_json(path)
    required = {"decision", "author", "protocol_tag", "protocol_sha256",
                "inventory_sha256", "schedule_sha256"}
    missing = required - set(approval)
    if missing:
        raise HarnessError(f"materialization approval lacks {sorted(missing)}")
    if approval["decision"] != "accepted" or not approval["author"]:
        raise HarnessError("materialization approval is not an acceptance")
    if approval["protocol_tag"] != PROTOCOL_TAG:
        raise HarnessError("materialization approval does not cover the tagged protocol")
    return approval


def plan(arguments) -> dict:
    summary = load_json(SUMMARY_PATH)
    inventory = inventory_module.build_inventory()
    schedule = inventory_module.build_schedule(inventory)
    inventory_artifact = inventory_module.inventory_artifact(inventory)
    inventory_sha256 = inventory_module.artifact_sha256(inventory_artifact)
    schedule_artifact = inventory_module.schedule_artifact(schedule, inventory_sha256=inventory_sha256)
    schedule_sha256 = inventory_module.artifact_sha256(schedule_artifact)
    if (inventory_sha256, schedule_sha256) != (summary["inventory_sha256"], summary["schedule_sha256"]):
        raise HarnessError("regenerated inventory/schedule differ from the committed summary")
    approval = check_approval(Path(arguments.approval))
    if approval["inventory_sha256"] != inventory_sha256 or approval["schedule_sha256"] != schedule_sha256:
        raise HarnessError("the approval does not cover this inventory/schedule")

    root = Path(arguments.root)
    missing = []
    prompts = Path(arguments.prompts) if arguments.prompts else None
    if prompts is None or not prompts.is_file():
        missing.append(
            "rendered prompts for the 2.244 stable identifiers: download the release "
            "studio2-fase03-test-v1, run evidence/extract_test_lot_evidence.py for the "
            "windows assigned by D1, then build_final_prompts.py")
    else:
        rendered = {json.loads(line)["prompt_id"]
                    for line in prompts.read_text(encoding="utf-8").splitlines() if line}
        absent = [row["stable_id"] for row in inventory if row["stable_id"] not in rendered]
        if absent:
            missing.append(f"{len(absent)} scheduled prompts are not rendered")
    if not arguments.config or not Path(arguments.config).is_file():
        missing.append("executable configuration of the final target with the qualified 122B identity")
    if not arguments.generation or not Path(arguments.generation).is_file():
        missing.append("frozen generation contract of the final target")
    if not arguments.canary_prompts or not Path(arguments.canary_prompts).is_file():
        missing.append("the ten frozen canary prompts of §6")
    if not arguments.tokenizer_snapshot or not Path(arguments.tokenizer_snapshot).is_dir():
        missing.append("recoverable tokenizer snapshot of the consumer service")

    return {
        "artifact_version": "MATERIALIZZAZIONE_7_4_PLAN_1",
        "target_id": arguments.target_id,
        "root": str(root),
        "ledger": {"path": str(root / "ledger.sqlite3"), "pilot_id": arguments.target_id,
                   "profile": FINAL_BATCH_PROFILE.name},
        "stage_quota": dict(sorted(FINAL_BATCH_PROFILE.base_limits.items())),
        "planned_maximum": FINAL_BATCH_PROFILE.planned_maximum,
        "hard_stop": FINAL_BATCH_PROFILE.hard_stop,
        "retry_policy": (
            "author decision D3: a retry is admitted only against proof of zero generated "
            "tokens linked to the request; a received response is never regenerated"),
        "retry_quota": FINAL_BATCH_PROFILE.retry_quota,
        "consecutive_failure_stop": FINAL_BATCH_PROFILE.consecutive_failure_stop,
        "inventory_sha256": inventory_sha256,
        "schedule_sha256": schedule_sha256,
        "approval": {"path": str(Path(arguments.approval)), "sha256": sha256_file(Path(arguments.approval))},
        "blocking_prerequisites": missing,
        "status": "READY_TO_MATERIALIZE" if not missing else "BLOCKED_MISSING_PREREQUISITES",
    }, inventory_artifact, schedule_artifact


def materialize(arguments, value, inventory_artifact, schedule_artifact) -> dict:
    if value["blocking_prerequisites"]:
        raise HarnessError("materialization blocked: " + "; ".join(value["blocking_prerequisites"]))
    root = Path(value["root"])
    if root.exists():
        raise HarnessError("the target root already exists; a fresh successor is never reused")
    root.mkdir(parents=True)
    durable_write(root / "INVENTARIO_FINALE_7_4.json", canonical_json(inventory_artifact) + "\n")
    durable_write(root / "SCHEDULE_FINALE_7_4.json", canonical_json(schedule_artifact) + "\n")
    shutil.copy2(CANARY_PATH, root / CANARY_PATH.name)
    prompts = Path(arguments.prompts)
    shutil.copy2(prompts, root / "final_prompts.jsonl")
    shutil.copy2(Path(arguments.canary_prompts), root / "canary_prompts.jsonl")
    ledger_path = root / "ledger.sqlite3"
    PilotLedger(ledger_path, pilot_id=arguments.target_id, profile=FINAL_BATCH_PROFILE.name)
    descriptor = {
        "artifact_version": "TARGET_FINALE_7_4_1",
        "target_id": arguments.target_id,
        "ledger": {"path": str(ledger_path), "pilot_id": arguments.target_id,
                   "profile": FINAL_BATCH_PROFILE.name},
        "config": {"path": str(Path(arguments.config).resolve()),
                   "sha256": sha256_file(Path(arguments.config))},
        "schedule": {"path": str(root / "SCHEDULE_FINALE_7_4.json"),
                     "sha256": sha256_file(root / "SCHEDULE_FINALE_7_4.json")},
        "prompts": {"path": str(root / "final_prompts.jsonl"),
                    "sha256": sha256_file(root / "final_prompts.jsonl")},
        "canary_expectations": {"path": str(root / CANARY_PATH.name),
                                "sha256": sha256_file(root / CANARY_PATH.name)},
        "canary_prompts": {"path": str(root / "canary_prompts.jsonl"),
                           "sha256": sha256_file(root / "canary_prompts.jsonl")},
        "tokenizer_snapshot": str(Path(arguments.tokenizer_snapshot).resolve()),
        "generation": load_json(Path(arguments.generation)),
        "results_dir": str(root / "results"),
        "inventory_sha256": value["inventory_sha256"],
        "schedule_sha256": value["schedule_sha256"],
        "approval": value["approval"],
    }
    path = root / "TARGET_FINALE_7_4.json"
    durable_write(path, json.dumps(descriptor, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
    return dict(value, status="MATERIALIZED", descriptor=str(path),
                descriptor_sha256=sha256_file(path))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-id", default=TARGET_ID)
    parser.add_argument("--root", default=str(DEFAULT_ROOT))
    parser.add_argument("--approval", required=True,
                        help="author decision releasing the tagged protocol for materialization")
    parser.add_argument("--config", default="", help="executable configuration of the final target")
    parser.add_argument("--prompts", default="", help="rendered prompts for the 2.244 identifiers")
    parser.add_argument("--canary-prompts", default="", help="the ten frozen canary prompts")
    parser.add_argument("--generation", default="", help="frozen generation contract")
    parser.add_argument("--tokenizer-snapshot", default="")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--acknowledge")
    arguments = parser.parse_args(argv)

    value, inventory_artifact, schedule_artifact = plan(arguments)
    if arguments.execute:
        if arguments.acknowledge != ACK:
            raise SystemExit(f"--execute requires --acknowledge {ACK}")
        value = materialize(arguments, value, inventory_artifact, schedule_artifact)
    else:
        value = dict(value, dry_run=True,
                     requires=f"--execute --acknowledge {ACK}")
    print(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if value.get("status") != "BLOCKED_MISSING_PREREQUISITES" else 3


if __name__ == "__main__":
    raise SystemExit(main())
