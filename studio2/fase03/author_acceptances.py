#!/usr/bin/env python3
"""03.13-ACC: verify every author acceptance before the consumer gate and freeze pre-gate inputs.

Plan-only unless ``--execute --acknowledge ACCEPT_PHASE03_PRE_GATE_INPUTS``.  Offline: no
provider call, no network.  The execution configuration and its authorization are verified,
never rewritten: every durable stage binding embeds the exact configuration, so a rewritten
configuration would itself be refused by ``d9.validate_binding`` and
``preparation.authenticate``.  What is still missing before the gate is generated here:

* the frozen source inventory (``presentation.author_decision=accepted``) and the executable
  manifest, built in-process with ``inputs.build_inventory`` under the pilot configuration;
* the prepared prompts/plan/hashes (``prepare_gate.prepare``);
* a non-normative acceptance record of the author who ran this command.

Blocking conditions that no acceptance can lift (suspension, missing stage PASS, changed
configuration) are reported by the census and refused before any write.
"""
from __future__ import annotations

import argparse
from contextlib import closing, contextmanager
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from studio2.fase03.harness.common import (HarnessError, canonical_json, load_json,  # noqa: E402
                                           sha256_file, sha256_text)

ACK = "ACCEPT_PHASE03_PRE_GATE_INPUTS"
CONFIG_NAME = "execution/pilot_d9_successor_candidate_03_13.private.json"
HANDOFF_NAME = "results/validated_insight_library_qwen_122b_primary_producer_remediation.json"
SNAPSHOT_NAME = "tokenizers/a099dee70ccfcd8d5dda56aaa0b60cb8ecadabc9"
FROZEN_INVENTORY_NAME = "execution/PILOT_INPUT_SOURCES.frozen.json"
FROZEN_MANIFEST_NAME = "execution/PILOT_INPUT_MANIFEST.frozen.json"
RECORD_NAME = "execution/PRE_GATE_ACCEPTANCE_03_13.private.json"
PREPARED_NAME = "prepared"
PREPARED_FILES = ("pilot_prompts.jsonl", "pre_gate_plan.json", "pre_gate_hashes.json")
READY = "READY_FOR_PRE_GATE_GENERATION_PROBE"
BACKUP_SUFFIX = ".pre_acceptance"


def _sha(path: Path):
    return sha256_file(path) if path.is_file() else None


def _file_hash_ok(ref):
    try:
        return isinstance(ref, dict) and Path(ref["path"]).is_file() and sha256_file(Path(ref["path"])) == ref["sha256"]
    except (KeyError, TypeError, OSError):
        return False


def _check(results, key, *, file, field, formula, verifier, ok, detail="", blocking=True):
    results.append(dict(id=key, file=str(file), key=field, hash_formula=formula, verifier=verifier,
                        status="SATISFIED" if ok else ("BLOCKING" if blocking else "INFORMATIONAL"),
                        detail=detail))


def _read_ledger(path: Path):
    """Read-only census view; never used for decisions that write."""
    uri = f"file:{path}?mode=ro&immutable=1"
    with closing(sqlite3.connect(uri, uri=True)) as c:
        events = {r[0]: json.loads(r[1]) for r in c.execute("SELECT event, detail_json FROM events")}
        stages = {r[0]: json.loads(r[1]) for r in c.execute("SELECT stage, binding_json FROM stages")}
        intents = c.execute("SELECT count(*) FROM requests WHERE status='INTENT'").fetchone()[0]
    return events, stages, intents


def census(config_path: Path, *, handoff: Path) -> list[dict[str, Any]]:
    """Every author/durable acceptance between here and the end of the gate, in order."""
    from studio2.fase03.harness.guards import require_execution
    from studio2.fase03.harness.ordering import presentation_order
    out: list[dict[str, Any]] = []
    config = load_json(config_path)
    payload = {k: v for k, v in config.items() if k != "execution_authorization"}
    d = config.get("d9") or {}
    _check(out, "C01_model_decision", file=config_path, field="study_model_decision,status",
           formula="literal APPROVED / APPROVED_FOR_PHASE03_EXECUTION", verifier="guards.require_execution",
           ok=config.get("study_model_decision") == "APPROVED"
           and config.get("status") == "APPROVED_FOR_PHASE03_EXECUTION")
    _check(out, "C02_d9_roles_status", file=config_path, field="d9.roles,d9.status,d9.missing_requirements",
           formula="literal", verifier="d9.validate_config",
           ok=d.get("status") == "DOCUMENTED_FOR_AUTHORIZED_STAGE" and d.get("missing_requirements") == [])
    try:
        ordered = presentation_order(d.get("presentation_order", []))
        approval = load_json(Path(config["presentation_approval"]["path"]))
        ok = (_file_hash_ok(config["presentation_approval"]) and approval.get("decision") == "accepted"
              and bool(approval.get("author"))
              and approval.get("ordered_labels_sha256") == sha256_text(canonical_json(ordered)))
        detail = config["presentation_approval"]["path"]
    except (HarnessError, KeyError, TypeError) as exc:
        ok, detail = False, str(exc)
    _check(out, "C03_presentation_approval", file=config_path, field="presentation_approval{path,sha256}",
           formula="sha256(file); ordered_labels_sha256=sha256(canonical_json(presentation_order(d9.presentation_order)))",
           verifier="d9.validate_config -> guards.require_presentation", ok=ok, detail=detail)
    try:
        auth = load_json(Path(config["execution_authorization"]["path"]))
        ok = (_file_hash_ok(config["execution_authorization"]) and auth.get("decision") == "accepted"
              and bool(auth.get("author"))
              and auth.get("configuration_sha256") == sha256_text(canonical_json(payload)))
        detail = f"author={auth.get('author')} scope={auth.get('scope')}"
    except (HarnessError, KeyError, TypeError) as exc:
        ok, detail = False, str(exc)
    _check(out, "C04_execution_authorization", file=config_path, field="execution_authorization{path,sha256}",
           formula="sha256(file); configuration_sha256=sha256(canonical_json(config - execution_authorization))",
           verifier="guards.require_execution", ok=ok, detail=detail)
    refs = [d.get("successor_lineage"), d.get("successor_lineage_approval")] if d.get("successor_lineage") else [d.get("history_reconciliation")]
    _check(out, "C05_lineage_or_history", file=config_path,
           field="d9.successor_lineage(+_approval) | d9.history_reconciliation",
           formula="sha256(file)", verifier="d9.validate_config", ok=all(_file_hash_ok(r) for r in refs))
    docs = [s.get("documentation") for s in (d.get("services") or {}).values()]
    _check(out, "C06_service_documentation", file=config_path, field="d9.services.*.documentation",
           formula="sha256(file)", verifier="d9.validate_config", ok=bool(docs) and all(_file_hash_ok(r) for r in docs))
    _check(out, "C07_producer_allowlist", file=config_path,
           field="approved_producer_config_sha256 == d9.producer_configs", formula="set equality",
           verifier="d9.validate_config",
           ok=set(config.get("approved_producer_config_sha256", [])) == set((d.get("producer_configs") or {}).values()))
    placement = d.get("alternate_placement")
    _check(out, "C08_alternate_placement", file=config_path, field="d9.alternate_placement",
           formula="literal pilot|deferred", verifier="d9.validate_config; d9.validate_binding(budget/stability)",
           ok=placement in {"pilot", "deferred"}, detail=str(placement))
    _check(out, "C09_pilot_go", file=config_path, field="pilot_go", formula="none",
           verifier="not checked by code (plan output only)", ok=True, detail=str(config.get("pilot_go")),
           blocking=False)
    try:
        require_execution(config)
        ok, detail = True, ""
    except (HarnessError, OSError, KeyError, TypeError) as exc:
        ok, detail = False, str(exc)
    _check(out, "C10_require_execution", file=config_path, field="(whole configuration)",
           formula="all of C01-C08 plus service/tokenizer pins", verifier="guards.require_execution", ok=ok, detail=detail)
    ledger_path = Path((config.get("pilot_ledger") or {}).get("path", ""))
    if not ledger_path.is_file():
        _check(out, "L00_ledger", file=ledger_path, field="pilot_ledger.path", formula="file exists",
               verifier="guards.require_pilot_ledger", ok=False)
        return out
    events, stages, intents = _read_ledger(ledger_path)
    stops = sorted(k for k in events if k == "stop:tokenizer_accounting" or k.startswith("stop:tokenizer_accounting#"))
    reconciled = "stop_reconciled:tokenizer_accounting" in events
    _check(out, "L01_accounting_stop", file=ledger_path, field="events stop:tokenizer_accounting[#N]",
           formula="stop_reconciled.artifact_sha256 == stop.artifact_sha256; embedded approval bytes rehashed",
           verifier="ledger._require_no_tokenizer_accounting_stop",
           ok=not stops or (stops == ["stop:tokenizer_accounting"] and reconciled),
           detail=f"stops={stops} reconciled={reconciled}")
    suspended = sorted(k for k in events if k.startswith("suspended:"))
    _check(out, "L02_not_suspended", file=ledger_path, field="events suspended:*",
           formula="absent", verifier="ledger._prerequisites (every stage) and inputs._insights",
           ok=not suspended, detail="; ".join(f"{k}: {events[k].get('reason')}" for k in suspended))
    _check(out, "L03_no_open_intent", file=ledger_path, field="requests.status=INTENT", formula="count == 0",
           verifier="runtime.execute_request (resume only)", ok=intents == 0, detail=str(intents))
    outcome = lambda stage: (events.get("outcome:" + stage) or {}).get("outcome")
    primary = "producer_remediation" if "remediation_authorized" in events else "producer_conformity"
    for key, stage, needed in [("L04_technical_pass", "technical_qualification_122b", bool(d.get("successor_lineage"))),
                               ("L05_primary_producer_pass", primary, True),
                               ("L06_alternate_pass", "alternate_conformity", placement == "pilot")]:
        _check(out, key, file=ledger_path, field="events outcome:" + stage,
               formula="outcome == PASS (re-authenticated by _closed_outcome)",
               verifier="ledger._prerequisites / d9.validate_binding",
               ok=(not needed) or outcome(stage) == "PASS", detail=f"required={needed} outcome={outcome(stage)}")
    changed = sorted(s for s, b in stages.items() if "execution_config" in b and b["execution_config"] != config)
    _check(out, "L07_binding_config_equality", file=ledger_path, field="stages.binding_json.execution_config",
           formula="== configuration file content", verifier="d9.validate_binding; preparation.authenticate",
           ok=not changed, detail=",".join(changed))
    try:
        value = load_json(handoff)
        ok = value.get("validated") is True and value.get("stage") == primary and value.get("pilot_id") == config["pilot_ledger"]["pilot_id"]
        detail = f"stage={value.get('stage')} library_sha256={value.get('library_sha256')}"
    except (HarnessError, AttributeError) as exc:
        ok, detail = False, str(exc)
    _check(out, "H01_insight_handoff", file=handoff, field="stage,pilot_id,library,library_sha256,records_sha256",
           formula="== reconstruction from durable raw responses of the primary stage",
           verifier="inputs._insights", ok=ok, detail=detail)
    for key, field, verifier in [
            ("P01_frozen_inventory", "presentation.author_decision=accepted; status=COMPLETE_READY_TO_FREEZE",
             "render.build_real_pilot_sample; preparation.authenticate"),
            ("P02_executable_manifest", "status=FROZEN_FOR_PHASE03_PRE_GATE", "preparation.authenticate"),
            ("P03_prepared_plan", f"status={READY}; pilot_id; pre_gate_hashes", "run_pilot.load_prepared"),
            ("G01_frozen_gate_config", "results/frozen_gate_config.json", "run_pilot.run_stability_stage (produced by budget stage)")]:
        _check(out, key, file="(generated)", field=field, formula="see verifier", verifier=verifier,
               ok=True, detail="generated by this script" if key.startswith("P") else "not an author acceptance",
               blocking=False)
    return out


def blocking(rows):
    return [r for r in rows if r["status"] == "BLOCKING"]


@contextmanager
def _config_path(path: Path):
    from studio2.fase03 import prepare_gate, run_pilot
    saved = prepare_gate.PREFLIGHT_CONFIG_PATH, run_pilot.PREFLIGHT_CONFIG_PATH
    prepare_gate.PREFLIGHT_CONFIG_PATH = run_pilot.PREFLIGHT_CONFIG_PATH = path
    try:
        yield
    finally:
        prepare_gate.PREFLIGHT_CONFIG_PATH, run_pilot.PREFLIGHT_CONFIG_PATH = saved


def _write_json_idempotent(path: Path, value, changes):
    data = (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    before = _sha(path)
    if before == sha256_text(data.decode("utf-8")):
        changes.append(dict(path=str(path), before=before, after=before, action="UNCHANGED"))
        return
    if before is not None:
        shutil.copy2(path, path.with_name(path.name + BACKUP_SUFFIX))
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_bytes(data)
    os.replace(tmp, path)
    changes.append(dict(path=str(path), before=before, after=_sha(path), action="WRITTEN"))


def _git_head(worktree: Path):
    try:
        return subprocess.run(["git", "-C", str(worktree), "rev-parse", "HEAD"], check=True,
                              capture_output=True, text=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def run(*, runtime: Path, worktree: Path, author: str, evidence_root: Path, execute: bool,
        config_path: Path | None = None, handoff: Path | None = None, snapshot: Path | None = None,
        normal_handoff: Path | None = None, schema_dir: Path | None = None) -> dict[str, Any]:
    runtime, worktree = Path(runtime).resolve(), Path(worktree).resolve()
    if worktree != ROOT.resolve():
        raise HarnessError(f"--worktree must be the checkout that contains this script: {ROOT}")
    if not author or not author.strip():
        raise HarnessError("author is required")
    config_path = Path(config_path or runtime / CONFIG_NAME).resolve()
    handoff = Path(handoff or runtime / HANDOFF_NAME).resolve()
    snapshot = Path(snapshot or runtime / SNAPSHOT_NAME).resolve()
    normal_handoff = Path(normal_handoff or ROOT / "studio2/fase03/baseline_numerica/NORMAL_DEV_HANDOFF.json")
    schema_dir = Path(schema_dir or ROOT / "studio2/fase03/schema_insight")
    frozen_inventory, frozen_manifest = runtime / FROZEN_INVENTORY_NAME, runtime / FROZEN_MANIFEST_NAME
    prepared, record_path = runtime / PREPARED_NAME, runtime / RECORD_NAME
    config = load_json(config_path)
    ledger_path = Path(config["pilot_ledger"]["path"])
    guarded = {"config": config_path, "execution_authorization": Path(config["execution_authorization"]["path"]),
               "presentation_approval": Path(config["presentation_approval"]["path"]),
               "insight_handoff": handoff, "ledger": ledger_path}
    touched = [frozen_inventory, frozen_manifest, *(prepared / n for n in PREPARED_FILES), record_path]
    rows = census(config_path, handoff=handoff)
    result = dict(status="PLAN_ONLY", worktree_head=_git_head(worktree), config=str(config_path),
                  census=rows, blocking=[r["id"] for r in blocking(rows)],
                  guarded_before={k: _sha(p) for k, p in guarded.items()},
                  touched_before={str(p): _sha(p) for p in touched},
                  steps=["census (read-only)", "open ledger as inputs.py does; require_execution; require_pilot_ledger",
                         "inputs.build_inventory under this configuration -> " + str(frozen_inventory),
                         "require_presentation(frozen inventory)",
                         "prepare_gate.prepare -> " + str(prepared) + " (reused if load_prepared already passes)",
                         "run_pilot.load_prepared (40 prompts)", "acceptance record -> " + str(record_path)])
    if not execute:
        return result
    if result["blocking"]:
        result["status"] = "REFUSED_BLOCKING_CONDITIONS"
        return result
    from studio2.fase03 import prepare_gate, run_pilot
    from studio2.fase03.harness import inputs
    from studio2.fase03.harness.d9 import r4_counter
    from studio2.fase03.harness.guards import (require_execution, require_pilot_ledger,
                                               require_presentation, verify_tokenizer)
    from studio2.fase03.harness.ledger import PilotLedger
    changes: list[dict[str, Any]] = []
    require_execution(config)
    verify_tokenizer(snapshot, **config["tokenizer"])
    ledger = PilotLedger(ledger_path, pilot_id=config["pilot_ledger"]["pilot_id"])
    require_pilot_ledger(config, ledger)
    raw_count = r4_counter(config, lambda *a, **k: prepare_gate.offline_token_counter(*a, **k))
    inventory, manifest = inputs.build_inventory(
        evidence_root=evidence_root, pseudolabel_path=ROOT / "studio2/fase03/pseudolabel/PSEUDOLABEL_MAP.json",
        assignment_path=ROOT / "studio2/fase03/pseudolabel/AGENT_ASSIGNMENT.json",
        derangement_path=ROOT / "studio2/fase03/pseudolabel/CONDITION_E_DERANGEMENTS.json",
        assembly_base_commit=inputs.verified_pending_inventory()["assembly_base_commit"],
        normal_handoff=normal_handoff, insight_handoff=handoff, ledger=ledger, token_count=raw_count,
        schema_dir=schema_dir, presentation_approval=config["presentation_approval"])
    if manifest is None or manifest.get("status") != "FROZEN_FOR_PHASE03_PRE_GATE":
        raise HarnessError("inventory is incomplete: " + canonical_json(inventory.get("missing_requirements")))
    require_presentation(inventory, config["presentation_approval"])
    _write_json_idempotent(frozen_inventory, inventory, changes)
    _write_json_idempotent(frozen_manifest, manifest, changes)
    with _config_path(config_path):
        reused = False
        if all((prepared / n).is_file() for n in PREPARED_FILES):
            try:
                plan = load_json(prepared / "pre_gate_plan.json")
                if (plan.get("source_inventory") == str(frozen_inventory.resolve())
                        and plan.get("insight_handoff") == str(handoff)):
                    run_pilot.load_prepared(prepared, ledger=ledger)
                    reused = True
            except (HarnessError, RuntimeError, KeyError, OSError, ValueError):
                reused = False
        if not reused:
            for name in PREPARED_FILES:
                if (prepared / name).is_file():
                    shutil.copy2(prepared / name, prepared / (name + BACKUP_SUFFIX))
            plan = prepare_gate.prepare(frozen_manifest, snapshot, prepared, source_inventory_path=frozen_inventory,
                                        insight_handoff=handoff, ledger=ledger, schema_dir=schema_dir)
            if plan["status"] != READY:
                raise HarnessError("prepared plan is not ready: " + plan["status"])
        plan, prompts = run_pilot.load_prepared(prepared, ledger=ledger)
    if len(prompts) != 40 or plan["prompt_count"] != 40:
        raise HarnessError("pre-gate sample must contain exactly 40 prompts")
    for name in PREPARED_FILES:
        changes.append(dict(path=str(prepared / name), before=result["touched_before"][str(prepared / name)],
                            after=_sha(prepared / name), action="REUSED" if reused else "WRITTEN"))
    record = dict(artifact_version="PRE_GATE_ACCEPTANCE_03_13_1", decision="accepted", author=author.strip(),
                  scope="pre-gate inputs of this pilot only; no provider call; no pilot GO",
                  pilot_id=ledger.pilot_id, worktree_head=result["worktree_head"],
                  configuration_file_sha256=sha256_file(config_path),
                  presentation_approval=config["presentation_approval"],
                  execution_authorization=config["execution_authorization"],
                  insight_handoff=dict(path=str(handoff), sha256=sha256_file(handoff)),
                  frozen_inventory=dict(path=str(frozen_inventory), sha256=sha256_file(frozen_inventory)),
                  frozen_manifest=dict(path=str(frozen_manifest), sha256=sha256_file(frozen_manifest)),
                  prepared={n: sha256_file(prepared / n) for n in ("pilot_prompts.jsonl", "pre_gate_plan.json")},
                  census=[{k: r[k] for k in ("id", "status")} for r in rows])
    existing = load_json(record_path) if record_path.is_file() else None
    if existing is not None and {k: v for k, v in existing.items() if k != "recorded_utc"} == record:
        record["recorded_utc"] = existing.get("recorded_utc")
    else:
        record["recorded_utc"] = datetime.now(timezone.utc).isoformat()
    _write_json_idempotent(record_path, record, changes)
    after = {k: _sha(p) for k, p in guarded.items() if k != "ledger"}
    if any(after[k] != result["guarded_before"][k] for k in after):
        raise HarnessError("a guarded acceptance file changed during the run")
    result.update(status=READY, prepared_dir=str(prepared), prompt_count=len(prompts), changes=changes,
                  guarded_after=dict(after, ledger=_sha(ledger_path)))
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--runtime", type=Path, required=True)
    parser.add_argument("--worktree", type=Path, required=True)
    parser.add_argument("--author", required=True)
    parser.add_argument("--evidence-root", type=Path, required=True,
                        help="extracted studio2-fase03-evidence-v2 .../studio2/fase03/evidence/output")
    parser.add_argument("--config", type=Path)
    parser.add_argument("--insight-handoff", type=Path)
    parser.add_argument("--model-snapshot", type=Path)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--acknowledge")
    args = parser.parse_args(argv)
    if args.execute and args.acknowledge != ACK:
        raise SystemExit(f"execution requires --execute --acknowledge {ACK}")
    result = run(runtime=args.runtime, worktree=args.worktree, author=args.author,
                 evidence_root=args.evidence_root, execute=args.execute, config_path=args.config,
                 handoff=args.insight_handoff, snapshot=args.model_snapshot)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if result["status"] == READY or result["status"] == "PLAN_ONLY":
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
