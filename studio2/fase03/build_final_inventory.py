#!/usr/bin/env python3
"""Build and verify the logical inventory and the execution schedule of the final batch.

Offline and idempotent: no model call, no materialization, no ledger access.  Running it
twice produces byte-identical artifacts, so the recorded SHA-256 values are reproducible
by an independent reviewer from this commit alone.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from studio2.fase03.harness import final_inventory as inventory_module  # noqa: E402
from studio2.fase03.harness.common import canonical_json, sha256_text  # noqa: E402
from studio2.fase03.harness.runtime import durable_write  # noqa: E402

LIBRARIES_PATH = ROOT / "studio2/fase03/librerie/LIBRERIE_FINALI_CANDIDATE.json"
DEFAULT_OUT = ROOT / "studio2/fase03/batch_finale/build"
SUMMARY_PATH = ROOT / "studio2/fase03/batch_finale/INVENTARIO_SCHEDULE_7_4.json"


LIBRARY_ROOTS: list[Path] = []


def _library_rows(role: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    from studio2.fase03.harness.common import load_json
    from studio2.fase03.harness.final_prompts import resolve_library_path

    candidate = load_json(LIBRARIES_PATH)
    entry = candidate["producers"][role]
    payload = load_json(resolve_library_path(entry, roots=LIBRARY_ROOTS))
    return payload["library"], entry


def be_structural_diff() -> dict[str, Any]:
    """Re-run the §3.3 check: B-LF -> E-LF changes only ``pseudolabel``."""
    from studio2.fase03.protocol import peer_insights
    from studio2.fase03.harness.common import load_json

    assignment = load_json(inventory_module.ASSIGNMENT_PATH)
    derangements = load_json(inventory_module.ROOT / "pseudolabel" / "CONDITION_E_DERANGEMENTS.json")["derangements"]
    label_map = load_json(inventory_module.PSEUDOLABEL_MAP_PATH)
    agents = assignment["agents"]
    results = {}
    for role in ("122B", "27B"):
        try:
            library, entry = _library_rows(role)
        except Exception as exc:  # pragma: no cover - reported, never silently skipped
            results[role] = {"status": "NOT_AVAILABLE", "reason": str(exc)}
            continue
        # The library was validated upstream by 7.2-R; here only the B->E delta matters.
        from studio2.fase03.protocol import Insight
        rows = [Insight(**{key: (tuple(value) if key == "variable_ids" else value)
                           for key, value in item.items()}) for item in library]
        compared = 0
        changed_fields: set[str] = set()
        for agent_id, agent in agents.items():
            before = peer_insights(rows, agent_id=agent_id, local_label=agent["local_fault_label"],
                                   condition="B-LF", derangements=derangements)
            after = peer_insights(rows, agent_id=agent_id, local_label=agent["local_fault_label"],
                                  condition="E-LF", derangements=derangements)
            for left, right in zip(before, after):
                left_row, right_row = left.to_dict(), right.to_dict()
                changed_fields |= {key for key in left_row if left_row[key] != right_row[key]}
                compared += 1
        results[role] = {
            "status": "PASS" if changed_fields == {"pseudolabel"} and compared == 112 else "FAIL",
            "records_compared": compared,
            "changed_fields": sorted(changed_fields),
            "library_canonical_sha256": entry["library_canonical_sha256"],
        }
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT,
                        help="directory receiving the full inventory and schedule artifacts")
    parser.add_argument("--write-summary", action="store_true",
                        help="also refresh the committed summary next to the generator")
    parser.add_argument("--libraries-root", type=Path, action="append", default=[],
                        help="directory holding the accepted insight libraries when the "
                             "path recorded in LIBRERIE_FINALI_CANDIDATE.json is not portable")
    parser.add_argument("--skip-library-check", action="store_true",
                        help="skip the B->E structural re-check when the runtime libraries are unreachable")
    arguments = parser.parse_args()

    LIBRARY_ROOTS.extend(arguments.libraries_root)
    inventory = inventory_module.build_inventory()
    schedule = inventory_module.build_schedule(inventory)
    inventory_artifact = inventory_module.inventory_artifact(inventory)
    inventory_sha256 = inventory_module.artifact_sha256(inventory_artifact)
    schedule_artifact = inventory_module.schedule_artifact(schedule, inventory_sha256=inventory_sha256)
    schedule_sha256 = inventory_module.artifact_sha256(schedule_artifact)

    out = arguments.out_dir
    durable_write(out / "INVENTARIO_FINALE_7_4.json", canonical_json(inventory_artifact) + "\n")
    durable_write(out / "SCHEDULE_FINALE_7_4.json", canonical_json(schedule_artifact) + "\n")

    diff = {"status": "SKIPPED"} if arguments.skip_library_check else be_structural_diff()
    summary = {
        "artifact_version": "INVENTARIO_SCHEDULE_7_4_1",
        "status": "CANDIDATE_NOT_AUTHENTICATED",
        "generator": "studio2/fase03/build_final_inventory.py",
        "module": "studio2/fase03/harness/final_inventory.py",
        "protocol_reference": "PROTOCOLLO_FINALE_CANDIDATE.md e0db132",
        "counts": inventory_artifact["counts"],
        "be_pairing": inventory_artifact["be_pairing"],
        "be_structural_diff": diff,
        "identifier_fields": list(inventory_module.ID_FIELDS),
        "schedule": {
            "namespace": inventory_module.SCHEDULE_NAMESPACE,
            "seed": inventory_module.SCHEDULE_SEED,
            "bit_generator": schedule_artifact["bit_generator"],
            "permutation_call": schedule_artifact["permutation_call"],
            "numpy_version": schedule_artifact["numpy_version"],
            "requests_total": schedule_artifact["requests_total"],
        },
        "inventory_sha256": inventory_sha256,
        "schedule_sha256": schedule_sha256,
        "first_scheduled_logical_id": schedule[0]["logical_id"],
        "last_scheduled_logical_id": schedule[-1]["logical_id"],
    }
    text = json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if arguments.write_summary:
        durable_write(SUMMARY_PATH, text)
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
