#!/usr/bin/env python3
"""Uniform sampling of the class-disjoint derangements of E5 (piano 8.12).

A valid map for family F is a permutation of the cases of the evaluated subset S_F that

* has no fixed point (no case keeps its own evidence of F), and
* never maps a case onto a case of its own class (disjoint by class, decided 2026-09-12).

Sampling is by rejection from uniform random permutations, so the result is **uniform on
the set of valid maps** and not merely "some valid map": rejection keeps the distribution
of the accepted sample equal to the uniform distribution restricted to the admissible set.
The acceptance rate is the ratio between valid maps and all permutations, and is reported.

The map is built on identifiers only: this module never sees a descriptor value.
"""

from __future__ import annotations

import random
from typing import Iterable, Sequence


class DerangementError(RuntimeError):
    pass


def is_valid(order: Sequence[int], classes: Sequence[str]) -> bool:
    """``order[i]`` is the donor index of recipient ``i``."""
    return all(donor != index and classes[donor] != classes[index]
               for index, donor in enumerate(order))


def feasible(classes: Sequence[str]) -> bool:
    """A class-disjoint map exists iff no class holds more than half of the cases."""
    if len(classes) < 2:
        return False
    counts: dict[str, int] = {}
    for name in classes:
        counts[name] = counts.get(name, 0) + 1
    return max(counts.values()) * 2 <= len(classes)


def sample(case_ids: Sequence[str], classes: Sequence[str], *, seed: int,
           max_attempts: int = 2_000_000) -> dict[str, object]:
    """Return one uniform class-disjoint derangement of ``case_ids``."""
    if len(case_ids) != len(classes):
        raise DerangementError("case_ids and classes have different lengths")
    if len(set(case_ids)) != len(case_ids):
        raise DerangementError("duplicate case id")
    if not feasible(classes):
        raise DerangementError(
            "no class-disjoint derangement exists: one class holds more than half the cases")
    rng = random.Random(seed)
    indices = list(range(len(case_ids)))
    for attempt in range(1, max_attempts + 1):
        order = indices[:]
        rng.shuffle(order)
        if is_valid(order, classes):
            return {
                "seed": seed,
                "attempts": attempt,
                "n": len(case_ids),
                "pairs": {case_ids[index]: case_ids[donor]
                          for index, donor in enumerate(order)},
                "donor_class": {case_ids[index]: classes[donor]
                                for index, donor in enumerate(order)},
            }
    raise DerangementError(f"no valid map found in {max_attempts} attempts")


def exact_valid_fraction(classes: Sequence[str]) -> float:
    """Exact fraction of permutations that are class-disjoint (hence fixed-point free).

    The forbidden cells form one square block per class, so inclusion-exclusion over
    non-attacking rook placements is exact and cheap: for a block of size m every k-subset
    contributes ``C(m,k)**2 * k!`` placements, the blocks convolve, and

        valid = sum_k (-1)**k * R_k * (n-k)!

    where ``R_k`` is the number of ways to place k non-attacking rooks on forbidden cells.
    A fixed point is a same-class cell, so it is already excluded.
    """
    from math import comb, factorial

    counts: dict[str, int] = {}
    for name in classes:
        counts[name] = counts.get(name, 0) + 1
    rooks = [1]
    for size in counts.values():
        block = [comb(size, k) ** 2 * factorial(k) for k in range(size + 1)]
        merged = [0] * (len(rooks) + len(block) - 1)
        for i, left in enumerate(rooks):
            for j, right in enumerate(block):
                merged[i + j] += left * right
        rooks = merged
    total = len(classes)
    valid = sum((-1) ** k * value * factorial(total - k)
                for k, value in enumerate(rooks) if k <= total)
    return valid / factorial(total)


def acceptance_rate(classes: Sequence[str], *, seed: int, trials: int = 20_000) -> float:
    rng = random.Random(seed)
    indices = list(range(len(classes)))
    accepted = 0
    for _ in range(trials):
        order = indices[:]
        rng.shuffle(order)
        accepted += is_valid(order, classes)
    return accepted / trials


def pairing_matrix(pairs: dict[str, str], class_of: dict[str, str]) -> dict[str, int]:
    """Counts of (recipient class -> donor class), the matrix 8.12 asks to document."""
    matrix: dict[str, int] = {}
    for recipient, donor in pairs.items():
        key = f"{class_of[recipient]}<-{class_of[donor]}"
        matrix[key] = matrix.get(key, 0) + 1
    return dict(sorted(matrix.items()))
