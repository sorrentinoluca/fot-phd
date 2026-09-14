"""Presentation ordering kept separate from evaluator-side label ordering."""

from __future__ import annotations

from .common import HarnessError, sha256_text


PRESENTATION_NAMESPACE = "studio2-fase03-presentation-v1"


def presentation_order(label_space: list[str] | tuple[str, ...]) -> list[str]:
    labels = list(label_space)
    if len(labels) != 9 or labels[-1] != "Normal" or len(set(labels)) != 9:
        raise HarnessError("label_space must contain eight unique fault labels then Normal")
    faults = sorted(
        labels[:-1], key=lambda label: sha256_text(f"{PRESENTATION_NAMESPACE}|{label}")
    )
    return [*faults, "Normal"]


def spearman_against_catalog(
    ordered_labels: list[str] | tuple[str, ...],
    catalog_labels: list[str] | tuple[str, ...],
) -> float:
    left, right = list(ordered_labels), list(catalog_labels)
    if len(left) != len(right) or len(left) < 2 or set(left) != set(right):
        raise HarnessError("Spearman inputs must be permutations of the same labels")
    catalog_rank = {label: rank for rank, label in enumerate(right, start=1)}
    presented_rank = {label: rank for rank, label in enumerate(left, start=1)}
    squared = sum(
        (catalog_rank[label] - presented_rank[label]) ** 2 for label in catalog_rank
    )
    n = len(left)
    return 1.0 - (6.0 * squared) / (n * (n * n - 1))


