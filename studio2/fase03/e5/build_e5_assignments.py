#!/usr/bin/env python3
"""Build the E5 assignment artifacts on identifiers only, before any test datum is opened.

Outputs (both written next to this file by default):

* ``DERANGEMENTS_E5.json`` -- one uniform class-disjoint derangement per family, over the
  evaluated subset S_F, with its seed, its acceptance rate and the pairing matrix that
  8.12 requires to be documented;
* ``RICEVENTI_E5.json``    -- the recipient table, in the mode decided by the author
  (decision A): ``one`` (one recipient per physical run, balanced over the seven
  non-owner agents, overall and within each fault) or ``all`` (all seven non-owners).

Nothing here reads a descriptor, a neutral text or an outcome: only case identifiers,
fault labels and agent identifiers. The same recipient holds for FULL, PERM and OMIT and
for every family in which that run appears (8.12).

No network, no model call, no write outside the output directory.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import e5_derangement  # noqa: E402

AGENTS = tuple(f"agent_{index}" for index in range(1, 9))
FAULTS = ("F1", "F2", "F3", "F8", "F10", "F13", "F14", "F15")
PRIMARY_RUNS = 8
DEFAULT_ASSIGNMENT = REPO_ROOT / "studio2/fase03/pseudolabel/AGENT_ASSIGNMENT.json"
DEFAULT_MAP = HERE / "family_map.json"
NAMESPACE = "studio2-fase03-e5-v1"
DEFAULT_SEED = 20260919


def case_id(fault: str, run: int) -> str:
    """The case identifier of the final test lot (harness/final_inventory.primary_case_id)."""
    return f"test-primary-{fault}-r{run:02d}"


def owner_by_fault(path: Path) -> dict[str, str]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    owners = {row["identifier"]: agent for agent, row in payload["assignment"].items()}
    if set(owners) != set(FAULTS):
        raise SystemExit("the agent assignment does not cover the eight catalogue faults")
    return owners


def family_seed(family: str, base_seed: int) -> int:
    digest = hashlib.sha256(f"{NAMESPACE}|{base_seed}|{family}".encode()).hexdigest()
    return int(digest[:12], 16)


def subsets(family_map: dict, family: str) -> list[str]:
    entry = family_map["subsets_S_F_proposal"][family]
    return list(entry["target_faults"]) + list(entry["control_faults"])


def build_derangements(family_map: dict, *, base_seed: int, runs: int) -> dict:
    out = {}
    for family in family_map["families"]:
        faults = subsets(family_map, family)
        cases = [case_id(fault, run) for fault in faults for run in range(1, runs + 1)]
        classes = [fault for fault in faults for _ in range(1, runs + 1)]
        seed = family_seed(family, base_seed)
        mapping = e5_derangement.sample(cases, classes, seed=seed)
        class_of = dict(zip(cases, classes))
        out[family] = {
            "column": family_map["families"][family]["column"],
            "subset_S_F": faults,
            "case_count": len(cases),
            "seed": seed,
            "attempts_until_valid": mapping["attempts"],
            "valid_map_fraction_exact": e5_derangement.exact_valid_fraction(classes),
            "pairs": mapping["pairs"],
            "pairing_matrix_recipient_from_donor":
                e5_derangement.pairing_matrix(mapping["pairs"], class_of),
            "same_mechanism_donor_note":
                "class-disjoint, NOT mechanism-disjoint: the donor may share the recipient's "
                "mechanism; the pairing matrix above is the declared documentation (8.12)",
        }
    return out


def _extra_matching(owners: dict[str, str], rng: random.Random) -> dict[str, str]:
    """A perfect matching fault -> agent with ``agent != owner(fault)``, uniform by rejection.

    With eight runs per fault and seven eligible recipients, one run of each fault needs a
    second turn from some agent. Giving those eight extras to eight distinct agents is what
    keeps the overall count at exactly eight runs per agent.
    """
    faults = list(FAULTS)
    agents = list(AGENTS)
    for _ in range(100_000):
        candidate = agents[:]
        rng.shuffle(candidate)
        matching = dict(zip(faults, candidate))
        if all(matching[fault] != owners[fault] for fault in faults):
            return matching
    raise SystemExit("no balanced extra matching found")


def build_recipients(owners: dict[str, str], *, mode: str, base_seed: int,
                     runs: int) -> dict:
    table: dict[str, list[str]] = {}
    rng = random.Random(family_seed("recipients", base_seed))
    extras = _extra_matching(owners, rng) if mode == "one" and runs == len(AGENTS) else {}
    if mode == "one" and not extras:
        raise SystemExit("the balanced extra matching assumes eight runs and eight agents")
    for fault in FAULTS:
        eligible = [agent for agent in AGENTS if agent != owners[fault]]
        if mode == "all":
            for run in range(1, runs + 1):
                table[case_id(fault, run)] = list(eligible)
            continue
        # mode "one": each of the seven non-owners once, plus one extra run. The extra
        # is not drawn per fault: the eight extras are a perfect matching fault -> agent
        # with agent != owner(fault), so every agent ends with exactly eight runs --
        # balanced within each fault AND overall, as 8.12 requires.
        order = eligible[:]
        rng.shuffle(order)
        order.append(extras[fault])
        rng.shuffle(order)
        for run, agent in zip(range(1, runs + 1), order):
            table[case_id(fault, run)] = [agent]
    counts: dict[str, int] = {}
    for recipients in table.values():
        for agent in recipients:
            counts[agent] = counts.get(agent, 0) + 1
    return {
        "mode": mode,
        "rule": ("one recipient per physical run, drawn among the seven non-owners, "
                 "balanced within each fault (each eligible agent once, one of them twice)"
                 if mode == "one" else
                 "all seven non-owner agents for every run (decision A option b)"),
        "seed": family_seed("recipients", base_seed),
        "owner_by_fault": owners,
        "assignments": table,
        "calls_per_family_arm": sum(len(value) for value in table.values()),
        "recipient_counts": dict(sorted(counts.items())),
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--assignment", type=Path, default=DEFAULT_ASSIGNMENT)
    parser.add_argument("--family-map", type=Path, default=DEFAULT_MAP)
    parser.add_argument("--mode", choices=("one", "all"), default="one",
                        help="decision A: one recipient per run, or all seven non-owners")
    parser.add_argument("--runs", type=int, default=PRIMARY_RUNS)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--out", type=Path, default=HERE)
    arguments = parser.parse_args(argv)

    family_map = json.loads(arguments.family_map.read_text(encoding="utf-8"))
    owners = owner_by_fault(arguments.assignment)
    derangements = build_derangements(family_map, base_seed=arguments.seed, runs=arguments.runs)
    recipients = build_recipients(owners, mode=arguments.mode, base_seed=arguments.seed,
                                  runs=arguments.runs)

    arguments.out.mkdir(parents=True, exist_ok=True)
    header = {
        "artifact_version": "E5_ASSIGNMENTS_1",
        "status": "PROPOSTA_NON_CONGELATA: dipende dalle decisioni A e C",
        "namespace": NAMESPACE,
        "base_seed": arguments.seed,
        "built_on": "identifiers only; no descriptor, no text, no outcome",
        "family_map_sha256": hashlib.sha256(
            arguments.family_map.read_bytes()).hexdigest(),
    }
    (arguments.out / "DERANGEMENTS_E5.json").write_text(
        json.dumps({**header, "derangements": derangements}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    (arguments.out / "RICEVENTI_E5.json").write_text(
        json.dumps({**header, "recipients": recipients}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    print(json.dumps({
        "derangement_cases": {family: value["case_count"]
                              for family, value in derangements.items()},
        "recipient_mode": recipients["mode"],
        "calls_per_family_arm": recipients["calls_per_family_arm"],
        "recipient_counts": recipients["recipient_counts"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
