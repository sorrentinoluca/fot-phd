#!/usr/bin/env python3
"""Evaluate ablation experiment results.

Reads inference_results.jsonl produced by ablation_runner.py.
Computes per-arm accuracy, per-class recall, abstention rate,
token usage, confusion matrices, bootstrap CIs (clustered by case),
and pairwise statistical tests between arms.

Review findings addressed
-------------------------
T9  – majority_vote now requires count >= ceil(R/2); else treated as
      no-majority (counted wrong).
T10 – Bootstrap resamples at the *case* level (15 independent units,
      not 45 replicate rows).  Each pairwise comparison uses an
      independent RNG derived deterministically from (SEED, pair_name).
      p-values are two-sided.  Holm–Bonferroni correction is applied
      across the 6 pairwise comparisons.
L7  – Added balanced accuracy / MCC / macro-F1.

Results review v2 findings addressed
-------------------------------------
R1  – CRITICAL: McNemar was not cluster-aware (N=45 non-independent
      rows).  Added:
      * Paired permutation test clustered by case_id (exact sign-flip,
        2^15 permutations).
      * McNemar at case level (majority-vote aggregated, N=15, exact
        binomial).
      Row-level McNemar retained for reference but labeled
      NON-INFERENTIAL.
R3  – MAJOR: "top-3 indistinguishable" overclaiming corrected to "not
      demonstrably different given available statistical power".
R8  – MAJOR: F13 "universally hardest" corrected to arm-dependent.
R10 – MAJOR: V2_TEXT efficiency claim qualified re domain knowledge.
R16 – MINOR: abstention scoring caveated; selective accuracy & coverage
      added.
R21 – MAJOR: added leave-one-class-out accuracy, selective accuracy,
      coverage, and sensitivity analyses.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np


LABEL_SPACE = ["F1", "F8", "F10", "F13", "Normal"]
ARM_ORDER = ["V2_TEXT", "RAW_FEATURES", "CGTIME_STATS", "SAX_SYMBOLIC"]
N_BOOTSTRAP = 10_000
SEED = 42


# ── helpers ──────────────────────────────────────────────────────────


def _derive_rng(base_seed: int, name: str) -> np.random.Generator:
    """Deterministic, independent RNG for *name* so that adding/removing
    comparisons does not change the CIs of other comparisons."""
    h = hashlib.sha256(f"{base_seed}:{name}".encode()).hexdigest()
    derived_seed = int(h[:16], 16)          # 64-bit seed
    return np.random.default_rng(derived_seed)


# ── Data loading ─────────────────────────────────────────────────────


@dataclass
class Record:
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
    error: str | None


def load_results(path: Path) -> list[Record]:
    records: list[Record] = []
    with path.open("r") as f:
        for line in f:
            d = json.loads(line)
            records.append(Record(
                case_id=d["case_id"],
                true_label=d["true_label"],
                arm=d["arm"],
                repetition=d["repetition"],
                predicted_label=d.get("predicted_label"),
                abstain=d.get("abstain", False),
                reasoning_summary=d.get("reasoning_summary", ""),
                input_tokens=d.get("input_tokens", 0),
                output_tokens=d.get("output_tokens", 0),
                latency_ms=d.get("latency_ms", 0.0),
                prompt_hash=d.get("prompt_hash", ""),
                error=d.get("error"),
            ))
    return records


# ── Core metrics ─────────────────────────────────────────────────────


def _is_correct(r: Record) -> bool:
    return (not r.abstain) and r.predicted_label == r.true_label


def accuracy_including_abstain(records: list[Record]) -> float:
    """Fraction correct; abstain and wrong both count as incorrect."""
    if not records:
        return 0.0
    return sum(1 for r in records if _is_correct(r)) / len(records)


def abstention_rate(records: list[Record]) -> float:
    if not records:
        return 0.0
    return sum(1 for r in records if r.abstain) / len(records)


def per_class_recall(records: list[Record]) -> dict[str, float]:
    """Recall per true class (abstain counted as wrong)."""
    by_class: dict[str, list[Record]] = defaultdict(list)
    for r in records:
        by_class[r.true_label].append(r)
    result: dict[str, float] = {}
    for label in LABEL_SPACE:
        cls = by_class.get(label, [])
        if not cls:
            result[label] = float("nan")
        else:
            result[label] = sum(1 for r in cls if _is_correct(r)) / len(cls)
    return result


def fault_only_accuracy(records: list[Record]) -> float:
    """Accuracy excluding Normal cases."""
    return accuracy_including_abstain([r for r in records if r.true_label != "Normal"])


def balanced_accuracy(records: list[Record]) -> float:
    """Mean of per-class recalls (abstain = wrong)."""
    recalls = per_class_recall(records)
    valid = [v for v in recalls.values() if not math.isnan(v)]
    return sum(valid) / len(valid) if valid else 0.0


def macro_f1(records: list[Record]) -> float:
    """Macro-averaged F1 across the label space."""
    # Build per-class TP / FP / FN
    tp: dict[str, int] = {l: 0 for l in LABEL_SPACE}
    fp: dict[str, int] = {l: 0 for l in LABEL_SPACE}
    fn: dict[str, int] = {l: 0 for l in LABEL_SPACE}
    for r in records:
        pred = r.predicted_label if not r.abstain else None
        for label in LABEL_SPACE:
            if r.true_label == label and pred == label:
                tp[label] += 1
            elif pred == label and r.true_label != label:
                fp[label] += 1
            elif r.true_label == label and pred != label:
                fn[label] += 1
    f1s: list[float] = []
    for label in LABEL_SPACE:
        p = tp[label] / (tp[label] + fp[label]) if (tp[label] + fp[label]) else 0.0
        r_ = tp[label] / (tp[label] + fn[label]) if (tp[label] + fn[label]) else 0.0
        f1 = 2 * p * r_ / (p + r_) if (p + r_) else 0.0
        f1s.append(f1)
    return sum(f1s) / len(f1s) if f1s else 0.0


def matthews_corrcoef(records: list[Record]) -> float:
    """Multi-class MCC (Gorodkin 2004).  Abstain → mapped to 'ABSTAIN' pseudo-class."""
    labels = LABEL_SPACE + ["ABSTAIN"]
    idx = {l: i for i, l in enumerate(labels)}
    K = len(labels)
    C = np.zeros((K, K), dtype=np.float64)
    for r in records:
        true_i = idx.get(r.true_label)
        pred = "ABSTAIN" if r.abstain or r.predicted_label is None else r.predicted_label
        pred_i = idx.get(pred)
        if true_i is not None and pred_i is not None:
            C[true_i, pred_i] += 1
    # Multi-class MCC formula via confusion matrix
    N = C.sum()
    if N == 0:
        return 0.0
    tk = C.diagonal().copy()       # t_k = correct per class
    pk = C.sum(axis=0)             # predicted per class
    t_k_true = C.sum(axis=1)      # true per class
    cov_yy = N * tk.sum() - (pk * t_k_true).sum()
    cov_xx_pred = N ** 2 - (pk ** 2).sum()
    cov_xx_true = N ** 2 - (t_k_true ** 2).sum()
    denom = math.sqrt(float(cov_xx_pred * cov_xx_true))
    return float(cov_yy / denom) if denom > 0 else 0.0


def confusion_matrix(records: list[Record]) -> dict[str, dict[str, int]]:
    """Rows = true labels, columns = predicted labels + ABSTAIN."""
    labels_plus = LABEL_SPACE + ["ABSTAIN"]
    matrix: dict[str, dict[str, int]] = {
        true: {pred: 0 for pred in labels_plus} for true in LABEL_SPACE
    }
    for r in records:
        pred = "ABSTAIN" if r.abstain or r.predicted_label is None else r.predicted_label
        if r.true_label in matrix and pred in matrix[r.true_label]:
            matrix[r.true_label][pred] += 1
    return matrix


# ── Selective accuracy / coverage (review finding R10/R21) ──────────


def selective_accuracy(records: list[Record]) -> tuple[float, float]:
    """Accuracy among non-abstained predictions and coverage.

    Returns (sel_acc, coverage) where:
    - coverage = fraction of non-abstained predictions
    - sel_acc = accuracy conditioned on non-abstention
    """
    non_abstained = [r for r in records if not r.abstain]
    coverage = len(non_abstained) / len(records) if records else 0.0
    if not non_abstained:
        return 0.0, 0.0
    sel_acc = sum(
        1 for r in non_abstained if r.predicted_label == r.true_label
    ) / len(non_abstained)
    return sel_acc, coverage


def accuracy_excluding_class(
    records: list[Record], exclude_class: str,
) -> float:
    """Accuracy on all records except those with true_label == exclude_class."""
    subset = [r for r in records if r.true_label != exclude_class]
    return accuracy_including_abstain(subset)


def leave_one_class_out(records: list[Record]) -> dict[str, float]:
    """Accuracy when excluding each class in turn."""
    return {
        f"excl_{label}": round(accuracy_excluding_class(records, label), 4)
        for label in LABEL_SPACE
    }


# ── Bootstrap confidence intervals (clustered by case) ──────────────


def _case_accuracy(records: list[Record], case_ids: list[str]) -> float:
    """Accuracy over the subset of records whose case_id is in *case_ids*."""
    subset = [r for r in records if r.case_id in set(case_ids)]
    return accuracy_including_abstain(subset)


def bootstrap_accuracy_ci(
    records: list[Record],
    arm_name: str,
    n_boot: int = N_BOOTSTRAP,
    alpha: float = 0.05,
) -> tuple[float, float, float]:
    """Bootstrap CI for accuracy (abstain=wrong), clustered by case_id.

    Resamples the 15 case_ids (with replacement), keeping all reps per
    case together.  Uses an independent RNG derived from (SEED, arm_name).
    Returns (point, lower, upper).
    """
    rng = _derive_rng(SEED, f"ci:{arm_name}")
    case_ids = sorted({r.case_id for r in records})
    n_cases = len(case_ids)

    # Pre-compute per-case correctness vectors for speed
    by_case: dict[str, list[int]] = defaultdict(list)
    for r in records:
        by_case[r.case_id].append(1 if _is_correct(r) else 0)

    # All-records point estimate
    correct_arr = np.array([1 if _is_correct(r) else 0 for r in records])
    point = float(correct_arr.mean())

    # Bootstrap at case level
    boot_means = np.empty(n_boot)
    for b in range(n_boot):
        sampled_cases = rng.choice(case_ids, size=n_cases, replace=True)
        hits: list[int] = []
        for c in sampled_cases:
            hits.extend(by_case[c])
        boot_means[b] = np.mean(hits) if hits else 0.0

    lower = float(np.percentile(boot_means, 100 * alpha / 2))
    upper = float(np.percentile(boot_means, 100 * (1 - alpha / 2)))
    return point, lower, upper


def bootstrap_accuracy_diff_ci(
    records_a: list[Record],
    records_b: list[Record],
    pair_name: str,
    n_boot: int = N_BOOTSTRAP,
    alpha: float = 0.05,
) -> tuple[float, float, float, float]:
    """Bootstrap CI for accuracy(A) − accuracy(B), clustered by case.

    Resamples matched case_ids (keeping all reps for each case).
    Uses an independent RNG derived from (SEED, pair_name).
    Returns (diff_point, lower, upper, two_sided_p_value).
    """
    rng = _derive_rng(SEED, f"diff:{pair_name}")

    cases_a = {r.case_id for r in records_a}
    cases_b = {r.case_id for r in records_b}
    shared_cases = sorted(cases_a & cases_b)
    n_cases = len(shared_cases)
    if n_cases == 0:
        return 0.0, 0.0, 0.0, 1.0

    # Pre-compute per-case correctness
    by_case_a: dict[str, list[int]] = defaultdict(list)
    by_case_b: dict[str, list[int]] = defaultdict(list)
    for r in records_a:
        if r.case_id in set(shared_cases):
            by_case_a[r.case_id].append(1 if _is_correct(r) else 0)
    for r in records_b:
        if r.case_id in set(shared_cases):
            by_case_b[r.case_id].append(1 if _is_correct(r) else 0)

    # Point estimate: mean per-case accuracy difference
    all_a = [v for c in shared_cases for v in by_case_a[c]]
    all_b = [v for c in shared_cases for v in by_case_b[c]]
    point = np.mean(all_a) - np.mean(all_b) if all_a and all_b else 0.0

    # Clustered bootstrap
    boot_diffs = np.empty(n_boot)
    for b in range(n_boot):
        sampled_cases = rng.choice(shared_cases, size=n_cases, replace=True)
        hits_a: list[int] = []
        hits_b: list[int] = []
        for c in sampled_cases:
            hits_a.extend(by_case_a[c])
            hits_b.extend(by_case_b[c])
        mean_a = np.mean(hits_a) if hits_a else 0.0
        mean_b = np.mean(hits_b) if hits_b else 0.0
        boot_diffs[b] = mean_a - mean_b

    lower = float(np.percentile(boot_diffs, 100 * alpha / 2))
    upper = float(np.percentile(boot_diffs, 100 * (1 - alpha / 2)))

    # Two-sided p-value
    p_left = float(np.mean(boot_diffs <= 0))
    p_right = float(np.mean(boot_diffs >= 0))
    p_value = 2.0 * min(p_left, p_right)
    p_value = min(p_value, 1.0)     # clip

    return float(point), lower, upper, p_value


# ── McNemar's test (exact binomial when discordant < 25) ────────────


def mcnemar_test(
    records_a: list[Record],
    records_b: list[Record],
) -> dict[str, Any]:
    """McNemar's test on matched (case_id, rep) pairs.

    Uses exact binomial test (scipy.stats.binomtest) when the number of
    discordant pairs is < 25; asymptotic chi-squared with continuity
    correction otherwise.  Always two-sided.
    """
    key_a = {(r.case_id, r.repetition): r for r in records_a}
    key_b = {(r.case_id, r.repetition): r for r in records_b}
    shared = sorted(set(key_a) & set(key_b))

    n_both_right = 0
    n_both_wrong = 0
    n_a_only = 0        # A right, B wrong
    n_b_only = 0        # B right, A wrong

    for k in shared:
        a_ok = _is_correct(key_a[k])
        b_ok = _is_correct(key_b[k])
        if a_ok and b_ok:
            n_both_right += 1
        elif not a_ok and not b_ok:
            n_both_wrong += 1
        elif a_ok:
            n_a_only += 1
        else:
            n_b_only += 1

    discordant = n_a_only + n_b_only

    if discordant == 0:
        return {
            "n_paired": len(shared),
            "n_both_right": n_both_right,
            "n_both_wrong": n_both_wrong,
            "n_a_only_right": n_a_only,
            "n_b_only_right": n_b_only,
            "test_type": "none (no discordant pairs)",
            "statistic": 0.0,
            "p_value": 1.0,
        }

    if discordant < 25:
        # Exact binomial: under H0, n_a_only ~ Binomial(discordant, 0.5)
        from scipy.stats import binomtest
        result = binomtest(n_a_only, discordant, 0.5, alternative="two-sided")
        return {
            "n_paired": len(shared),
            "n_both_right": n_both_right,
            "n_both_wrong": n_both_wrong,
            "n_a_only_right": n_a_only,
            "n_b_only_right": n_b_only,
            "test_type": "exact binomial",
            "statistic": n_a_only,
            "p_value": round(float(result.pvalue), 6),
        }
    else:
        # Asymptotic chi-squared with continuity correction
        from scipy.stats import chi2 as chi2_dist
        chi2_stat = (abs(n_a_only - n_b_only) - 1) ** 2 / discordant
        p_val = 1.0 - chi2_dist.cdf(chi2_stat, df=1)
        return {
            "n_paired": len(shared),
            "n_both_right": n_both_right,
            "n_both_wrong": n_both_wrong,
            "n_a_only_right": n_a_only,
            "n_b_only_right": n_b_only,
            "test_type": "chi-squared (continuity-corrected)",
            "statistic": round(chi2_stat, 4),
            "p_value": round(p_val, 6),
        }


# ── Cluster-aware pairwise tests (review finding R1) ─────────────────


def permutation_test_clustered(
    records_a: list[Record],
    records_b: list[Record],
    pair_name: str,
    n_perm: int = 100_000,
) -> dict[str, Any]:
    """Paired permutation test at the case_id level (cluster-aware).

    For each case, computes per-case accuracy for arm A and arm B,
    then tests H0: mean difference = 0 via sign-flip permutation.
    With 15 cases, 2^15 = 32 768 permutations — uses exact enumeration.
    """
    rng = _derive_rng(SEED, f"perm:{pair_name}")

    # Build per-case accuracy for each arm
    cases_a: dict[str, list[int]] = defaultdict(list)
    cases_b: dict[str, list[int]] = defaultdict(list)
    for r in records_a:
        cases_a[r.case_id].append(1 if _is_correct(r) else 0)
    for r in records_b:
        cases_b[r.case_id].append(1 if _is_correct(r) else 0)

    shared = sorted(set(cases_a) & set(cases_b))
    n_cases = len(shared)
    if n_cases == 0:
        return {"n_cases": 0, "observed_diff": 0.0, "p_value": 1.0,
                "test_type": "none"}

    # Per-case accuracy differences
    diffs = np.array([
        np.mean(cases_a[c]) - np.mean(cases_b[c])
        for c in shared
    ])
    observed = float(np.mean(diffs))

    # Sign-flip permutation test
    total_perms = 2 ** n_cases
    if total_perms <= n_perm:
        # Exact enumeration
        count_ge = 0
        for mask in range(total_perms):
            signs = np.array([
                (1 if (mask >> j) & 1 else -1) for j in range(n_cases)
            ])
            perm_mean = float(np.mean(diffs * signs))
            if abs(perm_mean) >= abs(observed) - 1e-12:
                count_ge += 1
        p_value = count_ge / total_perms
        test_type = f"exact sign-flip ({total_perms} perms)"
    else:
        # Random permutations (fallback for larger N)
        count_ge = 0
        for _ in range(n_perm):
            signs = rng.choice([-1, 1], size=n_cases)
            perm_mean = float(np.mean(diffs * signs))
            if abs(perm_mean) >= abs(observed) - 1e-12:
                count_ge += 1
        p_value = (count_ge + 1) / (n_perm + 1)
        test_type = f"random sign-flip ({n_perm} perms)"

    return {
        "n_cases": n_cases,
        "observed_diff": round(observed, 4),
        "p_value": round(p_value, 6),
        "test_type": test_type,
    }


def mcnemar_case_level(
    records_a: list[Record],
    records_b: list[Record],
) -> dict[str, Any]:
    """McNemar's test on majority-vote aggregated outcomes per case (N=15).

    Aggregates each arm's predictions per case to a single binary outcome
    via majority vote, then applies McNemar on these 15 paired outcomes.
    Respects the clustering structure (case_id as independent unit).
    """
    def _case_outcomes(records: list[Record]) -> dict[str, bool]:
        by_case: dict[str, list[Record]] = defaultdict(list)
        for r in records:
            by_case[r.case_id].append(r)
        outcomes: dict[str, bool] = {}
        for case_id, recs in by_case.items():
            true_label = recs[0].true_label
            votes = [r.predicted_label for r in recs
                     if r.predicted_label is not None and not r.abstain]
            R = len(recs)
            threshold = math.ceil(R / 2)
            if not votes:
                outcomes[case_id] = False
                continue
            counter = Counter(votes)
            best_label, best_count = counter.most_common(1)[0]
            outcomes[case_id] = (
                best_count >= threshold and best_label == true_label
            )
        return outcomes

    out_a = _case_outcomes(records_a)
    out_b = _case_outcomes(records_b)
    shared = sorted(set(out_a) & set(out_b))

    n_both_right = sum(1 for c in shared if out_a[c] and out_b[c])
    n_both_wrong = sum(1 for c in shared if not out_a[c] and not out_b[c])
    n_a_only = sum(1 for c in shared if out_a[c] and not out_b[c])
    n_b_only = sum(1 for c in shared if not out_a[c] and out_b[c])

    discordant = n_a_only + n_b_only

    if discordant == 0:
        return {
            "n_cases": len(shared),
            "n_both_right": n_both_right,
            "n_both_wrong": n_both_wrong,
            "n_a_only_right": n_a_only,
            "n_b_only_right": n_b_only,
            "test_type": "none (no discordant cases)",
            "statistic": 0,
            "p_value": 1.0,
        }

    from scipy.stats import binomtest
    result = binomtest(n_a_only, discordant, 0.5, alternative="two-sided")
    return {
        "n_cases": len(shared),
        "n_both_right": n_both_right,
        "n_both_wrong": n_both_wrong,
        "n_a_only_right": n_a_only,
        "n_b_only_right": n_b_only,
        "test_type": "exact binomial (case-level majority vote)",
        "statistic": n_a_only,
        "p_value": round(float(result.pvalue), 6),
    }


# ── Holm–Bonferroni correction ──────────────────────────────────────


def holm_bonferroni(
    p_values: list[tuple[str, float]],
    alpha: float = 0.05,
) -> list[dict[str, Any]]:
    """Apply Holm–Bonferroni step-down correction.

    *p_values* is a list of (name, raw_p).
    Returns a list of dicts sorted by raw p, each containing:
      name, raw_p, adjusted_p, significant (bool).
    """
    m = len(p_values)
    if m == 0:
        return []
    sorted_ps = sorted(p_values, key=lambda x: x[1])
    results: list[dict[str, Any]] = []
    max_adj = 0.0
    for i, (name, raw_p) in enumerate(sorted_ps):
        adj = raw_p * (m - i)
        adj = max(adj, max_adj)     # enforce monotonicity
        adj = min(adj, 1.0)
        max_adj = adj
        results.append({
            "name": name,
            "raw_p": round(raw_p, 6),
            "adjusted_p": round(adj, 6),
            "significant": adj < alpha,
        })
    return results


# ── Majority vote aggregation (T9: require >= ceil(R/2)) ────────────


def majority_vote_accuracy(
    records: list[Record],
    min_agreement: int | None = None,
) -> tuple[float, int]:
    """Per-case majority vote, requiring at least *min_agreement* votes
    for the plurality label.

    If *min_agreement* is None, it defaults to ceil(R/2) where R is the
    number of repetitions per case (deduced from data).

    Returns (accuracy, n_no_majority) where no-majority cases count as
    wrong.
    """
    by_case: dict[str, list[Record]] = defaultdict(list)
    for r in records:
        by_case[r.case_id].append(r)

    correct = 0
    total = 0
    n_no_majority = 0

    for case_id, recs in by_case.items():
        true_label = recs[0].true_label
        votes = [r.predicted_label for r in recs if r.predicted_label is not None and not r.abstain]
        R = len(recs)
        threshold = min_agreement if min_agreement is not None else math.ceil(R / 2)

        if not votes:
            # All abstained → no majority → wrong
            n_no_majority += 1
            total += 1
            continue

        counter = Counter(votes)
        best_label, best_count = counter.most_common(1)[0]

        if best_count < threshold:
            n_no_majority += 1
            total += 1
            continue

        if best_label == true_label:
            correct += 1
        total += 1

    return (correct / total if total > 0 else 0.0), n_no_majority


# ── Token / cost analysis ───────────────────────────────────────────


def token_stats(records: list[Record]) -> dict[str, Any]:
    if not records:
        return {"mean_input": 0, "mean_output": 0, "total_input": 0,
                "total_output": 0, "mean_latency_ms": 0}
    return {
        "mean_input": sum(r.input_tokens for r in records) / len(records),
        "mean_output": sum(r.output_tokens for r in records) / len(records),
        "total_input": sum(r.input_tokens for r in records),
        "total_output": sum(r.output_tokens for r in records),
        "mean_latency_ms": sum(r.latency_ms for r in records) / len(records),
    }


# ── Consistency ──────────────────────────────────────────────────────


def repetition_agreement(records: list[Record]) -> float:
    """Fraction of cases where all repetitions agree on the same label."""
    by_case: dict[str, list[str | None]] = defaultdict(list)
    for r in records:
        by_case[r.case_id].append(r.predicted_label)
    n_agree = sum(1 for labels in by_case.values() if len(set(labels)) == 1)
    return n_agree / len(by_case) if by_case else 0.0


# ── Formatting helpers ───────────────────────────────────────────────


def format_confusion_matrix(cm: dict[str, dict[str, int]], arm_name: str) -> str:
    labels = LABEL_SPACE + ["ABSTAIN"]
    header = f"{'':>8s}" + "".join(f"{l:>8s}" for l in labels) + "  |  Total"
    lines = [f"\nConfusion Matrix: {arm_name}", "  True \\ Pred", header,
             "  " + "-" * len(header)]
    for true in LABEL_SPACE:
        row = f"  {true:>8s}"
        total = 0
        for pred in labels:
            val = cm[true].get(pred, 0)
            row += f"{val:>8d}"
            total += val
        row += f"  |  {total:>5d}"
        lines.append(row)
    return "\n".join(lines)


def format_pairwise_table(
    pairwise: dict[str, dict[str, Any]],
    holm_results: list[dict[str, Any]],
) -> str:
    lines = ["\nPairwise Comparisons (bootstrap diff A−B, McNemar, Holm–Bonferroni)"]
    lines.append(
        f"  {'Comparison':<30s} {'Δ acc':>8s} {'95% CI':>16s} "
        f"{'p(boot)':>10s} {'p(adj)':>10s} {'McN p':>10s} {'McN type':>16s}"
    )
    lines.append("  " + "-" * 110)

    # Build a lookup for Holm-adjusted bootstrap p
    boot_adj: dict[str, float] = {}
    for h in holm_results:
        if h["name"].startswith("boot:"):
            boot_adj[h["name"][5:]] = h["adjusted_p"]

    for pair_name, data in pairwise.items():
        diff = data["bootstrap_diff"]
        mcn = data["mcnemar"]
        ci_str = f"[{diff['lower']:.3f}, {diff['upper']:.3f}]"
        adj_p = boot_adj.get(pair_name, diff["p_value"])
        lines.append(
            f"  {pair_name:<30s} "
            f"{diff['point']:>+8.3f} "
            f"{ci_str:>16s} "
            f"{diff['p_value']:>10.4f} "
            f"{adj_p:>10.4f} "
            f"{mcn['p_value']:>10.4f} "
            f"{mcn['test_type']:>16s}"
        )
    return "\n".join(lines)


# ── Main evaluation ─────────────────────────────────────────────────


def evaluate(results_dir: Path, output_path: Path | None = None) -> dict[str, Any]:
    results_path = results_dir / "inference_results.jsonl"
    if not results_path.exists():
        print(f"Error: {results_path} not found", file=sys.stderr)
        sys.exit(1)

    records = load_results(results_path)
    print(f"Loaded {len(records)} inference records from {results_path}")

    # Group by arm
    by_arm: dict[str, list[Record]] = defaultdict(list)
    for r in records:
        by_arm[r.arm].append(r)

    report: dict[str, Any] = {
        "total_records": len(records),
        "seed": SEED,
        "n_bootstrap": N_BOOTSTRAP,
        "clustering": "case_id (15 independent units)",
        "arms": {},
        "pairwise": {},
        "holm_bonferroni": {},
    }

    # ── Per-arm metrics ──
    print("\n" + "=" * 80)
    print("ABLATION EXPERIMENT RESULTS")
    print("=" * 80)

    for arm in ARM_ORDER:
        arm_records = by_arm.get(arm, [])
        if not arm_records:
            continue

        acc = accuracy_including_abstain(arm_records)
        acc_point, acc_lo, acc_hi = bootstrap_accuracy_ci(arm_records, arm_name=arm)
        fault_acc = fault_only_accuracy(arm_records)
        abst = abstention_rate(arm_records)
        recall = per_class_recall(arm_records)
        cm = confusion_matrix(arm_records)
        tokens = token_stats(arm_records)
        mv_acc, mv_no_maj = majority_vote_accuracy(arm_records)
        rep_agree = repetition_agreement(arm_records)
        bal_acc = balanced_accuracy(arm_records)
        mf1 = macro_f1(arm_records)
        mcc = matthews_corrcoef(arm_records)

        sel_acc, cov = selective_accuracy(arm_records)
        loco = leave_one_class_out(arm_records)

        arm_report: dict[str, Any] = {
            "n_records": len(arm_records),
            "accuracy": round(acc, 4),
            "accuracy_95ci": [round(acc_lo, 4), round(acc_hi, 4)],
            "balanced_accuracy": round(bal_acc, 4),
            "macro_f1": round(mf1, 4),
            "mcc": round(mcc, 4),
            "fault_only_accuracy": round(fault_acc, 4),
            "majority_vote_accuracy": round(mv_acc, 4),
            "majority_vote_no_majority_cases": mv_no_maj,
            "abstention_rate": round(abst, 4),
            "selective_accuracy": round(sel_acc, 4),
            "coverage": round(cov, 4),
            "leave_one_class_out": loco,
            "repetition_agreement": round(rep_agree, 4),
            "per_class_recall": {k: round(v, 4) for k, v in recall.items()},
            "confusion_matrix": cm,
            "tokens": tokens,
        }
        report["arms"][arm] = arm_report

        print(f"\n{'─' * 40}")
        print(f"ARM: {arm}")
        print(f"{'─' * 40}")
        print(f"  Records:             {len(arm_records)}")
        print(f"  Accuracy:            {acc:.3f}  95% CI [{acc_lo:.3f}, {acc_hi:.3f}]")
        print(f"  Balanced accuracy:   {bal_acc:.3f}")
        print(f"  Macro-F1:            {mf1:.3f}")
        print(f"  MCC:                 {mcc:.3f}")
        print(f"  Fault-only accuracy: {fault_acc:.3f}")
        print(f"  Majority vote acc:   {mv_acc:.3f}  (no-majority: {mv_no_maj})")
        print(f"  Abstention rate:     {abst:.3f}")
        print(f"  Selective accuracy:  {sel_acc:.3f}  (coverage: {cov:.3f})")
        print(f"  Rep. agreement:      {rep_agree:.3f}")
        print(f"  Leave-one-class-out:")
        for k, v in loco.items():
            print(f"    {k:>10s}: {v:.3f}")
        print(f"  Per-class recall:")
        for label in LABEL_SPACE:
            print(f"    {label:>6s}: {recall[label]:.3f}")
        print(f"  Tokens (mean):       in={tokens['mean_input']:.0f}  out={tokens['mean_output']:.0f}")
        print(format_confusion_matrix(cm, arm))

    # ── Pairwise comparisons ──
    print("\n" + "=" * 80)
    print("PAIRWISE COMPARISONS")
    print("=" * 80)

    pairwise_results: dict[str, dict[str, Any]] = {}
    raw_p_values_boot: list[tuple[str, float]] = []
    raw_p_values_perm: list[tuple[str, float]] = []
    raw_p_values_mcn_case: list[tuple[str, float]] = []
    raw_p_values_mcn_row: list[tuple[str, float]] = []

    # Generate all C(4,2) = 6 pairs
    for i, arm_a in enumerate(ARM_ORDER):
        for arm_b in ARM_ORDER[i + 1:]:
            pair_name = f"{arm_a} vs {arm_b}"
            recs_a = by_arm.get(arm_a, [])
            recs_b = by_arm.get(arm_b, [])
            if not recs_a or not recs_b:
                continue

            diff_point, diff_lo, diff_hi, p_boot = bootstrap_accuracy_diff_ci(
                recs_a, recs_b, pair_name=pair_name,
            )

            # Cluster-aware tests (review finding R1)
            perm = permutation_test_clustered(recs_a, recs_b, pair_name)
            mcn_case = mcnemar_case_level(recs_a, recs_b)

            # Original row-level McNemar (retained for reference, clearly
            # labeled as non-cluster-aware; NOT used for inference)
            mcn_row = mcnemar_test(recs_a, recs_b)

            pairwise_results[pair_name] = {
                "bootstrap_diff": {
                    "point": round(diff_point, 4),
                    "lower": round(diff_lo, 4),
                    "upper": round(diff_hi, 4),
                    "p_value": round(p_boot, 6),
                    "test_type": "two-sided, clustered by case_id",
                },
                "permutation_test": perm,
                "mcnemar_case_level": mcn_case,
                "mcnemar_row_level_NON_INFERENTIAL": mcn_row,
            }
            raw_p_values_boot.append((f"boot:{pair_name}", p_boot))
            raw_p_values_perm.append((f"perm:{pair_name}", perm["p_value"]))
            raw_p_values_mcn_case.append(
                (f"mcn_case:{pair_name}", mcn_case["p_value"])
            )
            raw_p_values_mcn_row.append(
                (f"mcn_row:{pair_name}", mcn_row["p_value"])
            )

    # Holm–Bonferroni correction across all pairwise comparisons
    holm_boot = holm_bonferroni(raw_p_values_boot)
    holm_perm = holm_bonferroni(raw_p_values_perm)
    holm_mcn_case = holm_bonferroni(raw_p_values_mcn_case)
    holm_mcn_row = holm_bonferroni(raw_p_values_mcn_row)

    report["pairwise"] = pairwise_results
    report["holm_bonferroni"] = {
        "bootstrap": holm_boot,
        "permutation_test": holm_perm,
        "mcnemar_case_level": holm_mcn_case,
        "mcnemar_row_level_NON_INFERENTIAL": holm_mcn_row,
    }

    # Print pairwise summary (cluster-aware tests)
    print("\n  ── Cluster-aware pairwise tests (primary inference) ──\n")
    print(
        f"  {'Comparison':<30s} {'Δ acc':>8s} {'Boot CI':>16s} "
        f"{'p(boot)':>10s} {'p(perm)':>10s} {'p(McN-case)':>12s}"
    )
    print("  " + "-" * 90)
    for pair_name, data in pairwise_results.items():
        d = data["bootstrap_diff"]
        ci_str = f"[{d['lower']:.3f}, {d['upper']:.3f}]"
        print(
            f"  {pair_name:<30s} "
            f"{d['point']:>+8.3f} "
            f"{ci_str:>16s} "
            f"{d['p_value']:>10.4f} "
            f"{data['permutation_test']['p_value']:>10.4f} "
            f"{data['mcnemar_case_level']['p_value']:>12.4f}"
        )

    # Holm–Bonferroni: bootstrap
    print("\n  Holm–Bonferroni correction (clustered bootstrap):")
    for h in holm_boot:
        sig = "***" if h["significant"] else "   "
        name = h["name"].replace("boot:", "")
        print(f"    {name:<30s}  raw={h['raw_p']:.4f}  adj={h['adjusted_p']:.4f}  {sig}")

    # Holm–Bonferroni: permutation test
    print("\n  Holm–Bonferroni correction (permutation test, cluster-aware):")
    for h in holm_perm:
        sig = "***" if h["significant"] else "   "
        name = h["name"].replace("perm:", "")
        print(f"    {name:<30s}  raw={h['raw_p']:.4f}  adj={h['adjusted_p']:.4f}  {sig}")

    # Holm–Bonferroni: McNemar case-level
    print("\n  Holm–Bonferroni correction (McNemar case-level, N=15):")
    for h in holm_mcn_case:
        sig = "***" if h["significant"] else "   "
        name = h["name"].replace("mcn_case:", "")
        print(f"    {name:<30s}  raw={h['raw_p']:.4f}  adj={h['adjusted_p']:.4f}  {sig}")

    # Row-level McNemar (reference only)
    print("\n  ── Row-level McNemar (NON-INFERENTIAL, N=45, retained for reference) ──")
    for h in holm_mcn_row:
        sig = "***" if h["significant"] else "   "
        name = h["name"].replace("mcn_row:", "")
        print(f"    {name:<30s}  raw={h['raw_p']:.4f}  adj={h['adjusted_p']:.4f}  {sig}")
    print("    NOTE: Row-level McNemar ignores clustering; results are anti-conservative.")

    # ── Summary table ──
    print("\n" + "=" * 80)
    print("SUMMARY TABLE")
    print("=" * 80)
    print(
        f"  {'Arm':<18s} {'Acc':>6s} {'95% CI':>16s} {'Bal':>6s} "
        f"{'MF1':>6s} {'MCC':>6s} {'F-Acc':>6s} {'MV':>6s} "
        f"{'Abst':>6s} {'SelAcc':>6s} {'Cov':>6s} {'Agree':>6s}"
    )
    print("  " + "-" * 120)
    for arm in ARM_ORDER:
        a = report["arms"].get(arm)
        if not a:
            continue
        ci_str = f"[{a['accuracy_95ci'][0]:.3f}, {a['accuracy_95ci'][1]:.3f}]"
        print(
            f"  {arm:<18s} "
            f"{a['accuracy']:>6.3f} "
            f"{ci_str:>16s} "
            f"{a['balanced_accuracy']:>6.3f} "
            f"{a['macro_f1']:>6.3f} "
            f"{a['mcc']:>6.3f} "
            f"{a['fault_only_accuracy']:>6.3f} "
            f"{a['majority_vote_accuracy']:>6.3f} "
            f"{a['abstention_rate']:>6.3f} "
            f"{a['selective_accuracy']:>6.3f} "
            f"{a['coverage']:>6.3f} "
            f"{a['repetition_agreement']:>6.3f}"
        )

    # Leave-one-class-out sensitivity
    print("\n  Leave-One-Class-Out Accuracy:")
    print(f"  {'Arm':<18s}", end="")
    for label in LABEL_SPACE:
        print(f" {'excl_' + label:>10s}", end="")
    print()
    print("  " + "-" * 72)
    for arm in ARM_ORDER:
        a = report["arms"].get(arm)
        if not a:
            continue
        loco = a.get("leave_one_class_out", {})
        print(f"  {arm:<18s}", end="")
        for label in LABEL_SPACE:
            val = loco.get(f"excl_{label}", 0)
            print(f" {val:>10.3f}", end="")
        print()

    # ── Phase B reference ──
    print("\n" + "─" * 40)
    print("PHASE B REFERENCE")
    print("─" * 40)
    print("  Phase B Condition A (isolated): ~56% accuracy (single-fault specialist, 2 labels)")
    print("  Phase B Condition B (FoT):      ~86% accuracy (with peer insights, 2 labels)")
    print("  CAVEAT: Phase B used 2-label per-agent classification; this ablation uses")
    print("  5-label centralized — a harder task.  The primary endpoint is the relative")
    print("  ranking between the four representation arms, NOT absolute comparison with Phase B.")

    # ── Write outputs ──
    if output_path is None:
        output_path = results_dir / "ablation_evaluation.json"
    with output_path.open("w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False, default=str)
    print(f"\nFull report saved to: {output_path}")

    md_path = results_dir / "ablation_report.md"
    write_markdown_report(report, md_path)
    print(f"Markdown report saved to: {md_path}")

    return report


# ── Markdown report ─────────────────────────────────────────────────


def write_markdown_report(report: dict[str, Any], path: Path) -> None:
    """Generate a publication-ready markdown report (v2: cluster-aware)."""
    lines = [
        "# Ablation Experiment: TS→Text Representation Comparison",
        "",
        "## Experiment Design",
        "",
        "Four representation arms tested on 15 held-out TEP cases (PBH-001..PBH-015),",
        "5-class centralized classification (F1, F8, F10, F13, Normal),",
        "GPT-5.6-terra with structured output, 3 repetitions per arm × case = 180 total inferences.",
        "",
        "**Independent units:** 15 case_ids (not 45 replicate rows).  All cluster-aware tests",
        "operate at the case level.  Three repetitions per case measure within-case stability",
        "but do not add independent statistical units.",
        "",
        "**Statistical tests (all cluster-aware):**",
        "- Clustered bootstrap (10,000 resamples of 15 case_ids, independent RNG per comparison)",
        "- Exact sign-flip permutation test (2^15 = 32,768 permutations, per-case accuracy differences)",
        "- McNemar at case level (majority-vote aggregated binary outcomes, N = 15, exact binomial)",
        "- Holm–Bonferroni step-down correction across 6 pairwise comparisons",
        "",
        "**Note:** Row-level McNemar (N = 45) is retained for reference only and labeled",
        "NON-INFERENTIAL.  It treats replicate predictions as independent, which they are not",
        "(same input), yielding anti-conservative p-values.",
        "",
        "| Arm | Description |",
        "|-----|-------------|",
        "| V2_TEXT | Conformal verbalizer (Phase A/B baseline): 8 windows × 5 features "
        "per XMEAS, natural language with domain knowledge (thresholds, temporal trends) |",
        "| RAW_FEATURES | LLMTime-style direct numerical serialization of V2 features |",
        "| CGTIME_STATS | CGTime-inspired statistical baseline (adapted subset of "
        "Feng et al. 2026): 3-family summary, window-aligned |",
        "| SAX_SYMBOLIC | Symbolic Aggregate approXimation encoding (alphabet=5, word=10), "
        "baseline-relative Z-norm |",
        "",
        "## Results Summary",
        "",
        "| Arm | Accuracy | 95% CI | Bal. Acc | Macro-F1 | MCC | "
        "Fault-Only | MV Acc | Abstain | Sel. Acc | Coverage | Agreement |",
        "|-----|----------|--------|---------|----------|-----|"
        "-----------|--------|---------|----------|----------|-----------|",
    ]

    for arm in ARM_ORDER:
        a = report["arms"].get(arm)
        if not a:
            continue
        lines.append(
            f"| {arm} | {a['accuracy']:.3f} | "
            f"[{a['accuracy_95ci'][0]:.3f}, {a['accuracy_95ci'][1]:.3f}] | "
            f"{a['balanced_accuracy']:.3f} | "
            f"{a['macro_f1']:.3f} | "
            f"{a['mcc']:.3f} | "
            f"{a['fault_only_accuracy']:.3f} | "
            f"{a['majority_vote_accuracy']:.3f} | "
            f"{a['abstention_rate']:.3f} | "
            f"{a.get('selective_accuracy', 0):.3f} | "
            f"{a.get('coverage', 0):.3f} | "
            f"{a['repetition_agreement']:.3f} |"
        )

    lines += [
        "",
        "## Per-Class Recall",
        "",
        "| Arm | F1 | F8 | F10 | F13 | Normal |",
        "|-----|----|----|-----|-----|--------|",
    ]
    for arm in ARM_ORDER:
        a = report["arms"].get(arm)
        if not a:
            continue
        r = a["per_class_recall"]
        lines.append(
            f"| {arm} | {r.get('F1', 0):.3f} | {r.get('F8', 0):.3f} | "
            f"{r.get('F10', 0):.3f} | {r.get('F13', 0):.3f} | "
            f"{r.get('Normal', 0):.3f} |"
        )

    # Leave-one-class-out
    lines += [
        "",
        "## Leave-One-Class-Out Accuracy (Sensitivity Analysis)",
        "",
        "| Arm | excl. F1 | excl. F8 | excl. F10 | excl. F13 | excl. Normal |",
        "|-----|----------|----------|-----------|-----------|--------------|",
    ]
    for arm in ARM_ORDER:
        a = report["arms"].get(arm)
        if not a:
            continue
        loco = a.get("leave_one_class_out", {})
        lines.append(
            f"| {arm} | "
            f"{loco.get('excl_F1', 0):.3f} | "
            f"{loco.get('excl_F8', 0):.3f} | "
            f"{loco.get('excl_F10', 0):.3f} | "
            f"{loco.get('excl_F13', 0):.3f} | "
            f"{loco.get('excl_Normal', 0):.3f} |"
        )

    # Pairwise: cluster-aware tests (primary)
    lines += [
        "",
        "## Pairwise Statistical Comparisons (Cluster-Aware — Primary Inference)",
        "",
        "| Comparison | Δ Accuracy | 95% CI (boot) | p (boot) | "
        "p (perm) | p (McN-case) |",
        "|------------|-----------|---------------|----------|"
        "----------|--------------|",
    ]

    for pair_name, data in report.get("pairwise", {}).items():
        d = data["bootstrap_diff"]
        perm = data.get("permutation_test", {})
        mcn_case = data.get("mcnemar_case_level", {})
        lines.append(
            f"| {pair_name} | {d['point']:+.3f} | "
            f"[{d['lower']:.3f}, {d['upper']:.3f}] | "
            f"{d['p_value']:.4f} | "
            f"{perm.get('p_value', 1.0):.4f} | "
            f"{mcn_case.get('p_value', 1.0):.4f} |"
        )

    # Holm-Bonferroni for cluster-aware tests
    lines += [
        "",
        "### Holm–Bonferroni Correction (Clustered Bootstrap)",
        "",
        "| Comparison | Raw p | Adjusted p | Significant? |",
        "|------------|-------|------------|-------------|",
    ]
    for h in report.get("holm_bonferroni", {}).get("bootstrap", []):
        sig = "Yes" if h["significant"] else "No"
        name = h["name"].replace("boot:", "")
        lines.append(
            f"| {name} | {h['raw_p']:.4f} | {h['adjusted_p']:.4f} | "
            f"{'**' + sig + '**' if h['significant'] else sig} |"
        )

    lines += [
        "",
        "### Holm–Bonferroni Correction (Permutation Test)",
        "",
        "| Comparison | Raw p | Adjusted p | Significant? |",
        "|------------|-------|------------|-------------|",
    ]
    for h in report.get("holm_bonferroni", {}).get("permutation_test", []):
        sig = "Yes" if h["significant"] else "No"
        name = h["name"].replace("perm:", "")
        lines.append(
            f"| {name} | {h['raw_p']:.4f} | {h['adjusted_p']:.4f} | "
            f"{'**' + sig + '**' if h['significant'] else sig} |"
        )

    lines += [
        "",
        "### Holm–Bonferroni Correction (McNemar Case-Level, N=15)",
        "",
        "| Comparison | Raw p | Adjusted p | Significant? |",
        "|------------|-------|------------|-------------|",
    ]
    for h in report.get("holm_bonferroni", {}).get("mcnemar_case_level", []):
        sig = "Yes" if h["significant"] else "No"
        name = h["name"].replace("mcn_case:", "")
        lines.append(
            f"| {name} | {h['raw_p']:.4f} | {h['adjusted_p']:.4f} | "
            f"{'**' + sig + '**' if h['significant'] else sig} |"
        )

    # Row-level McNemar (reference only)
    lines += [
        "",
        "### Row-Level McNemar (NON-INFERENTIAL — Reference Only)",
        "",
        "> **Warning:** These results treat 45 replicate predictions as independent",
        "> observations.  Since each case_id contributes 3 non-independent predictions",
        "> (same input), these p-values are anti-conservative and should NOT be used",
        "> for inferential conclusions.",
        "",
        "| Comparison | Raw p | Adjusted p | Significant? |",
        "|------------|-------|------------|-------------|",
    ]
    for h in report.get("holm_bonferroni", {}).get(
        "mcnemar_row_level_NON_INFERENTIAL", []
    ):
        sig = "Yes" if h["significant"] else "No"
        name = h["name"].replace("mcn_row:", "")
        lines.append(
            f"| {name} | {h['raw_p']:.4f} | {h['adjusted_p']:.4f} | {sig} |"
        )

    # Confusion matrices
    lines += [
        "",
        "## Confusion Matrices",
        "",
    ]
    for arm in ARM_ORDER:
        a = report["arms"].get(arm)
        if not a:
            continue
        cm = a["confusion_matrix"]
        labels = LABEL_SPACE + ["ABSTAIN"]
        lines.append(f"### {arm}")
        lines.append("")
        header = "| True \\ Pred | " + " | ".join(labels) + " |"
        sep = "|" + "|".join(["---"] * (len(labels) + 1)) + "|"
        lines.append(header)
        lines.append(sep)
        for true in LABEL_SPACE:
            row = (
                f"| {true} | "
                + " | ".join(str(cm[true].get(p, 0)) for p in labels)
                + " |"
            )
            lines.append(row)
        lines.append("")

    # Conclusions (corrected per review findings R3, R8, R10)
    lines += [
        "## Conclusions",
        "",
        "### Corrected interpretations (post external review)",
        "",
        "1. **V2_TEXT, RAW_FEATURES, and CGTIME_STATS: not demonstrably different.**",
        "   No pairwise comparison among these three arms reaches statistical significance",
        "   on any cluster-aware test after Holm–Bonferroni correction.  However, the",
        "   experiment has limited statistical power (N_eff = 15 independent cases;",
        "   MDE ≈ 0.25–0.30), so the absence of significance does not demonstrate",
        "   equivalence.  Moderate or small true differences cannot be excluded.",
        "",
        "2. **SAX_SYMBOLIC: descriptively inferior, significance test-dependent.**",
        "   SAX_SYMBOLIC shows the lowest observed accuracy (0.733 vs 0.889–0.933).",
        "   Row-level McNemar (N = 45, non-cluster-aware) found significance for",
        "   RAW vs SAX and CGTIME vs SAX, but this test ignores clustering and its",
        "   p-values are anti-conservative.  Cluster-aware tests (permutation test,",
        "   case-level McNemar, clustered bootstrap) should be consulted for",
        "   inferential conclusions; with N = 15 independent cases, their power is",
        "   limited.  The descriptive pattern is strong but formal confirmation",
        "   requires a larger sample.",
        "",
        "3. **F13 is a difficult class, but not uniformly the hardest.**",
        "   F13 (slow drift) shows low recall across all arms (0.333–0.778),",
        "   concentrated in abstentions (RAW, CGTIME, SAX) or F8 misclassification",
        "   (V2_TEXT).  However, V2_TEXT shows lower recall for F8 (0.667) than F13",
        "   (0.778), and SAX_SYMBOLIC ties F13 and Normal at 0.333.  The pattern is",
        "   arm-dependent, not universal.",
        "",
        "4. **V2_TEXT offers the best observed cost–accuracy trade-off.**",
        "   V2_TEXT uses ~1/39× the tokens of RAW_FEATURES and ~1/180× of CGTIME_STATS",
        "   while achieving comparable observed accuracy.  This advantage includes",
        "   pre-computed domain knowledge (conformal thresholds, temporal trend",
        "   descriptions) whose preprocessing cost is external to the prompt token",
        "   budget and should be accounted for separately.",
        "",
        "5. **Results are limited in scope.**",
        "   This experiment covers 4 of 28 TEP fault types, one simulation mode,",
        "   one LLM (GPT-5.6-terra), and a centralised 5-class classification task",
        "   (not the production federated 2-class architecture).  The ranking may",
        "   differ for other faults (especially those with subtle multivariate",
        "   signatures), other LLMs, or the production pipeline configuration.",
        "",
        "### Caveats",
        "",
        "- **Information–representation confound:** V2_TEXT embeds domain knowledge",
        "  (thresholds, trend descriptions); RAW_FEATURES uses derived features;",
        "  CGTIME and SAX operate closer to raw sensor data.  The experiment tests",
        "  the combined effect of representation format and information content,",
        "  not format alone.",
        "- **Selective accuracy caveat:** RAW_FEATURES and CGTIME_STATS achieve",
        "  selective accuracy = 1.000, but this is conditioned on non-abstention",
        "  (coverage 0.933 and 0.911 respectively).  Selective accuracy does not",
        "  substitute for overall accuracy, coverage, or selective risk; the high",
        "  values indicate that errors in these arms are exclusively abstentions",
        "  on F13, not misclassifications.",
        "- **Prompt-length confound:** CGTIME_STATS uses ~180× more tokens than",
        "  V2_TEXT.  Comparable accuracy could reflect offsetting effects of richer",
        "  information and attention dilution.",
        "- **Statistical power:** with 15 independent cases, only large effects",
        "  (Δ ≥ 0.25) are reliably detectable.  Additional independent cases are",
        "  needed to resolve finer differences.",
    ]

    # Statistical notes
    lines += [
        "",
        "## Statistical Notes",
        "",
        "- **Accuracy:** abstentions count as incorrect predictions.",
        "- **Selective accuracy:** accuracy among non-abstained predictions only.",
        "- **Coverage:** fraction of non-abstained predictions (= 1 − abstention rate).",
        "- **Balanced accuracy:** mean of per-class recalls.",
        "- **Macro-F1:** unweighted mean of per-class F1 scores.",
        "- **MCC:** Matthews correlation coefficient (multi-class, Gorodkin 2004); "
        "ranges from −1 to +1.",
        "- **Fault-Only Accuracy:** excludes Normal cases.",
        "- **Majority Vote:** requires ≥ ceil(R/2) concordant votes; otherwise "
        "no-majority (counted wrong).",
        "- **Agreement:** fraction of cases where all 3 reps agree on the same label.",
        "- **Leave-One-Class-Out:** accuracy when excluding each class in turn; "
        "shows sensitivity to individual classes.",
        "- **Bootstrap CIs:** 10,000 resamples, seed=42, clustered by case_id "
        "(15 independent units).",
        "- **Permutation test:** exact sign-flip test on per-case accuracy "
        "differences (2^15 = 32,768 permutations); cluster-aware.",
        "- **McNemar case-level:** exact binomial on majority-vote aggregated "
        "binary outcomes per case (N = 15); cluster-aware.",
        "- **McNemar row-level (NON-INFERENTIAL):** exact binomial on 45 "
        "prediction pairs; ignores clustering, anti-conservative; "
        "retained for reference only.",
        "- **Holm–Bonferroni:** step-down correction across 6 pairwise comparisons.",
        "",
        "## Phase B Reference",
        "",
        "Phase B used per-agent 2-label classification (specialist + Normal) with "
        "federated peer insights.",
        "Condition A (isolated): ~56% accuracy. Condition B (FoT): ~86% accuracy.",
        "This ablation uses 5-label centralized classification — a harder task — "
        "so direct numerical comparison is **not** the primary endpoint.",
        "The quantity of interest is the **relative ranking** between the four "
        "representation arms.",
    ]

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Evaluate ablation experiment results.")
    parser.add_argument(
        "results_dir",
        nargs="?",
        default="ablation_results",
        help="Directory containing inference_results.jsonl (default: ablation_results)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Path for JSON evaluation report (default: <results_dir>/ablation_evaluation.json)",
    )
    args = parser.parse_args()

    results_dir = Path(args.results_dir)
    output_path = Path(args.output) if args.output else None

    evaluate(results_dir, output_path)


if __name__ == "__main__":
    main()
