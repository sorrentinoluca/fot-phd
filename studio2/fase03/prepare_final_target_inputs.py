#!/usr/bin/env python3
"""7.4-MAT: runtime prerequisites of the final target. Offline; Luca runs it on the Mac.

From the runtime of ``studio2-fase03-d9-pilot-03`` and from ``prepared-7-4`` it derives the
four inputs ``materialize_final_target.py`` needs:

* ``execution.private.json``  executable configuration of the fresh final target
  (``d9.final_target``, REVISIONE_002), same consumer service and transport as the gate;
* ``generation.json``         the generation contract frozen by the pilot gate, verbatim;
* ``canary_prompts.jsonl``    the ten §6 prompts, byte-identical lines of the pilot file;
* ``final_prompts.jsonl``     the 2,244 prompts, re-rendered and checked on the id->hash map.

Without ``--execute`` nothing is written outside a temporary directory. It never contacts
a model, never opens a ledger of the pilot, never reads ``api_key.json`` or
``server_enea.json`` and prints only paths, SHA-256, counts and PASS/FAIL. Fail-closed.

The execution approval is the author's: ``--execute`` requires ``--author`` and
``--accept-configuration-sha256`` equal to the value the plan printed.
"""

from __future__ import annotations

import argparse
from contextlib import redirect_stdout
from copy import deepcopy
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from studio2.fase03.harness.common import (  # noqa: E402
    HarnessError, canonical_json, load_json, sha256_file, sha256_text,
)
from studio2.fase03.harness import d9  # noqa: E402
from studio2.fase03.harness import final_inventory as inventory_module  # noqa: E402
from studio2.fase03.harness.ledger import FINAL_BATCH_PROFILE, FINAL_CANARY_STAGE, PilotLedger, digest  # noqa: E402
from studio2.fase03.harness.runtime import durable_write  # noqa: E402
from studio2.fase03.harness.guards import require_reference_environment  # noqa: E402
from studio2.fase03 import materialize_final_target as materializer  # noqa: E402

ACK = "PREPARE_PHASE03_FINAL_TARGET_INPUTS"
FASE = ROOT / "studio2/fase03"
RUNTIME = Path("/Users/luker/fot-tep-runtime")
PILOT_ID = "studio2-fase03-d9-pilot-03"
PILOT_CONFIG = "execution/pilot_d9_successor_candidate_03_13.private.json"
TOKENIZER_REVISION = "a099dee70ccfcd8d5dda56aaa0b60cb8ecadabc9"
QUALIFIED_IDENTITY = {"returned_model": "qwen3.5-122b", "system_fingerprint": "vllm-0.27.1-934a3247"}
FROZEN_GATE_CANONICAL_SHA256 = "de1f59ceb28e50cd8b9027874f5d2d22cb1337ceab2e4dda8c2adda4b2dda6f2"
FROZEN_GATE_FILE_SHA256 = "709ae3400238b3ecdf50ef5b7d377b0bea4fdf87fcec569994d24cace39fa8ac"
GATE_GENERATION = {"max_tokens": 2560, "seed": 20260829, "thinking_token_budget": 2048}
PINS = {
    "inventory_sha256": "227e5e9c797dbfd8be746d85b77298f5dfb091846dc301f0b2e31ea1dbc6df3f",
    "schedule_sha256": "1acfc4044c53f113016ed0bfab58863291a9060a9edc9abadb68a21d30687819",
    "window_assignment_file_sha256": "c809e79d2c03d74f4a5a37988eca809bda336468ab0060f794d3c214f9a6a775",
    "test_input_manifest_sha256": "67e7584a80d743efc06edc4c97019c20803cc4787c1d70c8d924ad23736612e8",
    "prompt_map_sha256": "b819200396da480d3ed9d4aa8f6b6aac8c135d97f0876b734a9b607b75736489",
}
PROMPTS_FILE_SHA256_FIX2 = "f938604c512394df0e149732e474eb7d17b02a8dd1ed72155b84f19579a1385d"
PROTOCOL_MD = FASE / "protocollo_finale/PROTOCOLLO_FINALE_CANDIDATE.md"
REVISION_MD = FASE / "protocollo_finale/REVISIONE_002_NESSUN_LIMITE_DI_GIORNI.md"
APPROVAL_TEMPLATE = FASE / "batch_finale/APPROVAZIONE_MATERIALIZZAZIONE_7_4.json"
# Keys of the pilot configuration the final one is allowed to differ on.
ALLOWED_TOP_LEVEL_CHANGES = {"execution_authorization", "pilot_ledger", "call_budget", "d9",
                             "derived_from"}
ALLOWED_D9_CHANGES = set(d9.PILOT_HISTORY_KEYS) | {"final_target"}


class Report:
    def __init__(self):
        self.rows = []

    def check(self, name, passed, detail=None):
        self.rows.append({"check": name, "result": "PASS" if passed else "FAIL",
                          **({"detail": detail} if detail is not None else {})})
        if not passed:
            raise HarnessError(f"FAIL {name}" + (f": {detail}" if detail else ""))

    def note(self, name, detail):
        self.rows.append({"check": name, "result": "NOTE", "detail": detail})


def table_section6() -> dict[str, dict]:
    """The ten rows of the §6 table of the frozen protocol, parsed from its bytes."""
    rows = {}
    pattern = re.compile(
        r"^\| `(S2-P03-\d{3})` \| (A|B-LF|E-LF) \| (\d) \| `([0-9a-f]{64})` \| (true|false) \| "
        r"(null|`[^`]+`) \| `([0-9a-f]{64})` \|$")
    for line in PROTOCOL_MD.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line.strip())
        if match:
            prompt_id, condition, agent, prompt_sha, abstain, label, raw_sha = match.groups()
            rows[prompt_id] = {"condition": condition, "agent_id": f"agent_{agent}",
                               "prompt_sha256": prompt_sha, "abstain": abstain == "true",
                               "predicted_label": None if label == "null" else label.strip("`"),
                               "raw_response_sha256": raw_sha}
    return rows


def final_configuration(pilot_config: dict, *, target_id: str, ledger_path: Path,
                        frozen_canonical: str) -> dict:
    config = deepcopy(pilot_config)
    config.pop("execution_authorization", None)
    config["pilot_ledger"] = {"path": str(ledger_path), "pilot_id": target_id}
    section = config["d9"]
    for key in d9.PILOT_HISTORY_KEYS:
        section.pop(key, None)
    section["final_target"] = {"artifact_version": d9.FINAL_TARGET_VERSION, "target_id": target_id,
                               "predecessor_consumption": d9.FINAL_TARGET_PREDECESSORS}
    # The transport counts its own sends per process; the ledger profile is the real ceiling.
    config["call_budget"] = {
        "profile": FINAL_BATCH_PROFILE.name,
        "stage_quota": dict(sorted(FINAL_BATCH_PROFILE.base_limits.items())),
        "retry_quota": FINAL_BATCH_PROFILE.retry_quota,
        "planned_maximum": FINAL_BATCH_PROFILE.planned_maximum,
        "hard_stop_provider_requests": FINAL_BATCH_PROFILE.hard_stop,
    }
    config["derived_from"] = {"pilot_id": PILOT_ID,
                              "pilot_configuration_canonical_sha256": digest(pilot_config),
                              "frozen_gate_canonical_sha256": frozen_canonical,
                              "protocol_revision": REVISION_MD.name}
    return config


def configuration_sha256(config: dict) -> str:
    payload = {k: v for k, v in config.items() if k != "execution_authorization"}
    return sha256_text(canonical_json(payload))


def canary_lines(pilot_prompts: Path, expectations: dict[str, dict]) -> tuple[bytes, list[str]]:
    """The ten lines of the pilot prompt file, byte for byte, in the order of that file."""
    chosen, seen = [], []
    for raw in pilot_prompts.read_bytes().split(b"\n"):
        if not raw.strip():
            continue
        row = json.loads(raw)
        reference = expectations.get(row.get("prompt_id"))
        if reference is None:
            continue
        if (sha256_text(row["text"]) != reference["prompt_sha256"]
                or row.get("condition") != reference["condition"]
                or row.get("agent_id") != reference["agent_id"]):
            raise HarnessError(f"canary prompt {row['prompt_id']} differs from the frozen table")
        chosen.append(raw + b"\n")
        seen.append(row["prompt_id"])
    if sorted(seen) != sorted(expectations) or len(seen) != len(set(seen)):
        raise HarnessError("the pilot prompt file does not hold each canary prompt exactly once")
    return b"".join(chosen), seen


def render_prompts(arguments, out_dir: Path) -> dict:
    from studio2.fase03 import build_final_prompts
    pilot = arguments.pilot_runtime
    sink = io.StringIO()
    with redirect_stdout(sink):
        status = build_final_prompts.main([
            "--pilot-manifest", str(pilot / "execution/PILOT_INPUT_MANIFEST.frozen.json"),
            "--pilot-sources", str(pilot / "execution/PILOT_INPUT_SOURCES.frozen.json"),
            "--test-input", str(arguments.test_input),
            "--libraries-root", str(pilot / "results"),
            "--tokenizer-snapshot", str(pilot / "tokenizers" / TOKENIZER_REVISION),
            "--out", str(out_dir)])
    if status != 0:
        raise HarnessError("build_final_prompts is blocked: " + sink.getvalue()[-600:])
    return load_json(out_dir / "PROMPT_FINALI_7_4.json")


def rehearsal(config: dict, *, expectations_sha256: str, canary_path: Path, snapshot: Path,
              generation: dict) -> dict:
    """The canary plan and its real binding on a throw-away ledger carrying the target identity.

    No call, no reservation. It walks exactly the D9 chain the real target will walk:
    ``require_execution``, ``require_pilot_ledger`` and ``bind_stage`` with ``execution_config``.
    """
    from studio2.fase03 import run_final_canary, run_pilot
    from studio2.fase03.harness.guards import require_execution, require_pilot_ledger
    from studio2.fase03.protocol import DIAGNOSTIC_SCHEMA_PATH
    require_execution(config)
    schema = run_pilot.vllm_grammar_schema(load_json(DIAGNOSTIC_SCHEMA_PATH))
    with tempfile.TemporaryDirectory() as scratch:
        ledger = PilotLedger(Path(scratch).resolve() / "rehearsal.sqlite3",
                             pilot_id=config["pilot_ledger"]["pilot_id"],
                             identity_path=Path(config["pilot_ledger"]["path"]),
                             profile=FINAL_BATCH_PROFILE.name)
        require_pilot_ledger(config, ledger)
        target = {"canary_expectations": {"path": str(materializer.CANARY_PATH),
                                          "sha256": expectations_sha256},
                  "canary_prompts": {"path": str(canary_path), "sha256": sha256_file(canary_path)},
                  "tokenizer_snapshot": str(snapshot)}
        prompts = run_final_canary.canary_prompts(target)
        specs = [dict(logical_id=f"canary:day{index}:{prompt['prompt_id']}",
                      model=config["candidate"]["requested_model"], producer="consumer",
                      prompt_sha256=prompt["prompt_sha256"],
                      case_sha256=digest([prompt["agent_id"], prompt["case_id"]]),
                      contract_sha256=digest(generation), condition=prompt["condition"],
                      group=prompt["prompt_id"], repetition=1)
                 for index in range(1, run_final_canary.MAX_DAYS + 1) for prompt in prompts]
        binding = run_final_canary.canary_binding(specs, config=config, schema=schema, target=target)
        ledger.bind_stage(FINAL_CANARY_STAGE, binding)
        reread = ledger.binding(FINAL_CANARY_STAGE)
        return {"canary_slots_bound": len(reread["requests"]),
                "binding_sha256": digest(reread),
                "ledger": "temporary, deleted; identity of the final target"}


def git(*arguments: str) -> str | None:
    try:
        return subprocess.run(["git", "-C", str(ROOT), *arguments], check=True, text=True,
                              capture_output=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def approval_template(files: dict[str, str]) -> dict:
    tag = materializer.PROTOCOL_TAG
    tag_commit, head = git("rev-parse", tag + "^{commit}"), git("rev-parse", "HEAD")
    if tag_commit is None or tag_commit != head:
        raise HarnessError(f"the approval template requires tag {tag} on the commit being run")
    return {
        "artifact_version": "APPROVAZIONE_MATERIALIZZAZIONE_7_4_1",
        "decision": None, "author": None, "date": None,
        "decision_instructions": "the author sets decision='accepted', author and date by hand",
        "protocol_tag": tag, "protocol_commit": tag_commit,
        "protocol_sha256": sha256_file(PROTOCOL_MD),
        "protocol_revision_sha256": sha256_file(REVISION_MD),
        "inventory_sha256": PINS["inventory_sha256"], "schedule_sha256": PINS["schedule_sha256"],
        "input_files_sha256": files,
        "planned_maximum": FINAL_BATCH_PROFILE.planned_maximum,
        "stage_quota": dict(sorted(FINAL_BATCH_PROFILE.base_limits.items())),
        "retry_quota": FINAL_BATCH_PROFILE.retry_quota,
        "target_id": materializer.TARGET_ID,
    }


def run(arguments) -> dict:
    report = Report()
    pilot, prepared, config_dir = arguments.pilot_runtime, arguments.prepared, arguments.config_dir
    target_root = arguments.runtime_root / arguments.target_id
    outputs = {"execution.private.json": config_dir / "execution.private.json",
               "generation.json": config_dir / "generation.json",
               "canary_prompts.jsonl": prepared / "canary_prompts.jsonl",
               "final_prompts.jsonl": prepared / "final_prompts.jsonl"}
    approval_path = config_dir / "execution_authorization.private.json"

    if arguments.approval_template:
        # After the tag: the four prepared files are hashed as they are, nothing is rebuilt.
        missing = [name for name, path in outputs.items() if not path.is_file()]
        if missing:
            raise HarnessError(f"prepare the inputs first; missing {missing}")
        if APPROVAL_TEMPLATE.exists():
            raise HarnessError("the materialization approval already exists; it is never overwritten")
        template = approval_template({name: sha256_file(path) for name, path in outputs.items()})
        durable_write(APPROVAL_TEMPLATE, json.dumps(template, indent=2, ensure_ascii=False,
                                                    sort_keys=True) + "\n")
        return {"status": "APPROVAL_TEMPLATE_WRITTEN", "path": str(APPROVAL_TEMPLATE),
                "sha256": sha256_file(APPROVAL_TEMPLATE), "template": template}

    # 0. Profile and pins of the revision in force.
    report.check("profile final_batch: canary 300, maximum 7432",
                 FINAL_BATCH_PROFILE.base_limits[FINAL_CANARY_STAGE] == 300
                 and FINAL_BATCH_PROFILE.planned_maximum == FINAL_BATCH_PROFILE.hard_stop == 7432)
    inventory = inventory_module.build_inventory()
    inventory_sha = inventory_module.artifact_sha256(inventory_module.inventory_artifact(inventory))
    schedule_sha = inventory_module.artifact_sha256(inventory_module.schedule_artifact(
        inventory_module.build_schedule(inventory), inventory_sha256=inventory_sha))
    report.check("pin inventory", inventory_sha == PINS["inventory_sha256"], inventory_sha)
    report.check("pin schedule", schedule_sha == PINS["schedule_sha256"], schedule_sha)
    assignment_sha = sha256_file(FASE / "batch_finale/ASSEGNAZIONE_FINESTRE_7_4.json")
    report.check("pin window assignment", assignment_sha == PINS["window_assignment_file_sha256"],
                 assignment_sha)
    manifest_sha = sha256_file(arguments.test_input / "INPUT_MANIFEST_TEST_7_4.json")
    report.check("pin test input manifest", manifest_sha == PINS["test_input_manifest_sha256"],
                 manifest_sha)
    report.check("target root does not exist yet", not target_root.exists(), str(target_root))

    # 1. Generation contract = the pilot gate's, field by field.
    frozen_path = pilot / "results/frozen_gate_config.json"
    frozen = load_json(frozen_path)
    report.check("frozen gate file bytes", sha256_file(frozen_path) == FROZEN_GATE_FILE_SHA256,
                 sha256_file(frozen_path))
    report.check("frozen gate canonical content", digest(frozen) == FROZEN_GATE_CANONICAL_SHA256,
                 digest(frozen))
    report.check("frozen gate status", frozen.get("status") == "FROZEN_FOR_STABILITY_GATE")
    generation = frozen["generation"]
    differences = sorted(key for key in set(generation) | set(GATE_GENERATION)
                         if generation.get(key) != GATE_GENERATION.get(key))
    report.check("generation contract equals the gate, field by field", not differences, differences)
    d9.generation_kwargs(generation, model_role="122B")
    generation_bytes = (json.dumps(generation, indent=2, ensure_ascii=False, sort_keys=True) + "\n")

    # 2. Executable configuration, derived from the configuration the gate ran under.
    pilot_config = load_json(pilot / PILOT_CONFIG)
    report.check("pilot configuration is the one of the gate",
                 digest(pilot_config) == frozen.get("config_sha256"), digest(pilot_config))
    config = final_configuration(pilot_config, target_id=arguments.target_id,
                                 ledger_path=(target_root / "ledger.sqlite3").resolve(),
                                 frozen_canonical=digest(frozen))
    report.check("qualified 122B identity",
                 config.get("expected_response") == QUALIFIED_IDENTITY
                 and config["candidate"].get("requested_model") == "qwen3.5-122b"
                 and config["d9"]["services"]["122B"]["expected_response"] == QUALIFIED_IDENTITY,
                 QUALIFIED_IDENTITY)
    report.check("consumer candidate (service, transport) identical to the gate",
                 config["candidate"] == frozen.get("candidate") == pilot_config["candidate"])
    changed = sorted(key for key in set(config) | set(pilot_config)
                     if config.get(key) != pilot_config.get(key))
    changed_d9 = sorted(key for key in set(config["d9"]) | set(pilot_config["d9"])
                        if config["d9"].get(key) != pilot_config["d9"].get(key))
    report.check("differences from the pilot configuration are the declared ones only",
                 set(changed) <= ALLOWED_TOP_LEVEL_CHANGES and set(changed_d9) <= ALLOWED_D9_CHANGES,
                 {"top_level": changed, "d9": changed_d9})
    report.check("output limit of the service covers the contract",
                 generation["max_tokens"] <= config["d9"]["services"]["122B"]["max_output_tokens"])
    d9.validate_config(config)
    report.check("d9.validate_config (final_target mode, 122B identity binding)", True)
    accepted_sha = configuration_sha256(config)

    # 3. Canary prompts, byte-identical, authenticated against §6 and CANARY_ATTESI.
    expectations_file = load_json(materializer.CANARY_PATH)
    expectations = {row["prompt_id"]: row for row in expectations_file["expectations"]}
    table = table_section6()
    report.check("§6 table has ten rows", len(table) == 10, len(table))
    report.check("§6 table equals CANARY_ATTESI_7_4.json",
                 all({key: expectations.get(prompt_id, {}).get(key) for key in row} == row
                     for prompt_id, row in table.items()) and set(table) == set(expectations))
    pilot_prompts = pilot / "prepared/pilot_prompts.jsonl"
    report.check("pilot prompt file is the one of the gate",
                 sha256_file(pilot_prompts) == frozen.get("prompt_file_sha256"),
                 sha256_file(pilot_prompts))
    canary_bytes, canary_ids = canary_lines(pilot_prompts, expectations)
    report.check("ten canary prompts, byte-identical lines, SHA of §6", len(canary_ids) == 10,
                 canary_ids)

    # 4. Final prompts, re-rendered with the tokenizer snapshot.
    snapshot = pilot / "tokenizers" / TOKENIZER_REVISION
    report.check("tokenizer snapshot present", snapshot.is_dir(), str(snapshot))
    with tempfile.TemporaryDirectory() as scratch:
        out_dir = prepared if arguments.execute else Path(scratch)
        summary = render_prompts(arguments, out_dir)
        prompts_sha = sha256_file(out_dir / "final_prompts.jsonl")
        rendered = sum(1 for line in (out_dir / "final_prompts.jsonl").read_text(
            encoding="utf-8").splitlines() if line)
    report.check("prompt id->hash map", summary.get("prompts_sha256") == PINS["prompt_map_sha256"],
                 summary.get("prompts_sha256"))
    report.check("2244 prompts rendered", rendered == 2244 == summary.get("unique_total"), rendered)
    report.note("final_prompts.jsonl file SHA (A3: recorded here)",
                {"sha256": prompts_sha, "equals_7_4_FIX_2": prompts_sha == PROMPTS_FILE_SHA256_FIX2})

    result = {"artifact_version": "PREPARAZIONE_TARGET_FINALE_7_4_1",
              "target_id": arguments.target_id, "target_root": str(target_root),
              "configuration_sha256_to_accept": accepted_sha,
              "outputs": {name: str(path) for name, path in outputs.items()},
              "execution_authorization": str(approval_path)}
    if not arguments.execute:
        return dict(result, status="PLAN_ONLY", checks=report.rows,
                    requires=(f"--execute --acknowledge {ACK} --author <name> "
                              f"--accept-configuration-sha256 {accepted_sha}"))

    # 5. Writes. The author's acceptance names the exact configuration.
    if not arguments.author or arguments.accept_configuration_sha256 != accepted_sha:
        raise HarnessError("the author must accept exactly the configuration SHA of the plan")
    config_dir.mkdir(parents=True, exist_ok=True)
    approval = {"artifact_version": "EXECUTION_AUTHORIZATION_BATCH_FINALE_1",
                "author": arguments.author, "decision": "accepted",
                "configuration_sha256": accepted_sha, "target_id": arguments.target_id,
                "scope": "final batch 7.4 on the fresh target; REVISIONE_002",
                "protocol_tag": materializer.PROTOCOL_TAG}
    for path, data in ((approval_path, json.dumps(approval, indent=2, ensure_ascii=False,
                                                   sort_keys=True) + "\n"),):
        if path.exists() and path.read_text(encoding="utf-8") != data:
            raise HarnessError(f"{path.name} exists with other bytes; nothing is overwritten")
        durable_write(path, data)
    config["execution_authorization"] = {"path": str(approval_path),
                                         "sha256": sha256_file(approval_path)}
    config_bytes = json.dumps(config, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    for name, data in (("execution.private.json", config_bytes), ("generation.json", generation_bytes)):
        path = outputs[name]
        if path.exists() and path.read_text(encoding="utf-8") != data:
            raise HarnessError(f"{name} exists with other bytes; nothing is overwritten")
        durable_write(path, data)
    canary_path = outputs["canary_prompts.jsonl"]
    if canary_path.exists() and canary_path.read_bytes() != canary_bytes:
        raise HarnessError("canary_prompts.jsonl exists with other bytes; nothing is overwritten")
    canary_path.parent.mkdir(parents=True, exist_ok=True)
    canary_path.write_bytes(canary_bytes)
    report.check("written configuration reloads and is covered by the approval",
                 configuration_sha256(load_json(outputs["execution.private.json"])) == accepted_sha)
    report.check("written generation contract reloads equal",
                 load_json(outputs["generation.json"]) == generation)
    outcome = rehearsal(load_json(outputs["execution.private.json"]),
                        expectations_sha256=sha256_file(materializer.CANARY_PATH),
                        canary_path=canary_path, snapshot=snapshot, generation=generation)
    report.check("rehearsal: D9 chain and real canary binding on a throw-away final_batch ledger",
                 outcome["canary_slots_bound"] == FINAL_BATCH_PROFILE.base_limits[FINAL_CANARY_STAGE],
                 outcome)
    files = {name: sha256_file(path) for name, path in outputs.items()}
    files["execution_authorization.private.json"] = sha256_file(approval_path)
    return dict(result, status="PREPARED", files_sha256=files, checks=report.rows)


def main(argv=None) -> int:
    require_reference_environment()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime-root", type=Path, default=RUNTIME)
    parser.add_argument("--pilot-runtime", type=Path)
    parser.add_argument("--prepared", type=Path)
    parser.add_argument("--config-dir", type=Path)
    parser.add_argument("--test-input", type=Path, default=FASE / "evidence/output_test")
    parser.add_argument("--target-id", default=materializer.TARGET_ID)
    parser.add_argument("--author")
    parser.add_argument("--accept-configuration-sha256")
    parser.add_argument("--approval-template", action="store_true",
                        help="only write batch_finale/APPROVAZIONE_MATERIALIZZAZIONE_7_4.json from the "
                             "prepared files, with decision, author and date left empty; requires "
                             "the protocol tag on the commit being run")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--acknowledge")
    arguments = parser.parse_args(argv)
    arguments.pilot_runtime = arguments.pilot_runtime or arguments.runtime_root / PILOT_ID
    arguments.prepared = arguments.prepared or arguments.runtime_root / "prepared-7-4"
    arguments.config_dir = (arguments.config_dir
                            or arguments.runtime_root / (arguments.target_id + ".config"))
    if arguments.execute and arguments.acknowledge != ACK:
        raise SystemExit(f"--execute requires --acknowledge {ACK}")
    try:
        value = run(arguments)
    except (HarnessError, OSError, KeyError, ValueError) as exc:
        print(json.dumps({"status": "FAIL", "error": f"{type(exc).__name__}: {exc}"},
                         indent=2, ensure_ascii=False))
        return 2
    print(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
