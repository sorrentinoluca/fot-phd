#!/usr/bin/env python3
"""Run the frozen centralized supervisor-model suite for C02b."""

from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import io
import json
import pickle
from pathlib import Path
import random
import sys
from typing import Any
import warnings

import numpy as np
import pandas as pd
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
import sklearn
import torch
from torch import nn


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
CODE = ROOT / "code"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(CODE) not in sys.path:
    sys.path.insert(0, str(CODE))

from evaluate_verbalizer_v2 import signature_vector  # noqa: E402
from tep_features import XMEAS, load_case  # noqa: E402
from tep_verbalize_v2 import (  # noqa: E402
    load_config as load_v2_config,
    load_development_baseline,
    verbalize_case,
)
from phase_b.baselines.c02b_shared_numeric_prototypes.run_baseline import (  # noqa: E402
    normal_blocks,
    verify_protocol as verify_parent_protocol,
)


CONFIG_PATH = HERE / "protocol_config.json"
FREEZE_PATH = HERE / "protocol_freeze_manifest.json"
DEFAULT_OUTPUT_DIR = HERE / "results"
PARENT_RESULTS = ROOT / "phase_b/baselines/c02b_shared_numeric_prototypes/results"
SOURCE_MAP_PATH = ROOT / "phase_b/final_evaluation/evaluator_side/heldout_source_mapping.json"
TRUTH_PATH = ROOT / "phase_b/heldout/phase_b_heldout_manifest.csv"
MAPPING_PATH = ROOT / "phase_b/config/evaluator_side/pseudolabel_mapping.json"
HELDOUT_DIR = ROOT / "tep_heldout/mode1"
MODEL_ORDER = (
    "adaboost",
    "random_forest",
    "mlp",
    "linear_elastic_net",
    "knn",
    "lstm_causal_attention",
    "bilstm_attention",
    "multimodal_bilstm_attention_tfidf",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False)
        + "\n"
    ).encode("utf-8")


def csv_bytes(rows: list[dict[str, Any]], fieldnames: list[str]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def write_deterministic(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() != content:
        raise RuntimeError(f"refusing to overwrite different output: {path}")
    path.write_bytes(content)


def canonical_torch_state_bytes(model: nn.Module) -> bytes:
    """Serialize a state dict without timestamps or pickle storage identifiers."""
    stream = io.BytesIO()
    stream.write(b"C02B_TORCH_STATE_V1\n")
    for name, tensor in sorted(model.state_dict().items()):
        array = np.ascontiguousarray(tensor.detach().cpu().numpy())
        if array.dtype.byteorder == ">":
            array = array.byteswap().view(array.dtype.newbyteorder("<"))
        payload = array.tobytes(order="C")
        metadata = {
            "bytes": len(payload),
            "dtype": array.dtype.str,
            "name": name,
            "shape": list(array.shape),
        }
        stream.write(json_bytes(metadata))
        stream.write(payload)
        stream.write(b"\n")
    return stream.getvalue()


def verify_protocol() -> dict[str, Any]:
    freeze = load_json(FREEZE_PATH)
    if freeze["status"] != "FROZEN_BEFORE_MODEL_EVALUATION":
        raise RuntimeError("suite freeze status mismatch")
    for relative, expected in freeze["artifacts"].items():
        if sha256_file(ROOT / relative) != expected:
            raise RuntimeError(f"suite protocol artifact hash mismatch: {relative}")
    config = load_json(CONFIG_PATH)
    if config["status"] != "FROZEN_BEFORE_MODEL_EVALUATION":
        raise RuntimeError("suite config is not frozen")
    for relative, expected in config["frozen_parent_artifact_hashes"].items():
        if sha256_file(ROOT / relative) != expected:
            raise RuntimeError(f"upstream hash mismatch: {relative}")
    verify_parent_protocol()
    expected = config["software"]
    actual = {
        "numpy": np.__version__,
        "pandas": pd.__version__,
        "scikit_learn": sklearn.__version__,
        "torch": torch.__version__.split("+")[0],
    }
    for name, version in actual.items():
        if version != expected[name]:
            raise RuntimeError(f"software version mismatch for {name}: {version}")
    if not sys.version.split()[0].startswith(expected["python"]):
        raise RuntimeError("Python version mismatch")
    return config


def set_determinism(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.use_deterministic_algorithms(True)
    torch.set_num_threads(1)


def validate_finite(name: str, value: np.ndarray, shape: tuple[int, ...]) -> np.ndarray:
    array = np.asarray(value)
    if array.shape != shape:
        raise RuntimeError(f"{name}: expected shape {shape}, found {array.shape}")
    if not np.all(np.isfinite(array)):
        raise RuntimeError(f"{name}: non-finite value")
    return array


def sequence_rows(frame: pd.DataFrame, config: dict[str, Any]) -> np.ndarray:
    seq_config = config["representations"]["sequence"]
    start, end = map(float, seq_config["interval_h"])
    segment = frame[(frame.Time >= start) & (frame.Time < end)]
    expected_raw = int((end - start) * 60)
    if len(segment) != expected_raw:
        raise RuntimeError(f"expected {expected_raw} one-minute rows, found {len(segment)}")
    stride = int(seq_config["stride_minutes"])
    sequence = segment[XMEAS].to_numpy(dtype=np.float64)[::stride]
    return validate_finite(
        "raw sequence",
        sequence,
        (int(seq_config["steps"]), int(seq_config["channels"])),
    )


def fit_sequence_normalizer(
    normal_frames: list[pd.DataFrame], config: dict[str, Any]
) -> tuple[np.ndarray, np.ndarray]:
    pooled = np.concatenate([sequence_rows(frame, config) for frame in normal_frames])
    mean = pooled.mean(axis=0)
    std = pooled.std(axis=0, ddof=1)
    if np.any(~np.isfinite(std)) or np.any(std <= 1e-12):
        raise RuntimeError("degenerate development-only sequence normalizer")
    return mean, std


def normalize_sequence(
    raw: np.ndarray, mean: np.ndarray, std: np.ndarray
) -> np.ndarray:
    normalized = np.clip((raw - mean) / std, -10.0, 10.0) / 10.0
    if not np.all(np.isfinite(normalized)):
        raise RuntimeError("non-finite normalized sequence")
    return normalized.astype(np.float32)


def represent_frame(
    frame: pd.DataFrame,
    baseline: Any,
    v2_config: dict[str, Any],
    sequence_mean: np.ndarray,
    sequence_std: np.ndarray,
    config: dict[str, Any],
) -> tuple[np.ndarray, np.ndarray, str]:
    rendered = verbalize_case(
        frame,
        baseline,
        config=v2_config,
        start_h=10.0,
        end_h=50.0,
    )
    signature = np.asarray(signature_vector(rendered["structured"]), dtype=np.float64)
    validate_finite("signature", signature, (697,))
    if np.any((signature < 0.0) | (signature > 1.0)):
        raise RuntimeError("signature component outside [0,1]")
    sequence = normalize_sequence(
        sequence_rows(frame, config), sequence_mean, sequence_std
    )
    text = rendered["text"]
    if not isinstance(text, str) or not text.strip():
        raise RuntimeError("empty neutral verbalization")
    return signature, sequence, text


def build_development(
    config: dict[str, Any],
) -> tuple[list[dict[str, Any]], np.ndarray, np.ndarray, Any, dict[str, Any]]:
    mapping = load_json(MAPPING_PATH)["real_to_opaque"]
    v2_config = load_v2_config(CODE / "verbalizer_config_v2.json")
    normal_path = CODE / "tep_cache/mode1_normal_500.xlsx"
    baseline = load_development_baseline(normal_path, v2_config)
    blocks = normal_blocks(normal_path)
    sequence_mean, sequence_std = fit_sequence_normalizer(list(blocks.values()), config)
    rows: list[tuple[str, str, Path | None, pd.DataFrame]] = []
    for real_label, opaque_label in mapping.items():
        fault = int(real_label[1:])
        for batch in config["task"]["development_fault_batches"]:
            path = CODE / "tep_cache" / f"mode1_{fault}_{batch}.xlsx"
            rows.append((f"{opaque_label}-B{batch}", opaque_label, path, load_case(path)))
    for block_name, frame in blocks.items():
        rows.append((block_name, "Normal", None, frame))
    records = []
    for case_id, label, path, frame in rows:
        signature, sequence, text = represent_frame(
            frame, baseline, v2_config, sequence_mean, sequence_std, config
        )
        records.append(
            {
                "case_id": case_id,
                "opaque_label": label,
                "source_path": (
                    str(path.relative_to(ROOT))
                    if path is not None
                    else "code/tep_cache/mode1_normal_500.xlsx"
                ),
                "signature": signature,
                "sequence": sequence,
                "text": text,
            }
        )
    counts = Counter(record["opaque_label"] for record in records)
    if set(counts) != set(config["task"]["labels"]) or set(counts.values()) != {5}:
        raise RuntimeError(f"development class coverage mismatch: {counts}")
    return records, sequence_mean, sequence_std, baseline, v2_config


def build_heldout_without_truth(
    config: dict[str, Any],
    sequence_mean: np.ndarray,
    sequence_std: np.ndarray,
    baseline: Any,
    v2_config: dict[str, Any],
) -> list[dict[str, Any]]:
    source_map = load_json(SOURCE_MAP_PATH)
    records = []
    for item in source_map["cases"]:
        path = HELDOUT_DIR / item["source_filename"]
        if sha256_file(path) != item["source_file_sha256"]:
            raise RuntimeError(f"held-out source hash mismatch: {path.name}")
        signature, sequence, text = represent_frame(
            load_case(path), baseline, v2_config, sequence_mean, sequence_std, config
        )
        records.append(
            {
                "physical_case_id": item["physical_case_id"],
                "signature": signature,
                "sequence": sequence,
                "text": text,
            }
        )
    ids = [record["physical_case_id"] for record in records]
    if ids != config["task"]["heldout_physical_case_ids"]:
        raise RuntimeError("held-out order or coverage mismatch")
    return records


def classical_models(config: dict[str, Any]) -> dict[str, Any]:
    seed = int(config["random_seed"])
    return {
        "adaboost": AdaBoostClassifier(
            n_estimators=200, learning_rate=0.5, random_state=seed
        ),
        "random_forest": RandomForestClassifier(
            n_estimators=500,
            max_features="sqrt",
            class_weight="balanced",
            random_state=seed,
            n_jobs=1,
        ),
        "mlp": Pipeline(
            [
                ("scale", StandardScaler()),
                (
                    "model",
                    MLPClassifier(
                        hidden_layer_sizes=(128, 64),
                        activation="relu",
                        solver="lbfgs",
                        alpha=0.001,
                        max_iter=2000,
                        random_state=seed,
                    ),
                ),
            ]
        ),
        "linear_elastic_net": Pipeline(
            [
                ("scale", StandardScaler()),
                (
                    "model",
                    SGDClassifier(
                        loss="log_loss",
                        penalty="elasticnet",
                        alpha=0.001,
                        l1_ratio=0.5,
                        max_iter=5000,
                        tol=1e-5,
                        random_state=seed,
                    ),
                ),
            ]
        ),
        "knn": Pipeline(
            [
                ("scale", StandardScaler()),
                (
                    "model",
                    KNeighborsClassifier(n_neighbors=3, weights="distance", p=2),
                ),
            ]
        ),
    }


class AttentionPool(nn.Module):
    def __init__(self, dimensions: int) -> None:
        super().__init__()
        self.score = nn.Linear(dimensions, 1)

    def forward(self, states: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        weights = torch.softmax(self.score(states).squeeze(-1), dim=1)
        pooled = torch.sum(states * weights.unsqueeze(-1), dim=1)
        return pooled, weights


class LSTMAttentionClassifier(nn.Module):
    def __init__(
        self, input_size: int, hidden_size: int, classes: int, bidirectional: bool
    ) -> None:
        super().__init__()
        self.bidirectional = bidirectional
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            batch_first=True,
            bidirectional=bidirectional,
        )
        dimensions = hidden_size * (2 if bidirectional else 1)
        self.attention = AttentionPool(dimensions)
        self.classifier = nn.Linear(dimensions, classes)

    def forward(self, sequence: torch.Tensor) -> torch.Tensor:
        states, _ = self.lstm(sequence)
        pooled, _ = self.attention(states)
        return self.classifier(pooled)


class MultimodalLSTMAttentionClassifier(nn.Module):
    def __init__(self, input_size: int, hidden_size: int, text_size: int, classes: int):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            batch_first=True,
            bidirectional=True,
        )
        self.attention = AttentionPool(hidden_size * 2)
        self.text_branch = nn.Sequential(nn.Linear(text_size, 32), nn.ReLU())
        self.fusion = nn.Sequential(
            nn.Linear(hidden_size * 2 + 32, 64),
            nn.ReLU(),
            nn.Linear(64, classes),
        )

    def forward(self, sequence: torch.Tensor, text: torch.Tensor) -> torch.Tensor:
        states, _ = self.lstm(sequence)
        temporal, _ = self.attention(states)
        textual = self.text_branch(text)
        return self.fusion(torch.cat([temporal, textual], dim=1))


def select_predictions(
    scores: np.ndarray, score_labels: list[str], tolerance: float = 1e-12
) -> list[str]:
    predictions = []
    for row in scores:
        maximum = float(np.max(row))
        tied = sorted(
            score_labels[index]
            for index, value in enumerate(row)
            if abs(float(value) - maximum) <= tolerance
        )
        predictions.append(tied[0])
    return predictions


def train_torch_model(
    name: str,
    model: nn.Module,
    train_sequence: np.ndarray,
    train_text: np.ndarray | None,
    train_targets: np.ndarray,
    test_sequence: np.ndarray,
    test_text: np.ndarray | None,
    config: dict[str, Any],
) -> tuple[np.ndarray, np.ndarray, bytes, dict[str, Any]]:
    training = config["neural_training"]
    sequence_train = torch.from_numpy(train_sequence)
    target_train = torch.from_numpy(train_targets.astype(np.int64))
    sequence_test = torch.from_numpy(test_sequence)
    text_train = torch.from_numpy(train_text) if train_text is not None else None
    text_test_tensor = torch.from_numpy(test_text) if test_text is not None else None
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=float(training["learning_rate"]),
        weight_decay=float(training["weight_decay"]),
    )
    criterion = nn.CrossEntropyLoss()
    losses = []
    model.train()
    for _ in range(int(training["epochs"])):
        optimizer.zero_grad(set_to_none=True)
        logits = (
            model(sequence_train, text_train)
            if text_train is not None
            else model(sequence_train)
        )
        loss = criterion(logits, target_train)
        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), float(training["gradient_clip_norm"]))
        optimizer.step()
        losses.append(float(loss.detach()))
    model.eval()
    with torch.no_grad():
        train_logits = (
            model(sequence_train, text_train)
            if text_train is not None
            else model(sequence_train)
        )
        test_logits = (
            model(sequence_test, text_test_tensor)
            if text_test_tensor is not None
            else model(sequence_test)
        )
        train_scores = torch.softmax(train_logits, dim=1).cpu().numpy()
        test_scores = torch.softmax(test_logits, dim=1).cpu().numpy()
    state_bytes = canonical_torch_state_bytes(model)
    history = {
        "model": name,
        "epochs": int(training["epochs"]),
        "initial_loss": losses[0],
        "final_loss": losses[-1],
        "minimum_loss": min(losses),
        "loss_by_epoch": losses,
    }
    return train_scores, test_scores, state_bytes, history


def truth_by_case(config: dict[str, Any]) -> dict[str, str]:
    mapping = load_json(MAPPING_PATH)["real_to_opaque"]
    truth = {}
    with TRUTH_PATH.open(encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream):
            if row["case_id"] not in config["task"]["heldout_physical_case_ids"]:
                continue
            label = row["class_offline"]
            truth[row["case_id"]] = "Normal" if label == "Normal" else mapping[label]
    if set(truth) != set(config["task"]["heldout_physical_case_ids"]):
        raise RuntimeError("truth case coverage mismatch")
    return truth


def projected_scope(agent: str, true_label: str, config: dict[str, Any]) -> str:
    if true_label == "Normal":
        return "normal"
    return "local_seen" if config["task"]["agents"][agent] == true_label else "local_unseen"


def metric_block(rows: list[dict[str, Any]]) -> dict[str, Any]:
    n = len(rows)
    correct = sum(int(row["correct"]) for row in rows)
    return {"n": n, "correct": correct, "accuracy": correct / n if n else None}


def bootstrap_interval(
    rows: list[dict[str, Any]], labels: list[str], draws: int, seed: int
) -> dict[str, Any]:
    rng = np.random.default_rng(seed)
    grouped = {
        label: [row for row in rows if row["true_pseudolabel"] == label]
        for label in labels
    }
    values = []
    for _ in range(draws):
        sampled = []
        for group in grouped.values():
            indices = rng.integers(0, len(group), size=len(group))
            sampled.extend(group[int(index)] for index in indices)
        values.append(sum(int(row["correct"]) for row in sampled) / len(sampled))
    low, high = np.quantile(values, [0.025, 0.975])
    return {
        "method": "stratified physical-case bootstrap",
        "draws": draws,
        "seed": seed,
        "confidence_level": 0.95,
        "lower": float(low),
        "upper": float(high),
    }


def evaluate(
    scored: list[dict[str, Any]],
    training_accuracy: dict[str, float],
    model_bytes: dict[str, int],
    config: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    metrics: dict[str, Any] = {}
    confusion: dict[str, Any] = {}
    labels = config["task"]["labels"]
    for model_name in MODEL_ORDER:
        model_rows = [row for row in scored if row["model"] == model_name]
        fault_rows = [row for row in model_rows if row["true_pseudolabel"] != "Normal"]
        normal_rows = [row for row in model_rows if row["true_pseudolabel"] == "Normal"]
        projected = []
        for row in model_rows:
            for agent in config["task"]["agents"]:
                projected.append(
                    {
                        **row,
                        "agent_id": agent,
                        "scope": projected_scope(agent, row["true_pseudolabel"], config),
                    }
                )
        metrics[model_name] = {
            "physical_cases": metric_block(model_rows),
            "fault_cases": metric_block(fault_rows),
            "normal_cases": metric_block(normal_rows),
            "projected_local_seen": metric_block(
                [row for row in projected if row["scope"] == "local_seen"]
            ),
            "projected_local_unseen": metric_block(
                [row for row in projected if row["scope"] == "local_unseen"]
            ),
            "per_class": {
                label: metric_block(
                    [row for row in model_rows if row["true_pseudolabel"] == label]
                )
                for label in labels
            },
            "training_accuracy": training_accuracy[model_name],
            "serialized_model_bytes": model_bytes[model_name],
            "bootstrap_95_physical_accuracy": bootstrap_interval(
                model_rows,
                labels,
                int(config["metrics"]["confidence_interval"]["draws"]),
                int(config["metrics"]["confidence_interval"]["seed"]),
            ),
        }
        matrix = {
            true: {predicted: 0 for predicted in labels}
            for true in labels
        }
        for row in model_rows:
            matrix[row["true_pseudolabel"]][row["predicted_pseudolabel"]] += 1
        confusion[model_name] = {"labels": labels, "matrix": matrix}
    return metrics, confusion


def report_text(
    metrics: dict[str, Any], confusion: dict[str, Any], config: dict[str, Any]
) -> str:
    display = {
        "adaboost": "AdaBoost",
        "random_forest": "Random Forest",
        "mlp": "MLP",
        "linear_elastic_net": "Lineare elastic-net",
        "knn": "k-NN",
        "lstm_causal_attention": "LSTM causale + attention",
        "bilstm_attention": "BiLSTM + attention",
        "multimodal_bilstm_attention_tfidf": "BiLSTM multimodale + attention",
    }
    lines = [
        "# C02b — confronti richiesti dal supervisor",
        "",
        "## Esito in breve",
        "",
        "Sono stati eseguiti tutti i gruppi richiesti: boosting, MLP, Random Forest, "
        "lineare elastic-net, k-NN, LSTM causale con attention, BiLSTM con attention "
        "e una BiLSTM multimodale sequenza+testo. I risultati sotto sono riferimenti "
        "centralizzati: vedono tutte le pseudoclassi nei soli dati development e non "
        "sono presentati come metodi federati.",
        "",
        "## Risultati held-out",
        "",
        "| Modello | 15 casi | 12 fault | Local-unseen proiettato | Train | Modello byte | Bootstrap 95% |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for name in MODEL_ORDER:
        item = metrics[name]
        physical = item["physical_cases"]
        fault = item["fault_cases"]
        unseen = item["projected_local_unseen"]
        interval = item["bootstrap_95_physical_accuracy"]
        lines.append(
            f"| {display[name]} | {physical['correct']}/{physical['n']} "
            f"({physical['accuracy']:.1%}) | {fault['correct']}/{fault['n']} "
            f"({fault['accuracy']:.1%}) | {unseen['correct']}/{unseen['n']} "
            f"({unseen['accuracy']:.1%}) | {item['training_accuracy']:.1%} | "
            f"{item['serialized_model_bytes']} | "
            f"[{interval['lower']:.1%}, {interval['upper']:.1%}] |"
        )
    lines.extend(
        [
            "",
            "## Confronti già disponibili",
            "",
            "La baseline class-disjoint a prototipi condivisi rimane il confronto "
            "diretto: 36/36 local-unseen (100%). FoT-B ha ottenuto 31/36 (86,1%). "
            "Questi denominatori sono viste agente-caso; l'incertezza continua a usare "
            "i 12 casi fisici fault. Non si deve usare la tabella centralizzata per "
            "sostenere una superiorità federata.",
            "",
            "## Recall per pseudoclasse",
            "",
            "| Modello | CLS-ZOGAA | CLS-OJNSG | CLS-R463B | CLS-Z3ISU | Normal |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for name in MODEL_ORDER:
        values = []
        for label in config["task"]["labels"]:
            item = metrics[name]["per_class"][label]
            values.append(f"{item['correct']}/{item['n']}")
        lines.append(f"| {display[name]} | " + " | ".join(values) + " |")
    lines.extend(
        [
            "",
            "## Matrici di confusione",
            "",
            "Righe = verità, colonne = predizione; ogni riga contiene tre casi fisici.",
            "",
        ]
    )
    labels = config["task"]["labels"]
    for name in MODEL_ORDER:
        lines.extend(
            [
                f"### {display[name]}",
                "",
                "| Vera \\ Predetta | " + " | ".join(labels) + " |",
                "|---|" + "---:|" * len(labels),
            ]
        )
        for true in labels:
            values = [str(confusion[name]["matrix"][true][pred]) for pred in labels]
            lines.append(f"| {true} | " + " | ".join(values) + " |")
        lines.append("")
    lines.extend(
        [
            "## Interpretazione e limiti",
            "",
            "- I modelli hanno soltanto cinque casi development per classe: il confronto "
            "è molto piccolo e gli intervalli riflettono appena 15 casi held-out.",
            "- LSTM causale e BiLSTM sono varianti separate: una rete bidirezionale non "
            "è causale in senso stretto.",
            "- La variante multimodale usa due rappresentazioni degli stessi sensori "
            "(sequenza numerica e testo neutro), non una seconda sorgente fisica indipendente.",
            "- MLP, lineare e k-NN usano scaling fit solo sul development; nessun metodo "
            "usa il test per preprocessing, tuning o vocabolario.",
            "- Questi modelli centralizzano i dati e quindi non risolvono da soli C02b. "
            "Lo stato resta **Mitigata**, non 'risolta sperimentalmente'.",
            "",
            "## Riproducibilità",
            "",
            "Protocollo, configurazione, predizioni non valutate e valutate, metriche, "
            "matrici, modelli serializzati, storie di training e hash SHA-256 sono nella "
            "presente cartella.",
            "",
        ]
    )
    return "\n".join(lines)


def run(output_dir: Path) -> dict[str, Any]:
    config = verify_protocol()
    seed = int(config["random_seed"])
    set_determinism(seed)
    development, seq_mean, seq_std, baseline, v2_config = build_development(config)
    heldout = build_heldout_without_truth(
        config, seq_mean, seq_std, baseline, v2_config
    )
    labels = list(config["task"]["labels"])
    label_to_index = {label: index for index, label in enumerate(labels)}
    train_signature = np.stack([row["signature"] for row in development])
    test_signature = np.stack([row["signature"] for row in heldout])
    train_sequence = np.stack([row["sequence"] for row in development])
    test_sequence = np.stack([row["sequence"] for row in heldout])
    train_targets = np.asarray(
        [label_to_index[row["opaque_label"]] for row in development], dtype=np.int64
    )
    vectorizer = TfidfVectorizer(
        max_features=256,
        ngram_range=(1, 2),
        sublinear_tf=True,
        norm="l2",
        dtype=np.float32,
    )
    train_text = vectorizer.fit_transform([row["text"] for row in development]).toarray()
    test_text = vectorizer.transform([row["text"] for row in heldout]).toarray()
    if train_text.shape[1] == 0:
        raise RuntimeError("empty development TF-IDF vocabulary")

    model_dir = output_dir / "models"
    histories = {}
    training_accuracy: dict[str, float] = {}
    model_bytes: dict[str, int] = {}
    unscored: list[dict[str, Any]] = []
    train_predictions: list[dict[str, Any]] = []

    for name, model in classical_models(config).items():
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always", ConvergenceWarning)
            model.fit(train_signature, [row["opaque_label"] for row in development])
        train_scores = model.predict_proba(train_signature)
        test_scores = model.predict_proba(test_signature)
        score_labels = list(model.classes_)
        train_pred = select_predictions(train_scores, score_labels)
        test_pred = select_predictions(test_scores, score_labels)
        blob = pickle.dumps(model, protocol=5)
        write_deterministic(model_dir / f"{name}.pkl", blob)
        model_bytes[name] = len(blob)
        training_accuracy[name] = float(
            np.mean(
                [
                    prediction == row["opaque_label"]
                    for prediction, row in zip(train_pred, development, strict=True)
                ]
            )
        )
        histories[name] = {
            "model": name,
            "warnings": [str(item.message) for item in caught],
        }
        for row, prediction in zip(development, train_pred, strict=True):
            train_predictions.append(
                {
                    "model": name,
                    "development_case_id": row["case_id"],
                    "true_training_pseudolabel": row["opaque_label"],
                    "predicted_pseudolabel": prediction,
                    "correct": int(prediction == row["opaque_label"]),
                }
            )
        for row, prediction, scores in zip(heldout, test_pred, test_scores, strict=True):
            unscored.append(
                {
                    "model": name,
                    "physical_case_id": row["physical_case_id"],
                    "predicted_pseudolabel": prediction,
                    "class_scores_json": json.dumps(
                        {label: float(score) for label, score in zip(score_labels, scores)},
                        sort_keys=True,
                        separators=(",", ":"),
                    ),
                }
            )

    torch_specs = [
        (
            "lstm_causal_attention",
            LSTMAttentionClassifier(41, 32, len(labels), bidirectional=False),
            None,
            None,
        ),
        (
            "bilstm_attention",
            LSTMAttentionClassifier(41, 24, len(labels), bidirectional=True),
            None,
            None,
        ),
        (
            "multimodal_bilstm_attention_tfidf",
            MultimodalLSTMAttentionClassifier(41, 24, train_text.shape[1], len(labels)),
            train_text.astype(np.float32),
            test_text.astype(np.float32),
        ),
    ]
    for name, model, train_text_input, test_text_input in torch_specs:
        train_scores, test_scores, blob, history = train_torch_model(
            name,
            model,
            train_sequence,
            train_text_input,
            train_targets,
            test_sequence,
            test_text_input,
            config,
        )
        train_pred = select_predictions(train_scores, labels)
        test_pred = select_predictions(test_scores, labels)
        write_deterministic(model_dir / f"{name}.bin", blob)
        model_bytes[name] = len(blob)
        training_accuracy[name] = float(
            np.mean(
                [
                    prediction == row["opaque_label"]
                    for prediction, row in zip(train_pred, development, strict=True)
                ]
            )
        )
        histories[name] = history
        for row, prediction in zip(development, train_pred, strict=True):
            train_predictions.append(
                {
                    "model": name,
                    "development_case_id": row["case_id"],
                    "true_training_pseudolabel": row["opaque_label"],
                    "predicted_pseudolabel": prediction,
                    "correct": int(prediction == row["opaque_label"]),
                }
            )
        for row, prediction, scores in zip(heldout, test_pred, test_scores, strict=True):
            unscored.append(
                {
                    "model": name,
                    "physical_case_id": row["physical_case_id"],
                    "predicted_pseudolabel": prediction,
                    "class_scores_json": json.dumps(
                        {label: float(score) for label, score in zip(labels, scores)},
                        sort_keys=True,
                        separators=(",", ":"),
                    ),
                }
            )

    unscored_fields = [
        "model",
        "physical_case_id",
        "predicted_pseudolabel",
        "class_scores_json",
    ]
    write_deterministic(
        output_dir / "predictions_unscored.csv",
        csv_bytes(unscored, unscored_fields),
    )

    # Evaluator truth is deliberately loaded only after unscored predictions exist.
    truth = truth_by_case(config)
    scored = [
        {
            **row,
            "true_pseudolabel": truth[row["physical_case_id"]],
            "correct": int(
                row["predicted_pseudolabel"] == truth[row["physical_case_id"]]
            ),
        }
        for row in unscored
    ]
    scored_fields = unscored_fields + ["true_pseudolabel", "correct"]
    write_deterministic(output_dir / "predictions.csv", csv_bytes(scored, scored_fields))
    write_deterministic(
        output_dir / "training_predictions.csv",
        csv_bytes(
            train_predictions,
            [
                "model",
                "development_case_id",
                "true_training_pseudolabel",
                "predicted_pseudolabel",
                "correct",
            ],
        ),
    )
    metrics, confusion = evaluate(scored, training_accuracy, model_bytes, config)
    result = {
        "protocol_id": config["protocol_id"],
        "status": "COMPLETE",
        "interpretation": "centralized descriptive references",
        "c02b_status": "Mitigata",
        "model_order": list(MODEL_ORDER),
        "metrics": metrics,
        "comparison_anchors": {
            "shared_prototypes_local_unseen": {"correct": 36, "n": 36, "accuracy": 1.0},
            "fot_B_local_unseen": {"correct": 31, "n": 36, "accuracy": 31 / 36},
        },
        "tfidf_vocabulary_size": len(vectorizer.vocabulary_),
        "sequence_normalizer": {
            "mean": seq_mean.tolist(),
            "std": seq_std.tolist(),
        },
    }
    write_deterministic(output_dir / "metrics.json", json_bytes(result))
    write_deterministic(output_dir / "confusion_matrices.json", json_bytes(confusion))
    write_deterministic(output_dir / "training_history.json", json_bytes(histories))
    write_deterministic(
        output_dir / "tfidf_vocabulary.json",
        json_bytes({term: int(index) for term, index in vectorizer.vocabulary_.items()}),
    )
    write_deterministic(
        output_dir / "SUPERVISOR_MODEL_SUITE_REPORT.md",
        report_text(metrics, confusion, config).encode("utf-8"),
    )
    manifest_paths = [
        CONFIG_PATH,
        FREEZE_PATH,
        Path(__file__),
        output_dir / "predictions_unscored.csv",
        output_dir / "predictions.csv",
        output_dir / "training_predictions.csv",
        output_dir / "metrics.json",
        output_dir / "confusion_matrices.json",
        output_dir / "training_history.json",
        output_dir / "tfidf_vocabulary.json",
        output_dir / "SUPERVISOR_MODEL_SUITE_REPORT.md",
        *sorted(model_dir.glob("*")),
    ]
    manifest = {
        "protocol_id": config["protocol_id"],
        "status": "COMPLETE",
        "artifacts": {
            str(path.relative_to(ROOT)): sha256_file(path) for path in manifest_paths
        },
    }
    write_deterministic(output_dir / "output_hash_manifest.json", json_bytes(manifest))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    result = run(args.output_dir.resolve())
    print(f"completed {len(result['model_order'])} centralized model references")
    for name in result["model_order"]:
        metric = result["metrics"][name]["physical_cases"]
        print(f"{name}: {metric['correct']}/{metric['n']} ({metric['accuracy']:.1%})")


if __name__ == "__main__":
    main()
