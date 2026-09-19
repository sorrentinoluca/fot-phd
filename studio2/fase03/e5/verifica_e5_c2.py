#!/usr/bin/env python3
"""E5-C2 feasibility measurement (gate G0): length only, on development data, offline.

What it measures, and nothing else: the distribution of ``|token_PERM - token_FULL| /
token_FULL`` under the class-disjoint derangement, with the frozen verbalizer and the
tokenizer of the model actually used (Qwen3.5-122B snapshot ``a099dee7...``).

No predicted label, no accuracy, no diagnostic preview: piano 8.12 forbids any diagnostic
result from entering the choice of the 5 % threshold. No model call is made: the tokenizer
runs locally on the frozen snapshot.

Geometry of the simulation. The final study assigns **one window per run** (D1), so each
replicate samples one window per development run and treats it as a case. For each family
F a uniform class-disjoint derangement over the evaluated subset S_F supplies the donor;
the donor's column of F replaces the recipient's, and the frozen verbalizer re-renders the
text with every derived quantity recomputed (E5-B).

Denominator. Only the neutral text of the case changes between FULL and PERM: the frozen
renderer puts it in the ``CASE TO DIAGNOSE`` section and every other section -- base
instruction, policy, label space, local examples, peer insights, output schema -- is byte
identical in the two arms. Hence ``|Delta token|`` on the full prompt equals
``|Delta token|`` on the neutral text, and the ratio on the text alone is an **upper bound**
on the ratio on the full prompt, which carries a larger denominator. Both are reported:
``ratio_text`` (upper bound, the conservative reading) and ``ratio_prompt`` for a few sizes
of the constant part.

Diagnostic control (8.12, "rapid congelata"): for ``residual`` and ``diff`` the script also
counts the PERM text in which the ``rapid`` sentence is put back to its FULL value. It
attributes part of the shift to the recomputation of ``rapid`` rather than to the swapped
column. It is diagnostic only and enters no contrast.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import statistics
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
for candidate in (REPO_ROOT, REPO_ROOT / "code", Path(__file__).resolve().parent):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

import pandas as pd  # noqa: E402

import tep_verbalize_v2 as verbalizer  # noqa: E402
import e5_corruption  # noqa: E402
import e5_derangement  # noqa: E402
import protocol_omit  # noqa: E402

DEFAULT_SNAPSHOT = (REPO_ROOT / "studio2/fase03/evidence"
                    / "qwen3_5_122b_tokenizer_a099dee70ccfcd8d5dda56aaa0b60cb8ecadabc9")
FAMILIES = ("level", "trend", "residual", "diff")
SEED_NAMESPACE = "studio2-fase03-e5-c2-v1"
PROMPT_PREFIX_SIZES = (0, 2000, 3000, 4000)
QUALIFIED_CONTEXT = 131072
RESERVED_OUTPUT_TOKENS = 2560


def stable_seed(base_seed: int, family: str) -> int:
    """Seed of the derangement of one family, stable across processes and machines.

    ``hash()`` is salted per process in Python (PYTHONHASHSEED), so a seed derived from it
    is NOT reproducible: the same base seed would give a different derangement on a second
    run. The seed is therefore derived from SHA-256, exactly as ``build_e5_assignments.py``
    does for the frozen assignment artifacts.
    """
    digest = hashlib.sha256(f"{SEED_NAMESPACE}|{base_seed}|{family}".encode()).hexdigest()
    return int(digest[:12], 16)


def build_counter(snapshot: Path):
    """Token counter on the frozen snapshot: ``tokenizers`` if present, else transformers."""
    tokenizer_json = Path(snapshot) / "tokenizer.json"
    if not tokenizer_json.is_file():
        raise SystemExit(f"tokenizer snapshot not found: {tokenizer_json}")
    try:
        from tokenizers import Tokenizer
        tokenizer = Tokenizer.from_file(str(tokenizer_json))

        def count(text: str) -> int:
            return len(tokenizer.encode(text, add_special_tokens=False).ids)
        count.backend = "tokenizers"  # type: ignore[attr-defined]
        return count
    except ImportError:
        pass
    from transformers import AutoTokenizer  # noqa: F401
    tokenizer = AutoTokenizer.from_pretrained(str(snapshot), local_files_only=True,
                                              trust_remote_code=False)

    def count_hf(text: str) -> int:
        return len(tokenizer.encode(text, add_special_tokens=False))
    count_hf.backend = "transformers"  # type: ignore[attr-defined]
    return count_hf


def load_units(cache: Path) -> tuple[list[dict], dict[str, pd.DataFrame]]:
    index = json.loads((cache / "DEV_UNITS_INDEX.json").read_text(encoding="utf-8"))
    frames = {row["run_id"]: pd.read_csv(row["features_path"]) for row in index["runs"]}
    return index["runs"], frames


def subset_for(family: str, runs: list[dict], family_map: dict, *, all_classes: bool) -> list[dict]:
    if all_classes:
        return list(runs)
    subset = family_map["subsets_S_F_proposal"][family]
    keep = set(subset["target_faults"]) | set(subset["control_faults"])
    return [row for row in runs if row["fault"] in keep]


def replace_rapid_sentence(perm_structured, perm_text, full_structured) -> str:
    """PERM text with the ``rapid`` sentence restored to its FULL value (diagnostic only)."""
    perm_sentences = protocol_omit._family_sentences(perm_structured, "residual")
    full_sentences = protocol_omit._family_sentences(full_structured, "residual")
    perm_rapid = perm_sentences[1] if len(perm_sentences) > 1 else None
    full_rapid = full_sentences[1] if len(full_sentences) > 1 else None
    if perm_rapid is None and full_rapid is None:
        return perm_text
    if perm_rapid is None:
        return perm_text.rstrip() + " " + full_rapid
    if full_rapid is None:
        return perm_text.replace(" " + perm_rapid, "", 1)
    return perm_text.replace(perm_rapid, full_rapid, 1)


def run(cache: Path, snapshot: Path, *, seeds: int, base_seed: int,
        all_classes: bool, config=None, raw_out: Path | None = None) -> dict:
    count = build_counter(snapshot)
    family_map = e5_corruption.load_family_map()
    runs, frames = load_units(cache)
    config = config or verbalizer.load_config()
    protocol_omit.verify_frozen_renderer()

    window_starts = {row["run_id"]: sorted(frames[row["run_id"]].window_start_h.unique())
                     for row in runs}
    observations: dict[str, list[dict]] = {family: [] for family in FAMILIES}
    rapid_control: dict[str, list[float]] = {"residual": [], "diff": []}

    for replicate in range(seeds):
        seed = base_seed + replicate
        rng = random.Random(seed)
        units: dict[str, pd.DataFrame] = {}
        chosen_window: dict[str, float] = {}
        for row in runs:
            run_id = row["run_id"]
            start = rng.choice(window_starts[run_id])
            frame = frames[run_id]
            unit = frame[frame.window_start_h == start].copy().sort_values("variable")
            units[run_id] = unit.reset_index(drop=True)
            chosen_window[run_id] = float(start)
        full_cache: dict[str, dict] = {}
        for run_id, unit in units.items():
            result = verbalizer.verbalize_feature_table(unit, config)
            full_cache[run_id] = {"structured": result["structured"], "text": result["text"],
                                  "tokens": count(result["text"])}

        for family in FAMILIES:
            subset = subset_for(family, runs, family_map, all_classes=all_classes)
            ids = [row["run_id"] for row in subset]
            classes = [row["fault"] for row in subset]
            family_seed = stable_seed(seed, family)
            mapping = e5_derangement.sample(ids, classes, seed=family_seed)
            class_of = dict(zip(ids, classes))
            for recipient, donor in mapping["pairs"].items():
                permuted = e5_corruption.swap_family(units[recipient], units[donor], family,
                                                     family_map=family_map)
                result = verbalizer.verbalize_feature_table(permuted, config)
                tokens_perm = count(result["text"])
                tokens_full = full_cache[recipient]["tokens"]
                delta = tokens_perm - tokens_full
                observations[family].append({
                    "seed": seed, "family_seed": family_seed,
                    "recipient": recipient, "donor": donor,
                    "recipient_class": class_of[recipient], "donor_class": class_of[donor],
                    "window_start_h": chosen_window[recipient],
                    "tokens_full": tokens_full, "tokens_perm": tokens_perm,
                    "delta": delta, "ratio_text": abs(delta) / tokens_full,
                })
                if family in rapid_control:
                    restored = replace_rapid_sentence(
                        result["structured"], result["text"],
                        full_cache[recipient]["structured"])
                    rapid_control[family].append(
                        abs(count(restored) - tokens_full) / tokens_full)

    if raw_out is not None:
        with Path(raw_out).open("a", encoding="utf-8") as handle:
            for family, rows in observations.items():
                for row in rows:
                    handle.write(json.dumps({"family": family, **row}) + "\n")
            for family, values in rapid_control.items():
                for value in values:
                    handle.write(json.dumps(
                        {"family": family, "kind": "rapid_frozen", "ratio_text": value}) + "\n")

    def quantiles(values: list[float]) -> dict:
        ordered = sorted(values)
        def q(p: float) -> float:
            if not ordered:
                return float("nan")
            position = p * (len(ordered) - 1)
            low = int(position)
            high = min(low + 1, len(ordered) - 1)
            return ordered[low] + (position - low) * (ordered[high] - ordered[low])
        return {"min": ordered[0], "p50": q(0.5), "p90": q(0.9), "p95": q(0.95),
                "p99": q(0.99), "max": ordered[-1], "mean": statistics.fmean(ordered)}

    summary = {
        "artifact_version": "VERIFICA_E5_C2_1",
        "scope": "length only; development data only; no model call",
        "tokenizer_snapshot": str(snapshot),
        "tokenizer_backend": getattr(count, "backend", "unknown"),
        "replicates": seeds,
        "base_seed": base_seed,
        "subset_mode": "all_classes" if all_classes else "S_F_proposal",
        "windows_per_case": 1,
        "qualified_context": QUALIFIED_CONTEXT,
        "reserved_output_tokens": RESERVED_OUTPUT_TOKENS,
        "families": {},
        "rapid_frozen_control": {},
    }
    for family in FAMILIES:
        rows = observations[family]
        ratios = [row["ratio_text"] for row in rows]
        tokens_full = [row["tokens_full"] for row in rows]
        deltas = [abs(row["delta"]) for row in rows]
        entry = {
            "pairs": len(rows),
            "tokens_full": quantiles([float(value) for value in tokens_full]),
            "abs_delta_tokens": quantiles([float(value) for value in deltas]),
            "ratio_text_upper_bound": quantiles(ratios),
            "share_above_5pct_text": sum(value > 0.05 for value in ratios) / len(ratios),
            "share_above_5pct_by_prefix": {
                str(prefix): sum(
                    abs(row["delta"]) / (prefix + row["tokens_full"]) > 0.05 for row in rows
                ) / len(rows) for prefix in PROMPT_PREFIX_SIZES},
            "max_ratio_by_prefix": {
                str(prefix): max(abs(row["delta"]) / (prefix + row["tokens_full"])
                                 for row in rows) for prefix in PROMPT_PREFIX_SIZES},
            "required_prefix_tokens_for_5pct": {
                "max": max(abs(row["delta"]) / 0.05 - row["tokens_full"] for row in rows),
                "p99": sorted(abs(row["delta"]) / 0.05 - row["tokens_full"]
                              for row in rows)[int(0.99 * (len(rows) - 1))],
                "p95": sorted(abs(row["delta"]) / 0.05 - row["tokens_full"]
                              for row in rows)[int(0.95 * (len(rows) - 1))],
                "note": ("constant part of the B-LF prompt that would make every pair "
                         "(resp. 99 %, 95 % of them) satisfy |delta|/token_FULL <= 5 % "
                         "on the full prompt"),
            },
            "worst_pair": max(rows, key=lambda row: row["ratio_text"]),
        }
        summary["families"][family] = entry
    for family, values in rapid_control.items():
        if values:
            summary["rapid_frozen_control"][family] = {
                "pairs": len(values), "ratio_text": quantiles(values),
                "share_above_5pct_text": sum(value > 0.05 for value in values) / len(values),
            }
    return summary


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dev-units", type=Path, required=True)
    parser.add_argument("--snapshot", type=Path, default=DEFAULT_SNAPSHOT)
    parser.add_argument("--seeds", type=int, default=200)
    parser.add_argument("--base-seed", type=int, default=20260919)
    parser.add_argument("--all-classes", action="store_true",
                        help="ignore the proposed S_F and derange over all eight classes")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--raw-out", type=Path, default=None,
                        help="append every pair as JSONL, for chunked runs merged later")
    arguments = parser.parse_args(argv)
    summary = run(arguments.dev_units, arguments.snapshot, seeds=arguments.seeds,
                  base_seed=arguments.base_seed, all_classes=arguments.all_classes,
                  raw_out=arguments.raw_out)
    arguments.out.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
                             encoding="utf-8")
    print(json.dumps({family: {
        "p95": value["ratio_text_upper_bound"]["p95"],
        "max": value["ratio_text_upper_bound"]["max"],
        "share>5%": value["share_above_5pct_text"]}
        for family, value in summary["families"].items()}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
