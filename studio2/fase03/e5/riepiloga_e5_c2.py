#!/usr/bin/env python3
"""Merge the JSONL chunks of ``verifica_e5_c2.py`` into one E5-C2 summary.

Length only. The summary reports, per family:

* the distribution of ``|Delta token| / token_FULL`` computed on the **neutral text alone**
  (``ratio_text``), which is an upper bound on the ratio on the full prompt because the
  numerator is identical in the two and the denominator of the full prompt is larger;
* the same ratio for a few sizes of the constant part of the B-LF prompt;
* ``indicative_prefix_for_5pct_NOT_A_PROOF``: how large the constant part would have to be
  for the 5 % rule to hold on every pair **if** token counts were additive across the
  junctions of the prompt. A BPE tokenizer gives no such guarantee, so this is an order of
  magnitude and nothing more. The criterion itself is verified on whole composed prompts by
  ``verifica_e5_c2_prompt.py``, which adds and subtracts nothing.
"""

from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path

FAMILIES = ("level", "trend", "residual", "diff")
PREFIX_SIZES = (0, 500, 1000, 1500, 2000, 2500, 3000, 4000, 5000)


def quantiles(values: list[float]) -> dict:
    ordered = sorted(values)

    def q(p: float) -> float:
        position = p * (len(ordered) - 1)
        low = int(position)
        high = min(low + 1, len(ordered) - 1)
        return ordered[low] + (position - low) * (ordered[high] - ordered[low])

    return {"min": ordered[0], "p50": q(0.5), "p90": q(0.9), "p95": q(0.95),
            "p99": q(0.99), "max": ordered[-1], "mean": statistics.fmean(ordered)}


def load(paths: list[Path]) -> tuple[dict, dict]:
    pairs: dict[str, list[dict]] = {family: [] for family in FAMILIES}
    rapid: dict[str, list[float]] = {"residual": [], "diff": []}
    for path in paths:
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                row = json.loads(line)
                if row.get("kind") == "rapid_frozen":
                    rapid[row["family"]].append(row["ratio_text"])
                else:
                    pairs[row["family"]].append(row)
    return pairs, rapid


def summarize(pairs: dict, rapid: dict, *, label: str) -> dict:
    out = {"artifact_version": "RIEPILOGO_E5_C2_1", "scope": label, "families": {},
           "rapid_frozen_control": {}}
    for family, rows in pairs.items():
        if not rows:
            continue
        ratios = [row["ratio_text"] for row in rows]
        deltas = [abs(row["delta"]) for row in rows]
        tokens = [float(row["tokens_full"]) for row in rows]
        required = sorted(abs(row["delta"]) / 0.05 - row["tokens_full"] for row in rows)
        out["families"][family] = {
            "pairs": len(rows),
            "replicates": len({row["seed"] for row in rows}),
            "tokens_full_text": quantiles(tokens),
            "abs_delta_tokens": quantiles([float(value) for value in deltas]),
            "ratio_text_only_NOT_THE_CRITERION": quantiles(ratios),
            "share_above_5pct_text": sum(value > 0.05 for value in ratios) / len(ratios),
            "share_above_5pct_by_prefix_additive_approximation": {
                str(prefix): sum(abs(row["delta"]) / (prefix + row["tokens_full"]) > 0.05
                                 for row in rows) / len(rows) for prefix in PREFIX_SIZES},
            "max_ratio_by_prefix_additive_approximation": {
                str(prefix): max(abs(row["delta"]) / (prefix + row["tokens_full"])
                                 for row in rows) for prefix in PREFIX_SIZES},
            "indicative_prefix_for_5pct_NOT_A_PROOF": {
                "max": required[-1],
                "p99": required[int(0.99 * (len(required) - 1))],
                "p95": required[int(0.95 * (len(required) - 1))],
                "warning": ("obtained by treating token counts as additive across the "
                            "junctions of the prompt, which a BPE tokenizer does not "
                            "guarantee. It is an order of magnitude, not a verification: "
                            "the 5 % rule is checked on whole composed prompts by "
                            "verifica_e5_c2_prompt.py"),
            },
            "signed_delta_mean": statistics.fmean(row["delta"] for row in rows),
            "share_perm_longer": sum(row["delta"] > 0 for row in rows) / len(rows),
        }
    for family, values in rapid.items():
        if values:
            out["rapid_frozen_control"][family] = {
                "pairs": len(values),
                "ratio_text": quantiles(values),
                "share_above_5pct_text": sum(value > 0.05 for value in values) / len(values),
            }
    return out


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw", type=Path, nargs="+", required=True)
    parser.add_argument("--label", default="S_F proposal, development data only")
    parser.add_argument("--out", type=Path, required=True)
    arguments = parser.parse_args(argv)
    pairs, rapid = load(arguments.raw)
    summary = summarize(pairs, rapid, label=arguments.label)
    arguments.out.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
                             encoding="utf-8")
    for family, value in summary["families"].items():
        print(f"{family:9s} pairs={value['pairs']:5d} "
              f"|d|p50={value['abs_delta_tokens']['p50']:6.1f} "
              f"|d|max={value['abs_delta_tokens']['max']:6.1f} "
              f"tokFULL p50={value['tokens_full_text']['p50']:6.1f} "
              f"prefix~max={value['indicative_prefix_for_5pct_NOT_A_PROOF']['max']:8.0f} "
              f"prefix~p95={value['indicative_prefix_for_5pct_NOT_A_PROOF']['p95']:8.0f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
