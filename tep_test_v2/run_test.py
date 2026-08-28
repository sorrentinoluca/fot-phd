#!/usr/bin/env python3
"""Run the final frozen V2 test evaluation without adapting V2."""
from __future__ import annotations

from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import sys
from typing import Any

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CODE = ROOT / "code"
sys.path.insert(0, str(CODE))
sys.path.insert(0, str(ROOT))

from evaluate_verbalizer_v2 import (  # noqa: E402
    FEATURE_SECTIONS,
    distribution,
    evaluate,
    jaccard,
    load_development_cases,
    signature_similarity,
)
from tep_features import analyze_case_windows, normalize_schema  # noqa: E402
from tep_validation_v2.run_validation import (  # noqa: E402
    fmt,
    grouped,
    record_from_structured,
    write_jsonl,
)
from tep_verbalize_v2 import (  # noqa: E402
    load_config,
    load_development_baseline,
    render_text,
    verbalize_feature_table,
)

OUT = ROOT / "tep_test_v2"
STRUCTURED_DIR = OUT / "cases" / "structured"
NORMAL_PATH = CODE / "tep_cache" / "mode1_normal_500.xlsx"
CONFIG_PATH = CODE / "verbalizer_config_v2.json"
ANALYSIS_DIR = CODE / "tep_analysis_v2"
VALIDATION_DIR = ROOT / "tep_validation_v2"
TOP_K = 4

CASE_METADATA = [
    {"case_id": "test_case_01", "class_label": "F1", "case_type": "fault", "fault": 1, "batch": 8},
    {"case_id": "test_case_02", "class_label": "F1", "case_type": "fault", "fault": 1, "batch": 9},
    {"case_id": "test_case_03", "class_label": "F1", "case_type": "fault", "fault": 1, "batch": 10},
    {"case_id": "test_case_04", "class_label": "F8", "case_type": "fault", "fault": 8, "batch": 8},
    {"case_id": "test_case_05", "class_label": "F8", "case_type": "fault", "fault": 8, "batch": 9},
    {"case_id": "test_case_06", "class_label": "F8", "case_type": "fault", "fault": 8, "batch": 10},
    {"case_id": "test_case_07", "class_label": "F10", "case_type": "fault", "fault": 10, "batch": 8},
    {"case_id": "test_case_08", "class_label": "F10", "case_type": "fault", "fault": 10, "batch": 9},
    {"case_id": "test_case_09", "class_label": "F10", "case_type": "fault", "fault": 10, "batch": 10},
    {"case_id": "test_case_10", "class_label": "F13", "case_type": "fault", "fault": 13, "batch": 8},
    {"case_id": "test_case_11", "class_label": "F13", "case_type": "fault", "fault": 13, "batch": 9},
    {"case_id": "test_case_12", "class_label": "F13", "case_type": "fault", "fault": 13, "batch": 10},
    {"case_id": "test_case_13", "class_label": "Normal", "case_type": "normal", "normal_block": "N8"},
    {"case_id": "test_case_14", "class_label": "Normal", "case_type": "normal", "normal_block": "N9"},
    {"case_id": "test_case_15", "class_label": "Normal", "case_type": "normal", "normal_block": "N10"},
]


def make_normal_cases(config: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], pd.DataFrame]:
    baseline = load_development_baseline(NORMAL_PATH, config)
    # Keep the header, skip exactly N1-N7 (21,000 data rows), and read only
    # N8-N10 (9,000 rows). No validation block is materialized here.
    raw = pd.read_excel(
        NORMAL_PATH,
        skiprows=range(1, 21_001),
        nrows=9_000,
    )
    test_normal = normalize_schema(raw, source="Normal N8-N10 bounded read")
    if (
        len(test_normal) != 9_000
        or float(test_normal.Time.min()) < 350.0
        or float(test_normal.Time.max()) >= 500.0
    ):
        raise RuntimeError("Bounded Normal test read is outside N8-N10")

    outputs: dict[str, dict[str, Any]] = {}
    feature_tables: list[pd.DataFrame] = []
    for case_id, block, start, end in [
        ("test_case_13", "N8", 350.0, 400.0),
        ("test_case_14", "N9", 400.0, 450.0),
        ("test_case_15", "N10", 450.0, 500.0),
    ]:
        data = test_normal[(test_normal.Time >= start) & (test_normal.Time < end)].copy()
        if len(data) != 3_000:
            raise RuntimeError(f"{block} has {len(data)} samples instead of 3000")
        features = analyze_case_windows(
            data, baseline, start_h=start, end_h=end,
            window_h=float(config["window_hours"]),
        )
        features.insert(0, "normal_block", block)
        feature_tables.append(features)
        result = verbalize_feature_table(features.drop(columns="normal_block"), config)
        outputs[case_id] = result["structured"]
        with (STRUCTURED_DIR / f"{case_id}.json").open("w", encoding="utf-8") as handle:
            json.dump(result["structured"], handle, indent=2, ensure_ascii=False)
            handle.write("\n")
    return outputs, pd.concat(feature_tables, ignore_index=True)


def normal_fpr(features: pd.DataFrame, config: dict[str, Any]) -> pd.DataFrame:
    t = config["thresholds"]
    d = features.copy()
    d["level"] = d.abs_shift_sigma > t["abs_shift_sigma"]
    d["trend"] = d.abs_slope_sigma_h > t["abs_slope_sigma_h"]
    d["residual"] = d.residual_std_ratio > t["residual_std_ratio"]
    d["diff"] = d.diff_std_ratio > t["diff_std_ratio"]
    d["rapid"] = d.residual & d["diff"]
    rows: list[dict[str, Any]] = []
    for scope, group in [*list(d.groupby("normal_block")), ("N8-N10", d)]:
        per_window = group.groupby(["window_start_h", "window_end_h"])[
            ["level", "trend", "residual", "diff", "rapid"]
        ].any()
        per_window["any-primary"] = per_window[
            ["level", "trend", "residual", "diff"]
        ].any(axis=1)
        for feature in ["level", "trend", "residual", "diff", "rapid", "any-primary"]:
            count, total = int(per_window[feature].sum()), int(len(per_window))
            rows.append({
                "scope": scope, "feature": feature,
                "positive_windows": count, "total_windows": total,
                "positive_fraction": count / total,
            })
    return pd.DataFrame(rows)


def load_validation_records() -> list[dict[str, Any]]:
    structures = {}
    with (VALIDATION_DIR / "validation_structured_signatures.jsonl").open(encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            structures[row["case_id"]] = row["structured"]
    metadata = [
        json.loads(line)
        for line in (VALIDATION_DIR / "validation_metadata.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    return [record_from_structured(meta, structures[meta["case_id"]]) for meta in metadata]


def pair_rows(
    test: list[dict[str, Any]], validation: list[dict[str, Any]],
    development: list[dict[str, Any]],
) -> pd.DataFrame:
    tg, vg, dg = grouped(test), grouped(validation), grouped(development)
    rows: list[dict[str, Any]] = []

    def add(kind: str, left: dict[str, Any], right: dict[str, Any]) -> None:
        rows.append({
            "comparison": kind,
            "left_class": left["class_label"], "right_class": right["class_label"],
            "left_case": left["case_id"], "right_case": right["case_id"],
            "similarity": signature_similarity(left["vector"], right["vector"]),
        })

    for cases in tg.values():
        for left, right in combinations(cases, 2):
            add("test_intra", left, right)
    for left_label, right_label in combinations(sorted(tg), 2):
        for left in tg[left_label]:
            for right in tg[right_label]:
                add("test_inter", left, right)
    for label in sorted(tg):
        for left in tg[label]:
            for right in dg[label]:
                add("test_to_development_same_class", left, right)
            for right in vg[label]:
                add("test_to_validation_same_class", left, right)
    return pd.DataFrame(rows)


def validation_pair_distribution(kind: str, label: str) -> dict[str, Any]:
    d = pd.read_csv(VALIDATION_DIR / "validation_pairwise_similarity.csv")
    if "__" in label:
        left, right = label.split("__")
        values = d[
            (d.comparison == kind) & (d.left_class == left) & (d.right_class == right)
        ].similarity.tolist()
    else:
        values = d[(d.comparison == kind) & (d.left_class == label)].similarity.tolist()
    return distribution(values)


def similarity_summary(
    pairs: pd.DataFrame, test_eval: dict[str, Any], validation_eval: dict[str, Any],
    development_eval: dict[str, Any],
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []

    def add(kind: str, label: str, values: list[float], dev: dict[str, Any] | None,
            val: dict[str, Any] | None) -> None:
        test_stats = distribution(values)
        row: dict[str, Any] = {"comparison": kind, "label": label}
        for prefix, stats in [("test", test_stats), ("development", dev), ("validation", val)]:
            for key in ["n", "median", "q1", "q3", "min", "max"]:
                row[f"{prefix}_{key}"] = None if stats is None else stats[key]
        rows.append(row)

    for label, dev in development_eval["intra_class_similarity"].items():
        values = pairs[(pairs.comparison == "test_intra") & (pairs.left_class == label)].similarity.tolist()
        add("test_intra", label, values, dev, validation_eval["intra_class_similarity"][label])
    for pair, dev in development_eval["inter_class_similarity"].items():
        left, right = pair.split("__")
        values = pairs[
            (pairs.comparison == "test_inter") & (pairs.left_class == left) & (pairs.right_class == right)
        ].similarity.tolist()
        add("test_inter", pair, values, dev, validation_eval["inter_class_similarity"][pair])
    for label, dev in development_eval["intra_class_similarity"].items():
        values = pairs[
            (pairs.comparison == "test_to_development_same_class") & (pairs.left_class == label)
        ].similarity.tolist()
        add(
            "test_to_development_same_class", label, values, dev,
            validation_pair_distribution("validation_to_development_same_class", label),
        )
        values = pairs[
            (pairs.comparison == "test_to_validation_same_class") & (pairs.left_class == label)
        ].similarity.tolist()
        add(
            "test_to_validation_same_class", label, values, dev,
            validation_eval["intra_class_similarity"][label],
        )
    for label, value in test_eval["separation_margin"]["values"].items():
        rows.append({
            "comparison": "margin", "label": label,
            "test_n": 1, "test_median": value, "test_q1": value, "test_q3": value,
            "test_min": value, "test_max": value,
            "development_median": development_eval["separation_margin"]["values"][label],
            "validation_median": validation_eval["separation_margin"]["values"][label],
        })
    return pd.DataFrame(rows)


def topk_and_recurrence(
    test: list[dict[str, Any]], validation_eval: dict[str, Any],
    development_eval: dict[str, Any],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    tg = grouped(test)
    j_rows: list[dict[str, Any]] = []
    r_rows: list[dict[str, Any]] = []
    val_recurrence = pd.read_csv(VALIDATION_DIR / "validation_variable_recurrence.csv")
    for label, cases in tg.items():
        for feature in FEATURE_SECTIONS:
            sets = [set(case["dominant"][feature][:TOP_K]) for case in cases]
            raw = [jaccard(a, b) for a, b in combinations(sets, 2)]
            stats = distribution([value for value in raw if value is not None])
            dev = development_eval["dominant_variable_stability"][label][feature]["pairwise_jaccard"]
            val = validation_eval["dominant_variable_stability"][label][feature]["pairwise_jaccard"]
            j_rows.append({
                "class_label": label, "feature": feature, "top_k": TOP_K,
                "test_n": stats["n"], "test_median": stats["median"],
                "test_q1": stats["q1"], "test_q3": stats["q3"],
                "test_min": stats["min"], "test_max": stats["max"],
                "test_undefined_empty_union_pairs": sum(value is None for value in raw),
                "development_median": dev["median"], "development_q1": dev["q1"],
                "development_q3": dev["q3"], "development_min": dev["min"],
                "development_max": dev["max"],
                "validation_median": val["median"], "validation_min": val["min"],
                "validation_max": val["max"],
            })
            recurrence = Counter(name for values in sets for name in values)
            dev_rec = development_eval["dominant_variable_stability"][label][feature]["recurrence"]
            val_rows = val_recurrence[
                (val_recurrence.class_label == label) & (val_recurrence.feature == feature)
            ]
            val_rec = dict(zip(val_rows.variable, val_rows.validation_count))
            for variable in sorted(set(recurrence) | set(dev_rec) | set(val_rec)):
                r_rows.append({
                    "class_label": label, "feature": feature, "variable": variable,
                    "test_count": recurrence.get(variable, 0), "test_cases": 3,
                    "validation_count": val_rec.get(variable, 0), "validation_cases": 2,
                    "development_count": dev_rec.get(variable, 0), "development_cases": 5,
                })
    return pd.DataFrame(j_rows), pd.DataFrame(r_rows)


def split_comparison(
    test: list[dict[str, Any]], validation: list[dict[str, Any]],
    development: list[dict[str, Any]], summary: pd.DataFrame,
    jaccard_df: pd.DataFrame,
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for label in sorted(grouped(test)):
        for metric, comparison in [
            ("intra_similarity", "test_intra"),
            ("same_class_similarity_to_development", "test_to_development_same_class"),
            ("margin", "margin"),
        ]:
            r = summary[(summary.comparison == comparison) & (summary.label == label)].iloc[0]
            rows.append({
                "class_label": label, "metric": metric,
                "development": r.development_median,
                "validation": r.validation_median,
                "test": r.test_median,
            })
        for feature in FEATURE_SECTIONS:
            r = jaccard_df[
                (jaccard_df.class_label == label) & (jaccard_df.feature == feature)
            ].iloc[0]
            rows.append({
                "class_label": label, "metric": f"top4_jaccard_{feature}",
                "development": r.development_median,
                "validation": r.validation_median,
                "test": r.test_median,
            })
        for feature in FEATURE_SECTIONS:
            values = {}
            for split, records in [
                ("development", development), ("validation", validation), ("test", test)
            ]:
                subset = [r for r in records if r["class_label"] == label]
                values[split] = float(np.median([
                    r["structured"]["system_summary"]["window_activity"][feature]["active_fraction"]
                    for r in subset
                ]))
            rows.append({
                "class_label": label, "metric": f"system_active_fraction_{feature}",
                **values,
            })
    return pd.DataFrame(rows)


def report_text(
    test: list[dict[str, Any]], fpr: pd.DataFrame, summary: pd.DataFrame,
    jaccard_df: pd.DataFrame, recurrence_df: pd.DataFrame,
    split_df: pd.DataFrame,
) -> str:
    metadata = {row["case_id"]: row for row in CASE_METADATA}
    lines = [
        "# Verbalizer V2 final test report", "",
        "## Frozen protocol", "",
        "- Freeze commit: `3fd960a192bafacbaabce9471e3c3614d6b2d2db`.",
        "- Validation commit: `1d9c1617b56c19d2bc71dfef7b7902df0670b537`.",
        "- Frozen config, features, renderer, evaluator, thresholds, `top_k=4`, and similarity were unchanged.",
        "- Test data: F1/F8/F10/F13 batches 8–10 and Normal N8–N10 only.",
        "- No retrospective pass/fail threshold is used.",
        "", "## Normal N8–N10", "",
        "| Scope | Feature | Positive windows | Fraction |", "|---|---|---:|---:|",
    ]
    for row in fpr.itertuples(index=False):
        lines.append(
            f"| {row.scope} | {row.feature} | {row.positive_windows}/{row.total_windows} | {row.positive_fraction:.1%} |"
        )

    lines += ["", "## Similarities and margins", "",
              "| Comparison | Label | Development | Validation | Test median [Q1, Q3] | Test range |",
              "|---|---|---:|---:|---:|---:|"]
    for row in summary.itertuples(index=False):
        lines.append(
            f"| {row.comparison} | {row.label} | {fmt(getattr(row, 'development_median', None))} "
            f"| {fmt(getattr(row, 'validation_median', None))} "
            f"| {fmt(row.test_median)} [{fmt(row.test_q1)}, {fmt(row.test_q3)}] "
            f"| {fmt(row.test_min)}–{fmt(row.test_max)} |"
        )

    lines += ["", "## Test temporal evidence", "",
              "Tables report frozen structured counts without assigning mechanisms.", ""]
    for label in ["F1", "F8", "F10", "F13"]:
        lines += [f"### {label}", ""]
        for record in [r for r in test if r["class_label"] == label]:
            meta = metadata[record["case_id"]]
            s = record["structured"]
            lines += [f"#### Batch {meta['batch']} (`{record['case_id']}`)", "",
                      "| Feature | Active | Fraction | Initial | Late | Dominant top-4 |",
                      "|---|---:|---:|---:|---:|---|"]
            for feature in FEATURE_SECTIONS:
                a = s["system_summary"]["window_activity"][feature]
                dominant = ", ".join(record["dominant"][feature][:TOP_K]) or "none"
                lines.append(
                    f"| {feature} | {a['n_active_windows']}/{s['n_windows']} | {a['active_fraction']:.3f} "
                    f"| {a['initial_active_windows']} | {a['late_active_windows']} | {dominant} |"
                )
            lines.append("")

    lines += ["## Top-4 Jaccard across splits", "",
              "| Class | Feature | Development median | Validation | Test median [range] |",
              "|---|---|---:|---:|---:|"]
    for row in jaccard_df.itertuples(index=False):
        lines.append(
            f"| {row.class_label} | {row.feature} | {fmt(row.development_median)} "
            f"| {fmt(row.validation_median)} | {fmt(row.test_median)} "
            f"[{fmt(row.test_min)}, {fmt(row.test_max)}] |"
        )

    lines += ["", "## Dominant-variable recurrence", "",
              "Full counts are stored in `test_variable_recurrence.csv`. Variables present in all three test top-4 sets:", ""]
    for (label, feature), group in recurrence_df[recurrence_df.test_count == 3].groupby(["class_label", "feature"]):
        values = ", ".join(
            f"{r.variable} (validation {r.validation_count}/2; development {r.development_count}/5)"
            for r in group.itertuples(index=False)
        )
        lines.append(f"- {label} / {feature}: {values}")

    lines += ["", "## Development–validation–test comparison", "",
              "| Class | Metric | Development | Validation | Test |",
              "|---|---|---:|---:|---:|"]
    for row in split_df.itertuples(index=False):
        lines.append(
            f"| {row.class_label} | {row.metric} | {fmt(row.development)} | {fmt(row.validation)} | {fmt(row.test)} |"
        )

    lines += ["", "## Final descriptive verdict", "",
              "This section is completed after inspecting the frozen outputs. No retrospective threshold is introduced.", ""]
    return "\n".join(lines)


def main() -> None:
    config = load_config(CONFIG_PATH)
    normal_outputs, normal_features = make_normal_cases(config)

    structured: dict[str, dict[str, Any]] = {}
    for meta in CASE_METADATA:
        case_id = meta["case_id"]
        if case_id in normal_outputs:
            structured[case_id] = normal_outputs[case_id]
        else:
            with (STRUCTURED_DIR / f"{case_id}.json").open(encoding="utf-8") as handle:
                structured[case_id] = json.load(handle)

    write_jsonl(
        OUT / "test_structured_signatures.jsonl",
        [{"case_id": case_id, "structured": structured[case_id]} for case_id in sorted(structured)],
    )
    with (OUT / "test_neutral_text.txt").open("w", encoding="utf-8") as handle:
        for case_id in sorted(structured):
            handle.write(f"=== {case_id} ===\n{render_text(structured[case_id])}\n\n")
    write_jsonl(OUT / "test_metadata.jsonl", CASE_METADATA)

    fpr = normal_fpr(normal_features, config)
    fpr.to_csv(OUT / "test_normal_fpr.csv", index=False)

    test_records = [record_from_structured(meta, structured[meta["case_id"]]) for meta in CASE_METADATA]
    validation_records = load_validation_records()
    development_records = load_development_cases(ANALYSIS_DIR, config)
    test_eval = evaluate(test_records, top_k=TOP_K)
    validation_eval = evaluate(validation_records, top_k=TOP_K)
    development_eval = evaluate(development_records, top_k=TOP_K)

    pairs = pair_rows(test_records, validation_records, development_records)
    pairs.to_csv(OUT / "test_pairwise_similarity.csv", index=False)
    summary = similarity_summary(pairs, test_eval, validation_eval, development_eval)
    summary.to_csv(OUT / "test_similarity_summary.csv", index=False)
    jaccard_df, recurrence_df = topk_and_recurrence(test_records, validation_eval, development_eval)
    jaccard_df.to_csv(OUT / "test_topk_jaccard.csv", index=False)
    recurrence_df.to_csv(OUT / "test_variable_recurrence.csv", index=False)
    split_df = split_comparison(
        test_records, validation_records, development_records, summary, jaccard_df
    )
    split_df.to_csv(OUT / "test_split_comparison.csv", index=False)

    with (OUT / "test_evaluator_metrics.json").open("w", encoding="utf-8") as handle:
        json.dump({
            "note": "Metric sections computed by frozen evaluate(); static development-only scope metadata omitted.",
            "top_k": TOP_K, "similarity": "1 - mean(abs(a-b))",
            "intra_class_similarity": test_eval["intra_class_similarity"],
            "inter_class_similarity": test_eval["inter_class_similarity"],
            "separation_margin": test_eval["separation_margin"],
            "dominant_variable_stability": test_eval["dominant_variable_stability"],
        }, handle, indent=2, ensure_ascii=False)
        handle.write("\n")

    report = report_text(test_records, fpr, summary, jaccard_df, recurrence_df, split_df)
    (OUT / "test_report.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
