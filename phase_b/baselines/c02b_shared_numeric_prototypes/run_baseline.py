#!/usr/bin/env python3
"""Run the frozen C02b shared numerical prototype baseline."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from collections import defaultdict
from pathlib import Path
import sys
from typing import Any

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
CODE = ROOT / "code"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(CODE) not in sys.path:
    sys.path.insert(0, str(CODE))

from evaluate_verbalizer_v2 import signature_vector  # noqa: E402
from tep_features import load_case, normalize_schema  # noqa: E402
from tep_verbalize_v2 import (  # noqa: E402
    load_config as load_v2_config,
    load_development_baseline,
    verbalize_case,
)


CONFIG_PATH = HERE / "protocol_config.json"
FREEZE_MANIFEST_PATH = HERE / "protocol_freeze_manifest.json"
DEFAULT_OUTPUT_DIR = HERE / "results"
HELDOUT_DIR = ROOT / "tep_heldout" / "mode1"
HELDOUT_SOURCE_MAP = (
    ROOT / "phase_b/final_evaluation/evaluator_side/heldout_source_mapping.json"
)
TRUTH_MANIFEST = ROOT / "phase_b/heldout/phase_b_heldout_manifest.csv"
MAPPING_PATH = ROOT / "phase_b/config/evaluator_side/pseudolabel_mapping.json"
FOT_RESULTS_PATH = ROOT / "phase_b/final_evaluation/evaluation_results.json"
LABEL_WIDTH = 9
ABSTAIN = "__ABSTAIN__"
ARMS = ("shared_prototypes", "local_only", "centralized_reference")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True, allow_nan=False)
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
        raise RuntimeError(f"refusing to overwrite different deterministic output: {path}")
    path.write_bytes(content)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def verify_protocol() -> dict[str, Any]:
    freeze = load_json(FREEZE_MANIFEST_PATH)
    if freeze["status"] != "FROZEN_BEFORE_BASELINE_EVALUATION":
        raise RuntimeError("protocol freeze status mismatch")
    for relative, expected in freeze["artifacts"].items():
        if sha256_file(ROOT / relative) != expected:
            raise RuntimeError(f"protocol artifact hash mismatch: {relative}")
    config = load_json(CONFIG_PATH)
    if config["status"] != "FROZEN_BEFORE_BASELINE_EVALUATION":
        raise RuntimeError("protocol config is not frozen")
    for relative, expected in config["input_hashes"].items():
        if sha256_file(ROOT / relative) != expected:
            raise RuntimeError(f"frozen input hash mismatch: {relative}")
    return config


def validate_vector(vector: np.ndarray, dimensions: int) -> np.ndarray:
    value = np.asarray(vector, dtype=np.float64)
    if value.shape != (dimensions,):
        raise RuntimeError(f"expected vector shape {(dimensions,)}, got {value.shape}")
    if not np.all(np.isfinite(value)) or np.any((value < 0.0) | (value > 1.0)):
        raise RuntimeError("vector contains a non-finite or out-of-range component")
    return value


def case_vector(
    frame: pd.DataFrame,
    baseline: Any,
    v2_config: dict[str, Any],
    dimensions: int,
) -> np.ndarray:
    structured = verbalize_case(
        frame,
        baseline,
        config=v2_config,
        start_h=10.0,
        end_h=50.0,
    )["structured"]
    return validate_vector(signature_vector(structured), dimensions)


def normal_blocks(path: Path) -> dict[str, pd.DataFrame]:
    normal = normalize_schema(pd.read_excel(path), source=str(path))
    blocks: dict[str, pd.DataFrame] = {}
    for number in range(1, 6):
        left = 50.0 * (number - 1)
        block = normal[(normal.Time >= left) & (normal.Time < left + 50.0)].copy()
        if len(block) != 3000:
            raise RuntimeError(f"Normal N{number} must contain 3000 samples")
        block["Time"] = block["Time"] - left
        blocks[f"N{number}"] = block
    return blocks


def build_development_vectors(
    config: dict[str, Any], mapping: dict[str, str]
) -> tuple[dict[str, list[np.ndarray]], list[dict[str, Any]]]:
    v2_config = load_v2_config(CODE / "verbalizer_config_v2.json")
    normal_path = CODE / "tep_cache/mode1_normal_500.xlsx"
    baseline = load_development_baseline(normal_path, v2_config)
    dimensions = int(config["representation"]["dimensions"])
    grouped: dict[str, list[np.ndarray]] = defaultdict(list)
    provenance: list[dict[str, Any]] = []

    for real_label, opaque_label in mapping.items():
        fault = int(real_label[1:])
        for batch in config["task"]["development_fault_batches"]:
            path = CODE / "tep_cache" / f"mode1_{fault}_{batch}.xlsx"
            vector = case_vector(load_case(path), baseline, v2_config, dimensions)
            grouped[opaque_label].append(vector)
            provenance.append(
                {
                    "case_id": f"{opaque_label}-B{batch}",
                    "opaque_label": opaque_label,
                    "source_path": str(path.relative_to(ROOT)),
                    "source_sha256": sha256_file(path),
                }
            )

    for block_id, frame in normal_blocks(normal_path).items():
        vector = case_vector(frame, baseline, v2_config, dimensions)
        grouped["Normal"].append(vector)
        provenance.append(
            {
                "case_id": block_id,
                "opaque_label": "Normal",
                "source_path": str(normal_path.relative_to(ROOT)),
                "source_sha256": sha256_file(normal_path),
            }
        )

    if set(grouped) != set(config["task"]["labels"]):
        raise RuntimeError("development label coverage mismatch")
    if {len(vectors) for vectors in grouped.values()} != {5}:
        raise RuntimeError("every prototype must use exactly five development cases")
    return dict(grouped), provenance


def build_prototypes(
    grouped: dict[str, list[np.ndarray]], dimensions: int
) -> dict[str, np.ndarray]:
    return {
        label: validate_vector(np.mean(np.stack(vectors), axis=0), dimensions)
        for label, vectors in grouped.items()
    }


def load_heldout_vectors(
    config: dict[str, Any], baseline: Any, v2_config: dict[str, Any]
) -> dict[str, np.ndarray]:
    source_map = load_json(HELDOUT_SOURCE_MAP)
    expected_ids = set(config["task"]["heldout_physical_case_ids"])
    if {item["physical_case_id"] for item in source_map["cases"]} != expected_ids:
        raise RuntimeError("held-out source-map case coverage mismatch")
    dimensions = int(config["representation"]["dimensions"])
    vectors: dict[str, np.ndarray] = {}
    for item in source_map["cases"]:
        path = HELDOUT_DIR / item["source_filename"]
        if sha256_file(path) != item["source_file_sha256"]:
            raise RuntimeError(f"held-out source hash mismatch: {path.name}")
        vectors[item["physical_case_id"]] = case_vector(
            load_case(path), baseline, v2_config, dimensions
        )
    return vectors


def available_labels(
    arm: str, agent: str, config: dict[str, Any]
) -> list[str]:
    local_fault = config["task"]["agent_local_fault"][agent]
    if arm == "local_only":
        return [local_fault, "Normal"]
    if arm in {"shared_prototypes", "centralized_reference"}:
        return list(config["task"]["labels"])
    raise KeyError(arm)


def classify(
    vector: np.ndarray,
    prototypes: dict[str, np.ndarray],
    labels: list[str],
    tie_tolerance: float,
) -> tuple[str | None, bool, dict[str, float]]:
    distances = {
        label: float(np.mean(np.abs(vector - prototypes[label]))) for label in labels
    }
    minimum = min(distances.values())
    tied = sorted(
        label for label, distance in distances.items() if abs(distance - minimum) <= tie_tolerance
    )
    if len(tied) != 1:
        return None, True, distances
    return tied[0], False, distances


def build_unscored_predictions(
    config: dict[str, Any],
    heldout: dict[str, np.ndarray],
    prototypes: dict[str, np.ndarray],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    tolerance = float(config["classifier"]["tie_tolerance_absolute"])
    for arm in ARMS:
        for agent in sorted(config["task"]["agent_local_fault"]):
            labels = available_labels(arm, agent, config)
            for case_id in config["task"]["heldout_physical_case_ids"]:
                predicted, abstain, distances = classify(
                    heldout[case_id], prototypes, labels, tolerance
                )
                rows.append(
                    {
                        "arm": arm,
                        "agent_id": agent,
                        "physical_case_id": case_id,
                        "predicted_pseudolabel": predicted or "",
                        "abstain": str(abstain).lower(),
                        "available_pseudolabels": "|".join(labels),
                        "distances_json": json.dumps(
                            distances, ensure_ascii=True, sort_keys=True, separators=(",", ":")
                        ),
                    }
                )
    if len(rows) != 180:
        raise RuntimeError("prediction count mismatch")
    return rows


def load_truth_after_prediction(
    config: dict[str, Any], mapping: dict[str, str]
) -> dict[str, str]:
    truth: dict[str, str] = {}
    with TRUTH_MANIFEST.open(encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream):
            real = row["class_offline"]
            truth[row["case_id"]] = "Normal" if real == "Normal" else mapping[real]
    if set(truth) != set(config["task"]["heldout_physical_case_ids"]):
        raise RuntimeError("truth case coverage mismatch")
    return truth


def scope(agent: str, truth: str, config: dict[str, Any]) -> str:
    if truth == "Normal":
        return "normal"
    if truth == config["task"]["agent_local_fault"][agent]:
        return "local_seen"
    return "local_unseen"


def score_predictions(
    unscored: list[dict[str, Any]], truth: dict[str, str], config: dict[str, Any]
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in unscored:
        actual = truth[row["physical_case_id"]]
        predicted = row["predicted_pseudolabel"]
        rows.append(
            {
                **row,
                "true_pseudolabel": actual,
                "scope": scope(row["agent_id"], actual, config),
                "correct": str(bool(predicted and predicted == actual)).lower(),
            }
        )
    return rows


def bool_field(row: dict[str, Any], key: str) -> bool:
    return row[key] is True or row[key] == "true"


def metric(rows: list[dict[str, Any]]) -> dict[str, Any]:
    correct = sum(bool_field(row, "correct") for row in rows)
    abstentions = sum(bool_field(row, "abstain") for row in rows)
    return {
        "n": len(rows),
        "correct": correct,
        "accuracy": correct / len(rows) if rows else None,
        "abstentions": abstentions,
    }


def compute_metrics(
    rows: list[dict[str, Any]], config: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    labels = list(config["task"]["labels"])
    summary: dict[str, Any] = {}
    confusion: dict[str, Any] = {}
    detailed: list[dict[str, Any]] = []
    for arm in ARMS:
        arm_rows = [row for row in rows if row["arm"] == arm]
        summary[arm] = {"overall": metric(arm_rows)}
        for name in ("local_unseen", "local_seen", "normal"):
            summary[arm][name] = metric(
                [row for row in arm_rows if row["scope"] == name]
            )
        matrix = {
            truth: {prediction: 0 for prediction in labels + [ABSTAIN]}
            for truth in labels
        }
        for row in arm_rows:
            predicted = ABSTAIN if bool_field(row, "abstain") else row["predicted_pseudolabel"]
            matrix[row["true_pseudolabel"]][predicted] += 1
        confusion[arm] = matrix

        for agent in sorted(config["task"]["agent_local_fault"]):
            for label in labels:
                selected = [
                    row
                    for row in arm_rows
                    if row["agent_id"] == agent and row["true_pseudolabel"] == label
                ]
                stats = metric(selected)
                detailed.append(
                    {
                        "arm": arm,
                        "agent_id": agent,
                        "true_pseudolabel": label,
                        "scope": scope(agent, label, config),
                        **stats,
                    }
                )
    return summary, confusion, detailed


def bootstrap_local_unseen(
    rows: list[dict[str, Any]], config: dict[str, Any]
) -> dict[str, Any]:
    unseen = [
        row
        for row in rows
        if row["arm"] == "shared_prototypes" and row["scope"] == "local_unseen"
    ]
    by_case: dict[str, list[dict[str, Any]]] = defaultdict(list)
    case_label: dict[str, str] = {}
    for row in unseen:
        by_case[row["physical_case_id"]].append(row)
        case_label[row["physical_case_id"]] = row["true_pseudolabel"]
    if len(by_case) != 12 or {len(value) for value in by_case.values()} != {3}:
        raise RuntimeError("bootstrap requires 12 physical fault cases with 3 rows each")
    strata: dict[str, list[str]] = defaultdict(list)
    for case_id, label in case_label.items():
        strata[label].append(case_id)
    if len(strata) != 4 or {len(value) for value in strata.values()} != {3}:
        raise RuntimeError("bootstrap strata mismatch")

    spec = config["metrics"]["confidence_intervals"]
    rng = np.random.default_rng(int(spec["seed"]))
    draws = np.empty(int(spec["draws"]), dtype=float)
    for index in range(len(draws)):
        sampled_rows: list[dict[str, Any]] = []
        for label in sorted(strata):
            cases = sorted(strata[label])
            for sampled in rng.choice(cases, size=len(cases), replace=True):
                sampled_rows.extend(by_case[str(sampled)])
        draws[index] = np.mean([bool_field(row, "correct") for row in sampled_rows])
    return {
        "method": spec["method"],
        "draws": len(draws),
        "seed": int(spec["seed"]),
        "confidence_level": float(spec["confidence_level"]),
        "n_physical_clusters": len(by_case),
        "n_agent_case_rows": len(unseen),
        "clusters_per_pseudolabel": {key: len(value) for key, value in sorted(strata.items())},
        "point_estimate": metric(unseen)["accuracy"],
        "ci_lower": float(np.quantile(draws, 0.025)),
        "ci_upper": float(np.quantile(draws, 0.975)),
    }


def emit_payloads(
    output_dir: Path, prototypes: dict[str, np.ndarray], config: dict[str, Any]
) -> dict[str, Any]:
    agents: dict[str, Any] = {}
    total_bytes = 0
    total_scalars = 0
    total_transmissions = 0
    for agent, local_fault in sorted(config["task"]["agent_local_fault"].items()):
        peer_labels = sorted(
            label
            for label in config["task"]["labels"]
            if label not in {local_fault, "Normal"}
        )
        payload = bytearray()
        for label in peer_labels:
            encoded = label.encode("ascii")
            if len(encoded) != LABEL_WIDTH:
                raise RuntimeError("opaque label does not have frozen 9-byte width")
            payload.extend(encoded)
            payload.extend(np.asarray(prototypes[label], dtype="<f8").tobytes(order="C"))
        path = output_dir / "payloads" / f"{agent}.bin"
        write_deterministic(path, bytes(payload))
        try:
            reported_path = str(path.relative_to(ROOT))
        except ValueError:
            reported_path = str(path)
        agents[agent] = {
            "peer_pseudolabels": peer_labels,
            "prototype_transmissions": len(peer_labels),
            "scalar_values": len(peer_labels) * len(next(iter(prototypes.values()))),
            "payload_path": reported_path,
            "payload_bytes": path.stat().st_size,
            "payload_sha256": sha256_file(path),
        }
        total_bytes += path.stat().st_size
        total_scalars += agents[agent]["scalar_values"]
        total_transmissions += len(peer_labels)
    return {
        "unique_fault_prototypes": 4,
        "unique_normal_prototypes": 1,
        "prototype_dimensions": len(next(iter(prototypes.values()))),
        "delivery": agents,
        "total_peer_fault_prototype_transmissions": total_transmissions,
        "total_transmitted_scalar_values": total_scalars,
        "total_payload_bytes": total_bytes,
        "transport_framing_included": False,
    }


def fot_comparison(metrics: dict[str, Any]) -> dict[str, Any]:
    frozen = load_json(FOT_RESULTS_PATH)
    baseline = metrics["shared_prototypes"]["local_unseen"]["accuracy"]
    conditions = {}
    for condition in ("A", "B", "E"):
        value = frozen["condition_metrics"][condition]["unseen"]["accuracy"]
        conditions[condition] = {
            "accuracy": value,
            "shared_numeric_minus_condition": baseline - value,
            "n": frozen["condition_metrics"][condition]["unseen"]["n"],
        }
    return {
        "scope": "same 36 local-unseen agent-case observations from 12 physical fault cases",
        "point_estimates_only": True,
        "source_path": str(FOT_RESULTS_PATH.relative_to(ROOT)),
        "source_sha256": sha256_file(FOT_RESULTS_PATH),
        "conditions": conditions,
    }


def format_accuracy(item: dict[str, Any]) -> str:
    return f"{item['correct']}/{item['n']} ({item['accuracy']:.1%})"


def report_text(
    metrics: dict[str, Any],
    confusion: dict[str, Any],
    bootstrap: dict[str, Any],
    payload: dict[str, Any],
    comparison: dict[str, Any],
    detailed: list[dict[str, Any]],
) -> str:
    lines = [
        "# C02b — baseline numerica con prototipi condivisi, ispirata a FedProto",
        "",
        "## Esito",
        "",
        "La baseline numerica equa è stata completata sullo stesso compito di FoT. "
        "Lo stato di C02b passa da **Aperta** a **Mitigata**: esiste ora un confronto "
        "esterno diretto, ma non una suite sufficiente di algoritmi federati originali "
        "per dichiarare la critica risolta sperimentalmente.",
        "",
        "## Protocollo in breve",
        "",
        "Ogni classe è riassunta dalla media di cinque vettori development a 697 "
        "componenti, estratti prima della verbalizzazione. Ogni agente conserva i "
        "prototipi Normal e del proprio fault e riceve i tre prototipi fault dei peer. "
        "La predizione è il prototipo a minima distanza L1 media. Il classificatore "
        "usa soltanto pseudolabel opache; la verità PBH viene unita dopo avere scritto "
        "le predizioni non valutate.",
        "",
        "## Metriche",
        "",
        "| Braccio | Complessiva | Local-seen | Local-unseen | Normal |",
        "|---|---:|---:|---:|---:|",
    ]
    for arm in ARMS:
        item = metrics[arm]
        lines.append(
            f"| `{arm}` | {format_accuracy(item['overall'])} | "
            f"{format_accuracy(item['local_seen'])} | "
            f"{format_accuracy(item['local_unseen'])} | "
            f"{format_accuracy(item['normal'])} |"
        )
    lines.extend(
        [
            "",
            f"Per la metrica primaria, l'intervallo bootstrap al 95% è "
            f"[{bootstrap['ci_lower']:.1%}, {bootstrap['ci_upper']:.1%}]. Il bootstrap "
            f"ricampiona {bootstrap['n_physical_clusters']} casi fisici, stratificati "
            "per fault; le tre viste local-unseen dello stesso caso restano unite.",
            "",
            "## Confronto diretto con A, B ed E",
            "",
            "| Metodo | Accuratezza local-unseen | Differenza baseline numerica − metodo |",
            "|---|---:|---:|",
        ]
    )
    baseline_acc = metrics["shared_prototypes"]["local_unseen"]["accuracy"]
    lines.append(f"| Prototipi condivisi | {baseline_acc:.1%} | — |")
    for condition in ("A", "B", "E"):
        item = comparison["conditions"][condition]
        lines.append(
            f"| FoT {condition} | {item['accuracy']:.1%} | "
            f"{item['shared_numeric_minus_condition']:+.1%} |"
        )
    lines.extend(
        [
            "",
            "Le differenze sono descrittive e appaiate sullo stesso held-out, ma qui "
            "non sono presentate come test di superiorità. A è un information floor "
            "senza conoscenza peer; E corrompe le associazioni testuali; B è il confronto "
            "FoT pertinente. Il riferimento centralizzato coincide matematicamente con "
            "il braccio condiviso perché entrambi usano gli stessi cinque centroidi; "
            "la differenza è dove vengono costruiti e trasferiti.",
            "",
            "## Risultato per fault e agente — braccio condiviso",
            "",
            "| Agente | Fault/pseudolabel | Ambito | Risultato |",
            "|---|---|---|---:|",
        ]
    )
    for row in detailed:
        if row["arm"] != "shared_prototypes" or row["true_pseudolabel"] == "Normal":
            continue
        lines.append(
            f"| `{row['agent_id']}` | `{row['true_pseudolabel']}` | "
            f"{row['scope']} | {row['correct']}/{row['n']} ({row['accuracy']:.1%}) |"
        )
    labels = ["CLS-ZOGAA", "CLS-OJNSG", "CLS-R463B", "CLS-Z3ISU", "Normal"]
    matrix = confusion["shared_prototypes"]
    lines.extend(
        [
            "",
            "## Matrice di confusione — braccio condiviso",
            "",
            "Le righe sono le pseudolabel vere; le colonne sono le predizioni. Ogni "
            "fault compare 12 volte perché i tre casi fisici sono valutati da quattro "
            "agenti; questa duplicazione non viene trattata come indipendenza statistica.",
            "",
            "| Vera \\ Predetta | CLS-ZOGAA | CLS-OJNSG | CLS-R463B | CLS-Z3ISU | Normal | Astensione |",
            "|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for truth_label in labels:
        row = matrix[truth_label]
        lines.append(
            f"| `{truth_label}` | {row['CLS-ZOGAA']} | {row['CLS-OJNSG']} | "
            f"{row['CLS-R463B']} | {row['CLS-Z3ISU']} | {row['Normal']} | "
            f"{row[ABSTAIN]} |"
        )
    per_agent = payload["delivery"]
    one = next(iter(per_agent.values()))
    lines.extend(
        [
            "",
            "## Comunicazione",
            "",
            f"Ogni agente riceve {one['prototype_transmissions']} prototipi, "
            f"{one['scalar_values']} scalari e {one['payload_bytes']} byte effettivi. "
            f"Nel sistema sono trasmesse {payload['total_peer_fault_prototype_transmissions']} "
            f"copie di prototipo, {payload['total_transmitted_scalar_values']} scalari e "
            f"{payload['total_payload_bytes']} byte. I byte includono pseudolabel e float64 "
            "nel formato congelato, ma non il framing di rete.",
            "",
            "## Limiti",
            "",
            "- È nearest-prototype su feature frozen, non l'algoritmo FedProto originale.",
            "- Il vettore a 697 componenti eredita soglie e scelte del verbalizzatore V2; "
            "non misura il vantaggio del testo rispetto a tutte le possibili feature numeriche.",
            "- Cinque casi development per classe e tre casi held-out per fault danno "
            "incertezza ampia; le 36 viste agente-caso non sono indipendenti.",
            "- Il riferimento centralizzato non è un upper bound garantito e non è un "
            "confronto federato separato: è un controllo di equivalenza dei centroidi.",
            "- PCA+SVM centralizzata e FedAvg non sono stati eseguiti perché, senza un "
            "nuovo protocollo di output class-disjoint, cambierebbero il compito o non "
            "renderebbero predicibili le pseudoclassi mai viste localmente.",
            "",
            "## Artefatti",
            "",
            "Configurazione, freeze, codice, prototipi, predizioni non valutate e "
            "valutate, matrici di confusione, dettaglio agente×fault, payload binari, "
            "bootstrap e manifest SHA-256 sono nella presente cartella.",
            "",
        ]
    )
    return "\n".join(lines)


def run(output_dir: Path) -> dict[str, Any]:
    config = verify_protocol()
    mapping_doc = load_json(MAPPING_PATH)
    mapping = mapping_doc["real_to_opaque"]
    dimensions = int(config["representation"]["dimensions"])

    grouped, development_provenance = build_development_vectors(config, mapping)
    prototypes = build_prototypes(grouped, dimensions)

    v2_config = load_v2_config(CODE / "verbalizer_config_v2.json")
    baseline = load_development_baseline(CODE / "tep_cache/mode1_normal_500.xlsx", v2_config)
    heldout = load_heldout_vectors(config, baseline, v2_config)
    unscored = build_unscored_predictions(config, heldout, prototypes)

    unscored_fields = [
        "arm", "agent_id", "physical_case_id", "predicted_pseudolabel",
        "abstain", "available_pseudolabels", "distances_json",
    ]
    write_deterministic(
        output_dir / "predictions_unscored.csv", csv_bytes(unscored, unscored_fields)
    )

    # The evaluator-side truth is deliberately loaded only after predictions exist.
    truth = load_truth_after_prediction(config, mapping)
    scored = score_predictions(unscored, truth, config)
    scored_fields = unscored_fields + ["true_pseudolabel", "scope", "correct"]
    write_deterministic(output_dir / "predictions.csv", csv_bytes(scored, scored_fields))

    metrics, confusion, detailed = compute_metrics(scored, config)
    bootstrap = bootstrap_local_unseen(scored, config)
    payload = emit_payloads(output_dir, prototypes, config)
    comparison = fot_comparison(metrics)

    prototype_doc = {
        "method": config["method_name"],
        "dimensions": dimensions,
        "cases_per_prototype": 5,
        "development_provenance": development_provenance,
        "prototypes": {label: vector.tolist() for label, vector in sorted(prototypes.items())},
    }
    result_doc = {
        "protocol_id": config["protocol_id"],
        "method_name": config["method_name"],
        "evaluation_status": "COMPLETE",
        "c02b_status": "MITIGATA",
        "statistical_unit": "physical_case_id",
        "metrics": metrics,
        "bootstrap": bootstrap,
        "comparison_with_fot_A_B_E": comparison,
        "communication": payload,
    }
    write_deterministic(output_dir / "prototypes.json", json_bytes(prototype_doc))
    write_deterministic(output_dir / "metrics.json", json_bytes(result_doc))
    write_deterministic(output_dir / "confusion_matrices.json", json_bytes(confusion))
    write_deterministic(output_dir / "bootstrap_results.json", json_bytes(bootstrap))
    write_deterministic(output_dir / "payload_manifest.json", json_bytes(payload))
    write_deterministic(
        output_dir / "per_agent_fault_metrics.csv",
        csv_bytes(
            detailed,
            [
                "arm", "agent_id", "true_pseudolabel", "scope", "n",
                "correct", "accuracy", "abstentions",
            ],
        ),
    )
    write_deterministic(
        output_dir / "C02B_BASELINE_REPORT.md",
        report_text(metrics, confusion, bootstrap, payload, comparison, detailed).encode("utf-8"),
    )

    manifest_paths = [
        CONFIG_PATH,
        FREEZE_MANIFEST_PATH,
        Path(__file__),
        output_dir / "predictions_unscored.csv",
        output_dir / "predictions.csv",
        output_dir / "prototypes.json",
        output_dir / "metrics.json",
        output_dir / "confusion_matrices.json",
        output_dir / "bootstrap_results.json",
        output_dir / "payload_manifest.json",
        output_dir / "per_agent_fault_metrics.csv",
        output_dir / "C02B_BASELINE_REPORT.md",
        *sorted((output_dir / "payloads").glob("*.bin")),
    ]
    hash_manifest = {
        "protocol_id": config["protocol_id"],
        "status": "COMPLETE_DETERMINISTIC_OUTPUTS",
        "artifacts": {
            str(path.relative_to(ROOT)): sha256_file(path) for path in manifest_paths
        },
    }
    write_deterministic(output_dir / "output_hash_manifest.json", json_bytes(hash_manifest))
    return result_doc


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    result = run(args.output_dir.resolve())
    primary = result["metrics"]["shared_prototypes"]["local_unseen"]
    print(
        f"C02b baseline complete: {primary['correct']}/{primary['n']} "
        f"({primary['accuracy']:.6f}) local-unseen; status={result['c02b_status']}"
    )


if __name__ == "__main__":
    main()
