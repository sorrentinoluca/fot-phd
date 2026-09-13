#!/usr/bin/env python3
"""Esecuzione deterministica di D1 (studio 2, Fase 03, §6.1).

Implementa alla lettera la procedura §5 del registro congelato
docs/lit_review/DECISIONE_CRITERI_SELEZIONE_FAULT_STUDIO2.md (revisione 1,
tag studio2-fase03-criteri-selezione-frozen-001, commit 9faecaf):

  1. enumerare le combinazioni crescenti di quattro ID fra gli undici non di
     continuità;
  2. aggiungere la continuità, filtrare con i vincoli §4, ordinare le quadruple
     ammissibili lessicograficamente come tuple di interi;
  3. rejection sampling deterministico su SHA-256: per c = 0, 1, ... digest dei
     byte UTF-8 di "studio2-fase03-D1-v1|20260913|c", intero unsigned
     big-endian x, L = 2**256 - (2**256 % N), accettare il primo x < L,
     indice = x % N;
  4. registrare lista ordinata, N, seed, contatore accettato, digest, indice,
     catalogo, conteggi, commit e hash dei criteri.

Snapshot eseguito originariamente: execution_snapshot/draw_d1.py.
Questo file è la revisione per replay verificato; non riscrive il log originario.

Uso:
  python3 draw_d1.py --enumerate-only        # solo passi 1-2, nessun digest
  python3 draw_d1.py --out /tmp/D1_DRAW_LOG_replay.json  # passi 1-4, scrive il record

Nessun input casuale del sistema, nessun hash() del linguaggio, nessuna
dipendenza esterna. Un replay riproduce byte per byte lo stesso record
(il campo `generated_at` è escluso dal record per mantenerlo riproducibile;
la data e il commit del contesto originale sono parametri espliciti, vincolati
all’estrazione registrata; HEAD corrente può avanzare senza alterare il record).
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import subprocess
import sys
from pathlib import Path

# --- Costanti prespecificate dal registro (rev. 1) -------------------------

NAMESPACE = "studio2-fase03-D1-v1"
SEED = "20260913"
CONTINUITY = (1, 8, 10, 13)
UNIVERSE = tuple(range(1, 16))  # IDV(1)..IDV(15), tabella 8 di Downs & Vogel 1993
HARD_STRATUM = frozenset({3, 9, 15})  # H, difficoltà di rilevazione documentata

# Tabella 8 (Downs & Vogel 1993, p. 250) trascritta nel registro §2.
FAULTS = {
    1: ("rapporto A/C, B costante, flusso 4", "step", "ratio_ac_s4"),
    2: ("composizione B, A/C costante, flusso 4", "step", "composition_b_s4"),
    3: ("temperatura alimentazione D, flusso 2", "step", "temperature_d_s2"),
    4: ("temperatura ingresso acqua reattore", "step", "temperature_cw_reactor"),
    5: ("temperatura ingresso acqua condensatore", "step", "temperature_cw_condenser"),
    6: ("perdita alimentazione A, flusso 1", "step", "feed_a_loss_s1"),
    7: ("pressione/disponibilità alimentazione C, flusso 4", "step", "header_c_pressure_s4"),
    8: ("composizione A/B/C, flusso 4", "random variation", "composition_abc_s4"),
    9: ("temperatura alimentazione D, flusso 2", "random variation", "temperature_d_s2"),
    10: ("temperatura alimentazione C, flusso 4", "random variation", "temperature_c_s4"),
    11: ("temperatura ingresso acqua reattore", "random variation", "temperature_cw_reactor"),
    12: ("temperatura ingresso acqua condensatore", "random variation", "temperature_cw_condenser"),
    13: ("cinetica di reazione", "slow drift", "reaction_kinetics"),
    14: ("valvola acqua reattore", "sticking valve", "valve_cw_reactor"),
    15: ("valvola acqua condensatore", "sticking valve", "valve_cw_condenser"),
}

# Vincoli §4 (tutti congiunti).
MIN_COVERAGE = {"step": 2, "random variation": 2, "sticking valve": 2, "slow drift": 1}
MIN_HARD = 2

DRAW_CONTEXT_COMMIT = "9faecaf7337e5864b7a3ad44cadb8971853dd260"
CRITERIA_TAG = "studio2-fase03-criteri-selezione-frozen-001"
MANIFEST_PATH = "studio2/fase03/selection/CRITERIA_FREEZE.json"
MANIFEST_SHA256_EXPECTED = "ecae57172d6a83d8b0943f5a9f47b49a3966b96e2fb47f807a9ff61449755c9b"

CRITERIA_PATH = "docs/lit_review/DECISIONE_CRITERI_SELEZIONE_FAULT_STUDIO2.md"
CRITERIA_SHA256_EXPECTED = "d58a7606d69a560a626da44833c065ddbf1aa395ae8b2e523262daf8622231c7"


def mechanism_counts(catalog):
    counts = {m: 0 for m in ("step", "random variation", "slow drift", "sticking valve")}
    for f in catalog:
        counts[FAULTS[f][1]] += 1
    return counts


def admissible(catalog):
    """Applica §4.1–§4.4 e restituisce (bool, motivi di scarto)."""
    reasons = []
    if len(set(catalog)) != 8 or not set(CONTINUITY) <= set(catalog):
        reasons.append("4.1 otto ID distinti con continuità")
    counts = mechanism_counts(catalog)
    for mech, minimum in MIN_COVERAGE.items():
        if counts[mech] < minimum:
            reasons.append(f"4.2 copertura {mech} < {minimum}")
    keys = [FAULTS[f][2] for f in catalog]
    if len(set(keys)) != len(keys):
        reasons.append("4.3 chiave di identità duplicata")
    if len(HARD_STRATUM & set(catalog)) < MIN_HARD:
        reasons.append("4.4 meno di 2 membri di H")
    return (not reasons), reasons


def enumerate_admissible():
    pool = [f for f in UNIVERSE if f not in CONTINUITY]
    assert len(pool) == 11
    total = 0
    admitted = []
    for quad in itertools.combinations(pool, 4):  # combinazioni crescenti
        total += 1
        catalog = tuple(sorted(CONTINUITY + quad))
        ok, _ = admissible(catalog)
        if ok:
            admitted.append(quad)
    # Ordinamento lessicografico come tuple di interi (§5.2).
    admitted_sorted = sorted(admitted)
    # Controllo: itertools.combinations su un pool crescente è già lessicografico.
    assert admitted_sorted == admitted
    return total, admitted_sorted


def draw_index(n):
    """Rejection sampling §5.3. Restituisce (contatore accettato, digest, x, indice, rifiutati)."""
    if n <= 0:
        raise SystemExit("N=0: arresto prima di qualsiasi hash (registro §4/§5).")
    two256 = 1 << 256
    limit = two256 - (two256 % n)
    rejected = []
    c = 0
    while True:
        msg = f"{NAMESPACE}|{SEED}|{c}".encode("utf-8")
        digest = hashlib.sha256(msg).hexdigest()
        x = int.from_bytes(bytes.fromhex(digest), "big")
        if x < limit:
            return c, digest, x, x % n, rejected
        rejected.append({"counter": c, "message": msg.decode("ascii"), "sha256": digest})
        c += 1


def sha256_file(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_frozen_context(repo: Path, context_commit: str, date: str):
    """Verifica il contesto prima di enumerare o calcolare digest del sorteggio."""
    if context_commit != DRAW_CONTEXT_COMMIT or date != "2026-09-13":
        raise SystemExit("Replay limitato al contesto e alla data dell'estrazione D1 registrata.")

    def git(*args):
        return subprocess.check_output(["git", "-C", str(repo), *args], stderr=subprocess.PIPE)

    try:
        if git("cat-file", "-t", CRITERIA_TAG).decode().strip() != "tag":
            raise ValueError("tag dei criteri non annotato")
        if git("rev-parse", CRITERIA_TAG + "^{}").decode().strip() != context_commit:
            raise ValueError("tag dei criteri su commit inatteso")
        git("merge-base", "--is-ancestor", context_commit, "HEAD")
        manifest_bytes = (repo / MANIFEST_PATH).read_bytes()
        if hashlib.sha256(manifest_bytes).hexdigest() != MANIFEST_SHA256_EXPECTED:
            raise ValueError("manifest originale dei criteri alterato")
        if git("show", context_commit + ":" + MANIFEST_PATH) != manifest_bytes:
            raise ValueError("manifest non corrispondente al tag")
        manifest = json.loads(manifest_bytes)
        for row in manifest["files"]:
            # Il piano vivo è una fonte storica, non un file congelato per sempre.
            snapshot = git("show", manifest["source_commit"] + ":" + row["path"])
            if len(snapshot) != row["bytes"] or hashlib.sha256(snapshot).hexdigest() != row["sha256"]:
                raise ValueError("snapshot della fonte diverso dall'impronta congelata")
        criteria_sha = sha256_file(repo / CRITERIA_PATH)
        if criteria_sha != CRITERIA_SHA256_EXPECTED:
            raise ValueError("registro dei criteri diverso da quello congelato")
    except (OSError, subprocess.CalledProcessError, ValueError, KeyError) as exc:
        raise SystemExit(f"Contesto dei criteri non valido: {exc}") from exc
    return criteria_sha


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--enumerate-only", action="store_true", help="solo passi 1-2, nessun digest")
    ap.add_argument("--out", type=Path, default=None, help="file JSON del record (passo 4)")
    ap.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[3])
    ap.add_argument("--date", default="2026-09-13", help="data operativa dell'estrazione")
    ap.add_argument("--draw-context-commit", default=DRAW_CONTEXT_COMMIT,
                    help="commit storico dell'estrazione, non HEAD corrente; validato contro il tag dei criteri")
    args = ap.parse_args()
    criteria_sha = validate_frozen_context(args.repo, args.draw_context_commit, args.date)

    total, admitted = enumerate_admissible()
    compositions = {}
    for quad in admitted:
        c = mechanism_counts(tuple(sorted(CONTINUITY + quad)))
        key = f"step={c['step']},random={c['random variation']},drift={c['slow drift']},sticking={c['sticking valve']}"
        compositions[key] = compositions.get(key, 0) + 1

    print(f"quadruple candidate: {total}  ammissibili (N): {len(admitted)}")
    for i, quad in enumerate(admitted):
        cat = tuple(sorted(CONTINUITY + quad))
        print(f"  [{i:2d}] nuovi={quad}  catalogo={cat}  H={sorted(HARD_STRATUM & set(cat))}")
    print("composizioni:", compositions)

    if args.enumerate_only:
        return 0

    n = len(admitted)
    counter, digest, x, index, rejected = draw_index(n)
    quad = admitted[index]
    catalog = tuple(sorted(CONTINUITY + quad))

    record = {
        "schema_version": 1,
        "scope": "phase03_D1_draw_execution",
        "date": args.date,
        "procedure_source": {
            "path": CRITERIA_PATH,
            "sha256": criteria_sha,
            "section": "5",
            "freeze_tag": "studio2-fase03-criteri-selezione-frozen-001",
            "freeze_commit": "9faecaf7337e5864b7a3ad44cadb8971853dd260",
        },
        "worktree_head_at_draw": args.draw_context_commit,
        "universe": list(UNIVERSE),
        "continuity": list(CONTINUITY),
        "hard_stratum_H": sorted(HARD_STRATUM),
        "constraints": {
            "distinct_ids": 8,
            "min_coverage": MIN_COVERAGE,
            "forbidden_identity_pairs": [[3, 9], [4, 11], [5, 12]],
            "min_H_members": MIN_HARD,
        },
        "candidate_quadruples": total,
        "N_admissible": n,
        "ordering": "lexicographic on the 4-tuple of new IDs as integers (ascending)",
        "admissible_ordered": [
            {"index": i, "new": list(q), "catalog": sorted(CONTINUITY + q)} for i, q in enumerate(admitted)
        ],
        "mechanism_compositions": compositions,
        "sampling": {
            "method": "rejection sampling on SHA-256, unsigned big-endian, L = 2**256 - (2**256 mod N)",
            "namespace": NAMESPACE,
            "seed": SEED,
            "message_format": f"{NAMESPACE}|{SEED}|<c>",
            "rejected": rejected,
            "accepted_counter": counter,
            "accepted_message": f"{NAMESPACE}|{SEED}|{counter}",
            "accepted_sha256": digest,
            "accepted_x_mod_N": index,
            "selected_index": index,
        },
        "result": {
            "new_faults": list(quad),
            "catalog": list(catalog),
            "mechanism_counts": mechanism_counts(catalog),
            "H_members": sorted(HARD_STRATUM & set(catalog)),
        },
        "single_draw": True,
        "reruns": 0,
        "model_calls": 0,
        "per_fault_results_opened": False,
    }
    text = json.dumps(record, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        canonical_log = Path(__file__).resolve().parent / "D1_DRAW_LOG.json"
        if args.out.resolve() == canonical_log.resolve():
            raise SystemExit("Il log originale si conserva: scrivere il replay in un percorso distinto.")
        args.out.write_text(text, encoding="utf-8")
        print(f"record scritto in {args.out}")
    print(f"accettato c={counter}  rifiutati={len(rejected)}  indice={index}")
    print(f"nuovi={quad}  catalogo={catalog}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
