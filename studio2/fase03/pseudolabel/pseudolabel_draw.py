#!/usr/bin/env python3
"""Sotto-fase 03.7 — pseudolabel opache, assegnazione fault↔agente e derangement di E.

Implementa alla lettera `SPECIFICA_PSEUDOLABEL.md` (stessa cartella), scritta prima
dell'esecuzione:

  §2  guardia sul catalogo D1 (SHA-256 e lista dei fault al tag);
  §3  nove label: SHA-256 di "NAMESPACE|label|<identifier>|<counter>", base32, 5 caratteri,
      prefisso S2-CLS-; rifiuto per collisione o per guardia di opacità; Normal letterale;
      label_space = otto label in ordine lessicografico + Normal;
  §4  assegnazione: fault ordinati per SHA-256 di "NAMESPACE|assignment|<identifier>",
      il k-esimo è il fault locale di agent_k;
  §5  derangement: per agente, indice uniforme fra i 1854 derangement dei 7 peer
      (ordine lessicografico delle permutazioni) tramite rejection sampling su parole
      a 32 bit da SHA-256 di "NAMESPACE|SEED|derangement|<agent_id>|<i>".

Il pattern digest+base32 riprende, riscrivendolo, `derive_opaque_pseudolabel` di
`phase_b/config/protocol.py` (commit c431cd8, riga di provenienza in studio2/PROVENIENZA.md).
Nessun import da phase_b/, nessuna chiamata a modelli, nessuna simulazione, nessun
input casuale del sistema.

Uso (dalla radice del repository):
  python3 -m studio2.fase03.pseudolabel.pseudolabel_draw            # scrive i quattro artefatti
  python3 -m studio2.fase03.pseudolabel.pseudolabel_draw --check    # replay byte-identico
  python3 -m studio2.fase03.pseudolabel.pseudolabel_draw --freeze <commit>  # PSEUDOLABEL_FREEZE.json
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import itertools
import json
from pathlib import Path
import re
import sys
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CATALOG_PATH = ROOT / "studio2/fase03/selection/CATALOG_FREEZE.json"

NAMESPACE = "studio2-fase03-pseudolabel-v1"
SEED = 20260913
PREFIX = "S2-CLS-"
SUFFIX_LENGTH = 5
NORMAL_LABEL = "Normal"
PSEUDOLABEL = re.compile(r"^S2-CLS-[A-Z0-9]{5}$")  # identica a protocol.PSEUDOLABEL
AGENT_IDS = tuple(f"agent_{index}" for index in range(1, 9))  # identica a protocol.AGENT_IDS
PEERS_PER_AGENT = 7
SUBFACTORIAL_7 = 1854

CATALOG_TAG = "studio2-fase03-catalogo-D1-frozen-001"
CATALOG_COMMIT = "ab43f0b20f45cdb475c0caf52c6f7afcbae50891"
CATALOG_SHA256 = "68b8461a6382c93e1a5dd8dc6c9def66b26b2ec865f0bc0786dd88fa95acedda"
CATALOG_IDVS = [1, 2, 3, 8, 10, 13, 14, 15]
CATALOG_IDENTIFIERS = ["F1", "F2", "F3", "F8", "F10", "F13", "F14", "F15"]

ARTIFACTS = {
    "map": "PSEUDOLABEL_MAP.json",
    "assignment": "AGENT_ASSIGNMENT.json",
    "derangements": "CONDITION_E_DERANGEMENTS.json",
    "log": "DRAW_LOG.json",
}
FREEZE_FILE = "PSEUDOLABEL_FREEZE.json"
CODE_FILES = ("pseudolabel_draw.py", "test_pseudolabel.py")
PROPOSED_FREEZE_TAG = "studio2-fase03-pseudolabel-frozen-001"


class CatalogMismatch(RuntimeError):
    """Il catalogo su disco non è quello congelato al tag D1."""


class DrawError(RuntimeError):
    """Violazione di un invariante della specifica durante la generazione."""


# --------------------------------------------------------------------------- utilità

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def serialize(value: Any) -> bytes:
    """Serializzazione unica per tutti gli artefatti (§6)."""
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


# --------------------------------------------------------------------------- §2 catalogo

def load_catalog(path: Path = CATALOG_PATH) -> dict[str, Any]:
    raw = path.read_bytes()
    digest = sha256_bytes(raw)
    if digest != CATALOG_SHA256:
        raise CatalogMismatch(f"CATALOG_FREEZE.json sha256 {digest} != frozen {CATALOG_SHA256}")
    catalog = json.loads(raw.decode("utf-8"))
    if catalog.get("catalog") != CATALOG_IDVS:
        raise CatalogMismatch(f"catalog list {catalog.get('catalog')} != {CATALOG_IDVS}")
    faults = catalog.get("faults", [])
    identifiers = [entry.get("label") for entry in faults]
    idvs = [entry.get("idv") for entry in faults]
    if identifiers != CATALOG_IDENTIFIERS or idvs != CATALOG_IDVS:
        raise CatalogMismatch("catalog fault labels/idv differ from the frozen D1 catalog")
    return catalog


# --------------------------------------------------------------------------- §3 label

def label_message(identifier: str, counter: int, namespace: str = NAMESPACE) -> str:
    return f"{namespace}|label|{identifier}|{counter}"


def candidate_suffix(message: str) -> tuple[str, str]:
    digest = hashlib.sha256(message.encode("utf-8")).digest()
    suffix = base64.b32encode(digest).decode("ascii").rstrip("=")[:SUFFIX_LENGTH]
    return digest.hex(), suffix


def derive_labels(faults: list[dict[str, Any]], namespace: str = NAMESPACE) -> tuple[dict[str, str], dict[str, int], list[dict[str, Any]]]:
    labels: dict[str, str] = {}
    counters: dict[str, int] = {}
    attempts: list[dict[str, Any]] = []
    taken: set[str] = set()
    for entry in faults:  # ordine di elaborazione: quello del catalogo (idv crescente)
        identifier, idv = entry["label"], int(entry["idv"])
        counter = 0
        while True:
            message = label_message(identifier, counter, namespace)
            digest_hex, suffix = candidate_suffix(message)
            reasons = []
            if suffix in taken:
                reasons.append("collision")
            if str(idv) in suffix:
                reasons.append("opacity_guard_idv_digits")
            record = {
                "identifier": identifier,
                "counter": counter,
                "message": message,
                "sha256": digest_hex,
                "suffix": suffix,
                "accepted": not reasons,
                "rejection_reasons": reasons,
            }
            attempts.append(record)
            if not reasons:
                break
            counter += 1
        label = PREFIX + suffix
        if not PSEUDOLABEL.fullmatch(label):
            raise DrawError(f"derived label {label!r} does not match the protocol regex")
        labels[identifier] = label
        counters[identifier] = counter
        taken.add(suffix)
    if len(set(labels.values())) != len(faults):
        raise DrawError("derived labels are not unique")
    return labels, counters, attempts


def build_label_space(labels: dict[str, str]) -> list[str]:
    return sorted(labels.values()) + [NORMAL_LABEL]


# --------------------------------------------------------------------------- §4 assegnazione

def assignment_key(identifier: str, namespace: str = NAMESPACE) -> str:
    return hashlib.sha256(f"{namespace}|assignment|{identifier}".encode("utf-8")).hexdigest()


def assign_agents(faults: list[dict[str, Any]], labels: dict[str, str], namespace: str = NAMESPACE) -> tuple[dict[str, dict[str, Any]], list[dict[str, str]]]:
    keyed = [(assignment_key(entry["label"], namespace), entry) for entry in faults]
    if len({key for key, _ in keyed}) != len(keyed):
        raise DrawError("assignment keys collide")
    ordered = sorted(keyed, key=lambda item: item[0])
    if len(ordered) != len(AGENT_IDS):
        raise DrawError("catalog size must equal the number of agents")
    assignment: dict[str, dict[str, Any]] = {}
    keys_log: list[dict[str, str]] = []
    for agent_id, (key, entry) in zip(AGENT_IDS, ordered):
        assignment[agent_id] = {
            "identifier": entry["label"],
            "idv": int(entry["idv"]),
            "local_fault_label": labels[entry["label"]],
        }
        keys_log.append({"identifier": entry["label"], "assignment_sha256": key, "agent_id": agent_id})
    owned = [value["local_fault_label"] for value in assignment.values()]
    if sorted(owned) != sorted(labels.values()):
        raise DrawError("assignment is not a bijection onto the eight fault labels")
    return assignment, keys_log


# --------------------------------------------------------------------------- §5 derangement

def enumerate_derangements(n: int = PEERS_PER_AGENT) -> list[tuple[int, ...]]:
    """Tutti i derangement di (0..n-1) in ordine lessicografico della tupla."""
    return [perm for perm in itertools.permutations(range(n)) if all(perm[i] != i for i in range(n))]


def derangement_word(agent_id: str, draw_index: int, namespace: str = NAMESPACE, seed: int = SEED) -> tuple[str, int]:
    message = f"{namespace}|{seed}|derangement|{agent_id}|{draw_index}"
    digest = hashlib.sha256(message.encode("utf-8")).digest()
    return message, int.from_bytes(digest[:4], "big")


def sample_derangements(assignment: dict[str, dict[str, Any]], label_space: list[str], namespace: str = NAMESPACE, seed: int = SEED) -> tuple[dict[str, dict[str, str]], dict[str, Any]]:
    table = enumerate_derangements()
    if len(table) != SUBFACTORIAL_7:
        raise DrawError(f"expected {SUBFACTORIAL_7} derangements, enumerated {len(table)}")
    limit = 2**32 - (2**32 % SUBFACTORIAL_7)
    fault_labels = label_space[:-1]
    derangements: dict[str, dict[str, str]] = {}
    log: dict[str, Any] = {"derangement_count": SUBFACTORIAL_7, "acceptance_limit": limit, "agents": {}}
    for agent_id in AGENT_IDS:
        local = assignment[agent_id]["local_fault_label"]
        peers = [label for label in fault_labels if label != local]
        if len(peers) != PEERS_PER_AGENT:
            raise DrawError(f"{agent_id} must have exactly seven peers")
        draws = []
        draw_index = 0
        while True:
            message, word = derangement_word(agent_id, draw_index, namespace, seed)
            accepted = word < limit
            draws.append({"draw_index": draw_index, "message": message, "word": word, "accepted": accepted})
            if accepted:
                break
            draw_index += 1
        index = word % SUBFACTORIAL_7
        perm = table[index]
        mapping = {peers[j]: peers[perm[j]] for j in range(PEERS_PER_AGENT)}
        _check_derangement(agent_id, mapping, peers, local)
        derangements[agent_id] = mapping
        log["agents"][agent_id] = {
            "local_fault_label": local,
            "peers_in_label_space_order": peers,
            "draws": draws,
            "rejections": draw_index,
            "selected_index": index,
            "permutation": list(perm),
        }
    return derangements, log


def _check_derangement(agent_id: str, mapping: dict[str, str], peers: list[str], local: str) -> None:
    if set(mapping) != set(peers) or set(mapping.values()) != set(peers):
        raise DrawError(f"{agent_id} derangement domain/codomain must be its seven peers")
    if any(source == target for source, target in mapping.items()):
        raise DrawError(f"{agent_id} derangement contains a fixed point")
    if local in mapping or local in mapping.values():
        raise DrawError(f"{agent_id} derangement must not touch the local label")


# --------------------------------------------------------------------------- generazione

def generate(namespace: str = NAMESPACE, seed: int = SEED, catalog_path: Path = CATALOG_PATH) -> dict[str, bytes]:
    """Restituisce i quattro artefatti serializzati, senza toccare il disco."""
    catalog = load_catalog(catalog_path)
    faults = catalog["faults"]
    labels, counters, attempts = derive_labels(faults, namespace)
    label_space = build_label_space(labels)
    assignment, keys_log = assign_agents(faults, labels, namespace)
    derangements, derangement_log = sample_derangements(assignment, label_space, namespace, seed)
    reverse = {label: identifier for identifier, label in labels.items()}

    pseudolabel_map = {
        "schema_version": 1,
        "scope": "EVALUATOR_SIDE_ONLY_never_in_prompts",
        "namespace": namespace,
        "catalog_tag": CATALOG_TAG,
        "catalog_sha256": CATALOG_SHA256,
        "label_by_identifier": {**labels, NORMAL_LABEL: NORMAL_LABEL},
        "idv_by_identifier": {entry["label"]: int(entry["idv"]) for entry in faults},
        "label_space": label_space,
        "label_space_order": "eight opaque labels sorted lexicographically (ASCII), then Normal",
        "unknown": "not a label: abstain=true, predicted_label=null (D10)",
    }
    agent_assignment = {
        "schema_version": 1,
        "scope": "EVALUATOR_SIDE_ONLY_never_in_prompts",
        "namespace": namespace,
        "rule": "faults sorted by sha256(namespace|assignment|identifier); k-th fault is local to agent_k",
        "assignment": assignment,
        "agents": {agent_id: {"local_fault_label": value["local_fault_label"]} for agent_id, value in assignment.items()},
    }
    condition_e = {
        "schema_version": 1,
        "scope": "EVALUATOR_SIDE_ONLY_never_in_prompts",
        "namespace": namespace,
        "seed": seed,
        "method": "uniform derangement of each agent's seven peers (rejection sampling over the 1854 derangements, SHA-256 word stream)",
        "derangements": derangements,
        "derangements_by_identifier": {
            agent_id: {reverse[source]: reverse[target] for source, target in mapping.items()}
            for agent_id, mapping in derangements.items()
        },
    }
    draw_log = {
        "schema_version": 1,
        "specification": "studio2/fase03/pseudolabel/SPECIFICA_PSEUDOLABEL.md",
        "namespace": namespace,
        "seed": seed,
        "prefix": PREFIX,
        "suffix_length": SUFFIX_LENGTH,
        "catalog": {
            "path": str(catalog_path.relative_to(ROOT)),
            "tag": CATALOG_TAG,
            "commit": CATALOG_COMMIT,
            "sha256": CATALOG_SHA256,
            "idvs": CATALOG_IDVS,
        },
        "processing_order": [entry["label"] for entry in faults],
        "order_of_operations": ["catalog_guard", "labels", "label_space", "assignment", "derangements"],
        "label_attempts": attempts,
        "label_counters": counters,
        "assignment_keys": keys_log,
        "derangement_rejections": {agent_id: value["rejections"] for agent_id, value in derangement_log["agents"].items()},
        "derangements": derangement_log,
    }
    return {
        ARTIFACTS["map"]: serialize(pseudolabel_map),
        ARTIFACTS["assignment"]: serialize(agent_assignment),
        ARTIFACTS["derangements"]: serialize(condition_e),
        ARTIFACTS["log"]: serialize(draw_log),
    }


def write_artifacts(out_dir: Path = HERE) -> list[Path]:
    written = []
    for name, payload in generate().items():
        path = out_dir / name
        path.write_bytes(payload)
        written.append(path)
    return written


def check_replay(out_dir: Path = HERE) -> list[str]:
    """Rigenera in memoria e confronta byte per byte; restituisce l'elenco dei mismatch."""
    mismatches = []
    for name, payload in generate().items():
        path = out_dir / name
        if not path.exists():
            mismatches.append(f"{name}: missing")
        elif path.read_bytes() != payload:
            mismatches.append(f"{name}: bytes differ")
    return mismatches


def build_freeze(source_commit: str, out_dir: Path = HERE) -> dict[str, Any]:
    if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise ValueError("source_commit must be a full lowercase Git object ID")
    mismatches = check_replay(out_dir)
    if mismatches:
        raise DrawError(f"replay mismatch, refusing to freeze: {mismatches}")
    files = []
    for name in list(ARTIFACTS.values()) + list(CODE_FILES) + ["SPECIFICA_PSEUDOLABEL.md"]:
        path = out_dir / name
        files.append({"path": str(path.relative_to(ROOT)), "sha256": sha256_file(path), "bytes": path.stat().st_size})
    return {
        "schema_version": 1,
        "date": "2026-09-13",
        "scope": "phase03_subphase_03_7_pseudolabels_agent_assignment_condition_E_derangements",
        "status": "frozen_pending_independent_verification",
        "proposed_freeze_tag": PROPOSED_FREEZE_TAG,
        "tag_conditions": [
            "independent verification OK recorded in VERIFICA_PSEUDOLABEL.md",
            "source_commit reachable from origin/main",
            "python3 -m studio2.fase03.pseudolabel.pseudolabel_draw --check passes at the tagged commit",
        ],
        "namespace": NAMESPACE,
        "seed": SEED,
        "source_commit": source_commit,
        "catalog_tag": CATALOG_TAG,
        "catalog_commit": CATALOG_COMMIT,
        "catalog_sha256": CATALOG_SHA256,
        "files": files,
        "interface_note": "if 03.12 changes the pseudolabel format, regenerate deterministically under namespace studio2-fase03-pseudolabel-v2 in new files; never overwrite v1",
        "model_calls": 0,
        "simulations": 0,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="replay in memoria e confronto byte per byte")
    parser.add_argument("--freeze", metavar="COMMIT", help="scrive PSEUDOLABEL_FREEZE.json con il commit sorgente")
    parser.add_argument("--out-dir", type=Path, default=HERE)
    args = parser.parse_args(argv)
    if args.check:
        mismatches = check_replay(args.out_dir)
        if mismatches:
            print("REPLAY MISMATCH:\n  " + "\n  ".join(mismatches))
            return 1
        print(f"replay OK: {len(ARTIFACTS)} artefatti byte-identici in {args.out_dir}")
        return 0
    if args.freeze:
        freeze = build_freeze(args.freeze, args.out_dir)
        (args.out_dir / FREEZE_FILE).write_bytes(serialize(freeze))
        print(f"written {args.out_dir / FREEZE_FILE}")
        return 0
    for path in write_artifacts(args.out_dir):
        print(f"written {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
