"""Shared frozen-input and local-server helpers for the EXP2 Qwen lane."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

from phase_b.conditions.builders import render_diagnostic_prompt
from phase_b.config import load_protocol_config
from phase_b.insights import validate_global_insights


ROOT = Path(__file__).resolve().parents[3]
LANE_DIR = ROOT / "phase_b/exp2/qwen"
CONFIG_PATH = LANE_DIR / "config.json"
SCHEMA_PATH = ROOT / "phase_b/conditions/diagnostic_output.openai.schema.json"
SCHEDULE_PATH = ROOT / "phase_b/final_evaluation/inference_schedule.json"
VERBALIZATION_MANIFEST_PATH = (
    ROOT / "phase_b/final_evaluation/heldout_verbalizations_manifest.json"
)
LOCAL_EXAMPLES_PATH = ROOT / "phase_b/local_knowledge/local_examples.json"
GLOBAL_INSIGHTS_PATH = ROOT / "phase_b/insights/final_local_insights.json"
DERANGEMENTS_PATH = (
    ROOT / "phase_b/config/evaluator_side/condition_e_derangements.json"
)
ORIGINAL_RECORDS_PATH = (
    ROOT / "phase_b/final_evaluation/inference/repetition_records.jsonl"
)
AGENT_PACK = {
    "agent_1": "LKP-001",
    "agent_2": "LKP-002",
    "agent_3": "LKP-003",
    "agent_4": "LKP-004",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_frozen_hashes(config: dict[str, Any] | None = None) -> None:
    config = load_json(CONFIG_PATH) if config is None else config
    if sha256_file(SCHEDULE_PATH) != config["schedule_sha256"]:
        raise RuntimeError("frozen schedule SHA-256 mismatch")
    for relative, expected in config["frozen_input_hashes"].items():
        path = ROOT / relative
        if sha256_file(path) != expected:
            raise RuntimeError(f"frozen input SHA-256 mismatch: {relative}")


class FrozenPromptInputs:
    """Read-only view over the original Experiment 1 prompt-facing inputs."""

    def __init__(self) -> None:
        self.protocol = load_protocol_config()
        artifact = load_json(LOCAL_EXAMPLES_PATH)
        self.local_examples = {
            agent: artifact["packs"][pack] for agent, pack in AGENT_PACK.items()
        }
        self.global_insights = validate_global_insights(
            load_json(GLOBAL_INSIGHTS_PATH), self.protocol
        )
        self.derangements = load_json(DERANGEMENTS_PATH)["derangements"]
        manifest = load_json(VERBALIZATION_MANIFEST_PATH)
        self.case_text = {
            item["physical_case_id"]: (
                ROOT / item["neutral_text_path"]
            ).read_text(encoding="utf-8").strip()
            for item in manifest["cases"]
        }

    def render(self, entry: dict[str, Any]):
        condition = entry["condition"]
        return render_diagnostic_prompt(
            agent_id=entry["agent_id"],
            condition=condition,
            case_text=self.case_text[entry["physical_case_id"]],
            local_examples=self.local_examples[entry["agent_id"]],
            config=self.protocol,
            global_insights=None if condition == "A" else self.global_insights,
            derangements=self.derangements if condition == "E" else None,
        )


def http_json(
    url: str,
    *,
    payload: dict[str, Any] | None = None,
    timeout: float = 30.0,
) -> dict[str, Any]:
    data = None if payload is None else canonical_json(payload).encode("utf-8")
    request = Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="GET" if payload is None else "POST",
    )
    with urlopen(request, timeout=timeout) as response:
        value = json.loads(response.read().decode("utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"expected JSON object from {url}")
    return value


def discover_server(config: dict[str, Any]) -> dict[str, Any]:
    origin = config["base_url"].removesuffix("/v1")
    version = http_json(f"{origin}/version")
    models = http_json(f"{config['base_url']}/models")
    matches = [
        item for item in models.get("data", [])
        if item.get("id") == config["requested_model"]
    ]
    if len(matches) != 1:
        raise RuntimeError("requested model alias is missing or ambiguous")
    model = matches[0]
    return {
        "vllm_version": version.get("version"),
        "requested_model": config["requested_model"],
        "model_id": model.get("id"),
        "model_root": model.get("root"),
        "max_model_len": model.get("max_model_len"),
        "owned_by": model.get("owned_by"),
    }


def tokenize_prompt(config: dict[str, Any], prompt: str) -> int:
    value = http_json(
        f"{config['base_url'].removesuffix('/v1')}/tokenize",
        payload={"model": config["requested_model"], "prompt": prompt},
        timeout=60.0,
    )
    count = value.get("count")
    if type(count) is not int:
        tokens = value.get("tokens")
        if isinstance(tokens, list):
            count = len(tokens)
    if type(count) is not int or count < 0:
        raise RuntimeError("/tokenize did not return a usable token count")
    return count


def original_prompt_hashes() -> dict[tuple[str, str, str], str]:
    lookup: dict[tuple[str, str, str], str] = {}
    for line in ORIGINAL_RECORDS_PATH.read_text(encoding="utf-8").splitlines():
        record = json.loads(line)
        key = (
            record["physical_case_id"],
            record["agent_id"],
            record["condition"],
        )
        previous = lookup.setdefault(key, record["prompt_hash"])
        if previous != record["prompt_hash"]:
            raise RuntimeError(f"original repetitions changed prompt hash: {key}")
    if len(lookup) != 180:
        raise RuntimeError("original prompt-hash lookup must contain 180 keys")
    return lookup
