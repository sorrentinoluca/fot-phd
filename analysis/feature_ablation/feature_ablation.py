#!/usr/bin/env python3
"""Leave-one-feature-out ablation of the frozen V2 structured signature.

Question answered: does each of the four primary features contribute to
class separability of the structured representation?

Scope guarantees (enforced, not merely documented):
- reads only code/tep_analysis_v2/ development tables (Normal N1-N5, fault
  batches 1-5); the loader in evaluate_verbalizer_v2 raises if anything else
  appears;
- uses the frozen verbalizer_config_v2.json thresholds unchanged;
- creates no classifier, no learned weight, no prototype;
- changes nothing under ablation/, phase_b/, icl/, reproducibility/ or any
  tep_*_v2/ directory.

What is ablated is the *evaluator signature*, not the rendered text. The
endpoint is separability of the structured representation on development data,
not LLM diagnostic accuracy.
"""
from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path
import sys

import numpy as np

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "code"))

from evaluate_verbalizer_v2 import (  # noqa: E402
    load_development_cases,
    signature_similarity,
)
from tep_verbalize_v2 import load_config  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent
SEED = 20260911
N_PERM = 100_000

# Component offsets inside the frozen 17-component per-XMEAS block.
# Order is fixed by signature_vector() in evaluate_verbalizer_v2.py.
BLOCKS = {
    "level": [0, 1, 2, 3],      # shift_sigma
    "trend": [4, 5, 6, 7],      # slope_sigma_h
    "residual": [8, 9, 10],     # residual_std_ratio
    "diff": [11, 12, 13],       # diff_std_ratio
    "rapid": [14, 15, 16],      # derived: residual AND diff jointly active
}
BLOCK_WIDTH = 17

# Two removal policies, reported side by side.
#  coherent: `rapid` is derived from residual AND diff, so it is not computable
#            once a parent is removed; it is removed with the parent.
#  isolated: only the family's own components are removed; `rapid` is kept.
#            Confounded by construction, reported to show the coupling is not
#            what drives the result.
ARMS = [
    ("FULL", [], "reference: all 17 components"),
    ("drop_level", ["level"], "coherent: remove shift_sigma"),
    ("drop_trend", ["trend"], "coherent: remove slope_sigma_h"),
    ("drop_residual", ["residual", "rapid"], "coherent: remove residual_std_ratio and its derived rapid"),
    ("drop_diff", ["diff", "rapid"], "coherent: remove diff_std_ratio and its derived rapid"),
    ("drop_residual_only", ["residual"], "isolated: remove residual_std_ratio, keep rapid"),
    ("drop_diff_only", ["diff"], "isolated: remove diff_std_ratio, keep rapid"),
    ("drop_rapid", ["rapid"], "reference: remove only the derived feature"),
    ("keep_only_level", ["trend", "residual", "diff", "rapid"], "keep-only: shift_sigma alone"),
    ("keep_only_trend", ["level", "residual", "diff", "rapid"], "keep-only: slope_sigma_h alone"),
    ("keep_only_residual", ["level", "trend", "diff", "rapid"], "keep-only: residual_std_ratio alone"),
    ("keep_only_diff", ["level", "trend", "residual", "rapid"], "keep-only: diff_std_ratio alone"),
    ("keep_only_location", ["residual", "diff", "rapid"], "keep-only: location block (level+trend)"),
    ("keep_only_variability", ["level", "trend"], "keep-only: variability block (residual+diff+rapid)"),
]


def mask_for(dropped: list[str], n_variables: int) -> np.ndarray:
    keep = np.ones(BLOCK_WIDTH, dtype=bool)
    for family in dropped:
        keep[BLOCKS[family]] = False
    return np.tile(keep, n_variables)


def similarity_matrix(vectors: np.ndarray) -> np.ndarray:
    n = len(vectors)
    sim = np.zeros((n, n), dtype=float)
    for i, j in combinations(range(n), 2):
        s = signature_similarity(vectors[i], vectors[j])
        sim[i, j] = sim[j, i] = s
    np.fill_diagonal(sim, np.nan)
    return sim


def per_case_margin(sim: np.ndarray, labels: np.ndarray) -> np.ndarray:
    """Within-class median similarity minus best between-class median."""
    classes = np.unique(labels)
    margins = np.empty(len(labels), dtype=float)
    for i in range(len(labels)):
        own = labels[i]
        same = [sim[i, j] for j in range(len(labels)) if j != i and labels[j] == own]
        best_other = max(
            float(np.median([sim[i, j] for j in range(len(labels)) if labels[j] == c]))
            for c in classes
            if c != own
        )
        margins[i] = float(np.median(same)) - best_other
    return margins


def class_level_margins(sim: np.ndarray, labels: np.ndarray) -> dict[str, float]:
    """Reproduces the frozen evaluator's separation_margin definition."""
    classes = sorted(set(labels.tolist()))
    intra = {}
    for c in classes:
        idx = [i for i, l in enumerate(labels) if l == c]
        intra[c] = float(np.median([sim[i, j] for i, j in combinations(idx, 2)]))
    out = {}
    for c in classes:
        idx_c = [i for i, l in enumerate(labels) if l == c]
        betweens = []
        for d in classes:
            if d == c:
                continue
            idx_d = [i for i, l in enumerate(labels) if l == d]
            betweens.append(float(np.median([sim[i, j] for i in idx_c for j in idx_d])))
        out[c] = intra[c] - max(betweens)
    return out


def loo_1nn_accuracy(sim: np.ndarray, labels: np.ndarray) -> tuple[float, list[str]]:
    preds = []
    for i in range(len(labels)):
        row = sim[i].copy()
        row[i] = -np.inf
        preds.append(labels[int(np.nanargmax(row))])
    correct = int(sum(p == t for p, t in zip(preds, labels)))
    return correct / len(labels), preds


def sign_flip_test(diff: np.ndarray, rng: np.random.Generator) -> dict[str, float]:
    """Exact-in-spirit paired permutation test: two-sided, sign-flip null."""
    observed = float(np.mean(diff))
    flips = rng.choice([-1.0, 1.0], size=(N_PERM, len(diff)))
    null = (flips * diff).mean(axis=1)
    p = float((np.abs(null) >= abs(observed) - 1e-15).mean())
    return {"mean_difference": observed, "p_two_sided": p, "n_permutations": N_PERM}


def main() -> None:
    config = load_config(str(REPO / "code" / "verbalizer_config_v2.json"))
    records = load_development_cases(REPO / "code" / "tep_analysis_v2", config)
    labels = np.array([r["class_label"] for r in records])
    case_ids = [f'{r["class_label"]}/{r["case_id"]}' for r in records]
    full_vectors = np.vstack([r["vector"] for r in records])
    n_variables = full_vectors.shape[1] // BLOCK_WIDTH
    assert full_vectors.shape[1] == n_variables * BLOCK_WIDTH

    rng = np.random.default_rng(SEED)
    results = {}
    baseline_margins = None

    for name, dropped, note in ARMS:
        mask = mask_for(dropped, n_variables)
        vectors = full_vectors[:, mask]
        sim = similarity_matrix(vectors)
        margins = per_case_margin(sim, labels)
        accuracy, preds = loo_1nn_accuracy(sim, labels)
        entry = {
            "dropped_families": dropped,
            "note": note,
            "components_per_variable": int(mask[:BLOCK_WIDTH].sum()),
            "components_total": int(mask.sum()),
            "mean_per_case_margin": float(np.mean(margins)),
            "median_per_case_margin": float(np.median(margins)),
            "min_per_case_margin": float(np.min(margins)),
            "n_cases_with_negative_margin": int((margins < 0).sum()),
            "loo_1nn_accuracy": accuracy,
            "loo_1nn_errors": [
                f"{case_ids[i]} -> {preds[i]}"
                for i in range(len(labels))
                if preds[i] != labels[i]
            ],
            "class_level_separation_margin": class_level_margins(sim, labels),
            "per_case_margin": {case_ids[i]: float(margins[i]) for i in range(len(labels))},
        }
        if name == "FULL":
            baseline_margins = margins
        else:
            delta = margins - baseline_margins
            entry["paired_vs_FULL"] = {
                "mean_margin_change": float(np.mean(delta)),
                "median_margin_change": float(np.median(delta)),
                "n_cases_degraded": int((delta < 0).sum()),
                "n_cases_improved": int((delta > 0).sum()),
                "n_cases_unchanged": int((delta == 0).sum()),
                **sign_flip_test(delta, rng),
            }
        results[name] = entry

    payload = {
        "scope": {
            "development_only": True,
            "normal_blocks": ["N1", "N2", "N3", "N4", "N5"],
            "fault_batches": [1, 2, 3, 4, 5],
            "classes": sorted(set(labels.tolist())),
            "n_cases": int(len(labels)),
            "validation_or_test_data_used": False,
            "thresholds": "frozen verbalizer_config_v2.json, unchanged",
            "learned_parameters": False,
        },
        "method": {
            "signature": f"{n_variables} XMEAS x {BLOCK_WIDTH} components",
            "similarity": "1 - mean absolute component difference (mean, so arms of "
                          "different dimensionality stay on the same scale)",
            "per_case_margin": "median similarity to same-class cases minus the best "
                               "between-class median similarity",
            "paired_test": "two-sided sign-flip permutation on per-case margin changes",
            "seed": SEED,
        },
        "arms": results,
    }
    (OUT_DIR / "feature_ablation_results.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    header = ("arm", "comps/var", "mean margin", "Δ vs FULL", "degraded/25", "p", "1NN LOO")
    print(f"{header[0]:<20}{header[1]:>10}{header[2]:>14}{header[3]:>12}{header[4]:>14}{header[5]:>9}{header[6]:>10}")
    for name, entry in results.items():
        paired = entry.get("paired_vs_FULL")
        d = f'{paired["mean_margin_change"]:+.5f}' if paired else "--"
        deg = f'{paired["n_cases_degraded"]}/25' if paired else "--"
        p = f'{paired["p_two_sided"]:.5f}' if paired else "--"
        print(
            f'{name:<20}{entry["components_per_variable"]:>10}'
            f'{entry["mean_per_case_margin"]:>14.5f}{d:>12}{deg:>14}{p:>9}'
            f'{entry["loo_1nn_accuracy"]:>10.3f}'
        )


if __name__ == "__main__":
    main()
