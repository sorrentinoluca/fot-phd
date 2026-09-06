"""Condition C offline evaluator — metrics, paired delta C−B, bootstrap, firewall.

Evaluates CAggregatePrediction records against evaluator-side pseudolabel
truth.  Condition C uses a single centralized agent ("central") so there
are no per-agent scopes — every fault case is class-covered.

The paired delta Δ_{C-B} follows R5 §5.2:
  Δ = (1/12) Σ_{i=1}^{12} [1(C_i=y_i) - (1/|U_i|) Σ_{a∈U_i} 1(B_{ia}=y_i)]

where U_i is the set of 3 agents for whom fault case i is unseen
(local_fault_label ≠ y_i).

Bootstrap CI (R5 §5.3): 12 clusters, 4 fault strata × 3, paired
resampling, 10 000 draws, seed 20260906, 95 % percentile.

Evaluator-side firewall:
  • Reads pseudolabel truth from phase_b/heldout/phase_b_heldout_manifest.csv
    + phase_b/config/evaluator_side/pseudolabel_mapping.json.
  • Never writes to or modifies any inference artifact.
  • The runner never sees pseudolabel_mapping.json.

No LLM call is made by this module.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from icl.evaluation.aggregation_c import (
    CAggregatePrediction,
    aggregate_c_records,
)
from icl.runner.records_c import CRunRecord, LABEL_SPACE as _RECORD_LABEL_SPACE


ROOT = Path(__file__).resolve().parents[2]

HELDOUT_MANIFEST_PATH = (
    ROOT / "phase_b" / "heldout" / "phase_b_heldout_manifest.csv"
)
MAPPING_PATH = (
    ROOT / "phase_b" / "config" / "evaluator_side" / "pseudolabel_mapping.json"
)
PROTOCOL_CONFIG_PATH = ROOT / "phase_b" / "config" / "protocol_config.json"
PHASE_B_AGGREGATE_PATH = (
    ROOT / "phase_b" / "final_evaluation" / "inference"
    / "aggregate_records.jsonl"
)
INFERENCE_HASH_MANIFEST_PATH = (
    ROOT / "phase_b" / "final_evaluation" / "inference"
    / "inference_output_hash_manifest.json"
)
EVALUATOR_FREEZE_MANIFEST_PATH = (
    ROOT / "icl" / "full_evaluation" / "freeze_manifest_evaluator.json"
)
C_RECORDS_PATH = ROOT / "icl" / "inference" / "c_records.jsonl"
C_SCHEDULE_PATH = ROOT / "icl" / "full_evaluation" / "c_schedule.json"
C_PREDICTIONS_MANIFEST_PATH = (
    ROOT / "icl" / "full_evaluation" / "c_predictions_manifest.json"
)

ABSTAIN_TOKEN = "__ABSTAIN__"


# ------------------------------------------------------------------
# Evaluator-side truth loader (firewall: evaluator side only)
# ------------------------------------------------------------------

def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_case_truth(
    *,
    heldout_manifest_path: Path = HELDOUT_MANIFEST_PATH,
    mapping_path: Path = MAPPING_PATH,
) -> tuple[dict[str, str], dict[str, Any]]:
    """Load evaluator-side ground truth for the 15 held-out cases.

    Returns ``(case_truth, integrity_info)`` where *case_truth* maps
    ``physical_case_id → opaque pseudolabel``.

    The truth is derived by joining:
      1. The heldout manifest CSV (case_id + class_offline)
      2. The pseudolabel mapping     (real_class → opaque label)

    This function lives on the evaluator side of the firewall: the
    runner never calls it and never sees pseudolabel_mapping.json.
    """
    mapping = json.loads(mapping_path.read_text(encoding="utf-8"))
    real_to_opaque: dict[str, str] = mapping["real_to_opaque"]
    normal_label: str = mapping["normal_label"]

    with heldout_manifest_path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    if len(rows) != 15:
        raise ValueError(
            f"expected 15 held-out cases, got {len(rows)}"
        )

    case_truth: dict[str, str] = {}
    real_class_counts: Counter[str] = Counter()

    for row in rows:
        case_id = row["case_id"]
        real_class = row["class_offline"]
        real_class_counts[real_class] += 1

        if real_class == "Normal":
            pseudolabel = normal_label
        elif real_class in real_to_opaque:
            pseudolabel = real_to_opaque[real_class]
        else:
            raise RuntimeError(
                f"unmapped class_offline {real_class!r} for {case_id}"
            )

        if case_id in case_truth:
            raise RuntimeError(f"duplicate case_id in manifest: {case_id}")
        case_truth[case_id] = pseudolabel

    # Expect 5 classes × 3 runs each.
    if set(real_class_counts.values()) != {3} or len(real_class_counts) != 5:
        raise ValueError(
            "held-out manifest must contain three runs for each of five classes"
        )

    return case_truth, {
        "physical_cases_mapped": len(case_truth),
        "unique_mapping": True,
        "fault_pseudoclass_count": 4,
        "runs_per_class": 3,
        "heldout_manifest_sha256": _sha256_file(heldout_manifest_path),
        "pseudolabel_mapping_sha256": _sha256_file(mapping_path),
    }


# ------------------------------------------------------------------
# Agent config loader (evaluator side)
# ------------------------------------------------------------------

def load_agents_config(
    config_path: Path = PROTOCOL_CONFIG_PATH,
) -> dict[str, str]:
    """Return ``{agent_id: local_fault_label}`` from protocol_config.json."""
    config = json.loads(config_path.read_text(encoding="utf-8"))
    return {
        agent_id: agent["local_fault_label"]
        for agent_id, agent in config["agents"].items()
    }


def unseen_agents(
    true_label: str,
    agents_config: dict[str, str],
) -> list[str]:
    """Return sorted agent_ids whose local_fault_label ≠ *true_label*.

    For fault cases this gives the 3 agents for whom the case is unseen
    in Phase B.  Normal cases are not used in the paired delta.
    """
    return sorted(
        aid for aid, local in agents_config.items()
        if local != true_label
    )


# ------------------------------------------------------------------
# Correctness
# ------------------------------------------------------------------

def is_correct(
    prediction: CAggregatePrediction | dict[str, Any],
    true_label: str,
) -> bool:
    """Return True iff the prediction matches the true label (abstain → False)."""
    parsed = (
        prediction.parsed_output
        if isinstance(prediction, CAggregatePrediction)
        else prediction["parsed_output"]
    )
    return bool(
        not parsed["abstain"] and parsed["predicted_label"] == true_label
    )


# ------------------------------------------------------------------
# Core metrics  (R5 §3.8)
# ------------------------------------------------------------------

def _metric(
    rows: list[tuple[CAggregatePrediction, str]],
) -> dict[str, float | int | None]:
    """Accuracy / abstention for a set of (prediction, truth) pairs."""
    n = len(rows)
    correct = sum(is_correct(pred, truth) for pred, truth in rows)
    abstained = sum(
        bool(pred.parsed_output["abstain"]) for pred, _ in rows
    )
    return {
        "n": n,
        "correct": correct,
        "accuracy": correct / n if n else None,
        "abstentions": abstained,
        "abstention_rate": abstained / n if n else None,
    }


def condition_c_metrics(
    aggregates: list[CAggregatePrediction],
    case_truth: dict[str, str],
    *,
    label_space: set[str] | None = None,
    normal_label: str = "Normal",
) -> dict[str, Any]:
    """Compute accuracy_C_fault (n=12), accuracy_C_normal (n=3), overall.

    Also produces per-class breakdown and confusion matrix.
    """
    if label_space is None:
        label_space = set(_RECORD_LABEL_SPACE)

    classified = [
        (agg, case_truth[agg.physical_case_id]) for agg in aggregates
    ]

    overall = _metric(classified)

    # Fault vs Normal split (R5 §3.8).
    fault_rows = [(p, t) for p, t in classified if t != normal_label]
    normal_rows = [(p, t) for p, t in classified if t == normal_label]

    accuracy_C_fault = _metric(fault_rows)
    accuracy_C_normal = _metric(normal_rows)

    # Per-class breakdown.
    per_class: dict[str, dict[str, float | int | None]] = {}
    for label in sorted(label_space):
        per_class[label] = _metric(
            [(pred, truth) for pred, truth in classified if truth == label]
        )

    # Confusion matrix.
    prediction_columns = sorted(label_space) + [ABSTAIN_TOKEN]
    confusion: dict[str, dict[str, int]] = {
        truth: {pred_col: 0 for pred_col in prediction_columns}
        for truth in sorted(label_space)
    }
    for pred, truth in classified:
        parsed = pred.parsed_output
        predicted = (
            ABSTAIN_TOKEN if parsed["abstain"] else parsed["predicted_label"]
        )
        confusion[truth][predicted] += 1

    return {
        "overall": overall,
        "accuracy_C_fault": accuracy_C_fault,
        "accuracy_C_normal": accuracy_C_normal,
        "per_class": per_class,
        "confusion_matrix": confusion,
    }


# ------------------------------------------------------------------
# Phase B aggregates loader
# ------------------------------------------------------------------

def load_phase_b_aggregates(
    path: Path = PHASE_B_AGGREGATE_PATH,
) -> list[dict[str, Any]]:
    """Load Phase B frozen aggregate records (read-only, evaluator side)."""
    lines = path.read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines if line.strip()]


# ------------------------------------------------------------------
# Paired delta C − B  (R5 §5.2)
# ------------------------------------------------------------------

def build_paired_rows(
    c_aggregates: list[CAggregatePrediction],
    b_records: list[dict[str, Any]],
    case_truth: dict[str, str],
    agents_config: dict[str, str],
    *,
    normal_label: str = "Normal",
) -> list[dict[str, Any]]:
    """Build paired rows for the 12 fault physical cases.

    Each row contains:
      - physical_case_id
      - true_pseudolabel
      - c_correct: int (0 or 1)
      - b_unseen_mean: float — mean correctness of the |U_i| unseen B agents
      - paired_delta_i: float — c_correct − b_unseen_mean
    """
    # Index C aggregates by physical_case_id.
    c_by_case: dict[str, CAggregatePrediction] = {
        agg.physical_case_id: agg for agg in c_aggregates
    }

    # Index B condition==B records by (physical_case_id, agent_id).
    b_by_case_agent: dict[tuple[str, str], dict[str, Any]] = {}
    for rec in b_records:
        if rec["condition"] != "B":
            continue
        key = (rec["physical_case_id"], rec["agent_id"])
        b_by_case_agent[key] = rec

    rows: list[dict[str, Any]] = []

    for case_id in sorted(case_truth):
        truth = case_truth[case_id]
        if truth == normal_label:
            continue  # Only fault cases enter the delta.

        if case_id not in c_by_case:
            raise ValueError(f"missing C aggregate for fault case {case_id}")

        c_correct = int(is_correct(c_by_case[case_id], truth))

        u_i = unseen_agents(truth, agents_config)
        if len(u_i) != 3:
            raise ValueError(
                f"expected 3 unseen agents for {case_id} "
                f"(truth={truth}), got {len(u_i)}"
            )

        b_correct_sum = 0
        for agent_id in u_i:
            key = (case_id, agent_id)
            if key not in b_by_case_agent:
                raise ValueError(
                    f"missing B aggregate for {case_id}, {agent_id}"
                )
            b_correct_sum += int(is_correct(b_by_case_agent[key], truth))

        b_unseen_mean = b_correct_sum / len(u_i)

        rows.append({
            "physical_case_id": case_id,
            "true_pseudolabel": truth,
            "c_correct": c_correct,
            "b_unseen_mean": b_unseen_mean,
            "paired_delta_i": c_correct - b_unseen_mean,
        })

    if len(rows) != 12:
        raise ValueError(f"expected 12 fault paired rows, got {len(rows)}")

    return rows


def delta_c_minus_b(
    paired_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    """Compute the paired delta Δ_{C-B} per R5 §5.2.

    Returns a dict with the point estimate and supporting detail.
    """
    if len(paired_rows) != 12:
        raise ValueError(f"expected 12 paired rows, got {len(paired_rows)}")

    delta = sum(r["paired_delta_i"] for r in paired_rows) / 12.0
    c_acc_fault = sum(r["c_correct"] for r in paired_rows) / 12.0
    b_acc_fault = sum(r["b_unseen_mean"] for r in paired_rows) / 12.0

    return {
        "estimand": "paired_delta_C_minus_B_fault_only",
        "formula": "R5_§5.2",
        "n_fault_cases": 12,
        "delta_C_minus_B": delta,
        "accuracy_C_fault": c_acc_fault,
        "accuracy_B_unseen_fault": b_acc_fault,
        "per_case": paired_rows,
    }


# ------------------------------------------------------------------
# Bootstrap CI for paired delta  (R5 §5.3)
# ------------------------------------------------------------------

def bootstrap_paired_delta(
    paired_rows: list[dict[str, Any]],
    *,
    iterations: int = 10000,
    seed: int = 20260906,
    confidence_level: float = 0.95,
) -> dict[str, Any]:
    """Stratified cluster bootstrap for the paired Δ_{C-B}.

    Resamples 12 physical-case clusters stratified by true pseudolabel
    (4 fault strata × 3 clusters each).  Each draw resamples clusters
    within each stratum with replacement, then computes the paired delta
    over the resampled set.
    """
    import numpy as np

    if not paired_rows:
        raise ValueError("no paired rows for bootstrap")
    if len(paired_rows) != 12:
        raise ValueError(f"expected 12 paired rows, got {len(paired_rows)}")
    if not 0.0 < confidence_level < 1.0:
        raise ValueError("confidence_level must be in (0, 1)")
    if iterations <= 0:
        raise ValueError("iterations must be positive")

    # Stratify by true pseudolabel.
    strata: dict[str, list[str]] = defaultdict(list)
    by_case: dict[str, dict[str, Any]] = {}
    for row in paired_rows:
        cid = row["physical_case_id"]
        strata[row["true_pseudolabel"]].append(cid)
        by_case[cid] = row

    # Validate: 4 fault strata × 3 clusters = 12.
    clusters_per_label = {
        label: len(cases) for label, cases in sorted(strata.items())
    }
    if set(clusters_per_label.values()) != {3} or len(clusters_per_label) != 4:
        raise ValueError(
            f"expected 4 fault strata × 3 clusters, got {clusters_per_label}"
        )

    rng = np.random.default_rng(seed)
    draws = np.empty(iterations, dtype=float)

    for i in range(iterations):
        sampled: list[str] = []
        for label in sorted(strata):
            cluster_ids = sorted(strata[label])
            sampled.extend(
                rng.choice(cluster_ids, size=len(cluster_ids), replace=True)
                .tolist()
            )
        delta_sum = sum(by_case[cid]["paired_delta_i"] for cid in sampled)
        draws[i] = delta_sum / len(sampled)

    alpha = 1.0 - confidence_level
    point_estimate = sum(r["paired_delta_i"] for r in paired_rows) / len(paired_rows)

    return {
        "method": (
            "physical_case_id cluster bootstrap "
            "stratified by true pseudolabel (fault only)"
        ),
        "statistic": "paired_delta_C_minus_B",
        "point_estimate": point_estimate,
        "confidence_level": confidence_level,
        "ci_lower": float(np.quantile(draws, alpha / 2.0)),
        "ci_upper": float(np.quantile(draws, 1.0 - alpha / 2.0)),
        "iterations": iterations,
        "seed": seed,
        "n_physical_clusters": 12,
        "clusters_per_pseudolabel": clusters_per_label,
        "independence_claim": False,
    }


# ------------------------------------------------------------------
# Evaluator-side freeze verification
# ------------------------------------------------------------------

def verify_evaluator_freeze(
    *,
    manifest_path: Path = EVALUATOR_FREEZE_MANIFEST_PATH,
    heldout_manifest_path: Path = HELDOUT_MANIFEST_PATH,
    mapping_path: Path = MAPPING_PATH,
    b_aggregate_path: Path = PHASE_B_AGGREGATE_PATH,
    hash_manifest_path: Path = INFERENCE_HASH_MANIFEST_PATH,
    root: Path = ROOT,
) -> dict[str, Any]:
    """Verify evaluator-side artifact integrity.

    When *manifest_path* exists, verifies all artifact hashes listed in
    ``freeze_manifest_evaluator.json`` against files on disk — the
    evaluator-side counterpart of the runner's inference freeze guard.

    Always checks:
      1. pseudolabel_mapping.json exists and is well-formed.
      2. heldout manifest CSV exists and has 15 rows.
      3. Phase B aggregate records exist.
      4. If inference_output_hash_manifest.json exists, verify
         aggregate_records.jsonl hash against it.

    Does NOT access the inference-side manifest.
    """
    integrity: dict[str, Any] = {}

    # ── Manifest-based hash verification (mandatory / fail-closed) ──
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for rel_path, expected in manifest["artifact_hashes"].items():
        actual = _sha256_file(root / rel_path)
        if actual != expected:
            raise RuntimeError(
                f"evaluator freeze guard: {rel_path} hash mismatch "
                f"(expected {expected[:16]}…, got {actual[:16]}…)"
            )
    integrity["evaluator_manifest_verified"] = True

    # ── Structural checks (always run) ──

    # Pseudolabel mapping.
    if not mapping_path.exists():
        raise FileNotFoundError(
            f"pseudolabel mapping not found: {mapping_path}"
        )
    mapping = json.loads(mapping_path.read_text(encoding="utf-8"))
    if "real_to_opaque" not in mapping or "normal_label" not in mapping:
        raise ValueError("pseudolabel_mapping.json missing required keys")
    integrity["pseudolabel_mapping_sha256"] = _sha256_file(mapping_path)

    # Heldout manifest.
    if not heldout_manifest_path.exists():
        raise FileNotFoundError(
            f"heldout manifest not found: {heldout_manifest_path}"
        )
    integrity["heldout_manifest_sha256"] = _sha256_file(heldout_manifest_path)

    # Phase B aggregates.
    if not b_aggregate_path.exists():
        raise FileNotFoundError(
            f"Phase B aggregates not found: {b_aggregate_path}"
        )
    integrity["b_aggregate_sha256"] = _sha256_file(b_aggregate_path)

    # Verify B aggregate hash against inference output hash manifest.
    if hash_manifest_path.exists():
        exp1_manifest = json.loads(
            hash_manifest_path.read_text(encoding="utf-8")
        )
        artifacts = exp1_manifest.get("artifacts", {})
        b_agg_rel = str(b_aggregate_path.relative_to(root))
        if b_agg_rel in artifacts:
            expected = artifacts[b_agg_rel]
            actual = integrity["b_aggregate_sha256"]
            if actual != expected:
                raise RuntimeError(
                    f"Phase B aggregate hash mismatch: "
                    f"expected {expected[:16]}…, got {actual[:16]}…"
                )
            integrity["b_aggregate_hash_verified"] = True

    return integrity


# ------------------------------------------------------------------
# Predictions integrity barrier (fail-closed)
# ------------------------------------------------------------------

def verify_c_predictions_freeze(
    *,
    c_records_path: Path | None = None,
    manifest_path: Path | None = None,
    schedule_path: Path | None = None,
) -> dict[str, Any]:
    """Verify c_records.jsonl integrity against its predictions manifest.

    Fail-closed: raises on missing files, hash mismatch, count mismatch,
    invalid records, schedule reference mismatch, or schedule cross-check
    failure.

    The predictions manifest must contain:
      - c_records_sha256: SHA-256 of c_records.jsonl
      - record_count: expected number of records
      - schedule_reference: {path, sha256} tying predictions to the schedule

    Returns integrity dict on success.
    """
    rec_path = c_records_path if c_records_path is not None else C_RECORDS_PATH
    man_path = manifest_path if manifest_path is not None else C_PREDICTIONS_MANIFEST_PATH
    sched_path = schedule_path if schedule_path is not None else C_SCHEDULE_PATH

    # All must exist (fail-closed).
    manifest = json.loads(man_path.read_text(encoding="utf-8"))

    # --- Required manifest keys ---
    _REQUIRED_KEYS = {"c_records_sha256", "record_count", "schedule_reference"}
    missing_keys = _REQUIRED_KEYS - set(manifest)
    if missing_keys:
        raise RuntimeError(
            f"c_predictions_manifest.json missing required keys: "
            f"{sorted(missing_keys)}"
        )

    # --- Hash verification ---
    expected = manifest["c_records_sha256"]
    actual = _sha256_file(rec_path)
    if actual != expected:
        raise RuntimeError(
            f"c_records.jsonl hash mismatch: "
            f"expected {expected[:16]}…, got {actual[:16]}…"
        )

    # --- Record count ---
    expected_count: int = manifest["record_count"]
    raw_text = rec_path.read_text(encoding="utf-8")
    lines = [ln for ln in raw_text.strip().split("\n") if ln.strip()]
    if len(lines) != expected_count:
        raise RuntimeError(
            f"c_records.jsonl record count mismatch: "
            f"expected {expected_count}, got {len(lines)}"
        )

    # --- Schedule reference verification ---
    sched_ref = manifest["schedule_reference"]
    if not isinstance(sched_ref, dict) or "sha256" not in sched_ref:
        raise RuntimeError(
            "schedule_reference must be a dict with at least 'sha256'"
        )
    actual_sched_sha = _sha256_file(sched_path)
    if actual_sched_sha != sched_ref["sha256"]:
        raise RuntimeError(
            f"schedule SHA-256 mismatch: manifest says "
            f"{sched_ref['sha256'][:16]}…, actual {actual_sched_sha[:16]}…"
        )

    # Load schedule for cross-check.
    schedule: list[dict[str, Any]] = json.loads(
        sched_path.read_text(encoding="utf-8")
    )

    # R7 P1-3: record count must equal schedule length (45 for full
    # evaluation).  The pilot subset (15) is not valid for evaluation.
    if expected_count != len(schedule):
        raise RuntimeError(
            f"record count ({expected_count}) does not match schedule "
            f"length ({len(schedule)}): evaluation requires the full "
            f"schedule, not a pilot subset"
        )

    sched_lookup: dict[int, dict[str, Any]] = {
        e["sequence_index"]: e for e in schedule
    }

    # --- Parse, validate, and cross-check every record ---
    records: list[CRunRecord] = []
    seen_indices: dict[int, int] = {}
    for i, line in enumerate(lines):
        try:
            rec = CRunRecord.from_jsonl_line(line)
        except Exception as exc:
            raise RuntimeError(
                f"c_records.jsonl line {i}: invalid CRunRecord: {exc}"
            ) from exc
        records.append(rec)

        # Duplicate check.
        idx = rec.sequence_index
        if idx in seen_indices:
            raise RuntimeError(
                f"duplicate sequence_index {idx} at lines "
                f"{seen_indices[idx]} and {i}"
            )
        seen_indices[idx] = i

        # Schedule cross-check: (sequence_index, case_id, repetition).
        expected_entry = sched_lookup.get(idx)
        if expected_entry is None:
            raise RuntimeError(
                f"record {i}: sequence_index {idx} not in schedule"
            )
        if rec.physical_case_id != expected_entry["physical_case_id"]:
            raise RuntimeError(
                f"record {i}: physical_case_id mismatch at "
                f"sequence_index {idx}: record has "
                f"{rec.physical_case_id!r}, schedule has "
                f"{expected_entry['physical_case_id']!r}"
            )
        if rec.repetition != expected_entry["repetition"]:
            raise RuntimeError(
                f"record {i}: repetition mismatch at "
                f"sequence_index {idx}: record has "
                f"{rec.repetition}, schedule has "
                f"{expected_entry['repetition']}"
            )

    # --- Sequence completeness ---
    expected_indices = set(range(expected_count))
    actual_indices = set(seen_indices)
    if actual_indices != expected_indices:
        missing = sorted(expected_indices - actual_indices)
        extra = sorted(actual_indices - expected_indices)
        raise RuntimeError(
            f"sequence_index completeness check failed: "
            f"missing={missing}, extra={extra}"
        )

    return {
        "c_predictions_manifest_verified": True,
        "c_records_sha256": actual,
        "record_count": expected_count,
        "schedule_sha256": actual_sched_sha,
        "verified_records": records,
    }


# ------------------------------------------------------------------
# Full evaluation pipeline
# ------------------------------------------------------------------

def evaluate_c_predictions(
    c_records: list[Any] | None = None,
    *,
    case_truth: dict[str, str] | None = None,
    agents_config: dict[str, str] | None = None,
    label_space: set[str] | None = None,
    b_records: list[dict[str, Any]] | None = None,
    bootstrap_iterations: int = 10000,
    bootstrap_seed: int = 20260906,
    evaluator_manifest_path: Path | None = None,
    c_records_path: Path | None = None,
    c_predictions_manifest_path: Path | None = None,
    c_schedule_path: Path | None = None,
) -> dict[str, Any]:
    """Run the full Condition C evaluation pipeline.

    Parameters
    ----------
    c_records:
        CRunRecord instances or dicts from c_records.jsonl.
    case_truth:
        ``{physical_case_id: true_pseudolabel}``.  If None, loaded from
        evaluator-side files (firewall: evaluator side only).
    agents_config:
        ``{agent_id: local_fault_label}``.  If None, loaded from
        protocol_config.json.
    label_space:
        Valid label set.  Defaults to canonical Condition C labels.
    b_records:
        Phase B frozen aggregate records for delta comparison.  If None,
        loaded from the canonical path (read-only).
    bootstrap_iterations:
        Number of bootstrap resamples.
    bootstrap_seed:
        RNG seed for reproducibility.

    Returns
    -------
    Evaluation results dict with condition_c_metrics, delta_c_minus_b,
    bootstrap, and integrity information.
    """
    # Predictions integrity barrier FIRST (mandatory / fail-closed).
    # R7 review P2-1: predictions barrier must run before evaluator guard
    # so that a tampered c_records.jsonl is caught before any evaluation
    # artifacts (ground truth) are loaded.
    predictions_integrity = verify_c_predictions_freeze(
        c_records_path=c_records_path,
        manifest_path=c_predictions_manifest_path,
        schedule_path=c_schedule_path,
    )

    # Evaluator-side freeze guard (mandatory / fail-closed, R5 review).
    evaluator_integrity = verify_evaluator_freeze(
        manifest_path=(
            evaluator_manifest_path
            if evaluator_manifest_path is not None
            else EVALUATOR_FREEZE_MANIFEST_PATH
        ),
    )

    # Use records from verified file when available (P1-4: tie input
    # to verified artifact).  Fall back to c_records parameter only
    # when verify did not return parsed records (e.g. mocked in tests).
    verified_records = predictions_integrity.pop("verified_records", None)
    eval_records = verified_records if verified_records is not None else c_records
    if eval_records is None:
        raise ValueError(
            "No records available: verify_c_predictions_freeze did not "
            "return records and c_records was not provided"
        )

    if label_space is None:
        label_space = set(_RECORD_LABEL_SPACE)

    # Load evaluator-side truth if not provided.
    truth_integrity: dict[str, Any] | None = None
    if case_truth is None:
        case_truth, truth_integrity = load_case_truth()

    # Load agents config if not provided.
    if agents_config is None:
        agents_config = load_agents_config()

    # Validate case_truth labels.
    if set(case_truth.values()) - label_space:
        raise ValueError(
            "case_truth contains labels outside the label space"
        )

    # Validate agents_config: 4 agents with distinct local_fault_labels.
    if len(agents_config) != 4:
        raise ValueError(f"expected 4 agents, got {len(agents_config)}")
    if len(set(agents_config.values())) != 4:
        raise ValueError("agents must have distinct local_fault_labels")

    # Aggregate C records (completeness validated against truth keys).
    aggregates = aggregate_c_records(
        eval_records,
        label_space=label_space,
        expected_case_ids=set(case_truth),
    )

    # Validate all aggregates have truth.
    missing = {
        agg.physical_case_id
        for agg in aggregates
        if agg.physical_case_id not in case_truth
    }
    if missing:
        raise ValueError(
            f"aggregates missing evaluator-side truth: {sorted(missing)}"
        )

    # Core metrics (R5 §3.8).
    c_metrics = condition_c_metrics(
        aggregates, case_truth, label_space=label_space
    )

    # Paired delta C − B (R5 §5.2) and bootstrap (R5 §5.3).
    delta_result: dict[str, Any] | None = None
    bootstrap_result: dict[str, Any] | None = None

    if b_records is None:
        try:
            b_records = load_phase_b_aggregates()
        except FileNotFoundError:
            b_records = None

    if b_records is not None and len(b_records) > 0:
        paired_rows = build_paired_rows(
            aggregates, b_records, case_truth, agents_config
        )
        delta_result = delta_c_minus_b(paired_rows)

        bootstrap_result = bootstrap_paired_delta(
            paired_rows,
            iterations=bootstrap_iterations,
            seed=bootstrap_seed,
        )

    results: dict[str, Any] = {
        "evaluation_status": "OFFLINE_EVALUATION_CONDITION_C",
        "primary_unit": "physical_case_id",
        "abstain_treatment": "incorrect",
        "condition_c_metrics": c_metrics,
    }
    if delta_result is not None:
        results["delta_c_minus_b"] = delta_result
    if bootstrap_result is not None:
        results["bootstrap"] = bootstrap_result
    if truth_integrity is not None:
        results["ground_truth_join"] = truth_integrity
    results["evaluator_freeze_integrity"] = evaluator_integrity
    results["predictions_freeze_integrity"] = predictions_integrity

    return results


# ------------------------------------------------------------------
# Pilot gate  (R7 review P2-2)
# ------------------------------------------------------------------

PILOT_CASE_IDS = frozenset({
    "PBH-001", "PBH-004", "PBH-007", "PBH-010", "PBH-013",
})
_PILOT_RECORD_COUNT = 15  # 5 pilot cases × 3 reps


def verify_pilot_gate(
    *,
    c_records_path: Path | None = None,
    schedule_path: Path | None = None,
    expected_model: str | None = None,
    expected_sdk_version: str | None = None,
) -> dict[str, Any]:
    """Blind pilot gate: 15/15 valid records, correct model, no parse failures.

    Raises RuntimeError on any failure.  Returns integrity dict on success.

    Checks (all fail-closed):
      1. Exactly 15 records present (5 pilot cases × 3 reps).
      2. All 15 records have valid=True (no parse failures).
      3. All records reference the correct model (model_requested).
      4. All records have consistent prompt_sha256 per case_id.
      5. If *expected_sdk_version* is given, all records match it.
    """
    rec_path = c_records_path if c_records_path is not None else C_RECORDS_PATH
    sched_path = schedule_path if schedule_path is not None else C_SCHEDULE_PATH

    raw_text = rec_path.read_text(encoding="utf-8")
    lines = [ln for ln in raw_text.strip().split("\n") if ln.strip()]

    # Load schedule to identify pilot entries.
    schedule: list[dict[str, Any]] = json.loads(
        sched_path.read_text(encoding="utf-8")
    )
    pilot_indices = frozenset(
        e["sequence_index"] for e in schedule if e["pilot"]
    )
    if len(pilot_indices) != _PILOT_RECORD_COUNT:
        raise RuntimeError(
            f"schedule has {len(pilot_indices)} pilot entries, "
            f"expected {_PILOT_RECORD_COUNT}"
        )

    # Parse all records and filter pilot.
    pilot_records: list[CRunRecord] = []
    for i, line in enumerate(lines):
        try:
            rec = CRunRecord.from_jsonl_line(line)
        except Exception as exc:
            raise RuntimeError(
                f"c_records.jsonl line {i}: parse error: {exc}"
            ) from exc
        if rec.sequence_index in pilot_indices:
            pilot_records.append(rec)

    # 1. Exactly 15 pilot records.
    if len(pilot_records) != _PILOT_RECORD_COUNT:
        raise RuntimeError(
            f"pilot gate: expected {_PILOT_RECORD_COUNT} pilot records, "
            f"got {len(pilot_records)}"
        )

    # 2. All valid=True (no parse failures).
    invalid = [
        (r.sequence_index, r.physical_case_id)
        for r in pilot_records if not r.valid
    ]
    if invalid:
        raise RuntimeError(
            f"pilot gate: {len(invalid)} record(s) have valid=False — "
            f"indices {[idx for idx, _ in invalid]}"
        )

    # 3. Correct model.
    if expected_model is not None:
        wrong_model = [
            (r.sequence_index, r.model_requested)
            for r in pilot_records
            if r.model_requested != expected_model
        ]
        if wrong_model:
            raise RuntimeError(
                f"pilot gate: {len(wrong_model)} record(s) have wrong "
                f"model_requested — expected {expected_model!r}, got "
                f"{set(m for _, m in wrong_model)}"
            )

    # 4. Consistent prompt_sha256 per case_id.
    prompt_by_case: dict[str, set[str]] = defaultdict(set)
    for r in pilot_records:
        prompt_by_case[r.physical_case_id].add(r.prompt_sha256)
    inconsistent = {
        cid: hashes for cid, hashes in prompt_by_case.items()
        if len(hashes) > 1
    }
    if inconsistent:
        raise RuntimeError(
            f"pilot gate: inconsistent prompt_sha256 for cases "
            f"{sorted(inconsistent)}"
        )

    # 5. SDK version.
    if expected_sdk_version is not None:
        wrong_sdk = [
            (r.sequence_index, r.openai_sdk_version)
            for r in pilot_records
            if r.openai_sdk_version != expected_sdk_version
        ]
        if wrong_sdk:
            raise RuntimeError(
                f"pilot gate: {len(wrong_sdk)} record(s) have wrong "
                f"openai_sdk_version — expected {expected_sdk_version!r}"
            )

    return {
        "pilot_gate_passed": True,
        "pilot_records": _PILOT_RECORD_COUNT,
        "pilot_all_valid": True,
        "model_checked": expected_model,
        "sdk_version_checked": expected_sdk_version,
        "pilot_case_ids": sorted(PILOT_CASE_IDS),
    }
