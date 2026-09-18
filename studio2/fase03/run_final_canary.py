#!/usr/bin/env python3
"""Daily canary of the final batch (protocol §6). Separate command, separate stage.

Ten frozen prompts per civil day Europe/Rome, before the day's first scientific lot, with
no calendar limit (REVISIONE_002): the only bound is the accounting guard of the canary
quota. The parsed pair decides; the raw hash is forensic only. An identity
change is an immediate STOP; the second marked day is a STOP pending an author decision.

Identity control (§6, rilievo C5): ``returned_model`` **and** ``system_fingerprint`` are
compared with the qualified identity on every canary call and are persisted, per prompt,
in the day's verdict event -- not only checked in memory.

A canary that fails is treated exactly like a scientific call under author decision D3:
a technical failure with proof of zero generated tokens may be retried within the batch
retry quota; a failure without that proof suspends the day and requires reconciliation; a
response that was received but is invalid is a recorded failure and is never regenerated,
so the day cannot be closed and no scientific lot may run on it.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from studio2.fase03.protocol import DIAGNOSTIC_SCHEMA_PATH, canonical_json, load_json, sha256_text  # noqa: E402
from studio2.fase03.harness.common import HarnessError  # noqa: E402
from studio2.fase03.harness import canary as canary_module  # noqa: E402
from studio2.fase03.harness.ledger import (  # noqa: E402
    CANARY_MARKED_PREFIX, CANARY_MAX_DAYS, CANARY_PASS_PREFIX, CANARY_STOP_PREFIX,
    FINAL_CANARY_STAGE,
    PilotLedger, digest, load_tokenizer_accounting_guard,
)
from studio2.fase03.harness.guards import (  # noqa: E402
    require_execution, require_pilot_ledger, require_reference_environment,
)
from studio2.fase03.harness.runtime import (  # noqa: E402
    IdentitySuspension, durable_write, execute_request,
)
from studio2.fase03 import run_pilot  # noqa: E402
from studio2.fase03.run_final_batch import (  # noqa: E402
    BatchStop, STOP_PREFIX, load_target, require_prompt_fields, resolve_civil_day,
    retry_backoff_seconds, stored_without_record, target_label_space,
)

ACK = "EXECUTE_PHASE03_FINAL_CANARY"
MAX_DAYS = CANARY_MAX_DAYS  # accounting guard (quota // 10), not a calendar limit
DAILY_CALLS = 10
ROME_OFFSET_NOTE = ("Europe/Rome civil day of this canary; it must equal the day observed "
                    "on the clock, because a canary opens the day it belongs to and never "
                    "crosses midnight (default: today)")


class CanaryProvider(run_pilot.Provider):
    ALLOWED_STAGES = {FINAL_CANARY_STAGE}


def canary_prompts(target: dict[str, Any]) -> list[dict[str, Any]]:
    """The ten frozen canary prompts, authenticated against the §6 table."""
    expectations = load_json(Path(target["canary_expectations"]["path"]))
    expected = {row["prompt_id"]: row for row in expectations["expectations"]}
    path = Path(target["canary_prompts"]["path"])
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        prompt = json.loads(line)
        if prompt["prompt_id"] not in expected:
            continue
        reference = expected[prompt["prompt_id"]]
        if sha256_text(prompt["text"]) != reference["prompt_sha256"]:
            raise BatchStop(STOP_PREFIX + f" canary prompt bytes changed: {prompt['prompt_id']}")
        prompt["prompt_sha256"] = reference["prompt_sha256"]
        rows.append(prompt)
    if len(rows) != DAILY_CALLS:
        raise BatchStop(STOP_PREFIX + f" expected {DAILY_CALLS} frozen canary prompts, found {len(rows)}")
    rows.sort(key=lambda row: row["prompt_id"])
    return rows


def canary_binding(specs, *, config, schema, target) -> dict[str, Any]:
    return dict(requests=specs, stage=FINAL_CANARY_STAGE, config_sha256=digest(config),
                execution_config=config, schema_sha256=digest(schema),
                expectations_sha256=target["canary_expectations"]["sha256"],
                tokenizer_snapshot=str(Path(target["tokenizer_snapshot"]).resolve()))


def day_state(ledger: PilotLedger) -> dict[str, list[str]]:
    events = ledger.snapshot()["events"]
    return {
        "passed": sorted(e[len(CANARY_PASS_PREFIX):] for e in events if e.startswith(CANARY_PASS_PREFIX)),
        "marked": sorted(e[len(CANARY_MARKED_PREFIX):] for e in events if e.startswith(CANARY_MARKED_PREFIX)),
        "stops": sorted(e for e in events if e.startswith(CANARY_STOP_PREFIX)),
    }


def run_day(*, target, ledger, config, generation, schema, day: str | None, results_dir: Path,
            execute: bool, provider_factory=None, accounting_guard=None,
            sleep=None, now: datetime | None = None, pilot_manifest=None) -> dict[str, Any]:
    # A canary opens the civil day it belongs to, so no crossing is admitted here: the
    # declared day must equal the observed Europe/Rome day (review rilievo B1).
    civil = resolve_civil_day(day, now=now, crossing_evidence=None)
    day, observed_day = civil["declared_day"], civil["observed_day"]
    state = day_state(ledger)
    if state["stops"]:
        raise BatchStop(STOP_PREFIX + f" canary stop in force: {state['stops']}")
    if day in state["passed"] or day in state["marked"]:
        raise BatchStop(STOP_PREFIX + f" canary day {day} already recorded")
    if len(state["passed"]) + len(state["marked"]) >= MAX_DAYS:
        raise BatchStop(STOP_PREFIX + f" the canary allowance of {MAX_DAYS} days is exhausted")

    prompts = canary_prompts(target)
    # The label space is not in the prompt file (the pilot injected it from its frozen
    # manifest at load time) and ``consumer_record`` cannot validate an answer without it.
    # Binding it here, before the plan returns, turns the plan into a real preflight: a
    # missing or altered manifest stops the day at zero calls instead of after the first.
    labels = target_label_space(target, pilot_manifest)
    for prompt in prompts:
        if "label_space" in prompt:
            raise BatchStop(STOP_PREFIX + f" canary prompt {prompt['prompt_id']} already "
                                          "carries label_space: the loader binds it")
        prompt["label_space"] = list(labels)
        # Canary rows are the pilot's own (``sample_role`` included): the same completeness
        # check as the batch, so a missing field stops the plan at zero calls.
        require_prompt_fields(prompt, source="canary")
    # The plan covers every slot of the canary quota from the start: the binding is immutable and
    # the day index, not the civil date, identifies the slot. The date lives in the event.
    day_index = len(state["passed"]) + len(state["marked"]) + 1
    specs = [dict(logical_id=f"canary:day{index}:{prompt['prompt_id']}",
                  model=config["candidate"]["requested_model"], producer="consumer",
                  prompt_sha256=prompt["prompt_sha256"],
                  case_sha256=digest([prompt["agent_id"], prompt["case_id"]]),
                  contract_sha256=digest(generation), condition=prompt["condition"],
                  group=prompt["prompt_id"], repetition=1)
             for index in range(1, MAX_DAYS + 1) for prompt in prompts]
    binding = canary_binding(specs, config=config, schema=schema, target=target)
    today = [spec for spec in specs if spec["logical_id"].startswith(f"canary:day{day_index}:")]
    if not execute:
        return {"day": day, "declared_day": day, "observed_day": observed_day,
                "day_index": day_index, "stage": FINAL_CANARY_STAGE,
                "planned": len(today), "status": "PLAN_ONLY", "state": state}

    ledger.bind_stage(FINAL_CANARY_STAGE, binding)
    provider = (provider_factory or CanaryProvider)(config)
    observations, identity_stop = [], None
    identity: dict[str, Any] = {}
    invalid: list[str] = []
    for prompt, spec in zip(prompts, today):
        messages = [{"role": "user", "content": prompt["text"]}]

        def evaluate(raw, prompt=prompt):
            return dict(run_pilot.consumer_record(raw, prompt, generation), repetition=1,
                        declared_day=day, observed_day=observed_day, midnight_crossing=False)

        leaf = ledger.leaf(FINAL_CANARY_STAGE, spec["logical_id"])
        retry_requests: tuple = ()
        from_stored = False
        if leaf is not None:
            if leaf["status"] == "COMPLETED":
                stored = ledger.response(leaf["request_id"])
                record = (stored or {}).get("record") or {}
                observations.append({"prompt_id": prompt["prompt_id"],
                                     "parsed_output": record.get("parsed_output"),
                                     "raw_response": record.get("raw_output") or ""})
                identity[prompt["prompt_id"]] = {
                    "returned_model": record.get("returned_model"),
                    "system_fingerprint": record.get("system_fingerprint"),
                    "request_id": leaf["request_id"]}
                if not isinstance(record.get("parsed_output"), dict):
                    invalid.append(prompt["prompt_id"])
                continue
            if leaf["status"] == "ZERO_TOKEN_PROVEN":
                # D3 row 1: retry admitted only against proof of zero generated tokens.
                retry_requests = (leaf["request_id"],)
                wait = retry_backoff_seconds(
                    len(ledger.attempts(FINAL_CANARY_STAGE, spec["logical_id"])))
                if wait and sleep is not None:
                    sleep(wait)
            elif stored_without_record(ledger, leaf["request_id"]):
                # The response is durable and unparsed: closing it consumes no call and the
                # day keeps the observation it already paid for.
                from_stored = True
            else:
                # D3 row 2: uncertain consumption suspends the day; no automatic resend.
                raise BatchStop(
                    STOP_PREFIX + f" uncertain canary request {leaf['request_id']} "
                    f"({leaf['status']}); reconcile it before resuming the canary")

        try:
            record = execute_request(
                ledger=ledger, stage=FINAL_CANARY_STAGE, spec=spec,
                transport=lambda transmitted=messages: provider.call(
                    prompt=prompt, messages=transmitted, schema=schema, generation=generation,
                    ledger=ledger, stage=FINAL_CANARY_STAGE, spec=spec),
                evaluate=evaluate, expected_identity=config["expected_response"],
                messages=messages, accounting_guard=accounting_guard,
                resume=bool(retry_requests) or from_stored, retry_requests=retry_requests)
        except IdentitySuspension as exc:
            # Typed, so a reworded message in runtime can never lose the durable event.
            identity_stop = {"message": str(exc), "field": exc.field,
                             "observed": exc.observed, "expected": exc.expected}
            break
        if from_stored:
            ledger.record_event("note:stored_response_evaluated:" + record["request_id"],
                                artifact_sha256=digest(record),
                                detail={"stage": FINAL_CANARY_STAGE,
                                        "logical_id": spec["logical_id"],
                                        "reason": "durable raw response evaluated without transport"})
        identity[prompt["prompt_id"]] = {
            "returned_model": record.get("returned_model"),
            "system_fingerprint": record.get("system_fingerprint"),
            "request_id": record.get("request_id")}
        if not isinstance(record.get("parsed_output"), dict):
            # D3 row 3: received but invalid. Recorded, never regenerated.
            invalid.append(prompt["prompt_id"])
        observations.append({"prompt_id": prompt["prompt_id"],
                             "parsed_output": record.get("parsed_output"),
                             "raw_response": record.get("raw_output") or ""})

    if identity_stop is not None:
        ledger.record_canary_stop(
            day, reason="returned_model or system_fingerprint changed",
            detail=dict(identity_stop, day_index=day_index, identity=identity,
                        declared_day=day, observed_day=observed_day),
            observed_day=observed_day)
        raise BatchStop(
            STOP_PREFIX + f" canary identity change on {day} "
            f"({identity_stop['field']}): {identity_stop['message']}")

    if invalid:
        # C5 under D3: the day is neither PASS nor MARKED, so the barrier of §7.1 step 3
        # keeps every scientific lot of this day closed until the author decides.
        durable_write(results_dir / f"canary_{day}_invalid.json",
                      json.dumps({"day": day, "declared_day": day,
                                  "observed_day": observed_day, "day_index": day_index,
                                  "invalid_prompt_ids": sorted(invalid),
                                  "identity": identity,
                                  "rule": "D3: a received but invalid response is never "
                                          "regenerated; the canary day cannot be closed"},
                                 indent=2, ensure_ascii=False, sort_keys=True) + "\n")
        raise BatchStop(
            STOP_PREFIX + f" canary day {day} has {len(invalid)} invalid responses "
            f"({sorted(invalid)}); D3 forbids regeneration, the day stays unclosed and no "
            "scientific lot may run on it: author decision required")

    comparison = canary_module.compare_run(Path(target["canary_expectations"]["path"]), observations)
    outcome = dict(day=day, declared_day=day, observed_day=observed_day,
                   day_index=day_index, marked=comparison["marked_day"],
                   behavior_changes=comparison["behavior_changes"],
                   raw_hash_changes=comparison["raw_hash_changes"],
                   comparison_sha256=comparison["comparison_sha256"],
                   details=comparison["details"])
    durable_write(results_dir / f"canary_{day}.json",
                  json.dumps(outcome, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
    verdict = "MARKED" if comparison["marked_day"] else "PASS"
    ledger.record_canary_day(day, verdict=verdict, comparison=comparison,
                             expectations_sha256=target["canary_expectations"]["sha256"],
                             identity=identity, observed_day=observed_day)
    outcome["verdict"] = verdict
    outcome["identity"] = identity
    if verdict == "MARKED":
        state = day_state(ledger)
        if state["stops"]:
            raise BatchStop(
                STOP_PREFIX + f" second marked canary day ({state['marked']}); author decision required")
    return outcome


def main(argv=None) -> int:
    require_reference_environment()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--day", help=ROME_OFFSET_NOTE)
    parser.add_argument("--pilot-manifest", type=Path,
                        help="frozen pilot input manifest that carries the label space "
                             "(default: beside the tokenizer snapshot of the target)")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--acknowledge")
    arguments = parser.parse_args(argv)

    target = load_target(arguments.target)
    config = load_json(Path(target["config"]["path"]))
    schema = run_pilot.vllm_grammar_schema(load_json(DIAGNOSTIC_SCHEMA_PATH))
    if arguments.execute:
        if arguments.acknowledge != ACK:
            raise SystemExit(f"--execute requires --acknowledge {ACK}")
        require_execution(config)
    ledger = PilotLedger(Path(target["ledger"]["path"]), pilot_id=target["ledger"]["pilot_id"],
                         profile=target["ledger"]["profile"])
    require_pilot_ledger(config, ledger)
    accounting_guard = None
    if config["candidate"]["requested_model"] == "qwen3.5-122b":
        accounting_guard = load_tokenizer_accounting_guard(Path(target["tokenizer_snapshot"]))
    outcome = run_day(target=target, ledger=ledger, config=config, generation=target["generation"],
                      schema=schema, day=arguments.day,
                      results_dir=Path(target["results_dir"]), execute=arguments.execute,
                      accounting_guard=accounting_guard, pilot_manifest=arguments.pilot_manifest)
    print(json.dumps(dict(outcome, state=day_state(ledger)), indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
