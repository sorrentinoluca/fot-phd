#!/usr/bin/env python3
"""NumPy-only implementation of the frozen local/FedAvg/centralized recipe."""

from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping

import numpy as np

LABELS = ("Normal", "F1", "F2", "F3", "F8", "F10", "F13", "F14", "F15")
CLIENTS = LABELS[1:]
DIMENSION = 697
PARAMETER_NAMES = ("w1", "b1", "w2", "b2")
FORBIDDEN_PARTS = {
    "test", "tests", "test_runs", "heldout", "held-out", "final_evaluation",
    "tep_exp3_v2_heldout",
}


@dataclass(frozen=True)
class Config:
    input_dim: int = DIMENSION
    hidden_dim: int = 32
    output_dim: int = len(LABELS)
    learning_rate: float = 0.05
    batch_size: int = 32
    local_epochs: int = 5
    rounds: int = 40
    seed: int = 20260914
    std_floor: float = 1e-8


@dataclass(frozen=True)
class Dataset:
    x: np.ndarray
    y: np.ndarray
    clients: np.ndarray
    clusters: np.ndarray
    batches: np.ndarray

    def __post_init__(self) -> None:
        n = len(self.x)
        if self.x.shape != (n, DIMENSION):
            raise ValueError(f"expected x shape (n, {DIMENSION}), got {self.x.shape}")
        if any(len(value) != n for value in (self.y, self.clients, self.clusters, self.batches)):
            raise ValueError("dataset columns have inconsistent lengths")
        if not np.isfinite(self.x).all():
            raise ValueError("dataset contains non-finite signatures")
        if not np.isin(self.y, np.arange(len(LABELS))).all():
            raise ValueError("dataset contains an unknown label index")
        if not np.isin(self.clients, np.asarray(CLIENTS)).all():
            raise ValueError("dataset contains an unknown client")
        cluster_batches: dict[str, set[str]] = {}
        for cluster, batch in zip(self.clusters, self.batches, strict=True):
            cluster_batches.setdefault(str(cluster), set()).add(str(batch))
        inconsistent = sorted(
            cluster for cluster, batches in cluster_batches.items() if len(batches) != 1
        )
        if inconsistent:
            raise ValueError(f"each physical run must map to one batch: {inconsistent}")


@dataclass(frozen=True)
class Normalizer:
    mean: np.ndarray
    scale: np.ndarray

    def transform(self, x: np.ndarray) -> np.ndarray:
        return (x - self.mean) / self.scale


@dataclass
class TrainedModel:
    parameters: dict[str, np.ndarray]
    normalizer: Normalizer
    visible_labels: tuple[int, ...]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def assert_development_path(path: Path) -> None:
    resolved = path.resolve()
    lowered = {part.lower() for part in resolved.parts}
    blocked = sorted(lowered.intersection(FORBIDDEN_PARTS))
    if blocked:
        raise ValueError(f"test/held-out path rejected by design: {resolved} ({blocked})")


def _confined_regular_file(path: Path, bundle_root: Path, role: str) -> Path:
    """Resolve one input before opening it and reject every symlink below the bundle root."""
    try:
        relative = path.relative_to(bundle_root)
    except ValueError as exc:
        raise ValueError(f"{role} is outside the evidence bundle: {path}") from exc
    current = bundle_root
    for component in relative.parts:
        current = current / component
        if current.is_symlink():
            raise ValueError(f"{role} symlink rejected by design: {current}")
    try:
        resolved = path.resolve(strict=True)
        resolved.relative_to(bundle_root)
    except (FileNotFoundError, ValueError) as exc:
        raise ValueError(f"{role} must resolve inside the evidence bundle: {path}") from exc
    assert_development_path(resolved)
    if not resolved.is_file():
        raise ValueError(f"{role} is not a regular file: {resolved}")
    return resolved


def _verified_digest(path: Path, expected: str, role: str) -> None:
    actual = sha256_file(path)
    if actual != expected:
        raise RuntimeError(f"{role} SHA-256 mismatch: expected {expected}, got {actual}")


def _read_signature(path: Path, expected_sha256: str) -> np.ndarray:
    _verified_digest(path, expected_sha256, "signature")
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if [int(row["component"]) for row in rows] != list(range(DIMENSION)):
        raise ValueError(f"signature components are not exactly 0..{DIMENSION - 1}: {path}")
    values = np.asarray([float(row["value"]) for row in rows], dtype=np.float64)
    if values.shape != (DIMENSION,) or not np.isfinite(values).all():
        raise ValueError(f"invalid 697-D finite signature: {path}")
    return values


def _client_from_index(row: Mapping[str, str], label: str) -> str:
    if label != "Normal":
        return label
    for key in ("client", "client_id", "agent_id", "owner_fault"):
        value = row.get(key, "")
        if value in CLIENTS:
            return value
        if value.startswith("agent_") and value[6:].isdigit():
            index = int(value[6:]) - 1
            if 0 <= index < len(CLIENTS):
                return CLIENTS[index]
    raise ValueError("Normal evidence must declare its exclusive client/agent assignment")


def load_evidence_bundle(
    root: Path,
    *,
    expected_manifest_sha256: str,
    expected_index_sha256: str,
) -> Dataset:
    """Load one published development bundle, verifying both indices and every signature."""
    assert_development_path(root)
    if root.is_symlink():
        raise ValueError(f"evidence bundle root symlink rejected by design: {root}")
    try:
        bundle_root = root.resolve(strict=True)
    except FileNotFoundError as exc:
        raise ValueError(f"evidence bundle does not exist: {root}") from exc
    if not bundle_root.is_dir():
        raise ValueError(f"evidence bundle root is not a directory: {bundle_root}")
    manifest_path = _confined_regular_file(
        bundle_root / "EVIDENCE_MANIFEST.csv", bundle_root, "evidence manifest"
    )
    index_path = _confined_regular_file(
        bundle_root / "EVALUATOR_INDEX.csv", bundle_root, "evaluator index"
    )
    _verified_digest(manifest_path, expected_manifest_sha256, "evidence manifest")
    _verified_digest(index_path, expected_index_sha256, "evaluator index")
    with manifest_path.open(newline="", encoding="utf-8") as handle:
        manifest = list(csv.DictReader(handle))
    with index_path.open(newline="", encoding="utf-8") as handle:
        index = list(csv.DictReader(handle))
    manifest_by_id = {row["evidence_id"]: row for row in manifest}
    index_by_id = {row["evidence_id"]: row for row in index}
    if len(manifest_by_id) != len(manifest) or len(index_by_id) != len(index):
        raise ValueError("evidence_id must be unique in both files")
    if manifest_by_id.keys() != index_by_id.keys():
        raise ValueError("manifest/evaluator index are not a one-to-one join")

    xs: list[np.ndarray] = []
    ys: list[int] = []
    clients: list[str] = []
    clusters: list[str] = []
    batches: list[str] = []
    for evidence_id in sorted(manifest_by_id):
        artifact = manifest_by_id[evidence_id]
        meta = index_by_id[evidence_id]
        if artifact.get("signature_dimension") != str(DIMENSION):
            raise ValueError(f"{evidence_id}: signature_dimension is not {DIMENSION}")
        if artifact.get("leakage_pass", "").lower() != "true":
            raise ValueError(f"{evidence_id}: leakage_pass is not true")
        label = meta.get("fault") or meta.get("label") or ""
        if label not in LABELS:
            raise ValueError(f"{evidence_id}: unknown label {label!r}")
        relative = Path(artifact["signature_path"])
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"{evidence_id}: unsafe signature_path")
        signature_path = _confined_regular_file(
            bundle_root / relative, bundle_root, f"{evidence_id} signature"
        )
        xs.append(_read_signature(signature_path, artifact["signature_sha256"]))
        ys.append(LABELS.index(label))
        clients.append(_client_from_index(meta, label))
        clusters.append(meta["run_id"])
        batches.append(str(meta["batch"]))
    return Dataset(
        x=np.stack(xs),
        y=np.asarray(ys, dtype=np.int64),
        clients=np.asarray(clients),
        clusters=np.asarray(clusters),
        batches=np.asarray(batches),
    )


def concatenate(datasets: Iterable[Dataset]) -> Dataset:
    values = tuple(datasets)
    if not values:
        raise ValueError("at least one dataset is required")
    return Dataset(
        x=np.concatenate([item.x for item in values]),
        y=np.concatenate([item.y for item in values]),
        clients=np.concatenate([item.clients for item in values]),
        clusters=np.concatenate([item.clusters for item in values]),
        batches=np.concatenate([item.batches for item in values]),
    )


def split_leave_one_batch_out(dataset: Dataset, held_out_batch: str) -> tuple[Dataset, Dataset]:
    held_out = dataset.batches == str(held_out_batch)
    if not held_out.any() or held_out.all():
        raise ValueError("held-out batch must create two non-empty folds")
    training = _subset(dataset, ~held_out)
    validation = _subset(dataset, held_out)
    overlap = sorted(set(training.clusters.tolist()).intersection(validation.clusters.tolist()))
    if overlap:
        raise ValueError(f"physical runs cross training/validation folds: {overlap}")
    return training, validation


def _subset(dataset: Dataset, mask: np.ndarray) -> Dataset:
    return Dataset(dataset.x[mask], dataset.y[mask], dataset.clients[mask],
                   dataset.clusters[mask], dataset.batches[mask])


def fit_normalizer(x: np.ndarray, floor: float) -> Normalizer:
    mean = x.mean(axis=0, dtype=np.float64)
    scale = x.std(axis=0, dtype=np.float64)
    scale = np.where(scale < floor, 1.0, scale)
    return Normalizer(mean, scale)


def stable_seed(base: int, *parts: object) -> int:
    payload = "|".join((str(base), *(str(part) for part in parts))).encode("utf-8")
    return int.from_bytes(hashlib.sha256(payload).digest()[:8], "little")


def initialize(config: Config, *, seed: int | None = None) -> dict[str, np.ndarray]:
    rng = np.random.Generator(np.random.PCG64(config.seed if seed is None else seed))
    limit1 = np.sqrt(6.0 / (config.input_dim + config.hidden_dim))
    limit2 = np.sqrt(6.0 / (config.hidden_dim + config.output_dim))
    return {
        "w1": rng.uniform(-limit1, limit1, (config.input_dim, config.hidden_dim)),
        "b1": np.zeros(config.hidden_dim, dtype=np.float64),
        "w2": rng.uniform(-limit2, limit2, (config.hidden_dim, config.output_dim)),
        "b2": np.zeros(config.output_dim, dtype=np.float64),
    }


def copy_parameters(parameters: Mapping[str, np.ndarray]) -> dict[str, np.ndarray]:
    return {name: np.asarray(parameters[name], dtype=np.float64).copy() for name in PARAMETER_NAMES}


def class_weights(y: np.ndarray) -> np.ndarray:
    present, counts = np.unique(y, return_counts=True)
    result = np.zeros(len(LABELS), dtype=np.float64)
    result[present] = len(y) / (len(present) * counts)
    return result


def _sgd_epoch(
    parameters: dict[str, np.ndarray], x: np.ndarray, y: np.ndarray,
    weights: np.ndarray, config: Config, rng: np.random.Generator,
) -> None:
    order = rng.permutation(len(x))
    for start in range(0, len(x), config.batch_size):
        idx = order[start:start + config.batch_size]
        xb, yb = x[idx], y[idx]
        hidden_pre = xb @ parameters["w1"] + parameters["b1"]
        hidden = np.maximum(hidden_pre, 0.0)
        logits = hidden @ parameters["w2"] + parameters["b2"]
        logits -= logits.max(axis=1, keepdims=True)
        probabilities = np.exp(logits)
        probabilities /= probabilities.sum(axis=1, keepdims=True)
        sample_weights = weights[yb]
        denom = sample_weights.sum()
        grad_logits = probabilities
        grad_logits[np.arange(len(yb)), yb] -= 1.0
        grad_logits *= (sample_weights / denom)[:, None]
        grad_w2 = hidden.T @ grad_logits
        grad_b2 = grad_logits.sum(axis=0)
        grad_hidden = (grad_logits @ parameters["w2"].T) * (hidden_pre > 0.0)
        grad_w1 = xb.T @ grad_hidden
        grad_b1 = grad_hidden.sum(axis=0)
        for name, gradient in zip(PARAMETER_NAMES, (grad_w1, grad_b1, grad_w2, grad_b2)):
            parameters[name] -= config.learning_rate * gradient


def train_steps(
    initial: Mapping[str, np.ndarray], x: np.ndarray, y: np.ndarray,
    config: Config, *, epochs: int, seed_parts: tuple[object, ...],
) -> dict[str, np.ndarray]:
    parameters = copy_parameters(initial)
    weights = class_weights(y)
    for epoch in range(epochs):
        rng = np.random.Generator(np.random.PCG64(stable_seed(config.seed, *seed_parts, epoch)))
        _sgd_epoch(parameters, x, y, weights, config, rng)
    return parameters


def aggregate_parameter_sets(
    parameter_sets: Iterable[Mapping[str, np.ndarray]], sample_counts: Iterable[int],
) -> dict[str, np.ndarray]:
    sets, counts = tuple(parameter_sets), np.asarray(tuple(sample_counts), dtype=np.float64)
    if not sets or len(sets) != len(counts) or (counts <= 0).any():
        raise ValueError("parameter sets need matching positive sample counts")
    fractions = counts / counts.sum()
    return {
        name: np.sum(np.stack([item[name] for item in sets]) *
                     fractions.reshape((-1,) + (1,) * sets[0][name].ndim), axis=0)
        for name in PARAMETER_NAMES
    }


def train_local(dataset: Dataset, config: Config) -> dict[str, TrainedModel]:
    result: dict[str, TrainedModel] = {}
    for client in CLIENTS:
        mask = dataset.clients == client
        if set(np.unique(dataset.y[mask])) != {0, LABELS.index(client)}:
            raise ValueError(f"client {client} must contain exactly Normal and its own fault")
        normalizer = fit_normalizer(dataset.x[mask], config.std_floor)
        initial = initialize(config)
        parameters = train_steps(
            initial, normalizer.transform(dataset.x[mask]), dataset.y[mask], config,
            epochs=config.rounds * config.local_epochs, seed_parts=("local", client),
        )
        result[client] = TrainedModel(parameters, normalizer, (0, LABELS.index(client)))
    return result


def train_fedavg(dataset: Dataset, config: Config) -> TrainedModel:
    normalizer = fit_normalizer(dataset.x, config.std_floor)
    normalized = normalizer.transform(dataset.x)
    global_parameters = initialize(config)
    for round_index in range(config.rounds):
        updates: list[dict[str, np.ndarray]] = []
        counts: list[int] = []
        for client in CLIENTS:
            mask = dataset.clients == client
            if not mask.any():
                raise ValueError(f"client {client} has no training examples")
            updates.append(train_steps(
                global_parameters, normalized[mask], dataset.y[mask], config,
                epochs=config.local_epochs, seed_parts=("fedavg", round_index, client),
            ))
            counts.append(int(mask.sum()))
        global_parameters = aggregate_parameter_sets(updates, counts)
    return TrainedModel(global_parameters, normalizer, tuple(range(len(LABELS))))


def train_centralized(dataset: Dataset, config: Config) -> TrainedModel:
    normalizer = fit_normalizer(dataset.x, config.std_floor)
    parameters = train_steps(
        initialize(config), normalizer.transform(dataset.x), dataset.y, config,
        epochs=config.rounds * config.local_epochs, seed_parts=("centralized",),
    )
    return TrainedModel(parameters, normalizer, tuple(range(len(LABELS))))


def train_all_modes(dataset: Dataset, config: Config = Config()) -> dict[str, object]:
    return {
        "local": train_local(dataset, config),
        "fedavg": train_fedavg(dataset, config),
        "centralized": train_centralized(dataset, config),
    }


def predict(model: TrainedModel, x: np.ndarray) -> np.ndarray:
    normalized = model.normalizer.transform(x)
    hidden = np.maximum(normalized @ model.parameters["w1"] + model.parameters["b1"], 0.0)
    logits = hidden @ model.parameters["w2"] + model.parameters["b2"]
    mask = np.ones(len(LABELS), dtype=bool)
    mask[list(model.visible_labels)] = False
    logits[:, mask] = -np.inf
    return logits.argmax(axis=1)


def weights_sha256(model: TrainedModel) -> str:
    digest = hashlib.sha256()
    for name in PARAMETER_NAMES:
        array = np.ascontiguousarray(model.parameters[name], dtype="<f8")
        digest.update(name.encode("ascii") + b"\0")
        digest.update(np.asarray(array.shape, dtype="<i8").tobytes())
        digest.update(array.tobytes())
    for name, array in (("mean", model.normalizer.mean), ("scale", model.normalizer.scale)):
        digest.update(name.encode("ascii") + b"\0")
        digest.update(np.ascontiguousarray(array, dtype="<f8").tobytes())
    return digest.hexdigest()


METRIC_FIELDS = (
    "mode", "cluster_id", "true_label", "receiver", "n_attempts", "correct", "accuracy",
    "abstentions", "abstention_rate", "non_abstained", "accuracy_non_abstained",
)


def cluster_metrics(mode: str, model: TrainedModel, dataset: Dataset, receiver: str) -> list[dict[str, object]]:
    predictions = predict(model, dataset.x)
    rows: list[dict[str, object]] = []
    for cluster in sorted(set(dataset.clusters.tolist())):
        mask = dataset.clusters == cluster
        correct = int((predictions[mask] == dataset.y[mask]).sum())
        n = int(mask.sum())
        rows.append({
            "mode": mode,
            "cluster_id": cluster,
            "receiver": receiver,
            "true_label": LABELS[int(dataset.y[mask][0])],
            "n_attempts": n,
            "correct": correct,
            "accuracy": correct / n,
            "abstentions": 0,
            "abstention_rate": 0.0,
            "non_abstained": n,
            "accuracy_non_abstained": correct / n,
        })
    return rows


def evaluate_all_modes(models: Mapping[str, object], dataset: Dataset) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    local = models["local"]
    if not isinstance(local, dict):
        raise TypeError("local models must be a mapping")
    for client in CLIENTS:
        rows.extend(cluster_metrics("local", local[client], dataset, client))
    for mode in ("fedavg", "centralized"):
        model = models[mode]
        if not isinstance(model, TrainedModel):
            raise TypeError(f"{mode} model has an invalid type")
        rows.extend(cluster_metrics(mode, model, dataset, "shared"))
    return rows


def write_metrics(path: Path, rows: Iterable[Mapping[str, object]]) -> None:
    fields = (
        "mode", "cluster_id", "receiver", "true_label", "n_attempts", "correct",
        "accuracy", "abstentions", "abstention_rate", "non_abstained",
        "accuracy_non_abstained",
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_weight_hashes(path: Path, models: Mapping[str, object]) -> None:
    local = models["local"]
    payload = {
        "schema_version": 1,
        "numpy_version": np.__version__,
        "local": {client: weights_sha256(local[client]) for client in CLIENTS},
        "fedavg": weights_sha256(models["fedavg"]),
        "centralized": weights_sha256(models["centralized"]),
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
