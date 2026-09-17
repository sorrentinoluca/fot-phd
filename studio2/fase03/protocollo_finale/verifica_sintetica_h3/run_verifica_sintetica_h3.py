#!/usr/bin/env python3
"""Verifica sintetica H3 pre-specificata in SPECIFICA_VERIFICA_SINTETICA_H3.md rev.1.

Il programma non legge dati TEP, evidence, ledger o risposte di modelli.  I soli input
scientifici sono gli assi e le formule congelati nella specifica e nel piano 03.8.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
import os
import platform
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import minimize_scalar
from scipy.stats import beta, norm


N = 64
MARGIN = 0.125
MAIN_SEED = 20260917
NAMESPACE = "studio2-fase03-h3-synthetic-q2-v1"
REPLICATES = 100_000
BATCH_SIZE = 10_000
ALPHAS = (0.05, 0.025)
DELTAS = (-0.125, 0.0, 0.05)
DISCORDANCES = (0.15, 0.30, 0.60, 0.90)
HET_D = (0.0, 0.5, 1.0)
HET_EFFECT = (0.0, 0.5, 1.0)
PATTERNS = ("fault_time", "time_interaction", "interaction_fault")
RHOS = (0.0, 0.05, 0.10, 0.20, 0.40)
TOL = 1e-12

PLAN_TAG = "studio2-fase03-piano-statistico-frozen-001"
PLAN_COMMIT = "11f504b2bf45a39c1bc4746952f50d58c5022743"
PLAN_FILE = "studio2/fase03/piano_statistico/PIANO_STATISTICO.md"
PLAN_FILE_SHA256 = "675dbbcc96d9e1e3c153388b905291c3ece7930e563a2f78f37183b6194d032a"
TANGO_FILE = "studio2/fase03/piano_statistico/design_resolution.py"
TANGO_FILE_BLOB = "1691e3b10d8a421eee66d69a33f612eb96b432c1"
TANGO_FILE_SHA256 = "25a648b99fcb86f8111eaaf2f712183d6c3e0a0af5960b6b84c424c38fb1e613"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def jsonable(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, dict):
        return {str(k): jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(v) for v in value]
    return value


def tango_restricted_p21(b: np.ndarray, c: np.ndarray, n: int = N, delta0: float = -MARGIN) -> np.ndarray:
    """Implementazione congelata di design_resolution.py al tag PLAN_TAG."""
    aa = 2.0 * n
    bb = -(b + c) + delta0 * (2.0 * n - b + c)
    cc = -c * delta0 * (1.0 - delta0)
    disc = np.maximum(bb * bb - 4.0 * aa * cc, 0.0)
    return (-bb + np.sqrt(disc)) / (2.0 * aa)


def tango_score_z(b: np.ndarray, c: np.ndarray, n: int = N, delta0: float = -MARGIN) -> np.ndarray:
    """Implementazione congelata di design_resolution.py al tag PLAN_TAG."""
    p21 = tango_restricted_p21(b, c, n, delta0)
    variance = n * (2.0 * p21 + delta0 * (1.0 - delta0))
    variance = np.where(variance <= 0.0, np.nan, variance)
    return (b - c - n * delta0) / np.sqrt(variance)


def constrained_loglik(q: float, b: int, c: int, n: int, delta0: float) -> float:
    p21, p12, p0 = q, q + delta0, 1.0 - 2.0 * q - delta0
    terms = ((b, p12), (c, p21), (n - b - c, p0))
    if any(p < 0.0 or p > 1.0 for _, p in terms):
        return -math.inf
    if any(count > 0 and p <= 0.0 for count, p in terms):
        return -math.inf
    return sum(count * math.log(p) for count, p in terms if count > 0)


def tango_independent_numeric(b: int, c: int, n: int = N, delta0: float = -MARGIN) -> tuple[float, float]:
    """Seconda via: massimizzazione numerica 1-D della verosimiglianza vincolata."""
    lo = max(0.0, -delta0)
    hi = (1.0 - delta0) / 2.0
    eps = np.finfo(float).eps * 32
    result = minimize_scalar(
        lambda q: -constrained_loglik(float(q), b, c, n, delta0),
        bounds=(lo + eps, hi - eps),
        method="bounded",
        options={"xatol": 1e-14, "maxiter": 1000},
    )
    candidates = [lo, hi, float(result.x)]
    q = max(candidates, key=lambda x: constrained_loglik(x, b, c, n, delta0))
    variance = n * (2.0 * q + delta0 * (1.0 - delta0))
    z = (b - c - n * delta0) / math.sqrt(variance)
    return q, z


def verify_tango() -> dict[str, Any]:
    cases = ((0, 0), (N, 0), (0, N), (8, 0), (0, 8), (5, 3), (17, 22))
    checked = []
    for b, c in cases:
        q_closed = float(tango_restricted_p21(np.array([b]), np.array([c]))[0])
        z_closed = float(tango_score_z(np.array([b]), np.array([c]))[0])
        q_numeric, z_numeric = tango_independent_numeric(b, c)
        if not (math.isfinite(z_closed) and abs(q_closed - q_numeric) <= 2e-7 and abs(z_closed - z_numeric) <= 2e-6):
            raise AssertionError((b, c, q_closed, q_numeric, z_closed, z_numeric))
        checked.append({"b": b, "c": c, "p21": q_closed, "z": z_closed})
    expected_zero = math.sqrt(N * MARGIN / (1.0 - MARGIN))
    if abs(checked[0]["z"] - expected_zero) > 1e-12:
        raise AssertionError("zero-discordant published reference mismatch")
    if abs(float(tango_score_z(np.array([0]), np.array([8]))[0])) > 1e-12:
        raise AssertionError("one-sided boundary reference mismatch")
    return {"method": "independent bounded likelihood maximization", "cases": checked}


def pattern_arrays(name: str) -> tuple[np.ndarray, np.ndarray]:
    fault = np.repeat(np.where(np.arange(8) < 4, -1.0, 1.0), 8).reshape(8, 8)
    tempo = np.tile(np.where(np.arange(8) < 4, -1.0, 1.0), 8).reshape(8, 8)
    interaction = fault * tempo
    return {
        "fault_time": (fault, tempo),
        "time_interaction": (tempo, interaction),
        "interaction_fault": (interaction, fault),
    }[name]


def probability_matrix(delta: float, d: float, a: float, b: float, pattern: str) -> dict[str, np.ndarray]:
    z, v = pattern_arrays(pattern)
    aa = min(d - abs(delta), 1.0 - d)
    d_cell = d + a * aa * z
    d_min = d - a * aa
    bb = d_min - abs(delta)
    delta_cell = delta + b * bb * v
    p_plus = (d_cell + delta_cell) / 2.0
    p_minus = (d_cell - delta_cell) / 2.0
    p_zero = 1.0 - d_cell
    arrays = {
        "d": d_cell,
        "delta": delta_cell,
        "p_minus": p_minus,
        "p_zero": p_zero,
        "p_both_correct": p_zero / 2.0,
        "p_both_wrong": p_zero / 2.0,
        "p_plus": p_plus,
    }
    for key, arr in arrays.items():
        if not np.all(np.isfinite(arr)):
            raise AssertionError(f"nonfinite {key}")
    if min(float(p_minus.min()), float(p_zero.min()), float(p_plus.min())) < -TOL:
        raise AssertionError("negative probability")
    if max(float(p_minus.max()), float(p_zero.max()), float(p_plus.max())) > 1.0 + TOL:
        raise AssertionError("probability above one")
    if not np.allclose(p_minus + p_zero + p_plus, 1.0, rtol=0.0, atol=TOL):
        raise AssertionError("probabilities do not sum to one")
    if abs(float(d_cell.mean()) - d) > TOL or abs(float(delta_cell.mean()) - delta) > TOL:
        raise AssertionError("matrix means mismatch")
    return arrays


def shared_uniform_moment(p_i: np.ndarray, p_j: np.ndarray) -> float:
    # Categorie in ordine -1, 0, +1; probabilita' nelle due marginali.
    values = (-1.0, 0.0, 1.0)
    starts_i = np.r_[0.0, np.cumsum(p_i)[:-1]]
    ends_i = np.cumsum(p_i)
    starts_j = np.r_[0.0, np.cumsum(p_j)[:-1]]
    ends_j = np.cumsum(p_j)
    total = 0.0
    for x, left_i, right_i in zip(values, starts_i, ends_i):
        for y, left_j, right_j in zip(values, starts_j, ends_j):
            overlap = max(0.0, min(right_i, right_j) - max(left_i, left_j))
            total += x * y * overlap
    return total


def calibrate_faults(probs: dict[str, np.ndarray], rho: float) -> list[dict[str, Any]]:
    result = []
    category = np.stack((probs["p_minus"], probs["p_zero"], probs["p_plus"]), axis=-1)
    for fault in range(8):
        means = probs["delta"][fault]
        variances = probs["d"][fault] - means * means
        correlations: list[dict[str, Any]] = []
        excluded: list[list[int]] = []
        for i, j in itertools.combinations(range(8), 2):
            if variances[i] <= TOL or variances[j] <= TOL:
                excluded.append([i, j])
                continue
            covariance = shared_uniform_moment(category[fault, i], category[fault, j]) - means[i] * means[j]
            correlations.append({"cells": [i, j], "correlation": covariance / math.sqrt(variances[i] * variances[j])})
        c_fault = float(np.mean([x["correlation"] for x in correlations])) if correlations else None
        if rho == 0.0:
            lam, feasible = 0.0, True
        elif c_fault is None or c_fault <= 0.0:
            lam, feasible = None, False
        else:
            lam = rho / c_fault
            feasible = -TOL <= lam <= 1.0 + TOL
        result.append({
            "fault": fault,
            "shared_uniform_mean_correlation": c_fault,
            "lambda": min(1.0, max(0.0, lam)) if feasible and lam is not None else lam,
            "feasible": feasible,
            "pair_correlations_at_lambda_1": correlations,
            "excluded_degenerate_pairs": excluded,
        })
    return result


def scenario_record(index: int, values: tuple[float, float, float, float, str, float]) -> dict[str, Any]:
    delta, d, a, b, pattern, rho = values
    probs = probability_matrix(delta, d, a, b, pattern)
    faults = calibrate_faults(probs, rho)
    return {
        "scenario_index": index,
        "delta3": delta,
        "discordance": d,
        "heterogeneity_discordance": a,
        "heterogeneity_effect": b,
        "pattern": pattern,
        "rho_target": rho,
        "seed_sequence_entropy": [MAIN_SEED, index],
        "n": N,
        "replicates": REPLICATES,
        "feasible": all(x["feasible"] for x in faults),
        "probabilities": {
            k: v.tolist()
            for k, v in probs.items()
            if k in ("p_minus", "p_zero", "p_both_correct", "p_both_wrong", "p_plus")
        },
        "fault_calibration": faults,
    }


def all_scenario_values():
    return itertools.product(DELTAS, DISCORDANCES, HET_D, HET_EFFECT, PATTERNS, RHOS)


def build_manifest(path: Path) -> dict[str, Any]:
    records = [scenario_record(index, values) for index, values in enumerate(all_scenario_values())]
    if len(records) != 1620:
        raise AssertionError(len(records))
    boundary = [r for r in records if r["delta3"] == -0.125 and r["rho_target"] == 0.0]
    if len(boundary) != 108:
        raise AssertionError(len(boundary))
    with path.open("w", encoding="utf-8") as fh:
        for record in records:
            fh.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    return {
        "target_scenarios": len(records),
        "feasible_scenarios": sum(r["feasible"] for r in records),
        "infeasible_scenarios": sum(not r["feasible"] for r in records),
        "boundary_icc0_points": len(boundary),
        "manifest_sha256": sha256_file(path),
    }


def read_manifest(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as fh:
        records = [json.loads(line) for line in fh if line.strip()]
    if len(records) != 1620 or [r["scenario_index"] for r in records] != list(range(1620)):
        raise RuntimeError("manifest identity/order failure")
    return records


def empty_accumulator() -> dict[str, Any]:
    return {
        "completed": 0,
        "numeric_errors": 0,
        "rejections": {"tango_0.05": 0, "tango_0.025": 0, "hoeffding_h3_0.05": 0, "hoeffding_h3_0.025": 0, "hoeffding_h12_0.05": 0, "hoeffding_h12_0.025": 0},
        "category_counts": np.zeros((8, 8, 3), dtype=np.int64),
        "sum_d": np.zeros((8, 8), dtype=np.float64),
        "sum_d2": np.zeros((8, 8), dtype=np.float64),
        "sum_cross": np.zeros((8, 8, 8), dtype=np.float64),
    }


def serialize_accumulator(acc: dict[str, Any]) -> dict[str, Any]:
    return jsonable(acc)


def restore_accumulator(raw: dict[str, Any]) -> dict[str, Any]:
    raw["category_counts"] = np.asarray(raw["category_counts"], dtype=np.int64)
    raw["sum_d"] = np.asarray(raw["sum_d"], dtype=np.float64)
    raw["sum_d2"] = np.asarray(raw["sum_d2"], dtype=np.float64)
    raw["sum_cross"] = np.asarray(raw["sum_cross"], dtype=np.float64)
    return raw


def simulate_batch(rng: np.random.Generator, record: dict[str, Any], size: int, acc: dict[str, Any]) -> None:
    lambdas = np.array([x["lambda"] for x in record["fault_calibration"]], dtype=float)
    # Consumo RNG congelato per batch: gate (repliche,8), U indipendenti (repliche,8,8),
    # U condivise (repliche,8). Anche le estrazioni non selezionate dal gate sono consumate.
    gates = rng.random((size, 8)) < lambdas[None, :]
    independent = rng.random((size, 8, 8))
    shared = rng.random((size, 8))
    uniforms = np.where(gates[:, :, None], shared[:, :, None], independent)
    p_minus = np.asarray(record["probabilities"]["p_minus"], dtype=float)
    p_zero = np.asarray(record["probabilities"]["p_zero"], dtype=float)
    d_values = np.where(uniforms < p_minus, -1, np.where(uniforms < p_minus + p_zero, 0, 1)).astype(np.int8)
    minus = (d_values == -1).sum(axis=(1, 2))
    plus = (d_values == 1).sum(axis=(1, 2))
    z = tango_score_z(plus, minus)
    nonfinite = int((~np.isfinite(z)).sum())
    acc["numeric_errors"] += nonfinite
    if nonfinite:
        raise FloatingPointError(f"{nonfinite} nonfinite Tango statistics")
    dbar = (plus - minus) / N
    for alpha in ALPHAS:
        acc["rejections"][f"tango_{alpha}"] += int((z > norm.ppf(1.0 - alpha)).sum())
        h_threshold = math.sqrt(2.0 * math.log(1.0 / alpha) / N)
        acc["rejections"][f"hoeffding_h3_{alpha}"] += int((dbar + MARGIN >= h_threshold).sum())
        if record["delta3"] == 0.0:
            acc["rejections"][f"hoeffding_h12_{alpha}"] += int((dbar >= h_threshold).sum())
    acc["category_counts"][:, :, 0] += (d_values == -1).sum(axis=0)
    acc["category_counts"][:, :, 1] += (d_values == 0).sum(axis=0)
    acc["category_counts"][:, :, 2] += (d_values == 1).sum(axis=0)
    acc["sum_d"] += d_values.sum(axis=0)
    acc["sum_d2"] += (d_values * d_values).sum(axis=0)
    acc["sum_cross"] += np.einsum("rfi,rfj->fij", d_values, d_values, dtype=np.int64, optimize=True)
    acc["completed"] += size


def binomial_summary(k: int, n: int) -> dict[str, Any]:
    phat = k / n
    low = 0.0 if k == 0 else float(beta.ppf(0.025, k, n - k + 1))
    high = 1.0 if k == n else float(beta.ppf(0.975, k + 1, n - k))
    return {"rejections": k, "phat": phat, "mcse": math.sqrt(phat * (1.0 - phat) / n), "clopper_pearson_95": [low, high]}


def realized_dependence(acc: dict[str, Any]) -> dict[str, Any]:
    reps = acc["completed"]
    means = acc["sum_d"] / reps
    variances = acc["sum_d2"] / reps - means * means
    faults = []
    for fault in range(8):
        pairs, excluded = [], []
        for i, j in itertools.combinations(range(8), 2):
            if variances[fault, i] <= 0.0 or variances[fault, j] <= 0.0:
                excluded.append([i, j])
                continue
            covariance = acc["sum_cross"][fault, i, j] / reps - means[fault, i] * means[fault, j]
            pairs.append({"cells": [i, j], "correlation": covariance / math.sqrt(variances[fault, i] * variances[fault, j])})
        faults.append({"fault": fault, "mean_correlation": float(np.mean([p["correlation"] for p in pairs])) if pairs else None, "pair_correlations": pairs, "excluded_degenerate_pairs": excluded})
    return {"faults": faults, "all_fault_mean": float(np.mean([f["mean_correlation"] for f in faults if f["mean_correlation"] is not None]))}


def final_scenario_result(record: dict[str, Any], acc: dict[str, Any], elapsed: float) -> dict[str, Any]:
    reps = acc["completed"]
    metrics = {key: binomial_summary(value, reps) for key, value in acc["rejections"].items()}
    boundary_decision = None
    if record["delta3"] == -0.125 and record["rho_target"] == 0.0:
        boundary_decision = "PASS" if metrics["tango_0.05"]["phat"] <= 0.055 else "FAIL"
    return {
        **record,
        "status": "COMPLETE",
        "replicates_valid": reps,
        "numeric_errors": acc["numeric_errors"],
        "elapsed_seconds": elapsed,
        "metrics": metrics,
        "boundary_tango_decision": boundary_decision,
        "realized_probabilities": (acc["category_counts"] / reps).tolist(),
        "realized_dependence": realized_dependence(acc),
    }


def run_scenario(record: dict[str, Any], output: Path, lock_hash: str) -> None:
    index = record["scenario_index"]
    result_path = output / "scenarios" / f"{index:04d}.json"
    state_path = output / "state" / f"{index:04d}.json"
    if result_path.exists():
        return
    if not record["feasible"]:
        atomic_json(result_path, {**record, "status": "INFEASIBLE", "replicates_valid": 0})
        return
    started = time.monotonic()
    rng = np.random.Generator(np.random.PCG64(np.random.SeedSequence([MAIN_SEED, index])))
    acc = empty_accumulator()
    elapsed_prior = 0.0
    if state_path.exists():
        state = json.loads(state_path.read_text(encoding="utf-8"))
        if state["lock_hash"] != lock_hash or state["scenario_index"] != index:
            raise RuntimeError(f"checkpoint identity failure: {index}")
        rng.bit_generator.state = state["rng_state"]
        acc = restore_accumulator(state["accumulator"])
        elapsed_prior = state["elapsed_seconds"]
    while acc["completed"] < REPLICATES:
        size = min(BATCH_SIZE, REPLICATES - acc["completed"])
        simulate_batch(rng, record, size, acc)
        atomic_json(state_path, {
            "lock_hash": lock_hash,
            "scenario_index": index,
            "rng_state": jsonable(rng.bit_generator.state),
            "accumulator": serialize_accumulator(acc),
            "elapsed_seconds": elapsed_prior + time.monotonic() - started,
        })
    atomic_json(result_path, final_scenario_result(record, acc, elapsed_prior + time.monotonic() - started))
    state_path.unlink()


def create_run_lock(manifest_path: Path, output: Path) -> dict[str, Any]:
    script_path = Path(__file__).resolve()
    lock = {
        "namespace": NAMESPACE,
        "seed": MAIN_SEED,
        "rng": "numpy.random.Generator(PCG64(SeedSequence([20260917, scenario_index])))",
        "batch_size": BATCH_SIZE,
        "replicates_per_feasible_scenario": REPLICATES,
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": __import__("scipy").__version__,
        "script_sha256": sha256_file(script_path),
        "manifest_sha256": sha256_file(manifest_path),
        "plan": {"tag": PLAN_TAG, "commit": PLAN_COMMIT, "file": PLAN_FILE, "file_sha256": PLAN_FILE_SHA256, "tango_file": TANGO_FILE, "tango_blob": TANGO_FILE_BLOB, "tango_file_sha256": TANGO_FILE_SHA256},
        "rng_consumption_per_batch": ["gate uniforms shape (batch,8)", "independent uniforms shape (batch,8,8)", "shared uniforms shape (batch,8)"],
    }
    lock_path = output / "RUN_LOCK.json"
    if lock_path.exists():
        existing = json.loads(lock_path.read_text(encoding="utf-8"))
        if existing != lock:
            raise RuntimeError("run lock differs; refusing mixed-byte resume")
    else:
        atomic_json(lock_path, lock)
    return lock


def run_all(manifest_path: Path, output: Path) -> None:
    verify_tango()
    records = read_manifest(manifest_path)
    lock = create_run_lock(manifest_path, output)
    lock_hash = hashlib.sha256(json.dumps(lock, sort_keys=True).encode()).hexdigest()
    for record in records:
        run_scenario(record, output, lock_hash)


def self_test() -> dict[str, Any]:
    tango = verify_tango()
    # Tre scenari fuori griglia; seed e numero repliche non sono quelli ufficiali.
    cases = [(-0.10, 0.22, 0.25, 0.75, "fault_time", 0.0), (0.02, 0.48, 0.75, 0.25, "time_interaction", 0.03), (0.08, 0.72, 0.25, 0.75, "interaction_fault", 0.07)]
    summaries = []
    for index, values in enumerate(cases):
        record = scenario_record(9000 + index, values)
        if not record["feasible"]:
            raise AssertionError("off-grid smoke scenario unexpectedly infeasible")
        rng = np.random.Generator(np.random.PCG64(np.random.SeedSequence([9917001, index])))
        acc = empty_accumulator()
        simulate_batch(rng, record, 2_000, acc)
        if acc["completed"] != 2_000 or acc["numeric_errors"]:
            raise AssertionError("smoke simulation accounting failure")
        summaries.append({"parameters": values, "replicates": 2_000, "tango_rejections": acc["rejections"]["tango_0.05"]})
    return {"status": "PASS", "official_grid_used": False, "seed": 9917001, "tango_control": tango, "smoke_cases": summaries}


def aggregate(manifest_path: Path, output: Path) -> None:
    records = read_manifest(manifest_path)
    results = []
    for record in records:
        path = output / "scenarios" / f"{record['scenario_index']:04d}.json"
        if not path.exists():
            raise RuntimeError(f"missing scenario result {record['scenario_index']}")
        results.append(json.loads(path.read_text(encoding="utf-8")))
    complete = [r for r in results if r["status"] == "COMPLETE"]
    boundary = [r for r in complete if r["delta3"] == -0.125 and r["rho_target"] == 0.0]
    if len(boundary) != 108:
        raise RuntimeError(f"boundary accounting {len(boundary)} != 108")
    worst_boundary = max(boundary, key=lambda r: (r["metrics"]["tango_0.05"]["phat"], -r["scenario_index"]))
    statistical_pass = all(r["metrics"]["tango_0.05"]["phat"] <= 0.055 for r in boundary)
    # La review b567 e' deliberatamente esterna a questa esecuzione. Un pass numerico non puo'
    # autocertificarla: §5 resta PENDING finche' la review indipendente non e' OK.
    decision = "PENDING" if statistical_pass else "FALLBACK HOEFFDING"

    procedure_keys = {"Tango H3": "tango_0.05", "Hoeffding H3": "hoeffding_h3_0.05", "Hoeffding H1/H2": "hoeffding_h12_0.05"}
    robustness = {}
    for label, key in procedure_keys.items():
        applicable = [r for r in complete if (r["delta3"] == -0.125 if label != "Hoeffding H1/H2" else r["delta3"] == 0.0)]
        by_rho = {}
        for rho in RHOS:
            at_rho = [r for r in applicable if r["rho_target"] == rho]
            by_rho[str(rho)] = {"points_tested": len(at_rho), "all_le_0.055": bool(at_rho) and all(r["metrics"][key]["phat"] <= 0.055 for r in at_rho), "worst": max(at_rho, key=lambda r: r["metrics"][key]["phat"])["scenario_index"] if at_rho else None}
        max_rho = None
        for rho in RHOS:
            if by_rho[str(rho)]["all_le_0.055"] and all(by_rho[str(prior)]["all_le_0.055"] for prior in RHOS if prior <= rho):
                max_rho = rho
            else:
                break
        robustness[label] = {"maximum_tested_rho_with_prefix_all_le_0.055": max_rho, "by_rho": by_rho}

    summary = {
        "outcome_section_5": decision,
        "statistical_boundary_result": "PASS" if statistical_pass else "FAIL",
        "independent_review_b567": "NOT_PERFORMED",
        "target_scenarios": len(results),
        "complete_scenarios": len(complete),
        "infeasible_scenarios": sum(r["status"] == "INFEASIBLE" for r in results),
        "total_valid_replicates": sum(r.get("replicates_valid", 0) for r in results),
        "total_numeric_errors": sum(r.get("numeric_errors", 0) for r in results),
        "worst_boundary_icc0": {"scenario_index": worst_boundary["scenario_index"], **worst_boundary["metrics"]["tango_0.05"]},
        "robustness": robustness,
    }
    atomic_json(output / "SUMMARY.json", summary)
    with (output / "SUMMARY.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["scenario_index", "status", "delta3", "discordance", "a", "b", "pattern", "rho", "procedure", "rejections", "phat", "mcse", "ci_low", "ci_high"])
        for r in results:
            if r["status"] != "COMPLETE":
                writer.writerow([r["scenario_index"], r["status"], r["delta3"], r["discordance"], r["heterogeneity_discordance"], r["heterogeneity_effect"], r["pattern"], r["rho_target"], "", "", "", "", "", ""])
                continue
            for key, metric in r["metrics"].items():
                writer.writerow([r["scenario_index"], r["status"], r["delta3"], r["discordance"], r["heterogeneity_discordance"], r["heterogeneity_effect"], r["pattern"], r["rho_target"], key, metric["rejections"], metric["phat"], metric["mcse"], *metric["clopper_pearson_95"]])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build-manifest", "self-test", "run", "aggregate"))
    parser.add_argument("--manifest", type=Path, default=Path(__file__).with_name("SCENARI_TARGET.jsonl"))
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("risultati"))
    args = parser.parse_args()
    if args.command == "build-manifest":
        print(json.dumps(build_manifest(args.manifest), indent=2, sort_keys=True))
    elif args.command == "self-test":
        print(json.dumps(self_test(), indent=2, sort_keys=True))
    elif args.command == "run":
        run_all(args.manifest, args.output)
    else:
        aggregate(args.manifest, args.output)


if __name__ == "__main__":
    main()
