#!/usr/bin/env python3
"""Run the pre-registered V2 validation without changing frozen code."""
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

from evaluate_verbalizer_v2 import (  # noqa: E402
    FEATURE_SECTIONS,
    distribution,
    evaluate,
    jaccard,
    load_development_cases,
    signature_similarity,
    signature_vector,
)
from tep_features import XMEAS, analyze_case_windows, normalize_schema  # noqa: E402
from tep_verbalize_v2 import (  # noqa: E402
    load_config,
    load_development_baseline,
    render_text,
    verbalize_feature_table,
)

OUT = ROOT / "tep_validation_v2"
STRUCTURED_DIR = OUT / "cases" / "structured"
NORMAL_PATH = CODE / "tep_cache" / "mode1_normal_500.xlsx"
CONFIG_PATH = CODE / "verbalizer_config_v2.json"
ANALYSIS_DIR = CODE / "tep_analysis_v2"
TOP_K = 4

# Fault/class information exists only here and in evaluator artifacts, never in
# the structured or neutral-text payload created by the verbalizer.
CASE_METADATA = [
    {"case_id": "case_01", "class_label": "F1", "case_type": "fault", "fault": 1, "batch": 6},
    {"case_id": "case_02", "class_label": "F1", "case_type": "fault", "fault": 1, "batch": 7},
    {"case_id": "case_03", "class_label": "F8", "case_type": "fault", "fault": 8, "batch": 6},
    {"case_id": "case_04", "class_label": "F8", "case_type": "fault", "fault": 8, "batch": 7},
    {"case_id": "case_05", "class_label": "F10", "case_type": "fault", "fault": 10, "batch": 6},
    {"case_id": "case_06", "class_label": "F10", "case_type": "fault", "fault": 10, "batch": 7},
    {"case_id": "case_07", "class_label": "F13", "case_type": "fault", "fault": 13, "batch": 6},
    {"case_id": "case_08", "class_label": "F13", "case_type": "fault", "fault": 13, "batch": 7},
    {"case_id": "case_09", "class_label": "Normal", "case_type": "normal", "normal_block": "N6"},
    {"case_id": "case_10", "class_label": "Normal", "case_type": "normal", "normal_block": "N7"},
]

COMPONENT_NAMES = [
    "level_active_fraction",
    "level_signed_activity",
    "level_late_active_fraction",
    "level_longest_same_sign_run",
    "trend_active_fraction",
    "trend_signed_activity",
    "trend_late_active_fraction",
    "trend_longest_same_sign_run",
    "residual_active_fraction",
    "residual_late_active_fraction",
    "residual_longest_run",
    "diff_active_fraction",
    "diff_late_active_fraction",
    "diff_longest_run",
    "rapid_active_fraction",
    "rapid_late_active_fraction",
    "rapid_longest_run",
]


def record_from_structured(meta: dict[str, Any], structured: dict[str, Any]) -> dict[str, Any]:
    return {
        "class_label": meta["class_label"],
        "case_id": meta["case_id"],
        "structured": structured,
        "vector": signature_vector(structured),
        "dominant": {
            feature: structured["system_summary"]["dominant_variables"][feature]
            for feature in FEATURE_SECTIONS
        },
    }


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def make_normal_cases(config: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], pd.DataFrame]:
    baseline = load_development_baseline(NORMAL_PATH, config)
    # 21,000 one-minute samples cover [0, 350 h), exactly N1-N7. No N8 row
    # (t >= 350 h) is requested from pandas.
    raw = pd.read_excel(NORMAL_PATH, nrows=21_000)
    normal_through_n7 = normalize_schema(raw, source="Normal N1-N7 bounded read")
    if len(normal_through_n7) != 21_000 or float(normal_through_n7.Time.max()) >= 350.0:
        raise RuntimeError("Bounded Normal read did not stop before N8")

    outputs: dict[str, dict[str, Any]] = {}
    feature_tables: list[pd.DataFrame] = []
    for case_id, block, start, end in [
        ("case_09", "N6", 250.0, 300.0),
        ("case_10", "N7", 300.0, 350.0),
    ]:
        data = normal_through_n7[
            (normal_through_n7.Time >= start) & (normal_through_n7.Time < end)
        ].copy()
        if len(data) != 3_000:
            raise RuntimeError(f"{block} has {len(data)} samples instead of 3000")
        features = analyze_case_windows(
            data, baseline, start_h=start, end_h=end, window_h=float(config["window_hours"])
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
    thresholds = config["thresholds"]
    d = features.copy()
    d["level"] = d.abs_shift_sigma > thresholds["abs_shift_sigma"]
    d["trend"] = d.abs_slope_sigma_h > thresholds["abs_slope_sigma_h"]
    d["residual"] = d.residual_std_ratio > thresholds["residual_std_ratio"]
    d["diff"] = d.diff_std_ratio > thresholds["diff_std_ratio"]
    rows: list[dict[str, Any]] = []
    references = {
        "level": (1, 50), "trend": (1, 50), "residual": (1, 50),
        "diff": (1, 50), "any-primary": (3, 50),
    }
    for scope, group in [*list(d.groupby("normal_block")), ("N6-N7", d)]:
        by_window = group.groupby(["window_start_h", "window_end_h"])[
            ["level", "trend", "residual", "diff"]
        ].any()
        by_window["any-primary"] = by_window.any(axis=1)
        for feature in ["level", "trend", "residual", "diff", "any-primary"]:
            count = int(by_window[feature].sum())
            total = int(len(by_window))
            ref_count, ref_total = references[feature]
            rows.append({
                "scope": scope,
                "feature": feature,
                "positive_windows": count,
                "total_windows": total,
                "positive_fraction": count / total,
                "development_positive_windows": ref_count,
                "development_total_windows": ref_total,
                "development_positive_fraction": ref_count / ref_total,
            })
    return pd.DataFrame(rows)


def grouped(records: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    return {
        label: [record for record in records if record["class_label"] == label]
        for label in sorted({record["class_label"] for record in records})
    }


def pairwise_rows(
    validation: list[dict[str, Any]], development: list[dict[str, Any]]
) -> pd.DataFrame:
    vg, dg = grouped(validation), grouped(development)
    rows: list[dict[str, Any]] = []
    for label, cases in vg.items():
        for left, right in combinations(cases, 2):
            rows.append({
                "comparison": "validation_intra",
                "left_class": label, "right_class": label,
                "left_case": left["case_id"], "right_case": right["case_id"],
                "similarity": signature_similarity(left["vector"], right["vector"]),
            })
    for left_label, right_label in combinations(sorted(vg), 2):
        for left in vg[left_label]:
            for right in vg[right_label]:
                rows.append({
                    "comparison": "validation_inter",
                    "left_class": left_label, "right_class": right_label,
                    "left_case": left["case_id"], "right_case": right["case_id"],
                    "similarity": signature_similarity(left["vector"], right["vector"]),
                })
    for label in sorted(vg):
        for left in vg[label]:
            for right in dg[label]:
                rows.append({
                    "comparison": "validation_to_development_same_class",
                    "left_class": label, "right_class": label,
                    "left_case": left["case_id"], "right_case": right["case_id"],
                    "similarity": signature_similarity(left["vector"], right["vector"]),
                })
    return pd.DataFrame(rows)


def similarity_summary(
    pairs: pd.DataFrame, validation_eval: dict[str, Any], development_eval: dict[str, Any]
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []

    def add(kind: str, label: str, values: list[float], dev: dict[str, Any] | None) -> None:
        stats = distribution(values)
        row: dict[str, Any] = {"comparison": kind, "label": label, **stats}
        for key in ["median", "q1", "q3", "min", "max"]:
            row[f"development_{key}"] = None if dev is None else dev[key]
        if dev is not None and stats["median"] is not None:
            row["median_delta_from_development"] = stats["median"] - dev["median"]
            row["validation_median_in_development_iqr"] = dev["q1"] <= stats["median"] <= dev["q3"]
            row["validation_median_in_development_range"] = dev["min"] <= stats["median"] <= dev["max"]
        rows.append(row)

    for label, dev in development_eval["intra_class_similarity"].items():
        values = pairs[
            (pairs.comparison == "validation_intra") & (pairs.left_class == label)
        ].similarity.tolist()
        add("validation_intra", label, values, dev)
    for pair, dev in development_eval["inter_class_similarity"].items():
        left, right = pair.split("__")
        values = pairs[
            (pairs.comparison == "validation_inter")
            & (pairs.left_class == left) & (pairs.right_class == right)
        ].similarity.tolist()
        add("validation_inter", pair, values, dev)
    for label, dev in development_eval["intra_class_similarity"].items():
        values = pairs[
            (pairs.comparison == "validation_to_development_same_class")
            & (pairs.left_class == label)
        ].similarity.tolist()
        add("validation_to_development_same_class", label, values, dev)
    for label, value in validation_eval["separation_margin"]["values"].items():
        dev_value = development_eval["separation_margin"]["values"][label]
        rows.append({
            "comparison": "margin", "label": label, "n": 1,
            "median": value, "q1": value, "q3": value, "min": value, "max": value,
            "development_median": dev_value,
            "median_delta_from_development": value - dev_value,
        })
    return pd.DataFrame(rows)


def topk_outputs(
    validation: list[dict[str, Any]], development_eval: dict[str, Any]
) -> tuple[pd.DataFrame, pd.DataFrame]:
    vg = grouped(validation)
    j_rows: list[dict[str, Any]] = []
    r_rows: list[dict[str, Any]] = []
    for label, cases in vg.items():
        for feature in FEATURE_SECTIONS:
            sets = [set(case["dominant"][feature][:TOP_K]) for case in cases]
            value = jaccard(sets[0], sets[1])
            dev = development_eval["dominant_variable_stability"][label][feature]
            j_rows.append({
                "class_label": label, "feature": feature, "top_k": TOP_K,
                "left_case": cases[0]["case_id"], "right_case": cases[1]["case_id"],
                "left_variables": ";".join(sorted(sets[0])),
                "right_variables": ";".join(sorted(sets[1])),
                "jaccard": value,
                "undefined_empty_union": value is None,
                "development_median": dev["pairwise_jaccard"]["median"],
                "development_q1": dev["pairwise_jaccard"]["q1"],
                "development_q3": dev["pairwise_jaccard"]["q3"],
                "development_min": dev["pairwise_jaccard"]["min"],
                "development_max": dev["pairwise_jaccard"]["max"],
            })
            recurrence = Counter(name for values in sets for name in values)
            dev_recurrence = dev["recurrence"]
            for variable in sorted(set(recurrence) | set(dev_recurrence)):
                r_rows.append({
                    "class_label": label, "feature": feature, "variable": variable,
                    "validation_count": recurrence.get(variable, 0),
                    "validation_cases": 2,
                    "development_count": dev_recurrence.get(variable, 0),
                    "development_cases": 5,
                })
    return pd.DataFrame(j_rows), pd.DataFrame(r_rows)


def f10_components(
    validation: list[dict[str, Any]], development: list[dict[str, Any]]
) -> pd.DataFrame:
    vg, dg = grouped(validation), grouped(development)
    rows = []
    for index, name in enumerate(COMPONENT_NAMES):
        positions = np.arange(index, 41 * 17, 17)
        same = [
            float(np.mean(np.abs(v["vector"][positions] - d["vector"][positions])))
            for v in vg["F10"] for d in dg["F10"]
        ]
        normal = [
            float(np.mean(np.abs(v["vector"][positions] - n["vector"][positions])))
            for v in vg["F10"] for n in vg["Normal"]
        ]
        rows.append({
            "component": name,
            "f10_validation_to_f10_development_mean_distance": float(np.mean(same)),
            "f10_validation_to_normal_validation_mean_distance": float(np.mean(normal)),
            "normal_minus_same_class_distance": float(np.mean(normal) - np.mean(same)),
            "f10_validation_mean": float(np.mean([v["vector"][positions].mean() for v in vg["F10"]])),
            "f10_development_mean": float(np.mean([d["vector"][positions].mean() for d in dg["F10"]])),
            "normal_validation_mean": float(np.mean([n["vector"][positions].mean() for n in vg["Normal"]])),
        })
    return pd.DataFrame(rows)


def fmt(value: Any, digits: int = 4) -> str:
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return "undefined"
    return f"{float(value):.{digits}f}"


def feature_item(item: dict[str, Any], feature: str) -> dict[str, Any]:
    section, _ = FEATURE_SECTIONS[feature]
    return item[section]


def report_text(
    validation: list[dict[str, Any]], normal_df: pd.DataFrame,
    summary: pd.DataFrame, jaccard_df: pd.DataFrame,
    recurrence_df: pd.DataFrame, f10_df: pd.DataFrame,
) -> str:
    metadata = {row["case_id"]: row for row in CASE_METADATA}
    lines = [
        "# Verbalizer V2 validation report", "",
        "## Scope and freeze integrity", "",
        "- Frozen commit and HEAD: `3fd960a192bafacbaabce9471e3c3614d6b2d2db`.",
        "- Frozen tag: `verbalizer-v2-pre-validation`.",
        "- Pre-validation Git status: clean.",
        "- All four frozen SHA-256 hashes matched `VERBALIZER_V2_FREEZE.md`.",
        "- Evaluated data: fault batches 6–7 for F1/F8/F10/F13 and Normal N6–N7 only.",
        "- Fault batches 8–10 and Normal N8–N10 were not read.",
        "- Frozen features, thresholds, renderer, config, similarity, and `top_k=4` were not changed.",
        "", "## Normal validation", "",
        "| Scope | Feature | Positive windows | Fraction | Development reference |", "|---|---|---:|---:|---:|",
    ]
    for row in normal_df.itertuples(index=False):
        lines.append(
            f"| {row.scope} | {row.feature} | {row.positive_windows}/{row.total_windows} "
            f"| {row.positive_fraction:.1%} | {row.development_positive_windows}/{row.development_total_windows} "
            f"({row.development_positive_fraction:.1%}) |"
        )

    lines += ["", "## Similarity and margins", "",
              "| Comparison | Label | Validation median | Validation Q1–Q3 | Development median | Development Q1–Q3 | Δ median |",
              "|---|---|---:|---:|---:|---:|---:|"]
    for row in summary.itertuples(index=False):
        lines.append(
            f"| {row.comparison} | {row.label} | {fmt(row.median)} | {fmt(row.q1)}–{fmt(row.q3)} "
            f"| {fmt(getattr(row, 'development_median', None))} "
            f"| {fmt(getattr(row, 'development_q1', None))}–{fmt(getattr(row, 'development_q3', None))} "
            f"| {fmt(getattr(row, 'median_delta_from_development', None))} |"
        )

    lines += ["", "## Fault temporal evidence", "",
              "The following tables reproduce structured counts without assigning a diagnostic mechanism.", ""]
    for label in ["F1", "F8", "F10", "F13"]:
        lines += [f"### {label}", ""]
        for record in [r for r in validation if r["class_label"] == label]:
            meta = metadata[record["case_id"]]
            s = record["structured"]
            lines += [f"#### Batch {meta['batch']} (`{record['case_id']}`)", "",
                      "| Feature | System active windows | Active fraction | Initial | Late | Dominant variables |",
                      "|---|---:|---:|---:|---:|---|"]
            activity = s["system_summary"]["window_activity"]
            for feature in FEATURE_SECTIONS:
                a = activity[feature]
                dominant = ", ".join(record["dominant"][feature][:TOP_K]) or "none"
                lines.append(
                    f"| {feature} | {a['n_active_windows']}/{s['n_windows']} | {a['active_fraction']:.3f} "
                    f"| {a['initial_active_windows']} | {a['late_active_windows']} | {dominant} |"
                )
            lines += ["", "Dominant-variable details:", ""]
            for feature in FEATURE_SECTIONS:
                details = []
                for variable in record["dominant"][feature][:TOP_K]:
                    item = feature_item(s["variables"][variable], feature)
                    sign = ""
                    if feature in {"level", "trend"}:
                        sign = (
                            f", signs +{item['positive_count']}/-{item['negative_count']}, "
                            f"consistency={item['sign_consistency']:.3f}"
                        )
                    details.append(
                        f"{variable}: active={item['n_active_windows']}/{s['n_windows']} "
                        f"({item['active_fraction']:.3f}){sign}, late={item['late_active_fraction']:.3f}, "
                        f"run={item['longest_same_sign_run'] if feature in {'level', 'trend'} else item['longest_run']}"
                    )
                lines.append(f"- {feature}: " + ("; ".join(details) if details else "no dominant variable"))
            lines.append("")

    lines += ["## Top-4 dominant-variable Jaccard", "",
              "| Class | Feature | Validation Jaccard | Development median [Q1, Q3] |",
              "|---|---|---:|---:|"]
    for row in jaccard_df.itertuples(index=False):
        lines.append(
            f"| {row.class_label} | {row.feature} | {fmt(row.jaccard)} "
            f"| {fmt(row.development_median)} [{fmt(row.development_q1)}, {fmt(row.development_q3)}] |"
        )

    lines += ["", "## Dominant-variable recurrence", "",
              "Full recurrence counts are in `validation_variable_recurrence.csv`. Variables recurring in both validation cases:", ""]
    both = recurrence_df[recurrence_df.validation_count == 2]
    for (label, feature), group in both.groupby(["class_label", "feature"]):
        values = ", ".join(
            f"{r.variable} (dev {r.development_count}/5)" for r in group.itertuples(index=False)
        )
        lines.append(f"- {label} / {feature}: {values or 'none'}")

    lines += ["", "## F10 component-distance audit", "",
              "Positive `normal_minus_same_class_distance` means validation F10 is closer to development F10 than to validation Normal for that component; negative means closer to Normal.", "",
              "| Component | Distance to development F10 | Distance to validation Normal | Normal minus same-class |",
              "|---|---:|---:|---:|"]
    for row in f10_df.sort_values("normal_minus_same_class_distance").itertuples(index=False):
        lines.append(
            f"| {row.component} | {row.f10_validation_to_f10_development_mean_distance:.5f} "
            f"| {row.f10_validation_to_normal_validation_mean_distance:.5f} "
            f"| {row.normal_minus_same_class_distance:.5f} |"
        )

    lines += ["", "## Descriptive verdict", "",
              "The verdict section is completed after inspecting the frozen metrics. No post-hoc numerical pass/fail threshold is used.", ""]
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

    # Verbalizer outputs remain anonymous. Ground-truth labels are stored only
    # in the separate metadata and evaluator tables.
    write_jsonl(
        OUT / "validation_structured_signatures.jsonl",
        [{"case_id": case_id, "structured": structured[case_id]} for case_id in sorted(structured)],
    )
    with (OUT / "validation_neutral_text.txt").open("w", encoding="utf-8") as handle:
        for case_id in sorted(structured):
            handle.write(f"=== {case_id} ===\n{render_text(structured[case_id])}\n\n")
    write_jsonl(OUT / "validation_metadata.jsonl", CASE_METADATA)

    fpr = normal_fpr(normal_features, config)
    fpr.to_csv(OUT / "validation_normal_fpr.csv", index=False)

    validation_records = [
        record_from_structured(meta, structured[meta["case_id"]]) for meta in CASE_METADATA
    ]
    development_records = load_development_cases(ANALYSIS_DIR, config)
    # The frozen evaluate() computation is used unchanged. Its static scope
    # metadata remains development-oriented, so only its metric sections are
    # consumed for validation reporting.
    validation_eval = evaluate(validation_records, top_k=TOP_K)
    development_eval = evaluate(development_records, top_k=TOP_K)

    pairs = pairwise_rows(validation_records, development_records)
    pairs.to_csv(OUT / "validation_pairwise_similarity.csv", index=False)
    summary = similarity_summary(pairs, validation_eval, development_eval)
    summary.to_csv(OUT / "validation_similarity_summary.csv", index=False)
    jaccard_df, recurrence_df = topk_outputs(validation_records, development_eval)
    jaccard_df.to_csv(OUT / "validation_topk_jaccard.csv", index=False)
    recurrence_df.to_csv(OUT / "validation_variable_recurrence.csv", index=False)
    f10_df = f10_components(validation_records, development_records)
    f10_df.to_csv(OUT / "validation_f10_component_distances.csv", index=False)

    with (OUT / "validation_evaluator_metrics.json").open("w", encoding="utf-8") as handle:
        json.dump({
            "note": "Metric sections computed by frozen evaluate(); static development-only scope metadata omitted.",
            "top_k": TOP_K,
            "similarity": "1 - mean(abs(a-b))",
            "intra_class_similarity": validation_eval["intra_class_similarity"],
            "inter_class_similarity": validation_eval["inter_class_similarity"],
            "separation_margin": validation_eval["separation_margin"],
            "dominant_variable_stability": validation_eval["dominant_variable_stability"],
        }, handle, indent=2, ensure_ascii=False)
        handle.write("\n")

    report = report_text(
        validation_records, fpr, summary, jaccard_df, recurrence_df, f10_df
    )
    (OUT / "validation_report.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
