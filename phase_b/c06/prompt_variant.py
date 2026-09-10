"""Construct B_LOCAL_FIRST_V1 from the byte-verified frozen B prompt."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import subprocess
from typing import Any

from phase_b.conditions import builders
from phase_b.config import load_protocol_config, validate_execution_ready
from phase_b.insights import validate_global_insights
from phase_b.prompts.leakage import scan_text

from .constants import (
    AGENT_PACK,
    C06_ROOT,
    FROZEN_WORKTREE_HASHES,
    HARNESS_COMMIT,
    HARNESS_TAG,
    HARNESS_TAG_OBJECT,
    LOCAL_FIRST_BLOCK,
    PROMPT_ANCHOR,
    ROOT,
    INFERENCE_GOVERNANCE_COMMIT,
    INFERENCE_TAG,
    INFERENCE_TAG_OBJECT,
    VERBALIZATION_GOVERNANCE_COMMIT,
    VERBALIZATION_TAG,
    VERBALIZATION_TAG_OBJECT,
    VERBALIZATION_PAYLOAD_COMMIT,
)


FORBIDDEN_PROMPT_SUBSTRINGS = (
    "exp3v2-",
    "local-seen",
    "local-unseen",
    "fault_id",
    "class_offline",
    "output_path",
    ".xlsx",
    "/private/",
    "/users/",
)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def git_show(commit: str, path: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
    ).stdout


def git_text(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ).stdout.strip()


def verify_annotated_tag(
    name: str, expected_object: str, expected_commit: str
) -> None:
    actual_object = git_text("rev-parse", f"refs/tags/{name}")
    if actual_object != expected_object:
        raise RuntimeError(f"annotated tag object mismatch: {name}")
    if git_text("cat-file", "-t", actual_object) != "tag":
        raise RuntimeError(f"tag is not annotated: {name}")
    if git_text("rev-parse", f"refs/tags/{name}^{{commit}}") != expected_commit:
        raise RuntimeError(f"tag target mismatch: {name}")


def verify_frozen_worktree() -> None:
    verify_annotated_tag(HARNESS_TAG, HARNESS_TAG_OBJECT, HARNESS_COMMIT)
    verify_annotated_tag(
        INFERENCE_TAG, INFERENCE_TAG_OBJECT, INFERENCE_GOVERNANCE_COMMIT
    )
    verify_annotated_tag(
        VERBALIZATION_TAG,
        VERBALIZATION_TAG_OBJECT,
        VERBALIZATION_GOVERNANCE_COMMIT,
    )
    for relative, expected in FROZEN_WORKTREE_HASHES.items():
        path = ROOT / relative
        if not path.is_file() or path.is_symlink():
            raise RuntimeError(f"frozen dependency missing or symlinked: {relative}")
        actual = sha256_file(path)
        if actual != expected:
            raise RuntimeError(f"frozen dependency hash mismatch: {relative}")
        tagged = sha256_bytes(git_show(HARNESS_COMMIT, relative))
        if tagged != expected:
            raise RuntimeError(f"harness-tag dependency hash mismatch: {relative}")


def insert_local_first(text: str) -> str:
    if text.count(PROMPT_ANCHOR) != 1:
        raise RuntimeError("frozen B prompt anchor is not unique")
    return text.replace(PROMPT_ANCHOR, PROMPT_ANCHOR + "\n\n" + LOCAL_FIRST_BLOCK)


@dataclass(frozen=True)
class RenderedVariant:
    text: str
    prompt_hash: str
    input_hash: str
    available_insight_ids: tuple[str, ...]
    character_count: int


class PromptAssets:
    """Prompt-side assets only; evaluator-side files are deliberately not loaded."""

    def __init__(self) -> None:
        verify_frozen_worktree()
        self.protocol = load_protocol_config(ROOT / "phase_b/config/protocol_config.json")
        validate_execution_ready(self.protocol)
        examples = json.loads(
            (ROOT / "phase_b/local_knowledge/local_examples.json").read_text(
                encoding="utf-8"
            )
        )
        self.local_examples = {
            agent_id: examples["packs"][pack_id]
            for agent_id, pack_id in AGENT_PACK.items()
        }
        raw_insights = json.loads(
            (ROOT / "phase_b/insights/final_local_insights.json").read_text(
                encoding="utf-8"
            )
        )
        self.global_insights = validate_global_insights(raw_insights, self.protocol)
        self.provider_schema = json.loads(
            (
                ROOT
                / "phase_b/conditions/diagnostic_output.openai.schema.json"
            ).read_text(encoding="utf-8")
        )
        manifest_bytes = git_show(
            VERBALIZATION_PAYLOAD_COMMIT,
            "verbalization_outputs/EXP3_V2_VERBALIZATION_OUTPUT_MANIFEST_001.json",
        )
        if sha256_bytes(manifest_bytes) != "79f9331ba7bf1f17a8ee0c60dd85c9e73a1cc59e13341e8b6e46fc6068039b1a":
            raise RuntimeError("frozen verbalization manifest hash mismatch")
        manifest = json.loads(manifest_bytes)
        self.case_manifest = {
            item["physical_case_id"]: item for item in manifest["cases"]
        }

    def case_text(self, case_id: str) -> str:
        item = self.case_manifest[case_id]
        relative = "verbalization_outputs/" + item["neutral_text_path"]
        payload = git_show(VERBALIZATION_PAYLOAD_COMMIT, relative)
        if len(payload) != item["neutral_text_size_bytes"]:
            raise RuntimeError(f"neutral text size mismatch: {case_id}")
        if sha256_bytes(payload) != item["neutral_text_sha256"]:
            raise RuntimeError(f"neutral text hash mismatch: {case_id}")
        return payload.decode("utf-8").strip()

    def render(self, agent_id: str, case_id: str) -> RenderedVariant:
        case_text = self.case_text(case_id)
        base = builders.render_diagnostic_prompt(
            agent_id=agent_id,
            condition="B",
            case_text=case_text,
            local_examples=self.local_examples[agent_id],
            config=self.protocol,
            global_insights=self.global_insights,
        )
        text = insert_local_first(base.text)
        variant_template = (C06_ROOT / "prompts/B_LOCAL_FIRST_V1.txt").read_text(
            encoding="utf-8"
        )
        expected_template = insert_local_first(
            (ROOT / "phase_b/prompts/fot_B.txt").read_text(encoding="utf-8")
        )
        if variant_template != expected_template:
            raise RuntimeError("variant template is not the exact frozen B insertion")
        lowered = text.lower()
        if any(token in lowered for token in FORBIDDEN_PROMPT_SUBSTRINGS):
            raise RuntimeError("rendered prompt contains forbidden metadata")
        if scan_text(text, source=f"C06:{agent_id}:{case_id}"):
            raise RuntimeError("rendered prompt contains evaluator-side class identity")
        return RenderedVariant(
            text=text,
            prompt_hash=sha256_bytes(text.encode("utf-8")),
            input_hash=base.input_hash,
            available_insight_ids=base.available_insight_ids,
            character_count=len(text),
        )
