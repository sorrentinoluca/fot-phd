#!/usr/bin/env python3
"""Ablation experiment runner: 4 arms × 15 held-out cases × 3 repetitions.

Centralized diagnostic prompt (all 5 labels, 10 local examples: 2 per class).
Examples are rendered in each arm's own representation format.
Uses the same GPT-5.6-terra model and structured output as Phase B.

Review fixes applied:
  T2  — Token budget preflight with configurable limit
  T6  — Provenance hashing for resume integrity
  T7  — max_retries renamed max_attempts for clarity
  T8  — Structured output validation (consistency, refusal, schema)
  T13 — Normal examples temporally aligned (Time 0-based, config unchanged)
  T14 — Manifest validation (labels, files, class balance, XMEAS columns)
  L6  — Example ordering: deterministic shuffle per arm (seed=42)
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import logging
import os
import random
import sys
import time
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

# Defer module imports until project root is known (see _init_imports)
tep_features = None
tep_verbalize_v2 = None
ablation_representations = None


def _init_imports(project_root: Path) -> None:
    """Add project code/ dir and ablation dir to sys.path, then import modules."""
    global tep_features, tep_verbalize_v2, ablation_representations

    code_dir = str(project_root / "code")
    ablation_dir = str(Path(__file__).resolve().parent)

    for d in (code_dir, ablation_dir):
        if d not in sys.path:
            sys.path.insert(0, d)

    import tep_features as _tf
    import tep_verbalize_v2 as _tv
    import ablation_representations as _ar

    tep_features = _tf
    tep_verbalize_v2 = _tv
    ablation_representations = _ar


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
)
log = logging.getLogger(__name__)


# ── Paths (relative to project root, set at runtime) ──

ROOT: Path = Path(".")
CODE: Path = ROOT / "code"
CACHE: Path = CODE / "tep_cache"
HELDOUT: Path = ROOT / "tep_heldout/mode1"
MANIFEST_CSV: Path = ROOT / "phase_b/heldout/phase_b_heldout_manifest.csv"
BASELINE_PATH: Path = CACHE / "mode1_normal_500.xlsx"
CONFIG_PATH: Path = CODE / "verbalizer_config_v2.json"


# ── Label space (centralized: all five labels visible to all arms) ──

LABEL_SPACE = ["F1", "F8", "F10", "F13", "Normal"]

# Development example source: batches 1-2 for faults, N1-N2 for Normal
# 2 examples per class × 5 classes = 10 examples
EXAMPLE_SOURCES = {
    "F1":     [("mode1_1_1.xlsx",  "F1"),  ("mode1_1_2.xlsx",  "F1")],
    "F8":     [("mode1_8_1.xlsx",  "F8"),  ("mode1_8_2.xlsx",  "F8")],
    "F10":    [("mode1_10_1.xlsx", "F10"), ("mode1_10_2.xlsx", "F10")],
    "F13":    [("mode1_13_1.xlsx", "F13"), ("mode1_13_2.xlsx", "F13")],
    "Normal": [("__normal_N1__",   "Normal"), ("__normal_N2__", "Normal")],
}


# ── Structured output schema (same as Phase B, minus insight fields) ──

OUTPUT_SCHEMA = {
    "type": "json_schema",
    "name": "diagnostic_output",
    "strict": True,
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "required": ["predicted_label", "abstain", "reasoning_summary"],
        "properties": {
            "predicted_label": {"type": ["string", "null"]},
            "abstain": {"type": "boolean"},
            "reasoning_summary": {"type": "string"},
        },
    },
}


# ── Prompt template ──

PROMPT_TEMPLATE = """\
You are a diagnostic reasoning agent for the Tennessee Eastman Process. \
Use only the supplied labeled examples and the case description. \
Choose from the supplied label space. The case description contains \
observations from process sensors, not a diagnosis. \
Return strict JSON only, without markdown or extra keys.

LABEL SPACE
{label_space}

LABELED EXAMPLES (10 examples, 2 per class, rendered in the same format as the case)
{examples_block}

CASE TO DIAGNOSE
{case_text}

OUTPUT SCHEMA
{{"predicted_label":"one supplied label or null only when abstaining","abstain":false,"reasoning_summary":"one to three concise sentences"}}

If abstain is false, predicted_label must be exactly one supplied label. \
If abstain is true, predicted_label must be null. Do not output confidence.\
"""


# ── Data classes ──

@dataclass
class InferenceRecord:
    case_id: str
    true_label: str
    arm: str
    repetition: int
    predicted_label: str | None
    abstain: bool
    reasoning_summary: str
    input_tokens: int
    output_tokens: int
    latency_ms: float
    prompt_hash: str
    timestamp_utc: str
    error: str | None = None


@dataclass
class AblationConfig:
    model: str = "gpt-5.6-terra"
    repetitions: int = 3
    max_attempts: int = 3                # T7: renamed from max_retries (=2)
    reasoning_effort: str = "medium"
    output_dir: str = "ablation_results"
    dry_run: bool = False
    resume: bool = False
    max_prompt_tokens: int = 900_000     # T2: conservative limit (GPT-5.6-terra: 1.05M input)


# ── Token estimation (T2) ──

def estimate_tokens(text: str) -> int:
    """Conservative token estimate (≈ chars / 4).

    Slightly overestimates for safety.  A proper tiktoken call would be
    more accurate but adds a dependency; this is a preflight guard.
    """
    return len(text) // 4


# ── Provenance hashing (T6) ──

def compute_provenance_hash() -> str:
    """Deterministic hash of source code + config + manifest.

    If any of these files change between runs, the hash changes and resume
    is blocked to prevent mixing incompatible results.
    """
    h = hashlib.sha256()
    for name in ("ablation_representations.py", "ablation_runner.py"):
        fpath = Path(__file__).resolve().parent / name
        if fpath.exists():
            h.update(fpath.read_bytes())
    for p in (CONFIG_PATH, MANIFEST_CSV):
        if p.exists():
            h.update(p.read_bytes())
    return h.hexdigest()


def save_provenance(output_dir: Path, prov_hash: str, examples_json: str) -> None:
    """Save provenance hashes for resume verification (T6)."""
    ex_hash = hashlib.sha256(examples_json.encode("utf-8")).hexdigest()
    prov = {
        "code_config_manifest_hash": prov_hash,
        "examples_hash": ex_hash,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    with (output_dir / "provenance.json").open("w") as f:
        json.dump(prov, f, indent=2)
    log.info("Provenance saved: code/config/manifest=%s…, examples=%s…",
             prov_hash[:16], ex_hash[:16])


def verify_provenance(output_dir: Path, prov_hash: str) -> None:
    """On resume, verify provenance matches previous run (T6).

    Aborts with RuntimeError if code, config, or manifest have changed.
    """
    prov_path = output_dir / "provenance.json"
    if not prov_path.exists():
        raise RuntimeError(
            "Cannot resume: provenance.json not found in output dir. "
            "Start a fresh run (without --resume)."
        )
    with prov_path.open() as f:
        saved = json.load(f)
    saved_hash = saved.get("code_config_manifest_hash")
    if saved_hash != prov_hash:
        raise RuntimeError(
            f"Resume aborted (T6): code, config, or manifest changed since "
            f"the original run.  Saved hash: {saved_hash[:16]}…, current: "
            f"{prov_hash[:16]}….  Start a fresh run or revert changes."
        )
    log.info("T6: Provenance verified — code/config/manifest unchanged.")


# ── Output validation (T8) ──

def _validate_output(parsed: dict[str, Any]) -> dict[str, Any]:
    """Validate and normalise structured output (T8).

    Enforces:
      • Required keys present
      • abstain ↔ predicted_label consistency
      • predicted_label ∈ LABEL_SPACE or null
    """
    # Ensure required fields
    for key, default in [
        ("predicted_label", None),
        ("abstain", True),
        ("reasoning_summary", ""),
    ]:
        if key not in parsed:
            parsed[key] = default

    # Consistency: abstain ↔ predicted_label
    if parsed["abstain"]:
        if parsed["predicted_label"] is not None:
            log.warning("  T8: abstain=True but predicted_label='%s' → null",
                        parsed["predicted_label"])
            parsed["predicted_label"] = None
    else:
        if parsed["predicted_label"] is None:
            log.warning("  T8: abstain=False but predicted_label=null → abstain=True")
            parsed["abstain"] = True

    # Label validity
    pred = parsed.get("predicted_label")
    if pred is not None and pred not in LABEL_SPACE:
        log.warning("  T8: invalid label '%s' → abstention", pred)
        parsed["abstain"] = True
        parsed["predicted_label"] = None

    return parsed


# ── Baseline and example loading ──

def load_baseline(path: Path):
    """Load normal baseline and split into N1-N5 blocks.

    Also computes the Ledoit-Wolf regularised covariance inverse (T3)
    and attaches it to the baseline object for Mahalanobis computation.
    """
    normal = pd.read_excel(path)
    d = tep_features.normalize_schema(normal, source="baseline")
    blocks = []
    for i in range(5):
        start = i * 50.0
        end = (i + 1) * 50.0
        mask = (d.Time >= start) & (d.Time < end)
        blocks.append(d.loc[mask])
    baseline = tep_features.compute_baseline_stats_from_blocks(blocks)

    # T3: compute regularised covariance inverse for CGTIME Mahalanobis
    cov_inv = ablation_representations.compute_regularised_cov_inv(
        blocks, list(tep_features.XMEAS),
    )
    if cov_inv is not None:
        log.info("T3: Ledoit-Wolf regularised cov inverse computed (%d×%d)",
                 cov_inv.shape[0], cov_inv.shape[1])

    return baseline, d, cov_inv


def load_held_out_manifest(path: Path) -> list[dict[str, str]]:
    """Load and validate PBH manifest (T14: thorough validation).

    Checks: 15 rows, required fields, labels ∈ LABEL_SPACE, 3 per class,
    file existence, no overlap with example sources.
    """
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    if len(rows) != 15:
        raise RuntimeError(f"Expected 15 held-out cases, got {len(rows)}")

    # T14: required fields
    required = {"case_id", "class_offline", "filename"}
    for i, row in enumerate(rows):
        missing = required - set(row.keys())
        if missing:
            raise RuntimeError(f"Manifest row {i}: missing fields {missing}")
        if row["class_offline"] not in LABEL_SPACE:
            raise RuntimeError(
                f"Manifest row {i}: unknown label '{row['class_offline']}', "
                f"expected one of {LABEL_SPACE}"
            )

    # T14: class balance (exactly 3 per class)
    label_counts = Counter(row["class_offline"] for row in rows)
    for label in LABEL_SPACE:
        count = label_counts.get(label, 0)
        if count != 3:
            raise RuntimeError(f"Expected 3 cases for '{label}', got {count}")

    # T14: file existence
    for row in rows:
        fpath = HELDOUT / row["filename"]
        if not fpath.exists():
            raise RuntimeError(f"Held-out file not found: {fpath}")

    # T14: no overlap between example sources and held-out files
    example_files = {
        fn for fns in EXAMPLE_SOURCES.values() for fn, _ in fns
        if not fn.startswith("__")
    }
    held_out_files = {row["filename"] for row in rows}
    overlap = example_files & held_out_files
    if overlap:
        raise RuntimeError(f"T14: Example/held-out file overlap: {overlap}")

    log.info("T14: Manifest validated — 15 cases, 3/class, files present, no overlap.")
    return rows


def prepare_example_representations(
    baseline,
    normal_df: pd.DataFrame,
    config: dict[str, Any],
    ref_cov_inv=None,
) -> dict[str, list[dict[str, str]]]:
    """Generate representations for all 10 examples, each in each arm's format.

    T13: Normal examples use Time reset to 0-based with the original config
         (fault_injection_h from config, typically 10), so windows 10–50 h
         match the held-out Normal cases exactly.
    L6:  After generation, examples are shuffled with a fixed seed (42) using
         the same permutation across all arms.

    Returns: {arm_name: [{"label": ..., "text": ...}, ...]}
    """
    examples_by_arm: dict[str, list[dict[str, str]]] = {
        arm: [] for arm in ablation_representations.ARMS
    }

    for label, sources in EXAMPLE_SOURCES.items():
        for filename, true_label in sources:
            if filename.startswith("__normal_"):
                # ── T13 fix ─────────────────────────────────────────────
                # Extract 50 h block from the 500 h normal baseline.
                block_idx = 0 if "N1" in filename else 1
                start_h = block_idx * 50.0
                end_h = (block_idx + 1) * 50.0
                mask = (normal_df.Time >= start_h) & (normal_df.Time < end_h)
                case_df = normal_df.loc[mask].copy()
                # Reset Time to 0-based so that fault_injection_h (=10 from
                # config) produces windows 10–50 h, matching held-out Normal.
                case_df["Time"] = case_df["Time"].values - start_h
                # Use the original config unchanged.
                example_config = config
            else:
                case_df = pd.read_excel(CACHE / filename)
                example_config = config

            representations = ablation_representations.generate_all_representations(
                case_df, baseline, example_config, ref_cov_inv=ref_cov_inv,
            )
            for arm_name, text in representations.items():
                examples_by_arm[arm_name].append({
                    "label": true_label,
                    "text": text,
                })

    # ── L6 fix ──────────────────────────────────────────────────────────
    # Deterministic shuffle — same permutation for all arms so the label
    # sequence seen by the model is identical across representations.
    indices = list(range(10))
    random.Random(42).shuffle(indices)
    for arm_name in examples_by_arm:
        examples_by_arm[arm_name] = [examples_by_arm[arm_name][i] for i in indices]
    log.info("L6: Examples shuffled with seed=42 — order: %s",
             [examples_by_arm["V2_TEXT"][i]["label"] for i in range(10)])

    return examples_by_arm


def format_examples_block(examples: list[dict[str, str]]) -> str:
    """Format 10 examples as a prompt block."""
    parts = []
    for i, ex in enumerate(examples, 1):
        parts.append(f"--- Example {i} (Label: {ex['label']}) ---\n{ex['text']}")
    return "\n\n".join(parts)


def build_prompt(
    arm_name: str,
    case_text: str,
    examples: list[dict[str, str]],
) -> str:
    """Build the complete diagnostic prompt for a given arm."""
    return PROMPT_TEMPLATE.format(
        label_space=json.dumps(LABEL_SPACE),
        examples_block=format_examples_block(examples),
        case_text=case_text,
    )


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ── Inference engine ──

def call_openai(
    prompt: str,
    config: AblationConfig,
) -> dict[str, Any]:
    """Call GPT-5.6-terra via OpenAI Responses API with structured output.

    T8: checks for refusal, empty output, and validates parsed fields.
    """
    import openai

    client = openai.OpenAI()

    t0 = time.monotonic()
    response = client.responses.create(
        model=config.model,
        instructions="",
        input=[{"role": "user", "content": prompt}],
        # Responses API format: unlike Chat Completions, the JSON-schema
        # fields are direct children of text.format (no json_schema wrapper).
        text={"format": OUTPUT_SCHEMA},
        reasoning={"effort": config.reasoning_effort},
    )
    latency_ms = (time.monotonic() - t0) * 1000

    # T8: Check for model refusal
    if hasattr(response, "refusal") and response.refusal:
        return {
            "parsed": _validate_output({
                "predicted_label": None,
                "abstain": True,
                "reasoning_summary": f"Model refused: {response.refusal}",
            }),
            "input_tokens": 0,
            "output_tokens": 0,
            "latency_ms": latency_ms,
            "error": f"refusal: {response.refusal}",
        }

    # Extract output text from response
    output_text = getattr(response, "output_text", "") or ""
    if not output_text:
        for item in getattr(response, "output", []):
            if hasattr(item, "text"):
                output_text = item.text
                break
            if hasattr(item, "content"):
                for block in item.content:
                    if hasattr(block, "text"):
                        output_text = block.text
                        break
                if output_text:
                    break

    # T8: Empty output guard
    if not output_text.strip():
        usage = getattr(response, "usage", None)
        return {
            "parsed": _validate_output({
                "predicted_label": None,
                "abstain": True,
                "reasoning_summary": "Empty output from model",
            }),
            "input_tokens": getattr(usage, "input_tokens", 0) if usage else 0,
            "output_tokens": getattr(usage, "output_tokens", 0) if usage else 0,
            "latency_ms": latency_ms,
            "error": "empty_output",
        }

    # Parse structured output
    try:
        parsed = json.loads(output_text)
    except json.JSONDecodeError:
        parsed = {
            "predicted_label": None,
            "abstain": True,
            "reasoning_summary": f"JSON parse error: {output_text[:200]}",
        }

    # T8: Validate consistency
    parsed = _validate_output(parsed)

    # Token accounting
    usage = getattr(response, "usage", None)
    input_tokens = getattr(usage, "input_tokens", 0) if usage else 0
    output_tokens = getattr(usage, "output_tokens", 0) if usage else 0

    return {
        "parsed": parsed,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "latency_ms": latency_ms,
    }


def dry_run_inference(prompt: str) -> dict[str, Any]:
    """Simulated inference for dry runs (no API calls)."""
    label = random.choice(LABEL_SPACE)
    parsed = _validate_output({
        "predicted_label": label,
        "abstain": False,
        "reasoning_summary": f"[DRY RUN] Random prediction: {label}",
    })
    return {
        "parsed": parsed,
        "input_tokens": len(prompt.split()),
        "output_tokens": 50,
        "latency_ms": 0.0,
    }


# ── Main execution logic ──

def build_inference_schedule(
    manifest_rows: list[dict[str, str]],
    config: AblationConfig,
) -> list[dict[str, Any]]:
    """Build the complete list of (case, arm, rep) tuples."""
    schedule = []
    for row in manifest_rows:
        case_id = row["case_id"]
        true_label = row["class_offline"]
        for arm_name in ablation_representations.ARMS:
            for rep in range(1, config.repetitions + 1):
                schedule.append({
                    "case_id": case_id,
                    "true_label": true_label,
                    "arm": arm_name,
                    "repetition": rep,
                    "filename": row["filename"],
                })
    return schedule


def load_completed(output_dir: Path) -> set[tuple[str, str, int]]:
    """Load already-completed (case_id, arm, rep) from results."""
    results_path = output_dir / "inference_results.jsonl"
    completed = set()
    if results_path.exists():
        with results_path.open("r") as f:
            for line in f:
                rec = json.loads(line)
                completed.add((rec["case_id"], rec["arm"], rec["repetition"]))
    return completed


def run_ablation(config: AblationConfig) -> None:
    """Execute the full ablation experiment."""
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save experiment configuration
    with (output_dir / "ablation_config.json").open("w") as f:
        json.dump(asdict(config), f, indent=2)

    # ── T6: Provenance hash ─────────────────────────────────────────────
    prov_hash = compute_provenance_hash()

    # ── Resume support ──────────────────────────────────────────────────
    completed = set()
    if config.resume:
        verify_provenance(output_dir, prov_hash)
        completed = load_completed(output_dir)
        log.info("Resuming: %d inferences already completed", len(completed))

    # ── Load data ───────────────────────────────────────────────────────
    log.info("Loading baseline statistics from %s", BASELINE_PATH)
    baseline, normal_df, ref_cov_inv = load_baseline(BASELINE_PATH)

    log.info("Loading verbalizer config from %s", CONFIG_PATH)
    v2_config = tep_verbalize_v2.load_config(str(CONFIG_PATH))

    log.info("Loading and validating held-out manifest from %s", MANIFEST_CSV)
    manifest_rows = load_held_out_manifest(MANIFEST_CSV)

    # ── Prepare examples (T13 + L6) ────────────────────────────────────
    log.info("Preparing example representations (10 examples × 4 arms)...")
    examples_by_arm = prepare_example_representations(
        baseline, normal_df, v2_config, ref_cov_inv=ref_cov_inv,
    )

    # Save examples for reproducibility
    examples_json = json.dumps(examples_by_arm, indent=2, ensure_ascii=False)
    examples_path = output_dir / "example_representations.json"
    with examples_path.open("w") as f:
        f.write(examples_json)
    log.info("Examples saved to %s", examples_path)

    # ── T6: Save provenance (first run only) ────────────────────────────
    if not config.resume:
        save_provenance(output_dir, prov_hash, examples_json)

    # ── Build inference schedule ────────────────────────────────────────
    schedule = build_inference_schedule(manifest_rows, config)
    log.info("Inference schedule: %d calls (%d cases × %d arms × %d reps)",
             len(schedule), len(manifest_rows),
             len(ablation_representations.ARMS), config.repetitions)

    # ── Pre-generate all case representations ───────────────────────────
    log.info("Pre-generating case representations...")
    case_representations: dict[str, dict[str, str]] = {}
    for row in manifest_rows:
        case_id = row["case_id"]
        filename = row["filename"]
        source = HELDOUT / filename
        case_df = pd.read_excel(source)

        # T14: verify XMEAS columns after normalisation
        d_check = tep_features.normalize_schema(case_df, source=f"held-out {case_id}")
        missing_cols = [c for c in tep_features.XMEAS if c not in d_check.columns]
        if missing_cols:
            raise RuntimeError(
                f"T14: {case_id} ({filename}) missing XMEAS columns: "
                f"{missing_cols[:5]}{'…' if len(missing_cols) > 5 else ''}"
            )

        reps = ablation_representations.generate_all_representations(
            case_df, baseline, v2_config, ref_cov_inv=ref_cov_inv,
        )
        case_representations[case_id] = reps
        log.info("  %s (%s): 4 representations generated", case_id, row["class_offline"])

    # Save representations
    repr_path = output_dir / "case_representations.json"
    with repr_path.open("w") as f:
        json.dump(case_representations, f, indent=2, ensure_ascii=False)
    log.info("Case representations saved to %s", repr_path)

    # ── T2: Token budget summary & pre-check ────────────────────────────
    token_summary: dict[str, dict[str, Any]] = {}
    budget_violations: list[tuple[str, int]] = []
    sample_cid = list(case_representations.keys())[0]

    for arm_name in ablation_representations.ARMS:
        chars = [len(case_representations[cid][arm_name]) for cid in case_representations]
        words = [len(case_representations[cid][arm_name].split()) for cid in case_representations]

        # Estimate full prompt tokens for a representative case
        sample_prompt = build_prompt(
            arm_name,
            case_representations[sample_cid][arm_name],
            examples_by_arm[arm_name],
        )
        est_tokens = estimate_tokens(sample_prompt)

        token_summary[arm_name] = {
            "mean_chars": round(sum(chars) / len(chars)),
            "max_chars": max(chars),
            "mean_words": round(sum(words) / len(words)),
            "est_prompt_tokens": est_tokens,
        }
        if est_tokens > config.max_prompt_tokens:
            budget_violations.append((arm_name, est_tokens))

    with (output_dir / "token_summary.json").open("w") as f:
        json.dump(token_summary, f, indent=2)

    log.info("T2 token estimates: %s",
             {k: f"~{v['est_prompt_tokens']:,} tok" for k, v in token_summary.items()})

    if budget_violations:
        for arm, toks in budget_violations:
            log.error("T2: arm %s exceeds token budget: ~%d > %d",
                      arm, toks, config.max_prompt_tokens)
        raise RuntimeError(
            f"T2: {len(budget_violations)} arm(s) exceed "
            f"max_prompt_tokens={config.max_prompt_tokens:,}. "
            "Increase --max-prompt-tokens or reduce representation size."
        )

    # ── Run inference ───────────────────────────────────────────────────
    results_path = output_dir / "inference_results.jsonl"
    mode = "a" if config.resume else "w"
    n_total = len(schedule)
    n_done = len(completed)

    with results_path.open(mode) as results_file:
        for idx, item in enumerate(schedule, 1):
            case_id = item["case_id"]
            arm_name = item["arm"]
            rep = item["repetition"]

            key = (case_id, arm_name, rep)
            if key in completed:
                continue

            case_text = case_representations[case_id][arm_name]
            examples = examples_by_arm[arm_name]
            prompt = build_prompt(arm_name, case_text, examples)
            prompt_hash = sha256_text(prompt)

            # T2: per-inference token pre-flight
            est = estimate_tokens(prompt)
            if est > config.max_prompt_tokens:
                log.error("T2: %s|%s|rep%d ~%d tokens > limit %d → skipping",
                          case_id, arm_name, rep, est, config.max_prompt_tokens)
                result = {
                    "parsed": _validate_output({
                        "predicted_label": None,
                        "abstain": True,
                        "reasoning_summary": (
                            f"Skipped: prompt ~{est:,} tokens exceeds limit "
                            f"{config.max_prompt_tokens:,}"
                        ),
                    }),
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "latency_ms": 0.0,
                }
                error = f"token_budget_exceeded: ~{est}"
            else:
                n_done += 1
                log.info("[%d/%d] %s | %s | rep %d | ~%d tokens",
                         n_done, n_total, case_id, arm_name, rep, est)

                error = None
                # T7: max_attempts loop (renamed from max_retries)
                for attempt in range(1, config.max_attempts + 1):
                    try:
                        if config.dry_run:
                            result = dry_run_inference(prompt)
                        else:
                            result = call_openai(prompt, config)
                        break
                    except Exception as e:
                        error = f"attempt {attempt}/{config.max_attempts}: {e}"
                        log.warning("  %s", error)
                        if attempt < config.max_attempts:
                            time.sleep(2 ** attempt)
                else:
                    # All attempts exhausted
                    result = {
                        "parsed": _validate_output({
                            "predicted_label": None,
                            "abstain": True,
                            "reasoning_summary": (
                                f"All {config.max_attempts} attempts failed: {error}"
                            ),
                        }),
                        "input_tokens": 0,
                        "output_tokens": 0,
                        "latency_ms": 0.0,
                    }

            parsed = result["parsed"]

            record = InferenceRecord(
                case_id=case_id,
                true_label=item["true_label"],
                arm=arm_name,
                repetition=rep,
                predicted_label=parsed.get("predicted_label"),
                abstain=parsed.get("abstain", False),
                reasoning_summary=parsed.get("reasoning_summary", ""),
                input_tokens=result["input_tokens"],
                output_tokens=result["output_tokens"],
                latency_ms=result["latency_ms"],
                prompt_hash=prompt_hash,
                timestamp_utc=datetime.now(timezone.utc).isoformat(),
                error=error,
            )

            results_file.write(json.dumps(asdict(record), ensure_ascii=False) + "\n")
            results_file.flush()

    log.info("Inference complete. Results: %s", results_path)
    log.info("Next: python ablation_evaluate.py %s", config.output_dir)


def main():
    parser = argparse.ArgumentParser(
        description="Run the 4-arm ablation experiment on TEP held-out cases."
    )
    parser.add_argument(
        "--model", default="gpt-5.6-terra",
        help="OpenAI model name (default: gpt-5.6-terra)",
    )
    parser.add_argument(
        "--repetitions", type=int, default=3,
        help="Repetitions per arm × case (default: 3)",
    )
    parser.add_argument(
        "--output-dir", default="ablation_results",
        help="Output directory for results (default: ablation_results)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Generate random predictions without calling the LLM",
    )
    parser.add_argument(
        "--resume", action="store_true",
        help="Resume from previously completed inferences",
    )
    parser.add_argument(
        "--project-root", default=".",
        help="Path to fot-tep project root",
    )
    parser.add_argument(
        "--reasoning-effort", default="medium",
        choices=["low", "medium", "high"],
        help="Reasoning effort for GPT-5.6-terra (default: medium)",
    )
    # T7: renamed from --max-retries
    parser.add_argument(
        "--max-attempts", type=int, default=3,
        help="Max API call attempts per inference (default: 3)",
    )
    # T2: token budget
    parser.add_argument(
        "--max-prompt-tokens", type=int, default=900_000,
        help="Abort if estimated prompt tokens exceed this limit (default: 900000)",
    )
    args = parser.parse_args()

    # Set project root paths
    global ROOT, CODE, CACHE, HELDOUT, MANIFEST_CSV, BASELINE_PATH, CONFIG_PATH
    ROOT = Path(args.project_root)
    CODE = ROOT / "code"
    CACHE = CODE / "tep_cache"
    HELDOUT = ROOT / "tep_heldout/mode1"
    MANIFEST_CSV = ROOT / "phase_b/heldout/phase_b_heldout_manifest.csv"
    BASELINE_PATH = CACHE / "mode1_normal_500.xlsx"
    CONFIG_PATH = CODE / "verbalizer_config_v2.json"

    # Validate paths
    for path, label in [
        (BASELINE_PATH, "baseline"),
        (MANIFEST_CSV, "heldout manifest"),
        (CONFIG_PATH, "verbalizer config"),
    ]:
        if not path.exists():
            log.error("Missing %s: %s", label, path)
            sys.exit(1)

    # Initialize imports now that project root is known
    _init_imports(ROOT)

    config = AblationConfig(
        model=args.model,
        repetitions=args.repetitions,
        max_attempts=args.max_attempts,
        output_dir=args.output_dir,
        dry_run=args.dry_run,
        resume=args.resume,
        reasoning_effort=args.reasoning_effort,
        max_prompt_tokens=args.max_prompt_tokens,
    )

    log.info("=" * 70)
    log.info("ABLATION EXPERIMENT: 4-arm TS→text representation comparison")
    log.info("=" * 70)
    log.info("Model: %s", config.model)
    log.info("Arms: %s", list(ablation_representations.ARMS.keys()))
    log.info("Cases: 15 (PBH-001..PBH-015)")
    log.info("Repetitions: %d", config.repetitions)
    log.info("Total inferences: %d", 4 * 15 * config.repetitions)
    log.info("Max attempts: %d", config.max_attempts)
    log.info("Max prompt tokens: %d", config.max_prompt_tokens)
    log.info("Dry run: %s", config.dry_run)
    log.info("Output: %s", config.output_dir)
    log.info("=" * 70)

    run_ablation(config)


if __name__ == "__main__":
    main()
