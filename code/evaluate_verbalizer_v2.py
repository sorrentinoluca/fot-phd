#!/usr/bin/env python3
"""Offline development-only evaluation of structured verbalizer V2 signatures.

True labels are used only to group pairwise stability/separability metrics. No
classifier, prompt, prototype, or learned weight is created here.
"""
from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from tep_features import XMEAS
from tep_verbalize_v2 import load_config, verbalize_feature_table

ROOT = Path(__file__).resolve().parent
DEFAULT_ANALYSIS = ROOT / "tep_analysis_v2"
FEATURE_SECTIONS = {
    "level": ("level", "longest_same_sign_run"),
    "trend": ("trend", "longest_same_sign_run"),
    "residual": ("residual_variability", "longest_run"),
    "diff": ("sample_to_sample_variation", "longest_run"),
    "rapid": ("rapid_variability", "longest_run"),
}


def signature_vector(structured: dict[str, Any]) -> np.ndarray:
    """Return a deterministic vector whose components all lie in [0, 1]."""
    n = structured["n_windows"]
    values: list[float] = []
    for variable in XMEAS:
        item = structured["variables"][variable]
        level = item["level"]
        trend = item["trend"]
        residual = item["residual_variability"]
        diff = item["sample_to_sample_variation"]
        rapid = item["rapid_variability"]
        signed_level = (level["positive_count"] - level["negative_count"]) / n
        signed_trend = (trend["positive_count"] - trend["negative_count"]) / n
        values.extend(
            [
                level["active_fraction"],
                (signed_level + 1.0) / 2.0,
                level["late_active_fraction"],
                level["longest_same_sign_run"] / n,
                trend["active_fraction"],
                (signed_trend + 1.0) / 2.0,
                trend["late_active_fraction"],
                trend["longest_same_sign_run"] / n,
                residual["active_fraction"],
                residual["late_active_fraction"],
                residual["longest_run"] / n,
                diff["active_fraction"],
                diff["late_active_fraction"],
                diff["longest_run"] / n,
                rapid["active_fraction"],
                rapid["late_active_fraction"],
                rapid["longest_run"] / n,
            ]
        )
    vector = np.asarray(values, dtype=float)
    if not np.all(np.isfinite(vector)) or np.any((vector < 0) | (vector > 1)):
        raise ValueError("Structured signature produced values outside [0, 1]")
    return vector


def signature_similarity(left: np.ndarray, right: np.ndarray) -> float:
    """Bounded similarity: one minus mean component-wise absolute distance."""
    if left.shape != right.shape:
        raise ValueError("Signature vectors must have the same shape")
    return float(1.0 - np.mean(np.abs(left - right)))


def jaccard(left: set[str], right: set[str]) -> float | None:
    union = left | right
    return float(len(left & right) / len(union)) if union else None


def distribution(values: list[float]) -> dict[str, float | int]:
    array = np.asarray(values, dtype=float)
    if len(array) == 0:
        return {"n": 0, "median": None, "q1": None, "q3": None, "min": None, "max": None}
    return {
        "n": len(array),
        "median": float(np.median(array)),
        "q1": float(np.quantile(array, 0.25)),
        "q3": float(np.quantile(array, 0.75)),
        "min": float(np.min(array)),
        "max": float(np.max(array)),
    }


def _case_record(
    class_label: str,
    case_id: str,
    feature_table: pd.DataFrame,
    config: dict[str, Any],
) -> dict[str, Any]:
    structured = verbalize_feature_table(feature_table, config)["structured"]
    return {
        "class_label": class_label,
        "case_id": case_id,
        "structured": structured,
        "vector": signature_vector(structured),
        "dominant": {
            feature: structured["system_summary"]["dominant_variables"][feature]
            for feature in FEATURE_SECTIONS
        },
    }


def load_development_cases(
    analysis_dir: str | Path = DEFAULT_ANALYSIS,
    config: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    cfg = load_config() if config is None else config
    analysis = Path(analysis_dir)
    normal = pd.read_csv(analysis / "normal_5h_variable_features.csv")
    faults = pd.read_csv(analysis / "development_window_features.csv")

    if set(normal.normal_block.unique()) != {"N1", "N2", "N3", "N4", "N5"}:
        raise RuntimeError("Evaluator accepts Normal N1-N5 only")
    if float(normal.window_end_h.max()) > 250.0:
        raise RuntimeError("Normal rows outside N1-N5 detected")
    if set(faults.batch.unique()) != {1, 2, 3, 4, 5}:
        raise RuntimeError("Evaluator accepts fault batches 1-5 only")
    if set(faults.fault.unique()) != {1, 8, 10, 13}:
        raise RuntimeError("Unexpected development fault set")

    records = []
    for block, group in normal.groupby("normal_block"):
        records.append(_case_record("Normal", str(block), group, cfg))
    for (fault, batch), group in faults.groupby(["fault", "batch"]):
        records.append(_case_record(f"F{int(fault)}", f"B{int(batch)}", group, cfg))
    return records


def evaluate(records: list[dict[str, Any]], top_k: int = 4) -> dict[str, Any]:
    classes = sorted({record["class_label"] for record in records})
    grouped = {
        label: [record for record in records if record["class_label"] == label]
        for label in classes
    }
    intra: dict[str, Any] = {}
    for label, cases in grouped.items():
        similarities = [
            signature_similarity(a["vector"], b["vector"])
            for a, b in combinations(cases, 2)
        ]
        intra[label] = distribution(similarities)

    inter: dict[str, Any] = {}
    for left_label, right_label in combinations(classes, 2):
        similarities = [
            signature_similarity(left["vector"], right["vector"])
            for left in grouped[left_label]
            for right in grouped[right_label]
        ]
        inter[f"{left_label}__{right_label}"] = distribution(similarities)

    margins = {}
    for label in classes:
        between_medians = [
            stats["median"]
            for pair, stats in inter.items()
            if label in pair.split("__")
        ]
        margins[label] = float(intra[label]["median"] - max(between_medians))

    dominant_stability: dict[str, Any] = {}
    for label, cases in grouped.items():
        dominant_stability[label] = {}
        for feature in FEATURE_SECTIONS:
            sets = [set(case["dominant"][feature][:top_k]) for case in cases]
            all_pairwise = [jaccard(a, b) for a, b in combinations(sets, 2)]
            pairwise = [value for value in all_pairwise if value is not None]
            recurrence = Counter(name for values in sets for name in values)
            dominant_stability[label][feature] = {
                "top_k": top_k,
                "pairwise_jaccard": distribution(pairwise),
                "undefined_empty_union_pairs": int(
                    sum(value is None for value in all_pairwise)
                ),
                "recurrence": dict(
                    sorted(recurrence.items(), key=lambda item: (-item[1], item[0]))
                ),
            }

    return {
        "scope": {
            "development_only": True,
            "normal_blocks": ["N1", "N2", "N3", "N4", "N5"],
            "fault_batches": [1, 2, 3, 4, 5],
            "classes": classes,
            "cases_per_class": {label: len(grouped[label]) for label in classes},
        },
        "representation": {
            "components_per_variable": 17,
            "variables": 41,
            "range": [0.0, 1.0],
            "similarity": "1 - mean absolute component difference",
            "learned_parameters": False,
        },
        "intra_class_similarity": intra,
        "inter_class_similarity": inter,
        "separation_margin": {
            "definition": "within-class median similarity minus highest between-class median similarity",
            "values": margins,
        },
        "dominant_variable_stability": dominant_stability,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--analysis-dir", default=str(DEFAULT_ANALYSIS))
    parser.add_argument("--config", default=str(ROOT / "verbalizer_config_v2.json"))
    parser.add_argument("--top-k", type=int, default=4)
    parser.add_argument("--output", help="optional JSON output path")
    args = parser.parse_args()
    config = load_config(args.config)
    result = evaluate(
        load_development_cases(args.analysis_dir, config), top_k=args.top_k
    )
    rendered = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
