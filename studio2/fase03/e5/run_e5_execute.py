#!/usr/bin/env python3
"""E5 execution adapter over the final-batch runner. Offline unless Luca passes --execute.

Delta after ``exp5-protocol-frozen-001``: the frozen E5 files are not touched. This file is
a thin adapter and reimplements nothing that the batch already does:

* transport, durable request lifecycle, identity STOP, retry of REVISIONE_003 and the five-
  failure STOP: ``run_final_batch.run_pass`` -> ``harness.runtime.execute_request``, unchanged;
* daily canary: ``run_final_canary.run_day`` with the **same ten prompts** and the same
  expectations of the batch (``batch_finale/CANARY_ATTESI_7_4.json``);
* pass closure: ``run_final_batch.close_pass``;
* scoring: ``harness.metrics._correct`` / ``_abstained`` over ``metric_row``, the one function
  7.5 must apply to FULL (B-LF r1-r3 of the batch) as well -- identity 6 of VERIFICA_FULL_BLF.

What is new, and only this:

* a fresh target ``studio2-fase03-e5-01`` with its own ledger. The ledger keeps the
  ``final_batch`` profile -- every rule of the batch is keyed on that name -- with an E5
  envelope: 192 slots per pass instead of 2,244 (``E5Ledger``). The envelope is recorded in
  the ledger at creation and checked at every open: the batch ledger can never be opened as
  an E5 one, nor the reverse;
* blocks ``e5_perm`` / ``e5_omit``. The condition stays ``B-LF``: an E5 prompt is a B-LF
  prompt of the batch whose ``CASE TO DIAGNOSE`` block alone was replaced (S18, re-proved at
  materialization against the carrier of the authenticated batch target). An inert PERM --
  case block unchanged by the swap -- is kept, sent and carried as ``inert`` into the
  schedule and the scores (REVISIONE_E5_001);
* the schedule: 192 prompts x R=3 (decisions A = one receiver per run, B2 = R3), one
  ``PCG64`` generator, three permutations, as in the batch; truth and strata of each slot are
  taken from the **authenticated batch schedule** (copied into the E5 target, SHA of the batch
  descriptor), cross-checked against the committed inventory;
* the configuration: the batch's own, with only the ledger and the target identity
  changed; generation contract, service and expected identity (model + fingerprint) are
  copied, so a different model or fingerprint stops E5 exactly as it stops the batch.

Never concurrent with the batch: canary and passes refuse ``--execute`` until the batch
ledger (read-only) holds ``outcome:final_batch_r3``.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
import dataclasses
import hashlib
import json
from pathlib import Path
import shutil
import sqlite3
import sys
import tempfile
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
for _p in (ROOT, ROOT / "code", HERE):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from studio2.fase03.protocol import (  # noqa: E402
    DIAGNOSTIC_SCHEMA_PATH, canonical_json, load_json, sha256_file, sha256_text,
)
from studio2.fase03.harness.common import HarnessError  # noqa: E402
from studio2.fase03.harness.final_prompts import RENDERED_ROW_KEYS  # noqa: E402
from studio2.fase03.harness.ledger import (  # noqa: E402
    FINAL_BATCH_PROFILE, FINAL_CANARY_STAGE, FINAL_PASS_STAGES, PROFILE_EVENT_PREFIX,
    UNOBSERVED_ABANDONED_PREFIX, PilotLedger, digest, load_tokenizer_accounting_guard,
)
from studio2.fase03.harness import final_inventory as inventory_module  # noqa: E402
from studio2.fase03.harness import metrics  # noqa: E402
from studio2.fase03.harness.runtime import durable_write  # noqa: E402
from studio2.fase03 import run_final_batch, run_final_canary, run_pilot  # noqa: E402
from studio2.fase03.run_final_batch import BatchStop, STOP_PREFIX  # noqa: E402

TARGET_VERSION = "TARGET_E5_1"
TARGET_ID = "studio2-fase03-e5-01"
PROTOCOL_TAG = "exp5-protocol-frozen-001"
DEFAULT_ROOT = Path("/Users/luker/fot-tep-runtime") / TARGET_ID
CANARY_EXPECTATIONS = ROOT / "studio2/fase03/batch_finale/CANARY_ATTESI_7_4.json"
DERANGEMENTS = HERE / "DERANGEMENTS_E5.json"
RECIPIENTS = HERE / "RICEVENTI_E5.json"

E5_PASS_ROWS = 192           # 96 PERM + 96 OMIT, one receiver per run (decision A)
E5_REPETITIONS = (1, 2, 3)   # decision B2
E5_CONDITION = "B-LF"
E5_LIBRARY_ROLE = "G_P"
E5_SAMPLE_ROLE = "e5_ablation"
ARM_BLOCK = {"PERM": "e5_perm", "OMIT": "e5_omit"}
CARRIER = {"block": "nucleus", "condition": "B-LF", "library_role": "G_P"}
# Protocol E5 "seeding": every seed from SHA-256, never from hash().
SCHEDULE_NAMESPACE = "studio2-fase03-e5-v1|schedule"
SCHEDULE_SEED = int.from_bytes(hashlib.sha256(SCHEDULE_NAMESPACE.encode()).digest()[:8], "big")
BATCH_CLOSED_EVENT = "outcome:" + FINAL_PASS_STAGES[-1]

ACK_MATERIALIZE = "MATERIALIZE_E5_TARGET"
ACK_CANARY = "EXECUTE_E5_CANARY"
ACK_PASS = "EXECUTE_E5_PASS"
# Top-level keys of the batch configuration E5 may change; everything else is identical.
ALLOWED_CONFIG_CHANGES = {"execution_authorization", "pilot_ledger", "call_budget", "d9",
                          "derived_from"}


# --- ledger envelope ---------------------------------------------------------------

def e5_profile(rows_per_pass: int = E5_PASS_ROWS):
    """The final_batch profile with E5 pass quotas; canary, retry and STOP rules unchanged."""
    limits = dict(FINAL_BATCH_PROFILE.base_limits)
    for stage in FINAL_PASS_STAGES:
        limits[stage] = rows_per_pass
    total = sum(limits.values()) + FINAL_BATCH_PROFILE.retry_quota
    return dataclasses.replace(FINAL_BATCH_PROFILE, base_limits=limits,
                               planned_maximum=total, hard_stop=total)


class E5Ledger(PilotLedger):
    """A ``final_batch`` ledger whose declared envelope is the E5 one, checked at every open."""

    envelope = e5_profile()

    def __init__(self, path, *, pilot_id: str = TARGET_ID, identity_path=None):
        super().__init__(Path(path), pilot_id=pilot_id, identity_path=identity_path,
                         profile=FINAL_BATCH_PROFILE.name)

    def _bind_profile(self, c):
        self.profile = self.envelope
        super()._bind_profile(c)
        row = c.execute("SELECT detail_json FROM events WHERE event=?",
                        (PROFILE_EVENT_PREFIX + self.profile.name,)).fetchone()
        declared = None if row is None else json.loads(row[0]).get("base_limits")
        if declared != dict(sorted(self.profile.base_limits.items())):
            raise HarnessError("ledger quota envelope is not the E5 one: refusing to open it as E5")


# --- inputs ----------------------------------------------------------------------

def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line]


def carriers_by_stable_id(rows) -> dict[str, dict[str, Any]]:
    return {row["stable_id"]: row for row in rows}


def load_manifest(path: Path, *, derangements=DERANGEMENTS, recipients=RECIPIENTS,
                  expected_rows: int = E5_PASS_ROWS) -> dict[str, Any]:
    """The E5 prompt manifest of ``build_e5_prompts``, validated by the frozen ``run_e5.plan``."""
    import run_e5
    plan = run_e5.plan(Path(path), E5_REPETITIONS, derangements, recipients)
    if plan["unique_prompts"] != expected_rows:
        raise HarnessError(f"E5 manifest has {plan['unique_prompts']} prompts, expected {expected_rows}")
    return load_json(Path(path))


def rendered_rows(manifest_rows, carriers) -> list[dict[str, Any]]:
    """E5 rows in the batch renderer's row format, each re-proved against its B-LF carrier."""
    from build_e5_prompts_rev1 import case_proof
    out = []
    for row in manifest_rows:
        carrier = carriers.get(row["source_stable_id"])
        if carrier is None:
            raise HarnessError(f"missing B-LF carrier {row['source_stable_id']}")
        if (any(carrier[key] != value for key, value in CARRIER.items())
                or carrier["case_id"] != row["case_id"] or carrier["agent_id"] != row["agent_id"]):
            raise HarnessError(f"carrier {carrier['stable_id']} is not the B-LF/G_P cell of {row['prompt_id']}")
        if carrier["prompt_sha256"] != sha256_text(carrier["text"]):
            raise HarnessError(f"carrier bytes changed: {carrier['stable_id']}")
        if row["prompt_sha256"] != sha256_text(row["text"]) or row["arm"] not in ARM_BLOCK:
            raise HarnessError(f"E5 row altered or of unknown arm: {row['prompt_id']}")
        proof = case_proof(carrier["text"], row["text"], arm=row["arm"])  # S18, fail-closed
        if proof["inert"] != bool(row.get("inert")):
            raise HarnessError(f"inert flag of {row['prompt_id']} contradicts its bytes (REVISIONE_E5_001)")
        text = row["text"]
        values = {"prompt_id": row["prompt_id"], "stable_id": row["stable_id"],
                  "block": ARM_BLOCK[row["arm"]], "condition": E5_CONDITION,
                  "case_id": row["case_id"], "agent_id": row["agent_id"],
                  "library_role": carrier["library_role"],
                  "available_insight_ids": carrier["available_insight_ids"],
                  "text": text, "prompt_sha256": row["prompt_sha256"],
                  "prompt_bytes": len(text.encode("utf-8"))}
        out.append({key: values[key] for key in RENDERED_ROW_KEYS})
    if len({row["prompt_id"] for row in out}) != len(out):
        raise HarnessError("E5 prompt identifiers are not unique")
    return out


TRUTH_FIELDS = ("fault", "run_index", "locality", "true_pseudolabel")


def truth_source(batch_entries, inventory=None) -> dict[str, dict[str, Any]]:
    """Per stable id, the strata and truth of the **authenticated batch schedule**.

    FULL is scored on the batch schedule, so E5 takes the same fields from the same bytes.
    The repetitions of one stable id must agree, and every cell is cross-checked against the
    committed generator: a disagreement stops, it is never resolved in favour of one side.
    """
    inventory = inventory_module.build_inventory() if inventory is None else inventory
    local = {row["stable_id"]: row for row in inventory}
    source: dict[str, dict[str, Any]] = {}
    for entry in batch_entries:
        cell = {key: entry[key] for key in ("stable_id", "block", "condition", "case_id",
                                             "recipient_agent", "library_role") + TRUTH_FIELDS}
        if source.setdefault(entry["stable_id"], cell) != cell:
            raise HarnessError(f"batch schedule disagrees with itself on {entry['stable_id']}")
    for stable_id, cell in source.items():
        reference = local.get(stable_id)
        if reference is None or any(reference[key] != cell[key] for key in cell):
            raise HarnessError(f"batch schedule differs from the committed inventory on {stable_id}")
    return source



def build_schedule(manifest_rows, source, *, expected_rows: int = E5_PASS_ROWS):
    """192 x R3; truth and strata copied from the batch schedule row of the carrier."""
    import numpy
    base = sorted(manifest_rows, key=lambda row: row["stable_id"])
    if len(base) != expected_rows:
        raise HarnessError(f"E5 schedule requires {expected_rows} prompts, got {len(base)}")
    generator = numpy.random.Generator(numpy.random.PCG64(SCHEDULE_SEED))
    schedule, position = [], 0
    for repetition in E5_REPETITIONS:
        for index in generator.permutation(len(base)):
            row = base[int(index)]
            carrier = source.get(row["source_stable_id"])
            if carrier is None or (carrier["block"], carrier["condition"], carrier["library_role"],
                                   carrier["case_id"], carrier["recipient_agent"]) != (
                    CARRIER["block"], CARRIER["condition"], CARRIER["library_role"],
                    row["case_id"], row["agent_id"]):
                raise HarnessError(f"no batch schedule cell for {row['prompt_id']}")
            position += 1
            schedule.append({
                "position": position, "repetition": repetition,
                "stable_id": row["stable_id"], "logical_id": f"{row['stable_id']}|r{repetition}",
                "block": ARM_BLOCK[row["arm"]], "condition": E5_CONDITION,
                "case_id": row["case_id"], "recipient_agent": row["agent_id"],
                "library_role": E5_LIBRARY_ROLE,
                **{key: carrier[key] for key in TRUTH_FIELDS},
                "arm": row["arm"], "family": row["family"], "donor_case_id": row["donor_case_id"],
                "source_stable_id": row["source_stable_id"], "inert": bool(row.get("inert"))})
    if len({row["logical_id"] for row in schedule}) != len(schedule):
        raise HarnessError("E5 logical identifiers are not unique")
    return schedule


def schedule_artifact(schedule, *, manifest_sha256: str) -> dict[str, Any]:
    return {"artifact_version": "SCHEDULE_E5_1", "namespace": SCHEDULE_NAMESPACE,
            "seed": SCHEDULE_SEED, "repetitions": list(E5_REPETITIONS),
            "manifest_sha256": manifest_sha256, "entries": schedule}


def e5_configuration(batch_config: dict, *, ledger_path: Path, target_id: str = TARGET_ID,
                     batch_config_sha256: str, batch_target_id: str) -> dict:
    """The batch configuration with only ledger and target identity changed."""
    config = deepcopy(batch_config)
    config.pop("execution_authorization", None)
    config["pilot_ledger"] = {"path": str(ledger_path), "pilot_id": target_id}
    final_target = config["d9"]["final_target"]
    config["d9"]["final_target"] = dict(final_target, target_id=target_id)
    profile = E5Ledger.envelope
    config["call_budget"] = {"profile": profile.name,
                             "stage_quota": dict(sorted(profile.base_limits.items())),
                             "retry_quota": profile.retry_quota,
                             "planned_maximum": profile.planned_maximum,
                             "hard_stop_provider_requests": profile.hard_stop}
    config["derived_from"] = {"batch_target_id": batch_target_id,
                              "batch_configuration_file_sha256": batch_config_sha256,
                              "protocol_tag": PROTOCOL_TAG,
                              "rule": "same service, identity and transport as the batch; "
                                      "only ledger and target identity differ"}
    changed = {key for key in set(config) | set(batch_config)
               if config.get(key) != batch_config.get(key)}
    if not changed <= ALLOWED_CONFIG_CHANGES:
        raise HarnessError(f"E5 configuration differs from the batch outside the ledger: {sorted(changed)}")
    d9_changed = {key for key in set(config["d9"]) | set(batch_config["d9"])
                  if config["d9"].get(key) != batch_config["d9"].get(key)}
    if d9_changed - {"final_target"}:
        raise HarnessError(f"E5 d9 section differs from the batch: {sorted(d9_changed)}")
    return config


def configuration_sha256(config: dict) -> str:
    payload = {k: v for k, v in config.items() if k != "execution_authorization"}
    return sha256_text(canonical_json(payload))


def authorization(*, author: str, configuration: str) -> dict[str, Any]:
    return {"artifact_version": "EXECUTION_AUTHORIZATION_E5_1", "author": author,
            "decision": "accepted", "configuration_sha256": configuration,
            "target_id": TARGET_ID, "protocol_tag": PROTOCOL_TAG,
            "scope": "E5 descriptor ablation, 576 calls on the fresh E5 target"}


def batch_closed(ledger_path: Path) -> bool:
    """Read-only: has the batch recorded the closure of its last pass?"""
    path = Path(ledger_path)
    if not path.is_file():
        return False
    connection = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    try:
        row = connection.execute("SELECT 1 FROM events WHERE event=?", (BATCH_CLOSED_EVENT,)).fetchone()
    finally:
        connection.close()
    return row is not None


def require_batch_closed(target: dict[str, Any]) -> None:
    if not batch_closed(Path(target["batch"]["ledger_path"])):
        raise BatchStop(STOP_PREFIX + f" the batch ledger has no {BATCH_CLOSED_EVENT}: "
                        "E5 never runs concurrently with the batch")


# --- rehearsal (no call, no reservation) --------------------------------------------

def rehearsal(config: dict, *, target: dict[str, Any], schedule, prompts, generation) -> dict:
    """The real D9 chain and the real canary binding on a throw-away E5 ledger; pass bindings planned."""
    from studio2.fase03.harness.guards import require_execution, require_pilot_ledger
    schema = run_pilot.vllm_grammar_schema(load_json(DIAGNOSTIC_SCHEMA_PATH))
    require_execution(config)
    with tempfile.TemporaryDirectory() as scratch:
        ledger = E5Ledger(Path(scratch).resolve() / "rehearsal.sqlite3",
                          pilot_id=config["pilot_ledger"]["pilot_id"],
                          identity_path=Path(config["pilot_ledger"]["path"]))
        require_pilot_ledger(config, ledger)
        canary = run_final_canary.canary_prompts(target)
        specs = [dict(logical_id=f"canary:day{index}:{prompt['prompt_id']}",
                      model=config["candidate"]["requested_model"], producer="consumer",
                      prompt_sha256=prompt["prompt_sha256"],
                      case_sha256=digest([prompt["agent_id"], prompt["case_id"]]),
                      contract_sha256=digest(generation), condition=prompt["condition"],
                      group=prompt["prompt_id"], repetition=1)
                 for index in range(1, run_final_canary.MAX_DAYS + 1) for prompt in canary]
        ledger.bind_stage(FINAL_CANARY_STAGE, run_final_canary.canary_binding(
            specs, config=config, schema=schema, target=target))
        # A pass binds only after a passed canary day (ledger barrier): its binding is built
        # here and checked against the envelope, not bound.
        planned = {}
        for index, stage in enumerate(FINAL_PASS_STAGES, start=1):
            rows = [row for row in schedule if row["repetition"] == index]
            binding = run_final_batch.pass_binding(rows, prompts, generation, config=config,
                                                   target=target, schema=schema, stage=stage)
            if len(binding["requests"]) != ledger.profile.base_limits[stage]:
                raise HarnessError(f"{stage}: {len(binding['requests'])} slots outside the E5 envelope")
            planned[stage] = len(binding["requests"])
        return {"canary_slots_bound": len(ledger.binding(FINAL_CANARY_STAGE)["requests"]),
                "pass_slots_planned": planned,
                "ledger": "temporary, deleted; identity of the E5 target"}


# --- materialization ---------------------------------------------------------------

def materialize(arguments) -> dict[str, Any]:
    batch_path = Path(arguments.batch_target)
    batch = run_final_batch.load_target(batch_path)  # authenticates config/schedule/prompts/canary
    if sha256_file(Path(batch["canary_prompts"]["path"])) != batch["canary_prompts"]["sha256"]:
        raise HarnessError("batch canary prompts differ from the batch target")
    if batch["canary_expectations"]["sha256"] != sha256_file(CANARY_EXPECTATIONS):
        raise HarnessError("batch canary expectations are not CANARY_ATTESI_7_4.json of the repository")
    manifest_path = Path(arguments.e5_prompts)
    manifest = load_manifest(manifest_path)
    if arguments.test_input:
        # Fail closed on any drift between the manifest and a fresh offline rebuild.
        import build_e5_prompts_rev1
        rebuilt = build_e5_prompts_rev1.build(full_prompts=Path(batch["prompts"]["path"]),
                                         test_input=Path(arguments.test_input),
                                         derangements=DERANGEMENTS, recipients=RECIPIENTS)
        if rebuilt["rows"] != manifest["rows"]:
            raise HarnessError("the E5 manifest differs from its offline rebuild on the batch carriers")
    carriers = carriers_by_stable_id(read_jsonl(Path(batch["prompts"]["path"])))
    prompts_rows = rendered_rows(manifest["rows"], carriers)
    batch_schedule_path = Path(batch["schedule"]["path"])
    schedule = build_schedule(manifest["rows"], truth_source(load_json(batch_schedule_path)["entries"]))
    root = Path(arguments.root).resolve()
    config_dir = root.parent / (root.name + ".config")
    ledger_path = root / "ledger.sqlite3"
    batch_config_path = Path(batch["config"]["path"])
    config = e5_configuration(load_json(batch_config_path), ledger_path=ledger_path,
                              batch_config_sha256=batch["config"]["sha256"],
                              batch_target_id=batch["target_id"])
    accepted = configuration_sha256(config)
    prompts_bytes = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in prompts_rows)
    schedule_bytes = canonical_json(schedule_artifact(
        schedule, manifest_sha256=sha256_file(manifest_path))) + "\n"
    summary = {"artifact_version": "MATERIALIZZAZIONE_E5_PLAN_1", "target_id": TARGET_ID,
               "root": str(root), "config_dir": str(config_dir),
               "batch_target": {"path": str(batch_path), "sha256": sha256_file(batch_path),
                                "target_id": batch["target_id"]},
               "batch_closed": batch_closed(Path(batch["ledger"]["path"])),
               "unique_prompts": len(prompts_rows), "planned_calls": len(schedule),
               "by_block": {block: sum(r["block"] == block for r in prompts_rows) for block in ARM_BLOCK.values()},
               "schedule_seed": SCHEDULE_SEED, "schedule_sha256": sha256_text(schedule_bytes),
               "prompts_file_sha256": sha256_text(prompts_bytes),
               "ledger_envelope": dict(sorted(E5Ledger.envelope.base_limits.items())),
               "configuration_sha256_to_accept": accepted,
               "expected_identity": config["expected_response"],
               "generation": batch["generation"]}

    def descriptor_for(prompts_path, schedule_path, canary_prompts_path, expectations_path, config_path):
        return {"artifact_version": TARGET_VERSION, "target_id": TARGET_ID, "protocol_tag": PROTOCOL_TAG,
                "ledger": {"path": str(ledger_path), "pilot_id": TARGET_ID,
                           "profile": FINAL_BATCH_PROFILE.name,
                           "envelope": dict(sorted(E5Ledger.envelope.base_limits.items()))},
                "config": {"path": str(config_path), "sha256": sha256_file(config_path)},
                "schedule": {"path": str(schedule_path), "sha256": sha256_file(schedule_path)},
                "prompts": {"path": str(prompts_path), "sha256": sha256_file(prompts_path)},
                "manifest": {"path": str(root / "e5_prompt_manifest.json"),
                             "sha256": sha256_file(manifest_path)},
                "canary_expectations": {"path": str(expectations_path), "sha256": sha256_file(expectations_path)},
                "canary_prompts": {"path": str(canary_prompts_path), "sha256": sha256_file(canary_prompts_path)},
                "batch_schedule": {"path": str(root / "BATCH_SCHEDULE_FINALE_7_4.json"),
                                   "sha256": batch["schedule"]["sha256"]},
                "tokenizer_snapshot": batch["tokenizer_snapshot"], "generation": batch["generation"],
                "results_dir": str(root / "results"),
                "batch": {"descriptor": summary["batch_target"], "ledger_path": batch["ledger"]["path"]}}

    # Rehearsal on files in a scratch copy of the root: same bytes, nothing real written.
    with tempfile.TemporaryDirectory() as scratch:
        s = Path(scratch)
        (s / "final.jsonl").write_text(prompts_bytes, encoding="utf-8")
        (s / "schedule.json").write_text(schedule_bytes, encoding="utf-8")
        shutil.copy2(batch["canary_prompts"]["path"], s / "canary_prompts.jsonl")
        shutil.copy2(CANARY_EXPECTATIONS, s / CANARY_EXPECTATIONS.name)
        approval = s / "authorization.json"
        approval.write_text(json.dumps(authorization(author="REHEARSAL (not an acceptance)",
                                                     configuration=accepted)), encoding="utf-8")
        rehearsed = dict(config, execution_authorization={"path": str(approval), "sha256": sha256_file(approval)})
        (s / "config.json").write_text(json.dumps(rehearsed), encoding="utf-8")
        target = descriptor_for(s / "final.jsonl", s / "schedule.json", s / "canary_prompts.jsonl",
                                s / CANARY_EXPECTATIONS.name, s / "config.json")
        prompts = load_prompts(target, label_space=run_final_batch.target_label_space(target, arguments.pilot_manifest))
        run_final_batch.executable_rows(schedule, prompts)
        summary["rehearsal"] = rehearsal(rehearsed, target=target, schedule=schedule,
                                         prompts=prompts, generation=batch["generation"])

    if not arguments.execute:
        return dict(summary, status="PLAN_ONLY",
                    requires=(f"--execute --acknowledge {ACK_MATERIALIZE} --author <name> "
                              f"--accept-configuration-sha256 {accepted}"))
    if arguments.acknowledge != ACK_MATERIALIZE:
        raise SystemExit(f"--execute requires --acknowledge {ACK_MATERIALIZE}")
    if not arguments.author or arguments.accept_configuration_sha256 != accepted:
        raise HarnessError("the author must accept exactly the configuration SHA of the plan")
    if root.exists() or config_dir.exists():
        raise HarnessError("the E5 target root already exists; a fresh target is never reused")
    root.mkdir(parents=True)
    config_dir.mkdir(parents=True)
    approval_path = config_dir / "execution_authorization.private.json"
    durable_write(approval_path, json.dumps(authorization(author=arguments.author, configuration=accepted),
                                            indent=2, ensure_ascii=False, sort_keys=True) + "\n")
    config["execution_authorization"] = {"path": str(approval_path), "sha256": sha256_file(approval_path)}
    config_path = config_dir / "execution.private.json"
    durable_write(config_path, json.dumps(config, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
    durable_write(root / "e5_prompts.jsonl", prompts_bytes)
    durable_write(root / "SCHEDULE_E5.json", schedule_bytes)
    shutil.copy2(manifest_path, root / "e5_prompt_manifest.json")
    shutil.copy2(batch_schedule_path, root / "BATCH_SCHEDULE_FINALE_7_4.json")
    shutil.copy2(batch["canary_prompts"]["path"], root / "canary_prompts.jsonl")
    shutil.copy2(CANARY_EXPECTATIONS, root / CANARY_EXPECTATIONS.name)
    E5Ledger(ledger_path)
    descriptor = descriptor_for(root / "e5_prompts.jsonl", root / "SCHEDULE_E5.json",
                                root / "canary_prompts.jsonl", root / CANARY_EXPECTATIONS.name, config_path)
    path = root / "TARGET_E5.json"
    durable_write(path, json.dumps(descriptor, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
    load_target(path)
    return dict(summary, status="MATERIALIZED", descriptor=str(path), descriptor_sha256=sha256_file(path))


# --- target, schedule and prompts at run time ----------------------------------------

def load_target(path: Path) -> dict[str, Any]:
    target = load_json(Path(path))
    if target.get("artifact_version") != TARGET_VERSION or target.get("target_id") != TARGET_ID:
        raise BatchStop(STOP_PREFIX + " not an E5 target descriptor")
    for role in ("config", "schedule", "prompts", "manifest", "canary_expectations", "canary_prompts",
                 "batch_schedule"):
        if sha256_file(Path(target[role]["path"])) != target[role]["sha256"]:
            raise BatchStop(f"{STOP_PREFIX} {role} bytes differ from the authenticated E5 target")
    if target["canary_expectations"]["sha256"] != sha256_file(CANARY_EXPECTATIONS):
        raise BatchStop(STOP_PREFIX + " E5 canary expectations are not those of the batch")
    return target


def load_schedule(target: dict[str, Any]) -> list[dict[str, Any]]:
    """Read the stored schedule and re-derive it from the stored manifest and batch schedule."""
    artifact = load_json(Path(target["schedule"]["path"]))
    manifest = load_manifest(Path(target["manifest"]["path"]))
    if artifact.get("seed") != SCHEDULE_SEED or artifact.get("namespace") != SCHEDULE_NAMESPACE:
        raise BatchStop(STOP_PREFIX + " E5 schedule seed/namespace is not the declared one")
    source = truth_source(load_json(Path(target["batch_schedule"]["path"]))["entries"])
    if artifact["entries"] != build_schedule(manifest["rows"], source):
        raise BatchStop(STOP_PREFIX + " E5 schedule differs from the deterministic generator")
    return artifact["entries"]


def load_prompts(target: dict[str, Any], *, label_space) -> dict[str, dict[str, Any]]:
    """The batch loader (hashes, renderer keys, label space), with the E5 provenance marker."""
    prompts = run_final_batch.load_prompts(target, label_space=label_space)
    for row in prompts.values():
        if row["block"] not in ARM_BLOCK.values() or row["condition"] != E5_CONDITION:
            raise BatchStop(STOP_PREFIX + f" {row['prompt_id']} is not an E5 prompt")
        row["sample_role"] = E5_SAMPLE_ROLE
    return prompts


def open_runtime(arguments, *, execute: bool, ack: str):
    from studio2.fase03.harness.guards import require_execution, require_pilot_ledger
    target = load_target(arguments.target)
    config = load_json(Path(target["config"]["path"]))
    if execute:
        if arguments.acknowledge != ack:
            raise SystemExit(f"--execute requires --acknowledge {ack}")
        require_execution(config)
        require_batch_closed(target)
    ledger = E5Ledger(Path(target["ledger"]["path"]), pilot_id=target["ledger"]["pilot_id"])
    require_pilot_ledger(config, ledger)
    guard = None
    if config["candidate"]["requested_model"] == "qwen3.5-122b":
        guard = load_tokenizer_accounting_guard(Path(target["tokenizer_snapshot"]))
    schema = run_pilot.vllm_grammar_schema(load_json(DIAGNOSTIC_SCHEMA_PATH))
    return target, config, ledger, guard, schema


# --- scoring ---------------------------------------------------------------------

def metric_row(record: dict[str, Any] | None, row: dict[str, Any]) -> dict[str, Any]:
    """One slot as ``harness.metrics`` reads it. Apply the same function to FULL in 7.5."""
    parsed = (record or {}).get("parsed_output")
    valid = bool(record and record.get("parse_valid_first_attempt") and isinstance(parsed, dict))
    value = {"valid": valid, "abstain": parsed.get("abstain") if valid else None,
             "predicted_label": parsed.get("predicted_label") if valid else None,
             "true_pseudolabel": row["true_pseudolabel"], "physical_case_id": row["case_id"]}
    return dict(value, correct=metrics._correct(value), abstained=metrics._abstained(value))


def score(target, ledger, schedule, *, partial: bool = False) -> dict[str, Any]:
    """Slot table. Refused until r1-r3 are closed, unless ``partial``: then it is marked so."""
    events = set(ledger.snapshot()["events"])
    open_passes = [stage for stage in FINAL_PASS_STAGES if "outcome:" + stage not in events]
    if open_passes and not partial:
        raise BatchStop(STOP_PREFIX + f" passes not closed: {open_passes}; scoring is for the "
                        "closed campaign (use --partial for a progress view, not analyzable)")
    rows = []
    for row in schedule:
        stage = FINAL_PASS_STAGES[row["repetition"] - 1]
        leaf = ledger.leaf(stage, row["logical_id"])
        record, status = None, "MISSING" if leaf is None else leaf["status"]
        if leaf is not None and UNOBSERVED_ABANDONED_PREFIX + leaf["request_id"] in events:
            status = "ABANDONED"
        elif status == "COMPLETED":
            record = ledger.response(leaf["request_id"])["record"]
        rows.append(dict({k: row[k] for k in ("logical_id", "stable_id", "repetition", "arm", "family",
                                               "case_id", "donor_case_id", "recipient_agent", "fault",
                                               "source_stable_id", "inert")},
                         status=status, **(metric_row(record, row) if status == "COMPLETED" else {})))
    return {"artifact_version": "E5_SLOT_SCORES_1", "target_id": target["target_id"],
            "status": "PARTIAL_NOT_ANALYZABLE" if open_passes else "CLOSED_R1_R3",
            "open_passes": open_passes,
            "scoring": "harness.metrics._correct/_abstained over run_e5_execute.metric_row",
            "slots": rows,
            "status_counts": {s: sum(r["status"] == s for r in rows) for s in sorted({r["status"] for r in rows})}}


# --- CLI -------------------------------------------------------------------------

def main(argv=None) -> int:
    from studio2.fase03.harness.guards import require_reference_environment
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    m = sub.add_parser("materialize", help="plan (default) or create the fresh E5 target")
    m.add_argument("--batch-target", type=Path, required=True, help="TARGET_FINALE_7_4.json of the batch")
    m.add_argument("--e5-prompts", type=Path, required=True, help="manifest of build_e5_prompts.py")
    m.add_argument("--test-input", type=Path, help="evidence/output_test: rebuild the manifest and compare")
    m.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    m.add_argument("--pilot-manifest", type=Path)
    m.add_argument("--author"); m.add_argument("--accept-configuration-sha256")
    for name in ("canary", "pass", "close", "score"):
        p = sub.add_parser(name)
        p.add_argument("--target", type=Path, required=True)
        if name in ("canary", "pass"):
            p.add_argument("--day"); p.add_argument("--pilot-manifest", type=Path)
        if name == "pass":
            p.add_argument("--pass-index", type=int, choices=(1, 2, 3), required=True)
            p.add_argument("--max-requests", type=int); p.add_argument("--resume", action="store_true")
        if name == "score":
            p.add_argument("--partial", action="store_true",
                           help="before r1-r3 are closed: progress view marked PARTIAL_NOT_ANALYZABLE")
        if name == "close":
            p.add_argument("--pass-index", type=int, choices=(1, 2, 3), required=True)
    for p in (m, sub.choices["canary"], sub.choices["pass"]):
        p.add_argument("--execute", action="store_true"); p.add_argument("--acknowledge")
    a = parser.parse_args(argv)
    require_reference_environment()
    try:
        if a.command == "materialize":
            value = materialize(a)
        elif a.command == "canary":
            target, config, ledger, guard, schema = open_runtime(a, execute=a.execute, ack=ACK_CANARY)
            value = run_final_canary.run_day(target=target, ledger=ledger, config=config,
                                             generation=target["generation"], schema=schema, day=a.day,
                                             results_dir=Path(target["results_dir"]), execute=a.execute,
                                             accounting_guard=guard, pilot_manifest=a.pilot_manifest)
        elif a.command == "pass":
            target, config, ledger, guard, schema = open_runtime(a, execute=a.execute, ack=ACK_PASS)
            schedule = load_schedule(target)
            prompts = load_prompts(target, label_space=run_final_batch.target_label_space(target, a.pilot_manifest))
            run_final_batch.executable_rows(schedule, prompts)
            value = run_final_batch.run_pass(
                target=target, ledger=ledger, schedule=schedule, prompts=prompts, config=config,
                generation=target["generation"], schema=schema, pass_index=a.pass_index,
                results_dir=Path(target["results_dir"]), execute=a.execute,
                max_requests=a.max_requests, resume=a.resume, accounting_guard=guard, day=a.day)
        elif a.command == "close":
            target, config, ledger, _, _ = open_runtime(a, execute=False, ack="")
            value = run_final_batch.close_pass(target=target, ledger=ledger, pass_index=a.pass_index)
        else:
            target, config, ledger, _, _ = open_runtime(a, execute=False, ack="")
            value = score(target, ledger, load_schedule(target), partial=a.partial)
            name = "E5_SLOT_SCORES.json" if not value["open_passes"] else "E5_SLOT_SCORES_PARTIAL_NOT_ANALYZABLE.json"
            out = Path(target["results_dir"]) / name
            durable_write(out, json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
            value = {"written": str(out), "status": value["status"], "status_counts": value["status_counts"]}
    except BatchStop as exc:
        print(exc, file=sys.stderr)
        return 2
    print(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
