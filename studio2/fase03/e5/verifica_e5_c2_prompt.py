#!/usr/bin/env python3
"""E5-C2 on the **whole prompt**: exact counts, no additivity assumption.

Why this replaces the earlier `misura_prefisso_blf.py`. That script computed the constant
part of a B-LF prompt as ``token(prompt) - token(case block)`` and evaluated the 5 % rule as
``|Delta on the text| / (constant part + text)``. With a BPE tokenizer this is only an
approximation: token counts are not additive across the junctions between prefix, case block
and suffix, so neither the subtraction nor the resulting threshold is a proof.

Here nothing is added or subtracted. Each arm's prompt is **composed** -- the case block of a
real rendered B-LF prompt is replaced by the FULL text and by the PERM text -- and each
composed prompt is tokenized whole:

    Delta = token(prompt with PERM text) - token(prompt with FULL text)
    ratio = |Delta| / token(prompt with FULL text)

The carrier prompt supplies the real prefix and suffix, so the junction bytes are the real
ones. The script also reports ``boundary_residual = Delta_prompt - Delta_text``: the exact
size of the error the additive shortcut would have made.

Two ways to run it.

* **Before G3, with the real carriers** (what closes E5-C2 for the development measurement):
  pass ``--prompts`` pointing at the rendered ``final_prompts.jsonl``. The prefixes and
  suffixes are then the real ones; only the case texts come from development data.
* **At G3, on the test lot**: pass ``--prompts`` and ``--case-texts`` -- a JSONL of the
  FULL/PERM texts actually produced for the test cases (format in ``pairs_from_case_texts``).
  That is the real measurement, on the same code path; nothing is recomputed from development
  data and the summary records ``measurement: G3``.

Which carrier. The ratio's denominator is the composed prompt, so the worst case is the
carrier that composes to the fewest tokens **with that text** -- which cannot be found by
counting prefix and suffix apart, for the same non-additivity reason. ``--carrier-mode``
decides: ``all`` evaluates every carrier on every pair and is the only exhaustive mode -- both
runs that are meant to close the 5 %, the pre-freeze one and G3, use it; ``candidates``
shortlists the carriers that compose shortest over a few probe texts, evaluates the whole
shortlist on every pair and reports the **worst carrier per pair**, which is an informed
shortcut and yields a feasibility check, never a proof; ``sample`` is for smoke runs only. The summary carries ``carrier_ranking.rank_stability``: false means the probe texts
disagreed on the shortest carrier, which is exactly why a shortlist is kept rather than one.

A synthetic wrapper is accepted for validating the machinery without any real prompt; a run
made that way is marked ``carrier: synthetic`` and proves nothing about the 5 %.

Read-only: no ledger, no model call, no network; it writes only ``--out``.
"""

from __future__ import annotations

import argparse
import json
import random
import statistics
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
for candidate in (REPO_ROOT, REPO_ROOT / "code", HERE):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

import pandas as pd  # noqa: E402

import tep_verbalize_v2 as verbalizer  # noqa: E402
import e5_corruption  # noqa: E402
import e5_derangement  # noqa: E402
from verifica_e5_c2 import (  # noqa: E402
    DEFAULT_SNAPSHOT, FAMILIES, build_counter, load_units, stable_seed, subset_for,
)

CASE_HEADING = "CASE TO DIAGNOSE"
SCHEMA_HEADING = "OUTPUT SCHEMA"
THRESHOLD = 0.05


class CarrierError(RuntimeError):
    pass


def split_carrier(text: str) -> tuple[str, str, str]:
    """(prefix, case block, suffix) of one rendered prompt, junction bytes included."""
    try:
        start = text.index(CASE_HEADING) + len(CASE_HEADING) + 2
        end = text.index(SCHEMA_HEADING, start)
    except ValueError as exc:
        raise CarrierError("the carrier is not a rendered diagnostic prompt") from exc
    return text[:start], text[start:end], text[end:]


def compose(prefix: str, case_text: str, suffix: str) -> str:
    """Put a case text back in the carrier, keeping the renderer's own separators."""
    return prefix + case_text.strip() + "\n\n" + suffix


def load_carriers(path: Path, *, limit: int | None, condition: str = "B-LF") -> list[dict]:
    carriers = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            if row.get("condition") != condition:
                continue
            prefix, case_block, suffix = split_carrier(row["text"])
            if compose(prefix, case_block, suffix) != row["text"]:
                raise CarrierError(
                    f"round trip failed on {row.get('prompt_id') or row.get('stable_id')}: "
                    "the case block is not delimited as expected")
            carriers.append({"id": row.get("stable_id") or row.get("prompt_id") or "?",
                             "prefix": prefix, "suffix": suffix,
                             "original_case": case_block})
            if limit and len(carriers) >= limit:
                break
    if not carriers:
        raise CarrierError(f"no {condition} prompt found in {path}")
    return carriers


def synthetic_carriers(wrapper_tokens: int) -> list[dict]:
    """A carrier with no real content, for validating the code path only."""
    filler = ("Esempio locale: intervallo osservato, soglie superate, nessuna diagnosi. "
              * max(1, wrapper_tokens // 12))
    prefix = ("BASE INSTRUCTION\n\nDECISION POLICY\n\npolicy\n\nLABEL SPACE\n\n[\"L1\"]\n\n"
              "LOCAL LABELED EXAMPLES\n\n" + filler + "\n\nPEER INSIGHTS\n\n" + filler
              + "\n\n" + CASE_HEADING + "\n\n")
    suffix = SCHEMA_HEADING + "\n\n{\"predicted_label\":null}\n"
    return [{"id": "synthetic", "prefix": prefix, "suffix": suffix, "original_case": ""}]


def pairs_from_dev_units(cache: Path, *, seeds: int, base_seed: int, all_classes: bool):
    """Yield (family, recipient, donor, full text, perm text) from the development units."""
    family_map = e5_corruption.load_family_map()
    runs, frames = load_units(cache)
    config = verbalizer.load_config()
    window_starts = {row["run_id"]: sorted(frames[row["run_id"]].window_start_h.unique())
                     for row in runs}
    for replicate in range(seeds):
        seed = base_seed + replicate
        rng = random.Random(seed)
        units = {}
        for row in runs:
            run_id = row["run_id"]
            start = rng.choice(window_starts[run_id])
            frame = frames[run_id]
            units[run_id] = (frame[frame.window_start_h == start].copy()
                             .sort_values("variable").reset_index(drop=True))
        full_text = {run_id: verbalizer.verbalize_feature_table(unit, config)["text"]
                     for run_id, unit in units.items()}
        for family in FAMILIES:
            subset = subset_for(family, runs, family_map, all_classes=all_classes)
            ids = [row["run_id"] for row in subset]
            classes = [row["fault"] for row in subset]
            family_seed = stable_seed(seed, family)
            mapping = e5_derangement.sample(ids, classes, seed=family_seed)
            for recipient, donor in mapping["pairs"].items():
                permuted = e5_corruption.swap_family(units[recipient], units[donor], family,
                                                     family_map=family_map)
                perm_text = verbalizer.verbalize_feature_table(permuted, config)["text"]
                yield {"family": family, "recipient": recipient, "donor": donor,
                       "seed": seed, "family_seed": family_seed,
                       "full_text": full_text[recipient], "perm_text": perm_text}


def pairs_from_case_texts(path: Path):
    """Yield the FULL/PERM pairs of the test lot, as produced after the freeze (G3).

    JSONL, one object per pair::

        {"family": "residual", "case_id": "test-primary-F8-r03",
         "donor_case_id": "test-primary-F1-r05",
         "full_text": "...", "perm_text": "..."}

    ``arm`` may be used instead of the two texts, in which case two rows with the same
    ``family`` and ``case_id`` -- one ``FULL``, one ``PERM`` -- form the pair. Nothing is
    recomputed here: these texts are the ones the frozen verbalizer produced for the test
    cases, so this is the real G3 measurement and not a simulation.
    """
    halves: dict[tuple[str, str], dict[str, str]] = {}
    with Path(path).open(encoding="utf-8") as handle:
        for number, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            family = row.get("family")
            case_id = row.get("case_id")
            if family not in FAMILIES or not case_id:
                raise CarrierError(f"{path}:{number}: missing or unknown family/case_id")
            if "full_text" in row and "perm_text" in row:
                yield {"family": family, "recipient": case_id,
                       "donor": row.get("donor_case_id", ""),
                       "seed": None, "family_seed": None,
                       "full_text": row["full_text"], "perm_text": row["perm_text"]}
                continue
            arm = (row.get("arm") or "").upper()
            if arm not in ("FULL", "PERM") or "text" not in row:
                raise CarrierError(
                    f"{path}:{number}: a row needs either full_text+perm_text, or arm+text")
            slot = halves.setdefault((family, case_id), {})
            if arm in slot:
                raise CarrierError(f"{path}:{number}: {arm} given twice for {case_id}/{family}")
            slot[arm] = row["text"]
            slot.setdefault("donor", row.get("donor_case_id", ""))
    for (family, case_id), slot in halves.items():
        if "FULL" not in slot or "PERM" not in slot:
            raise CarrierError(f"{case_id}/{family}: the pair is incomplete")
        yield {"family": family, "recipient": case_id, "donor": slot.get("donor", ""),
               "seed": None, "family_seed": None,
               "full_text": slot["FULL"], "perm_text": slot["PERM"]}


def rank_carriers(carriers: list[dict], probe_texts: list[str], count, *,
                  keep: int) -> tuple[list[dict], dict]:
    """Shortlist the carriers that give the shortest COMPOSED prompt, never prefix+suffix.

    Ranking a carrier by ``count(prefix + suffix)`` would assume the case block adds a fixed
    number of tokens, which is the very additivity a BPE tokenizer does not guarantee. The
    ranking here composes each candidate with real probe texts and sorts on the composed
    length; the shortlist is then evaluated pair by pair, and the worst carrier per pair is
    the one reported. ``rank_stability`` says whether the probe texts agreed on the winner.
    """
    if len(carriers) <= keep:
        return carriers, {"ranked": False, "reason": "every carrier is kept"}
    scored = []
    winners = []
    per_text: dict[str, list[tuple[int, int]]] = {}
    for index, carrier in enumerate(carriers):
        lengths = [count(compose(carrier["prefix"], text, carrier["suffix"]))
                   for text in probe_texts]
        scored.append((max(lengths), min(lengths), index))
        per_text[carrier["id"]] = list(zip(lengths, [index] * len(lengths)))
    for position in range(len(probe_texts)):
        winners.append(min(carriers, key=lambda item, p=position:
                           per_text[item["id"]][p][0])["id"])
    scored.sort()
    shortlist = [carriers[index] for _, _, index in scored[:keep]]
    return shortlist, {
        "ranked": True,
        "candidates_kept": keep,
        "probe_texts": len(probe_texts),
        "shortest_carrier_per_probe_text": sorted(set(winners)),
        "rank_stability": len(set(winners)) == 1,
        "note": ("the shortlist is evaluated on every pair and the worst carrier per pair is "
                 "the one reported; if rank_stability is false the shortlist is what protects "
                 "the worst case, which is why more than one candidate is kept"),
    }


def measure(pairs, carriers: list[dict], count, *, mode: str, carrier_sample: int,
            seed: int = 0) -> dict:
    rows_by_family: dict[str, list[dict]] = {family: [] for family in FAMILIES}
    chooser = random.Random(seed ^ 0x5F5E100)
    residuals: list[int] = []
    for pair in pairs:
        delta_text = count(pair["perm_text"]) - count(pair["full_text"])
        chosen = carriers
        if mode == "sample" and len(carriers) > carrier_sample:
            chosen = chooser.sample(carriers, carrier_sample)
        worst = None
        for carrier in chosen:
            tokens_full = count(compose(carrier["prefix"], pair["full_text"],
                                        carrier["suffix"]))
            tokens_perm = count(compose(carrier["prefix"], pair["perm_text"],
                                        carrier["suffix"]))
            delta = tokens_perm - tokens_full
            residuals.append(delta - delta_text)
            observation = {
                "family": pair["family"], "seed": pair["seed"],
                "family_seed": pair["family_seed"], "carrier": carrier["id"],
                "recipient": pair["recipient"], "donor": pair["donor"],
                "tokens_full_prompt": tokens_full, "tokens_perm_prompt": tokens_perm,
                "delta_prompt": delta, "delta_text": delta_text,
                "boundary_residual": delta - delta_text,
                "ratio": abs(delta) / tokens_full,
            }
            if worst is None or observation["ratio"] > worst["ratio"]:
                worst = observation
        if worst is not None:
            worst["carriers_evaluated"] = len(chosen)
            rows_by_family[pair["family"]].append(worst)

    summary = {
        "artifact_version": "VERIFICA_E5_C2_PROMPT_3",
        "scope": "length only, on whole composed prompts; no additivity assumption",
        "threshold": THRESHOLD,
        "reported_value": ("per pair, the WORST ratio over the carriers evaluated for that "
                           "pair (the worst case is chosen after composition, never from "
                           "prefix+suffix counted apart)"),
        "carrier_mode": mode,
        "carriers_available": len(carriers),
        "families": {},
    }
    for family, rows in rows_by_family.items():
        if not rows:
            continue
        ratios = [row["ratio"] for row in rows]
        summary["families"][family] = {
            "pairs": len(rows),
            "max_ratio": max(ratios),
            "p99_ratio": sorted(ratios)[int(0.99 * (len(ratios) - 1))],
            "mean_ratio": statistics.fmean(ratios),
            "share_above_threshold": sum(value > THRESHOLD for value in ratios) / len(ratios),
            "verdict": "PASS" if max(ratios) <= THRESHOLD else "FAIL",
            "worst_pair": max(rows, key=lambda row: row["ratio"]),
        }
    if residuals:
        summary["boundary_residual"] = {
            "definition": "delta on the composed prompt minus delta on the text alone",
            "observations": len(residuals),
            "min": min(residuals), "max": max(residuals),
            "share_nonzero": sum(value != 0 for value in residuals) / len(residuals),
        }
    summary["verdict"] = ("PASS" if summary["families"] and all(
        entry["verdict"] == "PASS" for entry in summary["families"].values()) else "FAIL")
    return summary


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--dev-units", type=Path,
                        help="development cache: the pre-freeze feasibility run")
    source.add_argument("--case-texts", type=Path,
                        help="JSONL of FULL/PERM texts of the test lot: the real G3 measurement")
    parser.add_argument("--prompts", type=Path, default=None,
                        help="rendered final_prompts.jsonl; without it the carrier is synthetic")
    parser.add_argument("--carrier-limit", type=int, default=None)
    parser.add_argument("--carrier-mode", choices=("candidates", "all", "sample"),
                        default="candidates",
                        help="candidates: shortlist the shortest COMPOSED carriers and take the "
                             "worst per pair; all: every carrier on every pair (exhaustive, slow); "
                             "sample: random carriers per pair (smoke only)")
    parser.add_argument("--candidates", type=int, default=5,
                        help="size of the shortlist in carrier-mode candidates")
    parser.add_argument("--probe-texts", type=int, default=8,
                        help="texts used to rank the carriers by composed length")
    parser.add_argument("--carrier-sample", type=int, default=1)
    parser.add_argument("--wrapper-tokens", type=int, default=1200)
    parser.add_argument("--snapshot", type=Path, default=DEFAULT_SNAPSHOT)
    parser.add_argument("--seeds", type=int, default=50)
    parser.add_argument("--base-seed", type=int, default=20260919)
    parser.add_argument("--all-classes", action="store_true")
    parser.add_argument("--out", type=Path, required=True)
    arguments = parser.parse_args(argv)

    count = build_counter(arguments.snapshot)
    if arguments.prompts:
        carriers = load_carriers(arguments.prompts, limit=arguments.carrier_limit)
        kind = "real"
    else:
        carriers = synthetic_carriers(arguments.wrapper_tokens)
        kind = "synthetic"

    if arguments.case_texts:
        pairs = list(pairs_from_case_texts(arguments.case_texts))
        origin = f"test-lot texts from {arguments.case_texts}"
    else:
        pairs = list(pairs_from_dev_units(
            arguments.dev_units, seeds=arguments.seeds, base_seed=arguments.base_seed,
            all_classes=arguments.all_classes))
        origin = "development units (not the test lot)"

    ranking = {"ranked": False, "reason": "carrier-mode is not candidates"}
    if arguments.carrier_mode == "candidates":
        probe = [pair["full_text"] for pair in pairs[:arguments.probe_texts]] or [""]
        carriers, ranking = rank_carriers(carriers, probe, count, keep=arguments.candidates)

    summary = measure(pairs, carriers, count, mode=arguments.carrier_mode,
                      carrier_sample=arguments.carrier_sample, seed=arguments.base_seed)
    summary["carrier"] = kind
    summary["carrier_ranking"] = ranking
    summary["case_texts"] = origin
    summary["measurement"] = ("G3, real test-lot texts" if arguments.case_texts
                              else "pre-freeze, development texts")
    summary["status_of_the_result"] = (
        "PROOF over the carriers available: every carrier evaluated on every pair"
        if arguments.carrier_mode == "all" else
        "FEASIBILITY CHECK ONLY: the carriers were shortlisted, so this does not verify the "
        "5 % on every pair and every carrier. Re-run with --carrier-mode all to close it.")
    if kind == "synthetic":
        summary["warning"] = ("synthetic carrier: this run validates the code path and "
                              "measures the boundary residual; it proves nothing about the "
                              "5 % rule on the real prompts")
    arguments.out.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
                             encoding="utf-8")
    print(json.dumps({key: value for key, value in summary.items() if key != "families"},
                     indent=2, ensure_ascii=False))
    for family, entry in summary["families"].items():
        print(f"{family:9s} pairs={entry['pairs']:5d} max_ratio={entry['max_ratio']:.4f} "
              f"share>5%={entry['share_above_threshold']:.4f} {entry['verdict']}")
    return 0 if summary["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
