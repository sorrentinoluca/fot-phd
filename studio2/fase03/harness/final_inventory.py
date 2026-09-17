"""Deterministic logical inventory and execution schedule for the final batch.

Normative source: ``PROTOCOLLO_FINALE_CANDIDATE.md`` §4 (blocks), §5 (counts) and
§7.1 (stable identifier, three passes, one ``PCG64(20260913)`` generator).

The inventory is *logical*: it enumerates the stable identifiers of the 2,244 unique
prompts and nothing else.  Prompt bytes are produced later, at materialization, by the
frozen renderer of §2 from the 03.11 test lot; this module never renders a prompt and
never reads case evidence.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

from .common import HarnessError, canonical_json, load_json, sha256_text


ROOT = Path(__file__).resolve().parents[1]

# --- frozen design constants (§1, §4) --------------------------------------------
FAULTS = ("F1", "F2", "F3", "F8", "F10", "F13", "F14", "F15")
PRIMARY_RUNS = 8
NORMAL_RUNS = 8
OOD_FAULTS = ("F4", "F5")
OOD_RUNS = 3
SWAP_FAULTS = ("F1", "F8", "F10", "F13")
ABLATION_UNSEEN_FAULTS = ("F1", "F2", "F14", "F15")
ABLATION_UNSEEN_RUNS = 3
AGENTS = tuple(f"agent_{index}" for index in range(1, 9))
CONDITIONS = ("A", "B-LF", "E-LF")
ABLATION_CONDITION = "B-noLF"
REPETITIONS = (1, 2, 3)

# --- blocks and library roles (§4) -----------------------------------------------
BLOCK_NUCLEUS = "nucleus"
BLOCK_SWAP = "producer_swap"
BLOCK_ABLATION = "ablation_b_no_lf"
BLOCK_OOD = "ood"
BLOCKS = (BLOCK_NUCLEUS, BLOCK_SWAP, BLOCK_ABLATION, BLOCK_OOD)
LIBRARY_NONE = "none"
LIBRARY_PRIMARY = "G_P"
LIBRARY_ALTERNATE = "G_A"

# --- schedule (§7.1) -------------------------------------------------------------
SCHEDULE_NAMESPACE = "studio2-fase03-final-order-v1"
SCHEDULE_SEED = 20260913

# --- independent counts (§5) -----------------------------------------------------
EXPECTED_UNIQUE = {BLOCK_NUCLEUS: 1728, BLOCK_SWAP: 224, BLOCK_ABLATION: 148, BLOCK_OOD: 144}
EXPECTED_UNIQUE_TOTAL = 2244
EXPECTED_REQUESTS = {BLOCK_NUCLEUS: 5184, BLOCK_SWAP: 672, BLOCK_ABLATION: 444, BLOCK_OOD: 432}
EXPECTED_REQUESTS_TOTAL = 6732

ID_FIELDS = ("block", "condition", "case_id", "recipient_agent", "library_role")

ASSIGNMENT_PATH = ROOT / "pseudolabel" / "AGENT_ASSIGNMENT.json"
PSEUDOLABEL_MAP_PATH = ROOT / "pseudolabel" / "PSEUDOLABEL_MAP.json"
PSEUDOLABEL_FREEZE_PATH = ROOT / "pseudolabel" / "PSEUDOLABEL_FREEZE.json"
TEST_LOT_SEAL_SHA256 = "9bd02e900429e971c08cbb8fc81f5dec54b8dcfb30b90e19faf622bb8558739d"


def stable_id(entry: dict[str, Any]) -> str:
    missing = [field for field in ID_FIELDS if not isinstance(entry.get(field), str) or not entry[field]]
    if missing:
        raise HarnessError(f"stable identifier is incomplete: {missing}")
    parts = [entry[field] for field in ID_FIELDS]
    if any("|" in part for part in parts):
        raise HarnessError("stable identifier fields must not contain the separator")
    return "|".join(parts)


def sort_key(entry: dict[str, Any]) -> tuple[str, ...]:
    """Lexicographic order over the canonical tuple of §7.1."""
    return tuple(entry[field] for field in ID_FIELDS)


def _frozen_pseudolabel_sources() -> tuple[dict[str, Any], dict[str, Any]]:
    """Read the agent assignment and label map under their own freeze hashes."""
    from .common import sha256_file

    freeze = load_json(PSEUDOLABEL_FREEZE_PATH)
    expected = {Path(row["path"]).name: row["sha256"] for row in freeze["files"]}
    for path in (ASSIGNMENT_PATH, PSEUDOLABEL_MAP_PATH):
        declared = expected.get(path.name)
        if declared is not None and sha256_file(path) != declared:
            raise HarnessError(f"frozen pseudolabel source changed: {path.name}")
    return load_json(ASSIGNMENT_PATH), load_json(PSEUDOLABEL_MAP_PATH)


def owner_by_fault() -> dict[str, str]:
    assignment, _ = _frozen_pseudolabel_sources()
    owners = {row["identifier"]: agent for agent, row in assignment["assignment"].items()}
    if set(owners) != set(FAULTS) or len(owners) != 8:
        raise HarnessError("agent assignment does not cover the eight catalogue faults exactly once")
    return owners


def _label_by_fault() -> dict[str, str]:
    _, mapping = _frozen_pseudolabel_sources()
    return dict(mapping["label_by_identifier"])


def primary_case_id(fault: str, run: int) -> str:
    return f"test-primary-{fault}-r{run:02d}"


def ood_case_id(fault: str, run: int) -> str:
    return f"test-ood-{fault}-r{run:02d}"


def _entry(*, block, condition, case_id, recipient_agent, library_role,
           fault, run_index, locality, true_pseudolabel):
    value = {
        "block": block,
        "condition": condition,
        "case_id": case_id,
        "recipient_agent": recipient_agent,
        "library_role": library_role,
        "fault": fault,
        "run_index": run_index,
        "locality": locality,
        "true_pseudolabel": true_pseudolabel,
        "out_of_label_space": true_pseudolabel is None,
    }
    value["stable_id"] = stable_id(value)
    return value


def build_inventory() -> list[dict[str, Any]]:
    """Enumerate the 2,244 unique prompts of §4 in lexicographic stable-ID order."""
    owners = owner_by_fault()
    labels = _label_by_fault()
    rows: list[dict[str, Any]] = []

    # Nucleus — local-unseen and local-seen (§4 rows 1 and 2).
    for fault in FAULTS:
        owner = owners[fault]
        for run in range(1, PRIMARY_RUNS + 1):
            case_id = primary_case_id(fault, run)
            for agent in AGENTS:
                locality = "local-seen" if agent == owner else "local-unseen"
                for condition in CONDITIONS:
                    rows.append(_entry(
                        block=BLOCK_NUCLEUS, condition=condition, case_id=case_id,
                        recipient_agent=agent,
                        library_role=LIBRARY_NONE if condition == "A" else LIBRARY_PRIMARY,
                        fault=fault, run_index=run, locality=locality,
                        true_pseudolabel=labels[fault]))

    # Nucleus — Normal (§4 row 3).
    for run in range(1, NORMAL_RUNS + 1):
        case_id = primary_case_id("Normal", run)
        for agent in AGENTS:
            for condition in CONDITIONS:
                rows.append(_entry(
                    block=BLOCK_NUCLEUS, condition=condition, case_id=case_id,
                    recipient_agent=agent,
                    library_role=LIBRARY_NONE if condition == "A" else LIBRARY_PRIMARY,
                    fault="Normal", run_index=run, locality="normal",
                    true_pseudolabel=labels["Normal"]))

    # Producer-swap — B-LF only, alternate library, locally-unseen recipients (§4 row 4).
    for fault in SWAP_FAULTS:
        owner = owners[fault]
        for run in range(1, PRIMARY_RUNS + 1):
            case_id = primary_case_id(fault, run)
            for agent in AGENTS:
                if agent == owner:
                    continue
                rows.append(_entry(
                    block=BLOCK_SWAP, condition="B-LF", case_id=case_id,
                    recipient_agent=agent, library_role=LIBRARY_ALTERNATE,
                    fault=fault, run_index=run, locality="local-unseen",
                    true_pseudolabel=labels[fault]))

    # Ablation B-without-local-first (§4 row 5).
    for fault in FAULTS:
        owner = owners[fault]
        for run in range(1, PRIMARY_RUNS + 1):
            rows.append(_entry(
                block=BLOCK_ABLATION, condition=ABLATION_CONDITION,
                case_id=primary_case_id(fault, run), recipient_agent=owner,
                library_role=LIBRARY_PRIMARY, fault=fault, run_index=run,
                locality="local-seen", true_pseudolabel=labels[fault]))
    for fault in ABLATION_UNSEEN_FAULTS:
        owner = owners[fault]
        for run in range(1, ABLATION_UNSEEN_RUNS + 1):
            case_id = primary_case_id(fault, run)
            for agent in AGENTS:
                if agent == owner:
                    continue
                rows.append(_entry(
                    block=BLOCK_ABLATION, condition=ABLATION_CONDITION, case_id=case_id,
                    recipient_agent=agent, library_role=LIBRARY_PRIMARY,
                    fault=fault, run_index=run, locality="local-unseen",
                    true_pseudolabel=labels[fault]))

    # OOD probe (§4 row 6): no agent owns F4/F5, so all eight recipients are unseen.
    for fault in OOD_FAULTS:
        for run in range(1, OOD_RUNS + 1):
            case_id = ood_case_id(fault, run)
            for agent in AGENTS:
                for condition in CONDITIONS:
                    rows.append(_entry(
                        block=BLOCK_OOD, condition=condition, case_id=case_id,
                        recipient_agent=agent,
                        library_role=LIBRARY_NONE if condition == "A" else LIBRARY_PRIMARY,
                        fault=fault, run_index=run, locality="ood",
                        true_pseudolabel=None))

    rows.sort(key=sort_key)
    verify_counts(rows)
    identifiers = {row["stable_id"] for row in rows}
    if len(identifiers) != len(rows):
        raise HarnessError("stable identifiers are not unique")
    return rows


def verify_counts(rows: Iterable[dict[str, Any]]) -> dict[str, Any]:
    """Independent check of the per-block counts against protocol §5."""
    from collections import Counter

    values = list(rows)
    unique = Counter(row["block"] for row in values)
    if dict(unique) != EXPECTED_UNIQUE or len(values) != EXPECTED_UNIQUE_TOTAL:
        raise HarnessError(f"block counts differ from protocol §5: {dict(unique)}")
    requests = {block: count * len(REPETITIONS) for block, count in unique.items()}
    if requests != EXPECTED_REQUESTS or sum(requests.values()) != EXPECTED_REQUESTS_TOTAL:
        raise HarnessError(f"request counts differ from protocol §5: {requests}")
    return {"unique_by_block": dict(unique), "requests_by_block": requests,
            "unique_total": len(values), "requests_total": sum(requests.values())}


def paired_be_cells(rows: Iterable[dict[str, Any]]) -> dict[str, int]:
    """B-LF and E-LF must pair exactly on (block, case, recipient, library).

    Only the blocks that carry both arms are paired: the producer-swap is descriptive
    and has no symmetric E arm (§4), and the ablation has no E arm either.
    """
    from collections import Counter

    values = list(rows)
    paired_blocks = {row["block"] for row in values if row["condition"] == "E-LF"}
    keys = Counter()
    for row in values:
        if row["block"] in paired_blocks and row["condition"] in {"B-LF", "E-LF"}:
            keys[(row["block"], row["case_id"], row["recipient_agent"], row["library_role"],
                  row["condition"])] += 1
    unbalanced = []
    cells = {(block, case, agent, library)
             for block, case, agent, library, _ in keys}
    for cell in cells:
        left = keys.get((*cell, "B-LF"), 0)
        right = keys.get((*cell, "E-LF"), 0)
        if left != right:
            unbalanced.append(cell)
    if unbalanced:
        raise HarnessError(f"B-LF/E-LF cells are not paired: {len(unbalanced)}")
    return {"paired_cells": len(cells), "paired_blocks": sorted(paired_blocks)}


def build_schedule(inventory: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Three passes, one generator, as prescribed by §7.1.

    A single ``numpy.random.Generator(PCG64(20260913))`` is created once and, for
    repetitions 1, 2 and 3 in this order, produces the permutation of the inventory
    previously sorted lexicographically by stable identifier.
    """
    import numpy

    base = sorted(inventory, key=sort_key)
    if len(base) != EXPECTED_UNIQUE_TOTAL:
        raise HarnessError("schedule requires the complete unique inventory")
    generator = numpy.random.Generator(numpy.random.PCG64(SCHEDULE_SEED))
    schedule: list[dict[str, Any]] = []
    position = 0
    for repetition in REPETITIONS:
        order = generator.permutation(len(base))
        for index in order:
            row = base[int(index)]
            position += 1
            schedule.append({
                "position": position,
                "repetition": repetition,
                "stable_id": row["stable_id"],
                "logical_id": f"{row['stable_id']}|r{repetition}",
                **{field: row[field] for field in ID_FIELDS},
                "fault": row["fault"],
                "run_index": row["run_index"],
                "locality": row["locality"],
                "true_pseudolabel": row["true_pseudolabel"],
            })
    if len(schedule) != EXPECTED_REQUESTS_TOTAL:
        raise HarnessError("schedule length differs from the planned request total")
    if len({row["logical_id"] for row in schedule}) != len(schedule):
        raise HarnessError("schedule logical identifiers are not unique")
    return schedule


def inventory_artifact(inventory: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "artifact_version": "FINAL_INVENTORY_7_4_1",
        "status": "LOGICAL_INVENTORY_NOT_MATERIALIZED",
        "scope": "stable identifiers only; prompt bytes are rendered at materialization",
        "protocol_reference": "PROTOCOLLO_FINALE_CANDIDATE.md e0db132 §4, §5, §7.1",
        "test_lot_seal_sha256": TEST_LOT_SEAL_SHA256,
        "identifier_fields": list(ID_FIELDS),
        "counts": verify_counts(inventory),
        "be_pairing": paired_be_cells(inventory),
        "entries": inventory,
    }


def schedule_artifact(schedule: list[dict[str, Any]], *, inventory_sha256: str) -> dict[str, Any]:
    import numpy

    return {
        "artifact_version": "FINAL_SCHEDULE_7_4_1",
        "status": "SCHEDULE_CANDIDATE_NOT_AUTHENTICATED",
        "namespace": SCHEDULE_NAMESPACE,
        "seed": SCHEDULE_SEED,
        "bit_generator": "numpy.random.PCG64",
        "permutation_call": "Generator.permutation(n) over the index range, once per repetition, 1 -> 2 -> 3",
        "numpy_version": numpy.__version__,
        "inventory_sha256": inventory_sha256,
        "requests_total": len(schedule),
        "entries": schedule,
    }


def artifact_sha256(artifact: dict[str, Any]) -> str:
    return sha256_text(canonical_json(artifact))
