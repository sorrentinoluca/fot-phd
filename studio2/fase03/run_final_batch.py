#!/usr/bin/env python3
"""Runner of the final scientific batch (protocol §4-§7).

Reuses the pilot machinery unchanged: ``harness.ledger.PilotLedger`` under its
``final_batch`` quota profile, ``harness.runtime.execute_request`` for the durable
request lifecycle, ``run_pilot.Provider`` for transport and ``run_pilot.consumer_record``
for parsing. Only the schedule walk, the progress view and the STOP rules of §7.2 are new.

Without ``--execute`` nothing is sent: the command validates every prerequisite, prints
the plan and exits.

Retry and STOP follow author decision D3 (2026-09-17), which replaces the absolute
``Q=0`` of the candidate:

* a technical error **with proof that no token was generated** (``reconcile_zero_token``)
  may be retried, within a separate cumulative quota and after an increasing wait;
* a timeout without that proof suspends the slot and requires reconciliation -- never an
  automatic resend;
* a response that was generated but is invalid or truncated is a recorded failure and is
  never regenerated;
* a valid but wrong or abstaining response is a definitive scientific outcome;
* five consecutive failed technical attempts on the same service -- retries included,
  counted persistently in the ledger -- stop the campaign, as do permanent errors, an
  identity change and any uncertain consumption.
"""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import date, datetime, timedelta, timezone
import json
from pathlib import Path
import sys
import time
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from studio2.fase03.protocol import (  # noqa: E402
    DIAGNOSTIC_SCHEMA_PATH, canonical_json, load_json, sha256_file, sha256_text,
)
from studio2.fase03.harness.common import HarnessError  # noqa: E402
from studio2.fase03.harness.ledger import (  # noqa: E402
    CANARY_MARKED_PREFIX, CANARY_PASS_PREFIX, CANARY_STOP_PREFIX, FINAL_PASS_STAGES,
    FINAL_CONSECUTIVE_FAILURE_STOP, FINAL_RETRY_QUOTA,
    PilotLedger, digest, load_tokenizer_accounting_guard,
)
from studio2.fase03.harness.canary_marking import rome_day  # noqa: E402
from studio2.fase03.harness.guards import require_execution, require_pilot_ledger  # noqa: E402
from studio2.fase03.harness.runtime import durable_write, execute_request  # noqa: E402
from studio2.fase03.harness import final_inventory as inventory_module  # noqa: E402
from studio2.fase03 import protocol_bnolf  # noqa: E402
from studio2.fase03 import run_pilot  # noqa: E402

ACK = "EXECUTE_PHASE03_FINAL_BATCH"
# A, B-LF and E-LF come from the frozen renderer of §2; B-noLF from its tracked revision
# ``protocol_bnolf.py`` (author decision D2).
RENDERABLE_CONDITIONS = protocol_bnolf.FINAL_CONDITIONS
STOP_PREFIX = "STOP:"
# D3: increasing wait between technical attempts on the same logical request.
RETRY_BACKOFF_BASE_SECONDS = 30.0
RETRY_BACKOFF_CAP_SECONDS = 900.0


class BatchStop(HarnessError):
    """Every §7.2 stop condition raised by the runner itself."""


class BatchProvider(run_pilot.Provider):
    ALLOWED_STAGES = set(FINAL_PASS_STAGES)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def retry_backoff_seconds(previous_attempts: int) -> float:
    """Increasing wait before the n-th technical attempt (D3): 30 s, 60 s, 120 s ... capped."""
    if previous_attempts < 1:
        return 0.0
    return min(RETRY_BACKOFF_BASE_SECONDS * (2 ** (previous_attempts - 1)),
               RETRY_BACKOFF_CAP_SECONDS)


def load_target(path: Path) -> dict[str, Any]:
    """Authenticate the target descriptor and every file it binds."""
    target = load_json(path)
    if target.get("artifact_version") != "TARGET_FINALE_7_4_1":
        raise BatchStop(STOP_PREFIX + " unknown target descriptor version")
    for role in ("config", "schedule", "prompts", "canary_expectations"):
        reference = target[role]
        observed = sha256_file(Path(reference["path"]))
        if observed != reference["sha256"]:
            raise BatchStop(f"{STOP_PREFIX} {role} bytes differ from the authenticated target")
    return target


def load_schedule(target: dict[str, Any]) -> list[dict[str, Any]]:
    """Read the schedule and re-derive it from the committed generator."""
    artifact = load_json(Path(target["schedule"]["path"]))
    entries = artifact["entries"]
    regenerated = inventory_module.build_schedule(inventory_module.build_inventory())
    if [row["logical_id"] for row in entries] != [row["logical_id"] for row in regenerated]:
        raise BatchStop(STOP_PREFIX + " schedule differs from the deterministic generator")
    if artifact["seed"] != inventory_module.SCHEDULE_SEED or artifact["namespace"] != inventory_module.SCHEDULE_NAMESPACE:
        raise BatchStop(STOP_PREFIX + " schedule seed/namespace is not the pre-registered one")
    return entries


def load_prompts(target: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Read the rendered prompts and check every prompt hash against its own bytes."""
    path = Path(target["prompts"]["path"])
    prompts: dict[str, dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        row = json.loads(line)
        if row["prompt_sha256"] != sha256_text(row["text"]):
            raise BatchStop(STOP_PREFIX + f" prompt bytes changed: {row.get('prompt_id')}")
        prompts[row["prompt_id"]] = row
    return prompts


def executable_rows(schedule: list[dict[str, Any]], prompts: dict[str, dict[str, Any]]) -> None:
    """Fail closed on any scheduled row this harness cannot render or log.

    The four arms of §4 are renderable: A, B-LF and E-LF by the frozen renderer of §2,
    B-noLF by its tracked revision ``protocol_bnolf.py`` (author decision D2), and all
    four are admitted by the §8.7 call-record contract. Any other condition is refused
    here rather than silently reinterpreted.
    """
    unsupported = sorted({row["condition"] for row in schedule
                          if row["condition"] not in RENDERABLE_CONDITIONS})
    if unsupported:
        raise BatchStop(
            STOP_PREFIX + " the schedule contains conditions the frozen renderer does not "
            f"produce: {unsupported}; see REPORT_7_4_PREP.md open point 1")
    missing = [row["stable_id"] for row in schedule if row["stable_id"] not in prompts]
    if missing:
        raise BatchStop(STOP_PREFIX + f" {len(missing)} scheduled prompts are not materialized")


def batch_spec(row: dict[str, Any], prompt: dict[str, Any], generation: dict[str, Any],
               *, config: dict[str, Any]) -> dict[str, Any]:
    return dict(logical_id=row["logical_id"], model=config["candidate"]["requested_model"],
                producer="consumer", prompt_sha256=prompt["prompt_sha256"],
                case_sha256=digest([row["recipient_agent"], row["case_id"]]),
                contract_sha256=digest(generation), condition=row["condition"],
                group=row["stable_id"], repetition=row["repetition"])


def pass_binding(rows, prompts, generation, *, config, target, schema, stage) -> dict[str, Any]:
    specs = [batch_spec(row, prompts[row["stable_id"]], generation, config=config) for row in rows]
    return dict(requests=specs, stage=stage,
                config_sha256=digest(config), execution_config=config,
                schedule_sha256=target["schedule"]["sha256"],
                prompts_sha256=target["prompts"]["sha256"],
                schema_sha256=digest(schema),
                tokenizer_snapshot=str(Path(target["tokenizer_snapshot"]).resolve()))


def canary_state(ledger: PilotLedger) -> dict[str, Any]:
    events = ledger.snapshot()["events"]
    return {
        "passed_days": sorted(e[len(CANARY_PASS_PREFIX):] for e in events if e.startswith(CANARY_PASS_PREFIX)),
        "marked_days": sorted(e[len(CANARY_MARKED_PREFIX):] for e in events if e.startswith(CANARY_MARKED_PREFIX)),
        "stops": sorted(e for e in events if e.startswith(CANARY_STOP_PREFIX)),
    }


MIDNIGHT_CROSSING_RULE = (
    "a lot may run past midnight only as the continuation of a lot already begun on the "
    "declared day: the observed Europe/Rome day must be the calendar day immediately after "
    "the declared one, and the stage must already hold a request completed on the declared "
    "day. Every other mismatch is a STOP.")


def _is_next_day(declared: str, observed: str) -> bool:
    return date.fromisoformat(observed) - date.fromisoformat(declared) == timedelta(days=1)


def stage_began_on(ledger: PilotLedger, stage: str, day: str) -> bool:
    """True when this stage already completed a request on that civil day."""
    for instant in ledger.completion_instants(stage):
        moment = datetime.fromisoformat(instant.replace("Z", "+00:00"))
        if rome_day(moment) == day:
            return True
    return False


def resolve_civil_day(declared: str | None, *, now: datetime | None = None,
                      crossing_evidence=None) -> dict[str, Any]:
    """Bind the declared civil day to the clock (review rilievo B1).

    ``--day`` exists for the one legitimate case, a lot that crosses midnight, and until
    now nothing compared it with the clock: a canary passed for day X and a lot launched
    with ``--day X`` on another day satisfied the barrier. Both values are returned so the
    caller persists them in the event and in every record.

    ``crossing_evidence`` is a zero-argument callable, evaluated only when the two days
    differ, that proves the lot really began on the declared day. Passing ``None``
    forbids the crossing outright, which is what the canary does: a canary opens the day.
    """
    observed = rome_day(now or datetime.now(timezone.utc))
    if declared is None:
        return {"declared_day": observed, "observed_day": observed, "midnight_crossing": False}
    try:
        date.fromisoformat(declared)
    except ValueError as exc:
        raise BatchStop(STOP_PREFIX + f" --day {declared!r} is not an ISO civil date") from exc
    if declared == observed:
        return {"declared_day": declared, "observed_day": observed, "midnight_crossing": False}
    if (crossing_evidence is not None and _is_next_day(declared, observed)
            and crossing_evidence()):
        return {"declared_day": declared, "observed_day": observed, "midnight_crossing": True}
    raise BatchStop(
        STOP_PREFIX + f" declared day {declared} differs from the observed Europe/Rome day "
        f"{observed}. " + MIDNIGHT_CROSSING_RULE)


def require_canary_ok(ledger: PilotLedger, day: str | None = None) -> dict[str, Any]:
    """The canary->lot barrier of §6: no scientific call outside a passed canary day.

    Three conditions, checked before *every* request, not only at the start of a pass:
    no canary STOP in force, at least one passed day (§7.1 order, step 3) and a canary
    PASS recorded for the civil day this call belongs to, because §6 requires the daily
    canary before the day's first scientific lot.
    """
    state = canary_state(ledger)
    if state["stops"]:
        raise BatchStop(STOP_PREFIX + f" canary stop in force: {state['stops']}")
    if not state["passed_days"]:
        raise BatchStop(STOP_PREFIX + " no canary day has passed yet (§7.1 order, step 3)")
    if len(state["marked_days"]) >= 2:
        raise BatchStop(STOP_PREFIX + " second marked canary day: author decision required (§6.4)")
    today = day or rome_day(datetime.now(timezone.utc))
    # ``day`` reaches here already bound to the clock by resolve_civil_day.
    if today not in state["passed_days"]:
        raise BatchStop(
            STOP_PREFIX + f" no canary PASS recorded for {today}: §6 requires the daily "
            "canary before the day's first scientific lot")
    return dict(state, barrier_day=today)


class Progress:
    """Readable, per-pass progress with a sequential ETA."""

    def __init__(self, stage: str, total: int, done: int) -> None:
        self.stage, self.total, self.done = stage, total, done
        self.invalid = self.abstained = self.sent = 0
        self.latencies: list[float] = []

    def observe(self, record: dict[str, Any]) -> None:
        self.done += 1
        self.sent += 1
        if not record.get("parse_valid_first_attempt"):
            self.invalid += 1
        parsed = record.get("parsed_output")
        if isinstance(parsed, dict) and parsed.get("abstain") is True:
            self.abstained += 1
        latency = record.get("latency_seconds")
        if isinstance(latency, (int, float)):
            self.latencies.append(float(latency))

    def skip(self) -> None:
        self.done += 1

    def line(self) -> str:
        mean = sum(self.latencies) / len(self.latencies) if self.latencies else None
        remaining = self.total - self.done
        eta = "n/a" if mean is None else f"{remaining * mean / 3600:.1f}h"
        mean_text = "n/a" if mean is None else f"{mean:.1f}s"
        return (f"{self.stage} {self.done}/{self.total} sent={self.sent} "
                f"invalid={self.invalid} abstain={self.abstained} mean={mean_text} eta={eta}")


def _call_record(row: dict[str, Any], prompt: dict[str, Any], record: dict[str, Any],
                 *, generation: dict[str, Any], config: dict[str, Any], attempt: int):
    from studio2.fase03.harness.logging_v1 import CallRecord

    return CallRecord.create(
        prompt_id=row["logical_id"], agent_id=row["recipient_agent"],
        physical_case_id=row["case_id"], condition=row["condition"],
        repetition=row["repetition"], attempt=attempt, timestamp_utc=record["received_utc"],
        provider=config["candidate"]["provider"], requested_model=config["candidate"]["requested_model"],
        returned_model=record["returned_model"] or "",
        returned_model_revision=config["candidate"].get("expected_model_revision"),
        request_id=record["request_id"], system_fingerprint=record["system_fingerprint"],
        temperature_supported=None, seed_supported="seed" in generation,
        generation=generation, prompt_sha256=record["prompt_sha256"],
        prompt_bytes=len(prompt["text"].encode("utf-8")), raw_response=record["raw_output"],
        latency_ms=(record["latency_seconds"] or 0.0) * 1000,
        prompt_tokens=record.get("prompt_tokens"), completion_tokens=record.get("completion_tokens"),
        total_tokens=record.get("total_tokens"), token_source="provider_usage",
        finish_reason=record.get("finish_reason"),
        truncated=record.get("finish_reason") == "length",
        parse_valid=bool(record.get("parse_valid_first_attempt")),
        schema_valid=bool(record.get("parse_valid_first_attempt")),
        parsed_output=record.get("parsed_output"),
        error=None if record.get("parse_error") is None else {"parse_error": record["parse_error"]},
    )


def run_pass(*, target, ledger, schedule, prompts, config, generation, schema, pass_index,
             results_dir: Path, execute: bool, max_requests: int | None, resume: bool = False,
             provider_factory=None, accounting_guard=None, sleep=time.sleep,
             day: str | None = None, now: datetime | None = None) -> dict[str, Any]:
    stage = FINAL_PASS_STAGES[pass_index - 1]
    rows = [row for row in schedule if row["repetition"] == pass_index]
    binding = pass_binding(rows, prompts, generation, config=config, target=target,
                           schema=schema, stage=stage)
    ledger.bind_stage(stage, binding)
    stage_run = digest(binding)

    existing = sum(ledger.leaf(stage, row["logical_id"]) is not None for row in rows)
    progress = Progress(stage, len(rows), 0)
    if not execute:
        return {"stage": stage, "planned": len(rows), "already_recorded": existing,
                "stage_run": stage_run, "status": "PLAN_ONLY"}
    if existing and not resume:
        raise BatchStop(STOP_PREFIX + " the pass already has recorded requests; "
                        "continue it with --resume, which never resends a terminal slot")

    civil = resolve_civil_day(day, now=now,
                              crossing_evidence=lambda: stage_began_on(ledger, stage, day))
    day = civil["declared_day"]
    require_canary_ok(ledger, day)
    provider = (provider_factory or BatchProvider)(config)
    log_path = results_dir / f"{stage}_call_log.jsonl"
    from studio2.fase03.harness.logging_v1 import JsonlCallLogger
    logger = JsonlCallLogger(log_path, create=not log_path.is_file())

    sent = 0
    retried = 0
    used_insight_ids: Counter = Counter()
    for row in rows:
        leaf = ledger.leaf(stage, row["logical_id"])
        retry_requests: tuple = ()
        if leaf is not None:
            if leaf["status"] == "COMPLETED":
                # A received response is terminal: valid, invalid or truncated, it is an
                # outcome and is never regenerated (D3, rows 3 and 4).
                progress.skip()
                continue
            if leaf["status"] == "ZERO_TOKEN_PROVEN":
                # D3, row 1: the only admitted retry, against proof -- linked to this very
                # request -- that no token was generated, reasoning included.
                retry_requests = (leaf["request_id"],)
            else:
                # D3, row 2: uncertain consumption is suspended, never resent automatically.
                raise BatchStop(
                    STOP_PREFIX + f" uncertain request {leaf['request_id']} ({leaf['status']}); "
                    "reconcile it with ledger_cli reconcile-zero-token before resuming")
        if max_requests is not None and sent >= max_requests:
            break
        if retry_requests:
            wait = retry_backoff_seconds(len(ledger.attempts(stage, row["logical_id"])))
            if wait and sleep is not None:
                sleep(wait)
            retried += 1
        civil = resolve_civil_day(day, now=now,
                                  crossing_evidence=lambda: stage_began_on(ledger, stage, day))
        require_canary_ok(ledger, day)
        prompt = prompts[row["stable_id"]]
        spec = next(s for s in binding["requests"] if s["logical_id"] == row["logical_id"])
        messages = [{"role": "user", "content": prompt["text"]}]

        def evaluate(raw, prompt=prompt, civil=civil):
            return dict(run_pilot.consumer_record(raw, prompt, generation),
                        repetition=row["repetition"], stable_id=row["stable_id"],
                        block=row["block"], library_role=row["library_role"],
                        declared_day=civil["declared_day"],
                        observed_day=civil["observed_day"],
                        midnight_crossing=civil["midnight_crossing"])

        record = execute_request(
            ledger=ledger, stage=stage, spec=spec,
            transport=lambda transmitted=messages: provider.call(
                prompt=prompt, messages=transmitted, schema=schema, generation=generation,
                ledger=ledger, stage=stage, spec=spec),
            evaluate=evaluate, expected_identity=config["expected_response"],
            messages=messages, accounting_guard=accounting_guard,
            resume=bool(retry_requests), retry_requests=retry_requests)
        sent += 1
        progress.observe(record)
        logger.append(_call_record(row, prompt, record, generation=generation,
                                   config=config,
                                   attempt=len(ledger.attempts(stage, row["logical_id"]))))
        parsed = record.get("parsed_output")
        if isinstance(parsed, dict):
            used_insight_ids.update(parsed.get("used_insight_ids") or [])
        durable_write(results_dir / f"{stage}_record_{record['request_id']}.json",
                      canonical_json(record) + "\n")
        print(progress.line(), flush=True)

    snapshot = ledger.snapshot()
    summary = {"stage": stage, "planned": len(rows), "completed": progress.done,
               "declared_day": civil["declared_day"], "observed_day": civil["observed_day"],
               "midnight_crossing": civil["midnight_crossing"],
               "midnight_crossing_rule": MIDNIGHT_CROSSING_RULE,
               "sent_this_run": sent, "retries_this_run": retried,
               "retry_quota": FINAL_RETRY_QUOTA,
               "retry_quota_used": snapshot.get("retry_quota_used", 0),
               "consecutive_technical_failures": snapshot.get("consecutive_technical_failures", {}),
               "consecutive_failure_stop": FINAL_CONSECUTIVE_FAILURE_STOP,
               "invalid": progress.invalid,
               "abstained": progress.abstained, "stage_run": stage_run,
               "t9_used_insight_ids": dict(sorted(used_insight_ids.items())),
               "status": "COMPLETE" if progress.done == len(rows) else "PARTIAL"}
    durable_write(results_dir / f"{stage}_summary.json",
                  json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
    return summary


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--pass-index", type=int, choices=(1, 2, 3), required=True)
    parser.add_argument("--max-requests", type=int)
    parser.add_argument("--resume", action="store_true",
                        help="continue an interrupted pass; terminal slots are skipped, never resent")
    parser.add_argument("--day", help="civil day Europe/Rome this lot belongs to; the canary "
                                      "of that day must have passed, and the declared day is "
                                      "checked against the clock: it may differ only for a lot "
                                      "that crosses midnight (default: today)")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--acknowledge")
    arguments = parser.parse_args(argv)

    target = load_target(arguments.target)
    config = load_json(Path(target["config"]["path"]))
    schedule = load_schedule(target)
    prompts = load_prompts(target)
    executable_rows(schedule, prompts)
    schema = run_pilot.vllm_grammar_schema(load_json(DIAGNOSTIC_SCHEMA_PATH))
    generation = target["generation"]
    results_dir = Path(target["results_dir"])

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

    summary = run_pass(target=target, ledger=ledger, schedule=schedule, prompts=prompts,
                       config=config, generation=generation, schema=schema,
                       pass_index=arguments.pass_index, results_dir=results_dir,
                       execute=arguments.execute, max_requests=arguments.max_requests,
                       resume=arguments.resume, accounting_guard=accounting_guard,
                       day=arguments.day)
    print(json.dumps(dict(summary, canary=canary_state(ledger),
                          ledger=ledger.snapshot()["requests_by_stage"]),
                     indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
