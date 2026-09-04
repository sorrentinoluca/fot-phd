#!/usr/bin/env python3
"""Dedicated fail-closed EXP3_V2 inference runner.

The CLI has no switch that disables tag, repository, runtime, hash, leakage,
locking, or output-boundary checks. Tests inject a fake Responses client into
the same sequential execution core; production creates the frozen OpenAI
adapter only after every preflight and ambiguity check has passed.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
import argparse
import hashlib
import importlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any

import jsonschema


HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
SCHEMA_DIR = HERE / "inference_schemas"
DEFAULT_MANIFEST = HERE / "EXP3_V2_INFERENCE_HARNESS_MANIFEST_001.json"
SCHEDULE_SCHEMA_KEYS = {
    "sequence_index",
    "block_index",
    "position_in_block",
    "physical_case_id",
    "agent_id",
    "repetition",
    "condition",
}
MODEL = "gpt-5.6-terra"
REASONING_EFFORT = "medium"
MAX_OUTPUT_TOKENS = 512
MAX_STRUCTURAL_RETRIES = 2
TIMEOUT_SECONDS = 120.0
REQUEST_PARAMETERS = {
    "reasoning_effort": REASONING_EFFORT,
    "max_output_tokens": MAX_OUTPUT_TOKENS,
    "store": False,
    "temperature_sent": False,
    "seed_sent": False,
    "previous_response_id_used": False,
}
AGENT_PACK = {
    "agent_1": "LKP-001",
    "agent_2": "LKP-002",
    "agent_3": "LKP-003",
    "agent_4": "LKP-004",
}
PARSE_FAILURE_OUTPUT = {
    "predicted_label": None,
    "abstain": True,
    "used_insight_ids": [],
    "reasoning_summary": "parse_failure",
}
CORRECTION_SUFFIX = """

CORRECTION REQUIRED
The previous response failed strict schema validation. Return only one valid JSON object with exactly: predicted_label, abstain, used_insight_ids, reasoning_summary. Do not add markdown, confidence, or any other key.
""".rstrip()
PROMPT_FORBIDDEN_SUBSTRINGS = (
    "exp3v2-",
    "mode1_",
    "class_offline",
    "fault_id",
    "output_path",
    ".xlsx",
    "/private/",
    "/users/",
)


class AmbiguousRequestError(RuntimeError):
    def __init__(
        self,
        entry: dict[str, Any],
        rendered: Any,
        attempt: int,
        intent_path: Path,
    ) -> None:
        super().__init__(
            f"AMBIGUOUS request intent lacks durable response: {intent_path}"
        )
        self.entry = entry
        self.rendered = rendered
        self.attempt = attempt
        self.intent_path = intent_path


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def canonical_json_bytes(value: Any) -> bytes:
    return (canonical_json(value) + "\n").encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def atomic_write_immutable(path: Path, content: bytes) -> None:
    if path.exists():
        if path.read_bytes() != content:
            raise RuntimeError(f"immutable artifact differs: {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(descriptor, "wb", closefd=True) as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        fsync_directory(path.parent)
    except BaseException:
        if temporary.exists():
            temporary.unlink()
        raise


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git_output(root: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        check=check,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.stdout.strip()


def verify_annotated_tag(
    root: Path, name: str, expected_object: str | None, expected_commit: str
) -> None:
    object_id = git_output(root, "rev-parse", f"refs/tags/{name}")
    if expected_object is not None and object_id != expected_object:
        raise RuntimeError(f"annotated tag object mismatch: {name}")
    if git_output(root, "cat-file", "-t", object_id) != "tag":
        raise RuntimeError(f"tag is not annotated: {name}")
    if git_output(root, "rev-parse", f"refs/tags/{name}^{{commit}}") != expected_commit:
        raise RuntimeError(f"tag target mismatch: {name}")


def verify_detached_clean_checkout(root: Path, expected_commit: str) -> None:
    if git_output(root, "rev-parse", "HEAD") != expected_commit:
        raise RuntimeError(f"checkout HEAD mismatch: {root}")
    symbolic = subprocess.run(
        ["git", "symbolic-ref", "-q", "HEAD"],
        cwd=root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if symbolic.returncode == 0:
        raise RuntimeError(f"checkout is not detached: {root}")
    if git_output(root, "status", "--porcelain=v1", "--untracked-files=all"):
        raise RuntimeError(f"checkout is not clean: {root}")


def verify_boundaries(
    manifest: dict[str, Any],
    manifest_path: Path,
    upstream_roots: dict[str, Path],
) -> Path:
    harness_root = Path(
        git_output(manifest_path.parent, "rev-parse", "--show-toplevel")
    ).resolve()
    if manifest_path.resolve() != harness_root / manifest["manifest_path"]:
        raise RuntimeError("manifest path does not match the frozen checkout contract")
    if manifest.get("status") != "HARNESS_FROZEN_FOR_INFERENCE":
        raise RuntimeError("inference harness is not frozen")
    if manifest.get("tag_created") is not True:
        raise RuntimeError("inference harness tag is not recorded as created")
    own_tag = manifest["prospective_tag"]
    head = git_output(harness_root, "rev-parse", "HEAD")
    verify_annotated_tag(harness_root, own_tag, None, head)
    verify_detached_clean_checkout(harness_root, head)

    for binding in manifest["upstream_tags"]:
        verify_annotated_tag(
            harness_root,
            binding["name"],
            binding["tag_object"],
            binding["peeled_commit"],
        )

    expected_names = {item["name"] for item in manifest["upstream_tags"]}
    if set(upstream_roots) != expected_names:
        raise RuntimeError("exactly four upstream checkout roots are required")
    for binding in manifest["upstream_tags"]:
        root = upstream_roots[binding["name"]]
        actual_root = Path(git_output(root, "rev-parse", "--show-toplevel")).resolve()
        if actual_root != root.resolve():
            raise RuntimeError(
                f"upstream path is not a Git worktree root: {binding['name']}"
            )
        verify_annotated_tag(
            root,
            binding["name"],
            binding["tag_object"],
            binding["peeled_commit"],
        )
        verify_detached_clean_checkout(root, binding["peeled_commit"])

    for artifact in manifest["harness_artifacts"]:
        path = harness_root / artifact["path"]
        if not path.is_file() or path.is_symlink():
            raise RuntimeError(
                f"missing or symlinked harness artifact: {artifact['path']}"
            )
        if (
            path.stat().st_size != artifact["size_bytes"]
            or sha256_file(path) != artifact["sha256"]
        ):
            raise RuntimeError(f"harness artifact mismatch: {artifact['path']}")
    return harness_root


def artifact_binding(manifest: dict[str, Any], relative_path: str) -> dict[str, Any]:
    matches = [
        item for item in manifest["harness_artifacts"] if item["path"] == relative_path
    ]
    if len(matches) != 1:
        raise RuntimeError(
            f"missing or duplicate harness artifact binding: {relative_path}"
        )
    return matches[0]


def verify_execution_authorization(
    harness_manifest: dict[str, Any],
    harness_manifest_path: Path,
    harness_root: Path,
    authorization_manifest_path: Path,
    authorization_root: Path,
) -> dict[str, Any]:
    contract = harness_manifest["execution_authorization"]
    if authorization_manifest_path.resolve() != Path(contract["manifest_path"]):
        raise RuntimeError("authorization manifest path differs from frozen command")
    if authorization_root.resolve() != Path(contract["checkout_root"]):
        raise RuntimeError("authorization root differs from frozen command")
    if (
        not authorization_manifest_path.is_file()
        or authorization_manifest_path.is_symlink()
    ):
        raise RuntimeError(
            "final execution-authorization manifest is absent or symlinked"
        )
    actual_root = Path(
        git_output(authorization_root, "rev-parse", "--show-toplevel")
    ).resolve()
    if actual_root != authorization_root.resolve():
        raise RuntimeError("authorization root is not its Git worktree root")
    authorization = load_json(authorization_manifest_path)
    validate_json(
        authorization,
        "exp3v2_inference_execution_authorization.schema.json",
    )
    tag_name = contract["prospective_tag"]
    authorization_head = git_output(authorization_root, "rev-parse", "HEAD")
    verify_annotated_tag(authorization_root, tag_name, None, authorization_head)
    verify_detached_clean_checkout(authorization_root, authorization_head)

    harness_commit = git_output(
        harness_root,
        "rev-parse",
        f"refs/tags/{harness_manifest['prospective_tag']}^{{commit}}",
    )
    parent_line = git_output(
        authorization_root, "rev-list", "--parents", "-n", "1", "HEAD"
    ).split()
    if len(parent_line) != 2 or parent_line[1] != harness_commit:
        raise RuntimeError(
            "authorization commit must have the harness commit as sole parent"
        )
    if authorization["harness_binding"] != {
        "tag": harness_manifest["prospective_tag"],
        "commit": harness_commit,
        "manifest_path": harness_manifest["manifest_path"],
        "manifest_sha256": sha256_file(harness_manifest_path),
    }:
        raise RuntimeError("authorization does not bind the exact frozen harness")

    added_paths = set(
        git_output(
            authorization_root,
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "--diff-filter=A",
            "-r",
            "HEAD",
        ).splitlines()
    )
    if added_paths != set(contract["authorization_commit_additions"]):
        raise RuntimeError(
            "authorization commit additions differ from frozen allowlist"
        )
    changed_paths = set(
        git_output(
            authorization_root,
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "-r",
            "HEAD",
        ).splitlines()
    )
    if changed_paths != added_paths:
        raise RuntimeError(
            "authorization commit modifies or deletes frozen harness paths"
        )

    sentinel_root = authorization_root / contract["sentinel_artifact_directory"]
    sentinel_verifier = importlib.import_module(
        "phase_b.exp3_v2.verify_exp3v2_inference_sentinel"
    )
    verified = sentinel_verifier.verify_sentinel(
        sentinel_root,
        expected_prompt_sha256=harness_manifest["sentinel"]["prompt_sha256"],
    )
    sentinel_binding = authorization["sentinel_binding"]
    for key in (
        "sentinel_id",
        "provider_submission_count",
        "returned_model",
    ):
        if sentinel_binding[key] != verified[key]:
            raise RuntimeError(f"authorization sentinel binding mismatch: {key}")
    if sentinel_binding["evidence_sha256"] != verified["evidence_sha256"]:
        raise RuntimeError("authorization sentinel evidence hash mismatch")
    if sentinel_binding["intent_sha256"] != verified["intent_sha256"]:
        raise RuntimeError("authorization sentinel intent hash mismatch")
    if sentinel_binding["receipt_sha256"] != verified["receipt_sha256"]:
        raise RuntimeError("authorization sentinel receipt hash mismatch")
    if (
        not sentinel_binding["token_accounting_pass"]
        or not sentinel_binding["verifier_pass"]
    ):
        raise RuntimeError("authorization sentinel checks are not PASS")

    expected_integrity = {
        "schedule_sha256": harness_manifest["schedule"]["sha256"],
        "runner_sha256": artifact_binding(
            harness_manifest,
            "phase_b/exp3_v2/run_exp3v2_inference.py",
        )["sha256"],
        "runtime_lock_sha256": artifact_binding(
            harness_manifest,
            "phase_b/exp3_v2/EXP3_V2_INFERENCE_RUNTIME_LOCK_001.json",
        )["sha256"],
    }
    if authorization["integrity_bindings"] != expected_integrity:
        raise RuntimeError(
            "authorization integrity bindings differ from frozen harness"
        )
    return authorization


def validate_schedule(schedule: list[dict[str, Any]], expected_sha256: str) -> None:
    from phase_b.exp3_v2.build_exp3v2_inference_schedule import (  # noqa: PLC0415
        validate_schedule as validate_generated_schedule,
    )

    if sha256_bytes(canonical_json_bytes(schedule)) != expected_sha256:
        raise RuntimeError("schedule SHA-256 mismatch")
    if any(set(item) != SCHEDULE_SCHEMA_KEYS for item in schedule):
        raise RuntimeError("schedule entry schema mismatch")
    validate_generated_schedule(schedule)


def load_case_texts(
    manifest: dict[str, Any], verbalizations_root: Path
) -> dict[str, str]:
    output_manifest_path = (
        verbalizations_root / manifest["inputs"]["output_manifest_path"]
    )
    if output_manifest_path.is_symlink() or not output_manifest_path.is_file():
        raise RuntimeError(
            "frozen verbalization output manifest is missing or symlinked"
        )
    if (
        sha256_file(output_manifest_path)
        != manifest["inputs"]["output_manifest_sha256"]
    ):
        raise RuntimeError("frozen verbalization output manifest hash mismatch")
    output_manifest = load_json(output_manifest_path)
    expected_cases = manifest["inputs"]["cases"]
    if [item["physical_case_id"] for item in output_manifest["cases"]] != [
        item["physical_case_id"] for item in expected_cases
    ]:
        raise RuntimeError("verbalization manifest case order mismatch")

    neutral_root = verbalizations_root / "verbalization_outputs" / "neutral_text"
    expected_paths = {item["path"] for item in expected_cases}
    observed_paths = {
        str(path.relative_to(verbalizations_root))
        for path in neutral_root.iterdir()
        if path.is_file()
    }
    if observed_paths != expected_paths:
        raise RuntimeError("neutral-text input set is partial or contains extra files")

    texts: dict[str, str] = {}
    for expected, source in zip(expected_cases, output_manifest["cases"], strict=True):
        relative = Path(expected["path"])
        if relative.is_absolute() or ".." in relative.parts:
            raise RuntimeError("neutral-text path is not canonical and relative")
        if source["neutral_text_path"] != str(
            relative.relative_to("verbalization_outputs")
        ):
            raise RuntimeError("neutral-text path differs from output manifest")
        if source["neutral_text_size_bytes"] != expected["size_bytes"]:
            raise RuntimeError("neutral-text size differs from output manifest")
        if source["neutral_text_sha256"] != expected["sha256"]:
            raise RuntimeError("neutral-text hash differs from output manifest")
        path = verbalizations_root / relative
        if path.is_symlink() or not path.is_file():
            raise RuntimeError(f"neutral-text input missing or symlinked: {relative}")
        content = path.read_bytes()
        if (
            len(content) != expected["size_bytes"]
            or sha256_bytes(content) != expected["sha256"]
        ):
            raise RuntimeError(f"neutral-text input mismatch: {relative}")
        text = content.decode("utf-8").strip()
        if not text:
            raise RuntimeError(f"neutral-text input is empty: {relative}")
        texts[expected["physical_case_id"]] = text
    return texts


class FrozenAssets:
    def __init__(self, harness_root: Path, case_texts: dict[str, str]) -> None:
        if str(harness_root) not in sys.path:
            sys.path.insert(0, str(harness_root))
        protocol_module = importlib.import_module("phase_b.config")
        insight_module = importlib.import_module("phase_b.insights")
        self.builder_module = importlib.import_module("phase_b.conditions.builders")
        self.scan_text = importlib.import_module("phase_b.prompts.leakage").scan_text
        self.parse_output = importlib.import_module(
            "phase_b.conditions.parser"
        ).parse_diagnostic_output
        self.protocol = protocol_module.load_protocol_config(
            harness_root / "phase_b/config/protocol_config.json"
        )
        protocol_module.validate_execution_ready(self.protocol)
        self.provider_schema = load_json(
            harness_root / "phase_b/conditions/diagnostic_output.openai.schema.json"
        )
        self.global_insights = insight_module.validate_global_insights(
            load_json(harness_root / "phase_b/insights/final_local_insights.json"),
            self.protocol,
        )
        self.derangements = load_json(
            harness_root / "phase_b/config/evaluator_side/condition_e_derangements.json"
        )["derangements"]
        examples = load_json(
            harness_root / "phase_b/local_knowledge/local_examples.json"
        )
        self.local_examples = {
            agent_id: examples["packs"][pack_id]
            for agent_id, pack_id in AGENT_PACK.items()
        }
        self.case_texts = case_texts
        self.verify_peer_libraries(harness_root)

    def verify_peer_libraries(self, harness_root: Path) -> None:
        for agent_id in AGENT_PACK:
            for condition in ("B", "E"):
                derived = self.builder_module.condition_peer_insights(
                    agent_id=agent_id,
                    condition=condition,
                    config=self.protocol,
                    global_insights=self.global_insights,
                    derangements=self.derangements,
                )
                frozen = load_json(
                    harness_root
                    / f"phase_b/insights/peer_libraries/{agent_id}_{condition}.json"
                )
                if [item.to_dict() for item in derived] != frozen:
                    raise RuntimeError(
                        f"derived condition {condition} differs from frozen peer library"
                    )

    def render(self, entry: dict[str, Any]):
        condition = entry["condition"]
        rendered = self.builder_module.render_diagnostic_prompt(
            agent_id=entry["agent_id"],
            condition=condition,
            case_text=self.case_texts[entry["physical_case_id"]],
            local_examples=self.local_examples[entry["agent_id"]],
            config=self.protocol,
            global_insights=(None if condition == "A" else self.global_insights),
            derangements=(self.derangements if condition == "E" else None),
        )
        lowered = rendered.text.lower()
        if any(token in lowered for token in PROMPT_FORBIDDEN_SUBSTRINGS):
            raise RuntimeError("rendered prompt contains forbidden case metadata")
        if self.scan_text(rendered.text, source=f"runtime:{entry['sequence_index']}"):
            raise RuntimeError("rendered prompt contains real fault identity")
        return rendered

    def parse(self, raw: str, available_insight_ids: tuple[str, ...]) -> dict[str, Any]:
        return self.parse_output(
            raw,
            label_space=self.protocol["label_space"],
            allowed_insight_ids=available_insight_ids,
        )


@dataclass(frozen=True)
class JournalPaths:
    intent: Path
    response: Path


def job_key(entry: dict[str, Any]) -> str:
    return "|".join(
        (
            entry["physical_case_id"],
            entry["agent_id"],
            entry["condition"],
            str(entry["repetition"]),
        )
    )


def journal_paths(output_root: Path, sequence_index: int, attempt: int) -> JournalPaths:
    stem = f"{sequence_index:04d}.attempt-{attempt}"
    root = output_root / "request_journal"
    return JournalPaths(root / f"{stem}.intent.json", root / f"{stem}.response.json")


def record_path(output_root: Path, sequence_index: int) -> Path:
    return output_root / "records" / f"{sequence_index:04d}.json"


def failure_path(output_root: Path, sequence_index: int, attempt: int) -> Path:
    return output_root / "failures" / f"{sequence_index:04d}.attempt-{attempt}.json"


def load_schema(name: str) -> dict[str, Any]:
    return load_json(SCHEMA_DIR / name)


def expanded_schema(name: str) -> dict[str, Any]:
    schema = load_schema(name)
    diagnostic = load_json(HERE.parent / "conditions/diagnostic_output.schema.json")
    if name == "exp3v2_inference_repetition_record.schema.json":
        schema["properties"]["parsed_final_output"] = diagnostic
    if name == "exp3v2_inference_aggregate.schema.json":
        schema["properties"]["parsed_output"] = diagnostic
    return schema


def validate_json(value: Any, schema_name: str) -> None:
    schema = (
        expanded_schema(schema_name)
        if schema_name
        in {
            "exp3v2_inference_repetition_record.schema.json",
            "exp3v2_inference_aggregate.schema.json",
        }
        else load_schema(schema_name)
    )
    jsonschema.Draft202012Validator(schema).validate(value)


class ExclusiveLock:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.owned = False

    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            descriptor = os.open(self.path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError as exc:
            raise RuntimeError(
                f"exclusive execution lock exists; stale locks require human removal: {self.path}"
            ) from exc
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(
                canonical_json({"pid": os.getpid(), "created_at": utc_now()}) + "\n"
            )
            stream.flush()
            os.fsync(stream.fileno())
        fsync_directory(self.path.parent)
        self.owned = True
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        del exc_type, exc, traceback
        if self.owned and self.path.exists():
            self.path.unlink()
            fsync_directory(self.path.parent)
            self.owned = False


def request_prompt(base_prompt: str, attempt: int) -> str:
    if attempt == 1:
        return base_prompt
    return base_prompt + CORRECTION_SUFFIX


def normalize_provider_response(response: Any) -> dict[str, Any]:
    value = response.to_dict() if hasattr(response, "to_dict") else dict(response)
    required = {
        "raw_output",
        "requested_model",
        "returned_model",
        "response_id",
        "request_id",
        "input_tokens",
        "output_tokens",
        "total_tokens",
        "usage_raw",
        "response_raw",
        "sdk_version",
        "api_family",
        "endpoint",
    }
    missing = sorted(required - set(value))
    if missing:
        raise RuntimeError(f"provider response missing fields: {missing}")
    return {key: value[key] for key in sorted(required)}


def make_intent(
    entry: dict[str, Any], rendered: Any, attempt: int, current_prompt: str
) -> dict[str, Any]:
    return {
        "record_type": "request_intent",
        "sequence_index": entry["sequence_index"],
        "attempt": attempt,
        "job_key": job_key(entry),
        "timestamp": utc_now(),
        "base_prompt_hash": rendered.prompt_hash,
        "prompt_hash": sha256_bytes(current_prompt.encode("utf-8")),
        "input_hash": rendered.input_hash,
        "requested_model": MODEL,
        "request_parameters": REQUEST_PARAMETERS,
        "response": None,
    }


def make_response_entry(
    intent: dict[str, Any], response: dict[str, Any]
) -> dict[str, Any]:
    return {
        **{key: intent[key] for key in intent if key != "response"},
        "record_type": "provider_response",
        "timestamp": utc_now(),
        "response": response,
    }


def validate_record(
    record: dict[str, Any], entry: dict[str, Any], rendered: Any, assets: Any
) -> None:
    validate_json(record, "exp3v2_inference_repetition_record.schema.json")
    for field in SCHEDULE_SCHEMA_KEYS:
        if record[field] != entry[field]:
            raise RuntimeError(f"record schedule mismatch: {field}")
    if (
        record["prompt_hash"] != rendered.prompt_hash
        or record["input_hash"] != rendered.input_hash
    ):
        raise RuntimeError("record prompt/input hash mismatch")
    if record["raw_output"] != record["raw_attempts"][-1]:
        raise RuntimeError("record final raw output mismatch")
    if record["retry_count"] != len(record["provider_attempts"]) - 1:
        raise RuntimeError("record retry count mismatch")
    responses = [item["response"] for item in record["provider_attempts"]]
    if record["raw_attempts"] != [item["raw_output"] for item in responses]:
        raise RuntimeError("record raw-attempt preservation mismatch")
    if record["total_tokens"] != record["input_tokens"] + record["output_tokens"]:
        raise RuntimeError("record final token total mismatch")
    if record["cumulative_total_tokens"] != (
        record["cumulative_input_tokens"] + record["cumulative_output_tokens"]
    ):
        raise RuntimeError("record cumulative token total mismatch")
    if record["parse_failure"]:
        try:
            assets.parse(record["raw_output"], rendered.available_insight_ids)
        except Exception:
            pass
        else:
            raise RuntimeError("parse-failure record contains a valid final output")
        if record["parsed_final_output"] != PARSE_FAILURE_OUTPUT or len(responses) != 3:
            raise RuntimeError("invalid parse-failure record")
    else:
        parsed = assets.parse(record["raw_output"], rendered.available_insight_ids)
        if parsed != record["parsed_final_output"]:
            raise RuntimeError("parsed output mismatch")
    if record["condition"] == "A" and record["parsed_final_output"]["used_insight_ids"]:
        raise RuntimeError("condition A used peer insight IDs")


def scan_ambiguous_state(
    schedule: list[dict[str, Any]], assets: Any, output_root: Path
) -> None:
    journal_root = output_root / "request_journal"
    records_root = output_root / "records"
    failures_root = output_root / "failures"
    allowed_top = {"request_journal", "records", "failures", "execution.lock"}
    allowed_top.update(
        {
            "repetition_records.jsonl",
            "aggregate_records.jsonl",
            "execution_metadata.json",
            "inference_output_hash_manifest.json",
        }
    )
    extra_top = {path.name for path in output_root.iterdir()} - allowed_top
    if extra_top:
        raise RuntimeError(f"unexpected output-root entries: {sorted(extra_top)}")
    pattern = re.compile(r"^(\d{4})\.attempt-([1-3])\.(intent|response)\.json$")
    if journal_root.exists():
        for path in journal_root.iterdir():
            match = pattern.fullmatch(path.name)
            if path.is_symlink() or not path.is_file() or not match:
                raise RuntimeError(f"unexpected request-journal artifact: {path.name}")
            sequence_index, attempt = int(match.group(1)), int(match.group(2))
            if sequence_index >= len(schedule):
                raise RuntimeError("request journal sequence is out of range")
            paths = journal_paths(output_root, sequence_index, attempt)
            if path == paths.response and not paths.intent.exists():
                raise RuntimeError("provider response exists without request intent")
    if records_root.exists():
        for path in records_root.iterdir():
            if path.is_symlink() or not re.fullmatch(r"\d{4}\.json", path.name):
                raise RuntimeError(f"unexpected record artifact: {path.name}")
    if failures_root.exists():
        for path in failures_root.iterdir():
            if path.is_symlink() or not re.fullmatch(
                r"\d{4}\.attempt-[1-3]\.json", path.name
            ):
                raise RuntimeError(f"unexpected failure artifact: {path.name}")

    for entry in schedule:
        sequence_index = entry["sequence_index"]
        rendered = assets.render(entry)
        completed = record_path(output_root, sequence_index).exists()
        for attempt in range(1, 4):
            paths = journal_paths(output_root, sequence_index, attempt)
            if paths.intent.exists():
                intent = load_json(paths.intent)
                validate_json(intent, "exp3v2_inference_request_journal.schema.json")
                current = request_prompt(rendered.text, attempt)
                if (
                    intent["sequence_index"] != sequence_index
                    or intent["attempt"] != attempt
                ):
                    raise RuntimeError("request intent schedule mismatch")
                if intent["job_key"] != job_key(entry):
                    raise RuntimeError("request intent job key mismatch")
                if intent["base_prompt_hash"] != rendered.prompt_hash:
                    raise RuntimeError("request intent base prompt hash mismatch")
                if intent["prompt_hash"] != sha256_bytes(current.encode("utf-8")):
                    raise RuntimeError("request intent submitted prompt hash mismatch")
                if intent["input_hash"] != rendered.input_hash:
                    raise RuntimeError("request intent input hash mismatch")
                if not paths.response.exists():
                    if completed:
                        raise RuntimeError(
                            "validated record exists without durable provider response"
                        )
                    raise AmbiguousRequestError(entry, rendered, attempt, paths.intent)
                response_entry = load_json(paths.response)
                validate_json(
                    response_entry, "exp3v2_inference_request_journal.schema.json"
                )
                for key in (
                    "sequence_index",
                    "attempt",
                    "job_key",
                    "base_prompt_hash",
                    "prompt_hash",
                    "input_hash",
                    "requested_model",
                    "request_parameters",
                ):
                    if response_entry[key] != intent[key]:
                        raise RuntimeError(f"provider response journal mismatch: {key}")
            elif paths.response.exists():
                raise RuntimeError("provider response exists without request intent")
        if completed:
            record = load_json(record_path(output_root, sequence_index))
            validate_record(record, entry, rendered, assets)
            validate_record_journal(record, output_root)


def write_failure(
    output_root: Path,
    entry: dict[str, Any],
    rendered: Any,
    attempt: int,
    intent_path: Path,
    error: BaseException,
) -> None:
    value = {
        "failure_kind": "infrastructure_failure",
        "sequence_index": entry["sequence_index"],
        "attempt": attempt,
        "job_key": job_key(entry),
        "timestamp": utc_now(),
        "prompt_hash": sha256_bytes(
            request_prompt(rendered.text, attempt).encode("utf-8")
        ),
        "input_hash": rendered.input_hash,
        "intent_path": str(intent_path.relative_to(output_root)),
        "response_path": None,
        "ambiguous": True,
        "error_type": type(error).__name__,
        "message": str(error),
    }
    validate_json(value, "exp3v2_inference_failure.schema.json")
    atomic_write_immutable(
        failure_path(output_root, entry["sequence_index"], attempt),
        canonical_json_bytes(value),
    )


def write_ambiguous_failure(output_root: Path, error: AmbiguousRequestError) -> None:
    path = failure_path(output_root, error.entry["sequence_index"], error.attempt)
    if path.exists():
        existing = load_json(path)
        validate_json(existing, "exp3v2_inference_failure.schema.json")
        return
    value = {
        "failure_kind": "ambiguous_request_state",
        "sequence_index": error.entry["sequence_index"],
        "attempt": error.attempt,
        "job_key": job_key(error.entry),
        "timestamp": utc_now(),
        "prompt_hash": sha256_bytes(
            request_prompt(error.rendered.text, error.attempt).encode("utf-8")
        ),
        "input_hash": error.rendered.input_hash,
        "intent_path": str(error.intent_path.relative_to(output_root)),
        "response_path": None,
        "ambiguous": True,
        "error_type": "AmbiguousRequestError",
        "message": str(error),
    }
    validate_json(value, "exp3v2_inference_failure.schema.json")
    atomic_write_immutable(path, canonical_json_bytes(value))


def execute_job(
    entry: dict[str, Any], rendered: Any, assets: Any, output_root: Path, adapter: Any
) -> dict[str, Any]:
    provider_attempts: list[dict[str, Any]] = []
    raw_attempts: list[str] = []
    errors: list[str] = []
    parsed: dict[str, Any] | None = None
    parse_failure = False

    for attempt in range(1, MAX_STRUCTURAL_RETRIES + 2):
        current_prompt = request_prompt(rendered.text, attempt)
        paths = journal_paths(output_root, entry["sequence_index"], attempt)
        if paths.intent.exists() or paths.response.exists():
            raise RuntimeError("job execution encountered pre-existing journal state")
        intent = make_intent(entry, rendered, attempt, current_prompt)
        validate_json(intent, "exp3v2_inference_request_journal.schema.json")
        atomic_write_immutable(paths.intent, canonical_json_bytes(intent))
        try:
            provider_value = normalize_provider_response(
                adapter.create_response(
                    prompt=current_prompt,
                    reasoning_effort=REASONING_EFFORT,
                    schema=assets.provider_schema,
                    max_output_tokens=MAX_OUTPUT_TOKENS,
                )
            )
        except BaseException as exc:
            write_failure(output_root, entry, rendered, attempt, paths.intent, exc)
            raise
        response_entry = make_response_entry(intent, provider_value)
        validate_json(response_entry, "exp3v2_inference_request_journal.schema.json")
        atomic_write_immutable(paths.response, canonical_json_bytes(response_entry))
        provider_attempts.append(
            {
                "attempt": attempt,
                "intent_path": str(paths.intent.relative_to(output_root)),
                "response_path": str(paths.response.relative_to(output_root)),
                "response": provider_value,
            }
        )
        raw_attempts.append(provider_value["raw_output"])
        try:
            parsed = assets.parse(
                provider_value["raw_output"], rendered.available_insight_ids
            )
            break
        except Exception as exc:
            errors.append(str(exc))
            if attempt == 3:
                parsed = dict(PARSE_FAILURE_OUTPUT)
                parse_failure = True

    if parsed is None:
        raise AssertionError("unreachable execution state")
    final = provider_attempts[-1]["response"]
    for name in ("input_tokens", "output_tokens", "total_tokens"):
        if type(final[name]) is not int or final[name] < 0:
            raise RuntimeError(f"provider token accounting unavailable: {name}")
    if final["total_tokens"] != final["input_tokens"] + final["output_tokens"]:
        raise RuntimeError("provider final token accounting mismatch")
    if any(item["response"]["returned_model"] != MODEL for item in provider_attempts):
        raise RuntimeError("provider returned model differs from frozen identity")

    record = {
        **entry,
        "requested_model": MODEL,
        "returned_model": MODEL,
        "reasoning_effort": REASONING_EFFORT,
        "temperature": None,
        "seed": None,
        "max_output_tokens": MAX_OUTPUT_TOKENS,
        "structured_outputs_strict": True,
        "max_structural_retries": MAX_STRUCTURAL_RETRIES,
        "prompt_hash": rendered.prompt_hash,
        "input_hash": rendered.input_hash,
        "prompt_character_count": rendered.character_count,
        "available_insight_ids": list(rendered.available_insight_ids),
        "provider_attempts": provider_attempts,
        "raw_attempts": raw_attempts,
        "raw_output": raw_attempts[-1],
        "parsed_final_output": parsed,
        "parse_failure": parse_failure,
        "structural_validation_errors": errors,
        "input_tokens": final["input_tokens"],
        "output_tokens": final["output_tokens"],
        "total_tokens": final["total_tokens"],
        "cumulative_input_tokens": sum(
            item["response"]["input_tokens"] for item in provider_attempts
        ),
        "cumulative_output_tokens": sum(
            item["response"]["output_tokens"] for item in provider_attempts
        ),
        "cumulative_total_tokens": sum(
            item["response"]["total_tokens"] for item in provider_attempts
        ),
        "retry_count": len(provider_attempts) - 1,
        "timestamp": response_entry["timestamp"],
        "stateless": True,
        "store": False,
        "previous_response_id_used": False,
    }
    validate_record(record, entry, rendered, assets)
    atomic_write_immutable(
        record_path(output_root, entry["sequence_index"]), canonical_json_bytes(record)
    )
    return record


def load_validated_records(
    schedule: list[dict[str, Any]], assets: Any, output_root: Path
) -> dict[int, dict[str, Any]]:
    records: dict[int, dict[str, Any]] = {}
    for entry in schedule:
        path = record_path(output_root, entry["sequence_index"])
        if not path.exists():
            continue
        rendered = assets.render(entry)
        record = load_json(path)
        validate_record(record, entry, rendered, assets)
        validate_record_journal(record, output_root)
        records[entry["sequence_index"]] = record
    return records


def validate_record_journal(record: dict[str, Any], output_root: Path) -> None:
    for index, provider_attempt in enumerate(record["provider_attempts"], start=1):
        if provider_attempt.get("attempt") != index:
            raise RuntimeError("provider-attempt order mismatch")
        intent_path = output_root / provider_attempt["intent_path"]
        response_path = output_root / provider_attempt["response_path"]
        expected = journal_paths(output_root, record["sequence_index"], index)
        if intent_path != expected.intent or response_path != expected.response:
            raise RuntimeError("provider-attempt journal path mismatch")
        intent = load_json(intent_path)
        response = load_json(response_path)
        validate_json(intent, "exp3v2_inference_request_journal.schema.json")
        validate_json(response, "exp3v2_inference_request_journal.schema.json")
        if response["response"] != provider_attempt["response"]:
            raise RuntimeError(
                "validated record differs from durable provider response"
            )
    for attempt in range(len(record["provider_attempts"]) + 1, 4):
        paths = journal_paths(output_root, record["sequence_index"], attempt)
        if paths.intent.exists() or paths.response.exists():
            raise RuntimeError(
                "journal contains attempts after the validated final attempt"
            )


def aggregate_records(
    records: list[dict[str, Any]], assets: Any
) -> list[dict[str, Any]]:
    aggregation_module = importlib.import_module("phase_b.evaluation.aggregation")
    records_module = importlib.import_module("phase_b.evaluation.records")
    frozen = [
        records_module.RunRecord(
            agent_id=item["agent_id"],
            condition=item["condition"],
            repetition=item["repetition"],
            model=item["requested_model"],
            model_version=item["returned_model"],
            prompt_hash=item["prompt_hash"],
            input_hash=item["input_hash"],
            raw_output=item["raw_output"],
            raw_attempts=tuple(item["raw_attempts"]),
            parsed_output=item["parsed_final_output"],
            physical_case_id=item["physical_case_id"],
            temperature=None,
            seed=None,
            timestamp=item["timestamp"],
            prompt_tokens=item["input_tokens"],
            completion_tokens=item["output_tokens"],
            token_count_method="response.usage",
        )
        for item in records
    ]
    derived = aggregation_module.aggregate_run_records(
        frozen, label_space=assets.protocol["label_space"]
    )
    by_key = {
        (item.physical_case_id, item.agent_id, item.condition): item for item in derived
    }
    case_order = list(dict.fromkeys(item["physical_case_id"] for item in records))
    values: list[dict[str, Any]] = []
    for case_id in case_order:
        for agent_id in AGENT_PACK:
            for condition in ("A", "B", "E"):
                item = by_key[(case_id, agent_id, condition)]
                value = {
                    "physical_case_id": item.physical_case_id,
                    "agent_id": item.agent_id,
                    "condition": item.condition,
                    "parsed_output": item.parsed_output,
                    "repetition_outcomes": list(item.repetition_outcomes),
                    "aggregation_rule": "frozen_valid_label_majority_2_of_3_else_abstain",
                }
                validate_json(value, "exp3v2_inference_aggregate.schema.json")
                values.append(value)
    if len(values) != 360:
        raise RuntimeError("aggregate record count is not 360")
    return values


def output_inventory(
    output_root: Path, paths: list[Path]
) -> tuple[list[dict[str, Any]], str]:
    artifacts = [
        {
            "path": str(path.relative_to(output_root)),
            "size_bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        }
        for path in sorted(paths, key=lambda item: str(item.relative_to(output_root)))
    ]
    return artifacts, sha256_bytes(canonical_json_bytes(artifacts))


def finalize_outputs(
    schedule: list[dict[str, Any]],
    records: list[dict[str, Any]],
    assets: Any,
    output_root: Path,
    schedule_sha256: str,
) -> dict[str, Any]:
    if len(records) != 1080 or [item["sequence_index"] for item in records] != list(
        range(1080)
    ):
        raise RuntimeError("cannot finalize an incomplete or reordered record set")
    if Counter(item["condition"] for item in records) != Counter(
        {"A": 360, "B": 360, "E": 360}
    ):
        raise RuntimeError("final record condition counts mismatch")
    repetitions_path = output_root / "repetition_records.jsonl"
    aggregates_path = output_root / "aggregate_records.jsonl"
    metadata_path = output_root / "execution_metadata.json"
    output_manifest_path = output_root / "inference_output_hash_manifest.json"

    atomic_write_immutable(
        repetitions_path,
        b"".join(canonical_json_bytes(item) for item in records),
    )
    aggregates = aggregate_records(records, assets)
    atomic_write_immutable(
        aggregates_path,
        b"".join(canonical_json_bytes(item) for item in aggregates),
    )
    failures = (
        list((output_root / "failures").glob("*.json"))
        if (output_root / "failures").exists()
        else []
    )
    metadata = {
        "status": "COMPLETE_PENDING_INFERENCE_DATA_FREEZE",
        "planned_repetition_records": 1080,
        "completed_repetition_records": 1080,
        "condition_counts": {"A": 360, "B": 360, "E": 360},
        "aggregate_records": 360,
        "schedule_sha256": schedule_sha256,
        "schedule_adherence": True,
        "stateless_calls": True,
        "single_process_sequential": True,
        "provider": "openai",
        "requested_model": MODEL,
        "returned_models": [MODEL],
        "reasoning_effort": REASONING_EFFORT,
        "temperature": None,
        "seed": None,
        "max_output_tokens": MAX_OUTPUT_TOKENS,
        "structured_outputs_strict": True,
        "max_structural_retries": MAX_STRUCTURAL_RETRIES,
        "structural_retries_total": sum(item["retry_count"] for item in records),
        "provider_network_failures": len(failures),
        "ambiguous_request_states": 0,
        "final_parse_failures": sum(item["parse_failure"] for item in records),
        "provider_attempts": sum(len(item["provider_attempts"]) for item in records),
        "cumulative_input_tokens": sum(
            item["cumulative_input_tokens"] for item in records
        ),
        "cumulative_output_tokens": sum(
            item["cumulative_output_tokens"] for item in records
        ),
        "cumulative_total_tokens": sum(
            item["cumulative_total_tokens"] for item in records
        ),
        "token_accounting_complete": True,
        "ground_truth_joined": False,
        "metrics_calculated": False,
        "completed_at": max(item["timestamp"] for item in records),
    }
    validate_json(metadata, "exp3v2_inference_execution_metadata.schema.json")
    atomic_write_immutable(metadata_path, canonical_json_bytes(metadata))

    journal_paths_all = list((output_root / "request_journal").glob("*.json"))
    record_paths_all = list((output_root / "records").glob("*.json"))
    artifacts, inventory_sha = output_inventory(
        output_root,
        journal_paths_all
        + record_paths_all
        + failures
        + [repetitions_path, aggregates_path, metadata_path],
    )
    output_manifest = {
        "schema_version": "1.0",
        "status": "COMPLETE_PENDING_INFERENCE_DATA_FREEZE",
        "schedule_sha256": schedule_sha256,
        "repetition_record_count": 1080,
        "aggregate_record_count": 360,
        "artifacts": artifacts,
        "inventory_sha256": inventory_sha,
        "ground_truth_included": False,
        "metrics_calculated": False,
    }
    validate_json(output_manifest, "exp3v2_inference_output_hash_manifest.schema.json")
    atomic_write_immutable(output_manifest_path, canonical_json_bytes(output_manifest))
    return output_manifest


def run_execution(
    schedule: list[dict[str, Any]],
    assets: Any,
    output_root: Path,
    adapter: Any | None,
    schedule_sha256: str,
    adapter_factory: Any | None = None,
) -> dict[str, Any]:
    output_root.mkdir(parents=True, exist_ok=True)
    with ExclusiveLock(output_root / "execution.lock"):
        try:
            scan_ambiguous_state(schedule, assets, output_root)
        except AmbiguousRequestError as exc:
            write_ambiguous_failure(output_root, exc)
            raise
        existing = load_validated_records(schedule, assets, output_root)
        if len(existing) < 1080 and adapter is None:
            if adapter_factory is None:
                raise RuntimeError("provider adapter factory is unavailable")
            adapter = adapter_factory()
        for entry in schedule:
            sequence_index = entry["sequence_index"]
            if sequence_index in existing:
                continue
            rendered = assets.render(entry)
            existing[sequence_index] = execute_job(
                entry, rendered, assets, output_root, adapter
            )
        records = [existing[index] for index in range(1080)]
        return finalize_outputs(schedule, records, assets, output_root, schedule_sha256)


def main(argv: list[str] | None = None, *, client: Any | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--verbalization-harness-root", type=Path, required=True)
    parser.add_argument("--verbalizations-root", type=Path, required=True)
    parser.add_argument("--authorization-manifest", type=Path, required=True)
    parser.add_argument("--authorization-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args(argv)
    manifest = load_json(args.manifest)
    expected = manifest["future_execution"]
    if args.manifest.resolve() != Path(expected["manifest_path"]):
        raise RuntimeError("manifest argument differs from frozen future command")
    if args.verbalizations_root.resolve() != Path(expected["verbalizations_root"]):
        raise RuntimeError("verbalizations-root differs from frozen future command")
    if args.source_root.resolve() != Path(expected["source_root"]):
        raise RuntimeError("source-root differs from frozen future command")
    if args.data_root.resolve() != Path(expected["data_root"]):
        raise RuntimeError("data-root differs from frozen future command")
    if args.verbalization_harness_root.resolve() != Path(
        expected["verbalization_harness_root"]
    ):
        raise RuntimeError(
            "verbalization-harness-root differs from frozen future command"
        )
    if args.output_root.absolute() != Path(expected["output_root"]):
        raise RuntimeError("output-root differs from frozen future command")
    if args.authorization_manifest.resolve() != Path(
        expected["authorization_manifest_path"]
    ):
        raise RuntimeError("authorization-manifest differs from frozen future command")
    if args.authorization_root.resolve() != Path(expected["authorization_root"]):
        raise RuntimeError("authorization-root differs from frozen future command")

    upstream_roots = {
        "exp3-v2-heldout-frozen-002": args.source_root,
        "exp3-v2-heldout-data-frozen-001": args.data_root,
        "exp3-v2-verbalization-harness-frozen-001": args.verbalization_harness_root,
        "exp3-v2-verbalizations-frozen-001": args.verbalizations_root,
    }
    harness_root = verify_boundaries(manifest, args.manifest, upstream_roots)
    verify_execution_authorization(
        manifest,
        args.manifest,
        harness_root,
        args.authorization_manifest,
        args.authorization_root,
    )
    runtime_validator = importlib.import_module(
        "phase_b.exp3_v2.validate_exp3v2_inference_runtime"
    )
    runtime_validator.validate_runtime(Path(manifest["runtime"]["lock_path"]))
    schedule_path = harness_root / manifest["schedule"]["path"]
    schedule = load_json(schedule_path)
    validate_schedule(schedule, manifest["schedule"]["sha256"])
    case_texts = load_case_texts(manifest, args.verbalizations_root)
    assets = FrozenAssets(harness_root, case_texts)

    if not args.output_root.exists():
        pass
    elif not args.output_root.is_dir() or args.output_root.is_symlink():
        raise RuntimeError("output root is not a regular directory")

    def adapter_factory():
        adapter_module = importlib.import_module("phase_b.execution.openai_adapter")
        if client is None:
            return adapter_module.OpenAIAdapter(
                requested_model=MODEL,
                timeout_seconds=TIMEOUT_SECONDS,
            )
        return adapter_module.OpenAIAdapter(requested_model=MODEL, client=client)

    result = run_execution(
        schedule,
        assets,
        args.output_root,
        None,
        manifest["schedule"]["sha256"],
        adapter_factory,
    )
    print(
        canonical_json(
            {"status": "PASS", "inventory_sha256": result["inventory_sha256"]}
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
